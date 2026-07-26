# -*- coding: utf-8 -*-
"""测试日报生成"""
import sys
import os
os.chdir(r'C:\Users\Administrator\AppData\Roaming\winclaw\.openclaw\workspace\tvbox-abu-new')
sys.path.insert(0, '.')

from daily_report import generate_report, format_markdown

print("=" * 60)
print("阿不 TVBox 每日工作日报 - 测试生成")
print("=" * 60)

report = generate_report()
md = format_markdown(report)

print(md)

print("\n\n*** 日报生成成功！可直接推送 ***")
