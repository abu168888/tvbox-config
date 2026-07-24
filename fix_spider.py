import json

config_path = 'config.json'
base_url = 'https://abu168888.github.io/tvbox-config/'

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Fix spider path to use actual filename on GitHub
config['spider'] = base_url + 'spider.jar'

print(f"Updated spider to: {config['spider']}")

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print("✅ Spider path fixed!")
