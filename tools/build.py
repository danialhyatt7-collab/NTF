#!/usr/bin/env python3
"""Static site generator for the NTF custom sportswear website.

Layout follows a technical catalog structure (numbered sections, mono spec
labels, size chips, spec matrix) rendered in a light corporate theme with a
dark-mode switch.

Run:  python3 tools/build.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def ver(relpath):
    """Cache-busting query built from the asset's content hash.

    Without it a browser can hold a stale stylesheet against fresh HTML,
    which silently breaks the theming and layout that CSS carries."""
    import hashlib
    full = os.path.join(ROOT, relpath)
    try:
        return "?v=" + hashlib.md5(open(full, "rb").read()).hexdigest()[:8]
    except OSError:
        return ""

PHONE = "+92 333 8686122"
PHONE_TEL = "+923338686122"
PHONE_WA = "923338686122"
EMAIL = "support@ntf.com.pk"

I = {  # inline icons (stroke = currentColor)
"arrow": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
"phone": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.2a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
"mail": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7 10-7"/></svg>',
"pin": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
"clock": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
"wa": '<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2zm5.2 14.1c-.2.6-1.2 1.2-1.7 1.2-.5.1-1 .1-1.7-.1a13 13 0 0 1-5.6-4.4c-.6-.9-1-1.9-1-2.8 0-.9.5-1.4.7-1.6.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2 0 .4-.1.5l-.4.5c-.1.2-.3.3-.1.6a9 9 0 0 0 3.9 3.2c.3.1.5.1.6-.1l.7-.8c.2-.2.4-.2.6-.1l1.8.9c.3.1.4.2.5.3v1z"/></svg>',
"up": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5M5 12l7-7 7 7"/></svg>',
"moon": '<svg class="moon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
"sun": '<svg class="sun" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
"scissors": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/></svg>',
"layers": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 9 5-9 5-9-5 9-5zM3 12l9 5 9-5M3 17l9 5 9-5"/></svg>',
"shield": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/></svg>',
"globe": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18 15 15 0 0 1 0-18z"/></svg>',
"gauge": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM13.4 10.6 19 5M20.5 16a9 9 0 1 0-17 0"/></svg>',
"tag": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20.6 13.4 12 22l-9-9V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg>',
"box": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/></svg>',
}

def P(name, tags, sub, sizes, moq, desc, specs, img, out=()):
    return dict(name=name, tags=tags, sub=sub, sizes=sizes, moq=moq,
                desc=desc, specs=specs, img=img, out=out)

CATEGORIES = [
{
 "slug": "martial-arts", "name": "Martial Arts", "tag": "Uniforms & Belts", "hero": "ma-hero",
 "blurb": "Competition-grade gis, dobok and belts cut to federation weights and finished with your branding.",
 "long": "Traditional martial arts kit is judged the moment an athlete steps on the mat. We weave, cut and stitch gis, dobok and belts to federation weights, pre-shrink every fabric, and reinforce the seams that actually take load: shoulders, skirt vents, lapel and knee panels. Your logo goes on as embroidery, sublimation or a woven label.",
 "products": [
  P("Pearl Weave BJJ Gi", ["550 GSM", "Pearl Weave"], "Pre-shrunk // IBJJF cut", ["A0","A1","A2","A3","A4","A5"], 12,
    "Pre-shrunk pearl-weave jacket with EVA-padded collar, ripstop trousers and triple-stitched stress points.",
    [("Fabric","550 GSM pearl weave cotton"),("Trouser","10 oz ripstop, 4 belt loops"),("Collar","EVA foam core, bar-tacked"),("Decoration","Embroidery, woven patch, sublimated panel")], "ma-bjj-gi"),
  P("Heavyweight Karate Gi", ["14 oz", "Canvas"], "Kata cut // Pre-shrunk", ["000","0","1","2","3","4","5","6"], 12,
    "Traditional 14 oz canvas kata gi with reinforced lapel, reverse-stitched skirt and a snap-crisp finish.",
    [("Fabric","14 oz cotton canvas"),("Cut","Traditional kata, long skirt"),("Lapel","Multi-row stitched, pre-shrunk"),("Colours","White, blue, black")], "ma-karate-gi"),
  P("Taekwondo Dobok", ["Poly-Cotton", "WT Pattern"], "Ribbed collar // V-neck", ["140","150","160","170","180","190"], 12,
    "Ribbed-collar dobok in breathable poly-cotton with V-neck top and elasticated waist trouser.",
    [("Fabric","65/35 poly-cotton, 240 GSM"),("Pattern","WT competition shape"),("Collar","Ribbed, colour-fast"),("Waist","Elastic + drawcord")], "ma-dobok"),
  P("Judo Double Weave Gi", ["750 GSM", "Double Weave"], "Grip-fight build // IJF-style", ["1","2","3","4","5","6","7"], 10,
    "Double-weave judo jacket built for grip fighting, with bar-tacked lapel and a four-row skirt stitch.",
    [("Fabric","750 GSM double weave cotton"),("Lapel","Bar-tacked, high-density"),("Skirt","4-row lock stitch"),("Cut","IJF-style sleeve and skirt length")], "ma-judo-gi"),
  P("Embroidered Rank Belt", ["8-Row", "Cotton Core"], "Custom rank // Colour tipping", ["000","0","1","2","3","4","5","6","7"], 25,
    "Eight-row stitched belt with a cotton core, custom rank embroidery and colour-matched tipping.",
    [("Build","8-row stitch, cotton core"),("Width","4.5 cm standard"),("Decoration","Embroidered name, rank and club"),("Finish","Colour-matched tip bar")], "ma-belt"),
 ]},
{
 "slug": "mma-wear", "name": "MMA Wear", "tag": "Fight Kit", "hero": "mma-hero",
 "blurb": "Fight shorts, rash guards and compression built to move at full extension and survive the cage floor.",
 "long": "MMA kit lives or dies on stretch recovery and seam strength. We build fight wear on four-way stretch knits and sublimated polyester, bond the panels where stitching would chafe, and flatlock everything that touches skin. Full-bleed art, team names and sponsor blocks are printed into the fabric rather than onto it, so nothing cracks or peels.",
 "products": [
  P("Pro Fight Shorts", ["4-Way Stretch", "Sublimated"], "Split vents // Grip waistband", ["S","M","L","XL","2XL"], 20,
    "Four-way stretch shell with split side vents, hook-and-loop fly and a silicone-gripped inner waistband.",
    [("Shell","Four-way stretch polyester"),("Vents","Split side, bonded hem"),("Closure","Hook-and-loop fly + drawcord"),("Print","Full sublimation, edge to edge")], "mma-shorts"),
  P("Long Sleeve Rash Guard", ["260 GSM", "Flatlock"], "UPF 50+ // Anti-odour", ["S","M","L","XL","2XL"], 20,
    "260 GSM poly-spandex rash guard with flatlock seams and a silicone waist gripper that stops ride-up.",
    [("Fabric","260 GSM poly-spandex"),("Seams","Flatlock, chafe-free"),("Waist","Silicone gripper tape"),("Finish","UPF 50+, anti-odour treatment")], "mma-rashguard"),
  P("Grappling Spats", ["Compression", "Gusseted"], "Knee panel // Squat-proof", ["S","M","L","XL","2XL"], 20,
    "High-compression spats with a gusseted crotch and reinforced knee panel for mat work.",
    [("Fabric","280 GSM poly-spandex"),("Gusset","Diamond, flatlocked"),("Knee","Double-layer abrasion panel"),("Waist","Wide bonded band")], "mma-spats"),
  P("Vale Tudo Shorts", ["Bonded Hem", "Mid Thigh"], "Tight fit // Drawcord", ["S","M","L","XL","2XL"], 20,
    "Tight-fit vale tudo shorts with a bonded hem and drawcord waist that stays put under a takedown.",
    [("Fabric","Compression knit, 4-way"),("Hem","Laser-cut, bonded"),("Waist","Internal drawcord"),("Length","Mid-thigh, custom on request")], "mma-valetudo"),
  P("Walkout Fight Jersey", ["Team Kit", "Mesh Back"], "Sponsor panels // Sublimated", ["S","M","L","XL","2XL","3XL"], 15,
    "Lightweight walkout jersey with a sponsor-ready panel layout and team name across the shoulders.",
    [("Fabric","150 GSM sublimation poly"),("Back","Engineered mesh zone"),("Layout","Pre-mapped sponsor blocks"),("Sizing","Team grading, S-3XL")], "mma-jersey"),
 ]},
{
 "slug": "mma-grappling-dummy", "name": "MMA Grappling Dummy", "tag": "Training Gear", "hero": "dummy-hero",
 "blurb": "Unfilled and filled throwing dummies in micro-fibre leather and heavy canvas, stitched to take daily slams.",
 "long": "A dummy is only as good as its seams. Ours are cut from micro-fibre leather or heavy canvas, double lock-stitched with bonded nylon thread, and reinforced at the shoulders, hips and neck: the three places cheap dummies split. Ship them unfilled to keep freight sane, or filled and closed for ready-to-train delivery.",
 "products": [
  P("Ground & Pound Dummy", ["Micro-Fibre", "Unfilled"], "Double lock-stitch // Reinforced joints", ["4FT","5FT","6FT"], 5,
    "Full-body ground and pound dummy in micro-fibre leather, double lock-stitched and supplied unfilled.",
    [("Shell","Micro-fibre leather, 1.2 mm"),("Stitch","Double lock, bonded nylon"),("Fill","Shipped unfilled (textile offcuts recommended)"),("Height","4 ft to 6 ft")], "dummy-gp"),
  P("Throwing Judo Dummy", ["Heavy Canvas", "Bar-Tacked"], "Filled option // Custom logo", ["4FT","5FT","6FT"], 5,
    "Heavy canvas throwing dummy with bar-tacked shoulder and hip joints for repeated slams.",
    [("Shell","18 oz cotton canvas"),("Joints","Bar-tacked shoulders and hips"),("Fill","Unfilled or pre-filled"),("Branding","Screen print or embroidered patch")], "dummy-throw"),
  P("Youth Training Dummy", ["Junior", "Soft Grip"], "3FT-4FT // Club branding", ["3FT","3.5FT","4FT"], 5,
    "Scaled-down dummy for junior programmes, with the same seam spec at a lighter finished weight.",
    [("Shell","Soft-grip vinyl or canvas"),("Weight","8 kg to 15 kg filled"),("Fill","Unfilled as standard"),("Use","Junior classes, technique drills")], "dummy-youth"),
  P("Submission Grappling Dummy", ["Jointed Arms", "Holds Position"], "Arm bars // Guard passing", ["5FT","5.5FT","6FT"], 5,
    "Articulated-arm dummy that holds position for arm bars, kimuras and guard-passing drills.",
    [("Arms","Articulated, position-holding"),("Shell","Vinyl or micro-fibre leather"),("Stitch","Double lock + bar-tack"),("Height","5 ft to 6 ft")], "dummy-sub"),
  P("Wrestling Takedown Bag", ["Pre-Filled", "Double Handle"], "Abrasion shell // Ready to train", ["70CM","90CM","110CM"], 5,
    "Legged takedown bag with a double-handle grip, filled and closed for immediate club use.",
    [("Shell","Abrasion-resistant synthetic"),("Handles","Double, bar-tacked"),("Fill","Pre-filled, closed"),("Weight","25 kg to 45 kg")], "dummy-bag"),
 ]},
{
 "slug": "fitness-wear", "name": "Fitness Wear", "tag": "Gym Apparel", "hero": "fit-hero",
 "blurb": "Seamless, sculpted and performance-knit gym apparel for private-label ranges and studio kit.",
 "long": "Studio and label ranges need fit consistency across the size run and a hand-feel that sells itself on first touch. We run seamless knits, peached poly-spandex and brushed cotton blends, grade every pattern properly instead of scaling a medium, and finish with your woven labels, hang tags and packaging so the product lands shelf-ready.",
 "products": [
  P("Seamless Sculpt Leggings", ["Seamless", "High Waist"], "Squat-proof // Contour band", ["XS","S","M","L","XL","2XL","3XL"], 30,
    "Seamless knit leggings with a contoured waistband, squat-proof gusset and ribbed knee zone.",
    [("Knit","Seamless nylon-spandex"),("Waist","Contoured, 12 cm band"),("Gusset","Squat-proof, opaque"),("Sizes","XS to 3XL, graded")], "fit-leggings"),
  P("Performance Training Tee", ["Dry-Fit", "Raglan"], "Moisture wick // Taped neck", ["S","M","L","XL","2XL"], 40,
    "Lightweight moisture-wicking tee with raglan shoulders and a taped neckline for full-range lifting.",
    [("Fabric","140 GSM poly micro-mesh"),("Shoulder","Raglan, chafe-free"),("Neck","Self-fabric tape"),("Print","Screen, transfer or sublimation")], "fit-tee"),
  P("Sculpt Sports Bra", ["Medium Impact", "Removable Cups"], "Wide band // Racer back", ["XS","S","M","L","XL","2XL"], 30,
    "Medium-impact bra with removable cups, a wide underband and racer-back strap layout.",
    [("Support","Medium impact"),("Cups","Removable moulded pads"),("Band","Wide elastic underband"),("Straps","Racer back, bar-tacked")], "fit-bra"),
  P("Tapered Jogger Pants", ["Brushed Fleece", "Zip Pockets"], "Tapered leg // Rib cuff", ["S","M","L","XL","2XL"], 25,
    "Brushed-back fleece joggers with zip pockets, a tapered leg and a rib cuff that holds its shape.",
    [("Fabric","280 GSM brushed fleece"),("Pockets","Two zip side, one back"),("Cuff","2x2 rib, elastane blend"),("Waist","Elastic + flat drawcord")], "fit-jogger"),
  P("Lifting Stringer Vest", ["Cotton Blend", "Deep Cut"], "Open back // Raw edge", ["S","M","L","XL","2XL"], 40,
    "Deep-cut stringer in a soft-touch cotton blend with reinforced strap joins and raw-edge finish.",
    [("Fabric","Cotton-modal blend, 160 GSM"),("Cut","Deep armhole, open back"),("Straps","Reinforced join, bar-tacked"),("Edge","Raw-cut or coverstitched")], "fit-stringer"),
 ]},
{
 "slug": "gym-wrist-straps", "name": "GYM Wrist Straps", "tag": "Lifting Support", "hero": "strap-hero",
 "blurb": "Lifting straps, wrist wraps and figure-8s in cotton, neoprene and full-grain leather, branded your way.",
 "long": "Support gear takes more abuse per gram than anything else in a gym bag. We build straps from heavyweight cotton webbing and full-grain leather, bar-tack every load point, and back the wrist plate with neoprene so the strap bites the bar instead of the skin. Woven labels, printed webbing and custom colourways all run from low minimums.",
 "products": [
  P("Heavy Cotton Lifting Straps", ["24 Inch", "Neoprene Pad"], "Bar-tacked // Sold in pairs", ["ONE SIZE"], 50,
    "24-inch cotton webbing straps with a neoprene wrist pad and bar-tacked load loop.",
    [("Webbing","Heavyweight cotton, 3.8 cm"),("Length","24 inch (18 inch on request)"),("Pad","5 mm neoprene, stitched"),("Load point","Double bar-tack")], "strap-cotton"),
  P("Figure-8 Deadlift Straps", ["Closed Loop", "Flat Stitch"], "Max pulls // Custom colour", ["S","M","L"], 50,
    "Closed-loop figure-8 straps for maximal pulls, stitched flat so nothing digs in under load.",
    [("Build","Closed-loop figure 8"),("Webbing","Heavy cotton or nylon"),("Stitch","Flat lock, no raised seam"),("Sizes","S / M / L by wrist girth")], "strap-fig8"),
  P("Stiff Wrist Wraps", ["18/24 Inch", "Thumb Loop"], "Stiff weave // Printed logo", ["18IN","24IN"], 50,
    "Stiff-weave elastic wraps with a thumb loop and wide hook-and-loop closure for pressing.",
    [("Weave","Stiff elastic, 8 cm wide"),("Length","18 or 24 inch"),("Closure","Wide hook-and-loop"),("Branding","Printed webbing or woven label")], "strap-wraps"),
  P("Leather Lasso Straps", ["Full Grain", "Riveted"], "Breaks in // Embossed logo", ["ONE SIZE"], 30,
    "Full-grain leather lasso straps that break in to the wrist and grip without slipping.",
    [("Leather","Full-grain, 2.5 mm"),("Build","Lasso loop, riveted"),("Finish","Oiled or natural"),("Branding","Debossed or hot-foil logo")], "strap-leather"),
  P("Padded Wrist Support Wrap", ["Contoured Pad", "Low Profile"], "Daily training // Breathable", ["ONE SIZE"], 50,
    "Lighter daily-training wrap with contoured padding and a low-profile closure that sits under gloves.",
    [("Padding","Contoured EVA insert"),("Shell","Breathable knit"),("Closure","Low-profile hook-and-loop"),("Use","Daily training, high volume")], "strap-padded"),
 ]},
]

GALLERY = ["ma-hero","mma-shorts","fit-leggings","fac-mill-v2","strap-cotton","dummy-throw",
           "ma-belt","mma-rashguard","fit-tee","fac-thread","strap-fig8","dummy-gp"]

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def img(rel, key, alt, cls="", extra=""):
    return f'<img src="{rel}assets/img/photos/{key}.jpg" alt="{alt}" loading="lazy" decoding="async" class="{cls}" {extra}>'

NAV = [("Home","index.html"),("Collections","collections.html"),("Process","process.html"),
       ("About","about.html"),("Contact","contact.html")]

def head(title, desc, rel):
    style_v = ver("assets/css/style.css")
    fonts_v = ver("assets/css/fonts.css")
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{rel}assets/img/logo-green.svg" type="image/svg+xml">
<link rel="preload" as="font" type="font/woff2" href="{rel}assets/fonts/plus-jakarta-sans-800-latin.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="{rel}assets/fonts/inter-400-latin.woff2" crossorigin>
<link rel="stylesheet" href="{rel}assets/css/fonts.css{fonts_v}">
<link rel="stylesheet" href="{rel}assets/css/style.css{style_v}">
<script>(function(){{try{{var t=localStorage.getItem('ntf-theme');if(!t)t=matchMedia('(prefers-color-scheme:dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
</head>
<body>
<div class="progress"></div>
"""

