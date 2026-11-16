(() => {
  const vis = el => { const r = el.getBoundingClientRect(), s = getComputedStyle(el); return r.width > 1 && r.height > 1 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity > 0.05; };
  const inView = r => r.bottom > 4 && r.top < innerHeight - 4 && r.right > 4 && r.left < innerWidth - 4;
  const cls = el => (typeof el.className === 'string' ? el.className : '').split(' ')[0].replace(/^_/, '').replace(/_[A-Za-z0-9-]+_\d+$/, '');
  const name = el => `${el.tagName.toLowerCase()}${cls(el) ? '.' + cls(el) : ''}"${(el.textContent || '').trim().slice(0, 18)}"`;
  const chain = (el, f) => { for (let p = el; p; p = p.parentElement) if (f(p)) return p; return null; };
  const out = { hscroll: document.documentElement.scrollWidth > innerWidth + 1, covered: [], clipped: [], small: [], tiny: [], offscreen: [] };
  const leaves = [...document.querySelectorAll('body *')].filter(el => vis(el) && (el.tagName === 'IMG' || [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim().length > 0)) && inView(el.getBoundingClientRect()));
  for (const el of leaves) {
    if (chain(el, p => p.tagName === 'DETAILS' && !p.open) && !chain(el, p => p.tagName === 'SUMMARY')) continue;   // folded away
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    // is the element really painted where it is? sample its centre and two inner points
    const pts = [[.5, .5], [.2, .5], [.8, .5]].map(([fx, fy]) => [r.left + r.width * fx, r.top + r.height * fy]).filter(([x, y]) => x > 0 && y > 0 && x < innerWidth && y < innerHeight);
    for (const [x, y] of pts) {
      const top = document.elementFromPoint(x, y);
      if (!top || top === el || el.contains(top) || top.contains(el)) continue;
      // expected: scrolled under a sticky header, or under an opened dialog / the end card, or outside its scroll box
      if (chain(top, p => getComputedStyle(p).position === 'sticky')) continue;
      if (chain(top, p => p.getAttribute('role') === 'dialog' || /end|scrim|overlay/i.test(cls(p)))) continue;
      const box = chain(el.parentElement, p => /auto|scroll|hidden/.test(getComputedStyle(p).overflowY));
      if (box) { const q = box.getBoundingClientRect(); if (y < q.top || y > q.bottom || x < q.left || x > q.right) continue; }
      if (top.tagName === 'IMG' && el.tagName === 'IMG' && top.parentElement === el.parentElement) continue;   // a pile of faces
      out.covered.push(`${name(el)} under ${name(top)}`); break;
    }
    if (el.tagName !== 'IMG') {
      if (el.scrollWidth > el.clientWidth + 2 && !/visible|auto|scroll/.test(s.overflowX)) out.clipped.push(name(el));
      if (parseFloat(s.fontSize) < 12) out.tiny.push(`${name(el)} ${s.fontSize}`);
    }
    if (r.right > innerWidth + 2 || r.left < -2) out.offscreen.push(name(el));
    // cut: sticks out sideways of a box that clips it and cannot be scrolled sideways
    const clip = chain(el.parentElement, p => getComputedStyle(p).overflowX !== 'visible');
    if (clip && !/auto|scroll/.test(getComputedStyle(clip).overflowX) || (clip && clip.scrollWidth <= clip.clientWidth + 1)) {
      const q = clip.getBoundingClientRect();
      if (r.right > q.right + 2 || r.left < q.left - 2) out.clipped.push('cut ' + name(el));
    }
  }
  // unreachable: below or right of the screen with no scroll box around it and a page that does not scroll
  const pageScrolls = document.documentElement.scrollHeight > innerHeight + 1;
  for (const el of document.querySelectorAll('body *')) {
    if (!vis(el) || !(el.tagName === 'IMG' || [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()))) continue;
    if (chain(el, p => p.tagName === 'DETAILS' && !p.open) && !chain(el, p => p.tagName === 'SUMMARY')) continue;
    const r = el.getBoundingClientRect();
    if (r.top < innerHeight - 4 && r.left < innerWidth - 4) continue;
    if (pageScrolls || chain(el.parentElement, p => /auto|scroll/.test(getComputedStyle(p).overflowY) && p.scrollHeight > p.clientHeight)) continue;
    out.offscreen.push('unreachable ' + name(el));
  }
  for (const el of document.querySelectorAll('button, a, summary, [role=button], input')) {
    if (!vis(el)) continue; const r = el.getBoundingClientRect(); if (!inView(r)) continue;
    if (r.height < 40 || r.width < 40) out.small.push(`${name(el)} ${Math.round(r.width)}x${Math.round(r.height)}`);
  }
  for (const k of ['covered', 'clipped', 'small', 'tiny', 'offscreen']) { out[k] = [...new Set(out[k])]; if (out[k].length > 8) out[k] = [...out[k].slice(0, 8), `+${out[k].length - 8} more`]; }
  return JSON.stringify(out);
})()
