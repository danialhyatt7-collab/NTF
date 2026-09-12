#!/usr/bin/env python3
"""Static site generator for the NTF custom sportswear website.

Run:  python3 tools/build.py
Writes HTML pages into the repository root (and /products, /collections).
"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHONE = "+92 333 8686122"
PHONE_TEL = "+923338686122"
PHONE_WA = "923338686122"
EMAIL = "support@ntf.com.pk"

# --------------------------------------------------------------------------
# artwork: one line-art SVG per category, used as product/category imagery
# --------------------------------------------------------------------------
ART = {
"martial-arts": """<svg viewBox="0 0 200 160" fill="none" stroke="#00a650" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M40 44h120l-22 26 22 26H40l22-26z" stroke-width="5"/><path d="M62 70h76" stroke="#eaf3ed" stroke-opacity=".55"/><path d="M30 126h140" stroke="#eaf3ed" stroke-opacity=".25"/><circle cx="100" cy="24" r="10"/></svg>""",
"mma-wear": """<svg viewBox="0 0 200 160" fill="none" stroke="#00a650" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M64 34l36 16 36-16 30 20-16 30-14-6v56H64V78l-14 6-16-30z" stroke-width="5"/><path d="M86 40c4 10 24 10 28 0" stroke="#eaf3ed" stroke-opacity=".55"/><path d="M78 96h44" stroke="#eaf3ed" stroke-opacity=".3"/></svg>""",
"grappling-dummy": """<svg viewBox="0 0 200 160" fill="none" stroke="#00a650" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><circle cx="100" cy="34" r="18" stroke-width="5"/><path d="M100 52v54M100 70L58 92M100 70l42 22M100 106l-26 40M100 106l26 40"/><path d="M74 78h52" stroke="#eaf3ed" stroke-opacity=".35"/></svg>""",
"fitness-wear": """<svg viewBox="0 0 200 160" fill="none" stroke="#00a650" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><path d="M70 30h60l34 22-18 26-16-9v62H70V69l-16 9-18-26z" stroke-width="5"/><path d="M88 32c2 12 22 12 24 0" stroke="#eaf3ed" stroke-opacity=".55"/><path d="M84 104h32M84 118h32" stroke="#eaf3ed" stroke-opacity=".28"/></svg>""",
"wrist-straps": """<svg viewBox="0 0 200 160" fill="none" stroke="#00a650" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"><rect x="36" y="52" width="78" height="46" rx="14" stroke-width="5"/><path d="M114 62c28 0 44 10 50 18-8 10-22 18-50 18"/><path d="M52 66v18M68 66v18" stroke="#eaf3ed" stroke-opacity=".4"/></svg>""",
}

ICON = {
"factory": """<svg viewBox="0 0 24 24" width="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18V9l-6 4V9l-6 4V4H3z"/></svg>""",
"phone": """<svg viewBox="0 0 24 24" width="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>""",
"mail": """<svg viewBox="0 0 24 24" width="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7 10-7"/></svg>""",
"clock": """<svg viewBox="0 0 24 24" width="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>""",
"pin": """<svg viewBox="0 0 24 24" width="20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>""",
"wa": """<svg viewBox="0 0 24 24" width="26" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.2 14.1c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.7-.1a13 13 0 0 1-5.6-4.4c-.6-.9-1-1.9-1-2.8 0-.9.5-1.4.7-1.6.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2 0 .4-.1.5l-.4.5c-.1.2-.3.3-.1.6a9 9 0 0 0 3.9 3.2c.3.1.5.1.6-.1l.7-.8c.2-.2.4-.2.6-.1l1.8.9c.3.1.4.2.5.3v1z"/></svg>""",
}

