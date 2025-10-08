import re

splide_b64_file = "/home/azureuser/replica/splide.min.js.b64"
cmsfilter_b64_file = "/home/azureuser/replica/cmsfilter.js.b64"

html_files = [
    "/home/azureuser/replica/rail-100-localized.html",
    "/home/azureuser/replica/rail-banking-partners-100-localized.html",
    "/home/azureuser/replica/rail-blog-100-localized.html",
    "/home/azureuser/replica/rail-company-100-localized.html",
    "/home/azureuser/replica/rail-contact-100-localized.html",
    "/home/azureuser/replica/rail-how-it-works-100-localized.html",
    "/home/azureuser/replica/rail-payment-clients-100-localized.html"
]

with open(splide_b64_file, 'r') as f:
    splide_base64 = f.read().strip()

with open(cmsfilter_b64_file, 'r') as f:
    cmsfilter_base64 = f.read().strip()

splide_pattern = re.compile(
    r'<script\s+src="https://cdn\.jsdelivr\.net/npm/@splidejs/splide@4\.1\.4/dist/js/splide\.min\.js"[^>]*></script>'
)
cmsfilter_pattern = re.compile(
    r'<script\s+async\s+src="https://cdn\.jsdelivr\.net/npm/@finsweet/attributes-cmsfilter@1/cmsfilter\.js"[^>]*></script>'
)

splide_replacement = f'<script src="data:text/javascript;base64,{splide_base64}"></script>'
cmsfilter_replacement = f'<script src="data:text/javascript;base64,{cmsfilter_base64}"></script>'

for html_file in html_files:
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = splide_pattern.sub(splide_replacement, content)
    new_content = cmsfilter_pattern.sub(cmsfilter_replacement, new_content)
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated: {html_file}")

print("All remaining scripts embedded successfully!")
