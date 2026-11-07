#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''检查 docs 下的相对 Markdown 链接是否存在。'''
import re
import sys
from pathlib import Path


def main(root="docs"):
    base = Path(root)
    bad = []
    for md in base.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"\[[^\]]+\]\(([^)]+\.md)(?:#[^)]*)?\)", text):
            raw = m.group(1)
            if raw.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = (md.parent / raw).resolve()
            if not target.exists():
                bad.append(f"{md}: {m.group(1)}")
    if bad:
        print("\n".join(bad))
        sys.exit(1)
    print("links OK")


if __name__ == "__main__":
    main(*sys.argv[1:])
