"""
build_static.py
Renders all Jinja2 templates into static HTML files and places them in
the public/ directory so Firebase Hosting can serve them.

Run from the SURYA project root:
    python build_static.py
"""

import io
import sys
import os
import subprocess
import shutil

# Force UTF-8 stdout so print() never fails on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Tell Python to read/write text files as UTF-8 by default
os.environ["PYTHONUTF8"] = "1"

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# ── Setup ────────────────────────────────────────────────────────────────────
ROOT   = Path(__file__).parent
TMPL   = ROOT / "public" / "templates"
PUBLIC = ROOT / "public"

# --- React Analytics Build Step ---
# print("Building React Analytics App...")
# try:
#     subprocess.run("npm run build", cwd=str(ROOT / "react-analytics"), check=True, shell=True)
#     
#     # Copy output to public/assets/
#     dist_assets = ROOT / "react-analytics" / "dist" / "assets"
#     public_assets = PUBLIC / "assets"
#     
#     if dist_assets.exists():
#         for file in dist_assets.iterdir():
#             shutil.copy(file, public_assets / file.name)
#         print("  [OK]  React Analytics bundle copied.")
#     else:
#         print("  [WARN] React Analytics dist/assets not found.")
# except Exception as e:
#     print(f"  [ERROR] Failed to build React Analytics: {e}")
    
# ── Setup ────────────────────────────────────────────────────────────────────
env = Environment(
    loader=FileSystemLoader(str(TMPL), encoding="utf-8"),
    autoescape=False,
)

# Pages to render: (template_name, output_filename_in_public)
# "Surya.html" becomes "index.html" so Firebase serves it at the root URL.
PAGES = [
    ("CandidateDashboard.html", "CandidateDashboard.html"),
    ("Surya.html",          "index.html"),
    ("About.html",          "About.html"),
    ("Contact.html",        "Contact.html"),
    ("ImportantDates.html", "ImportantDates.html"),
    ("Resources.html",      "Resources.html"),
    ("Articles.html",       "Articles.html"),
    ("SET01.html",          "SET01.html"),
    ("SET02.html",          "SET02.html"),
    ("SA.html",             "SA.html"),
    ("SST.html",            "SST.html"),
    ("SAT.html",            "SAT.html"),
    ("SATSyllabus.html",    "SATSyllabus.html"),
    ("SME.html",            "SME.html"),
    ("KSSEAB.html",         "KSSEAB.html"),
    ("KSPUEAB.html",        "KSPUEAB.html"),
    ("KSSSCE.html",         "KSSSCE.html"),
    ("Register.html",       "Register.html"),
    ("admin.html",          "admin.html"),
    ("admin_schedule.html", "admin_schedule.html"),
    ("SET_Session01_Exam_Portal.html", "SET_Session01_Exam_Portal.html"),
    ("SET_Session02_Exam_Portal.html", "SET_Session02_Exam_Portal.html"),
    ("KSPUEAB_Dates.html", "KSPUEAB_Dates.html"),
    ("KSSSCE_Dates.html", "KSSSCE_Dates.html"),
    ("KSSEAB_Dates.html", "KSSEAB_Dates.html"),
    ("SME_Dates.html", "SME_Dates.html"),
    ("SA_Dates.html", "SA_Dates.html"),
    ("SST_Dates.html", "SST_Dates.html"),
    ("SAT_Dates.html", "SAT_Dates.html"),
    ("SET02_Dates.html", "SET02_Dates.html"),
    ("SET01_Dates.html", "SET01_Dates.html"),
    ("Register_SET.html", "Register_SET.html"),
    ("Register_SST.html", "Register_SST.html"),
    ("Register_SAT.html", "Register_SAT.html"),
    ("Register_SME.html", "Register_SME.html"),
    ("Register_SA.html", "Register_SA.html"),
    ("Register_Boards.html", "Register_Boards.html"),
]

# ── Load Data ────────────────────────────────────────────────────────────────
import csv

def load_broadcasts():
    broadcasts = []
    csv_path = ROOT / "broadcasts.csv"
    if csv_path.exists():
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    broadcasts.append(row)
        except Exception as e:
            print(f"Error loading broadcasts.csv: {e}")
    return list(reversed(broadcasts))

def load_csv_rows(filename):
    csv_path = ROOT / filename
    if not csv_path.exists():
        return []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            return list(reader)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return []

