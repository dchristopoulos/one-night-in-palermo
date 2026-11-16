#!/usr/bin/env python3
"""Lab: try prompt and rule variants on the real engine without editing game.py.

It imports game.py, patches it in memory, and saves the game under games/lab/. Every game.py flag still works
(--days, --budget, --seed, --seats, --roles, --kill-night1, --no-parity, --reveal-night, --notes, --checks, --hide-vote,
--no-last-words, --no-ghosts, --repeat-save, --history f1,f2, --prompt NAME ...).

  python3 lab.py --name base-11 --seed 11 --days 1                 # today's engine, one day
  python3 lab.py --name bare-11 --seed 11 --days 1 --lab bare      # same deal, short system prompt
  python3 lab.py --moment officer [--lab bare]                     # one moment, every seat, real calls
  python3 lab.py --report games/lab/*.json                         # numbers per game
  python3 lab.py --show games/lab/base-11.json                     # public transcript (plus the viewer-only lines)

Switches for --lab (comma separated). The switches tried on 2026-11-14 (noexamples, stakes, wants, history, banter,
testimony, graveyard, lastwords, will, seven, fun) are engine behaviour now; see docs/engine-rules.md.
  bare       system prompt = the rules + three lines; no "what is at stake", no talk rules; lines cut at 25 words
  hunter     a voted-out player takes one player out with them
"""
import collections
import json
import pathlib
import random
import re
import statistics
import sys

ARGV = sys.argv[1:]


def opt(name, default=""):
    if name in ARGV:
        i = ARGV.index(name)
        value = ARGV[i + 1]
        del ARGV[i:i + 2]
        return value
    return default


LAB = set(filter(None, opt("--lab").split(",")))
NAME = opt("--name", "t")
MOMENT = opt("--moment")
FILLER = r"nothing (yet|solid|stands|to report)|no read|too early|what('s| is) your (first )?read|\bany(thing)? stand"

def metrics(path):
    ev = json.load(open(path))
    says = [e for e in ev if e["type"] == "say" and e.get("why") not in ("confession", "before the game", "last words")]
    lines = [e["text"] for e in says]
    if not lines:
        return None
    day, d1 = "", []
    for e in ev:
        if e["type"] == "phase":
            day = e["text"]
        if e["type"] == "say" and day == "Day 1" and e.get("why") != "confession":
            d1.append(e["text"])
    by = collections.defaultdict(list)
    for e in says:
        by[e["name"]].append(e["text"])
    wc = [len(l.split()) for l in lines]
    end = [e for e in ev if e["type"] == "end"]
    cast = {p["name"]: p["role"] + ("*" if p.get("shown") else "") for p in ev[0]["players"]}
    out = [(e["name"], e["how"]) for e in ev if e["type"] == "death"]
    names = "|".join(cast)
    return {
        "file": pathlib.Path(path).stem, "winner": end[-1]["winner"] if end else "-", "lines": len(lines), "day1": len(d1),
        "words": statistics.median(wc), "long": sum(w > 20 for w in wc) / len(wc),
        "q": sum(l.rstrip().endswith("?") for l in lines) / len(lines),
        "filler": sum(bool(re.search(FILLER, l, re.I)) for l in lines) / len(lines),
        "namefirst": sum(bool(re.match(rf"\W*({names})\b", l)) for l in lines) / len(lines),
        "openers": len({re.sub(r"\W", "", l.split()[0].lower()) for l in lines}) / len(lines),
        "first_out": f"{out[0][0]} ({cast[out[0][0]]}, {out[0][1]})" if out else "-",
        "min": round(ev[-1]["t"] / 60, 1), "ghost": sum(e["type"] == "ghost" for e in ev),
    }


def report(files):
    print(f"{'game':22s} {'winner':8s} {'min':>4s} {'lines':>5s} {'d1':>3s} {'med w':>5s} {'>20w':>5s} {'q':>4s} {'filler':>6s} "
          f"{'name1st':>7s} {'openers':>7s}  first out")
    for f in files:
        m = metrics(f)
        if m:
            print(f"{m['file']:22s} {m['winner']:8s} {m['min']:4.1f} {m['lines']:5d} {m['day1']:3d} {m['words']:5.0f} {m['long']:5.0%} "
                  f"{m['q']:4.0%} {m['filler']:6.0%} {m['namefirst']:7.0%} {m['openers']:7.0%}  {m['first_out']}")


