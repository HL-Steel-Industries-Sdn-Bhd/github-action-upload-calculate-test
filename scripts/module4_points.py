from config import (COL_F_RECEIVED, COL_H_RECV_PT,
                    COL_I_JOB, COL_K_COMP_PT)

def run(rows, color_marks, log):
    for idx, row in enumerate(rows):
        f_val = row[COL_F_RECEIVED]
        f_str = str(f_val).strip() if f_val else ""
        i_val = row[COL_I_JOB]
        i_str = str(i_val).strip() if i_val else ""
        cm = color_marks[idx]

        if f_str:
            row[COL_H_RECV_PT] = 1
        else:
            cm[COL_F_RECEIVED] = "coral"
            cm[COL_F_RECEIVED+1] = "coral"
            cm[COL_H_RECV_PT] = "coral"
            cm[15] = "coral"; cm[16] = "coral"

        if i_str:
            row[COL_K_COMP_PT] = 2
        else:
            cm[COL_I_JOB] = "coral"
            cm[COL_I_JOB+1] = "coral"
            cm[COL_K_COMP_PT] = "coral"
            cm[15] = "coral"; cm[16] = "coral"

        color_marks[idx] = cm

    log(f"[module4] 基础分写入完成")
