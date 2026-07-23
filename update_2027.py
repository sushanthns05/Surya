# -*- coding: utf-8 -*-
import os
import glob

def update_files():
    files = glob.glob('templates/*.html') + glob.glob('*.csv') + glob.glob('*.html') + ['build_static.py']
    changed_files = 0
    
    for filepath in files:
        if not os.path.exists(filepath): continue
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace('2025-26', '2026-27')
        new_content = new_content.replace('2025–26', '2026-27')
        new_content = new_content.replace('2026', '2027')
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {filepath}')
            changed_files += 1
            
    print(f'Done. Changed {changed_files} files.')

if __name__ == '__main__':
    update_files()
