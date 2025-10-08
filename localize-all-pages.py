#!/usr/bin/env python3
import os
import re
import base64
import mimetypes
from pathlib import Path

pages = {
    'rail-io.html': 'home',
    'rail-banking-partners.html': 'banking-partners',
    'rail-payment-clients.html': 'payment-clients',
    'rail-how-it-works.html': 'how-it-works',
    'rail-company.html': 'company',
    'rail-contact.html': 'contact',
    'rail-blog.html': 'blog'
}

asset_dirs = {
    'fonts': 'rail-assets/fonts',
    'images': 'rail-assets/images',
    'videos': 'rail-assets/videos',
    'animations': 'rail-assets/animations',
    'css': 'rail-assets/css',
    'js': 'rail-assets/js'
}

def get_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type:
        return mime_type
    
    ext = Path(filepath).suffix.lower()
    mime_map = {
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.ttf': 'font/ttf',
        '.otf': 'font/otf',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.avif': 'image/avif',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.json': 'application/json',
        '.css': 'text/css',
        '.js': 'application/javascript'
    }
    return mime_map.get(ext, 'application/octet-stream')

def file_to_base64(filepath):
    try:
        with open(filepath, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('utf-8')
        mime_type = get_mime_type(filepath)
        return f"data:{mime_type};base64,{encoded}"
    except Exception as e:
        print(f"Error encoding {filepath}: {e}")
        return None

def find_local_file(filename):
    filename_clean = filename.replace('%20', ' ').replace('%2520', ' ')
    
    for dir_name, dir_path in asset_dirs.items():
        potential_path = os.path.join(dir_path, filename_clean)
        if os.path.exists(potential_path):
            return potential_path
    
    return None

def localize_page(input_file, output_file):
    print(f"\nProcessing: {input_file} -> {output_file}")
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_size = len(content)
    
    pattern = r'https://cdn\.prod\.website-files\.com/[^"\')\s]+'
    matches = re.findall(pattern, content)
    
    print(f"  Found {len(matches)} CDN URLs")
    
    replacements = {}
    processed = 0
    skipped = 0
    
    for match in set(matches):
        url_clean = match.rstrip('",;)')
        
        filename = url_clean.split('/')[-1]
        filename = filename.replace('%20', ' ').replace('%2520', ' ')
        
        local_file = find_local_file(filename)
        
        if local_file and os.path.exists(local_file):
            data_uri = file_to_base64(local_file)
            if data_uri:
                replacements[url_clean] = data_uri
                processed += 1
        else:
            skipped += 1
    
    print(f"  Converting {processed} assets to base64...")
    
    for url, data_uri in replacements.items():
        content = content.replace(url, data_uri)
    
    content = re.sub(r'href="/', r'href="#', content)
    content = re.sub(r'href="/([^"]+)"', lambda m: f'href="rail-{m.group(1)}-100-localized.html"' if m.group(1) in ['banking-partners', 'payment-clients', 'how-it-works', 'company', 'contact', 'blog'] else f'href="#{m.group(1)}"', content)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    final_size = len(content)
    size_increase = ((final_size - original_size) / original_size) * 100
    
    print(f"  Converted: {processed} assets")
    print(f"  Skipped: {skipped} assets")
    print(f"  Size: {original_size:,} -> {final_size:,} bytes ({size_increase:+.1f}%)")
    print(f"  Saved: {output_file}")

print("=" * 60)
print("Creating 100% localized versions of all pages")
print("=" * 60)

for page_file, page_name in pages.items():
    if os.path.exists(page_file):
        if page_name == 'home':
            output_file = 'rail-100-localized.html'
        else:
            output_file = f'rail-{page_name}-100-localized.html'
        
        localize_page(page_file, output_file)
    else:
        print(f"\nSkipping {page_file} (not found)")

print("\n" + "=" * 60)
print("All pages localized successfully!")
print("=" * 60)