def load_seoas_registrations():
    jsonl_path = ROOT / "seoas_registrations.jsonl"
    if not jsonl_path.exists():
        return []
    import json
    rows = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                try:
                    data = json.loads(line)
                    # Mapping to match registrations.csv:
                    # registration_id,name,email,phone,dob,gender,exam_category,priority_1,priority_2,priority_3,allocated_center,education_board
                    row = [
                        data.get("application_number", "UNKNOWN"),
                        data.get("reg-name", ""),
                        data.get("reg-email", ""),
                        data.get("reg-mobile", ""),
                        data.get("pd-dob", ""),
                        data.get("pd-gender", ""),
                        data.get("exam-type", "SST"), # Defaults to SST if not specified
                        data.get("preference-1", ""),
                        data.get("preference-2", ""),
                        data.get("preference-3", "N/A"),
                        "Pending", # allocated_center
                        data.get("academic-board", "")
                    ]
                    rows.append(row)
                except Exception as ex:
                    pass
    except Exception as e:
        print(f"Error loading seoas_registrations.jsonl: {e}")
    return rows

broadcasts_list = load_broadcasts()
registration_rows = load_csv_rows("registrations.csv")

# Ensure header exists if registration_rows is empty
if not registration_rows:
    registration_rows = [["registration_id","name","email","phone","dob","gender","exam_category","priority_1","priority_2","priority_3","allocated_center","education_board"]]

seoas_rows = load_seoas_registrations()
registration_rows.extend(seoas_rows)

contact_rows = load_csv_rows("contacts.csv")

# Ensure uploads directory exists in public
(PUBLIC / "uploads").mkdir(exist_ok=True)

# ── Render ───────────────────────────────────────────────────────────────────
ok = 0
fail = 0
for template_name, output_name in PAGES:
    try:
        tmpl = env.get_template(template_name)
        html = tmpl.render(
            broadcasts=broadcasts_list,
            registration_rows=registration_rows,
            contact_rows=contact_rows,
            registration_closed=False,
            show_header_rules=(template_name != 'Surya.html')
        )
        out_path = PUBLIC / output_name
        out_path.write_text(html, encoding="utf-8")
        print(f"  [OK]  {output_name}")
        ok += 1
    except Exception as e:
        print(f"  [FAIL]  {output_name}  ->  {e}")
        fail += 1

print(f"\nBuild complete: {ok} OK, {fail} failed.")

import json
def build_dob_passwords(dob_value):
    if not dob_value:
        return []
    dob_value = dob_value.strip()
    from datetime import datetime
    candidates = []
    for fmt in ('%Y-%m-%d', '%d-%m-%Y', '%d/%m/%Y', '%Y/%m/%d', '%d.%m.%Y'):
        try:
            dob = datetime.strptime(dob_value, fmt)
            candidates.append(dob.strftime('%d%b%Y'))
            candidates.append(dob.strftime('%d%B%Y'))
            candidates.append(dob.strftime('%d%m%Y'))
            break
        except ValueError:
            continue
    return [p.lower() for p in candidates if p]

def generate_candidates_json():
    rows = registration_rows
    if not rows or len(rows) <= 1: return
    headers = [h.strip().lower() for h in rows[0]]
    try:
        app_index = next(i for i, h in enumerate(headers) if h in ['registration_id', 'registration id', 'application_number', 'application number'])
    except StopIteration:
        return
    name_index = next((i for i, h in enumerate(headers) if h == 'name'), None)
    email_index = next((i for i, h in enumerate(headers) if h == 'email'), None)
    phone_index = next((i for i, h in enumerate(headers) if h == 'phone'), None)
    dob_index = next((i for i, h in enumerate(headers) if h == 'dob'), None)
    password_index = next((i for i, h in enumerate(headers) if h == 'password'), None)

    candidates = {}
    for row in rows[1:]:
        if len(row) <= app_index: continue
        app_num = row[app_index].strip().upper()
        if not app_num: continue
        
        candidate_passwords = []
        if password_index is not None and len(row) > password_index and row[password_index].strip():
            candidate_passwords.append(row[password_index].strip().lower())
        
        if dob_index is not None and len(row) > dob_index and row[dob_index].strip():
            candidate_passwords.extend(build_dob_passwords(row[dob_index].strip()))
        
        if phone_index is not None and len(row) > phone_index and row[phone_index].strip():
            candidate_passwords.append(row[phone_index].strip()[-4:].lower())

        candidates[app_num] = {
            "name": row[name_index].strip() if name_index is not None and len(row) > name_index else '',
            "passwords": candidate_passwords
        }
    
    candidates_json_str = json.dumps(candidates)
    
    # Inject directly into the built HTML files in public directory
    for portal in ["SET_Session01_Exam_Portal.html", "SET_Session02_Exam_Portal.html"]:
        portal_path = PUBLIC / portal
        if portal_path.exists():
            content = portal_path.read_text(encoding="utf-8")
            script_injection = f"\n<script>window.CANDIDATES_DATA = {candidates_json_str};</script>\n</body>"
            content = content.replace("</body>", script_injection)
            portal_path.write_text(content, encoding="utf-8")
    
    print("  [OK]  CANDIDATES_DATA injected into portal HTML files.")

generate_candidates_json()
print("Run  firebase deploy  to publish.")
