import os
import requests
import fitz  # PyMuPDF
from urllib.parse import urljoin

base_url = "https://gate2026.iitg.ac.in/exam-papers-and-syllabus.html"

subjects = [
    ("Aerospace Engineering", "AE"),
    ("Agricultural Engineering", "AG"),
    ("Architecture and Planning", "AR"),
    ("Biomedical Engineering", "BM"),
    ("Biotechnology", "BT"),
    ("Civil Engineering", "CE"),
    ("Chemical Engineering", "CH"),
    ("Computer Science & Information Technology", "CS"),
    ("Chemistry", "CY"),
    ("Data Science & Artificial Intelligence", "DA"),
    ("Electronics & Communication Engineering", "EC"),
    ("Electrical Engineering", "EE"),
    ("Environmental Science & Engineering", "ES"),
    ("Ecology and Evolution", "EY"),
    ("Geomatics Engineering", "GE"),
    ("Geology & Geophysics", "GG"),
    ("Instrumentation Engineering", "IN"),
    ("Mathematics", "MA"),
    ("Mechanical Engineering", "ME"),
    ("Mining Engineering", "MN"),
    ("Metallurgical Engineering", "MT"),
    ("Naval Architecture & Marine Engineering", "NM"),
    ("Petroleum Engineering", "PE"),
    ("Physics", "PH"),
    ("Production & Industrial Engineering", "PI"),
    ("Statistics", "ST"),
    ("Textile Engineering & Fibre Science", "TF"),
    ("Engineering Sciences", "XE"),
    ("Humanities & Social Sciences", "XH"),
    ("Life Sciences", "XL"),
]

output_dir = "assets/syllabus"
os.makedirs(output_dir, exist_ok=True)
os.makedirs("public/assets/syllabus", exist_ok=True)

for name, code in subjects:
    pdf_url = f"https://gate2026.iitg.ac.in/doc/GATE2026_Syllabus/{code}_2026_Syllabus.pdf"
    if code == "XE":
        pdf_url = "https://gate2026.iitg.ac.in/doc/GATE2026_Syllabus/XE-2026_Combined_Syllabus.pdf"
    elif code == "XH":
        pdf_url = "https://gate2026.iitg.ac.in/doc/GATE2026_Syllabus/XH-2026_Combined_Syllabus.pdf"
    elif code == "XL":
        pdf_url = "https://gate2026.iitg.ac.in/doc/GATE2026_Syllabus/XL-2026_Combined_Syllabus.pdf"

    print(f"Downloading {code} from {pdf_url}...")
    try:
        response = requests.get(pdf_url, timeout=15)
        response.raise_for_status()
        
        temp_pdf = f"temp_{code}.pdf"
        with open(temp_pdf, 'wb') as f:
            f.write(response.content)
            
        doc = fitz.open(temp_pdf)
        for page in doc:
            # Search for GATE (case-insensitive)
            text_instances = page.search_for("GATE")
            for inst in text_instances:
                # Add white rectangle to hide "GATE"
                page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
                # Insert "SAT"
                # inst is a Rect (x0, y0, x1, y1)
                fontsize = (inst.y1 - inst.y0) * 0.8
                page.insert_text((inst.x0, inst.y1 - (inst.y1 - inst.y0)*0.2), "SAT", fontsize=fontsize, color=(0, 0, 0.5))

            # Search for "Graduate Aptitude Test in Engineering" and replace it
            text_instances_full = page.search_for("Graduate Aptitude Test in Engineering")
            for inst in text_instances_full:
                page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
                fontsize = (inst.y1 - inst.y0) * 0.8
                page.insert_text((inst.x0, inst.y1 - (inst.y1 - inst.y0)*0.2), "SURYA Admission Test", fontsize=fontsize, color=(0, 0, 0.5))

        out_path = os.path.join(output_dir, f"{code}_SAT_Syllabus.pdf")
        doc.save(out_path)
        doc.close()
        
        # Copy to public folder
        out_pub_path = os.path.join("public/assets/syllabus", f"{code}_SAT_Syllabus.pdf")
        with open(out_path, 'rb') as f_in, open(out_pub_path, 'wb') as f_out:
            f_out.write(f_in.read())
            
        os.remove(temp_pdf)
        print(f"Successfully generated {code}_SAT_Syllabus.pdf")
        
    except Exception as e:
        print(f"Failed to process {code}: {e}")

print("All PDFs processed!")
