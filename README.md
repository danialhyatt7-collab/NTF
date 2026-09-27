# NTF INTERNATIONAL — website

Multi-page static website for **NTF INTERNATIONAL**, a custom sportswear and combat-gear manufacturer.

**Live site:** https://danialhyatt7-collab.github.io/NTF/

## Design

Monochrome black-and-white system. **Black is the default theme**; a switcher in the header
swaps to white (the choice is remembered in `localStorage`, with no flash of the wrong theme).
`--brand` is the single accent (white on black, black on white) and `--on-brand` is whatever
sits legibly on it, so the palette inverts cleanly from one set of tokens.
Layout follows a technical catalog structure — numbered sections, monospace spec labels,
size chips, corner tick marks and a capability matrix with animated meters.

Type: Plus Jakarta Sans (display), Inter (body), JetBrains Mono (technical labels) — all
self-hosted in `assets/fonts/`, so the site has **no external requests** at runtime.

Micro-animations throughout: staggered hero entrance, clip-path image reveals, count-up stats,
animated meters, magnetic buttons, shine sweep on buttons, hover lift and image zoom on cards,
marquee strips, scroll progress bar, header elevation, animated burger, accordion chevrons,
back-to-top fade. All disabled under `prefers-reduced-motion`.

## Contents

- **37 pages:** home, collections index, 5 category pages, 25 product pages, quote, process, about, contact, 404
- **Collections:** Martial Arts · MMA Wear · MMA Grappling Dummy · Fitness Wear · GYM Wrist Straps (5 products each)
- **Request a Quote:** inline-validated form, pre-filled from any product page
  (`quote.html?product=…&category=…`), composes an email to info@ntfint.com
- **Contact:** +92 333 8686122 · info@ntfint.com · WhatsApp button on every page

## Logo

Vector logos derived from the supplied brand PDF, in `assets/img/`:

| File | Use |
|---|---|
| `logo-black.svg` | Primary mark: light backgrounds, favicon, print |
| `logo-white.svg` | Dark backgrounds (the default theme) |

## Photography

36 free stock photos from [Unsplash](https://unsplash.com/license) in `assets/img/photos/`,
chosen per category so each range reads as one set (gi and belt work for martial arts, cage and
sparring for MMA, mat wrestling for dummies, studio apparel for fitness, barbell work for
straps, plus factory and fabric imagery). Resized to 1200px and re-encoded (~5 MB total).

## Structure

```
index.html  collections.html  quote.html  about.html  process.html  contact.html  404.html
collections/   5 category pages
products/      25 product pages
assets/css/style.css   assets/css/fonts.css   assets/js/main.js
assets/fonts/  assets/img/  assets/img/photos/
tools/build.py         static site generator — all content lives here
```

## Editing

All copy, products, specs and image mappings live in `tools/build.py`. Edit the data and regenerate:

```bash
python3 tools/build.py
```

Preview locally:

```bash
python3 -m http.server 8000
```

No frameworks and no build dependencies — plain HTML, CSS and vanilla JS.
