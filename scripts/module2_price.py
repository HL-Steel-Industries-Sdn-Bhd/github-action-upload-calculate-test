from sheets_client import open_ss, read_all
from config import GSD_ID, COL_B_SO, COL_C_ITEM, COL_D_PRICE

def run(rows, color_marks, log):
    ss = open_ss(GSD_ID)
    ws = ss.get_worksheet(0)
    data = read_all(ws)

    price_map = {}
    for r in data[1:]:
        r = list(r) + [""] * (10 - len(r))
        so = (r[0] or "").strip()
        item = (r[2] or "").strip()
        try:
            price = float(r[9])
        except (ValueError, TypeError):
            continue
        if so and item:
            price_map[f"{so}___{item}"] = price

    for idx, row in enumerate(rows):
        so = (str(row[COL_B_SO]) if row[COL_B_SO] else "").strip()
        item = (str(row[COL_C_ITEM]) if row[COL_C_ITEM] else "").strip()
        key = f"{so}___{item}"
        if key in price_map:
            converted = price_map[key] * 0.003 * 22 / 7
            row[COL_D_PRICE] = round(converted, 2)
        else:
            cm = color_marks[idx]
            cm[COL_D_PRICE] = "green"
            cm[15] = "green"; cm[16] = "green"
            color_marks[idx] = cm

    log(f"[module2] 价格写入完成，{len(rows)} 行")
