import os
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

_client = None

def get_client():
    global _client
    if _client is not None:
        return _client
    sa_path = os.environ.get("GOOGLE_SA_JSON", "/tmp/sa.json")
    creds = Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    _client = gspread.authorize(creds)
    return _client

def open_ss(ss_id):
    return get_client().open_by_key(ss_id)

def ensure_sheet(ss, name, rows=1000, cols=30):
    try:
        return ss.worksheet(name)
    except gspread.WorksheetNotFound:
        return ss.add_worksheet(title=name, rows=rows, cols=cols)

def read_all(sheet):
    return sheet.get_all_values()
