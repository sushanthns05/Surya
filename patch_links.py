import os

base = r'e:\Sushanth Projects\SURYA\templates'

mappings = {
    'SST.html': '/Register_SST.html',
    'SET01.html': '/Register_SET.html',
    'SET02.html': '/Register_SET.html',
    'SAT.html': '/Register_SAT.html',
    'SME.html': '/Register_SME.html',
    'SA.html': '/Register_SA.html',
    'KSSEAB.html': '/Register_Boards.html',
    'KSSSCE.html': '/Register_Boards.html',
    'KSPUEAB.html': '/Register_Boards.html'
}

for file, new_link in mappings.items():
    filepath = os.path.join(base, file)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content.replace('href="/Register.html"', f'href="{new_link}"')
        
        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {file}')
        else:
            print(f'No changes needed in {file}')
