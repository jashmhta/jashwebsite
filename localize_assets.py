#!/usr/bin/env python3
"""
Replace external CDN URLs with local asset paths and remove external links
"""
import re
import sys

def localize_html(filepath):
    """Replace external URLs with local paths in HTML file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    replacements_made = 0
    
    # Remove external doc/legal links
    external_links = [
        'https://docs.rail.io/',
        'https://docs.rail.io/guides/assets/',
        'https://legal.rail.io/legal/platformagreement/',
    ]
    
    for link in external_links:
        if link in content:
            # Remove from nav links - replace entire <a> tag
            content = re.sub(
                rf'<a[^>]*href="{re.escape(link)}"[^>]*>.*?</a>',
                '',
                content,
                flags=re.DOTALL
            )
            replacements_made += 1
    
    # Remove tracking scripts (Google Analytics, LinkedIn)
    tracking_patterns = [
        r'<script[^>]*src="https://www\.googletagmanager\.com/gtag/js[^"]*"[^>]*></script>',
        r'<script[^>]*src="https://snap\.licdn\.com/li\.lms-analytics/insight\.min\.js"[^>]*></script>',
        r'<img[^>]*src="https://px\.ads\.linkedin\.com/collect/[^"]*"[^>]*>',
        r'<script[^>]*>.*?gtag\(.*?\).*?</script>',
        r'b\.src\s*=\s*"https://snap\.licdn\.com/li\.lms-analytics/insight\.min\.js";',
        r'_linkedin_partner_id\s*=\s*"[^"]*";',
        r'window\._linkedin_data_partner_ids\s*=\s*window\._linkedin_data_partner_ids\s*\|\|\s*\[\];',
        r'window\._linkedin_data_partner_ids\.push\(_linkedin_partner_id\);',
    ]
    
    for pattern in tracking_patterns:
        matches = re.findall(pattern, content, flags=re.DOTALL)
        if matches:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
            replacements_made += len(matches)
    
    # Replace poster URLs (with and without &quot; suffix)
    poster_replacements = {
        'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917ac8f5c215b9e436c24a_rail%20video%201-poster-00001.jpg': 'assets/images/67917ac8f5c215b9e436c24a_rail video 1-poster-00001.jpg',
        'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917adff66792c665b8c1a9_rail%20video%202-poster-00001.jpg': 'assets/images/67917adff66792c665b8c1a9_rail video 2-poster-00001.jpg',
        'https://cdn.prod.website-files.com/67804fa80e81c597eb4f59ac%2F67917ae8f7c29db00d3801a8_rail%20video%203-poster-00001.jpg': 'assets/images/67917ae8f7c29db00d3801a8_rail video 3-poster-00001.jpg',
    }
    
    for old_url, new_path in poster_replacements.items():
        # Replace both with and without &quot; suffix
        if old_url in content:
            content = content.replace(old_url, new_path)
            replacements_made += 1
        if f'{old_url}&quot;)' in content:
            content = content.replace(f'{old_url}&quot;)', f'{new_path}&quot;)')
            replacements_made += 1
    
    # Write back if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ {filepath}: {replacements_made} replacements made")
        return True
    else:
        print(f"- {filepath}: No changes needed")
        return False

def main():
    html_files = [
        '/home/azureuser/replica/home.html',
        '/home/azureuser/replica/rail-payment-clients-100-localized.html',
        '/home/azureuser/replica/rail-banking-partners-100-localized.html',
        '/home/azureuser/replica/rail-how-it-works-100-localized.html',
        '/home/azureuser/replica/rail-company-100-localized.html',
        '/home/azureuser/replica/rail-blog-100-localized.html',
        '/home/azureuser/replica/rail-contact-100-localized.html',
    ]
    
    total_updated = 0
    for html_file in html_files:
        if localize_html(html_file):
            total_updated += 1
    
    print(f"\n✓ Complete: {total_updated}/{len(html_files)} files updated")

if __name__ == '__main__':
    main()
