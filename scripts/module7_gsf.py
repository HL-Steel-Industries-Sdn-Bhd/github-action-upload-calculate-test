from sheets_client import export_xlsx, read_xlsx_sheets
from config import GSF_ID, COL_B_SO, COL_C_ITEM, COL_P_CP_2DEC, COL_Q_CP_INT

def run(rows, color_marks, log):
    log("[module7] 导出 GSF...")
    buf = export_xlsx(GSF_ID, log)
    if buf is None:
        log("[module7] GSF 导出失败，跳过")
        return

    sheets_data = read_xlsx_sheets(buf)
    # GSF 的 sheet 名可能不叫 Sheet1，取第一个
    first_sheet_name = list(sheets_data.keys())[0]
    data = sheets_data[first_sheet_name]

    gsf_map = {}
    for r in data[1:]:
        r = list(r) + [""] * (4 - len(r))
        source = str(r[1] or "").strip()
        so = str(r[2] or "").strip()
        item = str(r[3] or "").strip()
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
            cm[15] = "purple"
            cm[16] = "purple"
            row[COL_P_CP_2DEC] = 0
            row[COL_Q_CP_INT] = 0
        elif source == "Internal":
            cm[15] = "purple"
            cm[16] = "purple"
            row[COL_P_CP_2DEC] = p + 20
            row[COL_Q_CP_INT] = q + 20

        color_marks[idx] = cm

    log("[module7] GSF 调整完成")
