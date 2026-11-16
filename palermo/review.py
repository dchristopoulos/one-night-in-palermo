#!/usr/bin/env python3
"""Print a saved game as a readable transcript with secrets, notes and a few metrics.
    python3 review.py games/<file>.json [more files]      # full transcript
    python3 review.py --day 2 games/<file>.json           # only that day's talk (plus votes/deaths)
"""
import json
import re
import statistics
import sys

args = sys.argv[1:]
only_day = None
if "--day" in args:
    only_day = int(args[args.index("--day") + 1])
    del args[args.index("--day"):args.index("--day") + 2]

for path in args:
    e = json.load(open(path))
    roles = {p["name"]: p["role"] + (" (shown)" if p.get("shown") else "") for p in e[0]["players"]}
    says = [x for x in e if x["type"] == "say"]
    notes = [x for x in e if x["type"] == "memory"]
    passes = sum(x["type"] == "pass" for x in e)
    gaps, prev = [], None
    for x in e:
        if x["type"] in ("say", "gm", "votes", "death"):
            if prev is not None:
                gaps.append(x["t"] - prev)
            prev = x["t"]
    print(f"\n######## {path}: {len(e)} events, {e[-1]['t'] / 60:.1f} min, winner={e[-1].get('winner')}")
    print("  roles: " + ", ".join(f"{n}={r}" for n, r in roles.items()))
    if says:
        import re as _re
        names = list(roles)
        meta = _re.compile(r"\b(push|accus|jump|pile|defend|dodg|answer|question|why did you|why are you|before anyone|quick|fast|eager|cover|frame|bandwagon|aggressive|obsessed|desperate)\w*", _re.I)
        day = [x for x in says if x.get("why") not in ("confession", "introduces themselves", "last words", "before the game")]
        lat = []
        for i, x in enumerate(day):
            for n in names:
                if n != x["name"] and _re.search(rf"\b{n}\b", x["text"]):
                    j = next((k for k in range(i + 1, len(day)) if day[k]["name"] == n), None)
                    lat.append(j - i if j else 99)
        print(f"  lines={len(says)} passes={passes} notes={len(notes)} median gap={statistics.median(gaps):.1f}s "
              f"max gap={max(gaps):.1f}s words/line={statistics.mean(len(x['text'].split()) for x in says):.0f} "
              f"meta={100 * sum(bool(meta.search(x['text'])) for x in day) // max(1, len(day))}% "
              f"questions={100 * sum('?' in x['text'] for x in day) // max(1, len(day))}% "
              f"named->replies next turn={100 * sum(l == 1 for l in lat) // max(1, len(lat))}% within 3={100 * sum(l <= 3 for l in lat) // max(1, len(lat))}%")
    day = 0
    for x in e:
        t = x["type"]
        if t == "phase":
            m = re.search(r"Day (\d+)", x["text"])
            day = int(m.group(1)) if m else day
            print(f"  === {x['text']}")
        elif only_day and day != only_day and t in ("say", "thought", "memory", "pass"):
            continue
        elif t == "say":
            to = f" -> {x['reply_to']}" if x.get("reply_to") else ""
            print(f"  {x['name']}{to} ({x.get('why', '')}): {x['text']}")
        elif t == "thought":
            print(f"      ({x['name']} thinks: {x['text']})")
        elif t == "memory":
            print(f"      📌 {x['name']} [{'!' * x['level']}] {x['text']}")
        elif t == "pass":
            print(f"      ({x['name']} passes)")
        elif t == "votes":
            print("    VOTES" + (" (runoff)" if x.get("runoff") else "") + ": "
                  + ", ".join(f"{a}->{b}" + (f' "{w[:60]}"' if w else "") for a, b, w in x["votes"]))
        elif t == "death":
            print(f"    ☠ {x['name']} ({x['how']}) was the {x['role'] or 'role not shown'}")
        elif t == "whisper":
            print(f"    🤫 {x['name']} -> {x['to']}: {x['text']}")
        elif t == "night_action":
            print(f"    [secret] {x['name']} {x['action']} {x['target']} {x.get('result', '')}")
        elif t == "gm":
            print(f"    [{'host aside' if x.get('aside') else 'narrator'}] {x['text']}")
        elif t == "note":
            print(f"    [note] {x['name']} left: {x['text']}")
        elif t == "ghost":
            print(f"    [out, to the audience] {x['name']}: {x['text']}")
        elif t == "recap":
            print(f"    [recap] {x['text']}")
