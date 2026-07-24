import json

config_path = 'config.json'

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Replace all "王二小" with "阿不"
replacements = [
    ('王二小放牛娃牛逼', '阿布 TVBox'),  # wallpaper domain
    ('王二小放牛娃', '阿不 TVBox'),      # UI display names
    ('二小', '阿不'),                     # short references
]

# Fix wallpaper URL
if 'wallpaper' in config:
    for old, new in replacements:
        config['wallpaper'] = config['wallpaper'].replace(old, new)

# Fix site names
for site in config.get('sites', []):
    if 'name' in site:
        for old, new in replacements:
            site['name'] = site['name'].replace(old, new)

print("✅ Brand replacement complete!")
print(f"Wallpaper: {config.get('wallpaper')}")

# Show first few changed sites
count = 0
for site in config.get('sites', []):
    if '阿不' in site.get('name', '') and count < 3:
        print(f"Site: {site['name']}")
        count += 1

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("\n📝 Config updated successfully!")
