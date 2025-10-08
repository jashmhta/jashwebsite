#!/usr/bin/env python3
import os
import re
import urllib.parse
import subprocess
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

def extract_assets_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    pattern = r'https://cdn\.prod\.website-files\.com/[^"\')\s]+'
    matches = re.findall(pattern, content)
    
    cleaned = []
    for match in matches:
        match = match.rstrip('",;)')
        if match not in cleaned:
            cleaned.append(match)
    
    return cleaned

print("Extracting all assets from all pages...")
all_assets = set()

for page_file in pages.keys():
    if os.path.exists(page_file):
        assets = extract_assets_from_file(page_file)
        all_assets.update(assets)
        print(f"  {page_file}: {len(assets)} asset references")

print(f"\nTotal unique assets: {len(all_assets)}")

asset_dirs = {
    'fonts': 'rail-assets/fonts',
    'images': 'rail-assets/images',
    'videos': 'rail-assets/videos',
    'animations': 'rail-assets/animations',
    'css': 'rail-assets/css',
    'js': 'rail-assets/js'
}

for dir_path in asset_dirs.values():
    os.makedirs(dir_path, exist_ok=True)

def categorize_asset(url):
    lower_url = url.lower()
    if any(ext in lower_url for ext in ['.woff', '.woff2', '.ttf', '.otf']):
        return 'fonts'
    elif any(ext in lower_url for ext in ['.mp4', '.webm', '.mov']):
        return 'videos'
    elif 'lottie' in lower_url or '.json' in lower_url:
        return 'animations'
    elif '.css' in lower_url:
        return 'css'
    elif '.js' in lower_url:
        return 'js'
    else:
        return 'images'

def get_filename_from_url(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    filename = path.split('/')[-1]
    filename = urllib.parse.unquote(filename)
    filename = filename.replace('%20', ' ').replace('%2520', ' ')
    return filename

print("\nDownloading assets...")
downloaded = []
failed = []

for i, asset_url in enumerate(sorted(all_assets), 1):
    category = categorize_asset(asset_url)
    filename = get_filename_from_url(asset_url)
    dest_dir = asset_dirs[category]
    dest_path = os.path.join(dest_dir, filename)
    
    if os.path.exists(dest_path):
        print(f"  [{i}/{len(all_assets)}] Already exists: {filename}")
        downloaded.append((asset_url, dest_path))
        continue
    
    try:
        print(f"  [{i}/{len(all_assets)}] Downloading: {filename}")
        result = subprocess.run(
            ['curl', '-s', '-L', '-o', dest_path, asset_url],
            capture_output=True,
            timeout=60
        )
        
        if result.returncode == 0 and os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
            downloaded.append((asset_url, dest_path))
        else:
            failed.append(asset_url)
            print(f"    FAILED: {asset_url}")
    except Exception as e:
        failed.append(asset_url)
        print(f"    ERROR: {e}")

print(f"\nDownload complete: {len(downloaded)} succeeded, {len(failed)} failed")

if failed:
    print("\nFailed downloads:")
    for url in failed:
        print(f"  - {url}")

print("\nAsset download complete!")
print(f"Total assets downloaded: {len(downloaded)}")
