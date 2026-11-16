window.__audit = async (sizes, urls) => {
  const code = await fetch('/games/lab/ui-audit.js?' + Date.now()).then(r => r.text());
  const res = [];
  for (const [w, h] of sizes) {
    const frames = urls.map(([label, u, tall]) => { const f = document.createElement('iframe'); f.style.cssText = `position:fixed;left:0;top:0;width:${w}px;height:${tall ? 5200 : h}px;border:0;opacity:0.01;pointer-events:none;z-index:-1`; f.src = '/ui/' + u; document.body.appendChild(f); return { f, label }; });
    await new Promise(r => setTimeout(r, 2600));
    for (const { f, label } of frames) {
      try { const o = JSON.parse(f.contentWindow.eval(code)); const bad = {}; for (const k of ['covered', 'clipped', 'small', 'tiny', 'offscreen']) if (o[k].length) bad[k] = o[k]; if (o.hscroll) bad.hscroll = true; if (Object.keys(bad).length) res.push({ at: `${label} @${w}x${h}`, ...bad }); }
      catch (e) { res.push({ at: `${label} @${w}x${h}`, error: String(e) }); }
      f.remove();
    }
  }
  return res.map(x => x.at + '\n' + Object.entries(x).filter(([k]) => k !== 'at').map(([k, v]) => '  ' + k + ': ' + (Array.isArray(v) ? v.filter(t => !/under path/.test(t)).slice(0, 5).join(' | ') : v)).filter(l => !/: $/.test(l)).join('\n')).filter(t => t.includes('\n  ')).join('\n') || `clean: ${sizes.length} sizes x ${urls.length} screens`;
};
window.__urls = g => { const G = `?file=games/${g}.json&at=`; return [['home', '', true], ['say', G + 60], ['whisper', G + 5], ['votes', G + 89], ['votes-guess', G + 89 + '&mode=guess'], ['lastwords', G + 91], ['death', G + 92], ['ghost', G + 95], ['long', G + 262], ['end', G + 269]]; };
