#!/usr/bin/env python3
"""Owner guide PDF: adding products, and making the quote form send real email.

Writes tools/howto-page.html for tools/make-howto.mjs to print.
"""
import os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build as B

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def e(s): return html.escape(str(s))
def code(s): return '<pre>' + html.escape(s.strip('\n')) + '</pre>'

SHEETS = []
def sheet(body, label): SHEETS.append((body, label))

# ---------------------------------------------------------------- sheet 2
sheet('''
<h2 class="sh">Why no email reaches you</h2>
<p class="intro">Nothing is broken in the form itself. The site is a static site on
GitHub Pages, and right now the Request a Quote button hands the enquiry to the
<i>visitor&rsquo;s own</i> mail app instead of sending it.</p>

<div class="what"><b>What happens today</b>
<ol class="flow">
  <li>A buyer fills in the form and presses send.</li>
  <li>The browser opens a pre-filled draft in <b>their</b> email program, addressed to
      info@ntfint.com.</li>
  <li>If they have no mail program set up, or they close that draft, or they simply
      never press send in it, <b>you get nothing</b> &mdash; and the site cannot tell you
      that it happened.</li>
</ol></div>

<p>This is why your own test never arrived: the draft was created, but no message was
ever actually sent. A static site has no server of its own, so it cannot send mail by
itself. It needs a small form service in between &mdash; that service receives the
submission and emails it straight to your inbox.</p>

<h3 class="sub">The three ways to fix it</h3>
<table class="opt">
  <tr><th>Option</th><th>Cost</th><th>What you get</th></tr>
  <tr><td><b>Form service</b><br><span class="mono">Recommended</span></td>
      <td>Free tier<br>(about 50 enquiries a month)</td>
      <td>The enquiry lands in your inbox within seconds, with a copy stored in the
          service dashboard. No server to run. One line of code to change.</td></tr>
  <tr><td><b>Your own backend</b></td><td>Hosting fees</td>
      <td>Full control, but something to host, maintain and secure for one form.</td></tr>
  <tr><td><b>Leave it as a mail draft</b></td><td>Free</td>
      <td>What happens now. Loses most enquiries. Not recommended.</td></tr>
</table>

<div class="aside"><b>Whichever route you take, add WhatsApp as the backup.</b> Your
buyers in this trade reply faster there than by email, and the number is already on
every page.</div>''', "Why no email reaches you")

# ---------------------------------------------------------------- sheet 3
sheet('''
<h2 class="sh">Turning the form into real email</h2>
<p class="intro">About ten minutes, once. These steps use Formspree; Web3Forms and
FormSubmit work the same way if you prefer one of those.</p>

<ol class="steps">
  <li><div class="num">01</div><div>
    <h3>Create the form endpoint</h3>
    <p>Go to formspree.io, sign up with <b>''' + e(B.EMAIL) + '''</b> &mdash; the inbox
    you want the enquiries in &mdash; and create a new form. You are given an address
    that looks like this:</p>
    ''' + code("https://formspree.io/f/xxxxxxxx") + '''
  </div></li>
  <li><div class="num">02</div><div>
    <h3>Confirm the inbox</h3>
    <p>Formspree sends one confirmation email. Click the link in it. Until you do, it
    will not deliver anything &mdash; this is the step people usually miss.</p>
  </div></li>
  <li><div class="num">03</div><div>
    <h3>Point the form at it</h3>
    <p>In <span class="mono">assets/js/main.js</span>, the submit handler currently ends
    with a line that opens a mail draft. It is replaced with a real send:</p>
    ''' + code('''fetch('https://formspree.io/f/xxxxxxxx', {
  method: 'POST',
  headers: { 'Accept': 'application/json' },
  body: new FormData(form)
});''') + '''
    <p>Send me the endpoint and I will make this change, test it and push it.</p>
  </div></li>
  <li><div class="num">04</div><div>
    <h3>Test it properly</h3>
    <p>Open the live site, send one enquiry, and check the inbox <b>and</b> the spam
    folder. Mark the first message as &ldquo;not spam&rdquo; so the rest land normally.</p>
  </div></li>
</ol>

<div class="aside"><b>After this is live</b> the visitor sees a confirmation on the page,
you get the email, and every enquiry is also kept in the Formspree dashboard &mdash; so
nothing is lost even if an email goes astray.</div>''', "Turning the form into real email")

