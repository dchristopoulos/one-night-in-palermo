#!/usr/bin/env python3
"""Judge an evening on the current engine (seven seats, two killers: one shown, one hidden; 2026-11-15 rules).

  python3 stats.py r5a            # games/r5a-1.json, games/r5a-2.json, ...
  python3 stats.py fin71 run81    # one table row per game, then a summary per tag
  python3 stats.py --all          # every tag in games/ whose games have seven seats (dry games skipped)

Unfinished games (no `end` event, or winner "stopped") are skipped. Reads only the saved event lists; never imports game.py.
It replaced an older leaderboard that imported game.py and counted games from earlier rule sets."""
import collections, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TALK_SKIP = ("confession", "before the game", "last words", "defends before the vote")


def analyse(ev, name=""):
    """One finished game -> a dict of facts. None if the game did not finish."""
    end = next((e for e in ev if e.get("type") == "end"), None)
    cast = next((e for e in ev if e.get("type") == "cast"), None)
    if not cast or not end or end.get("winner") not in ("town", "killer"):
        return None
    roles = {p["name"]: p["role"] for p in cast["players"]}
    killers = [p["name"] for p in cast["players"] if p["role"] == "killer"]
    shown = next((p["name"] for p in cast["players"] if p["role"] == "killer" and p.get("shown")), None)
    hidden = next((k for k in killers if k != shown), None)
    officer = next((n for n, r in roles.items() if r == "officer"), None)
    doctor = next((n for n, r in roles.items() if r == "doctor"), None)
    g = dict(name=name, winner=end["winner"], minutes=end.get("t", 0) / 60, roles=roles, shown=shown, hidden=hidden,
             officer=officer, days={}, deaths={}, claims=[], words=[], cut=0, lines=collections.Counter(),
             guards=[], saves=0, bus=None, d1out=None)
    phase, day, night, line, kill, claimed = "", 0, 0, 0, None, set()
    for e in ev:
        t = e.get("type")
        if t == "phase":
            phase = e["text"]
            if e.get("kind") == "night":
                night, kill = night + 1, None
            else:
                day, line = day + 1, 0
                g["days"][day] = dict(lines=0, budget=None, left=None, voted=False, runoffs=0, out=None)
        elif t == "clock" and day and not g["days"][day]["voted"]:
            d = g["days"][day]
            if d["budget"] is None:
                d["budget"] = e["total"]
            d["left"] = e["left"]
        elif t == "say":
            why, who = e.get("why", ""), e["name"]
            if e["text"].rstrip().endswith("…"):
                g["cut"] += 1
            if e.get("claim") == "officer" and why not in ("confession", "before the game"):
                if who not in claimed:
                    claimed.add(who)
                    g["claims"].append((who, day, "last words" if why == "last words" else line + 1, who == officer))
            if why in TALK_SKIP or not phase.startswith("Day"):
                continue
            line += 1
            g["days"][day]["lines"] += not g["days"][day]["voted"]    # the budgeted talk (a tie's extra round not counted)
            g["lines"][who] += 1
            g["words"].append(len(e["text"].split()))
        elif t in ("ghost", "note") and e["text"].rstrip().endswith("…"):
            g["cut"] += 1
        elif t == "votes":
            d = g["days"][day]
            d["runoffs"] += bool(e.get("runoff"))
            if day == 1 and not e.get("runoff") and hidden:
                g["bus"] = any(v[0] == hidden and v[1] == shown for v in e["votes"])
            d["voted"] = True
        elif t == "night_action":
            if e["action"] == "kill":
                kill = e["target"]
            elif e["action"] == "save" and e["name"] == doctor:
                g["guards"].append((night, e["target"], e["target"] in claimed))
        elif t == "death":
            how = e["how"]
            n = day if how == "vote" else night
            g["deaths"][e["name"]] = (how, n)
            if how == "vote":
                g["days"][day]["out"] = e["name"]
                if day == 1:
                    g["d1out"] = e["name"]
            if how == "night":
                kill = None
        if t == "phase" and e.get("kind") == "day" and night and kill is not None:
            g["saves"] += 1                                    # a kill was tried last night and nobody died
    how, n = list(g["deaths"].values())[-1] if g["deaths"] else ("", 0)
    g["ending"] = (f"last killer voted out day {n}" if g["winner"] == "town"
                   else f"parity {'day' if how == 'vote' else 'night'} {n}")
    g["ndays"] = day
    return g


def fate(g, who):
    if who not in g["deaths"]:
        return "alive"
    how, n = g["deaths"][who]
    return f"{'voted out day' if how == 'vote' else 'killed night'} {n}"


def where(claim):
    return f"day {claim[1]} " + (claim[2] if claim[2] == "last words" else f"line {claim[2]}")


def d1kind(g):
    x = g["d1out"]
    return ("nobody" if x is None else "shown killer" if x == g["shown"] else "hidden killer" if x == g["hidden"]
            else "officer" if x == g["officer"] else "other")


def load(tag):
    files = sorted(glob.glob(os.path.join(HERE, "games", f"{tag}-*.json")),
                   key=lambda f: int(re.findall(r"-(\d+)\.json$", f)[0]) if re.search(r"-\d+\.json$", f) else 0)
    out = []
    for f in files:
        if not re.fullmatch(re.escape(tag) + r"-\d+\.json", os.path.basename(f)):
            continue
        try:
            g = analyse(json.load(open(f)), os.path.basename(f)[:-5])
        except (OSError, ValueError, KeyError):
            continue
        if g:
            out.append(g)
    return out


