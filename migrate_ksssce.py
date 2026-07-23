import os
import re

def main():
    base_dir = r"e:\Sushanth Projects\SURYA"
    templates_dir = os.path.join(base_dir, "templates")

    # 1. Rename files
    ksseab_html = os.path.join(templates_dir, "KSSEAB.html")
    ksssce_html = os.path.join(templates_dir, "KSSSCE.html")
    if os.path.exists(ksseab_html):
        os.rename(ksseab_html, ksssce_html)

    ksseab_dates_html = os.path.join(templates_dir, "KSSEAB_Dates.html")
    ksssce_dates_html = os.path.join(templates_dir, "KSSSCE_Dates.html")
    if os.path.exists(ksseab_dates_html):
        os.rename(ksseab_dates_html, ksssce_dates_html)

    # 2. Update contents of KSSSCE.html
    if os.path.exists(ksssce_html):
        with open(ksssce_html, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Change page title block
        content = content.replace("KSSEAB — SURYA EDUCATION BOARD", "KSSSCE — SURYA EDUCATION BOARD")
        # Change CTA dates link
        content = content.replace('KSSEAB_Dates.html', 'KSSSCE_Dates.html')
        content = content.replace('View KSSEAB Dates', 'View KSSSCE Dates')
        
        with open(ksssce_html, "w", encoding="utf-8") as f:
            f.write(content)

    # 3. Update contents of KSSSCE_Dates.html
    if os.path.exists(ksssce_dates_html):
        with open(ksssce_dates_html, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace("KSSEAB Important Dates", "KSSSCE Important Dates")
        content = content.replace("Important Dates for KSSEAB", "Important Dates for KSSSCE")
        content = content.replace("the KSSEAB examination", "the KSSSCE examination")
        content = content.replace("KSSEAB.html", "KSSSCE.html")
        content = content.replace("Back to KSSEAB", "Back to KSSSCE")
        
        with open(ksssce_dates_html, "w", encoding="utf-8") as f:
            f.write(content)

    # 4. Update header.html
    header_path = os.path.join(templates_dir, "header.html")
    if os.path.exists(header_path):
        with open(header_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('href="/KSSEAB.html">KSSEAB</a>', 'href="/KSSSCE.html">KSSSCE</a>')
        with open(header_path, "w", encoding="utf-8") as f:
            f.write(content)

    # 5. Update build_static.py
    build_script = os.path.join(base_dir, "build_static.py")
    if os.path.exists(build_script):
        with open(build_script, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('"KSSEAB.html",         "KSSEAB.html"', '"KSSSCE.html",         "KSSSCE.html"')
        content = content.replace('"KSSEAB_Dates.html", "KSSEAB_Dates.html"', '"KSSSCE_Dates.html", "KSSSCE_Dates.html"')
        with open(build_script, "w", encoding="utf-8") as f:
            f.write(content)

    print("Migration to KSSSCE complete.")

if __name__ == "__main__":
    main()