def header(rel, current):
    links = "".join('<a href="%s%s"%s>%s</a>' % (rel, h, ' aria-current="page"' if h == current else '', n)
                    for n, h in NAV)
    return f"""<div class="announce"><div class="wrap">
<span><span class="dot"></span> Custom manufacturing from low minimums</span>
<a href="tel:{PHONE_TEL}">{PHONE}</a>
<a href="mailto:{EMAIL}">{EMAIL}</a>
</div></div>
<header class="site"><div class="wrap nav">
<a class="brand" href="{rel}index.html" aria-label="NTF Sportswear, home">
<img class="brand-mark" src="{rel}assets/img/logo-green.svg" alt="" width="36" height="36">
<span class="brand-type">NTF<span class="slash">//</span><span class="sub">Sportswear</span></span>
</a>
<nav class="menu">{links}
<a class="btn btn-primary btn-sm" href="{rel}quote.html">Request a Quote {I['arrow']}</a>
</nav>
<div class="nav-actions">
<button class="icon-btn" data-theme-toggle aria-label="Switch to dark mode">{I['moon']}{I['sun']}</button>
<a class="btn btn-primary btn-sm" href="{rel}quote.html" data-magnetic>Request a Quote {I['arrow']}</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i><i></i></button>
</div>
</div></header>
"""

