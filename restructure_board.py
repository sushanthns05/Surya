import os
import re

def main():
    base_dir = r"e:\Sushanth Projects\SURYA"
    templates_dir = os.path.join(base_dir, "templates")
    
    ksssce_html = os.path.join(templates_dir, "KSSSCE.html")
    ksseab_html = os.path.join(templates_dir, "KSSEAB.html")
    
    ksssce_dates = os.path.join(templates_dir, "KSSSCE_Dates.html")
    ksseab_dates = os.path.join(templates_dir, "KSSEAB_Dates.html")
    
    tenth_html = os.path.join(templates_dir, "10th Standard.html")
    tenth_dates = os.path.join(templates_dir, "10th_Dates.html")
    
    puc_html = os.path.join(templates_dir, "PUC.html")
    pueab_html = os.path.join(templates_dir, "KSPUEAB.html")
    
    puc_dates = os.path.join(templates_dir, "PUC_Dates.html")
    pueab_dates = os.path.join(templates_dir, "KSPUEAB_Dates.html")

    # 1. Revert KSSEAB (which was renamed to KSSSCE in the previous script)
    if os.path.exists(ksssce_html) and not os.path.exists(ksseab_html):
        # Read KSSSCE and revert the text
        with open(ksssce_html, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("KSSSCE — SURYA EDUCATION BOARD", "KSSEAB — SURYA EDUCATION BOARD")
        content = content.replace("KSSSCE_Dates.html", "KSSEAB_Dates.html")
        content = content.replace("View KSSSCE Dates", "View KSSEAB Dates")
        with open(ksseab_html, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(ksssce_html)

    if os.path.exists(ksssce_dates) and not os.path.exists(ksseab_dates):
        with open(ksssce_dates, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("KSSSCE Important Dates", "KSSEAB Important Dates")
        content = content.replace("Important Dates for KSSSCE", "Important Dates for KSSEAB")
        content = content.replace("the KSSSCE examination", "the KSSEAB examination")
        content = content.replace("KSSSCE.html", "KSSEAB.html")
        content = content.replace("Back to KSSSCE", "Back to KSSEAB")
        with open(ksseab_dates, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(ksssce_dates)
        
    # 2. Rename 10th Standard to KSSSCE
    if os.path.exists(tenth_html):
        with open(tenth_html, "r", encoding="utf-8") as f:
            content = f.read()
        # Update specific references in the file if needed
        content = content.replace("10th Standard (KSSSCE)", "KSSSCE")
        content = content.replace("10th Standard.html", "KSSSCE.html")
        content = content.replace("10th_Dates.html", "KSSSCE_Dates.html")
        content = content.replace("View 10th Standard Dates", "View KSSSCE Dates")
        with open(ksssce_html, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(tenth_html)

    if os.path.exists(tenth_dates):
        with open(tenth_dates, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("10th Standard Important Dates", "KSSSCE Important Dates")
        content = content.replace("Important Dates for 10th Standard", "Important Dates for KSSSCE")
        content = content.replace("the 10th Standard examination", "the KSSSCE examination")
        content = content.replace("10th%20Standard.html", "KSSSCE.html")
        content = content.replace("Back to 10th Standard", "Back to KSSSCE")
        with open(ksssce_dates, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(tenth_dates)

    # 3. Rename PUC to KSPUEAB
    if os.path.exists(puc_html):
        with open(puc_html, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("PUC — SURYA EDUCATION BOARD", "KSPUEAB — SURYA EDUCATION BOARD")
        content = content.replace("PUC_Dates.html", "KSPUEAB_Dates.html")
        content = content.replace("View PUC Dates", "View KSPUEAB Dates")
        content = content.replace("the PUC examinations", "the KSPUEAB examinations")
        with open(pueab_html, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(puc_html)

    if os.path.exists(puc_dates):
        with open(puc_dates, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("PUC Important Dates", "KSPUEAB Important Dates")
        content = content.replace("Important Dates for PUC", "Important Dates for KSPUEAB")
        content = content.replace("the PUC examination", "the KSPUEAB examination")
        content = content.replace("PUC.html", "KSPUEAB.html")
        content = content.replace("Back to PUC", "Back to KSPUEAB")
        with open(pueab_dates, "w", encoding="utf-8") as f:
            f.write(content)
        os.remove(puc_dates)

    # 4. Update header.html
    header_path = os.path.join(templates_dir, "header.html")
    if os.path.exists(header_path):
        with open(header_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Currently, header has:
        # <a href="/KSSSCE.html">KSSSCE</a>  (was KSSEAB)
        # <a href="/10th Standard.html">10th Standard</a>
        # <a href="/PUC.html">PUC</a>
        
        content = content.replace('href="/KSSSCE.html">KSSSCE</a>', 'href="/KSSEAB.html">KSSEAB</a>')
        content = content.replace('href="/10th Standard.html">10th Standard</a>', 'href="/KSSSCE.html">KSSSCE (10th)</a>')
        content = content.replace('href="/10th%20Standard.html">10th Standard</a>', 'href="/KSSSCE.html">KSSSCE (10th)</a>')
        content = content.replace('href="/PUC.html">PUC</a>', 'href="/KSPUEAB.html">KSPUEAB (PUC)</a>')
        
        with open(header_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 5. Update build_static.py
    build_script = os.path.join(base_dir, "build_static.py")
    if os.path.exists(build_script):
        with open(build_script, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace('"KSSSCE.html",         "KSSSCE.html"', '"KSSEAB.html",         "KSSEAB.html"')
        content = content.replace('"KSSSCE_Dates.html", "KSSSCE_Dates.html"', '"KSSEAB_Dates.html", "KSSEAB_Dates.html"')
        
        content = content.replace('"10th Standard.html",  "10th Standard.html"', '"KSSSCE.html",         "KSSSCE.html"')
        content = content.replace('"10th_Dates.html", "10th_Dates.html"', '"KSSSCE_Dates.html", "KSSSCE_Dates.html"')
        
        content = content.replace('"PUC.html",            "PUC.html"', '"KSPUEAB.html",        "KSPUEAB.html"')
        content = content.replace('"PUC_Dates.html", "PUC_Dates.html"', '"KSPUEAB_Dates.html", "KSPUEAB_Dates.html"')

        with open(build_script, "w", encoding="utf-8") as f:
            f.write(content)

    print("Restructuring complete.")

if __name__ == "__main__":
    main()
