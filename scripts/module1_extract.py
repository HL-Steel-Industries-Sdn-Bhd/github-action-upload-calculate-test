import re
from datetime import datetime
from sheets_client import open_ss, read_all
from config import GSB_IDS

def _parse_units_from_a1(a1_text):
    m = re.search(r"(\d+)\s+units\b", a1_text or "", re.IGNORECASE)
    return int(m.group(1)) if m else 0

def run(log):
    rows = []
    color_marks = []

    for gsb_id in GSB_IDS:
        ss = open_ss(gsb_id)
        wf_name = ss.title.split("-")[0].strip()
        log(f"[module1] 处理 {wf_name}")

        for ws in ss.worksheets():
            sheet_name = ws.title
            if sheet_name == "目录":
                continue
            name_parts = sheet_name.split(" - ")
            if len(name_parts) < 3 or not name_parts[0].startswith("SO-"):
                continue

            sales_order = name_parts[0].strip()
            m = re.search(r"Item\s+(\d+)", sheet_name)
            item_no = m.group(1) if m else ""

            all_vals = read_all(ws)
            last_row = len(all_vals)
            if last_row <= 3:
                continue

            a1_text = all_vals[0][0] if all_vals and all_vals[0] else ""
            total_units = _parse_units_from_a1(a1_text)

            data = all_vals[3:]
            if not data:
                continue

            received_set, completed_set = set(), set()
            received_list, completed_list = [], []
            job_to_people = {}
            job_to_units = {}

            for r in data:
                r = list(r) + [""] * (30 - len(r))
                timestamp = r[0]
                name = r[1]
                received = r[4]
                job_completed = r[6]
                unit = r[29]

                if name == "Albert":
                    if received and received not in received_set:
                        received_set.add(received)
                        received_list.append((received, timestamp))
                    if job_completed and job_completed not in completed_set:
                        completed_set.add(job_completed)
                        completed_list.append((job_completed, timestamp))

                if job_completed and name:
                    job_to_people.setdefault(job_completed, set()).add(name)
                    job_to_units.setdefault(job_completed, 0)
                    try:
                        job_to_units[job_completed] += float(unit)
                    except (ValueError, TypeError):
                        pass

            for job, people in job_to_people.items():
                if total_units == 1 and len(people) > 1:
                    total_units = len(people)

            max_len = max(len(received_list), len(completed_list))
            link_formula = f'=HYPERLINK("https://docs.google.com/spreadsheets/d/{gsb_id}/edit#gid={ws.id}", "{wf_name}")'

            for i in range(max_len):
                recv = received_list[i] if i < len(received_list) else (None, None)
                comp = completed_list[i] if i < len(completed_list) else (None, None)
                job_name = comp[0]

                row = [""] * 17
                row[0] = link_formula
                row[1] = sales_order
                row[2] = item_no
                if recv[0]:
                    row[5] = recv[0]
                    row[6] = recv[1]
                cm = {}
                if job_name:
                    row[8] = job_name
                    row[9] = comp[1]
                    units = "N/A"
                    for r in data:
                        r = list(r) + [""] * (30 - len(r))
                        if r[1] == "Albert" and r[6] == job_name:
                            u = r[29]
                            units = u if u not in (None, "") else "N/A"
                            break
                    row[13] = units
                    if isinstance(units, (int, float)) and job_to_units.get(job_name, 0) > total_units:
                        cm = {13: "red", 15: "red", 16: "red"}
                else:
                    row[13] = 1
                row[14] = total_units
                if total_units == 0:
                    cm[14] = "blue"; cm[15] = "blue"; cm[16] = "blue"

                rows.append(row)
                color_marks.append(cm)

    return rows, color_marks
