#!/usr/bin/env python3
"""Per-model table character: plain counts per seat across finished games, by the role each seat was dealt.

  python3 characters.py fun9 sun15 r7a          # games/fun9-1.json, ... ; one set of tables over all of them
  python3 characters.py fun9 sun15 r7a --md     # the same tables as GitHub Markdown

Unfinished games (no `end` event, winner "stopped", or a file still being written) are skipped. Reads only the saved
event lists; uses analyse() from stats.py for roles, deaths, officer claims, winner and day lines.
Definitions (one line each) are printed under each table."""
import collections, glob, json, os, re, sys

from stats import HERE, TALK_SKIP, analyse

SEATS = ("Sonnet", "Haiku", "Opus", "Sol", "Luna", "Terra", "Gemma")
TOWN = ("officer", "doctor", "citizen")


def files(tag):
    """The game files of one tag, in game-number order (tag-1.json, tag-2.json, ...)."""
    out = [f for f in glob.glob(os.path.join(HERE, "games", f"{tag}-*.json"))
           if re.fullmatch(re.escape(tag) + r"-\d+\.json", os.path.basename(f))]
    return sorted(out, key=lambda f: int(re.findall(r"-(\d+)\.json$", f)[0]))


def read(paths):
    """Finished games as (analyse() dict, event list) pairs. Broken or unfinished files are skipped."""
    out = []
    for f in paths:
        try:
            with open(f) as fh:
                ev = json.load(fh)
            g = analyse(ev, os.path.basename(f)[:-5])
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            continue
        if g:
            out.append((g, ev))
    return out


def load(tags):
    """Finished games of the tags, in tag order, then game number."""
    return read([f for tag in tags for f in files(tag)])


def walk(ev):
    """Facts per seat that analyse() does not keep: words per day line, passes, first-round ballots with their day,
    the last lean each seat stated on day 1, and the doctor's saves (a save on the night's kill target)."""
    f = dict(words=collections.defaultdict(list), passes=collections.Counter(), rounds=[], lean1={}, saves=0, acted=0)
    phase, day, kill, save = "", 0, None, None
    for e in ev:
        t = e.get("type")
        if t in ("phase", "end") and save is not None:
            f["saves"] += save == kill                  # the night is over: was the protected player the target?
            save = None
        if t == "phase":
            phase = e["text"]
            if e.get("kind") == "night":
                kill = None
            else:
                day += 1
        elif t == "say" and phase.startswith("Day") and e.get("why", "") not in TALK_SKIP:
            f["words"][e["name"]].append(len(e["text"].split()))
            if day == 1 and e.get("lean") and not any(r[0] == 1 for r in f["rounds"]):
                f["lean1"][e["name"]] = e["lean"]
        elif t == "pass" and phase.startswith("Day"):
            f["passes"][e["name"]] += 1
        elif t == "votes" and not e.get("runoff"):
            f["rounds"].append((day, [(v[0], v[1]) for v in e["votes"]]))
        elif t == "night_action":
            if e["action"] == "kill":
                kill = e["target"]
            elif e["action"] == "save":
                save = e["target"]
                f["acted"] += 1
    return f


def names(text, who):
    """True when the name `who` appears in the text as a word."""
    return bool(re.search(rf"\b{re.escape(who)}\b", text or ""))


def officer_named_shown(ev, g):
    """True when the officer made a claim-marked day line on day 1 that names the shown killer."""
    phase, day = "", 0
    for e in ev:
        if e.get("type") == "phase":
            phase, day = e["text"], day + (e.get("kind") != "night")
        elif (e.get("type") == "say" and day == 1 and phase.startswith("Day") and e["name"] == g["officer"]
              and e.get("claim") == "officer" and e.get("why", "") not in TALK_SKIP and names(e["text"], g["shown"])):
            return True
    return False


