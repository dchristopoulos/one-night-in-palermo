// Captures the two README screenshots of the local viewer at 1440x900 @2x (run: node scripts/readme-shots.mjs).
import puppeteer from 'puppeteer-core';
import { readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
const base = join(homedir(), '.cache/hyperframes/chrome/chrome-headless-shell');
const ver = readdirSync(base).find(d => d.startsWith('mac_arm'));
const exe = join(base, ver, 'chrome-headless-shell-mac-arm64/chrome-headless-shell');
const shots = [
  ['http://localhost:8766/ui/', '../palermo/docs/screenshot-home.jpg'],
  ['http://localhost:8766/ui/?file=games/fun9-4.json&at=57', '../palermo/docs/screenshot-table.jpg'],
];
const browser = await puppeteer.launch({ executablePath: exe, headless: true });
for (const [url, path] of shots) {
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 2 });
  await page.goto(url, { waitUntil: 'networkidle0' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
  });
  await new Promise(r => setTimeout(r, 800));
  await page.screenshot({ path, type: 'jpeg', quality: 88 });
  await page.close();
}
await browser.close();
console.log('ok');
