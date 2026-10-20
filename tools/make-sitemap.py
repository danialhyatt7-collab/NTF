#!/usr/bin/env python3
"""Render the branded site-map PDF from the same page data the site is built from.

Writes tools/sitemap-page.html, then tools/make-sitemap.mjs prints it to PDF.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def e(s): return html.escape(str(s))

TOP = [
    ("index.html", "Home", "Hero, catalogue, departments, process, proof, CTA"),
    ("collections.html", "Collections", "All five product lines, tiles into each category"),
    ("process.html", "Process", "The nine-step custom manufacturing route"),
    ("about.html", "About", "Who we are, the factory, the process banner"),
    ("contact.html", "Contact", "Phone, WhatsApp, email, address, hours"),
    ("quote.html", "Request a Quote", "Specification form: line, sizes, quantity, branding"),
]
UTIL = [
    ("404.html", "Not Found", "Fallback page with routes back into the catalogue"),
    ("sitemap.xml", "sitemap.xml", "Machine-readable index of all 36 pages"),
    ("robots.txt", "robots.txt", "Crawler directives, points at sitemap.xml"),
]

def node(url, title, note=""):
    return (f'<div class="node"><div class="nt">{e(title)}</div>'
            f'<div class="nu">/{e(url)}</div>'
            + (f'<div class="nn">{e(note)}</div>' if note else "") + '</div>')

def cat_block(i, c):
    prods = "".join(
        f'<li><span class="pn">{e(p["name"])}</span>'
        f'<span class="pu">/products/{e(B.slugify(p["name"]))}.html</span></li>'
        for p in c["products"])
    return f"""<section class="cat">
  <header>
    <span class="cn">{i:02d}</span>
    <div>
      <h3>{e(c["name"])}</h3>
      <div class="ct">{e(c["tag"])} &middot; /collections/{e(c["slug"])}.html</div>
    </div>
  </header>
  <ol class="prods">{prods}</ol>
