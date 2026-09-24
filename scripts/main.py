import sys
import traceback
from datetime import datetime, date

from sheets_client import open_ss, ensure_sheet
from config import (TARGET_SS_ID, RECORD_SHEET, SUMMARY_SHEET,
                    RECORD_HEADERS, TOTAL_COLS,
                    SUMMARY_HEADERS_AB, SUMMARY_E1_LABEL,
                    COLOR_RED, COLOR_BLUE, COLOR_GREEN, COLOR_CORAL,
                    COLOR_YELLOW, COLOR_CHOCOLATE, COLOR_PURPLE)

import module1_extract
import module2_price
import module3_difficulty
import module4_points
import module5_time
import module6_contribution
import module7_gsf
import module8_summary

COLOR_MAP = {
    "red": COLOR_RED, "blue": COLOR_BLUE, "green": COLOR_GREEN,
    "coral": COLOR_CORAL, "yellow": COLOR_YELLOW,
    "chocolate": COLOR_CHOCOLATE, "purple": COLOR_PURPLE,
}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def sanitize(v):
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(v, date):
        return v.strftime("%Y-%m-%d")
    return v

def sanitize_rows(rows):
    return [[sanitize(cell) for cell in row] for row in rows]

def apply_colors(sheet, color_marks):
    requests = []
    requests.append({
        "repeatCell": {
            "range": {"sheetId": sheet.id,
                      "startRowIndex": 1,
                      "endRowIndex": len(color_marks) + 1,
                      "startColumnIndex": 0,
                      "endColumnIndex": TOTAL_COLS},
            "cell": {"userEnteredFormat": {"backgroundColor": {"red":1,"green":1,"blue":1}}},
            "fields": "userEnteredFormat.backgroundColor"
        }
    })

    for r_idx, cm in enumerate(color_marks):
        for c_idx, color_name in cm.items():
            rgb = COLOR_MAP.get(color_name)
            if not rgb:
                continue
            requests.append({
                "repeatCell": {
                    "range": {"sheetId": sheet.id,
                              "startRowIndex": r_idx + 1,
                              "endRowIndex": r_idx + 2,
                              "startColumnIndex": c_idx,
                              "endColumnIndex": c_idx + 1},
                    "cell": {"userEnteredFormat": {"backgroundColor": rgb}},
                    "fields": "userEnteredFormat.backgroundColor"
                }
            })

    if requests:
        sheet.spreadsheet.batch_update({"requests": requests})
        log(f"背景色应用完成，{len(requests)} 个请求")

def main():
    try:
        log("=== 开始 ===")
        target = open_ss(TARGET_SS_ID)
        record = ensure_sheet(target, RECORD_SHEET, rows=5000, cols=TOTAL_COLS)
        summary = ensure_sheet(target, SUMMARY_SHEET, rows=200, cols=10)

        log("运行 module1...")
        rows, color_marks = module1_extract.run(log)
        log(f"module1 产生 {len(rows)} 行")

        log("运行 module2...")
        module2_price.run(rows, color_marks, log)

        log("运行 module3...")
        module3_difficulty.run(rows, log)

        log("运行 module4...")
        module4_points.run(rows, color_marks, log)

        log("运行 module5...")
        module5_time.run(rows, color_marks, log)

        log("运行 module6...")
        module6_contribution.run(rows, color_marks, log)

        log("运行 module7...")
        module7_gsf.run(rows, color_marks, log)

        log("运行 module8...")
        summary_rows, grand_total = module8_summary.run(rows, log)

        log("清空目标表...")
        record.clear()
        summary.clear()

        log("写标题...")
        record.update(values=[RECORD_HEADERS], range_name="A1")
        summary.update(values=[[SUMMARY_HEADERS_AB[0], SUMMARY_HEADERS_AB[1]]], range_name="A1")
        summary.update(values=[[SUMMARY_E1_LABEL, grand_total]], range_name="D1")

        if rows:
            log(f"写 Record，{len(rows)} 行...")
            rows_clean = sanitize_rows(rows)
            record.update(values=rows_clean,
                          range_name=f"A2:Q{len(rows_clean)+1}",
                          value_input_option="USER_ENTERED")

        if summary_rows:
            log(f"写 Summary，{len(summary_rows)} 行...")
            summary.update(values=[[r[0], r[1]] for r in summary_rows],
                           range_name=f"A2:B{len(summary_rows)+1}")

        log("应用颜色...")
        apply_colors(record, color_marks)

        log("=== 完成 ===")

    except Exception as e:
        log(f"错误: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
