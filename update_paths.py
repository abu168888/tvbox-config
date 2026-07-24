import json

with open(r"C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json", "r", encoding="utf-8") as f:
    d = json.load(f)

base = "https://abu168888.github.io/tvbox-config/"

# Replace spider path
if d.get("spider", "").startswith("./"):
    d["spider"] = base + d["spider"][2:]

# Replace live URLs
for live in d.get("lives", []):
    url = live.get("url", "")
    if url.startswith("./lib/"):
        live["url"] = base + url[2:]

# Replace site ext paths (all paths like ./lib/xxx)
for site in d.get("sites", []):
    ext = site.get("ext", "")
    if isinstance(ext, str) and ext.startswith("./lib/"):
        site["ext"] = base + ext[2:]
    elif isinstance(ext, dict):
        for k, v in ext.items():
            if isinstance(v, str) and v.startswith("./lib/"):
                ext[k] = base + v[2:]

with open(r"C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new\config.json", "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print("Done - paths updated to GitHub Pages URLs")
