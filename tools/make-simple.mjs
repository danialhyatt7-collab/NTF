// Prints tools/simple-page.html to /home/user/NTF/docs/NTF-INTERNATIONAL-Quick-Guide.pdf.
// Served over http so the self-hosted webfonts and logo resolve.
import { chromium } from 'playwright';
const EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
const b = await chromium.launch({ executablePath: EXE });
const p = await b.newPage();
await p.goto('http://localhost:8099/tools/simple-page.html', { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({
  path: '/home/user/NTF/docs/NTF-INTERNATIONAL-Quick-Guide.pdf',
  format: 'A4', printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
});
await b.close();