def tally(games):
    """Per seat, a Counter of every measure, plus the days on which a seat was voted out as a killer."""
    S = collections.defaultdict(collections.Counter)
    out_days = collections.defaultdict(list)
    for g, ev in games:
        f = walk(ev)
        killers = {g["shown"], g["hidden"]}
        d1out = g["d1out"]
        for who, role in g["roles"].items():
            s, kind = S[who], "k" if role == "killer" else "t"
            how, n = g["deaths"].get(who, ("", 0))
            won = g["winner"] == ("killer" if kind == "k" else "town")
            s["games"] += 1
            s[kind + " games"] += 1
            s[kind + " won"] += won
            s[kind + " voted out"] += how == "vote"
            s[kind + " killed"] += how == "night"
            s[kind + " alive"] += how == ""
            for day, ballots in f["rounds"]:
                if any(v == who for v, _ in ballots):
                    s[kind + " faced"] += 1
                    s[kind + " received"] += sum(t == who for _, t in ballots)
                for v, t in ballots:
                    if v == who:
                        s[kind + " cast"] += 1
                        s[kind + " on killer"] += t in killers
                        s["k on partner"] += kind == "k" and t in killers
            claimed = any(c[0] == who for c in g["claims"])
            if kind == "k":
                s["k claimed"] += claimed
                s["k shown"] += who == g["shown"]
                s["k shown won"] += who == g["shown"] and won
                s["k shown out"] += who == g["shown"] and how == "vote"
                s["k hidden out"] += who == g["hidden"] and how == "vote"
                s["k hidden won"] += who == g["hidden"] and won
                if how == "vote":
                    out_days[who].append(n)
            elif role != "officer":
                s["t false claim"] += claimed
            if role == "officer":
                s["o games"] += 1
                s["o claimed"] += claimed
                s["o named d1"] += officer_named_shown(ev, g)
                s["o voted out"] += how == "vote"
                s["o killed"] += how == "night"
                s["o shown out"] += g["deaths"].get(g["shown"], ("",))[0] == "vote"
                s["o won"] += won
            if role == "doctor":
                s["d games"] += 1
                s["d acted"] += f["acted"]
                s["d saves"] += f["saves"]
            s["lines"] += g["lines"][who]
            s["words"] += sum(f["words"][who])
            s["passes"] += f["passes"][who]
            lean = f["lean1"].get(who)
            if lean and d1out:
                s["lean1"] += 1
                s["lean1 out"] += lean == d1out
            if lean and kind == "t":
                s["t lean1"] += 1
                s["t lean1 killer"] += lean in killers
    return S, out_days


def of(a, b):
    return f"{a} of {b}" if b else "-"


