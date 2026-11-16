#!/usr/bin/env python3
"""Fun meter: how watchable is a finished game? Measures games; nothing here reaches the players.

  python3 funmeter.py r5a r7a sun15            # tags (games/r5a-*.json) or file paths
  python3 funmeter.py sun15 --judges gpt-6-sol,gpt-6-luna --report
  python3 funmeter.py games/sun15-3.json --force

Each game is rendered as the audience sees it in Watch mode and sent with the rubric (docs/fun-meter.md) to a judge
on the `codex` CLI (ChatGPT subscription; API keys stripped). Results: games/fun/<name>.json, cached per judge.
Stdlib only; never imports game.py (it reads sys.argv at import); the codex call is copied from game.call()."""
import concurrent.futures, glob, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "games", "fun")
RUBRIC = [  # key, name, 1 / 3 / 5 anchors (observable in a transcript); evidence in docs/fun-meter.md
    ("irony", "Lies the audience can see",
     "killers barely talk, or say what they think; nothing for a watcher who knows the cards to enjoy",
     "killers deny and deflect plausibly; a thought or whisper now and then contrasts with the public line",
     "a killer tells a bold lie or false claim to someone's face while the audience knows; the gap between thought and line is the show"),
    ("reversal", "Reversals",
     "everything goes the way day 1 pointed; no vote or card surprises",
     "one turn: a vote swings late, a save, a counter-claim, a trusted player turns out the killer",
     "two or more turns the audience did not see coming, at least one of which changes who is winning"),
    ("mistake", "Mistakes with consequences",
     "no visible errors, or errors that change nothing",
     "a wrong read or slip that costs something small",
     "a slip, a misremembered fact or a wrong vote-out the audience could see coming and that decides the game"),
    ("voices", "Distinct characters",
     "lines are interchangeable; remove the names and you cannot tell who speaks",
     "two or three players have a recognisable manner (temper, humour, bluntness, a grudge)",
     "nearly every player has a voice and a want of their own; you could tell them apart blind"),
    ("clash", "Confrontation",
     "players talk to the room in general terms; nobody is pressed",
     "direct accusations get answered, a defence under pressure",
     "a sustained head-to-head (accuse, deny, counter, the table splits) that the vote then settles"),
    ("quotable", "Quotable lines",
     "nothing you would repeat",
     "one line that is funny, sharp or memorable",
     "several lines a viewer would quote to a friend, including comedy from character or blunders"),
    ("freshness", "No dead air or repetition",
     "the same points restated, stretches where nothing moves, generic filler ('let's see who stays quiet')",
     "some restating, mostly moving",
     "nearly every line adds information, pressure or character; short and alive"),
    ("suspense", "Uncertain outcome",
     "decided early: after day 1 the winner is obvious to a watcher who knows the cards",
     "in doubt until the middle",
     "in doubt until the last vote or night; close votes, the hidden killer in real danger or nearly caught"),
    ("ending", "An ending decided by a choice",
     "ends by arithmetic or a formula nobody chose; the reveal lands flat",
     "the last vote or kill is a reasonable choice; the end card explains it",
     "the end turns on one player's decision or gamble (a swing vote, a bluff, a kill choice) and the reveal pays off"),
]
KEYS = [r[0] for r in RUBRIC]
STOP = set("the a an and or but to of in on at is are was were be been it its this that i you he she we they me him her us "
           "them my your not no so if then than as for with by from about just do did have has can would will what who why "
           "how when there here i'm it's don't".split())


def finished(ev):
    end = next((e for e in ev if e.get("type") == "end"), None)
    return bool(end) and end.get("winner") in ("town", "killer")


def paths(args):
    out = []
    for a in args:
        if os.path.exists(a):
            out.append(a)
            continue
        files = glob.glob(os.path.join(HERE, "games", f"{a}-*.json"))
        out += sorted((f for f in files if re.fullmatch(rf"{re.escape(a)}-\d+\.json", os.path.basename(f))),
                      key=lambda f: int(re.findall(r"\d+", os.path.basename(f))[-1]))
    return out