# ---------------------------------------------------------------- sheet 4
sheet('''
<h2 class="sh">Adding a product</h2>
<p class="intro">Every page on the site is generated from one file,
<span class="mono">tools/build.py</span>. You add the product once there and the site
builds its collection tile, its own product page, the search index and the sitemap
for you.</p>

<ol class="steps tight">
  <li><div class="num">01</div><div>
    <h3>Add the photo</h3>
    <p>Put a JPEG in <span class="mono">assets/img/photos/</span>. Name it in lower case
    with dashes, for example <span class="mono">mma-ankle-guards.jpg</span>. Roughly
    1600&nbsp;px wide, under 300&nbsp;KB.</p>
  </div></li>
  <li><div class="num">02</div><div>
    <h3>Add the entry</h3>
    <p>In <span class="mono">tools/build.py</span>, find the collection inside
    <span class="mono">CATEGORIES</span> and add one block to its
    <span class="mono">products</span> list:</p>
    ''' + code('''P("Ankle Guards", ["Neoprene", "Pair"], "Cage-legal // Slip-on",
  ["S","M","L","XL"], 25,
  "Slip-on neoprene ankle support with a stitched arch strap.",
  [("Fabric","4 mm neoprene"),
   ("Build","Flatlock seams"),
   ("Decoration","Heat transfer or embroidery")],
  "mma-ankle-guards"),''') + '''
    <p class="hint">The values in order: name, the two badges, the small line under the
    name, sizes, minimum order quantity, the description, the specification rows, and
    the photo file name without <span class="mono">.jpg</span>.</p>
  </div></li>
  <li><div class="num">03</div><div>
    <h3>Build and publish</h3>
    ''' + code("python3 tools/build.py\ngit add -A\ngit commit -m \"Add Ankle Guards to MMA Wear\"\ngit push") + '''
    <p>The live site updates about a minute later.</p>
  </div></li>
</ol>

<div class="aside"><b>A whole new collection</b> is the same job one level up: add a new
block to <span class="mono">CATEGORIES</span> with its slug, name, tag, hero photo and
description, then its products. The menu, the collections page and the site map all pick
it up automatically.</div>''', "Adding a product")

# ---------------------------------------------------------------- sheet 5
sheet('''
<h2 class="sh">Checklist</h2>
<p class="intro">Two lists worth keeping beside you.</p>

<div class="cols2">
  <div class="panel">
    <h3>To start receiving enquiries</h3>
    <ol class="check">
      <li>Create the form endpoint with your real inbox</li>
      <li>Click the confirmation email</li>
      <li>Send me the endpoint so the form can be wired to it</li>
      <li>Send one test enquiry from the live site</li>
      <li>Check inbox and spam; mark as not spam</li>
      <li>Add the inbox to your phone so nothing waits a day</li>
    </ol>
  </div>
  <div class="panel">
    <h3>Every time you add a product</h3>
    <ol class="check">
      <li>Photo into <span class="mono">assets/img/photos/</span></li>
      <li>One <span class="mono">P(...)</span> block in the right collection</li>
      <li>Minimum order quantity set honestly</li>
      <li>Three or four specification rows</li>
      <li>Run <span class="mono">python3 tools/build.py</span></li>
      <li>Commit and push</li>
      <li>Open the live product page and read it once</li>
    </ol>
  </div>
</div>

<div class="panel wide">
  <h3>Where things live</h3>
  <table class="where">
    <tr><td class="mono">tools/build.py</td><td>All text, products, collections, prices and contact details</td></tr>
    <tr><td class="mono">assets/img/photos/</td><td>Every photograph on the site</td></tr>
    <tr><td class="mono">assets/js/main.js</td><td>Form behaviour, theme switch, animations</td></tr>
    <tr><td class="mono">assets/css/style.css</td><td>The whole look of the site</td></tr>
    <tr><td class="mono">docs/</td><td>The site map PDFs and this guide</td></tr>
  </table>
</div>

<div class="aside"><b>One rule:</b> never edit the built <span class="mono">.html</span>
files by hand. The next build overwrites them. Change
<span class="mono">tools/build.py</span> and rebuild.</div>''', "Checklist")

