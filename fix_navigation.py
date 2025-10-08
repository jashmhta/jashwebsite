import re
import glob

# Mapping of anchor links to actual file paths
nav_mapping = {
    'href="#payment-clients"': 'href="rail-payment-clients-100-localized.html"',
    'href="#banking-partners"': 'href="rail-banking-partners-100-localized.html"',
    'href="#how-it-works"': 'href="rail-how-it-works-100-localized.html"',
    'href="/"': 'href="home.html"',
    'href="https://rail.io/"': 'href="home.html"',
    'href="https://www.rail.io/"': 'href="home.html"',
}

# Get all localized HTML files
files = glob.glob('/home/azureuser/replica/*-100-localized.html')
files.append('/home/azureuser/replica/home.html')

for filepath in files:
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Track changes
    changes_made = 0
    
    # Apply all navigation mappings
    for old_href, new_href in nav_mapping.items():
        old_count = content.count(old_href)
        if old_count > 0:
            content = content.replace(old_href, new_href)
            changes_made += old_count
            print(f"  - Replaced '{old_href}' → '{new_href}' ({old_count} times)")
    
    # Write back if changes were made
    if changes_made > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Saved {changes_made} changes\n")
    else:
        print(f"  - No navigation links found to update\n")

print("Navigation fix complete!")