def render(ev):
    """Watch mode as text: every role, table talk, the speaker's own thought with their line, votes, cards, ghosts, host."""
    cast = next(e for e in ev if e.get("type") == "cast")
    roles = {p["name"]: p["role"] for p in cast["players"]}
    head = ["ROLES (the audience knows them): " + ", ".join(
        f"{p['name']} {p['role']}" + (" (shown to the officer)" if p.get("shown") else
                                      " (hidden)" if p["role"] == "killer" else "") for p in cast["players"])]
    lines, thought = [], None
    for i, e in enumerate(ev):
        t = e.get("type")
        if t == "thought":
            thought = e
            continue
        mine = f" [thinks: {thought['text']}]" if thought and thought["name"] == e.get("name") else ""
        if t in ("phase", "gm", "ghost", "note", "votes", "death", "say", "whisper"):
            thought = None
        if t == "phase":
            lines.append(f"[{i}] ===== {e['text'].upper()} =====")
        elif t == "gm":
            lines.append(f"[{i}] HOST{' (aside)' if e.get('aside') else ''}: {e['text']}")
        elif t == "say":
            why = e.get("why", "")
            tag = f" ({why})" if why in ("last words", "confession", "before the game") else ""
            claim = f" <claims {e['claim']}>" if e.get("claim") else ""
            to = f" to {e['reply_to']}" if e.get("reply_to") else ""
            lines.append(f"[{i}] {e['name']} ({roles.get(e['name'], '?')}){to}{tag}{claim}: \"{e['text']}\"{mine}")
        elif t == "whisper":
            lines.append(f"[{i}] {e['name']} whispers to {e['to']}: \"{e['text']}\"{mine}")
        elif t == "votes":
            groups = {}
            for v in e["votes"]:
                groups.setdefault(v[1], []).append(v[0])
            tally = "; ".join(f"{k} {len(v)} ({', '.join(v)})" for k, v in sorted(groups.items(), key=lambda g: -len(g[1])))
            lines.append(f"[{i}] {'RUNOFF ' if e.get('runoff') else ''}VOTE: {tally}")
        elif t == "death":
            card = f"card turned: {e['role'].upper()}" if e.get("role") else "card stays face down"
            lines.append(f"[{i}] OUT: {e['name']} ({'voted out' if e.get('how') == 'vote' else 'killed in the night'}), {card}")
        elif t == "ghost" and re.search(r"[A-Za-z]{2}", e["text"]):
            lines.append(f"[{i}] {e['name']} (dead, to the audience only): \"{e['text']}\"")
        elif t == "note":
            lines.append(f"[{i}] NOTE left by {e['name']}: \"{e['text']}\"")
        elif t == "recap":
            lines.append(f"[{i}] RECAP (end card): {e['text']}")
        elif t == "end":
            lines.append(f"[{i}] END: the {'town' if e['winner'] == 'town' else 'killers'} win.")
    return "\n".join(head + lines)


def content(text):
    return {w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP and len(w) > 2}


def signals(ev):
    """Cheap measures, no model."""
    cast = next(e for e in ev if e.get("type") == "cast")
    roles = {p["name"]: p["role"] for p in cast["players"]}
    hidden = next((p["name"] for p in cast["players"] if p["role"] == "killer" and not p.get("shown")), None)
    alive, day, shifts, leans, leader = set(roles), 0, [], {}, None
    margins, wrong, claims, said, words, repeats, phase = [], 0, {}, {}, [], 0, ""
    for e in ev:
        t = e.get("type")
        if t == "phase":
            phase = e.get("kind", "")
            if phase == "day":
                day += 1
                shifts.append(0)
                leans, leader = {}, None
        elif t == "say" and phase == "day" and e.get("why") not in ("last words", "confession", "before the game"):
            words.append(len(e["text"].split()))
            cw, mine = content(e["text"]), said.setdefault((day, e["name"]), set())
            repeats += len(cw) >= 3 and len(cw & mine) / len(cw) >= 0.6   # mostly words this speaker already used today
            mine |= cw
            if e.get("lean") and e["lean"] != "none":
                leans[e["name"]] = e["lean"]
                counts = {}
                for v in leans.values():
                    counts[v] = counts.get(v, 0) + 1
                top = sorted(counts.items(), key=lambda c: -c[1])
                now = top[0][0] if top[0][1] >= 2 and (len(top) == 1 or top[1][1] < top[0][1]) else None
                if now and leader and now != leader:
                    shifts[-1] += 1
                leader = now or leader
        if t == "say" and e.get("claim") and e.get("why") not in ("confession", "before the game"):
            claims.setdefault(e["claim"], set()).add(e["name"])
        elif t == "votes":
            counts = sorted((sum(1 for v in e["votes"] if v[1] == n) for n in {v[1] for v in e["votes"]}), reverse=True)
            margins.append(counts[0] - (counts[1] if len(counts) > 1 else 0))
        elif t == "death":
            alive.discard(e["name"])
            wrong += e.get("how") == "vote" and roles.get(e["name"]) != "killer"
    end = next(e for e in ev if e.get("type") == "end")
    return {"days": day, "lean_shifts_per_day": round(sum(shifts) / max(1, day), 2), "lean_shifts": shifts,
            "vote_margin_mean": round(sum(margins) / max(1, len(margins)), 2), "vote_margin_min": min(margins or [0]),
            "counter_claims": sum(len(v) - 1 for v in claims.values()), "wrong_voteouts": wrong,
            "repeat_share": round(repeats / max(1, len(words)), 3),
            "words_per_line": round(sum(words) / max(1, len(words)), 1), "day_lines": len(words),
            "hidden_survived": hidden in alive, "winner": end["winner"], "minutes": round(end.get("t", 0) / 60, 1)}


