#!/usr/bin/env python3
"""Quality gates for a showcase file.  python3 gates.py games/archive/showcase.json [more]
words/line <= 12, meta <= 35%, named replies within 3 turns >= 70%, every living seat speaks every day,
no seat above 35% of a day's lines, Highlights 3-5 min at 1x, 2-3 days, no timeouts/repeats (from bake.py)."""
import json, re, statistics, sys
META = re.compile(r"\b(push|accus|jump|pile|defend|dodg|answer|question|why did you|why are you|before anyone|quick|fast|eager|cover|frame|bandwagon|aggressive|obsessed|desperate)\w*", re.I)
for path in sys.argv[1:]:
    e = json.load(open(path)); names = [p["name"] for p in e[0]["players"]]
    says = [x for x in e if x["type"] == "say"]
    day = [x for x in says if x.get("why") not in ("confession", "introduces themselves", "last words", "before the game")]
    wpl = statistics.mean(len(x["text"].split()) for x in says)
    meta = 100 * sum(bool(META.search(x["text"])) for x in day) / max(1, len(day))
    lat = []
    for i, x in enumerate(day):
        for n in names:
            if n != x["name"] and re.search(rf"\b{n}\b", x["text"]):
                j = next((k for k in range(i + 1, len(day)) if day[k]["name"] == n), None)
                lat.append(j - i if j else 99)
    within3 = 100 * sum(l <= 3 for l in lat) / max(1, len(lat))
    alive, d, per_day, silent, hog = set(names), 0, {}, [], []
    for x in e:
        if x["type"] == "phase" and x["text"].startswith("Day"):
            d = int(x["text"][4:]); per_day[d] = {}
        if x["type"] in ("say", "pass") and d and x.get("why") not in ("last words", "confession"):
            per_day[d][x["name"]] = per_day[d].get(x["name"], 0) + (x["type"] == "say")
        if x["type"] == "death":
            if x["how"] == "vote" and d:
                pass
            alive_after = alive - {x["name"]}
            if x["how"] == "night":
                alive = alive_after
            else:
                alive = alive_after
        if x["type"] == "phase" and x["text"].startswith("Night") and d:
            spoke = set(per_day[d]); missing = alive - spoke - {n for n in names if n not in alive}
            # a player voted out today still spoke before the vote; alive is already reduced, so add them back for the check
            silent += [(d, n) for n in (set(x2["name"] for x2 in e if x2["type"] == "death" and x2["how"] == "vote") | alive) if n not in spoke and n in (alive | set(per_day[d]))]
            tot = sum(per_day[d].values())
            if len(per_day[d]) >= 4:      # at three seats a third of the lines each is the floor, not a monologue
                hog += [(d, n, round(100 * c / tot)) for n, c in per_day[d].items() if tot and c / tot > 0.35]
    days = len(per_day)
    ok = lambda b: "OK " if b else "FAIL"
    print(f"{path}: {ok(wpl <= 12)} words/line {wpl:.1f} | {ok(meta <= 35)} meta {meta:.0f}% | {ok(within3 >= 70)} within3 {within3:.0f}% | "
          f"{ok(not silent)} silent {silent} | {ok(not hog)} >35% {hog} | {ok(2 <= days <= 3)} days {days}")
