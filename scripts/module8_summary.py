from config import (COL_A_WORKFLOW, COL_Q_CP_INT, EXCLUDED_WORKFLOWS)

def run(rows, log):
    summary_map = {}
    grand_total = 0

    for row in rows:
        wf = row[COL_A_WORKFLOW]
        q = row[COL_Q_CP_INT]
        try:
            qf = float(q)
        except (ValueError, TypeError):
            continue
        if wf:
            summary_map[wf] = summary_map.get(wf, 0) + qf
            if wf not in EXCLUDED_WORKFLOWS:
                grand_total += qf

    output = [[k, v] for k, v in summary_map.items()]
    log(f"[module8] Summary 完成，{len(output)} 个 WF，grand total = {grand_total}")
    return output, grand_total
