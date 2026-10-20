#!/usr/bin/env python3
"""Third site-map design: a plain-English multi-page guide.

Several A4 sheets, large type, no product URLs: what each page is for,
what sits in each collection, and the route a buyer takes to a quote.
Writes tools/sitemap-guide-page.html for tools/make-sitemap-guide.mjs.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def e(s): return html.escape(str(s))

MENU = [
    ("Home", "/index.html", "The front page. Shows who we are, the five product lines, the departments inside the factory and the nine-step process, then sends the visitor to a quote."),
    ("Collections", "/collections.html", "The catalogue. One tile per product line; clicking a tile opens that line's own page."),
    ("Process", "/process.html", "How an order is made, step by step, from your sketch to the packed carton."),
    ("About", "/about.html", "Who NTF INTERNATIONAL is, what the factory can do and the full manufacturing banner."),
    ("Contact", "/contact.html", "Phone, WhatsApp, email, address and working hours."),
    ("Request a Quote", "/quote.html", "The enquiry form: product line, sizes, quantity and how you want it branded."),
]

JOURNEY = [
    ("Arrives", "A buyer lands on the home page, from search or a link you sent."),
    ("Browses", "They open Collections and pick the line they need — say MMA Wear."),
    ("Compares", "Inside the line they see its five products, each with fabric, sizes and build detail."),
    ("Reads the detail", "A product page gives the full specification and the minimum order."),
    ("Checks you out", "Process and About answer the question every buyer asks: can this factory actually make it."),
    ("Asks for a price", "Request a Quote collects the line, sizes, quantity and branding, and emails it to you."),
]

SHEETS = []

nprod = sum(len(c["products"]) for c in B.CATEGORIES)
total = 6 + len(B.CATEGORIES) + nprod

def sheet(body, label, n=None):
    SHEETS.append((body, label))

# ---- sheet 1: cover -------------------------------------------------------
cover = f'''
<div class="cover">
  <img class="logo" src="../assets/img/logo-white.svg" alt="">
  <h1>Site<br>Map</h1>
  <p class="lede">A plain guide to every page on the {e(B.BRAND)} website &mdash;
  what each one is for, and the order a buyer meets them in.</p>
  <div class="stats">
    <div><b>{total}</b><span class="mono">Pages in total</span></div>
    <div><b>6</b><span class="mono">Menu pages</span></div>
    <div><b>{len(B.CATEGORIES)}</b><span class="mono">Product lines</span></div>
    <div><b>{nprod}</b><span class="mono">Products</span></div>
  </div>
  <div class="contents">
    <h2>What&rsquo;s inside</h2>
    <ol>{{contents}}</ol>
  </div>
  <div class="cfoot">
    <span class="mono">{e(B.SITE)}</span>
    <span class="mono">{e(B.EMAIL)} &middot; {e(B.PHONE)}</span>
  </div>
</div>'''
COVER = cover

# ---- sheet 2: the main menu ----------------------------------------------
menu_items = "".join(f'''<li>
  <div class="num">{i:02d}</div>
  <div>
    <h3>{e(name)}</h3>
    <div class="path">{e(path)}</div>
    <p>{e(desc)}</p>
  </div></li>''' for i, (name, path, desc) in enumerate(MENU, 1))
sheet(f'''<h2 class="sh">The main menu</h2>
<p class="intro">These six pages sit in the header on every screen. Everything else
on the site is reached from one of them.</p>
<ul class="menu">{menu_items}</ul>
<div class="aside"><b>Also on the site, but not in the menu:</b> a Not Found page that
catches a mistyped address and offers the catalogue, plus two files search engines
read &mdash; an index of all pages and a crawler instruction file.</div>''', "The main menu")

# ---- sheets 3+: the collections ------------------------------------------
PER = 2
chunks = [B.CATEGORIES[i:i + PER] for i in range(0, len(B.CATEGORIES), PER)]
n = 0
for k, chunk in enumerate(chunks):
    blocks = ""
    for c in chunk:
        n += 1
        items = "".join(f"<li>{e(p['name'])}</li>" for p in c["products"])
        blocks += f'''<section class="line">
  <header><span class="num">{n:02d}</span>
    <div><h3>{e(c["name"])}</h3><div class="tag">{e(c["tag"])}</div></div>
    <div class="count mono">{len(c["products"])} products</div>
  </header>
  <p>{e(c["blurb"])}</p>
  <ol class="prods">{items}</ol>
</section>'''
    title = "The five product lines" if k == 0 else "Product lines, continued"
    label = " & ".join(c["name"] for c in chunk)
    intro = ('<p class="intro">Each line has its own page, and every product on it has a '
             'page of its own with fabric, sizes, build detail and the minimum order.</p>'
             if k == 0 else "")
    sheet(f'<h2 class="sh">{title}</h2>{intro}{blocks}', label)

# ---- last sheet: the journey ---------------------------------------------
steps = "".join(f'''<li><div class="num">{i:02d}</div>
  <div><h3>{e(t)}</h3><p>{e(d)}</p></div></li>'''
  for i, (t, d) in enumerate(JOURNEY, 1))
sheet(f'''<h2 class="sh">How a buyer gets to a quote</h2>
<p class="intro">The whole site is built to carry someone from the front page to a
filled-in enquiry in six moves.</p>
<ul class="journey">{steps}</ul>
<div class="aside"><b>Every product page and every collection page</b> carries a
&ldquo;request a quote&rdquo; button, so a buyer never has to go looking for it.</div>''',
"How a buyer gets to a quote")

contents = "".join(
    f'<li><span>{i:02d}</span> {e(label)}</li>'
    for i, (_, label) in enumerate(SHEETS, 2))
SHEETS.insert(0, (COVER.replace("{contents}", contents), ""))

NS = len(SHEETS)
body = ""
for i, (content, label) in enumerate(SHEETS, 1):
    if i == 1:
        body += f'<div class="sheet first">{content}</div>'
    else:
        body += f'''<div class="sheet">
  <div class="mast"><span class="mono">{e(B.BRAND)} &middot; Site Map</span>
    <span class="mono">{i} / {NS}</span></div>
  {content}
  <footer><span class="mono">{e(label)}</span><span class="mono">{e(B.EMAIL)}</span></footer>
</div>'''

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{e(B.BRAND)} — Site Map</title>
<link rel="stylesheet" href="../assets/css/fonts.css">
<style>
  @page {{ size:A4; margin:0; }}
  :root {{ --bg:#000; --fg:#fff; --fg2:rgba(255,255,255,.64); --line:rgba(255,255,255,.2); }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ background:var(--bg); color:var(--fg); font-family:"Inter",system-ui,sans-serif;
    font-size:10.5pt; line-height:1.55; -webkit-print-color-adjust:exact;
    print-color-adjust:exact; }}
  .sheet {{ width:210mm; height:296mm; padding:18mm 18mm 14mm; overflow:hidden;
    display:flex; flex-direction:column; }}
  .sheet + .sheet {{ page-break-before:always; }}
  h1,h2,h3 {{ font-family:"Plus Jakarta Sans",sans-serif; font-weight:800;
    letter-spacing:-.025em; text-transform:uppercase; }}
  .mono {{ font-family:"JetBrains Mono",monospace; font-size:7pt; letter-spacing:.14em;
    text-transform:uppercase; color:var(--fg2); }}
  .num {{ font-family:"JetBrains Mono",monospace; font-size:9pt; color:var(--fg2);
    padding-top:1mm; }}

  /* cover */
  .first {{ padding:22mm 18mm 14mm; }}
  .cover {{ display:flex; flex-direction:column; height:100%; }}
  .logo {{ width:26mm; }}
  h1 {{ font-size:46pt; line-height:.92; margin:12mm 0 0; }}
  .lede {{ margin-top:7mm; max-width:120mm; font-size:12pt; color:var(--fg2); }}
  .stats {{ display:flex; border:1px solid var(--line); margin-top:12mm; }}
  .stats div {{ flex:1; padding:5mm 4mm; border-right:1px solid var(--line); }}
  .stats div:last-child {{ border-right:0; }}
  .stats b {{ display:block; font-family:"Plus Jakarta Sans",sans-serif; font-weight:800;
    font-size:22pt; letter-spacing:-.03em; line-height:1.1; }}
  .contents {{ margin-top:14mm; }}
  .contents h2 {{ font-size:11pt; padding-bottom:3mm; border-bottom:1px solid var(--line); }}
  .contents ol {{ list-style:none; margin-top:4mm; }}
  .contents li {{ padding:2.5mm 0; border-bottom:1px dotted var(--line); font-size:11pt; }}
  .contents span {{ font-family:"JetBrains Mono",monospace; font-size:8pt;
    color:var(--fg2); margin-right:4mm; }}
  .cfoot {{ margin-top:auto; display:flex; justify-content:space-between;
    padding-top:4mm; border-top:1.2px solid var(--fg); }}

  /* inner sheets */
  .mast {{ display:flex; justify-content:space-between; padding-bottom:3mm;
    border-bottom:1px solid var(--line); margin-bottom:9mm; }}
  .sh {{ font-size:21pt; line-height:1.05; }}
  .intro {{ margin:5mm 0 8mm; color:var(--fg2); max-width:150mm; }}

  .menu {{ list-style:none; }}
  .menu li {{ display:grid; grid-template-columns:11mm 1fr; gap:3mm;
    padding:4.5mm 0; border-top:1px solid var(--line); }}
  .menu h3 {{ font-size:14pt; }}
  .menu .path {{ font-family:"JetBrains Mono",monospace; font-size:7pt; color:var(--fg2);
    letter-spacing:.1em; margin:.8mm 0 2mm; }}
  .menu p {{ color:var(--fg2); font-size:10pt; }}

  .line {{ border:1px solid var(--line); padding:5mm 5.5mm; margin-bottom:5mm; }}
  .line header {{ display:flex; gap:4mm; align-items:baseline;
    padding-bottom:3mm; border-bottom:1px solid var(--line); }}
  .line header > div:first-of-type {{ flex:1; }}
  .line h3 {{ font-size:15pt; }}
  .tag {{ font-family:"JetBrains Mono",monospace; font-size:7pt; letter-spacing:.12em;
    text-transform:uppercase; color:var(--fg2); margin-top:1mm; }}
  .line p {{ margin:3.5mm 0 4mm; color:var(--fg2); font-size:9.6pt; }}
  .prods {{ list-style:none; display:grid; grid-template-columns:repeat(2,1fr);
    gap:1mm 7mm; counter-reset:p; }}
  .prods li {{ counter-increment:p; padding:1.6mm 0; border-bottom:1px dotted var(--line);
    font-weight:500; }}
  .prods li::before {{ content:counter(p,decimal-leading-zero);
    font-family:"JetBrains Mono",monospace; font-size:7.5pt; color:var(--fg2);
    margin-right:3.5mm; }}

  .journey {{ list-style:none; }}
  .journey li {{ display:grid; grid-template-columns:11mm 1fr; gap:3mm;
    padding:5mm 0; border-top:1px solid var(--line); }}
  .journey h3 {{ font-size:14pt; }}
  .journey p {{ color:var(--fg2); margin-top:1mm; }}

  .aside {{ margin-top:auto; border-left:2.5px solid var(--fg); padding:3.5mm 5mm;
    font-size:9.6pt; color:var(--fg2); }}
  .aside b {{ color:var(--fg); font-weight:600; }}
  footer {{ display:flex; justify-content:space-between; margin-top:7mm;
    padding-top:3mm; border-top:1.2px solid var(--fg); }}
</style></head><body>{body}</body></html>'''

out = os.path.join(ROOT, "tools", "sitemap-guide-page.html")
open(out, "w").write(page)
print(f"wrote {out} ({NS} sheets, {total} pages indexed)")
