// Captures one still of the local viewer for the end card (run: node scripts/screenshot.mjs).
import puppeteer from 'puppeteer-core';
import { readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
const base = join(homedir(), '.cache/hyperframes/chrome/chrome-headless-shell');
const ver = readdirSync(base).find(d => d.startsWith('mac_arm'));
const exe = join(base, ver, 'chrome-headless-shell-mac-arm64/chrome-headless-shell');
const browser = await puppeteer.launch({ executablePath: exe, headless: true });
const page = await browser.newPage();
await page.setViewport({ width: 390, height: 844, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
await page.goto('http://localhost:8766/ui/?file=games/fun9-4.json&at=57', { waitUntil: 'networkidle0' });
await page.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; })));
});
await new Promise(r => setTimeout(r, 800));
await page.screenshot({ path: 'assets/art/viewer.png' });
await browser.close();
console.log('ok');
