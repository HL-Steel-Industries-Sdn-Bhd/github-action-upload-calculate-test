import os
import gspread
import pandas as pd
from io import BytesIO
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_creds = None
_client = None
_drive = None

def _get_creds():
    global _creds
    if _creds is None:
        sa_path = os.environ.get("GOOGLE_SA_JSON", "/tmp/sa.json")
        _creds = Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    return _creds

def get_client():
    global _client
    if _client is None:
        _client = gspread.authorize(_get_creds())
    return _client

def get_drive():
    global _drive
    if _drive is None:
        _drive = build("drive", "v3", credentials=_get_creds())
    return _drive

def open_ss(ss_id):
    return get_client().open_by_key(ss_id)

def ensure_sheet(ss, name, rows=1000, cols=30):
    try:
        return ss.worksheet(name)
    except gspread.WorksheetNotFound:
        return ss.add_worksheet(title=name, rows=rows, cols=cols)

def export_xlsx(ss_id, log=print):
    """Drive API 一次性导出整个 Google Sheet 为 XLSX（含所有 tab）"""
    drive = get_drive()
    try:
        request = drive.files().export_media(
            fileId=ss_id,
            mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        buf = BytesIO()
        downloader = MediaIoBaseDownload(buf, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        buf.seek(0)
        log(f"  ✓ 导出 {ss_id[:12]}... 成功，{buf.getbuffer().nbytes / 1024:.1f} KB")
        return buf
    except Exception as e:
        log(f"  ✗ 导出 {ss_id[:12]}... 失败: {e}")
        return None

def read_xlsx_sheets(buf):
    """读 XLSX 返回 {sheet_name: [[row], [row], ...]}，NaN 转 ''"""
    xls = pd.ExcelFile(buf, engine="openpyxl")
    result = {}
    for name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=name, header=None, dtype=object)
        df = df.fillna("")
        result[name] = df.values.tolist()
    return result
