import os
import requests
import fitz  # PyMuPDF

pdf_url = "https://nta.ac.in/Download/Notice/Notice_20241230193629.pdf"
temp_pdf = "temp_sme.pdf"
output_dir = "assets/syllabus"
output_pdf = os.path.join(output_dir, "SME_Syllabus.pdf")
public_output_pdf = os.path.join("public/assets/syllabus", "SME_Syllabus.pdf")

os.makedirs(output_dir, exist_ok=True)
os.makedirs("public/assets/syllabus", exist_ok=True)

print(f"Downloading SME syllabus from {pdf_url}...")
try:
    # Adding a User-Agent header as NTA website might block standard python-requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(pdf_url, headers=headers, timeout=30)
    response.raise_for_status()
    
    with open(temp_pdf, 'wb') as f:
        f.write(response.content)
        
    doc = fitz.open(temp_pdf)
    for page_num, page in enumerate(doc):
        # We search for different variations of NEET
        targets = [
            ("NEET(UG)", "SME(UG)"),
            ("NEET (UG)", "SME (UG)"),
            ("NEET", "SME"),
            ("National Eligibility cum Entrance Test", "SURYA Medical Examination"),
            ("National Eligibility-cum-Entrance Test", "SURYA Medical Examination"),
            ("National Testing Agency", "SURYA Examination Authority"),
            ("NTA", "SEA")
        ]
        
        for search_term, replace_term in targets:
            text_instances = page.search_for(search_term)
            for inst in text_instances:
                # Add white rectangle to hide the original text
                page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))
                # Insert replacement text
                fontsize = (inst.y1 - inst.y0) * 0.8
                # Slight vertical adjustment for baseline
                y_pos = inst.y1 - (inst.y1 - inst.y0) * 0.2
                page.insert_text((inst.x0, y_pos), replace_term, fontsize=fontsize, color=(0.1, 0.3, 0.8))
        
        # On the first page, let's add a large SURYA branding watermark at the top
        if page_num == 0:
            rect = fitz.Rect(50, 20, 500, 80)
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1)) # Cover NTA header if it's there
            page.insert_text((150, 50), "SURYA EDUCATION BOARD", fontsize=24, color=(0.0, 0.2, 0.6), fontname="helv", fontfile=None)
            page.insert_text((180, 70), "SME 2026 OFFICIAL SYLLABUS", fontsize=16, color=(0.4, 0.4, 0.4))
            
    doc.save(output_pdf)
    doc.close()
    
    # Copy to public folder
    with open(output_pdf, 'rb') as f_in, open(public_output_pdf, 'wb') as f_out:
        f_out.write(f_in.read())
        
    os.remove(temp_pdf)
    print(f"Successfully generated {output_pdf}")
    
except Exception as e:
    print(f"Failed to process SME Syllabus: {e}")