NS = len(SHEETS) + 1
contents = "".join(f'<li><span>{i:02d}</span> {e(l)}</li>'
                   for i, (_, l) in enumerate(SHEETS, 2))

cover = f'''
<div class="cover">
  <img class="logo" src="../assets/img/logo-white.svg" alt="">
  <h1>Running<br>the Site</h1>
  <p class="lede">How to add products, and how to start receiving the enquiries people
  send from the Request a Quote page.</p>
  <div class="answer">
    <span class="mono">The short answer</span>
    <p>Enquiries are not reaching you because the form currently opens a draft in the
    visitor&rsquo;s own email program instead of sending anything. Nothing arrives unless
    they press send there. Connecting a small form service fixes it in about ten minutes
    &mdash; page 2 explains it, page 3 is the steps.</p>
  </div>
  <div class="contents"><h2>Inside</h2><ol>{contents}</ol></div>
  <div class="cfoot"><span class="mono">{e(B.BRAND)}</span>
    <span class="mono">{e(B.EMAIL)} &middot; {e(B.PHONE)}</span></div>
</div>'''

body = f'<div class="sheet first">{cover}</div>'
for i, (content, label) in enumerate(SHEETS, 2):
    body += f'''<div class="sheet">
  <div class="mast"><span class="mono">{e(B.BRAND)} &middot; Running the Site</span>
    <span class="mono">{i} / {NS}</span></div>
  {content}
  <footer><span class="mono">{e(label)}</span><span class="mono">{e(B.EMAIL)}</span></footer>
</div>'''

