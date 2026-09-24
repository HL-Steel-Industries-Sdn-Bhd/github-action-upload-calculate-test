# ============================================================
# 所有 ID、常量、列映射
# ============================================================

TARGET_SS_ID = "1P8-PVmRWDjgPGZ5HjpzHNXEelPWnpDhnXEupaMxnFxI"

GSB_IDS = [
    "11RS7BsU5O7pZwciypzMhpX2DoEEgivAgpSJup9pjrDY",  # Work Flow 12
    "1oZd56HEhPGIEWgZiEjGMarIneUg7dGQCXTNXDv0qJjQ",  # Work Flow 11
    "195mcmMLz-w3ZT8FwZU5WAq5DPHc7PTrpxsesScl12Ms",  # Work Flow 10
    "1n5zoYU_yVRyc-xmxhdQVoE2g3_aeMkGlamc8FPtLm64",  # Work Flow 9
    "1vFBZX0w0zBARy67Z4kRtDK8AKthjdozphp3GGljF8ZQ",  # Work Flow 8
    "1z992OeG5E7yBMp6wTJ0pDdTd-X-7NJJje0Qz8IQhLq8",  # Work Flow 7
]

GSC_ID = "1GuME9-Dkef1QCOq1ROvzoVYzNpp7W5zn2rcqcoy6mxM"
GSD_ID = "1lfkuHH3TJ0L9ZcSGcd5hOjp0LyWbpAhJCysIy2ATvIA"
GSF_ID = "1rzI20qWbjlIbZqVjZk6lhVSZ5cidkayniq_8Na0bUy8"

RECORD_SHEET = "Contribution Record"
SUMMARY_SHEET = "Contribution Summary"

COL_A_WORKFLOW    = 0
COL_B_SO          = 1
COL_C_ITEM        = 2
COL_D_PRICE       = 3
COL_E_DIFFICULTY  = 4
COL_F_RECEIVED    = 5
COL_G_RECV_TIME   = 6
COL_H_RECV_PT     = 7
COL_I_JOB         = 8
COL_J_COMP_TIME   = 9
COL_K_COMP_PT     = 10
COL_L_INTERVAL    = 11
COL_M_EFFECTIVE   = 12
COL_N_ALBERT_UNIT = 13
COL_O_TOTAL_UNIT  = 14
COL_P_CP_2DEC     = 15
COL_Q_CP_INT      = 16

TOTAL_COLS = 17

RECORD_HEADERS = [
    "Work Flow", "SO", "Item", "Price", "Difficulty",
    "Received", "Received Time", "Received Point",
    "Job Completed", "Completed Time", "Completed Point",
    "Interval(min)", "Effective",
    "Albert Unit", "Total Units",
    "CP(2dp)", "CP(int)"
]

SUMMARY_HEADERS_AB = ["Work Flow", "Total CP"]
SUMMARY_E1_LABEL = "Grand Total (excl. WF1-6)"

EXCLUDED_WORKFLOWS = [
    "Work Flow 1", "Work Flow 2", "Work Flow 3",
    "Work Flow 4", "Work Flow 5", "Work Flow 6",
]

COLOR_RED       = {"red": 0.973, "green": 0.843, "blue": 0.855}
COLOR_BLUE      = {"red": 0.824, "green": 0.918, "blue": 1.0}
COLOR_GREEN     = {"red": 0.8,   "green": 1.0,   "blue": 0.8}
COLOR_CORAL     = {"red": 1.0,   "green": 0.855, "blue": 0.725}
COLOR_YELLOW    = {"red": 1.0,   "green": 1.0,   "blue": 0.8}
COLOR_CHOCOLATE = {"red": 0.824, "green": 0.706, "blue": 0.549}
COLOR_PURPLE    = {"red": 0.878, "green": 0.843, "blue": 0.961}