# --------------------------------------------------------------------------
# content
# --------------------------------------------------------------------------
CATEGORIES = [
{
 "slug": "martial-arts",
 "name": "Martial Arts",
 "tag": "Uniforms & Belts",
 "blurb": "Competition-grade gis, uniforms and belts cut for clean lines, honest weight and hard washing cycles.",
 "long": "Traditional martial arts kit is judged the second an athlete steps on the mat. We weave, cut and stitch gis, dobok and belts to federation weights, pre-shrink every fabric and reinforce the seams that actually take the load: shoulders, skirt vents, lapel and knee panels. Your logo goes on as embroidery, sublimation or woven label.",
 "products": [
  ("Pearl Weave BJJ Gi", "550 GSM", "Pre-shrunk pearl-weave jacket with EVA-padded collar, ripstop trousers and triple-stitched stress points.", ["550 GSM", "Pearl weave", "IBJJF cut", "Sizes A0-A5"], 12),
  ("Heavyweight Karate Gi", "14 oz Canvas", "Traditional 14 oz canvas kata gi with reinforced lapel, reverse-stitched skirt and snap-crisp finish.", ["14 oz canvas", "Kata cut", "Pre-shrunk", "White / blue"], 12),
  ("Taekwondo Dobok", "WT Pattern", "Ribbed-collar dobok in breathable poly-cotton with V-neck top and elasticated waist trouser.", ["Poly-cotton", "WT pattern", "Ribbed collar", "Colour-fast"], 12),
  ("Judo Double Weave Gi", "750 GSM", "Double-weave judo jacket built for grip fighting, with bar-tacked lapel and 4-row skirt stitch.", ["750 GSM", "Double weave", "Bar-tacked", "IJF-style cut"], 10),
  ("Embroidered Rank Belt", "Cotton Core", "Eight-row stitched belt with cotton core, custom rank embroidery and colour-matched tipping.", ["8-row stitch", "Cotton core", "Custom embroidery", "Sizes 000-7"], 25),
 ],
},
{
 "slug": "mma-wear",
 "name": "MMA Wear",
 "tag": "Fight Kit",
 "blurb": "Fight shorts, rash guards and compression built to move at full extension and survive the cage floor.",
 "long": "MMA kit lives or dies on stretch recovery and seam strength. We build fight wear on four-way stretch knits and sublimated polyester, bond the panels where stitching would chafe, and flatlock everything that touches skin. Full-bleed art, team names and sponsor blocks are printed into the fabric, not onto it, so nothing cracks or peels.",
 "products": [
  ("Pro Fight Shorts", "Sublimated", "Four-way stretch shell with split side vents, hook-and-loop fly and silicone-gripped inner waistband.", ["4-way stretch", "Full sublimation", "Split vents", "Grip waistband"], 20),
  ("Long Sleeve Rash Guard", "Compression", "260 GSM poly-spandex rash guard with flatlock seams and silicone waist gripper to stop ride-up.", ["260 GSM", "Flatlock seams", "UPF 50+", "Anti-odour"], 20),
  ("Grappling Spats", "Full Length", "High-compression spats with gusseted crotch and reinforced knee panel for mat work.", ["Gusseted", "Knee panel", "Squat-proof", "4-way stretch"], 20),
  ("Vale Tudo Shorts", "Mid Thigh", "Tight-fit vale tudo shorts with bonded hem and drawcord waist that stays put under a takedown.", ["Bonded hem", "Drawcord", "Chafe-free", "Custom art"], 20),
  ("Walkout Fight Jersey", "Team Kit", "Lightweight walkout jersey with sponsor-ready panel layout and team name across the shoulders.", ["Sublimated", "Sponsor panels", "Mesh back", "Team sizing"], 15),
 ],
},
{
 "slug": "mma-grappling-dummy",
 "name": "MMA Grappling Dummy",
 "tag": "Training Gear",
 "blurb": "Unfilled and filled throwing dummies in leather and canvas, stitched to take daily slams.",
 "long": "A dummy is only as good as its seams. Ours are cut from micro-fibre leather or heavy canvas, double-lock-stitched with bonded nylon thread and finished with reinforced joints at the shoulders, hips and neck, the three places cheap dummies split. Ship them unfilled to keep freight sane, or filled and closed for ready-to-train delivery.",
 "products": [
  ("Ground & Pound Dummy", "Unfilled", "Full-body ground and pound dummy in micro-fibre leather, double lock-stitched and supplied unfilled.", ["Micro-fibre", "Unfilled", "4ft - 6ft", "Reinforced joints"], 5),
  ("Throwing Judo Dummy", "Canvas", "Heavy canvas throwing dummy with bar-tacked shoulder and hip joints for repeated slams.", ["Heavy canvas", "Bar-tacked", "Filled option", "Custom logo"], 5),
  ("Youth Training Dummy", "3ft-4ft", "Scaled-down dummy for junior programmes, same seam spec at a lighter finished weight.", ["Junior sizing", "Soft grip", "Unfilled", "Club branding"], 5),
  ("Submission Grappling Dummy", "Jointed Arms", "Articulated-arm dummy that holds position for arm bars, kimuras and guard passing drills.", ["Jointed arms", "Holds position", "Vinyl / leather", "5ft - 6ft"], 5),
  ("Wrestling Takedown Bag", "Filled", "Legged takedown bag with double-handle grip, filled and closed for immediate club use.", ["Pre-filled", "Double handles", "Abrasion shell", "Club branding"], 5),
 ],
},
{
 "slug": "fitness-wear",
 "name": "Fitness Wear",
 "tag": "Gym Apparel",
 "blurb": "Seamless, sculpted and performance-knit gym apparel for private-label and studio ranges.",
 "long": "Studio and label ranges need fit consistency across sizes and a hand-feel that sells itself in the first touch. We run seamless knits, peached poly-spandex and brushed cotton blends, grade every pattern properly rather than scaling a medium, and finish with your woven labels, hang tags and packaging so the product arrives shelf-ready.",
 "products": [
  ("Seamless Sculpt Leggings", "High Waist", "Seamless knit leggings with contoured waistband, squat-proof gusset and ribbed knee zone.", ["Seamless", "Squat-proof", "High waist", "XS-3XL"], 30),
  ("Performance Training Tee", "Dry-Fit", "Lightweight moisture-wicking tee with raglan shoulder and taped neckline for full-range lifting.", ["Moisture wick", "Raglan sleeve", "Taped neck", "Custom print"], 40),
  ("Sculpt Sports Bra", "Medium Impact", "Medium-impact bra with removable cups, wide underband and racer-back strap layout.", ["Removable cups", "Wide band", "Racer back", "XS-2XL"], 30),
  ("Tapered Jogger Pants", "Brushed Fleece", "Brushed-back fleece joggers with zip pockets, tapered leg and rib cuff that holds its shape.", ["Brushed fleece", "Zip pockets", "Tapered", "Custom label"], 25),
  ("Lifting Stringer Vest", "Open Back", "Deep-cut stringer in soft-touch cotton blend with reinforced strap join and raw-edge finish.", ["Cotton blend", "Deep cut", "Reinforced straps", "S-2XL"], 40),
 ],
},
{
 "slug": "gym-wrist-straps",
 "name": "GYM Wrist Straps",
 "tag": "Lifting Support",
 "blurb": "Lifting straps, wrist wraps and figure-8s in cotton, neoprene and leather, branded your way.",
 "long": "Support gear takes the most abuse per gram of anything in a gym bag. We build straps from heavyweight cotton webbing and full-grain leather, bar-tack every load point, and back the wrist plate with neoprene so the strap bites the bar instead of the skin. Woven labels, printed webbing and custom colourways all run from low minimums.",
 "products": [
  ("Heavy Cotton Lifting Straps", "Neoprene Pad", "24-inch cotton webbing straps with neoprene wrist pad and bar-tacked load loop.", ["24 inch", "Neoprene pad", "Bar-tacked", "Pairs"], 50),
  ("Figure-8 Deadlift Straps", "Closed Loop", "Closed-loop figure-8 straps for maximal pulls, stitched flat so nothing digs under load.", ["Closed loop", "Flat stitch", "S/M/L", "Custom colour"], 50),
  ("Stiff Wrist Wraps", "18 / 24 Inch", "Stiff-weave elastic wraps with thumb loop and wide hook-and-loop closure for pressing.", ["18/24 inch", "Thumb loop", "Stiff weave", "Printed logo"], 50),
  ("Leather Lasso Straps", "Full Grain", "Full-grain leather lasso straps that break in to the wrist and grip without slipping.", ["Full grain", "Lasso design", "Riveted", "Embossed logo"], 30),
  ("Padded Wrist Support Wrap", "Daily Train", "Lighter daily-training wrap with contoured padding and low-profile closure under gloves.", ["Contoured pad", "Low profile", "Breathable", "Club branding"], 50),
 ],
},
]

