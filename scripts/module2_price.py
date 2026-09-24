from sheets_client import export_xlsx, read_xlsx_sheets
from config import GSD_ID, COL_B_SO, COL_C_ITEM, COL_D_PRICE

def run(rows, color_marks, log):
    log("[module2] 导出 GSD 价格表...")
    buf = export_xlsx(GSD_ID, log)
    if buf is None:
        log("[module2] GSD 导出失败，跳过")
        return

    sheets_data = read_xlsx_sheets(buf)
    first_sheet_name = list(sheets_data.keys())[0]
    data = sheets_data[first_sheet_name]

    price_map = {}
    for r in data[1:]:
        r = list(r) + [""] * (10 - len(r))
        so = str(r[0] or "").strip()
        item = str(r[2] or "").strip()
        try:
            price = float(r[9])
        except (ValueError, TypeError):
            continue
        if so and item:
            price_map[f"{so}___{item}"] = price

    for idx, row in enumerate(rows):
        so = str(row[COL_B_SO] or "").strip()
        item = str(row[COL_C_ITEM] or "").strip()
        key = f"{so}___{item}"
        if key in price_map:
            converted = price_map[key] * 0.003 * 22 / 7
            row[COL_D_PRICE] = round(converted, 2)
        else:
            cm = color_marks[idx]
            cm[COL_D_PRICE] = "green"
            cm[15] = "green"
            cm[16] = "green"
            color_marks[idx] = cm

    log(f"[module2] 价格写入完成，{len(rows)} 行")