def footer(rel):
    js_v = ver("assets/js/main.js")
    cats = "".join(f'<li><a href="{rel}collections/{c["slug"]}.html">{c["name"]}</a></li>' for c in CATEGORIES)
    return f"""<section><div class="wrap"><div class="cta reveal">
<p class="mono" style="color:inherit;opacity:.7">[ Next step ]</p>
<h2>Let&rsquo;s build your line</h2>
<p>Send artwork, a tech pack or a rough sketch. You get per-unit costing and a sampling plan back within one working day.</p>
<div class="btns">
<a class="btn btn-primary btn-lg" href="{rel}quote.html" data-magnetic>Request a Quote {I['arrow']}</a>
<a class="btn btn-ghost btn-lg" href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp us</a>
</div></div></div></section>

<footer class="site"><div class="wrap">
<div class="fgrid">
<div>
<a class="brand brand-stack" href="{rel}index.html" aria-label="NTF Sportswear, home">
<img class="brand-mark light-only" src="{rel}assets/img/logo-black.svg" alt="" width="56" height="56">
<img class="brand-mark dark-only" src="{rel}assets/img/logo-white.svg" alt="" width="56" height="56">
<span class="brand-type"><span class="row">NTF<span class="slash">//</span></span><span class="sub">Sportswear</span></span></a>
<p class="muted" style="margin-top:1.4rem;max-width:34ch;font-size:.9rem">Custom sportswear and combat gear manufactured in Sialkot, Pakistan for gyms, academies and apparel labels worldwide.</p>
</div>
<div><h4>Collections</h4><ul>{cats}</ul></div>
<div><h4>Company</h4><ul>
<li><a href="{rel}about.html">About NTF</a></li>
<li><a href="{rel}process.html">How we work</a></li>
<li><a href="{rel}collections.html">All collections</a></li>
<li><a href="{rel}quote.html">Request a quote</a></li>
</ul></div>
<div><h4>Contact</h4><ul>
<li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a></li>
<li class="muted">Sialkot, Punjab, Pakistan</li>
</ul></div>
</div>
<div class="legal">
<span>&copy; <span id="year">2026</span> NTF Sportswear. All rights reserved.</span>
<span class="status">[ Quote turnaround: <b>24h</b> ] [ Ships: <b>worldwide</b> ] [ MOQ from <b>5 pcs</b> ]</span>
</div>
</div></footer>

<div class="fab">
<button class="top" aria-label="Back to top">{I['up']}</button>
<a class="wa" href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp">{I['wa']}</a>
</div>
<script src="{rel}assets/js/main.js{js_v}"></script>
</body>
</html>
"""