def show(path):
    ev = json.load(open(path))
    print("##", pathlib.Path(path).stem, "|", ", ".join(f"{p['name']}={p['role']}{'*' if p.get('shown') else ''}" for p in ev[0]["players"]))
    for e in ev:
        t = e["type"]
        if t == "phase":
            print(f"-- {e['text']}")
        elif t == "say":
            print(f"{e['name']}{' [' + e['why'] + ']' if e.get('why') in ('last words', 'confession', 'before the game') else ''}: {e['text']}")
        elif t == "gm":
            print(f"  ({'host aside' if e.get('aside') else 'narrator'}) {e['text']}")
        elif t == "note":
            print(f"  {e['name']} [note, read in the morning]: {e['text']}")
        elif t == "whisper":
            print(f"  ~ {e['name']} whispers to {e['to']}: {e['text']}")
        elif t == "ghost":
            print(f"  + {e['name']} (out, unheard): {e['text']}")
        elif t == "night_action" and e["action"] != "propose":
            print(f"  . {e['name']} {e['action']} {e['target']} {e.get('result', '')}")
        elif t == "votes":
            print("  VOTES: " + "; ".join(f"{a}->{b} ({why[:60]})" for a, b, why in e["votes"]))
        elif t == "death":
            print(f"  x {e['name']} out ({e['how']}, card: {e.get('role') or 'face down'})")
        elif t == "pass":
            print(f"{e['name']}: (passes)")
        elif t == "end":
            print(f"== winner: {e['winner']}")


if "--report" in ARGV:
    report([a for a in ARGV if a.endswith(".json")])
    sys.exit()
if "--show" in ARGV:
    for a in ARGV:
        if a.endswith(".json"):
            show(a)
    sys.exit()

sys.argv = [sys.argv[0], "--fast", "--tag", f"lab/{NAME}"] + ARGV
import game  # noqa: E402  (reads its flags from sys.argv on import)

UNKNOWN = LAB - {"bare", "hunter"}
if UNKNOWN:
    sys.exit(f"--lab: unknown switch {', '.join(sorted(UNKNOWN))} (bare, hunter; the others are engine behaviour now)")

if "bare" in LAB:
    the_game = game.RULES.split("\n\nWHAT IS AT STAKE")[0]
    game.RULES = (the_game + "\n\nYou are talking out loud at a table, so you say a few words at a time, the way anyone does. "
                  "How you play is up to you. Speak as \"I\".")
    game.trim.__defaults__ = (25,)

if "hunter" in LAB:
    _out, _day = game.Game.out, game.Game.day

    def out(self, p, how):
        _out(self, p, how)
        if how == "vote" and not getattr(self, "shooting", False):
            self.shooter = p                          # the shot comes after the narrator has announced the vote

    def hunter_day(self, n):
        self.shooter = None
        _day(self, n)
        p = self.shooter
        if p and len(self.alive()) > 2 and self.winner() is None:
            self.shooting = True                      # the one they take with them does not shoot back
            r = self.act(p, "Rule of this table: a voted-out player takes one player with them. Name the player who goes "
                            "out with you.", "TARGET", self.alive())
            self.emit({"type": "night_action", "name": p["name"], "action": "shoot", "target": r["pick"]["name"]})
            _out(self, r["pick"], "vote")
            r["pick"]["how"] = f"taken out by {p['name']} on day {self.day_no}"
            self.narrate(f"On the way out {p['name']} points at {r['pick']['name']}, and {r['pick']['name']} is out too."
                         + (f" {r['pick']['name']}'s card stays face down." if game.HIDE_VOTE else f" {r['pick']['name']} shows the card: {r['pick']['role']}."))
            self.shooting = False
    game.Game.out, game.Game.day = out, hunter_day
    game.RULES = game.RULES.replace("the player with the most votes is out",
                                    "the player with the most votes is out, names one player who goes out with them,", 1)


def setup():
    seats = [game.load(f)[0] for f in game.seat_files()]
    if game.DRY:                                  # --dry: no model is touched
        return [s["name"] for s in seats]
    game.check_subscriptions()
    game.ensure_local({m["model"].partition(":")[2] for m in seats if m["model"].startswith("local:")})
    return [s["name"] for s in seats]


