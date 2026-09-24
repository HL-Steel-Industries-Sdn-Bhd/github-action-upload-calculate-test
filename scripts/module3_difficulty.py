from sheets_client import open_ss, read_all
from config import GSC_ID, COL_I_JOB, COL_E_DIFFICULTY

def run(rows, log):
    ss = open_ss(GSC_ID)
    ws = ss.get_worksheet(0)
    data = read_all(ws)

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

    log(f"[module3] 难度写入完成")
