from sheets_client import export_xlsx, read_xlsx_sheets
from config import GSC_ID, COL_I_JOB, COL_E_DIFFICULTY

def run(rows, log):
    log("[module3] 导出 GSC 难度表...")
    buf = export_xlsx(GSC_ID, log)
    if buf is None:
        log("[module3] GSC 导出失败，跳过")
        return

    sheets_data = read_xlsx_sheets(buf)
    first_sheet_name = list(sheets_data.keys())[0]
    data = sheets_data[first_sheet_name]

    job_map = {}
    for r in data[1:]:
        r = list(r) + [""] * (2 - len(r))
        job = r[0]
        diff = r[1]
        if job:
            job_map[job] = diff

    for row in rows:
        job = row[COL_I_JOB]
        if not job:
            row[COL_E_DIFFICULTY] = 1
        else:
            row[COL_E_DIFFICULTY] = job_map.get(job, "")

    log("[module3] 难度写入完成")
