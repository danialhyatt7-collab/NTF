// Renders tools/og-card.html to assets/img/og-cover.jpg (1200x630).
// Run with a local server on :8099 serving the repo root:
//   python3 -m http.server 8099 & node tools/make-og.mjs
import { chromium } from 'playwright';
const exe = process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: exe });
const p = await b.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
await p.goto('http://localhost:8099/tools/og-card.html', { waitUntil: 'networkidle' });
await p.waitForTimeout(600);
await p.screenshot({ path: 'assets/img/og-cover.png' });
await b.close();
console.log('rendered assets/img/og-cover.png');
