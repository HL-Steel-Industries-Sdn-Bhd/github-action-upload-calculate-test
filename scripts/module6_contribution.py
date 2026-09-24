from config import (COL_B_SO, COL_C_ITEM, COL_D_PRICE, COL_E_DIFFICULTY,
                    COL_H_RECV_PT, COL_K_COMP_PT, COL_M_EFFECTIVE,
                    COL_N_ALBERT_UNIT, COL_O_TOTAL_UNIT,
                    COL_P_CP_2DEC, COL_Q_CP_INT)

def _to_float(v):
    try:
        return float(v)
    except (ValueError, TypeError):
        return 0.0

def run(rows, color_marks, log):
    for idx, row in enumerate(rows):
        so = str(row[COL_B_SO] or "").strip()
        cm = color_marks[idx]

        if so in ("SO-000000", "SO-999999"):
            for c in (COL_B_SO, COL_C_ITEM, COL_D_PRICE, COL_E_DIFFICULTY):
                cm[c] = "chocolate"
            cm[15] = "chocolate"
            cm[16] = "chocolate"

        if row[COL_N_ALBERT_UNIT] == "N/A":
            o = row[COL_O_TOTAL_UNIT]
            if isinstance(o, (int, float)):
                row[COL_N_ALBERT_UNIT] = o
            else:
                row[COL_N_ALBERT_UNIT] = 0

        D = _to_float(row[COL_D_PRICE])
        E = _to_float(row[COL_E_DIFFICULTY])
        H = _to_float(row[COL_H_RECV_PT])
        K = _to_float(row[COL_K_COMP_PT])
        M = _to_float(row[COL_M_EFFECTIVE])
        N = _to_float(row[COL_N_ALBERT_UNIT])
        O = _to_float(row[COL_O_TOTAL_UNIT])

        if O == 0:
            contribution = 0
        else:
            contribution = D * E * (H + K) / 3 * M * N / O

        row[COL_P_CP_2DEC] = round(contribution, 2)
        row[COL_Q_CP_INT] = round(contribution)

        color_marks[idx] = cm

    log("[module6] 贡献分计算完成")