def size_buttons(p, limit=None, name_prefix=""):
    """Size chips as real toggle buttons, so a buyer can mark the size run."""
    sizes = p["sizes"] if limit is None else p["sizes"][:limit]
    out = []
    for sz in sizes:
        disabled = ' disabled aria-disabled="true"' if sz in p["out"] else ''
        out.append(
            '<button type="button" class="size" data-size="%s" aria-pressed="false"%s>%s</button>'
            % (sz, disabled, sz))
    return "".join(out)

def qty_step(moq):
    """Increment the +/- buttons move by: whole cartons, not single pieces."""
    if moq <= 10:
        return moq
    return 10 if moq < 40 else 25

def qty_block(p, ident):
    """Quantity stepper, floored at the product's minimum order."""
    return f"""<div class="qty">
<b>Qty //</b>
<div class="qty-field">
<button type="button" class="qty-step" data-step="-1" aria-label="Decrease quantity">&minus;</button>
<input class="qty-input" id="qty-{ident}" type="number" inputmode="numeric" step="1"
 min="{p['moq']}" value="{p['moq']}" aria-label="Quantity of {p['name']} (minimum {p['moq']})">
<button type="button" class="qty-step" data-step="1" aria-label="Increase quantity">+</button>
</div>
<span class="qty-min">min {p['moq']}</span>
</div>"""

def pcard(c, p, rel):
    s = slugify(p["name"])
    ident = s + "-" + c["slug"]
    tags = "".join('<span%s>%s</span>' % (' class="brandtag"' if i == 0 else '', t)
                   for i, t in enumerate(p["tags"]))
    return f"""<article class="pcard reveal" data-picker
 data-product="{p['name']}" data-category="{c['slug']}" data-quote="{rel}quote.html" data-moq="{p['moq']}" data-step-size="{qty_step(p['moq'])}">
<a class="pcard-media" href="{rel}products/{s}.html" aria-label="{p['name']}">
<div class="tags">{tags}</div><div class="ticks"><i></i><i></i><i></i><i></i></div>
{img(rel, p['img'], p['name'] + ' - ' + c['name'] + ' by NTF')}
</a>
<div class="pcard-body">
<p class="kicker">{c['name']}</p>
<div class="pcard-head"><h3><a href="{rel}products/{s}.html">{p['name']}</a></h3><span class="moq">MOQ {p['moq']}</span></div>
<p class="pcard-sub">{p['sub']}</p>
<div class="pcard-divider"></div>
<div class="sizes" role="group" aria-label="Select sizes for {p['name']}"><b>Size //</b>{size_buttons(p, 7)}</div>
{qty_block(p, ident)}
<a class="pcard-cta" data-quote-cta href="{rel}quote.html?product={p['name'].replace(' ', '%20')}&amp;category={c['slug']}">Request a quote {I['arrow']}</a>
</div></article>"""

def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    open(full, "w", encoding="utf-8").write(html)