def prompt(text):
    rubric = "\n".join(f"- {k} ({n}): 1 = {a}; 3 = {b}; 5 = {c}." for k, n, a, b, c in RUBRIC)
    return f"""You judge how fun a recorded game of Palermo (Mafia/Werewolf) is to WATCH. Seven AI players; two are killers.
The viewer sees every role and each speaker's private thought in brackets (dramatic irony, like The Traitors).
Lines numbered [n] are event indexes. Lines marked confession and the RECAP come after the game ends.
Judge the game as entertainment for a stranger who likes these games, not the quality of play: a blunder can be
the best moment. Length is not merit: a short game can score 5s, a long one 1s. Use the whole 1-5 scale.

RUBRIC (score each 1-5; 2 and 4 lie between the anchors):
{rubric}

Reply with ONE JSON object and nothing else:
{{"criteria": {{{", ".join(f'"{k}": {{"score": 1-5, "evidence": "<short quote from the transcript, under 20 words>"}}' for k in KEYS)}}},
 "score": <0-100: would a stranger who likes these games keep watching to the end and tell a friend?>,
 "moments": [{{"at": <event index>, "text": "<one line: why it is a great moment>"}}] (up to 3, best first),
 "dull": [{{"from": <index>, "to": <index>, "why": "<reason>"}}] (up to 3 dull stretches; [] if none),
 "why": "<one sentence verdict>"}}

TRANSCRIPT
{text}
"""


def validate(raw, indexes):
    """Parsed, checked judge reply; ValueError if unusable. Moments/dull pointing outside the game are dropped."""
    m = re.search(r"\{.*\}", raw or "", re.S)
    if not m:
        raise ValueError("no JSON object")
    d = json.loads(m.group(0))
    crit = {}
    for k in KEYS:
        c = d.get("criteria", {}).get(k)
        if not isinstance(c, dict) or not isinstance(c.get("score"), (int, float)) or not 1 <= c["score"] <= 5:
            raise ValueError(f"criterion {k} missing or out of range")
        crit[k] = {"score": int(round(c["score"])), "evidence": str(c.get("evidence", ""))[:200]}
    if not isinstance(d.get("score"), (int, float)) or not 0 <= d["score"] <= 100:
        raise ValueError("score missing or out of range")
    ok = lambda n: isinstance(n, int) and n in indexes
    moments = [{"at": x["at"], "text": str(x.get("text", ""))} for x in d.get("moments") or []
               if isinstance(x, dict) and ok(x.get("at"))][:3]
    dull = [{"from": x["from"], "to": x["to"], "why": str(x.get("why", ""))} for x in d.get("dull") or []
            if isinstance(x, dict) and ok(x.get("from")) and ok(x.get("to")) and x["from"] <= x["to"]][:3]
    return {"score": round(float(d["score"])), "why": str(d.get("why", "")), "moments": moments, "dull": dull,
            "criteria": crit}


def codex(model, text, effort="medium"):
    """Same call as game.call() for the codex backend, with a longer timeout for a whole transcript."""
    cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
           "-c", f'model_reasoning_effort="{effort}"', "-c", 'model_verbosity="low"', "-c", "project_doc_max_bytes=0",
           "-m", model, "-"]
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}
    r = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=600, cwd=tempfile.gettempdir(), env=env)
    if re.search(r"usage limit|hit your limit", r.stderr + r.stdout, re.I):
        sys.exit("codex is out of quota")
    return r.stdout.strip()


def judge_one(model, text, indexes, ask=codex):
    note = ""
    for attempt in range(2):  # one retry on bad JSON, told what was wrong
        try:
            return validate(ask(model, prompt(text) + note), indexes)
        except (ValueError, subprocess.SubprocessError) as e:
            err = e
            note = (f"\nYOUR LAST REPLY WAS NOT USABLE ({e}). Reply with valid JSON only; inside strings use single "
                    "quotes, never unescaped double quotes.\n")
    raise RuntimeError(f"{model}: {err}")


