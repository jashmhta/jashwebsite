import re
import sys

jquery_b64_file = "/home/azureuser/replica/jquery-3.5.1.min.js.b64"
html_files = [
    "/home/azureuser/replica/rail-100-localized.html",
    "/home/azureuser/replica/rail-banking-partners-100-localized.html",
    "/home/azureuser/replica/rail-blog-100-localized.html",
    "/home/azureuser/replica/rail-company-100-localized.html",
    "/home/azureuser/replica/rail-contact-100-localized.html",
    "/home/azureuser/replica/rail-how-it-works-100-localized.html",
    "/home/azureuser/replica/rail-payment-clients-100-localized.html"
]

with open(jquery_b64_file, 'r') as f:
    jquery_base64 = f.read().strip()

jquery_pattern = re.compile(
    r'<script src="https://d3e54v103j8qbb\.cloudfront\.net/js/jquery-3\.5\.1\.min\.dc5e7f18c8\.js[^"]*"[^>]*></script>'
)

jquery_replacement = f'<script src="data:text/javascript;base64,{jquery_base64}"></script>'

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = jquery_pattern.sub(jquery_replacement, content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated: {html_file}")

print("All files updated successfully!")
