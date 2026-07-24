import json
import sys

config_path = 'config.json'
base_url = 'https://abu168888.github.io/tvbox-config/'

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

print(f"Original spider: {config['spider']}")

# Fix spider path
if config['spider'].startswith('./'):
    config['spider'] = base_url + config['spider'][2:]

# Fix lives
for live in config.get('lives', []):
    if live.get('url') and live['url'].startswith('./'):
        live['url'] = base_url + live['url'][2:]

# Fix site ext paths
count = 0
for site in config.get('sites', []):
    if isinstance(site.get('ext'), str) and site['ext'].startswith('./'):
        site['ext'] = base_url + site['ext'][2:]
        count += 1
    elif isinstance(site.get('ext'), dict):
        for key in site['ext']:
            if isinstance(site['ext'][key], str) and site['ext'][key].startswith('./'):
                site['ext'][key] = base_url + site['ext'][key][2:]
                count += 1

print(f"Fixed spider: {config['spider']}")
print(f"Fixed {count} site ext paths")

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("✅ Config file updated successfully!")

# Verify
with open(config_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
    
print("\nVerification - First 3 sites:")
print(json.dumps(verify['sites'][:3], indent=2, ensure_ascii=False))
