#!/usr/bin/env python3
"""Second site-map design: a single A3 tree diagram.

Same data source as make-sitemap.py (tools/build.py), different drawing:
one sheet, elbow-connected branches, products as chips under each line.
Writes tools/sitemap-tree-page.html for tools/make-sitemap-tree.mjs to print.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def e(s): return html.escape(str(s))

def leaf(title, url, note=""):
    return (f'<li class="leaf"><div class="box">'
            f'<span class="t">{e(title)}</span>'
            f'<span class="u">{e(url)}</span>'
            + (f'<span class="n">{e(note)}</span>' if note else "")
            + '</div></li>')

PRIMARY = [
    ("Process", "/process.html", "Nine-step manufacturing route"),
    ("About", "/about.html", "Factory, capability, process banner"),
    ("Contact", "/contact.html", "Phone, WhatsApp, email, address"),
    ("Request a Quote", "/quote.html", "Specification form: line, sizes, branding"),
]
UTIL = [("Not Found", "/404.html", ""), ("Index", "/sitemap.xml", ""), ("Crawlers", "/robots.txt", "")]

cats = ""
for i, c in enumerate(B.CATEGORIES, 1):
    chips = "".join(
        f'<span class="chip"><b>{e(p["name"])}</b>'
        f'<i>/products/{e(B.slugify(p["name"]))}.html</i></span>'
        for p in c["products"])
    cats += f'''<li class="leaf cat">
  <div class="box">
    <span class="t"><em>{i:02d}</em> {e(c["name"])}</span>
    <span class="u">/collections/{e(c["slug"])}.html</span>
    <span class="n">{e(c["tag"])} &middot; {len(c["products"])} products</span>
    <div class="chips">{chips}</div>
  </div>
</li>'''

nprod = sum(len(c["products"]) for c in B.CATEGORIES)
total = 6 + len(B.CATEGORIES) + nprod

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{e(B.BRAND)} — Site Map (Tree)</title>
<link rel="stylesheet" href="../assets/css/fonts.css">
<style>
  @page {{ size:A3; margin:0; }}
  :root {{ --bg:#000; --fg:#fff; --fg2:rgba(255,255,255,.6); --line:rgba(255,255,255,.22); }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--fg); font-family:"Inter",system-ui,sans-serif;
    font-size:9pt; line-height:1.4; -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  .sheet {{ width:297mm; height:419mm; overflow:hidden; padding:18mm 16mm 14mm; display:flex; flex-direction:column; }}
  h1,h2,.t {{ font-family:"Plus Jakarta Sans",sans-serif; font-weight:800;
    letter-spacing:-.02em; text-transform:uppercase; }}
  h1 {{ font-size:30pt; line-height:.95; }}
  .mono,.u,.n {{ font-family:"JetBrains Mono",monospace; letter-spacing:.1em;
    text-transform:uppercase; color:var(--fg2); font-size:6.8pt; }}
  .mast {{ display:flex; justify-content:space-between; align-items:flex-end;
    gap:12mm; padding-bottom:5mm; border-bottom:1.2px solid var(--fg); }}
  .mast img {{ width:18mm; margin-bottom:4mm; }}
  .mast .r {{ text-align:right; line-height:2; }}

  /* tree */
  .tree {{ flex:1; padding-top:7mm; }}
  .tree ul {{ list-style:none; padding-left:13mm; position:relative; }}
  .tree ul::before {{ content:""; position:absolute; left:4mm; top:0; bottom:0;
    border-left:1px solid var(--line); }}
  .tree ul > li {{ position:relative; padding:0 0 2.2mm 0; }}
  .tree ul.flat {{ display:grid; grid-template-columns:repeat(4,1fr); gap:3mm; }}
  .tree ul.flat > li {{ padding:0; }}
  .tree ul.flat > li::before {{ top:6mm; }}
  .tree ul.flat > li:not(:first-child)::before {{ display:none; }}
  .tree ul.flat > li > .box {{ height:100%; }}
  .tree ul > li::before {{ content:""; position:absolute; left:-9mm; top:7mm;
    width:9mm; border-top:1px solid var(--line); }}
  .tree ul > li:last-child > .stub {{ display:none; }}

  .root > .box {{ border:1.2px solid var(--fg); }}
  .box {{ border:1px solid var(--line); padding:2.6mm 3.5mm; }}
  .t {{ display:block; font-size:11pt; }}
  .t em {{ font-family:"JetBrains Mono",monospace; font-style:normal; font-size:7.5pt;
    color:var(--fg2); margin-right:2mm; }}
  .u {{ display:block; margin-top:1mm; }}
  .n {{ display:block; margin-top:1.5mm; text-transform:none; letter-spacing:.02em;
    font-family:"Inter",sans-serif; font-size:8pt; }}
  .branch > .box {{ border-left:2.5px solid var(--fg); }}
  .branch > .box .t {{ font-size:12.5pt; }}

  .chips {{ display:grid; grid-template-columns:repeat(5,1fr); gap:1.8mm; margin-top:2.4mm;
    padding-top:2.4mm; border-top:1px dotted var(--line); }}
  .chip {{ border:1px solid var(--line); padding:2mm 2.5mm; display:block; }}
  .chip b {{ display:block; font-weight:600; font-size:8.2pt; line-height:1.25; }}
  .chip i {{ display:block; font-family:"JetBrains Mono",monospace; font-style:normal;
    font-size:5.6pt; color:var(--fg2); margin-top:1.2mm; word-break:break-all; }}

  .cols {{ display:grid; grid-template-columns:1fr 1fr; gap:4mm; }}
  footer {{ display:flex; justify-content:space-between; margin-top:8mm;
    padding-top:3mm; border-top:1.2px solid var(--fg); }}
</style></head><body>
<div class="sheet">
  <div class="mast">
    <div><img src="../assets/img/logo-white.svg" alt=""><h1>Site Map</h1></div>
    <div class="r">
      <div class="mono">{e(B.BRAND)}</div>
      <div class="mono">{total} pages &middot; {len(B.CATEGORIES)} lines &middot; {nprod} products</div>
      <div class="mono">{e(B.SITE)}</div>
    </div>
  </div>

  <div class="tree">
    <div class="box root" style="max-width:95mm">
      <span class="t">Home</span><span class="u">/index.html</span>
      <span class="n">Hero, catalogue, departments, process, proof, quote CTA</span>
    </div>
    <ul>
      <li class="branch">
        <div class="box">
          <span class="t">Collections</span><span class="u">/collections.html</span>
          <span class="n">Five product lines, each tile opening its own page</span>
        </div>
        <ul>{cats}</ul>
      </li>
      <li class="branch">
        <div class="box"><span class="t">Company &amp; Enquiry</span>
          <span class="n">The four pages a buyer reaches from the header</span></div>
        <ul class="flat">{"".join(leaf(*t) for t in PRIMARY)}</ul>
      </li>
      <li class="branch">
        <div class="box"><span class="t">Utility &amp; Machine Routes</span>
          <span class="n">Not in navigation</span></div>
        <ul class="flat">{"".join(leaf(*t) for t in UTIL)}</ul>
      </li>
    </ul>
  </div>

  <footer><span class="mono">Tree view &middot; A3</span>
    <span class="mono">{e(B.EMAIL)} &middot; {e(B.PHONE)}</span></footer>
</div></body></html>'''

out = os.path.join(ROOT, "tools", "sitemap-tree-page.html")
open(out, "w").write(page)
print(f"wrote {out} ({total} pages)")
