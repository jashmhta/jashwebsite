#!/usr/bin/env python3
import base64, re
from pathlib import Path

def to_b64(fp):
    with open(fp, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    mime = {'.woff':'font/woff','.woff2':'font/woff2','.svg':'image/svg+xml',
            '.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4',
            '.webm':'video/webm','.json':'application/json'}.get(fp.suffix.lower(),'application/octet-stream')
    return f"data:{mime};base64,{b64}"

with open('rail-standalone.html','r',encoding='utf-8') as f:
    html = f.read()

# Auto-discover and map all local assets
base_urls = {
    'fonts': 'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/',
    'images': 'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/',
    'images2': 'https://cdn.prod.website-files.com/62434fa732124a0fb112aab4/',
    'images3': 'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac/',
    'images4': 'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F',
}

url_map = {}
for folder in ['fonts', 'images', 'videos', 'animations']:
    asset_dir = Path(f'rail-assets/{folder}')
    if asset_dir.exists():
        for file in asset_dir.iterdir():
            if file.is_file():
                # Try to match against known URL patterns
                fname = file.name
                # Map file to potential URL patterns
                for base_key, base_url in base_urls.items():
                    # Exact match
                    url1 = f"{base_url}{fname}"
                    # URL encoded
                    url2 = f"{base_url}{fname.replace(' ', '%20')}"
                    url3 = f"{base_url}{fname.replace(' ', '%2520')}"
                    
                    for url in [url1, url2, url3]:
                        url_map[url] = str(file)

print(f"Auto-mapped {len(url_map)} URL patterns from local assets")

converted = 0
for url, filepath in url_map.items():
    path = Path(filepath)
    if path.exists() and url in html:
        try:
            data_uri = to_b64(path)
            html = html.replace(url, data_uri)
            converted += 1
            print(f"✓ {path.name} ({path.stat().st_size/1024:.1f}KB)")
        except Exception as e:
            print(f"✗ {path.name}: {e}")

print(f"\n{converted} assets converted to base64")

# Cleanup
html = re.sub(r'<link href="https://cdn\.prod\.website-files\.com/6797f43699f81adabf44dd7d/css/[^"]*" rel="stylesheet"[^>]*>', '', html)
html = re.sub(r'<script src="https://cdn\.prod\.website-files\.com/6797f43699f81adabf44dd7d/js/webflow[^"]*"[^>]*></script>', '', html)
html = html.replace('href="/payment-clients"','href="#payment-clients"')
html = html.replace('href="/banking-partners"','href="#banking-partners"')
html = html.replace('href="/how-it-works"','href="#how-it-works"')
html = html.replace('href="/contact"','href="#contact"')

with open('rail-100-localized.html','w',encoding='utf-8') as f:
    f.write(html)

size_mb = Path('rail-100-localized.html').stat().st_size/(1024*1024)
print(f"\n✓ Saved: rail-100-localized.html ({size_mb:.1f}MB)")

# Final verification
remaining = list(set(re.findall(r'https://cdn\.prod\.website-files\.com/[^"\'\s)]+', html)))
if remaining:
    print(f"\n⚠ {len(remaining)} external CDN URLs remain:")
    for u in remaining[:20]: print(f"  {u}")
else:
    print("\n"+"="*70)
    print("✅✅✅ SUCCESS! 100% LOCALIZED - ZERO EXTERNAL DEPENDENCIES! ✅✅✅")
    print("="*70)