</section>"""

# three category blocks fill an A4 sheet; chunk so nothing is cut mid-table
PER_SHEET = 3
chunks = [B.CATEGORIES[i:i + PER_SHEET] for i in range(0, len(B.CATEGORIES), PER_SHEET)]
SHEETS = 1 + len(chunks)

total = 6 + len(B.CATEGORIES) + sum(len(c["products"]) for c in B.CATEGORIES)

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{e(B.BRAND)} — Site Map</title>
<link rel="stylesheet" href="../assets/css/fonts.css">
<style>
  @page {{ size: A4; margin: 0; }}
  :root {{ --bg:#000; --fg:#fff; --fg2:rgba(255,255,255,.62); --line:rgba(255,255,255,.16); }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--fg);
    font-family:"Inter",system-ui,sans-serif; font-size:9.2pt; line-height:1.45;
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
  .sheet {{ width:210mm; min-height:297mm; padding:16mm 15mm 14mm; }}
  .sheet + .sheet {{ page-break-before:always; }}
  h1,h2,h3 {{ font-family:"Plus Jakarta Sans",sans-serif; font-weight:800;
    letter-spacing:-.02em; text-transform:uppercase; }}
  h1 {{ font-size:25pt; line-height:1.02; }}
  .mono {{ font-family:"JetBrains Mono",monospace; font-size:7pt;
    letter-spacing:.14em; text-transform:uppercase; color:var(--fg2); }}
  .mast {{ display:flex; justify-content:space-between; align-items:flex-start;
    gap:10mm; padding-bottom:5mm; border-bottom:1px solid var(--fg); }}
  .mast img {{ width:17mm; display:block; }}
  .mast .r {{ text-align:right; }}
  .lede {{ margin:6mm 0 8mm; max-width:120mm; color:var(--fg2); font-size:9.6pt; }}
  .stats {{ display:flex; gap:0; border:1px solid var(--line); margin-bottom:9mm; }}
  .stats div {{ flex:1; padding:4mm; border-right:1px solid var(--line); }}
  .stats div:last-child {{ border-right:0; }}
  .stats b {{ display:block; font-family:"Plus Jakarta Sans",sans-serif;
    font-weight:800; font-size:17pt; letter-spacing:-.03em; }}
  h2 {{ font-size:11pt; padding-bottom:2.5mm; margin-bottom:4mm;
    border-bottom:1px solid var(--line); }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:3mm; margin-bottom:9mm; }}
  .node {{ border:1px solid var(--line); padding:3.5mm; }}
  .node .nt {{ font-family:"Plus Jakarta Sans",sans-serif; font-weight:700;
    font-size:10pt; letter-spacing:-.01em; }}
  .node .nu {{ font-family:"JetBrains Mono",monospace; font-size:6.6pt;
    color:var(--fg2); margin:1.2mm 0 1.8mm; word-break:break-all; }}
  .node .nn {{ font-size:7.6pt; color:var(--fg2); line-height:1.4; }}
  .cat {{ border:1px solid var(--line); padding:4mm 4.5mm 3mm; margin-bottom:4mm;
    page-break-inside:avoid; }}
  .cat header {{ display:flex; gap:4mm; align-items:baseline;
    padding-bottom:2.5mm; border-bottom:1px solid var(--line); margin-bottom:3mm; }}
  .cn {{ font-family:"JetBrains Mono",monospace; font-size:8pt; color:var(--fg2); }}
  .cat h3 {{ font-size:11.5pt; }}
  .ct {{ font-family:"JetBrains Mono",monospace; font-size:6.8pt;
    letter-spacing:.1em; text-transform:uppercase; color:var(--fg2); margin-top:1mm; }}
  .prods {{ list-style:none; display:grid; grid-template-columns:repeat(2,1fr);
    gap:1.5mm 5mm; }}
  .prods li {{ display:flex; justify-content:space-between; gap:3mm;
    padding:1.2mm 0; border-bottom:1px dotted var(--line); }}
  .pn {{ font-weight:500; }}
  .pu {{ font-family:"JetBrains Mono",monospace; font-size:6.4pt;
    color:var(--fg2); text-align:right; }}
  footer {{ display:flex; justify-content:space-between; margin-top:7mm;
    padding-top:3mm; border-top:1px solid var(--fg); }}
</style></head><body>

<div class="sheet">
  <div class="mast">
    <div>
      <img src="../assets/img/logo-white.svg" alt="">
      <h1 style="margin-top:5mm">Site<br>Map</h1>
    </div>
    <div class="r">
      <div class="mono">{e(B.BRAND)}</div>
      <div class="mono" style="margin-top:1.5mm">{e(B.SITE)}</div>
      <div class="mono" style="margin-top:1.5mm">{e(B.EMAIL)} &middot; {e(B.PHONE)}</div>
    </div>
  </div>

  <p class="lede">Every page of the {e(B.BRAND)} site, in the order a buyer meets it:
  six primary pages, five collection pages and one page per product, each with its
  own specification, size range and quote hand-off.</p>

  <div class="stats">
    <div><b>{total}</b><span class="mono">Pages indexed</span></div>
    <div><b>6</b><span class="mono">Primary pages</span></div>
    <div><b>{len(B.CATEGORIES)}</b><span class="mono">Collections</span></div>
    <div><b>{sum(len(c["products"]) for c in B.CATEGORIES)}</b><span class="mono">Product pages</span></div>
  </div>

  <h2>Primary navigation</h2>
  <div class="grid">{"".join(node(*t) for t in TOP)}</div>

  <h2>Utility &amp; machine routes</h2>
  <div class="grid">{"".join(node(*t) for t in UTIL)}</div>

  <footer><span class="mono">Sheet 1 / {SHEETS} &mdash; Structure</span>
    <span class="mono">{e(B.BRAND)}</span></footer>
</div>

{{cat_sheets}}
</body></html>'''

cat_sheets = ""
n = 0
for k, chunk in enumerate(chunks):
    blocks = ""
    for c in chunk:
        n += 1
        blocks += cat_block(n, c)
    head = ("Collections<br>&amp; Products" if k == 0 else "Collections<br>&amp; Products<br>cont.")
    cat_sheets += f'''<div class="sheet">
  <div class="mast">
    <div><h1>{head}</h1></div>
    <div class="r"><div class="mono">/collections.html</div>
      <div class="mono" style="margin-top:1.5mm">Lines {n - len(chunk) + 1}&ndash;{n} of {len(B.CATEGORIES)}</div></div>
  </div>
  <div style="height:7mm"></div>
  {blocks}
  <footer><span class="mono">Sheet {k + 2} / {SHEETS} &mdash; Catalogue</span>
    <span class="mono">{e(B.EMAIL)}</span></footer>
</div>'''

page = page.replace("{cat_sheets}", cat_sheets)

out = os.path.join(ROOT, "tools", "sitemap-page.html")
with open(out, "w") as f:
    f.write(page)
print(f"wrote {out} ({total} pages indexed)")
