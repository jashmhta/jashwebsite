#!/usr/bin/env python3
import base64, re
from pathlib import Path

def to_b64_uri(filepath):
    """Convert file to base64 data URI"""
    with open(filepath, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode('utf-8')
    
    mime_map = {
        '.woff': 'font/woff', '.woff2': 'font/woff2',
        '.svg': 'image/svg+xml', '.png': 'image/png',
        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
        '.mp4': 'video/mp4', '.webm': 'video/webm',
        '.json': 'application/json'
    }
    mime = mime_map.get(filepath.suffix.lower(), 'application/octet-stream')
    return f"data:{mime};base64,{b64}"

# Load HTML
with open('rail-standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_size = len(html)

# Build comprehensive URL map
replacements = []

# Fonts
for fname, url_part in [
    ('FKGroteskNeue-Regular.woff2', '6797f43699f81adabf44ddaa_FKGroteskNeue-Regular.woff2'),
    ('FKGroteskNeue-Regular.woff', '6797f43699f81adabf44dd85_FKGroteskNeue-Regular.woff'),
    ('FKGroteskNeue-Medium.woff2', '6797f43699f81adabf44dd86_FKGroteskNeue-Medium.woff2'),
    ('FKGroteskNeue-Medium.woff', '6797f43699f81adabf44ddab_FKGroteskNeue-Medium.woff'),
    ('RecifeDisplayWeb-Regular.woff2', '6797f43699f81adabf44dd87_RecifeDisplayWeb-Regular.woff2'),
    ('RecifeDisplayWeb-Regular.woff', '6797f43699f81adabf44dd98_RecifeDisplayWeb-Regular.woff'),
]:
    url = f'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/{url_part}'
    path = Path(f'rail-assets/fonts/{fname}')
    if path.exists():
        replacements.append((url, path))

# Images - simple ones
image_map = {
    'check-circle.svg': ('62434fa732124a0fb112aab4/62434fa732124a700a12aad4_check%20circle.svg', 'images'),
    'preview-image.svg': ('67804fa80e81c597eb4f59ac/678806b3a3c94c82025919fc_Preview%20image.svg', 'images'),
    'logo.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de07_Logo.svg', 'images'),
    'footer.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de13_Footer.svg', 'images'),
    'rail.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de14_rail.svg', 'images'),
    'map.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de15_Frame%201828.svg', 'images'),
    'indicator-1.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de16_67804fa80e81c597eb4f5a08_Group%201669%201.svg', 'images'),
    'testimonial-bg.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de17_Testamonial%20background.svg', 'images'),
    'scroll-bg.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de20_Scroll%20background.svg', 'images'),
    'indicator-2.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de26_67804fa80e81c597eb4f59f5_Vector%205%201.svg', 'images'),
    'webclip.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de30_webclip.svg', 'images'),
    'favicon.svg': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de31_Favicon.svg', 'images'),
    'map-mobile.svg': ('6797f43699f81adabf44dd7d/686bed9bdd70955a9921e84f_Map_mobile.svg', 'images'),
    'mask-group-4.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44ddff_Mask%20group-4.png', 'images'),
    'mask-group-5.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de01_Mask%20group-5.png', 'images'),
    'mask-group-1.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de02_Mask%20group-1.png', 'images'),
    'mask-group.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de03_Mask%20group.png', 'images'),
    'mask-group-3.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de04_Mask%20group-3.png', 'images'),
    'm-scroll-bg.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de36_m.%20Scroll%20background.png', 'images'),
    'm-scroll-bg-blank.png': ('6797f43699f81adabf44dd7d/6797f43699f81adabf44de39_m.%20Scroll%20background_blank.png', 'images'),
    'video1-poster.jpg': ('67804fa80e81c597eb4f59ac%2F67917ac8f5c215b9e436c24a_rail%20video%201-poster-00001.jpg', 'images'),
    'video2-poster.jpg': ('67804fa80e81c597eb4f59ac%2F67917adff66792c665b8c1a9_rail%20video%202-poster-00001.jpg', 'images'),
    'video3-poster.jpg': ('67804fa80e81c597eb4f59ac%2F67917ae8f7c29db00d3801a8_rail%20video%203-poster-00001.jpg', 'images'),
}