CAT_BY_SLUG = {c["slug"]: c for c in CATEGORIES}
ART_KEY = {"martial-arts": "martial-arts", "mma-wear": "mma-wear",
           "mma-grappling-dummy": "grappling-dummy", "fitness-wear": "fitness-wear",
           "gym-wrist-straps": "wrist-straps"}

def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def art(cat_slug):
    return ART[ART_KEY[cat_slug]]

# --------------------------------------------------------------------------
# layout
# --------------------------------------------------------------------------
NAV = [("Home", "index.html"), ("Collections", "collections.html"),
       ("Process", "process.html"), ("About", "about.html"), ("Contact", "contact.html")]

def head(title, desc, rel, page_class=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="{rel}assets/img/logo-green.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}assets/css/style.css">
</head>
<body class="{page_class}">
"""

def header(rel, current):
    parts = []
    for name, href in NAV:
        cur = ' aria-current="page"' if href == current else ''
        parts.append('<a href="%s%s"%s>%s</a>' % (rel, href, cur, name))
    links = "".join(parts)
    return f"""<div class="topbar"><div class="wrap">
<span>Custom manufacturing &middot; low minimums &middot; worldwide shipping</span>
<a href="tel:{PHONE_TEL}">{PHONE}</a>
<a href="mailto:{EMAIL}">{EMAIL}</a>
</div></div>
<header class="site"><div class="wrap nav">
<a class="brand" href="{rel}index.html">
<img src="{rel}assets/img/logo-green.svg" alt="NTF logo" width="42" height="42">
<span>NTF<small>Sportswear</small></span>
</a>
<button class="burger" aria-label="Toggle navigation" aria-expanded="false">&#9776;</button>
<nav class="menu">{links}<a class="btn btn-primary btn-sm" href="{rel}quote.html">Request a Quote</a></nav>
<a class="btn btn-primary btn-sm" href="{rel}quote.html">Request a Quote</a>
</div></header>
"""

def footer(rel):
    cats = "".join(f'<li><a href="{rel}collections/{c["slug"]}.html">{c["name"]}</a></li>' for c in CATEGORIES)
    return f"""<section class="cta"><div class="wrap">
<p class="eyebrow center">Ready when you are</p>
<h2>Let&rsquo;s build your line</h2>
<p class="muted" style="max-width:56ch;margin:1rem auto 0">Send us your artwork, tech pack or even a rough sketch. You get costing and a sampling plan back within one working day.</p>
<div class="btns">
<a class="btn btn-primary" href="{rel}quote.html">Request a Quote</a>
<a class="btn btn-ghost" href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp Us</a>
</div></div></section>
<footer class="site"><div class="wrap">
<div class="fgrid">
<div>
<a class="brand" href="{rel}index.html"><img src="{rel}assets/img/logo-white.svg" alt="NTF logo" width="42" height="42"><span>NTF<small>Sportswear</small></span></a>
<p class="muted" style="margin-top:1rem;max-width:36ch">Custom sportswear and combat gear manufactured in Sialkot, Pakistan for gyms, academies and apparel labels worldwide.</p>
</div>
<div><h4>Collections</h4><ul>{cats}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{rel}about.html">About NTF</a></li>
<li><a href="{rel}process.html">How We Work</a></li>
<li><a href="{rel}collections.html">All Collections</a></li>
<li><a href="{rel}quote.html">Request a Quote</a></li>
</ul></div>
<div><h4>Contact</h4><ul>
<li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a></li>
<li class="muted">Sialkot, Punjab, Pakistan</li>
</ul></div>
</div>
<div class="legal"><span>&copy; <span id="year">2026</span> NTF Sportswear. All rights reserved.</span>
<span>Manufacturer of custom martial arts, MMA and fitness apparel.</span></div>
</div></footer>
<a class="float" href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{ICON['wa']}</a>
<script src="{rel}assets/js/main.js"></script>
</body>
</html>
"""

def product_card(cat, p, rel):
    name, tag, desc, specs, moq = p
    slug = slugify(name)
    chips = "".join(f"<li>{s}</li>" for s in specs)
    return f"""<article class="card reveal">
<a href="{rel}products/{slug}.html" class="thumb"><span class="tag">{tag}</span>{art(cat['slug'])}</a>
<div class="card-body">
<h3><a href="{rel}products/{slug}.html">{name}</a></h3>
<p class="muted" style="font-size:.93rem;margin:0">{desc}</p>
<ul class="specs">{chips}</ul>
<p class="moq" style="margin:.6rem 0 0">MOQ {moq} pcs / design</p>
<a class="btn btn-ghost btn-sm" style="margin-top:.8rem;align-self:flex-start" href="{rel}quote.html?product={name.replace(' ', '%20')}&amp;category={cat['slug']}">Request a Quote</a>
</div></article>"""

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)

# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def build_home():
    rel = ""
    cats = "".join(f"""<a class="card cat reveal" href="collections/{c['slug']}.html">
<div class="thumb">{art(c['slug'])}</div>
<div class="card-body">
<p class="count">5 products</p>
<h3>{c['name']}</h3>
<p class="muted" style="font-size:.92rem">{c['blurb']}</p>
<span class="go">View collection &rarr;</span>
</div></a>""" for c in CATEGORIES)

    features = "".join(f"""<div class="feature reveal"><div class="n">{n}</div><h3>{t}</h3><p>{d}</p></div>"""
        for n, t, d in [
        ("01", "Low minimums", "Start at 5 to 50 pieces per design, so new labels can test a range before committing to volume."),
        ("02", "In-house cutting &amp; stitching", "Pattern, cut, sublimation, embroidery and finishing all run under one roof in Sialkot."),
        ("03", "Real samples first", "Nothing goes to bulk until you have held the sample and signed it off."),
        ("04", "Fabric you can name", "GSM, composition and mill are on your spec sheet, not hidden behind a marketing word."),
        ])

    steps = "".join(f"<li><div><b>{t}</b><span>{d}</span></div></li>" for t, d in [
        ("Share the brief", "Artwork, tech pack, competitor sample or a sketch on a napkin. All of it works."),
        ("Costing in 24 hours", "You get per-unit pricing, fabric options and a realistic lead time."),
        ("Sample &amp; sign-off", "We make it, ship it, adjust it. You approve before bulk starts."),
        ("Bulk &amp; delivery", "Production, QC on every piece, packing your way, door-to-door freight."),
    ])

    return (head("NTF Sportswear | Custom Martial Arts, MMA &amp; Fitness Apparel Manufacturer",
                 "NTF manufactures custom martial arts uniforms, MMA fight wear, grappling dummies, gym apparel and lifting straps. Low minimums, your branding, worldwide shipping.", rel)
    + header(rel, "index.html")
    + f"""<section class="hero"><div class="wrap hero-grid">
<div>
<p class="eyebrow">Custom sportswear manufacturer</p>
<h1>Built for the<em>fight in you</em></h1>
<p class="lead">NTF makes custom martial arts uniforms, MMA fight wear, grappling dummies, gym apparel and lifting support &mdash; cut, stitched and branded to your spec in Sialkot, Pakistan. Low minimums. Real samples. Shipped worldwide.</p>
<div class="hero-cta">
<a class="btn btn-primary" href="quote.html">Request a Quote</a>
<a class="btn btn-ghost" href="collections.html">Browse Collections</a>
</div>
<div class="hero-stats">
<div><b><span data-count="25" data-suffix="+">0</span></b><span>Products in stock ranges</span></div>
<div><b><span data-count="40" data-suffix="+">0</span></b><span>Countries shipped</span></div>
<div><b><span data-count="24" data-suffix="h">0</span></b><span>Quote turnaround</span></div>
</div>
</div>
<div class="hero-art">
<span class="ring"></span><span class="ring"></span><span class="ring"></span>
<img class="mark" src="assets/img/logo-green.svg" alt="NTF monogram" width="260" height="260">
</div>
</div></section>

<div class="ticker"><div class="ticker-track">
{"".join(['<span>Martial Arts</span><span>&bull;</span><span>MMA Wear</span><span>&bull;</span><span>Grappling Dummies</span><span>&bull;</span><span>Fitness Wear</span><span>&bull;</span><span>Wrist Straps</span><span>&bull;</span>'] * 4)}
</div></div>

<section><div class="wrap">
<div class="sec-head">
<div><p class="eyebrow">Collections</p><h2>Five ranges,<br>one factory</h2></div>
<p>Every range below is made to order. Pick a base product, send your colours and artwork, and we build it as your product &mdash; your labels, your packaging, your name on the box.</p>
</div>
<div class="grid g3">{cats}</div>
</div></section>

<section class="band"><div class="wrap split">
<div class="reveal">
<p class="eyebrow">Why NTF</p>
<h2>No middlemen,<br>no surprises</h2>
<p class="muted">You talk to the people who cut the fabric. That means honest lead times, fabric specs you can verify, and changes that actually get made instead of getting lost between three agents and a trading house.</p>
<a class="btn btn-primary" href="about.html">More about us</a>
</div>
<div class="grid g2">{features}</div>
</div></section>

<section><div class="wrap split">
<div class="reveal">
<p class="eyebrow">How it works</p>
<h2>From brief to bulk<br>in four steps</h2>
<p class="muted">Most clients go from first message to approved sample inside two weeks. Bulk follows in three to four, depending on fabric and decoration.</p>
<a class="btn btn-ghost" href="process.html">See the full process</a>
</div>
<ul class="steps reveal">{steps}</ul>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">Questions</p><h2>Straight answers</h2></div></div>
<div class="reveal">
<details open><summary>What is the minimum order?</summary><p>It depends on the product. Grappling dummies start at 5 pieces, martial arts uniforms at 10 to 12, apparel at 20 to 40, and straps at 30 to 50 per design. Mixed sizes within a design count toward the same minimum.</p></details>
<details><summary>Can you work from my tech pack?</summary><p>Yes. Send a tech pack, a physical sample, or reference photos and we will build the pattern from it and flag anything that will not behave in production.</p></details>
<details><summary>How long does sampling take?</summary><p>Seven to ten working days for most apparel, slightly longer for dummies and leather goods. Courier time is on top and we share the tracking number as soon as it ships.</p></details>
<details><summary>Do you handle branding and packaging?</summary><p>Woven labels, hang tags, heat transfers, embroidery, poly bags and printed cartons. Tell us how you want it to arrive and it arrives that way.</p></details>
<details><summary>Where do you ship?</summary><p>Worldwide by air or sea, DDU or DDP, through DHL, FedEx or your own forwarder. Most clients are in the UK, US, Europe, Australia and the Gulf.</p></details>
</div>
</div></section>
"""
    + footer(rel))

def build_collections():
    rel = ""
    cards = "".join(f"""<a class="card cat reveal" href="collections/{c['slug']}.html">
<div class="thumb">{art(c['slug'])}</div>
<div class="card-body">
<p class="count">{c['tag']} &middot; 5 products</p>
<h3>{c['name']}</h3>
<p class="muted" style="font-size:.92rem">{c['blurb']}</p>
<span class="go">View collection &rarr;</span>
</div></a>""" for c in CATEGORIES)
    return (head("Collections | NTF Custom Sportswear",
                 "Browse NTF collections: martial arts uniforms, MMA wear, grappling dummies, fitness wear and gym wrist straps. All made to order.", rel)
    + header(rel, "collections.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Collections</p>
<p class="eyebrow">Made to order</p>
<h1>Collections</h1>
<p>Five ranges covering the mat, the cage and the gym floor. Every product on this site is a starting point &mdash; colours, fabric weight, cut and branding are yours to change.</p>
</div></section>
<section><div class="wrap"><div class="grid g3">{cards}</div></div></section>
"""
    + footer(rel))