MOMENTS = {
    # the officer under a majority lean on day 1: do they claim and name the killer they know?
    "officer": (["{a}: Morning. {O}, you're quiet. What are you?", "{O}: Citizen. Just listening.", "{K}: {O} answered fast. Too fast.",
                 "{b}: Same. {O} hasn't said anything real.", "{c}: {K} jumped on {O} pretty quick.", "{K}: Because {O} is dodging. Gut.",
                 "{O}: I'm not dodging. {K}, why so eager?", "{d}: Nothing yet. {O} feels off though.",
                 "{a}: {O} turned it on {K} instantly. Classic.", "{b}: I'm voting {O}.", "{c}: I'm not sold, but {O} isn't helping.",
                 "{d}: {O}, give us one real read.", "{O}: {K} pushed first and hardest.", "{a}: Still {O}. I'm leaning there."],
                "O", "Most of the table leans on you (see LEANS NOW). Answer 1 of 2, then the vote."),
    # the shown killer named by a real officer claim: deny, counter-claim, or fold?
    "killer": (["{a}: Morning. Anyone got anything?", "{K}: Not yet. {c}, you look nervous.", "{c}: I'm fine. Why me?",
                "{O}: {K} keeps picking on people. I don't like it.", "{K}: I asked one question, {O}.",
                "{b}: {O}, that's thin. Why {K}?", "{O}: I'm the officer. {K} was shown to me as a killer on night 1. Vote {K}."],
               "K", "{O} just named you. Answer in a few words, or PASS (the table sees it)."),
}


def moment(kind, names):
    lines, who, task = MOMENTS[kind]
    for i, s in enumerate(names):
        rest = names[i + 1:] + names[:i]
        r = dict(zip("abcd", rest[1:]))
        r.update({"O": s, "K": rest[0]} if who == "O" else {"K": s, "O": rest[0]})
        hidden = r["a"]
        game.KILLER, game.SHOWN = hidden, ""
        game.ROTATE = {**{n: "citizen" for n in names},
                       r["O"]: "officer", r["K"]: "killer", hidden: "killer", r["b"]: "doctor", r["c"]: "citizen", r["d"]: "citizen"}
        game.TAG = f"lab/moment-{kind}-{'-'.join(sorted(LAB)) or 'base'}-{s}"
        g = game.Game()
        g.phase_name, g.day_no = "Day 1", 1
        officer = next(p for p in g.players if p["name"] == r["O"])
        if officer["checks"]:                                # --checks: the officer also has a night-1 check
            officer["notes"].append(f"Night 1: you checked {r['c']}: NOT a killer.")
        night = ("Night falls on Palermo and everyone closes their eyes. The killers meet in the dark, and the officer is shown "
                 "one of them. A new day dawns in Palermo. Nobody is out." if game.QUIET_NIGHT else
                 "Night falls on Palermo. The killers strike, but the doctor got there first. A new day dawns in Palermo, and "
                 "nobody is out.")
        g.today = [f"Narrator: {night}"] + [l.format(**r) for l in lines]
        g.public = list(g.today)
        g.leans = {r["K"]: s, r["a"]: s, r["b"]: s, r["d"]: s} if who == "O" else {r["O"]: s}
        p = next(x for x in g.players if x["name"] == s)
        a = g.act(p, task.format(**r), "SAY", extra=game.LEAN_FIELD)
        claim = "CLAIMS OFFICER" if game.CLAIM.search(a["text"]) else "no claim"
        named = "names " + r["K" if who == "O" else "O"] if re.search(rf"\b{r['K' if who == 'O' else 'O']}\b", a["text"], re.I) else "names nobody"
        print(f">> {s:7s} [{claim}, {named}] SAY: {a['text'] or '(pass)'}   | thinks: {a['thought']}", flush=True)


if __name__ == "__main__":
    if "--seed" in game.ARGS:
        random.seed(int(game.ARGS[game.ARGS.index("--seed") + 1]))
    seat_names = setup()
    if MOMENT:
        moment(MOMENT, seat_names)
        sys.exit()
    g = game.Game()
    print(f"lab switches: {sorted(LAB) or 'none'}; roles: " + ", ".join(f"{p['name']}={p['role']}" for p in g.players), flush=True)
    print(f"Winner: {g.run()}  (saved {g.files[0]})", flush=True)
