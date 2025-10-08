#!/usr/bin/env python3
import base64
import os
import re
from pathlib import Path

def file_to_base64(filepath):
    """Convert file to base64 data URI"""
    with open(filepath, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    
    # Determine MIME type
    ext = filepath.suffix.lower()
    mime_types = {
        '.woff': 'font/woff',
        '.woff2': 'font/woff2',
        '.svg': 'image/svg+xml',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.mp4': 'video/mp4',
        '.webm': 'video/webm',
        '.json': 'application/json'
    }
    mime = mime_types.get(ext, 'application/octet-stream')
    
    return f"data:{mime};base64,{b64}"

# Read the HTML file
with open('rail-standalone.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Map URLs to local files
url_map = {
    # Fonts
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddaa_FKGroteskNeue-Regular.woff2': 'rail-assets/fonts/FKGroteskNeue-Regular.woff2',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44dd85_FKGroteskNeue-Regular.woff': 'rail-assets/fonts/FKGroteskNeue-Regular.woff',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44dd86_FKGroteskNeue-Medium.woff2': 'rail-assets/fonts/FKGroteskNeue-Medium.woff2',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddab_FKGroteskNeue-Medium.woff': 'rail-assets/fonts/FKGroteskNeue-Medium.woff',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44dd87_RecifeDisplayWeb-Regular.woff2': 'rail-assets/fonts/RecifeDisplayWeb-Regular.woff2',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44dd98_RecifeDisplayWeb-Regular.woff': 'rail-assets/fonts/RecifeDisplayWeb-Regular.woff',
    
    # Images
    'https://cdn.prod.website-files.com/62434fa732124a0fb112aab4/62434fa732124a700a12aad4_check%20circle.svg': 'rail-assets/images/check-circle.svg',
    'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac/678806b3a3c94c82025919fc_Preview%20image.svg': 'rail-assets/images/preview-image.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de07_Logo.svg': 'rail-assets/images/logo.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de13_Footer.svg': 'rail-assets/images/footer.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de14_rail.svg': 'rail-assets/images/rail.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de15_Frame%201828.svg': 'rail-assets/images/map.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de16_67804fa80e81c597eb4f5a08_Group%201669%201.svg': 'rail-assets/images/indicator-1.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de17_Testamonial%20background.svg': 'rail-assets/images/testimonial-bg.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de20_Scroll%20background.svg': 'rail-assets/images/scroll-bg.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de26_67804fa80e81c597eb4f59f5_Vector%205%201.svg': 'rail-assets/images/indicator-2.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de30_webclip.svg': 'rail-assets/images/webclip.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de31_Favicon.svg': 'rail-assets/images/favicon.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/686bed9bdd70955a9921e84f_Map_mobile.svg': 'rail-assets/images/map-mobile.svg',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddff_Mask%20group-4.png': 'rail-assets/images/mask-group-4.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de01_Mask%20group-5.png': 'rail-assets/images/mask-group-5.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de02_Mask%20group-1.png': 'rail-assets/images/mask-group-1.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de03_Mask%20group.png': 'rail-assets/images/mask-group.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de04_Mask%20group-3.png': 'rail-assets/images/mask-group-3.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de36_m.%20Scroll%20background.png': 'rail-assets/images/m-scroll-bg.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de39_m.%20Scroll%20background_blank.png': 'rail-assets/images/m-scroll-bg-blank.png',
    'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917ac8f5c215b9e436c24a_rail%20video%201-poster-00001.jpg': 'rail-assets/images/video1-poster.jpg',
    'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917adff66792c665b8c1a9_rail%20video%202-poster-00001.jpg': 'rail-assets/images/video2-poster.jpg',
    'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917ae8f7c29db00d3801a8_rail%20video%203-poster-00001.jpg': 'rail-assets/images/video3-poster.jpg',
    
    # Videos
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de3b_rail%20video%201-transcode.mp4': 'rail-assets/videos/video1.mp4',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de3b_rail%20video%201-transcode.webm': 'rail-assets/videos/video1.webm',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de3c_rail%20video%202-transcode.mp4': 'rail-assets/videos/video2.mp4',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de3c_rail%20video%202-transcode.webm': 'rail-assets/videos/video2.webm',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de3d_rail%20video%203-transcode.mp4': 'rail-assets/videos/video3.mp4',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de3d_rail%20video%203-transcode.webm': 'rail-assets/videos/video3.webm',
    
    # Animations
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de2a_Rail_02_Start_v004.json': 'rail-assets/animations/lottie-start.json',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de32_Rail_02_Loop_v007.json': 'rail-assets/animations/lottie-loop.json',
}

print("Converting assets to base64...")
converted = 0
for url, filepath in url_map.items():
    path = Path(filepath)
    if path.exists():
        try:
            data_uri = file_to_base64(path)
            html = html.replace(url, data_uri)
            converted += 1
            print(f"✓ {path.name}")
        except Exception as e:
            print(f"✗ {path.name}: {e}")
    else:
        print(f"⚠ Not found: {filepath}")

print(f"\nConverted {converted} assets")

# Remove external CSS link (already embedded)
html = re.sub(r'<link href="https://cdn\.prod\.website-files\.com/6797f43699f81adabf44dd7d/css/[^"]*" rel="stylesheet"[^>]*>', '', html)

# Remove relative links to other pages (keep them as #)
html = html.replace('href="/payment-clients"', 'href="#payment-clients"')
html = html.replace('href="/banking-partners"', 'href="#banking-partners"')
html = html.replace('href="/how-it-works"', 'href="#how-it-works"')
html = html.replace('href="/contact"', 'href="#contact"')

# Write output
with open('rail-100-localized.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\n✓ Saved to rail-100-localized.html")

# Check for remaining external URLs
remaining = re.findall(r'https://cdn\.prod\.website-files\.com/[^"\'\s)]+', html)
if remaining:
    print(f"\n⚠ WARNING: {len(set(remaining))} unique external URLs still found:")
    for url in sorted(set(remaining))[:10]:
        print(f"  - {url}")
else:
    print("\n✓ NO external CDN URLs found!")

# Additional responsive image variants
responsive_urls = {
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddff_Mask%2520group-4-p-500.png': 'rail-assets/images/mask-group-4-p-500.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44ddff_Mask%2520group-4-p-800.png': 'rail-assets/images/mask-group-4-p-800.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de01_Mask%2520group-5-p-500.png': 'rail-assets/images/mask-group-5-p-500.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de01_Mask%2520group-5-p-800.png': 'rail-assets/images/mask-group-5-p-800.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de02_Mask%2520group-1-p-500.png': 'rail-assets/images/mask-group-1-p-500.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de02_Mask%2520group-1-p-800.png': 'rail-assets/images/mask-group-1-p-800.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de03_Mask%2520group-p-500.png': 'rail-assets/images/mask-group-p-500.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de03_Mask%2520group-p-800.png': 'rail-assets/images/mask-group-p-800.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de04_Mask%2520group-3-p-500.png': 'rail-assets/images/mask-group-3-p-500.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de04_Mask%2520group-3-p-800.png': 'rail-assets/images/mask-group-3-p-800.png',
    'https://cdn.prod.website-files.com/6797f43699f81adabf44dd7d/6797f43699f81adabf44de04_Mask%2520group-3-p-1080.png': 'rail-assets/images/mask-group-3-p-1080.png',
}
url_map.update(responsive_urls)