def tables(S, out_days, n):
    """Each table as (title, header, rows, notes)."""
    seats = [w for w in SEATS if w in S] + sorted(w for w in S if w not in SEATS)
    k = [[w, S[w]["k games"], of(S[w]["k won"], S[w]["k games"]), of(S[w]["k alive"], S[w]["k games"]),
          of(S[w]["k voted out"], S[w]["k games"]) + (f" (day {', '.join(map(str, sorted(out_days[w])))})"
                                                      if out_days[w] else ""),
          f"{S[w]['k received']} in {S[w]['k faced']}", of(S[w]["k claimed"], S[w]["k games"]),
          f"{S[w]['k shown']} / {S[w]['k games'] - S[w]['k shown']}",
          f"{S[w]['k shown out']} / {S[w]['k hidden out']}", f"{S[w]['k shown won']} / {S[w]['k hidden won']}"]
         for w in seats]
    t = [[w, S[w]["t games"], of(S[w]["t won"], S[w]["t games"]), of(S[w]["t voted out"], S[w]["t games"]),
          of(S[w]["t killed"], S[w]["t games"]), of(S[w]["t on killer"], S[w]["t cast"]),
          f"{S[w]['t received']} in {S[w]['t faced']}", of(S[w]["t false claim"], S[w]["t games"] - S[w]["o games"])]
         for w in seats]
    o = [[w, S[w]["o games"], of(S[w]["o claimed"], S[w]["o games"]), of(S[w]["o named d1"], S[w]["o games"]),
          of(S[w]["o voted out"], S[w]["o games"]), of(S[w]["o killed"], S[w]["o games"]),
          of(S[w]["o shown out"], S[w]["o games"]),
          of(S[w]["o won"], S[w]["o games"]), of(S[w]["d saves"], S[w]["d acted"]) + f" ({S[w]['d games']} games)"]
         for w in seats]
    talk = [[w, S[w]["games"], f"{S[w]['lines'] / max(1, S[w]['games']):.1f}",
             f"{S[w]['words'] / max(1, S[w]['lines']):.1f}", S[w]["passes"],
             of(S[w]["lean1 out"], S[w]["lean1"]), of(S[w]["t lean1 killer"], S[w]["t lean1"]),
             of(S[w]["k on partner"], S[w]["k cast"])] for w in seats]
    return [
        (f"As a killer ({n} games, 2 killers each)",
         ["seat", "games", "killers won", "alive at end", "voted out", "ballots received in votes faced",
          "claimed officer", "games as shown / hidden", "voted out as shown / hidden", "won as shown / hidden"], k,
         ["Votes faced: first-round votes in which the seat cast a ballot (runoffs not counted).",
          "Claimed officer: made at least one line the engine marked as an officer claim (day lines or last words)."]),
        ("As town (officer, doctor and citizens together)",
         ["seat", "games", "town won", "voted out", "killed at night", "ballots naming a killer",
          "ballots received in votes faced", "false officer claim (doctor, citizen)"], t,
         ["Ballots: first-round ballots only. A ballot names a killer when its target was dealt the killer card."]),
        ("As officer, and the doctor's saves",
         ["seat", "officer games", "claimed officer", "day-1 claim named the shown killer", "officer voted out",
          "officer killed at night", "shown killer voted out", "town won", "doctor saves of nights protected"], o,
         ["Day-1 claim named the shown killer: an officer's claim-marked day-1 line names the shown killer.",
          "Doctor save: the doctor's target was the killers' target that night."]),
        ("Talk and reads (all roles)",
         ["seat", "games", "day lines per game", "words per day line", "turns with no line",
          "day-1 lean was the player voted out", "day-1 lean on a killer, as town",
          "ballots on own partner, as killer"], talk,
         ["Day lines: lines in day talk, without last words, before-the-game lines, confessions and defences.",
          "Turns with no line: `pass` events (a chosen pass or a dropped line; the files do not tell them apart).",
          "Day-1 lean: the seat's last stated lean before the first vote of day 1; counted when someone went out."]),
    ]


def show(tbls, md):
    for title, head, rows, notes in tbls:
        if md:
            print(f"\n### {title}\n\n| " + " | ".join(head) + " |\n|" + "---|" * len(head))
            for r in rows:
                print("| " + " | ".join(map(str, r)) + " |")
            print("\n" + "\n".join(f"- {x}" for x in notes))
        else:
            cells = [head] + [list(map(str, r)) for r in rows]
            width = [max(len(c[i]) for c in cells) for i in range(len(head))]
            print(f"\n{title}")
            for c in cells:
                print("  ".join(x.ljust(w) for x, w in zip(c, width)).rstrip())
            for x in notes:
                print(f"  {x}")


def main(argv):
    tags = [a for a in argv if not a.startswith("-")]
    if not tags:
        sys.exit(__doc__)
    games = load(tags)
    S, out_days = tally(games)
    by_tag = collections.Counter(g["name"].rsplit("-", 1)[0] for g, _ in games)
    print(f"{len(games)} finished games: " + ", ".join(f"{t} {by_tag[t]}" for t in tags))
    show(tables(S, out_days, len(games)), "--md" in argv)


if __name__ == "__main__":
    main(sys.argv[1:])
