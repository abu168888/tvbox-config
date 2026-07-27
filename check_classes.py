import zipfile
import os

jar_path = "spider_local.jar"

with zipfile.ZipFile(jar_path, 'r') as z:
    names = z.namelist()
    print("Total files:", len(names))
    print("\n=== All files in spider.jar ===")
    for n in names:
        size = z.getinfo(n).file_size
        print("  %s (%d bytes)" % (n, size))
    
    # 检查 assets 目录
    assets = [n for n in names if n.startswith('assets/')]
    print("\n=== Asset files (%d) ===" % len(assets))
    for a in assets:
        size = z.getinfo(a).file_size
        print("  %s (%d bytes)" % (a, size))
    
    # 检查 META-INF
    meta = [n for n in names if n.startswith('META-INF/')]
    print("\n=== META-INF files (%d) ===" % len(meta))
    for m in meta:
        size = z.getinfo(m).file_size
        print("  %s (%d bytes)" % (m, size))
