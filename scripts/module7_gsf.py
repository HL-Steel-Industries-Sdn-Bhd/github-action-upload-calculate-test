from sheets_client import open_ss, read_all
from config import GSF_ID, COL_B_SO, COL_C_ITEM, COL_P_CP_2DEC, COL_Q_CP_INT

def run(rows, color_marks, log):
    ss = open_ss(GSF_ID)
    ws = ss.worksheet("Sheet1")
    data = read_all(ws)

    gsf_map = {}
    for r in data[1:]:
        r = list(r) + [""] * (4 - len(r))
        source = (r[1] or "").strip()
        so = (r[2] or "").strip()
        item = (r[3] or "").strip()
        if so and item and source:
            gsf_map[f"{so}___{item}"] = source

    for idx, row in enumerate(rows):
        so = str(row[COL_B_SO] or "").strip()
        item = str(row[COL_C_ITEM] or "").strip()
        key = f"{so}___{item}"
        source = gsf_map.get(key)
        if not source:
            continue

        cm = color_marks[idx]
        p = float(row[COL_P_CP_2DEC] or 0)
        q = float(row[COL_Q_CP_INT] or 0)

        if source == "External":
            cm[15] = "purple"; cm[16] = "purple"
            row[COL_P_CP_2DEC] = 0
            row[COL_Q_CP_INT] = 0
        elif source == "Internal":
            cm[15] = "purple"; cm[16] = "purple"
            row[COL_P_CP_2DEC] = p + 20
            row[COL_Q_CP_INT] = q + 20

        color_marks[idx] = cm

    log(f"[module7] GSF 调整完成")
