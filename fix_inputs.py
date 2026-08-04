import glob
files = glob.glob('public/Register*.html') + ['public/templates/SEOAS_Base.html']
for f in files:
    content = open(f, encoding='utf-8').read()
    content = content.replace('<input type="password"', '<input type="password" style="pointer-events: auto !important; z-index: 9999 !important; position: relative !important; cursor: text !important;"')
    open(f, 'w', encoding='utf-8').write(content)