def all_tags():
    tags = set()
    for f in glob.glob(os.path.join(HERE, "games", "*-*.json")):
        m = re.fullmatch(r"(.+)-\d+\.json", os.path.basename(f))
        if not m or re.fullmatch(r"\d{8}", m.group(1)) or "fixture" in m.group(1):
            continue
        try:
            cast = next(e for e in json.load(open(f)) if e.get("type") == "cast")
        except (OSError, ValueError, StopIteration):
            continue
        if len(cast["players"]) == 7 and not cast.get("dry"):
            tags.add(m.group(1))
    return sorted(tags)


def pct(a, b):
    return f"{a}/{b}" if b else "-"


def table(games):
    print("| game | won | how it ended | min | officer claim | counter | officer | day-1 out | hidden killer | bus | doc saves |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for g in games:
        own = next((c for c in g["claims"] if c[3]), None)
        fake = [c[0] for c in g["claims"] if not c[3]]
        print(f"| {g['name']} | {g['winner']} | {g['ending']} | {g['minutes']:.0f} | "
              f"{where(own) if own else 'no'} | {', '.join(fake) or '-'} | {fate(g, g['officer'])} | "
              f"{d1kind(g)} | {fate(g, g['hidden']).replace('voted out', 'caught').replace('alive', 'survived')} | "
              f"{'yes' if g['bus'] else 'no'} | {g['saves']} |")


def summary(tag, games):
    n = len(games)
    if not n:
        print(f"\n## {tag}: no finished games")
        return
    C = collections.Counter
    print(f"\n## {tag}: {n} game{'s' * (n != 1)}, town {sum(g['winner'] == 'town' for g in games)}, killers "
          f"{sum(g['winner'] == 'killer' for g in games)}; {sum(g['ndays'] for g in games) / n:.1f} days, "
          f"{sum(g['minutes'] for g in games) / n:.1f} min on average")
    print("ended: " + ", ".join(f"{k} x{v}" for k, v in sorted(C(g["ending"] for g in games).items())))
    for d in range(1, max(g["ndays"] for g in games) + 1):
        ds = [g["days"][d] for g in games if d in g["days"]]
        early = sum(1 for x in ds if x["left"])
        print(f"day {d}: {len(ds)} played, lines avg {sum(x['lines'] for x in ds) / len(ds):.1f} "
              f"(budget {'/'.join(sorted({str(x['budget']) for x in ds}))}), vote early {early} / at budget {len(ds) - early}, "
              f"ties {sum(x['runoffs'] > 0 for x in ds)} (runoffs {sum(x['runoffs'] for x in ds)}), nobody out "
              f"{sum(x['out'] is None for x in ds)}")
    own = [next((c for c in g["claims"] if c[3]), None) for g in games]
    print(f"officer: claimed {sum(bool(c) for c in own)}/{n} (" + ", ".join(where(c) for c in own if c)
          + f"); counter-claims {sum(1 for g in games for c in g['claims'] if not c[3])}; fate: "
          + ", ".join(f"{k} x{v}" for k, v in sorted(C(fate(g, g['officer']) for g in games).items())))
    print("day-1 vote-out: " + ", ".join(f"{k} x{v}" for k, v in sorted(C(d1kind(g) for g in games).items())))
    gd = [x for g in games for x in g["guards"]]
    print(f"doctor: {len(gd)} nights acted, {sum(g['saves'] for g in games)} saves; guarded a claimed officer "
          f"{sum(x[2] for x in gd)}, others {sum(not x[2] for x in gd)}")
    print("hidden killer: " + ", ".join(f"{k} x{v}" for k, v in sorted(C(
        fate(g, g["hidden"]).replace("voted out", "caught").replace("alive", "survived") for g in games).items()))
        + f"; voted for the partner on day 1 (bus) {sum(bool(g['bus']) for g in games)}/{n}")
    words = [w for g in games for w in g["words"]]
    lines = C()
    for g in games:
        lines.update(g["lines"])
    print(f"talk: {sum(words) / max(1, len(words)):.1f} words per day line, {sum(g['cut'] for g in games)} lines cut with '…', "
          f"lines per game: " + ", ".join(f"{k} {v / n:.1f}" for k, v in lines.most_common()))


def seats(games):
    S = collections.defaultdict(collections.Counter)
    for g in games:
        for who, role in g["roles"].items():
            s = S[who]
            s["games"] += 1
            s["wins"] += g["winner"] == ("killer" if role == "killer" else "town")
            s["killer"] += role == "killer"
            how = g["deaths"].get(who, ("",))[0]
            s["voted out"] += how == "vote"
            s["killed"] += how == "night"
    print("\n| seat | games | wins | killer | voted out | killed at night |\n|---|---|---|---|---|---|")
    for who, s in sorted(S.items(), key=lambda kv: (-kv[1]["wins"], kv[0])):
        print(f"| {who} | {s['games']} | {s['wins']} | {s['killer']} | {s['voted out']} | {s['killed']} |")


def main(argv):
    tags = all_tags() if "--all" in argv else [a for a in argv if not a.startswith("-")]
    if not tags:
        sys.exit(__doc__)
    per = {t: load(t) for t in tags}
    everything = [g for t in tags for g in per[t]]
    table(everything)
    for t in tags:
        summary(t, per[t])
    seats(everything)


if __name__ == "__main__":
    main(sys.argv[1:])
