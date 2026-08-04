f='public/templates/SEOAS_Base.html'; content = open(f, encoding='utf-8').read(); open(f, 'w', encoding='utf-8').write(content.replace('seoas.css', 'seoas.css?v=3'))
