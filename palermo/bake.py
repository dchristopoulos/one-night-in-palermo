#!/usr/bin/env python3
"""Bake-off numbers per saved game: days, minutes, winner, claims, whispers, repeats, timeouts, Highlights minutes.
    python3 bake.py games/archive/bake-A-1.json games/archive/bake-A-2.json …
Highlights minutes replay the viewer's own pace/isHighlight rules at 1x (index.html)."""
import json
import re
import sys

CLAIM = re.compile(r"\bI(?:['’]m| am) (?:the )?(?:real |actual )?(?:officer|police(?:man)?|cop|detective)\b", re.I)   # = game.CLAIM


def pace(ev):
    n = len(ev.get("text") or "")
    t = ev["type"]
    if t in ("say", "whisper", "note", "ghost"):
        return max(2500, 1800 + 42 * n)
    if t == "thought":
        return max(2500, 1200 + 40 * n)
    if t in ("gm", "recap"):
        return max(2500, 2000 + 42 * n)
    if t == "votes":
        return 2500 + 1200 * len(ev["votes"])
    return {"death": 3000, "phase": 2200, "night_action": 1600, "pass": 1200, "memory": 400}.get(t, 0)


def highlight(ev, nxt, roles, names):
    t, text = ev["type"], ev.get("text") or ""
    if t in ("phase", "gm", "votes", "death", "end", "recap", "vindicated", "whisper", "note"):
        return True
    if t == "say":
        if re.search(r"last word|confession|before the game", ev.get("why", "")) or ev.get("why") == "introduces themselves":
            return True
        s = 0
        s += 3 * bool(re.search(r"\b(i'?m|i am|i was) the (officer|doctor|killer)\b|\bi checked\b|\bi protected\b", text, re.I))
        s += 2 * bool(re.search(r"\bkiller\b", text, re.I) and any(re.search(rf"\b{n}\b", text) for n in names))
        s += bool(re.search(r"\bi(?:'m| am) voting\b|\bi vote\b|\bvote (for )?[A-Z]", text))
        s += bool(ev.get("reply_to") and "?" in text)
        return s >= 2
    if t == "thought":
        if re.search(r"killer|accomplice", roles.get(ev["name"], "")) and re.search(r"officer|doctor|mayor|killer|claim|kill|tonight|double vote|partner|shown", text, re.I):
            return True
        return bool(nxt and nxt["type"] == "say" and nxt["name"] == ev["name"] and highlight(nxt, None, roles, names))
    return False


for path in sys.argv[1:]:
    e = json.load(open(path))
    cast = e[0]
    roles = {p["name"]: p["role"] for p in cast["players"]}
    names = list(roles)
    says = [x for x in e if x["type"] == "say"]
    days = sum(x.get("kind") == "day" for x in e if x["type"] == "phase") - 1
    hi = sum(pace(x) for i, x in enumerate(e) if highlight(x, e[i + 1] if i + 1 < len(e) else None, roles, names)) / 60000
    claims = [x for x in says if CLAIM.search(x["text"])]
    claimers = list(dict.fromkeys(x["name"] for x in claims))
    texts = [x["text"].lower() for x in says]
    repeats = sum(texts.count(t) > 1 for t in set(texts))
    whispers = sum(x["type"] == "whisper" for x in e)
    try:
        log = open(path.replace(".json", ".log")).read()
    except OSError:
        try:   # a --games batch shares one TAG.log: take the segment that ends with this game's "saved TAG-i.json" line
            name = path.rsplit("/", 1)[-1]
            whole = open(re.sub(r"-\d+\.json$", ".log", path)).read()
            end = whole.index(f"(saved {name})")
            start = whole.rfind("(saved ", 0, end)
            log = whole[whole.index("\n", start) if start >= 0 else 0:end]
        except (OSError, ValueError):
            log = None
    if log is None:
        timeouts = guard = "-"
    else:
        timeouts, guard = log.count("timed out"), log.count("repeated themselves") + log.count("asking for game content")
    killed = [x["name"] for x in e if x["type"] == "death" and x["how"] == "night"]
    lynched = [f"{x['name']}({roles[x['name']]})" for x in e if x["type"] == "death" and x["how"] == "vote"]   # the cast role: with --hide-vote the death has none
    print(f"{path}: {e[-1].get('winner')} in {days} days, {e[-1]['t'] / 60:.1f} min, {len(says)} lines, Highlights {hi:.1f} min at 1x, "
          f"claims {len(claims)} by {claimers}, whispers {whispers}, repeats {repeats}, timeouts {timeouts}, guard {guard}, "
          f"night kills {killed}, lynched {lynched}, roles {roles}")