# ----------------------------------------------------------------- pages ---
def build_home():
    rel = ""
    tiles = ""
    for i, c in enumerate(CATEGORIES):
        wide = ' tile-wide' if i in (0, 3) else (' tile-full' if i == 4 else '')
        tiles += f"""<a class="tile reveal{wide}" href="collections/{c['slug']}.html">
{img(rel, c['hero'], c['name'] + ' manufacturing by NTF')}
<div class="tile-body"><p class="kicker">{c['tag']} &middot; 5 products</p><h3>{c['name']}</h3>
<p>{c['blurb']}</p><span class="arrow-link">View collection <span>{I['arrow']}</span></span></div></a>"""

    catalog = ""
    for c in CATEGORIES:
        catalog += pcard(c, c["products"][0], rel)
    for c in CATEGORIES[:1]:
        catalog += pcard(c, c["products"][4], rel)

    filters = "".join(f'<a href="collections/{c["slug"]}.html">{c["name"]}</a>' for c in CATEGORIES)
    gal = "".join(f'<figure>{img(rel, k, "NTF manufacturing and sport")}</figure>' for k in GALLERY * 2)
    strip = "".join('<span>%s</span>' % t for t in
                    ["Martial Arts","MMA Wear","Grappling Dummies","Fitness Wear","Wrist Straps",
                     "Private Label","Low Minimums","Worldwide Shipping"] * 2)

    return (head("NTF Sportswear | Custom Martial Arts, MMA &amp; Fitness Apparel Manufacturer",
        "NTF manufactures custom martial arts uniforms, MMA fight wear, grappling dummies, gym apparel and lifting straps. Low minimums, your branding, shipped worldwide.", rel)
    + header(rel, "index.html")
    + f"""<section class="hero"><div class="wrap hero-grid">
<div>
<p class="badge fade-up">Custom Sportswear // Sialkot, PK</p>
<h1 class="fade-up d1">Your brand,<br>built seam<br><span class="accent">by seam
<svg viewBox="0 0 300 12" preserveAspectRatio="none" aria-hidden="true"><path d="M3 8C60 3 150 2 297 6"/></svg></span></h1>
<p class="lead fade-up d2" style="max-width:52ch">NTF manufactures custom martial arts uniforms, MMA fight wear, grappling dummies, gym apparel and lifting support. Cut, stitched and branded to your spec. Low minimums, real samples, shipped worldwide.</p>
<div class="hero-specs fade-up d3">
<span><b>5 PCS</b> minimum order</span>
<span><b>24 H</b> quote turnaround</span>
<span><b>7-10 D</b> sampling</span>
</div>
<div class="hero-cta fade-up d4">
<a class="btn btn-primary btn-lg" href="quote.html" data-magnetic>Request a quote {I['arrow']}</a>
<a class="btn btn-ghost btn-lg" href="collections.html">Browse collections</a>
</div>
<div class="hero-meta fade-up d5">
<div><b><span data-count="25">0</span></b><span>Catalogue products</span></div>
<div><b><span data-count="40" data-suffix="+">0</span></b><span>Countries shipped</span></div>
<div><b><span data-count="5" data-suffix=" pcs">0</span></b><span>Lowest MOQ</span></div>
</div>
</div>
<div class="hero-art">
<figure class="reveal-img"><span class="annot annot-tl">Fabric<b>550 GSM</b></span>{img(rel, 'ma-bjj-gi', 'Athletes training in NTF custom gis')}</figure>
<figure class="reveal-img">{img(rel, 'fit-leggings', 'Custom fitness wear manufactured by NTF')}</figure>
<figure class="reveal-img"><span class="annot annot-br">Stitch<b>Lock + bar-tack</b></span>{img(rel, 'fac-mill-v2', 'NTF production floor in Sialkot')}</figure>
<div class="float-card">
<span class="dotg">{I['shield']}</span>
<span><b>Sample before bulk</b><span>Nothing ships until you sign it off</span></span>
</div>
</div>
</div></section>

<div class="strip"><div class="strip-track">{strip}</div></div>

<section><div class="wrap">
<div class="sec-head">
<div><div class="sec-index"><span class="idx">[ 01 ]</span><h2>The collections</h2></div>
<p>Five ranges covering the mat, the cage and the gym floor. Every product is a starting point: colours, fabric weight, cut and branding are yours to change.</p></div>
<a class="arrow-link" href="collections.html">All collections <span>{I['arrow']}</span></a>
</div>
<div class="grid g3">{tiles}</div>
</div></section>

<section class="section-alt"><div class="wrap">
<div class="sec-head">
<div><div class="sec-index"><span class="idx">[ 02 ]</span><h2>The catalog</h2></div>
<p>A cross-section of what leaves the floor. Twenty-five products across five ranges, each re-speccable in your fabric, colourway and branding.</p></div>
<span class="sec-note">Sort: featured</span>
</div>
<div class="filters"><a class="active" href="collections.html">All products</a>{filters}</div>
<div class="grid g3">{catalog}</div>
</div></section>

<section><div class="wrap">
<div class="sec-index"><span class="idx">[ 03 ]</span><h2>Build specification &amp; capability matrix</h2></div>
<p class="lead" style="max-width:62ch;margin-bottom:2.2rem">Every NTF product is built to a written spec: fabric weight, seam type, decoration method and tolerance. These are the numbers we work to.</p>
<div class="matrix reveal">
<div class="matrix-cell"><div class="ic">{I['tag']}</div><p class="lbl">Lowest minimum</p><p class="val"><span data-count="5">0</span> pcs</p><p class="sub">Per design on grappling dummies</p></div>
<div class="matrix-cell"><div class="ic">{I['gauge']}</div><p class="lbl">Quote turnaround</p><p class="val"><span data-count="24">0</span> h</p><p class="sub">Costing, fabric options, lead time</p></div>
<div class="matrix-cell"><div class="ic">{I['layers']}</div><p class="lbl">Fabric range</p><p class="val"><span data-count="140">0</span>-750</p><p class="sub">GSM, from mesh to double weave</p></div>
<div class="matrix-cell"><div class="ic">{I['globe']}</div><p class="lbl">Countries shipped</p><p class="val"><span data-count="40">0</span>+</p><p class="sub">Air or sea, DDU or DDP</p></div>
</div>
<div class="meters">
<div class="meter reveal" data-meter="92"><div class="meter-top"><span class="lbl">In-house production steps</span><span class="val">92%</span></div>
<div class="meter-track"><span class="meter-fill"></span></div><p class="meter-note">Cut, stitch, sublimation, embroidery, finishing</p></div>
<div class="meter reveal" data-meter="100"><div class="meter-top"><span class="lbl">Pieces inspected before packing</span><span class="val">100%</span></div>
<div class="meter-track"><span class="meter-fill"></span></div><p class="meter-note">Measurement, stitch and print check on every unit</p></div>
</div>
</div></section>

<section class="section-alt"><div class="wrap split">
<div class="reveal">
<div class="sec-index"><span class="idx">[ 04 ]</span><h2>A factory,<br>not a middleman</h2></div>
<p class="lead">You talk to the people who cut the fabric. That means honest lead times, fabric specs you can verify, and changes that actually get made instead of getting lost between three agents and a trading house.</p>
<a class="btn btn-dark" href="about.html" data-magnetic>More about NTF {I['arrow']}</a>
</div>
<div class="media-stack">
<div class="media-frame reveal-img">{img(rel, 'fac-floor-v2', 'NTF stitching line')}</div>
<div class="media-frame reveal-img">{img(rel, 'fac-thread', 'Thread store at the NTF factory')}</div>
<div class="media-frame reveal-img">{img(rel, 'fac-machine', 'Knitting machine detail')}</div>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><div><div class="sec-index"><span class="idx">[ 05 ]</span><h2>Brief to bulk</h2></div>
<p>Most clients go from first message to approved sample inside two weeks, and to delivered cartons in four to six.</p></div>
<a class="arrow-link" href="process.html">Full process <span>{I['arrow']}</span></a></div>
<div class="split">
<ul class="steps reveal">
<li><span class="num">01</span><div><b>Share the brief</b><p>Artwork, tech pack, a competitor sample or a sketch on a napkin. All of it works.</p></div></li>
<li><span class="num">02</span><div><b>Costing in 24 hours</b><p>Per-unit pricing at two or three quantity breaks, fabric options and a realistic lead time.</p></div></li>
<li><span class="num">03</span><div><b>Sample and sign-off</b><p>We make it, ship it with tracking, adjust it. Bulk starts only once you approve.</p></div></li>
<li><span class="num">04</span><div><b>Bulk and delivery</b><p>Production, QC on every piece, packed your way, door to door by air or sea.</p></div></li>
</ul>
<div class="media-frame reveal-img" style="aspect-ratio:3/4">{img(rel, 'fac-fabric', 'Rolled fabric ready for cutting')}</div>
</div>
</div></section>

<div class="gallery section-alt"><div class="gallery-track">{gal}</div></div>

<section><div class="wrap">
<div class="sec-index"><span class="idx">[ 06 ]</span><h2>Straight answers</h2></div>
<div style="max-width:820px;margin-top:2rem">
<details open><summary>What is the minimum order?</summary><div class="answer">It depends on the product. Grappling dummies start at 5 pieces, martial arts uniforms at 10 to 12, apparel at 20 to 40, and straps at 30 to 50 per design. Mixed sizes within one design count toward the same minimum.</div></details>
<details><summary>Can you work from my tech pack?</summary><div class="answer">Yes. Send a tech pack, a physical sample or reference photos. We build the pattern from it and flag anything that will not behave in production before we cut.</div></details>
<details><summary>How long does sampling take?</summary><div class="answer">Seven to ten working days for most apparel, slightly longer for dummies and leather goods. Courier time is on top, and we share the tracking number as soon as it ships.</div></details>
<details><summary>Do you handle branding and packaging?</summary><div class="answer">Woven labels, hang tags, heat transfers, embroidery, poly bags and printed cartons. Tell us how you want it to arrive and it arrives that way.</div></details>
<details><summary>Where do you ship?</summary><div class="answer">Worldwide by air or sea, DDU or DDP, through DHL, FedEx or your own forwarder. Most clients are in the UK, US, Europe, Australia and the Gulf.</div></details>
</div>
</div></section>
""" + footer(rel))

