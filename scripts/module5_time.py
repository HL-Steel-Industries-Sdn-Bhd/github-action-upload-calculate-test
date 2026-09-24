from datetime import datetime
from sheets_client import export_xlsx, read_xlsx_sheets
from config import (GSC_ID, COL_I_JOB, COL_G_RECV_TIME,
                    COL_J_COMP_TIME, COL_L_INTERVAL, COL_M_EFFECTIVE)

def _to_dt(v):
    if isinstance(v, datetime):
        return v
    if not v:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S",
                "%m/%d/%Y %H:%M:%S", "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(str(v).strip(), fmt)
        except ValueError:
            continue
    return None

def run(rows, color_marks, log):
    log("[module5] 导出 GSC 最小间隔表...")
    buf = export_xlsx(GSC_ID, log)
    if buf is None:
        log("[module5] GSC 导出失败，跳过")
        return

    sheets_data = read_xlsx_sheets(buf)
    first_sheet_name = list(sheets_data.keys())[0]
    data = sheets_data[first_sheet_name]

    min_interval_map = {}
    for r in data[1:]:
        r = list(r) + [""] * (3 - len(r))
        job = r[0]
        try:
            t = float(r[2])
        except (ValueError, TypeError):
            continue
        if job:
            min_interval_map[job] = t

    for idx, row in enumerate(rows):
        job = row[COL_I_JOB]
        recv_t = _to_dt(row[COL_G_RECV_TIME])
        comp_t = _to_dt(row[COL_J_COMP_TIME])
        cm = color_marks[idx]

        if recv_t and comp_t:
            interval = round((comp_t - recv_t).total_seconds() / 60, 3)
            row[COL_L_INTERVAL] = interval
            min_req = min_interval_map.get(job, 0)
            result = 1 if interval >= min_req else 0
            row[COL_M_EFFECTIVE] = result
            if result == 0:
                cm[COL_L_INTERVAL] = "yellow"
                cm[COL_M_EFFECTIVE] = "yellow"
                cm[15] = "yellow"
                cm[16] = "yellow"
        else:
            row[COL_M_EFFECTIVE] = 1

        color_marks[idx] = cm

    log("[module5] 时间间隔写入完成")
