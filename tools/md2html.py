#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 fish/docs 下的 Markdown 转成可浏览的 HTML 站点（轻量渲染，无第三方依赖）。"""
import html
import re
from pathlib import Path

import sys
DOCS = Path(sys.argv[1] if len(sys.argv) > 1 else "docs")
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else DOCS / "_html"

CSS = """
:root{--fg:#1f2937;--muted:#6b7280;--bg:#fafbfc;--card:#fff;--line:#e5e7eb;--accent:#0b6bcb;--code:#f3f4f6}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.85 -apple-system,"Microsoft YaHei",Segoe UI,sans-serif}
header{position:sticky;top:0;background:rgba(255,255,255,.92);border-bottom:1px solid var(--line);padding:10px 18px;backdrop-filter:blur(6px);z-index:9}
header a{color:var(--accent);text-decoration:none;font-weight:600}
main{max-width:920px;margin:0 auto;padding:28px 20px 80px}
h1,h2,h3,h4{line-height:1.35;margin:1.4em 0 .6em}
h1{font-size:1.9em;border-bottom:2px solid var(--line);padding-bottom:.3em}
h2{font-size:1.4em;border-bottom:1px solid var(--line);padding-bottom:.2em}
h3{font-size:1.15em}
a{color:var(--accent)}
code{background:var(--code);padding:2px 6px;border-radius:5px;font:13.5px/1.5 Consolas,monospace}
pre{background:#0f172a;color:#e2e8f0;padding:16px 18px;border-radius:10px;overflow:auto;font:13.5px/1.6 Consolas,monospace}
pre code{background:none;padding:0;color:inherit}
table{border-collapse:collapse;width:100%;margin:1em 0;background:var(--card);font-size:14.5px}
th,td{border:1px solid var(--line);padding:8px 10px;text-align:left;vertical-align:top}
th{background:#f1f5f9}
blockquote{margin:1em 0;padding:.6em 1em;border-left:4px solid var(--accent);background:#eef6ff;color:#334155;border-radius:0 8px 8px 0}
ul,ol{padding-left:1.4em}
li{margin:.25em 0}
hr{border:none;border-top:1px solid var(--line);margin:2em 0}
footer{max-width:920px;margin:0 auto;padding:0 20px 40px;color:var(--muted);font-size:13px}
.meta{color:var(--muted);font-size:13px;margin-bottom:1.2em}
"""


def slug(text: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff -]", "", text.strip())
    return re.sub(r"\s+", "-", s)[:60] or "section"


def inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m.group(2)[:-3] + ".html" if m.group(2).endswith(".md") and not m.group(2).startswith("http") else m.group(2)}">{m.group(1)}</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def join_para(lines):
    s = " ".join(lines)
    s = re.sub(r"([\u4e00-\u9fff，。；：！？、）」』]) (?=[\u4e00-\u9fff（「『])", r"\1", s)
    return s


def render_table(rows):
    head = rows[0]
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    out = ["<table><thead><tr>"]
    out += [f"<th>{inline(c)}</th>" for c in cells[0]]
    out.append("</tr></thead><tbody>")
    for row in cells[1:]:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "\n".join(out)


def render_list(lines, indent=0):
    out = ["<ul>"] if not re.match(r"^\s*\d+\.", lines[0]) else ["<ol>"]
    i = 0
    while i < len(lines):
        m = re.match(r"^(\s*)(?:[-*+]|\d+\.)\s+(.*)$", lines[i])
        if not m:
            out.append(inline(lines[i].strip()))
            i += 1
            continue
        cur_indent = len(m.group(1))
        content = m.group(2)
        i += 1
        children = []
        while i < len(lines) and len(re.match(r"^(\s*)", lines[i]).group(1)) > cur_indent and re.match(r"^\s*(?:[-*+]|\d+\.)\s+", lines[i]):
            children.append(lines[i])
            i += 1
        if children:
            out.append(f"<li>{inline(content)}\n{render_list(children, cur_indent + 2)}</li>")
        else:
            out.append(f"<li>{inline(content)}</li>")
    out.append("</ul>" if out[0] == "<ul>" else "</ol>")
    return "\n".join(out)


def md_to_html(text: str, title: str) -> str:
    lines = text.replace("\r\n", "\n").split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            t = m.group(2).strip()
            out.append(f'<h{level} id="{slug(t)}">{inline(t)}</h{level}>')
            i += 1
            continue
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue
        if line.startswith("> "):
            buf = []
            while i < len(lines) and (lines[i].startswith("> ") or lines[i].strip() == ">"):
                buf.append(lines[i][2:] if lines[i].startswith("> ") else "")
                i += 1
            out.append("<blockquote>" + inline(join_para(buf)) + "</blockquote>")
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:-]+\|", lines[i + 1] + "|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(render_table(rows))
            continue
        if re.match(r"^\s*(?:[-*+]|\d+\.)\s+", line):
            buf = []
            while i < len(lines) and (re.match(r"^\s*(?:[-*+]|\d+\.)\s+", lines[i]) or (buf and re.match(r"^\s{2,}\S", lines[i]))):
                buf.append(lines[i])
                i += 1
            out.append(render_list(buf))
            continue
        if line.strip() == "":
            i += 1
            continue
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() != "" and not re.match(r"^(#{1,6})\s|^```|^---+\s*$|^\|", lines[i]) and not re.match(r"^\s*(?:[-*+]|\d+\.)\s+", lines[i]) and not lines[i].startswith("> "):
            buf.append(lines[i])
            i += 1
        out.append("<p>" + inline(join_para([b.strip() for b in buf])) + "</p>")
    body = "\n".join(out)
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head><body>
<header><a href="index.html">← 大肥鱼文档中心</a></header>
<main><h1>{html.escape(title)}</h1>
{body}
</main><footer>大肥鱼文档中心 · 2026-11-07</footer></body></html>"""


def main():
    if OUT.exists():
        import shutil
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    md_files = [p for p in DOCS.rglob("*.md") if "_html" not in p.parts]
    pages = []
    for p in md_files:
        rel = p.relative_to(DOCS)
        text = p.read_text(encoding="utf-8")
        title = ""
        m = re.search(r"^#\s+(.+)$", text, re.M)
        if m:
            title = m.group(1).strip()
        html_text = md_to_html(text, title or p.stem)
        if rel.as_posix() == "README.md":
            out_rel = "index.html"
        else:
            out_rel = rel.with_suffix(".html").as_posix()
        dst = OUT / out_rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(html_text, encoding="utf-8")
        pages.append((out_rel, title or p.stem))
    # 索引页（如果 README 已生成 index.html，就补一个导航列表）
    extra = "\n".join(f'<li><a href="{u}">{html.escape(t)}</a></li>' for u, t in pages if u != "index.html")
    index = OUT / "index.html"
    if index.exists():
        base = index.read_text(encoding="utf-8")
        base = base.replace("</main>", f"<h2>全部页面</h2><ul>{extra}</ul></main>")
        index.write_text(base, encoding="utf-8")
    print(f"生成 {len(pages)} 个页面 -> {OUT}")


if __name__ == "__main__":
    main()
