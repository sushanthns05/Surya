import glob
files = glob.glob('public/templates/Register*.html') + glob.glob('public/Register*.html')
for f in files:
    content = open(f, encoding='utf-8').read()
    content = content.replace('<input type="password" id="reg-pass" required autocomplete="new-password" data-lpignore="true" data-1p-ignore>', '<input type="text" id="reg-pass" class="masked-password" required>')
    content = content.replace('<input type="password" id="reg-pass" required>', '<input type="text" id="reg-pass" class="masked-password" required>')
    open(f, 'w', encoding='utf-8').write(content)