def build_collections():
    rel = ""
    tiles = ""
    for i, c in enumerate(CATEGORIES):
        wide = ' tile-wide' if i in (0, 3) else (' tile-full' if i == 4 else '')
        tiles += f"""<a class="tile reveal{wide}" href="collections/{c['slug']}.html">
{img(rel, c['hero'], c['name'] + ' by NTF')}
<div class="tile-body"><p class="kicker">{c['tag']} &middot; 5 products</p><h3>{c['name']}</h3>
<p>{c['blurb']}</p><span class="arrow-link">View collection <span>{I['arrow']}</span></span></div></a>"""
    return (head("Collections | NTF Custom Sportswear",
        "Browse NTF collections: martial arts uniforms, MMA wear, grappling dummies, fitness wear and gym wrist straps.", rel)
    + header(rel, "collections.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Collections</p>
<div class="sec-index"><span class="idx">[ 01 ]</span><h1 style="font-size:clamp(2.2rem,5vw,3.4rem)">Collections</h1></div>
<p>Five ranges covering the mat, the cage and the gym floor. Twenty-five catalogue products, every one of them re-speccable in your fabric, colourway and branding.</p>
</div></section>
<section><div class="wrap"><div class="grid g3">{tiles}</div></div></section>
""" + footer(rel))

def build_category(c):
    rel = "../"
    cards = "".join(pcard(c, p, rel) for p in c["products"])
    others = "".join(f'<a href="{o["slug"]}.html">{o["name"]}</a>' for o in CATEGORIES if o["slug"] != c["slug"])
    return (head(f"{c['name']} | NTF Custom Sportswear", c["blurb"], rel)
    + header(rel, "collections.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="{rel}index.html">Home</a> / <a href="{rel}collections.html">Collections</a> / {c['name']}</p>
<p class="badge">{c['tag']} // 5 products</p>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);margin-top:1rem">{c['name']}</h1>
<p>{c['long']}</p>
<div class="hero-cta"><a class="btn btn-primary" href="{rel}quote.html?category={c['slug']}" data-magnetic>Request a quote {I['arrow']}</a>
<a class="btn btn-ghost" href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">WhatsApp</a></div>
</div></section>
<section><div class="wrap">
<div class="sec-head"><div><div class="sec-index"><span class="idx">[ 02 ]</span><h2>{c['name']} range</h2></div>
<p>Minimums are per design and drop with volume. Sizes shown are the standard run; custom grading is available.</p></div>
<span class="sec-note">5 products</span></div>
<div class="grid g3">{cards}</div>
</div></section>
<section class="section-alt"><div class="wrap">
<div class="sec-index"><span class="idx">[ 03 ]</span><h2>Other collections</h2></div>
<div class="filters" style="margin-top:1.6rem">{others}</div>
</div></section>
""" + footer(rel))

def build_product(c, p):
    rel = "../"
    s = slugify(p["name"])
    others = [q for q in c["products"] if q["name"] != p["name"]]
    thumbs = [p] + others[:3]
    thumb_html = "".join(
        f'<button data-pdp-thumb="{rel}assets/img/photos/{t["img"]}.jpg" data-alt="{t["name"]}" aria-selected="{"true" if i == 0 else "false"}">'
        f'{img(rel, t["img"], t["name"])}</button>' for i, t in enumerate(thumbs))
    rows = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in p["specs"])
    sizes = " &middot; ".join(p["sizes"])
    related = "".join(pcard(c, q, rel) for q in others[:3])
    tags = "".join(f'<span>{t}</span>' for t in p["tags"])
    return (head(f"{p['name']} | {c['name']} | NTF Custom Sportswear", p["desc"], rel)
    + header(rel, "collections.html")
    + f"""<section class="pagehead" style="background:var(--bg);border:0;padding-bottom:0">
<div class="wrap"><p class="crumbs"><a href="{rel}index.html">Home</a> / <a href="{rel}collections.html">Collections</a> / <a href="{rel}collections/{c['slug']}.html">{c['name']}</a> / {p['name']}</p></div>
</section>
<section style="padding-top:1.5rem"><div class="wrap pdp">
<div>
<div class="pdp-main"><img data-pdp-main src="{rel}assets/img/photos/{p['img']}.jpg" alt="{p['name']} manufactured by NTF" decoding="async"></div>
<div class="pdp-thumbs">{thumb_html}</div>
</div>
<div>
<p class="kicker">{c['name']}</p>
<h1 style="font-size:clamp(2rem,4vw,2.9rem);margin:.4rem 0 .8rem">{p['name']}</h1>
<div class="tags tags-static">{tags}</div>
<p class="lead">{p['desc']}</p>

<div class="picker" data-picker data-product="{p['name']}" data-category="{c['slug']}"
 data-quote="{rel}quote.html" data-moq="{p['moq']}" data-step-size="{qty_step(p['moq'])}">
<div class="picker-row">
<span class="picker-label">Sizes</span>
<div class="sizes sizes-lg" role="group" aria-label="Select sizes for {p['name']}">{size_buttons(p)}</div>
</div>
<div class="picker-row">
<span class="picker-label">Quantity</span>
{qty_block(p, s)}
</div>
<p class="picker-summary" data-picker-summary aria-live="polite">Pick your sizes and quantity, and they travel with your quote request.</p>
<div class="hero-cta" style="margin-top:1.2rem">
<a class="btn btn-primary btn-lg" data-quote-cta data-magnetic href="{rel}quote.html?product={p['name'].replace(' ', '%20')}&amp;category={c['slug']}">Request a quote {I['arrow']}</a>
<a class="btn btn-ghost btn-lg" href="tel:{PHONE_TEL}">Call {PHONE}</a>
</div>
</div>

<table class="spec-table"><tbody>{rows}
<tr><th>Standard sizes</th><td>{sizes}</td></tr>
<tr><th>Minimum order</th><td>{p['moq']} pieces per design</td></tr>
<tr><th>Sampling</th><td>7-10 working days, revised until sign-off</td></tr>
<tr><th>Bulk lead time</th><td>3-4 weeks after sample approval</td></tr>
</tbody></table>
</div>
</div></section>
<section class="section-alt"><div class="wrap">
<div class="sec-head"><div><div class="sec-index"><span class="idx">[ + ]</span><h2>More from {c['name']}</h2></div></div>
<a class="arrow-link" href="{rel}collections/{c['slug']}.html">View all 5 <span>{I['arrow']}</span></a></div>
<div class="grid g3">{related}</div>
</div></section>
""" + footer(rel))

