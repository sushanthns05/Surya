import json
import os
import subprocess
import urllib.parse

json_path = r"e:\Sushanth Projects\SURYA\Vaults\SET- SESSION 01 2027 FINAL PAPER.json"
html_path = r"e:\Sushanth Projects\SURYA\Vaults\Printable_SET_Session01.html"
pdf_path = r"e:\Sushanth Projects\SURYA\Vaults\SET_Session01_Paper.pdf"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# The json seems to have "sections" and "exam_meta".
# Let's extract them.

html_content = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>SET Session 01 - Question Paper</title>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  body { font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.5; color: #000; background: #fff; margin: 0; padding: 20px; }
  .header { text-align: center; border-bottom: 2px solid #000; padding-bottom: 10px; margin-bottom: 20px; }
  .header h1 { margin: 0 0 5px 0; font-size: 24px; color: #003087; }
  .header h2 { margin: 0; font-size: 16px; font-weight: normal; }
  .section { margin-bottom: 30px; }
  .sec-header { background: #f1f5f9; padding: 10px; font-weight: bold; font-size: 16px; border: 1px solid #cbd5e1; margin-bottom: 15px; }
  .question { margin-bottom: 20px; page-break-inside: avoid; }
  .q-num { font-weight: bold; float: left; width: 35px; }
  .q-content { margin-left: 35px; }
  .opts { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
  .opt { display: flex; gap: 8px; }
  .opt-label { font-weight: bold; width: 25px; }
  .opt-text { flex: 1; }
  .numerical-placeholder { margin-top: 10px; font-style: italic; color: #555; }
  
  @media print {
    body { padding: 0; }
    @page { margin: 15mm; }
  }
</style>
</head>
<body>
  <div class="header">
    <h1>Surya Entrance Test [SET] 2027 - Session 01</h1>
    <h2>Final Question Paper</h2>
  </div>
"""

letters = ['(A)', '(B)', '(C)', '(D)']

global_num = 1
for sec in data.get('sections', []):
    qs = sec.get('questions', [])
    html_content += f'<div class="section"><div class="sec-header">{sec.get("name", "Section")} ({len(qs)} Questions | +{sec.get("marks", {}).get("correct", 0)} / -{sec.get("marks", {}).get("wrong", 0)})</div>'
    
    for q in qs:
        html_content += '<div class="question">'
        html_content += f'<div class="q-num">Q{global_num}.</div>'
        html_content += f'<div class="q-content">{q.get("text", "")}'
        
        if sec.get('type') in ['mcq', 'mc']:
            html_content += '<div class="opts">'
            for j, opt in enumerate(q.get('opts', [])):
                html_content += f'<div class="opt"><div class="opt-label">{letters[j]}</div><div class="opt-text">{opt}</div></div>'
            html_content += '</div>'
        else:
            html_content += '<div class="numerical-placeholder">[ Numerical Answer Type — enter integer value ]</div>'
            
        html_content += '</div><div style="clear:both"></div></div>'
        global_num += 1
        
    html_content += '</div>'

html_content += """
  <script>
    // Wait for MathJax to finish then we can trigger a print event if needed, but Edge headless might wait for virtual time.
  </script>
</body>
</html>
"""

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML created successfully at: {html_path}")

# Run Edge Headless
url = "file:///" + urllib.parse.quote(html_path.replace("\\", "/"))
cmd = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    "--virtual-time-budget=10000",
    f"--print-to-pdf={pdf_path}",
    url
]
print("Running Edge command:", " ".join(cmd))
subprocess.run(cmd)
print("PDF created successfully at:", pdf_path)
