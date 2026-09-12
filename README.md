# NTF Sportswear — website

Multi-page static website for **NTF**, a custom sportswear and combat-gear manufacturer.

**Live site:** https://danialhyatt7-collab.github.io/NTF/

## Contents

- **Pages (37):** home, collections index, 5 category pages, 25 product pages, quote, process, about, contact, 404
- **Collections:** Martial Arts · MMA Wear · MMA Grappling Dummy · Fitness Wear · GYM Wrist Straps (5 products each)
- **Request a Quote:** validated form that pre-fills from any product page (`quote.html?product=…&category=…`) and opens a pre-composed email to support@ntf.com.pk
- **Contact:** +92 333 8686122 · support@ntf.com.pk · WhatsApp shortcut on every page

## Logo

Vector logos derived from the supplied brand PDF, in `assets/img/`:

| File | Use |
|---|---|
| `logo-green.svg` | Primary brand mark (`#00a650`) |
| `logo-black.svg` | Light backgrounds, print |
| `logo-white.svg` | Dark backgrounds (used in the footer) |

## Structure

```
index.html  collections.html  quote.html  about.html  process.html  contact.html  404.html
collections/   5 category pages
products/      25 product pages
assets/css/style.css   assets/js/main.js   assets/img/*.svg
tools/build.py         static site generator (all content lives here)
```

## Editing

All copy, products and categories live in `tools/build.py`. Change the data there and regenerate:

```bash
python3 tools/build.py
```

Preview locally:

```bash
python3 -m http.server 8000
```

No build tools, frameworks or dependencies — plain HTML, CSS and vanilla JS.