def build_quote():
    rel = ""
    opts = "".join(f'<option value="{c["slug"]}">{c["name"]}</option>' for c in CATEGORIES)
    chips = "".join(f'<label class="chip"><input type="checkbox" name="services" value="{s}"><span>{s}</span></label>'
                    for s in ["Custom manufacturing","Private label","Sampling only","Bulk reorder","Design help"])
    return (head("Request a Quote | NTF Custom Sportswear",
        "Tell NTF what you want made and get per-unit costing, fabric options and a lead time back within one working day.", rel)
    + header(rel, "quote.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Request a quote</p>
<p class="badge">Costing in 24 hours</p>
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);margin-top:1rem">Request a quote</h1>
<p>Fill this in and we come back with per-unit pricing, fabric options, sampling cost and a realistic lead time. No account, no subscription, no sales sequence.</p>
</div></section>
<section><div class="wrap split" style="align-items:start">
<form class="formcard" id="quote-form" novalidate>
<div class="ok"><b>Thanks, your quote request is ready to send.</b><p class="muted" style="margin:.4rem 0 0;font-size:.9rem">Your email app should open with the details filled in. If it does not, email <a href="mailto:{EMAIL}">{EMAIL}</a> directly.</p></div>
<div class="two">
<div class="field"><label for="name">Your name *</label><input id="name" name="name" required autocomplete="name"><span class="err" id="err-name"></span></div>
<div class="field"><label for="company">Company / gym</label><input id="company" name="company" autocomplete="organization"></div>
</div>
<div class="two">
<div class="field"><label for="email">Email *</label><input id="email" name="email" type="email" required autocomplete="email"><span class="err" id="err-email"></span></div>
<div class="field"><label for="phone">Phone / WhatsApp</label><input id="phone" name="phone" type="tel" autocomplete="tel"></div>
</div>
<div class="two">
<div class="field"><label for="category">Category *</label><select id="category" name="category" required>
<option value="">Select a category</option>{opts}<option value="other">Something else</option></select><span class="err" id="err-category"></span></div>
<div class="field"><label for="quantity">Quantity *</label><input id="quantity" name="quantity" type="number" min="1" placeholder="e.g. 100" required><span class="err" id="err-quantity"></span></div>
</div>
<div class="field"><label>What do you need?</label><div class="chips">{chips}</div></div>
<div class="field"><label for="details">Project details *</label>
<textarea id="details" name="details" required placeholder="Products, fabric, colours, sizes, branding, deadline, delivery country..."></textarea><span class="err" id="err-details"></span></div>
<button class="btn btn-primary btn-lg" type="submit" style="width:100%">Send quote request {I['arrow']}</button>
<p class="muted" style="font-size:.8rem;margin:.9rem 0 0">We reply from {EMAIL}. Your details are used for this quote only.</p>
</form>
<div>
<div class="grid" style="gap:.8rem">
<div class="info reveal"><div class="ic">{I['phone']}</div><div><b>Call or WhatsApp</b><a href="tel:{PHONE_TEL}">{PHONE}</a></div></div>
<div class="info reveal"><div class="ic">{I['mail']}</div><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="info reveal"><div class="ic">{I['clock']}</div><div><b>Response time</b><span>Within one working day, Monday to Saturday</span></div></div>
<div class="info reveal"><div class="ic">{I['box']}</div><div><b>Minimums</b><span>From 5 pieces per design on dummies, 10 to 50 on apparel and straps</span></div></div>
</div>
<div class="formcard" style="margin-top:1.2rem">
<div class="sec-index"><span class="idx">[ ! ]</span><h3>What to send us</h3></div>
<ul class="steps" style="margin-top:1rem">
<li><span class="num">01</span><div><b>Artwork</b><p>AI, EPS, PDF or high-resolution PNG. A phone photo of a sketch is enough to start.</p></div></li>
<li><span class="num">02</span><div><b>Size breakdown</b><p>How many of each size, or tell us your market and we will suggest a curve.</p></div></li>
<li><span class="num">03</span><div><b>Deadline</b><p>Event date or shelf date, so we can work the schedule backwards.</p></div></li>
</ul>
</div>
</div>
</div></section>
""" + footer(rel))

def build_about():
    rel = ""
    feats = [(I['scissors'],"Own your product","Your labels, your packaging, your spec sheet. We do not resell your design to the next buyer."),
             (I['layers'],"Verifiable specs","GSM, composition and thread type in writing, so you can check what arrived against what you ordered."),
             (I['shield'],"QC on every piece","Measurement, stitch and print checks before packing, not a spot check of one carton."),
             (I['globe'],"Grow with volume","Start at a handful of pieces to test the market, scale into container loads on the same patterns.")]
    f = "".join(f'<div class="feature reveal"><div class="ic">{i}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in feats)
    return (head("About | NTF Custom Sportswear",
        "NTF is a Sialkot-based manufacturer of custom martial arts, MMA and fitness apparel and training gear.", rel)
    + header(rel, "about.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / About</p>
<div class="sec-index"><span class="idx">[ 01 ]</span><h1 style="font-size:clamp(2.2rem,5vw,3.4rem)">A factory, not a middleman</h1></div>
<p>NTF is a custom sportswear manufacturer based in Sialkot, Pakistan, the city that has been making the world&rsquo;s combat sports gear for a century. We make for gyms, academies, fight teams and apparel labels who want their own product rather than a logo on someone else&rsquo;s catalogue.</p>
</div></section>
<section><div class="wrap split">
<div class="media-frame reveal-img" style="aspect-ratio:4/5">{img(rel, 'fac-mill-v2', 'NTF production floor')}</div>
<div class="reveal">
<div class="sec-index"><span class="idx">[ 02 ]</span><h2>What we actually do</h2></div>
<p class="lead">We take a brief, a tech pack, a competitor sample or sometimes just a conversation, and turn it into a pattern, a sample and then a production run.</p>
<p>Cutting, stitching, sublimation, embroidery and finishing all happen in-house, so when you ask for a change it reaches the person holding the scissors. Our ranges cover martial arts uniforms and belts, MMA fight wear, grappling dummies, gym apparel and lifting support.</p>
<a class="btn btn-dark" href="collections.html" data-magnetic>See the collections {I['arrow']}</a>
</div>
</div></section>
<section class="section-alt"><div class="wrap">
<div class="sec-index"><span class="idx">[ 03 ]</span><h2>How we judge our own work</h2></div>
<p class="lead" style="max-width:60ch;margin-bottom:2rem">Three things decide whether a piece leaves the floor: does it measure to spec, does the seam survive load, and does the decoration survive washing. Everything else is opinion.</p>
<div class="grid g4">{f}</div>
</div></section>
<section><div class="wrap">
<div class="sec-index"><span class="idx">[ 04 ]</span><h2>Inside the floor</h2></div>
<div class="grid g3" style="margin-top:2rem">
<div class="media-frame reveal-img">{img(rel, 'fac-floor-v2', 'Stitching line')}</div>
<div class="media-frame reveal-img">{img(rel, 'fac-spools', 'Thread spools')}</div>
<div class="media-frame reveal-img">{img(rel, 'fac-machine', 'Machine detail')}</div>
</div>
</div></section>
""" + footer(rel))

