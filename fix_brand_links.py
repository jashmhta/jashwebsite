import glob

files = glob.glob('/home/azureuser/replica/*-100-localized.html')
files.append('/home/azureuser/replica/home.html')

for filepath in files:
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix brand/logo link to go to home
    original = content
    content = content.replace('class="brand w-nav-brand', 'href="home.html" class="brand w-nav-brand')
    
    # Also fix any standalone brand links
    content = content.replace('<a href="#" aria-current="page" class="brand w-nav-brand', '<a href="home.html" class="brand w-nav-brand')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed brand link\n")
    else:
        print(f"  - No brand link changes needed\n")

print("Brand link fix complete!")