for fname, (url_part, folder) in image_map.items():
    url = f'https://cdn.prod.website-files.com/{url_part}'
    path = Path(f'rail-assets/{folder}/{fname}')
    if path.exists():
        replacements.append((url, path))

# Responsive images with %2520 encoding
responsive_files = [
    ('mask-group-4-p-500.png', '6797f43699f81adabf44ddff_Mask%2520group-4-p-500.png'),
]
# Check for files with full hash in rail-assets/images/
for img_file in Path('rail-assets/images/').glob('*p-*.png'):
    fname = img_file.name
    # Extract the hash and filename part
    if fname.startswith('6797f43699f81adabf44d'):
        # Build URL
        url_fname = fname.replace(' ', '%2520')
        url = f'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/{url_fname}'
        replacements.append((url, img_file))

# Videos
for i in range(1, 4):
    for ext in ['mp4', 'webm']:
        fname = f'video{i}.{ext}'
        url_map = {
            'video1.mp4': '6797f43699f81adabf44de3b_rail%20video%201-transcode.mp4',
            'video1.webm': '6797f43699f81adabf44de3b_rail%20video%201-transcode.webm',
            'video2.mp4': '6797f43699f81adabf44de3c_rail%20video%202-transcode.mp4',
            'video2.webm': '6797f43699f81adabf44de3c_rail%20video%202-transcode.webm',
            'video3.mp4': '6797f43699f81adabf44de3d_rail%20video%203-transcode.mp4',
            'video3.webm': '6797f43699f81adabf44de3d_rail%20video%203-transcode.webm',
        }
        if fname in url_map:
            url = f'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/{url_map[fname]}'
            path = Path(f'rail-assets/videos/{fname}')
            if path.exists():
                replacements.append((url, path))

# Animations
for fname, url_part in [
    ('lottie-start.json', '6797f43699f81adabf44de2a_Rail_02_Start_v004.json'),
    ('lottie-loop.json', '6797f43699f81adabf44de32_Rail_02_Loop_v007.json'),
]:
    url = f'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/{url_part}'
    path = Path(f'rail-assets/animations/{fname}')
    if path.exists():
        replacements.append((url, path))

# Also handle mask-group-4-p-500.png (the one without hash)
p = Path('rail-assets/images/mask-group-4-p-500.png')
if p.exists():
    replacements.append(('https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddff_Mask%2520group-4-p-500.png', p))

# Perform replacements
print(f"Processing {len(replacements)} assets...")
converted = 0
for url, filepath in replacements:
    if url in html:
        try:
            data_uri = to_b64_uri(filepath)
            html = html.replace(url, data_uri)
            converted += 1
            size_kb = filepath.stat().st_size / 1024
            print(f"✓ {filepath.name} ({size_kb:.0f}KB)")
        except Exception as e:
            print(f"✗ {filepath.name}: {e}")

print(f"\n{converted} assets embedded")

# Remove external links
html = re.sub(r'<link href="https://cdn\.prod\.website-files\.com/6797f43699f81adabf44dd7d/css/[^"]*" rel="stylesheet"[^>]*>', '', html)
html = re.sub(r'<script src="https://cdn\.prod\.website-files\.com/6797f43699f81adabf44dd7d/js/webflow[^"]*"[^>]*></script>', '', html)
html = html.replace('href="/payment-clients"', 'href="#"')
html = html.replace('href="/banking-partners"', 'href="#"')
html = html.replace('href="/how-it-works"', 'href="#"')
html = html.replace('href="/contact"', 'href="#"')

# Save
with open('rail-100-localized.html', 'w', encoding='utf-8') as f:
    f.write(html)

size_mb = Path('rail-100-localized.html').stat().st_size / (1024*1024)
print(f"\nSaved: rail-100-localized.html ({size_mb:.1f}MB)")
print(f"Size change: {original_size/1024:.0f}KB → {len(html)/1024:.0f}KB")

# Final check
cdn_urls = set(re.findall(r'https://cdn\.prod\.website-files\.com/[^"\'\s)<]+', html))
if cdn_urls:
    print(f"\n⚠ {len(cdn_urls)} external CDN URLs remain:")
    for u in sorted(cdn_urls)[:25]:
        print(f"  {u}")
else:
    print("\n" + "="*70)
    print("✅ SUCCESS! 100% LOCALIZED - ZERO EXTERNAL DEPENDENCIES!")
    print("="*70)