def build_process():
    rel = ""
    steps = [("01","Brief and costing","Send artwork, a tech pack or a reference product. Within one working day you get per-unit pricing at two or three quantity breaks, fabric options and a lead time."),
             ("02","Pattern and mock-up","We build the pattern and send a digital mock-up with your artwork placed, so placement and proportion are agreed before anything is cut."),
             ("03","Physical sample","A pre-production sample ships in 7 to 10 working days with tracking. Wear it, wash it, pull on it, then tell us what to change."),
             ("04","Revision and sign-off","Fit or spec changes are applied and re-sampled where needed. Bulk starts only once you approve in writing."),
             ("05","Production and QC","Three to four weeks for most bulk runs. Every piece is measured and inspected, and we share line photos mid-run."),
             ("06","Packing and freight","Poly-bagged, tagged and boxed your way, then shipped door to door by air or sea, our forwarder or yours.")]
    ls = "".join(f'<li><span class="num">{n}</span><div><b>{t}</b><p>{d}</p></div></li>' for n, t, d in steps)
    return (head("How We Work | NTF Custom Sportswear",
        "From brief to bulk: how NTF quotes, samples, produces and ships custom sportswear orders.", rel)
    + header(rel, "process.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Process</p>
<div class="sec-index"><span class="idx">[ 01 ]</span><h1 style="font-size:clamp(2.2rem,5vw,3.4rem)">Brief to bulk</h1></div>
<p>No portals and no onboarding calls. A short, honest sequence that most clients complete in four to six weeks from first message to delivered cartons.</p>
</div></section>
<section><div class="wrap split">
<ul class="steps reveal">{ls}</ul>
<div>
<div class="media-frame reveal-img" style="aspect-ratio:3/4">{img(rel, 'fac-fabric', 'Fabric rolls ready for cutting')}</div>
<div class="matrix reveal" style="grid-template-columns:1fr 1fr;margin-top:1rem">
<div class="matrix-cell"><p class="lbl">Sampling</p><p class="val"><span data-count="7">0</span>-10 d</p><p class="sub">Most apparel</p></div>
<div class="matrix-cell"><p class="lbl">Bulk</p><p class="val"><span data-count="3">0</span>-4 wk</p><p class="sub">After sign-off</p></div>
</div>
</div>
</div></section>
<section class="section-alt"><div class="wrap">
<div class="sec-index"><span class="idx">[ 02 ]</span><h2>Details that save you weeks</h2></div>
<div style="max-width:820px;margin-top:2rem">
<details open><summary>Sampling charges</summary><div class="answer">Samples are charged at cost plus courier, and credited against your first bulk invoice.</div></details>
<details><summary>Payment terms</summary><div class="answer">Typically 50% to start production and 50% against shipping documents, by bank transfer or Wise.</div></details>
<details><summary>Repeat orders</summary><div class="answer">Patterns and artwork stay on file, so a reorder skips straight to production with no sampling delay.</div></details>
<details><summary>Changes mid-run</summary><div class="answer">Colour or label changes are usually fine before cutting starts. After that they cost time, so we flag it honestly rather than quietly missing your date.</div></details>
</div>
</div></section>
""" + footer(rel))

def build_contact():
    rel = ""
    return (head("Contact | NTF Custom Sportswear",
        f"Contact NTF Sportswear. Call {PHONE} or email {EMAIL} for custom sportswear manufacturing.", rel)
    + header(rel, "contact.html")
    + f"""<section class="pagehead"><div class="wrap">
<p class="crumbs"><a href="index.html">Home</a> / Contact</p>
<div class="sec-index"><span class="idx">[ 01 ]</span><h1 style="font-size:clamp(2.2rem,5vw,3.4rem)">Contact NTF</h1></div>
<p>Message us on WhatsApp for the fastest answer, or email if you have files to send. We read everything ourselves.</p>
</div></section>
<section><div class="wrap split" style="align-items:start">
<div class="grid" style="gap:.8rem">
<div class="info reveal"><div class="ic">{I['phone']}</div><div><b>Phone and WhatsApp</b><a href="tel:{PHONE_TEL}">{PHONE}</a><br><a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">Open WhatsApp chat</a></div></div>
<div class="info reveal"><div class="ic">{I['mail']}</div><div><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></div></div>
<div class="info reveal"><div class="ic">{I['pin']}</div><div><b>Where we are</b><span>Sialkot, Punjab, Pakistan</span></div></div>
<div class="info reveal"><div class="ic">{I['clock']}</div><div><b>Hours</b><span>Monday to Saturday, 9am to 7pm PKT (UTC+5)</span></div></div>
</div>
<div class="formcard reveal">
<div class="sec-index"><span class="idx">[ 02 ]</span><h2 style="font-size:1.7rem">Fastest route</h2></div>
<p class="lead" style="margin-top:1rem">The quote form captures quantity, category and branding in one go, which means our first reply can already carry pricing instead of questions.</p>
<a class="btn btn-primary btn-lg" href="quote.html" data-magnetic>Request a quote {I['arrow']}</a>
<div style="margin-top:2rem;padding-top:1.6rem;border-top:1px solid var(--line)">
<h3>Prefer to write?</h3>
<p class="muted" style="margin-top:.5rem">Email <a href="mailto:{EMAIL}" style="color:var(--brand-strong)">{EMAIL}</a> with your artwork and quantity and we will take it from there.</p>
</div>
</div>
</div></section>
""" + footer(rel))

def build_404():
    rel = ""
    return (head("Page not found | NTF Sportswear", "That page does not exist.", rel)
    + header(rel, "")
    + f"""<section class="hero"><div class="wrap center">
<p class="badge">Error // 404</p>
<h1 style="margin:1.2rem 0">Missed the takedown</h1>
<p class="lead" style="margin-inline:auto;max-width:46ch">That page is not here. Try the collections, or tell us what you were looking for.</p>
<div class="hero-cta" style="justify-content:center"><a class="btn btn-primary btn-lg" href="index.html">Back home {I['arrow']}</a><a class="btn btn-ghost btn-lg" href="collections.html">Collections</a></div>
</div></section>
""" + footer(rel))

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
            write(f"products/{slugify(p['name'])}.html", build_product(c, p))
    urls = ["index.html","collections.html","quote.html","about.html","process.html","contact.html"]
    urls += [f"collections/{c['slug']}.html" for c in CATEGORIES]
    urls += [f"products/{slugify(p['name'])}.html" for c in CATEGORIES for p in c["products"]]
    base = "https://danialhyatt7-collab.github.io/NTF/"
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(f"  <url><loc>{base}{u}</loc></url>" for u in urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {base}sitemap.xml\n")
    write(".nojekyll", "")
    print("built", len(urls), "pages")

if __name__ == "__main__":
    main()