def combine(name, judges, sig):
    """The file the viewer reads: means over judges, the first judge's moments, dull stretches and evidence."""
    first = next(iter(judges.values()))
    crit = {k: {"score": round(sum(j["criteria"][k]["score"] for j in judges.values()) / len(judges), 2),
                "evidence": first["criteria"][k]["evidence"]} for k in KEYS}
    return {"name": name, "score": round(sum(j["score"] for j in judges.values()) / len(judges), 1), "why": first["why"],
            "moments": first["moments"], "dull": first["dull"], "criteria": crit, "judges": judges, "signals": sig}


def score_game(path, models, force=False):
    name = os.path.basename(path)[:-5]
    ev = json.load(open(path))
    if not finished(ev):
        return None
    out = os.path.join(OUT, name + ".json")
    old = json.load(open(out)).get("judges", {}) if os.path.exists(out) else {}
    text, judges = render(ev), {}
    indexes = {int(n) for n in re.findall(r"^\[(\d+)\]", text, re.M)}
    for m in models:
        judges[m] = old[m] if m in old and not force else judge_one(m, text, indexes)
    keep = {m: j for m, j in old.items() if m not in judges}  # other judges' cached results stay
    res = combine(name, {**judges, **keep}, signals(ev))
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(out, "w"), indent=1)
    return res


def ranks(xs):
    s = sorted(xs)
    return [s.index(x) + (s.count(x) - 1) / 2 for x in xs]  # ties share the mean rank


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sa = sum((x - ma) ** 2 for x in a) ** .5
    sb = sum((y - mb) ** 2 for y in b) ** .5
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sa * sb) if sa and sb else float("nan")


def spearman(a, b):
    return pearson(ranks(a), ranks(b))


def report(results, models):
    print("\n## Report")
    for i, a in enumerate(models):
        for b in models[i + 1:]:
            both = [r for r in results if a in r["judges"] and b in r["judges"]]
            if len(both) > 2:
                xa, xb = [r["judges"][a]["score"] for r in both], [r["judges"][b]["score"] for r in both]
                gap = sum(abs(x - y) for x, y in zip(xa, xb)) / len(both)
                print(f"judges {a} vs {b}: Spearman {spearman(xa, xb):.2f}, mean |diff| {gap:.1f} points, n={len(both)}")
                for k in KEYS:
                    ca = [r["judges"][a]["criteria"][k]["score"] for r in both]
                    cb = [r["judges"][b]["criteria"][k]["score"] for r in both]
                    print(f"   {k:<10} Spearman {spearman(ca, cb):5.2f}")
    score = [r["score"] for r in results]
    print("signal or criterion vs score (Spearman, all games):")
    for k in ["days", "minutes", "day_lines", "lean_shifts_per_day", "vote_margin_mean", "counter_claims",
              "wrong_voteouts", "repeat_share", "words_per_line", "hidden_survived"]:
        print(f"   {k:<20} {spearman([float(r['signals'][k]) for r in results], score):5.2f}")
    for k in KEYS:
        print(f"   {k:<20} {spearman([r['criteria'][k]['score'] for r in results], score):5.2f}"
              f"   mean {sum(r['criteria'][k]['score'] for r in results) / len(results):.2f}")


def main(argv):
    force, rep = "--force" in argv, "--report" in argv
    models, jobs, args = ["gpt-6-sol"], 4, []
    it = iter(argv)
    for a in it:
        if a in ("--judge", "--judges"):
            models = next(it).split(",")
        elif a == "--jobs":
            jobs = int(next(it))
        elif not a.startswith("--"):
            args.append(a)
    if not args:
        sys.exit(__doc__)
    files = paths(args)
    with concurrent.futures.ThreadPoolExecutor(jobs) as pool:
        futs = {f: pool.submit(score_game, f, models, force) for f in files}
    results, groups = [], {}
    for f, fut in futs.items():
        try:
            r = fut.result()
        except RuntimeError as e:
            print(f"{os.path.basename(f)}: judge failed ({e})")
            continue
        if r:
            results.append(r)
            groups.setdefault(re.sub(r"-\d+$", "", r["name"]), []).append(r)
    for tag, rs in groups.items():
        print(f"\n## {tag}\n| game | score | top | bottom | why |\n|---|---|---|---|---|")
        for r in rs:
            c = sorted(KEYS, key=lambda k: r["criteria"][k]["score"])
            print(f"| {r['name']} | {r['score']:.0f} | {c[-1]} {r['criteria'][c[-1]]['score']:g} | "
                  f"{c[0]} {r['criteria'][c[0]]['score']:g} | {r['why']} |")
    print("\n## Evening means")
    for tag, rs in groups.items():
        print(f"{tag:<8} {sum(r['score'] for r in rs) / len(rs):5.1f}  (n={len(rs)})")
    if rep and len(results) > 2:
        report(results, models)


if __name__ == "__main__":
    main(sys.argv[1:])
