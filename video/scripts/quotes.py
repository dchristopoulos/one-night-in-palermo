"""Fill {{Qn}} placeholders in compositions/*.html with verbatim lines from palermo/games/fun9-4.json,
and check every element with data-event against the JSON (run again after any edit: python3 scripts/quotes.py)."""
import html, json, pathlib, re, sys
root = pathlib.Path(__file__).resolve().parent.parent
ev = json.loads((root.parent / 'palermo/games/fun9-4.json').read_text())

def cut(i, how):
    t = ev[i]['text']
    if how == 'full': return t
    if how == 'first-sentence': return t.split('. ')[0] + '.'
    if how == 'first-clause': return t.split(',')[0] + '…'
    if how == 'tail-from-never': return '…' + t[t.index('never'):]
    raise ValueError(how)

ok = True
for f in sorted((root / 'compositions').glob('s*.html')):
    s = f.read_text()
    def fill(m):
        i, how = int(m.group(1)), m.group(2)
        return m.group(0).replace(f'{{{{Q{i}}}}}', html.escape(cut(i, how), quote=False))
    s2 = re.sub(r'data-event="(\d+)" data-cut="([\w-]+)">\{\{Q\d+\}\}', fill, s)
    if s2 != s: f.write_text(s2)
    for m in re.finditer(r'data-event="(\d+)" data-cut="([\w-]+)">(.*?)</p>', s2):
        got, want = html.unescape(m.group(3)), cut(int(m.group(1)), m.group(2))
        # every cut must come from the event text: the part without the added '…' is a prefix (or, for a tail, a suffix)
        core = want.strip('…')
        t = ev[int(m.group(1))]['text']
        good = got == want and (t.startswith(core) or t.endswith(core))
        ok &= good
        print(('OK  ' if good else 'BAD ') + f.name, m.group(1), repr(got))
sys.exit(0 if ok else 1)