page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>''' + e(B.BRAND) + ''' — Running the Site</title>
<link rel="stylesheet" href="../assets/css/fonts.css">
<style>
  @page { size:A4; margin:0; }
  :root { --bg:#000; --fg:#fff; --fg2:rgba(255,255,255,.64); --line:rgba(255,255,255,.2); }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:var(--bg); color:var(--fg); font-family:"Inter",system-ui,sans-serif;
    font-size:10pt; line-height:1.55; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .sheet { width:210mm; height:296mm; padding:17mm 18mm 13mm; overflow:hidden;
    display:flex; flex-direction:column; }
  .sheet + .sheet { page-break-before:always; }
  h1,h2,h3 { font-family:"Plus Jakarta Sans",sans-serif; font-weight:800;
    letter-spacing:-.025em; text-transform:uppercase; }
  .mono,.mono * { font-family:"JetBrains Mono",monospace; font-size:7pt;
    letter-spacing:.12em; text-transform:uppercase; color:var(--fg2); }
  p .mono, td.mono, span.mono { text-transform:none; letter-spacing:.02em; font-size:8.4pt;
    color:var(--fg); }
  pre { font-family:"JetBrains Mono",monospace; font-size:7.6pt; line-height:1.6;
    border:1px solid var(--line); border-left:2.5px solid var(--fg);
    padding:3mm 4mm; margin:3mm 0; white-space:pre-wrap; color:var(--fg); }
  .num { font-family:"JetBrains Mono",monospace; font-size:9pt; color:var(--fg2); padding-top:.6mm; }

  .first { padding:22mm 18mm 13mm; }
  .cover { display:flex; flex-direction:column; height:100%; }
  .logo { width:24mm; }
  h1 { font-size:40pt; line-height:.95; margin:11mm 0 0; }
  .lede { margin-top:6mm; max-width:122mm; font-size:11.5pt; color:var(--fg2); }
  .answer { margin-top:10mm; border:1px solid var(--line); border-left:2.5px solid var(--fg);
    padding:5mm 6mm; }
  .answer p { margin-top:2.5mm; font-size:10.5pt; }
  .contents { margin-top:10mm; }
  .contents h2 { font-size:11pt; padding-bottom:3mm; border-bottom:1px solid var(--line); }
  .contents ol { list-style:none; margin-top:3mm; }
  .contents li { padding:2.2mm 0; border-bottom:1px dotted var(--line); font-size:10.5pt; }
  .contents span { font-family:"JetBrains Mono",monospace; font-size:8pt; color:var(--fg2);
    margin-right:4mm; }
  .cfoot { margin-top:auto; display:flex; justify-content:space-between;
    padding-top:4mm; border-top:1.2px solid var(--fg); }

  .mast { display:flex; justify-content:space-between; padding-bottom:3mm;
    border-bottom:1px solid var(--line); margin-bottom:8mm; }
  .sh { font-size:20pt; line-height:1.05; }
  .sub { font-size:11.5pt; margin:7mm 0 3mm; }
  .intro { margin:4mm 0 6mm; color:var(--fg2); max-width:152mm; }
  i { color:var(--fg); font-style:italic; }

  .what { border:1px solid var(--line); padding:4mm 5mm; margin-bottom:5mm; }
  .flow { margin:2.5mm 0 0 5mm; color:var(--fg2); }
  .flow li { padding:.8mm 0; }
  b { font-weight:600; color:var(--fg); }

  table { width:100%; border-collapse:collapse; margin-top:2mm; }
  .opt th { text-align:left; font-family:"JetBrains Mono",monospace; font-size:6.8pt;
    letter-spacing:.12em; text-transform:uppercase; color:var(--fg2);
    padding:0 4mm 2mm 0; border-bottom:1px solid var(--line); }
  .opt td { vertical-align:top; padding:3.5mm 4mm 3.5mm 0; font-size:9.2pt;
    color:var(--fg2); border-bottom:1px dotted var(--line); }
  .opt td:first-child { width:34mm; color:var(--fg); }
  .opt td:nth-child(2) { width:34mm; }
  .where td { padding:2.2mm 4mm 2.2mm 0; font-size:9.2pt; color:var(--fg2);
    border-bottom:1px dotted var(--line); vertical-align:top; }
  .where td:first-child { width:52mm; }

  .steps { list-style:none; }
  .steps > li { display:grid; grid-template-columns:11mm 1fr; gap:3mm;
    padding:4.5mm 0; border-top:1px solid var(--line); }
  .steps.tight > li { padding:3.5mm 0; }
  .steps h3 { font-size:12.5pt; }
  .steps p { color:var(--fg2); margin-top:1.5mm; font-size:9.6pt; }
  .hint { font-size:9pt; }

  .cols2 { display:grid; grid-template-columns:1fr 1fr; gap:4mm; }
  .panel { border:1px solid var(--line); padding:4.5mm 5mm; }
  .panel.wide { margin-top:4mm; }
  .panel h3 { font-size:11.5pt; padding-bottom:2.5mm; border-bottom:1px solid var(--line);
    margin-bottom:3mm; }
  .check { list-style:none; counter-reset:c; }
  .check li { counter-increment:c; padding:1.8mm 0; border-bottom:1px dotted var(--line);
    font-size:9.4pt; color:var(--fg2); }
  .check li::before { content:counter(c,decimal-leading-zero);
    font-family:"JetBrains Mono",monospace; font-size:7.2pt; color:var(--fg2); margin-right:3.5mm; }

  .aside { margin-top:auto; border-left:2.5px solid var(--fg); padding:3.5mm 5mm;
    font-size:9.6pt; color:var(--fg2); }
  footer { display:flex; justify-content:space-between; margin-top:7mm;
    padding-top:3mm; border-top:1.2px solid var(--fg); }
</style></head><body>''' + body + '</body></html>'

out = os.path.join(ROOT, "tools", "howto-page.html")
open(out, "w").write(page)
print(f"wrote {out} ({NS} sheets)")
