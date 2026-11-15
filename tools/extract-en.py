# -*- coding: utf-8 -*-
"""导出 app/ui 中可能面向用户的英文候选串，便于补译。

用法: python tools/extract-en.py [app/ui 目录] > en.json
"""
import json, os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "ui")
WORDY = re.compile(r"^[A-Za-z][A-Za-z0-9 ,.'!?:;()/&+%\-]{2,79}$")
SKIP = {"SwiftDL", "OK", "MP4", "MB", "GB", "KB", "aria2", "yt-dlp", "ffmpeg"}


def keep(v: str) -> bool:
    v = v.strip()
    if not v or v in SKIP:
        return False
    if not WORDY.match(v):
        return False
    if not re.search(r"[A-Za-z]{3,}", v):
        return False
    return True


def scan(rel: str) -> list:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        return []
    text = open(path, encoding="utf-8").read()
    found = set()
    for m in re.finditer(r">([^<>{}]{2,120})<", text):          # HTML 文本节点
        if keep(m.group(1)):
            found.add(m.group(1).strip())
    for m in re.finditer(r"""["']([^"'\\\n]{3,120})["']""", text):  # 字符串字面量
        if keep(m.group(1)):
            found.add(m.group(1).strip())
    return sorted(found)


report = {}
for name in ["index.html", "download.html", "remote.html"]:
    r = scan(name)
    if r:
        report[name] = r
srcdir = os.path.join(ROOT, "src")
if os.path.isdir(srcdir):
    for f in sorted(os.listdir(srcdir)):
        if f.endswith(".ts"):
            r = scan(os.path.join("src", f))
            if r:
                report["src/" + f] = r
print(json.dumps(report, ensure_ascii=False, indent=1))