def build_category(c):
    rel = "../"
    cards = "".join(product_card(c, p, rel) for p in c["products"])
    others = "".join(f'<a class="btn btn-ghost btn-sm" href="{o["slug"]}.html">{o["name"]}</a>'
                     for o in CATEGORIES if o["slug"] != c["slug"])
    return (head(f"{c['name']} | NTF Custom Sportswear",
                 c["blurb"], rel)
    + header(rel, "collections.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="{rel}index.html">Home</a> / <a href="{rel}collections.html">Collections</a> / {c['name']}</p>
<p class="eyebrow">{c['tag']}</p>
<h1>{c['name']}</h1>
<p>{c['long']}</p>
<div class="hero-cta" style="margin-top:1.6rem"><a class="btn btn-primary" href="{rel}quote.html?category={c['slug']}">Request a Quote</a><a class="btn btn-ghost" href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a></div>
</div></section>
<section><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">5 products</p><h2>{c['name']} range</h2></div>
<p>Prices are quoted per design and drop with volume. Every item can be re-specced in your fabric, colourway and branding.</p></div>
<div class="grid g3">{cards}</div>
</div></section>
<section class="band"><div class="wrap center">
<p class="eyebrow center">Keep browsing</p>
<h2>Other collections</h2>
<div class="hero-cta" style="justify-content:center;margin-top:1.6rem">{others}</div>
</div></section>
"""
    + footer(rel))

def build_product(c, p):
    rel = "../"
    name, tag, desc, specs, moq = p
    slug = slugify(name)
    rows = "".join(f"<li>{s}</li>" for s in specs)
    related = "".join(product_card(c, q, rel) for q in c["products"] if q[0] != name)
    return (head(f"{name} | {c['name']} | NTF Custom Sportswear", desc, rel)
    + header(rel, "collections.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="{rel}index.html">Home</a> / <a href="{rel}collections.html">Collections</a> / <a href="{rel}collections/{c['slug']}.html">{c['name']}</a> / {name}</p>
</div></section>
<section style="padding-top:2rem"><div class="wrap split">
<div class="card" style="padding:0">
<div class="thumb" style="aspect-ratio:1"><span class="tag">{tag}</span>{art(c['slug'])}</div>
</div>
<div>
<p class="eyebrow">{c['name']}</p>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem)">{name}</h1>
<p class="muted" style="margin-top:1.2rem;font-size:1.05rem">{desc}</p>
<ul class="specs" style="margin:1.2rem 0">{rows}</ul>
<p class="moq">Minimum order {moq} pcs per design</p>
<div class="hero-cta" style="margin-top:1.4rem">
<a class="btn btn-primary" href="{rel}quote.html?product={name.replace(' ', '%20')}&amp;category={c['slug']}">Request a Quote</a>
<a class="btn btn-ghost" href="tel:{PHONE_TEL}">Call {PHONE}</a>
</div>
<ul class="steps" style="margin-top:2rem">
<li><div><b>Customisation</b><span>Your colourway, fabric weight, cut and logo placement. Embroidery, sublimation, heat transfer or woven label.</span></div></li>
<li><div><b>Sampling</b><span>Pre-production sample in 7 to 10 working days, revised until you sign it off.</span></div></li>
<li><div><b>Lead time</b><span>Roughly 3 to 4 weeks for bulk after sample approval, depending on quantity and decoration.</span></div></li>
</ul>
</div>
</div></section>
<section class="band"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">More from this range</p><h2>{c['name']}</h2></div>
<a class="btn btn-ghost btn-sm" href="{rel}collections/{c['slug']}.html">View all 5 &rarr;</a></div>
<div class="grid g4">{related}</div>
</div></section>
"""
    + footer(rel))

def build_quote():
    rel = ""
    opts = "".join(f'<option value="{c["slug"]}">{c["name"]}</option>' for c in CATEGORIES)
    services = ["Custom manufacturing", "Private label", "Sampling only", "Bulk reorder", "Design help"]
    chips = "".join(f'<label class="chip"><input type="checkbox" name="services" value="{s}"><span>{s}</span></label>' for s in services)
    return (head("Request a Quote | NTF Custom Sportswear",
                 "Tell NTF what you want made and get per-unit costing, fabric options and a lead time back within one working day.", rel)
    + header(rel, "quote.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Request a Quote</p>
<p class="eyebrow">Costing in 24 hours</p>
<h1>Request a quote</h1>
<p>Fill this in and we come back with per-unit pricing, fabric options, sampling cost and a realistic lead time. No account, no subscription, no sales sequence.</p>
</div></section>
<section><div class="wrap split" style="align-items:start">
<form class="formcard" id="quote-form" novalidate>
<div class="ok"><b>Thanks &mdash; your quote request is ready to send.</b><p class="muted" style="margin:.4rem 0 0">Your email app should open with the details filled in. If it does not, email us directly at <a href="mailto:{EMAIL}" style="color:var(--green-2)">{EMAIL}</a>.</p></div>
<div class="two">
<div class="field"><label for="name">Your name *</label><input id="name" name="name" required autocomplete="name"><span class="err" id="err-name"></span></div>
<div class="field"><label for="company">Company / gym</label><input id="company" name="company" autocomplete="organization"></div>
</div>
<div class="two">
<div class="field"><label for="email">Email *</label><input id="email" name="email" type="email" required autocomplete="email"><span class="err" id="err-email"></span></div>
<div class="field"><label for="phone">Phone / WhatsApp</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
</div>
<div class="two">
<div class="field"><label for="category">Category *</label>
<select id="category" name="category" required><option value="">Select a category</option>{opts}<option value="other">Something else</option></select>
<span class="err" id="err-category"></span></div>
<div class="field"><label for="quantity">Quantity *</label><input id="quantity" name="quantity" type="number" min="1" placeholder="e.g. 100" required><span class="err" id="err-quantity"></span></div>
</div>
<div class="field"><label>What do you need?</label><div class="chips">{chips}</div></div>
<div class="field"><label for="details">Project details *</label>
<textarea id="details" name="details" required placeholder="Products, fabric, colours, sizes, branding, deadline, delivery country..."></textarea>
<span class="err" id="err-details"></span></div>
<button class="btn btn-primary" type="submit" style="width:100%;justify-content:center">Send quote request</button>
<p class="muted" style="font-size:.82rem;margin:.9rem 0 0">We reply from {EMAIL}. Your details are used for this quote only.</p>
</form>
<div>
<div class="grid" style="gap:.9rem">
<div class="info"><div class="ic">{ICON['phone']}</div><div><b>Call or WhatsApp</b><a href="tel:{PHONE_TEL}">{PHONE}</a></div></div>
<div class="info"><div class="ic">{ICON['mail']}</div><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="info"><div class="ic">{ICON['clock']}</div><div><b>Response time</b><span class="muted">Within one working day, Mon to Sat</span></div></div>
<div class="info"><div class="ic">{ICON['factory']}</div><div><b>Minimums</b><span class="muted">From 5 pieces per design on dummies, 10 to 50 on apparel and straps</span></div></div>
</div>
<div class="formcard" style="margin-top:1.4rem">
<h3>What to send us</h3>
<ul class="steps" style="margin-top:1rem">
<li><div><b>Artwork</b><span>AI, EPS, PDF or high-resolution PNG. A phone photo of a sketch is enough to start.</span></div></li>
<li><div><b>Size breakdown</b><span>How many of each size, or tell us your market and we will suggest a curve.</span></div></li>
<li><div><b>Deadline</b><span>Event date or shelf date, so we can work the schedule backwards.</span></div></li>
</ul>
</div>
</div>
</div></section>
"""
    + footer(rel))

def build_about():
    rel = ""
    return (head("About | NTF Custom Sportswear",
                 "NTF is a Sialkot-based manufacturer of custom martial arts, MMA and fitness apparel and training gear for gyms, academies and apparel labels.", rel)
    + header(rel, "about.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / About</p>
<p class="eyebrow">Who we are</p>
<h1>A factory,<br>not a middleman</h1>
<p>NTF is a custom sportswear manufacturer based in Sialkot, Pakistan &mdash; the city that has been making the world&rsquo;s combat sports gear for a century. We make for gyms, academies, fight teams and apparel labels who want their own product rather than a logo slapped on someone else&rsquo;s catalogue.</p>
</div></section>

<section><div class="wrap split">
<div class="reveal">
<h2>What we actually do</h2>
<p class="muted">We take a brief &mdash; a tech pack, a competitor sample, sometimes just a conversation &mdash; and turn it into a pattern, a sample and then a production run. Cutting, stitching, sublimation, embroidery and finishing all happen in-house, so when you ask for a change it reaches the person holding the scissors.</p>
<p class="muted">Our ranges cover martial arts uniforms and belts, MMA fight wear, grappling dummies, gym apparel and lifting support. If it is worn or thrown in a combat or strength gym, we have probably built it.</p>
</div>
<div class="grid g2">
<div class="feature reveal"><div class="n">01</div><h3>Own your product</h3><p>Your labels, your packaging, your spec sheet. We do not sell your design to the next buyer.</p></div>
<div class="feature reveal"><div class="n">02</div><h3>Verifiable specs</h3><p>GSM, composition and thread type in writing, so you can check what you received against what you ordered.</p></div>
<div class="feature reveal"><div class="n">03</div><h3>QC on every piece</h3><p>Measurement, stitch and print checks before packing, not a sample of the carton.</p></div>
<div class="feature reveal"><div class="n">04</div><h3>Grow with volume</h3><p>Start at a handful of pieces to test the market, scale into container loads on the same patterns.</p></div>
</div>
</div></section>

<section class="band"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">The standard</p><h2>How we judge<br>our own work</h2></div>
<p>Three things decide whether a piece leaves the floor: does it measure to spec, does the seam survive load, and does the decoration survive washing. Everything else is opinion.</p></div>
<div class="grid g3">
<div class="feature reveal"><h3>Measure to spec</h3><p>Graded patterns per size, checked against the tech pack tolerance before packing.</p></div>
<div class="feature reveal"><h3>Seams under load</h3><p>Bar-tacks and lock-stitching at every stress point &mdash; lapels, gussets, strap joins, dummy joints.</p></div>
<div class="feature reveal"><h3>Decoration that lasts</h3><p>Sublimation into the fabric, embroidery with backing, transfers cured properly. Wash-tested, not guessed.</p></div>
</div>
</div></section>
"""
    + footer(rel))

def build_process():
    rel = ""
    return (head("How We Work | NTF Custom Sportswear",
                 "From brief to bulk: how NTF quotes, samples, produces and ships custom sportswear orders.", rel)
    + header(rel, "process.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Process</p>
<p class="eyebrow">How we work</p>
<h1>Brief to bulk</h1>
<p>No portals, no onboarding calls. A short, honest sequence that most clients complete in four to six weeks from first message to delivered cartons.</p>
</div></section>
<section><div class="wrap grid g2">
<div class="feature reveal"><div class="n">01</div><h3>Brief &amp; costing</h3><p>Send artwork, a tech pack or a reference product. Within one working day you get per-unit pricing at two or three quantity breaks, fabric options and a lead time.</p></div>
<div class="feature reveal"><div class="n">02</div><h3>Pattern &amp; mock-up</h3><p>We build the pattern and send a digital mock-up with your artwork placed, so placement and proportion are agreed before anything is cut.</p></div>
<div class="feature reveal"><div class="n">03</div><h3>Physical sample</h3><p>A pre-production sample ships in 7 to 10 working days with tracking. Wear it, wash it, pull on it. Tell us what to change.</p></div>
<div class="feature reveal"><div class="n">04</div><h3>Revision &amp; sign-off</h3><p>Fit or spec changes are applied and re-sampled where needed. Bulk starts only once you approve in writing.</p></div>
<div class="feature reveal"><div class="n">05</div><h3>Production &amp; QC</h3><p>3 to 4 weeks for most bulk runs. Every piece is measured and inspected, and we share line photos mid-run.</p></div>
<div class="feature reveal"><div class="n">06</div><h3>Packing &amp; freight</h3><p>Poly-bagged, tagged and boxed your way, then shipped door-to-door by air or sea &mdash; our forwarder or yours.</p></div>
</div></section>
<section class="band"><div class="wrap split">
<div class="reveal">
<p class="eyebrow">Good to know</p>
<h2>The details that<br>save you weeks</h2>
</div>
<div class="reveal">
<details open><summary>Sampling charges</summary><p>Samples are charged at cost plus courier and credited against your first bulk invoice.</p></details>
<details><summary>Payment terms</summary><p>Typically 50% to start production and 50% against shipping documents. Bank transfer or Wise.</p></details>
<details><summary>Repeat orders</summary><p>Patterns and artwork stay on file, so a reorder skips straight to production with no sampling delay.</p></details>
<details><summary>Small changes mid-run</summary><p>Colour or label changes are usually fine before cutting starts. After that they cost time, so we flag it honestly rather than quietly missing your date.</p></details>
</div>
</div></section>
"""
    + footer(rel))

def build_contact():
    rel = ""
    return (head("Contact | NTF Custom Sportswear",
                 f"Contact NTF Sportswear. Call {PHONE} or email {EMAIL} for custom sportswear manufacturing.", rel)
    + header(rel, "contact.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Contact</p>
<p class="eyebrow">Talk to us</p>
<h1>Contact NTF</h1>
<p>Message us on WhatsApp for the fastest answer, or email if you have files to send. We read everything ourselves.</p>
</div></section>
<section><div class="wrap split" style="align-items:start">
<div class="grid" style="gap:.9rem">
<div class="info reveal"><div class="ic">{ICON['phone']}</div><div><b>Phone &amp; WhatsApp</b><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">Open WhatsApp chat</a></div></div>
<div class="info reveal"><div class="ic">{ICON['mail']}</div><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="info reveal"><div class="ic">{ICON['pin']}</div><div><b>Where we are</b><span class="muted">Sialkot, Punjab, Pakistan</span></div></div>
<div class="info reveal"><div class="ic">{ICON['clock']}</div><div><b>Hours</b><span class="muted">Monday to Saturday, 9am to 7pm PKT (UTC+5)</span></div></div>
</div>
<div class="formcard reveal">
<p class="eyebrow">Fastest route</p>
<h2 style="margin-block:.6rem 1rem">Send a quote request</h2>
<p class="muted">The quote form captures quantity, category and branding in one go, which means our first reply can already carry pricing instead of questions.</p>
<a class="btn btn-primary" href="quote.html">Request a Quote</a>
<div style="margin-top:2rem">
<h3>Prefer to write?</h3>
<p class="muted" style="margin-top:.6rem">Email <a href="mailto:{EMAIL}" style="color:var(--green-2)">{EMAIL}</a> with your artwork and quantity and we will take it from there.</p>
</div>
</div>
</div></section>
"""
    + footer(rel))

def build_404():
    rel = ""
    return (head("Page not found | NTF Sportswear", "That page does not exist.", rel)
    + header(rel, "")
    + f"""<section class="hero"><div class="wrap center">
<p class="eyebrow center">404</p>
<h1>Missed the takedown</h1>
<p class="lead" style="margin-inline:auto">That page is not here. Try the collections, or send us what you were looking for.</p>
<div class="hero-cta" style="justify-content:center"><a class="btn btn-primary" href="index.html">Back home</a><a class="btn btn-ghost" href="collections.html">Collections</a></div>
</div></section>
"""
    + footer(rel))

def main():
    write("index.html", build_home())
    write("collections.html", build_collections())
    write("quote.html", build_quote())
    write("about.html", build_about())
    write("process.html", build_process())
    write("contact.html", build_contact())
    write("404.html", build_404())
    for c in CATEGORIES:
        write(f"collections/{c['slug']}.html", build_category(c))
        for p in c["products"]:
            write(f"products/{slugify(p[0])}.html", build_product(c, p))
    # sitemap
    urls = ["index.html", "collections.html", "quote.html", "about.html", "process.html", "contact.html"]
    urls += [f"collections/{c['slug']}.html" for c in CATEGORIES]
    urls += [f"products/{slugify(p[0])}.html" for c in CATEGORIES for p in c["products"]]
    base = "https://danialhyatt7-collab.github.io/NTF/"
    sm = "\n".join(f"  <url><loc>{base}{u}</loc></url>" for u in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")
    write(".nojekyll", "")

if __name__ == "__main__":
    main()
