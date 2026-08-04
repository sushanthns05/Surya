import glob
files = glob.glob('public/Register*.html') + ['public/templates/SEOAS_Base.html']
for f in files:
    content = open(f, encoding='utf-8').read()
    content = content.replace('<label>Password</label>', '<label for="reg-pass">Password</label>')
    content = content.replace('<label>Confirm Password</label>', '<label for="reg-pass2">Confirm Password</label>')
    open(f, 'w', encoding='utf-8').write(content)
