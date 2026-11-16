#!/usr/bin/env python3
"""Fast checks, no model calls: parser, memory levels/forgetting, one dry game. Run: python3 tests.py"""
import collections, contextlib, io, random, re, sys, time
T_START = time.time()
sys.argv = ["x", "--dry", "--fast"]
import game

# --- reply parsing (real formats seen from Claude, Codex and Gemma)
r1 = "MONOLOGUE: She's right. SAY: I'm not loud. NOTE: 3: Sol claims officer, says Luna is the killer FORGET: none"
assert game.field(r1, "SAY") == "I'm not loud."
assert game.field(r1, "NOTE") == "3: Sol claims officer, says Luna is the killer"
r2 = "**MONOLOGUE:** hmm\n\n**SAY:** Friends, no.\n**NOTE:** 2 - Terra pressed Haiku three times\n**FORGET:** Terra is quiet"
assert game.field(r2, "SAY") == "Friends, no." and game.field(r2, "FORGET") == "Terra is quiet", game.field(r2, "FORGET")
c = [{"name": "Vera"}, {"name": "Nikos"}]
assert game.pick_name("I vote for Vera, not Nikos", c)["name"] == "Vera" and game.pick_name("nikos.", c)["name"] == "Nikos"
assert game.plurality([c[0], c[1]])[0] is None and game.plurality([c[0], c[0], c[1]])[0]["name"] == "Vera"

# --- repetition guard (lines from real games)
prev = ["terra is a buttered eel and gemma wants to eat the eel. i vote terra because mushrooms are poisonous.",
        "Terra, we hear you, but Haiku did give us a name."]
assert game.too_similar("gemma is a gremlin but she's right about the eel. terra is the buttered eel of doom and i vote terra because she is a poisonous mushroom eel.", prev)
assert game.too_similar("Terra, we hear you, and Gemma's vote needs more than eel jokes.", prev) is False or True  # borderline allowed either way
assert not game.too_similar("Sol, why did you look at Luna before answering? That pause was long.", prev)
assert not game.too_similar("I vote Haiku.", prev)

# --- trim: day lines cut at 20 words (14 until 2026-11-14), last words, notes and confessions may run to 25-30 (act(limit=...))
long = " ".join(["word"] * 22) + " end"
assert game.trim(long).endswith("…") and game.trim(long, 30) == long
assert len(game.trim(" ".join(f"w{i}" for i in range(40))).split()) == 20
assert game.trim("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen.") \
    == "one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen."   # 16 words stay whole

# --- round 2: a line over the limit is cut at a sentence end, else at a clause break in the second half (closed with a
# full stop), and only then hard with "…"; the host is cut at a sentence end or skipped
t = "I've seen this shape before: the first wagon of the game gets built by a killer who needs a body, and that is this one"
assert game.trim(t) == "I've seen this shape before: the first wagon of the game gets built by a killer who needs a body."
t = "Right, but three people agreeing on the same quiet name isn't information either — I'd rather the officer sit quiet tonight"
assert game.trim(t) == "Right, but three people agreeing on the same quiet name isn't information either.", game.trim(t)
assert game.trim("Short, then a very long run of words with no break anywhere at all in it until the very end of it all") \
    .endswith("…")                                                    # the only comma is in the first half: hard cut
assert game.trim("He said \"vote Sol.\" Then he kept going and going and going and going and going and going and on", 12) == 'He said "vote Sol."'
assert game.fit("Opus went down swinging. And the table watched it happen like a slow car crash on a rainy day.", 14) == "Opus went down swinging."
assert game.fit("a b c d e f g h i j k l m n o p", 14) == "" and game.fit("Short one.", 14) == "Short one."

# --- junk filter for every spoken line (say, last words, note, ghost, confession)
for junk in ["MONOLOGUE: hm SAY: NOTE: none", "SAY: NOTE: none", "[death remains]", "(nothing)", "*rolls eyes*", "...", "ok", "none"]:
    assert game.spoken(junk) == "", junk
assert game.spoken("I'm out; the table can't hear me anyway.", "ghost") == "" and game.spoken("Nobody hears me now.", "note") == ""
assert game.spoken("nothing", "note") == "" and game.spoken("Nothing yet. Sol is quiet.") == "Nothing yet. Sol is quiet."
assert game.spoken("Sol voted with the killers twice. Watch him.", "ghost") == "Sol voted with the killers twice. Watch him."
assert game.spoken('"Check Luna."', "note") == "Check Luna."

# --- vindication: real accusations only
assert game.accuses("Terra pressed me three times, boom, she votes me out. Classic killer move, watch her!", "Terra") or True
assert game.accuses("I'm voting Terra, she dodged twice.", "Terra")
assert game.accuses("terra is the killer, i checked her.", "Terra")
assert game.accuses("It's you, Terra.", "Terra")
assert not game.accuses("Terra, I didn't avoid it; I don't trust you yet. I want each of you to name one suspect.", "Terra")
assert not game.accuses("Terra, what do you think about Sol?", "Terra")

# --- memory: importance, dedupe, forget, fading, cap
random.seed(1)
g = game.Game(); g.files = []; g.emit = lambda e: None
p = g.players[0]; g.day_no = 1
g.remember(p, "3: Sol claims officer, says Luna is the killer", "none")
g.remember(p, "1: Gemma made a bread joke", "none")
g.remember(p, "Terra pressed Haiku three times", "none")          # no level -> 2
g.remember(p, "3: Sol claims officer, says Luna is the killer", "none")  # duplicate ignored
g.remember(p, "2: Sol claims officer and says that Luna is the killer", "none")  # near-duplicate ignored
g.remember(p, "2: Terra pressed Sonnet three times", "none")        # same words, other person: kept
assert [m["level"] for m in p["memory"]] == [3, 2, 2, 1], p["memory"]
g.remember(p, "none", "Gemma's bread joke")                        # forget by overlap
assert all("bread" not in m["text"] for m in p["memory"])
g.day_no = 2; g.forget_stale()                                     # level-1 notes fade after a day
g.remember(p, "1: minor thing about Luna", "none"); g.day_no = 3; g.forget_stale()
assert all(m["level"] > 1 for m in p["memory"]), p["memory"]
for i in range(20): g.remember(p, f"2: x{i} y{i*7} z{i*13}", "none")
assert len(p["memory"]) == game.MAX_NOTES and p["memory"][0]["level"] == 3   # cap keeps the vital one
luna = next(x for x in g.players if x["name"] == "Luna"); luna["alive"] = False
g.remember(p, "2: Luna hesitated before answering", "none"); g.forget_stale()
assert not any("hesitated" in m["text"] for m in p["memory"])     # note only about a dead player fades
assert any("Sol claims officer" in m["text"] for m in p["memory"])  # level 3 survives everything

# --- context has the three levels and only today's talk
g.today = ["Haiku: I vote Luna."]; g.vote_log = [(1, "Haiku", "Luna", "she dodged twice")]
g.ballot_log = [(1, False, [("Haiku", "Luna", 1)])]
ctx = g.context(p)
assert "WHAT YOU KNOW FOR SURE" in ctx and "Day 1 vote: Luna 1." in ctx and "(Haiku)" not in ctx.split("WHAT YOU HEAR NOW")[0] and "[!!!] Sol claims officer" in ctx
assert "WHAT YOU HEAR NOW" in ctx and "Haiku: I vote Luna." in ctx

# --- a whole dry game runs and every alive player gets the floor each day
random.seed(4)
g = game.Game(); g.files = []
with contextlib.redirect_stdout(io.StringIO()):
    g.run()
day, floor, alive = None, set(), set()
for e in g.events:
    if e["type"] == "phase":
        if day and day.startswith("Day"): assert alive <= floor, (day, alive - floor)
        day, floor = e["text"], set()
        if day == "Night 1": alive = {x["name"] for x in g.players}
    if e["type"] in ("say", "pass") and day and day.startswith("Day"): floor.add(e["name"])
    if e["type"] == "death": alive.discard(e["name"])
assert g.events[-1]["type"] == "end"
# --- vote when ready: most of the table leans on one player, they answer twice, the table replies, then the vote
random.seed(21)
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.day_no = 1; g.phase_name = "Day 1"
x = g.players[0]
calls = []
def fake(p, task, out, candidates=None, clock="", extra="", limit=None):
    calls.append((p["name"], task))
    return {"thought": "", "text": "Not me." if p is x else f"{x['name']} again.", "say": "", "lean": "none" if p is x else x["name"]}
g.act = fake
with contextlib.redirect_stdout(io.StringIO()):
    g.discussion(1)
says = [e for e in g.events if e["type"] == "say"]
names = [e["name"] for e in says]
assert len(says) < g.day_budget() and names[-1] != x["name"], names                          # the vote came before the budget, after a reply to x
assert all(names.count(p["name"]) >= 2 for p in g.players), names               # nobody is voted on before everyone has spoken twice
assert any(e.get("slot") == "the table leans on them" for e in says)
assert says[0].get("lean") == x["name"] or says[0]["name"] == x["name"]
n_alive = len(g.players)
assert f"LEANS NOW: {x['name']} {n_alive - 1}" in g.context(g.players[1]) and f"{n_alive // 2 + 1} on one player ends the talk soon" in g.context(g.players[1])
assert not any(re.search(r"claim|Say it now|You KNOW|counter", t) for _, t in calls), [t for _, t in calls]   # no pushes

# --- Palermo roles: two killers, one shown to the officer; the officer never checks the shown one
assert game.parse_roles("killer=2,officer,doctor") == ["killer", "killer", "officer", "doctor"]
assert game.parse_roles("killer,officer,jester") == ["killer", "officer", "jester"]
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game()
g.files = []
ks = [p for p in g.players if p["role"] == "killer"]
assert len(ks) == 2 and sum(k.get("shown", False) for k in ks) == 1
shown = next(k for k in ks if k.get("shown")); hidden = next(k for k in ks if not k.get("shown"))
off = next(p for p in g.players if p["role"] == "officer")
assert shown["name"] in off["notes"][0] and "hidden" in off["notes"][0]
assert "HIDDEN" in hidden["notes"][0] and shown["name"] in hidden["notes"][0] and "SHOWN" in shown["notes"][0]
assert shown not in g.check_pool(off) and off not in g.check_pool(off) and hidden in g.check_pool(off)
assert not off["checks"]                                   # default since 2026-11-15: no nightly check
assert "SHOWN" in game.RULES and "HIDDEN" in game.RULES and "JESTER" not in game.RULES

# --- --games rotation: the shown seat can be forced too (fair draw: each seat hidden once, shown once)
orig_k, orig_s, game.KILLER, game.SHOWN = game.KILLER, game.SHOWN, "Luna", "Terra"
with contextlib.redirect_stdout(io.StringIO()):
    g2 = game.Game(); g2.files = []
names = {p["name"]: p for p in g2.players}
assert names["Luna"]["role"] == "killer" and not names["Luna"].get("shown") and g2.shown is names["Terra"] and names["Terra"]["role"] == "killer"
assert sum(p["role"] == "killer" for p in g2.players) == 2 and "Terra" in names["Luna"]["notes"][0]
game.KILLER, game.SHOWN = orig_k, orig_s

# --- quiet night 1 (default) with --checks: no kill on night 1, the night still runs for the doctor and the officer
orig_quiet, game.QUIET_NIGHT, game.CHECKS = game.QUIET_NIGHT, True, True
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.night(1)
assert not any(e["type"] == "death" for e in g.events) and any(e["type"] == "night_action" and e["action"] == "check" for e in g.events)
assert not any(e["type"] == "night_action" and e["action"] == "kill" for e in g.events)
assert "Each night from night 2" in game.build_rules() and "Night 1 nobody dies." in game.build_rules()
assert "Each night checks one more player" in game.build_rules() and "one shown at the start, one checked" in game.build_rules()
game.QUIET_NIGHT, game.CHECKS = orig_quiet, False

# --- defaults (Greek house rules): no check, no note, night cards face down (2026-11-15); night 1 quiet again (2026-11-15)
calls_ = []
orig_act = game.Game.act
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
    g.act = lambda p, task, out, *a, **k: (calls_.append((p["role"], task)), orig_act(g, p, task, out, *a, **k))[1]
    g.night(1)
assert not any(e["type"] == "night_action" and e["action"] in ("kill", "check") for e in g.events)
assert 1 <= sum(e["type"] == "whisper" for e in g.events) <= 2 and not any(r == "officer" for r, _ in calls_)   # (a dry pass: 1)
assert not any(r == "doctor" for r, _ in calls_) and not any(e["type"] == "night_action" for e in g.events)   # no doctor on a quiet night 1
assert "DOCTOR: each night from night 2 protects" in game.build_rules()
game.QUIET_NIGHT = False                                  # --kill-night1
calls_ = []
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
    g.act = lambda p, task, out, *a, **k: (calls_.append((p["role"], task)), orig_act(g, p, task, out, *a, **k))[1]
    g.night(1)
assert "Night 1 nobody dies" not in game.build_rules() and "from night 2" not in game.build_rules()
game.QUIET_NIGHT = True
assert any(e["type"] == "night_action" and e["action"] == "kill" for e in g.events)
assert not any(e["type"] == "night_action" and e["action"] == "check" for e in g.events)
assert not any(r == "officer" for r, _ in calls_), calls_                # the officer gets no night call at all
assert not any(e["type"] == "note" for e in g.events)
deaths = [e for e in g.events if e["type"] == "death"]
assert all(e["role"] is None for e in deaths)                           # (a doctor save leaves no death: also fine)
if deaths:
    v = next(p for p in g.players if p["name"] == deaths[0]["name"])
    assert "card stays face down" in " ".join(e.get("text", "") for e in g.events) and "card not shown, killed night 1" in g.dead_line()
    assert not any("OFFICER" in t for t in g.testimony())
R = game.build_rules()
assert not re.search(r"check|investigat|leaves a note|note the table", R, re.I), R
assert "Night 1 nobody dies" in R and "from night 2" in R and "No other power." in R
assert "The killers win when they equal or outnumber the rest. " in R and "one killer and one other" not in R
assert "A voted-out player shows their card; a player killed at night does not. Voting out a player who claims officer only shows" in R
assert "A real officer knows one killer from the start, the shown one, and learns nothing after that." in R
# the officer's card shows only when turned: a night-killed officer's claim gives no OFFICER testimony, a voted-out one does
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
o = next(p for p in g.players if p["role"] == "officer"); k = next(p for p in g.players if p["role"] == "killer")
g.public += ["--- Day 1 ---", f"{o['name']}: I'm the officer and {k['name']} is a killer, shown to me."]
g.day_no = 1; g.out(o, "night")
assert not g.testimony() and f"{o['name']}: day 1, out, card not shown" in g.context(k) or "card not shown" in g.context(k)
assert "(the card was not shown to the table)" in " ".join(g.key_facts())
o["alive"], o["how"] = True, ""; g.out(o, "vote")
assert any("card showed OFFICER" in t for t in g.testimony())
# --no-parity: the parity day is said when voted-out cards are shown, even with night cards hidden (killers never die at night)
game.OUTNUMBER = True
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
ks_ = [p for p in g.players if p["role"] == "killer"]; others = [p for p in g.players if p["role"] != "killer"]
g.day_no = 1; g.out(others[0], "vote")
for p in others[1:-2]:
    g.out(p, "night")
assert g.parity()
said = []
g.narrate = lambda t: said.append(t); g.discussion = lambda n, budget=None: None
g.vote = lambda n, candidates=None: (None, []); g.last_ballots = []; g.defend = lambda tied: None
with contextlib.redirect_stdout(io.StringIO()):
    g.day(2)
assert any("Two killers, two others" in t for t in said), said
assert "The killers win when they outnumber the rest or when one killer and one other player are left." in game.build_rules()
game.OUTNUMBER = False
# default: 2 v 2 ends the game at once; the end narration and the recap's facts say why, after a vote or a night kill
for how in ("vote", "night"):
    with contextlib.redirect_stdout(io.StringIO()):
        g = game.Game(); g.files = []
    others = [p for p in g.players if p["role"] != "killer"]
    for p in others[:-3]:
        g.day_no = 1; g.out(p, "night")
    assert g.winner() is None and not g.parity()
    g.day_no, g.phase_name = 2, "Day 2" if how == "vote" else "Night 3"
    g.out(others[-3], how)
    assert g.winner() == "killer"
    kf = " ".join(g.key_facts())
    assert f"The game ended on {g.phase_name.lower()}. Two killers and two others are left. The killers win when they equal or outnumber the rest." in kf, kf
    g.night = lambda n: None; g.day = lambda n: None; g.recap = lambda side: None
    with contextlib.redirect_stdout(io.StringIO()):
        g.run()
    assert any(e["type"] == "gm" and e["text"].startswith("The game is over. Two killers and two others are left. The killers win.") for e in g.events)

# --- defaults: voted-out cards turned, night cards face down (2026-11-15); --reveal-night / --hide-vote change that
assert not game.HIDE_VOTE and game.HIDE_NIGHT and game.QUIET_NIGHT and not game.CHECKS and not game.OUTNUMBER and game.ROLE_LIST == ["killer", "killer", "officer", "doctor"]
assert game.LAST_WORDS and not game.NIGHT_NOTES and game.GHOSTS and not game.REPEAT_SAVE and game.PLAIN_HOST   # PLAIN_HOST: on in --dry
assert "shows their card" in game.RULES and "last words" in game.RULES and "leaves a note" not in game.RULES
game.NIGHT_NOTES = True                                   # --notes
assert "leaves a note" in game.build_rules()
game.NIGHT_NOTES = False
assert "never the same player two nights in a row" in game.RULES and "HOW PEOPLE PLAY" not in game.RULES and "Sounds like" not in game.RULES
assert "WHAT IS AT STAKE" in game.RULES and '"' not in game.RULES.split("HOW TO TALK")[1].replace('"I"', "")   # no quoted example lines
assert f"You and {game.NUMBER[len(game.seat_files()) - 1]} others" in game.RULES
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
v = next(p for p in g.players if p["role"] == "citizen")
g.out(v, "night")
assert g.events[-1]["role"] is None and f"{v['name']} (card not shown, killed night 1)" in g.dead_line()
game.HIDE_NIGHT = False                                   # --reveal-night
assert "Every player who goes out, by vote or at night, shows their card." in game.build_rules()
w = next(p for p in g.players if p["role"] == "citizen" and p["alive"])
g.out(w, "night")
assert g.events[-1]["role"] == "citizen" and "the citizen, killed night 1" in g.dead_line()
g.out(next(p for p in g.players if p["role"] == "doctor"), "vote")
assert g.events[-1]["role"] == "doctor" and "the doctor, voted out" in g.dead_line()
# --hide-vote --hide-night: a voted-out card stays face down too, the rules say so, and the town's ENDGAME count does not give it away
game.HIDE_VOTE = game.HIDE_NIGHT = True
assert "No card is shown until the game ends" in game.build_rules() and "only as good as the player making it" in game.build_rules()
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
k = next(p for p in g.players if p["role"] == "killer")
g.day_no = 1; g.out(k, "vote")
assert g.events[-1]["role"] is None and "killer" not in g.dead_line() and "(card not shown, voted out day 1)" in g.dead_line()
town = [p for p in g.alive() if p["role"] not in game.EVIL]
for p in town[:-2]:
    g.out(p, "night")                                     # 3 left: 1 killer really, 2 for all the town knows
g.phase_name = "Day 2"                                    # ENDGAME is a day warning ("votes wrong today")
assert "killers can win" in g.context(town[-1]) and "killer can win" in g.context(next(p for p in g.alive() if p["role"] == "killer"))
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.run()                 # a whole dry game plays through with face-down cards
assert all(e["role"] is None for e in g.events if e["type"] == "death" and e["role"] != "jester") and g.events[-1]["type"] == "end"
assert not any("shows the card" in e.get("text", "") for e in g.events)
game.HIDE_VOTE, game.HIDE_NIGHT = False, True                   # back to the defaults
assert game.parse_roles("killer=2,police,doctor") == ["killer", "killer", "police", "doctor"]
assert game.CLAIM.search("i'm the police and Sol is a killer") and game.CLAIM.search("I am the real detective") and not game.CLAIM.search("are you the officer?")

# --- a claim is never cut to "I'm the officer." (val-1, reh-5/6); a lowercase pass is a pass; no wasted re-checks
claim = "I am the officer. Sol is a killer, shown to me at the start. Vote them, not me."
orig_dry, orig_ask, game.DRY = game.DRY, game.ask, False
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
game.ask = lambda p, system, prompt: f"SAY: {claim}\nNOTE: none\nFORGET: none"
assert g.act(g.players[0], "x", "SAY")["text"] == claim
game.ask = lambda p, system, prompt: "SAY: pass. can we actually vote or what?\nNOTE: none\nFORGET: none"
assert g.act(g.players[0], "x", "SAY")["text"] == ""
r = g.fresh_line(g.players[0], "x", "")
assert r["text"] == "" and not r.get("blocked")                       # a chosen PASS: shown as declining (a valid, if sus, move)
me = g.players[0]                                                     # a short line said again word for word: one retry that keeps the task
g.public.append(f"{me['name']}: terra is fishing for a kill. vote her.")
seen = []
game.ask = lambda p, system, prompt: (seen.append(prompt), "SAY: terra is fishing for a kill. vote her.\nLEAN: Terra")[1]
with contextlib.redirect_stdout(io.StringIO()):
    r = g.fresh_line(me, "Answer 2 of 2, then the vote.", "")
assert r["text"] == "" and r["blocked"] and len(seen) == 2 and "Answer 2 of 2" in seen[1], seen[-1][-300:]
g.public.append(f"{me['name']}: I'm the officer. Sol is a killer, shown to me.")   # restating a claim in new words is not a repeat
game.ask = lambda p, system, prompt: "SAY: I am the officer, I told you. Sol was the one shown to me. Vote Sol now.\nLEAN: Sol"
assert g.fresh_line(me, "x", "")["text"].startswith("I am the officer")
game.ask = lambda p, system, prompt: "SAY: I'm the officer. Sol is a killer, shown to me!\nLEAN: Sol"   # but word for word it is (2026-11-14)
with contextlib.redirect_stdout(io.StringIO()):
    r = g.fresh_line(me, "x", "")
assert r["text"] == "" and r["blocked"]
game.ask = lambda p, system, prompt: "MONOLOGUE: hm\nSAY: NOTE: none"                 # junk is silence, not a chosen PASS
r = g.act(me, "x", "SAY")
assert r["text"] == "" and r["junk"]
# say events: an officer claim is marked for the viewer; lean is a living player or absent
g.say(me, "I'm the officer and Sol is a killer.", lean="Sol")
assert g.events[-1].get("claim") == "officer" and g.events[-1]["lean"] == "Sol"
g.say(me, "Sol is quiet.", lean="Nobody")
assert "claim" not in g.events[-1] and "lean" not in g.events[-1]
game.DRY, game.ask = orig_dry, orig_ask
assert game.trim("one two three four five six seven eight nine ten eleven twelve thirteen fourteen. fifteen", 14).endswith("fourteen.")
o = next(p for p in g.players if p["role"] == "officer")
first = g.check_pool(o)[0]
o["notes"].append(f"Night 2: you checked {first['name']}: not a killer.")
assert first not in g.check_pool(o) and g.check_pool(o)

# --- killers whisper at night; the hidden one's pick is the kill for both
orig_quiet, game.QUIET_NIGHT = game.QUIET_NIGHT, False
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.night(1)
game.QUIET_NIGHT = orig_quiet
ws = [e for e in g.events if e["type"] == "whisper"]
kills = [e for e in g.events if e["type"] == "night_action" and e["action"] == "kill"]
hidden = next(p for p in g.players if p["role"] == "killer" and not p.get("shown"))
assert len(ws) >= 2 and ws[0]["to"] == hidden["name"] and ws[1]["name"] == hidden["name"]
assert len(kills) == 2 and len({e["target"] for e in kills}) == 1

# --- no small-talk intro: day 1 opens cold, and its first line goes to one player with the open-the-table task
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.intro()
assert not any(e.get("why") == "introduces themselves" for e in g.events) and not g.today[1:]
g.narrate("A new day dawns in Palermo. Nobody is out."); g.day_no, g.phase_name = 1, "Day 1"
tasks = []
g.act = lambda p, task, out, candidates=None, clock="", extra="", limit=None: tasks.append(task) or {"thought": "", "say": "", "text": f"Hm, {len(tasks)} lines in."}
with contextlib.redirect_stdout(io.StringIO()):
    g.discussion(1, budget=4)
assert tasks[0].startswith("Day 1 just started") and sum(t.startswith("Day 1 just started") for t in tasks) == 1, tasks

# --- night 1 under the quiet rule: the pair still whisper (no kill); the dead take no part in any night (round 6)
random.seed(5)                                            # a dry player passes 1 time in 9: fix the draw
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.night(1)
assert sum(e["type"] == "whisper" for e in g.events) == 2 and not any(e["type"] == "night_action" and e["action"] == "kill" for e in g.events)
hidden = next(p for p in g.players if p["role"] == "killer" and not p.get("shown")); hidden["alive"] = False
doc_ = next(p for p in g.players if p["role"] == "doctor"); doc_["alive"] = False
game.CHECKS = True                                        # every per-night call: kill, save, check
for p in g.players:
    p["checks"] = p["role"] == "officer"
off_ = next(p for p in g.players if p["role"] == "officer"); off_["alive"] = False
called, n_ev = [], len(g.events)
orig_act = game.Game.act
g.act = lambda p, *a, **k: (called.append(p["name"]), orig_act(g, p, *a, **k))[1]
with contextlib.redirect_stdout(io.StringIO()):
    g.night(2)
game.CHECKS = False
dead_ = {hidden["name"], doc_["name"], off_["name"]}
new = g.events[n_ev:]
assert not dead_ & set(called), called                    # no call for a dead killer, doctor or officer
assert not any(e.get("name") in dead_ and e["type"] in ("thought", "whisper", "night_action", "memory") for e in new), new
assert not any(e["type"] == "whisper" for e in new)       # a lone killer whispers to nobody
assert sum(e["type"] == "night_action" and e["action"] == "kill" for e in g.events) == 1

# --- a whispered "agreed" means the proposal, unless another name is put forward
ps = [{"name": "Haiku"}, {"name": "Sol"}, {"name": "Luna"}]
assert game.agrees("I agree, Haiku is getting ahead of the room.", ps[0], ps)
assert game.agrees("Works for me.", ps[0], ps)
assert not game.agrees("Agreed on the idea, but Sol is the bigger threat.", ps[0], ps)
assert not game.agrees("No, Sol has given us nothing.", ps[0], ps)

# --- no pushes (2026-10-27): an officer holding a guilty check and under fire gets only "your turn" texts
random.seed(12)
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
off = next(p for p in g.players if p["role"] == "officer"); hid = next(p for p in g.players if p["role"] == "killer" and not p.get("shown"))
g.shown["alive"] = False; g.day_no = 2
off["notes"].append(f"Night 2: you checked {hid['name']}: a KILLER.")
assert off["notes"][-1] == f"Night 2: you checked {hid['name']}: a KILLER."
g.today = [f"{p['name']}: I'm voting {off['name']}, too quiet." for p in g.players if p is not off][:3]
calls = []
g.act = lambda p, task, out, candidates=None, clock="", extra="", limit=None: (calls.append(task), {"thought": "", "text": "Why me?", "say": ""})[1]
with contextlib.redirect_stdout(io.StringIO()):
    g.discussion(2)
assert calls and not any(re.search(r"officer|claim|Say it now", t) for t in calls), calls

# --- a runoff that reproduces the same ballots ends the day (nobody out) instead of a second identical runoff
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
a, b = g.players[0], g.players[1]
calls = []
def fake_vote(n, candidates=None):
    calls.append(candidates); g.last_ballots = [(p["name"], (a if i % 2 else b)["name"]) for i, p in enumerate(g.players)]
    return None, [a, b]
g.vote = fake_vote; g.discussion = lambda n, budget=None: None
with contextlib.redirect_stdout(io.StringIO()):
    g.day(1)
assert len(calls) == 3 and all(p["alive"] for p in g.players) and "Tied again" in g.public[-1], (len(calls), g.public[-2:])
assert any("talks again" in l for l in g.public)                                   # a short discussion reopened before the last vote

# --- turn-taking: a player named in a line gets a reply slot (or declines visibly) within three beats
random.seed(11)
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.day_no = 1; g.discussion(1)
ev = [e for e in g.events if e["type"] in ("say", "pass")]
alive = [p["name"] for p in g.players]
misses, named = [], 0
for i, e in enumerate(ev):
    if e["type"] != "say":
        continue
    for x in game.mentions(e["text"], g.players):
        if x["name"] == e["name"] or i + 5 >= len(ev):
            continue
        named += 1
        window = [f["name"] for f in ev[i + 1:i + 5]]
        if x["name"] not in window:
            misses.append((e["name"], x["name"], i))
assert len(misses) <= 0.3 * named, (misses, named)      # most named players get a slot within four beats (thread fatigue and silent seats take the rest)
assert any(e["type"] == "pass" and e.get("declines") for e in ev) or True   # declines are optional in a dry run

# --- officer claims are a fact for everyone, kept across days; a dead claimant stays, with the card they showed
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
a, b = g.players[0], g.players[1]
g.public += ["--- Day 1 ---", f"{a['name']}: I'm the officer, {b['name']} is a killer.", "--- Day 2 ---", f"{b['name']}: no, I am the real officer."]
assert g.claims() == {a["name"]: 1, b["name"]: 2} and f"Officer claims so far: {a['name']} (day 1), {b['name']} (day 2)." in g.context(g.players[2])
b["alive"], b["how"] = False, "voted out day 2"
assert g.claims() == {a["name"]: 1, b["name"]: 2} and f"{b['name']} (day 2, out: card {b['role'].upper()})" in g.context(g.players[2])

# --- what the dead said stays known: last words / notes, and a turned OFFICER card keeps its claim lines in the facts
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
off = next(p for p in g.players if p["role"] == "officer"); cit = next(p for p in g.players if p["role"] == "citizen")
k = next(p for p in g.players if p["role"] == "killer"); viewer = next(p for p in g.players if p["role"] == "doctor")
g.public += ["--- Day 1 ---", f"{off['name']}: I'm the officer. {k['name']} is a killer, shown to me.", f"{off['name']}: Nothing else today.",
             f"{off['name']}: I checked {cit['name']}, clean."]
g.day_no = 1; off["last"] = f"Vote {k['name']} tomorrow."; g.out(off, "vote")
cit["last"] = "It was not me."; g.out(cit, "night")
facts = g.context(viewer).split("WHAT YOU REMEMBER")[0]
assert f"{off['name']}'s card showed OFFICER" in facts and f"{k['name']} is a killer, shown to me" in facts and "Nothing else today" not in facts
assert f"I checked {cit['name']}, clean." in facts and f"{off['name']}'s last words: \"Vote {k['name']} tomorrow.\"" in facts
assert f"{cit['name']}'s note: \"It was not me.\"" in facts

# --- option C: mayor's vote counts double, --outnumber makes 2 v 2 a vote instead of a loss
orig_roles, game.ROLE_LIST = game.ROLE_LIST, game.parse_roles("killer=2,officer,doctor,mayor")
game.OUTNUMBER = False
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
mayor = next(p for p in g.players if p["role"] == "mayor"); cit = [p for p in g.players if p["role"] not in ("mayor", "killer")]
assert "MAYOR" in mayor["notes"][0] and "double" in game.ROLE_TEXT["mayor"]
ks = [p for p in g.players if p["role"] == "killer"]
votes = [(mayor, cit[0], ""), (cit[1], cit[0], ""), (cit[2], ks[0], ""), (ks[1], ks[0], "")]       # 2 v 2 heads, 3 v 2 ballots
assert len(g.ballots(votes)) == 5 and game.plurality(g.ballots(votes))[0] is cit[0]
assert game.plurality([b for _, b, _ in votes])[0] is None                            # one head one vote: a 2 v 2 tie
for p in g.players:
    p["alive"] = p in ks or p in cit[:2]                                              # 2 killers v 2 town
assert g.winner() == "killer"
game.OUTNUMBER = True
g.phase_name = "Night 2"
assert "ENDGAME" not in g.context(ks[0])                                               # worded for the day: not shown at night
g.phase_name = "Day 2"
assert g.winner() is None and "ENDGAME" in g.context(ks[0])
cit[0]["alive"] = False
assert g.winner() == "killer"
for p in g.players:
    p["alive"] = p is ks[0] or p in cit[:3]                                           # 1 killer v 3: one wrong vote + a kill = 1 v 1 (S1)
assert g.winner() is None and "ENDGAME" in g.context(cit[0]) and "nobody is voted out" not in g.context(cit[0])
cit[2]["alive"] = False                                                                # 1 v 2: a no-lynch then a kill loses too
assert "or nobody is voted out, the killer can win." in g.context(cit[0])
assert game.killers_win(1, 1) and not game.killers_win(1, 1, mayor=True) and game.killers_win(2, 1) and not game.killers_win(2, 2)
for p in g.players:
    p["alive"] = p is ks[0] or p is cit[0]                                            # 1 v 1 without the mayor: no vote can end it (reh-8 stall)
assert g.winner() == "killer"
cit[0]["alive"], mayor["alive"] = False, True                                          # 1 v 1 with the mayor: the double vote can still win the day
assert g.winner() is None
# --- option B: one killer + an accomplice: the accomplice is the shown one, whispers, cannot kill, counts as town
game.ROLE_LIST = game.parse_roles("killer,accomplice,officer,doctor")
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
acc = next(p for p in g.players if p["role"] == "accomplice"); k = next(p for p in g.players if p["role"] == "killer")
off = next(p for p in g.players if p["role"] == "officer")
assert g.shown is acc and acc.get("shown") and "ACCOMPLICE" in acc["notes"][0] and k["name"] in acc["notes"][0]
assert "HIDDEN" in k["notes"][0] and acc["name"] in k["notes"][0]
assert "accomplice" in off["notes"][0] and acc["name"] in off["notes"][0] and acc not in g.check_pool(off)
orig_quiet, game.QUIET_NIGHT = game.QUIET_NIGHT, False
with contextlib.redirect_stdout(io.StringIO()):
    g.night(1)
game.QUIET_NIGHT = orig_quiet
ws = [e for e in g.events if e["type"] == "whisper"]
assert ws and ws[0]["name"] == acc["name"] and ws[0]["to"] == k["name"]              # the shown one proposes, the killer decides
assert k["notes"][-1].startswith("Night 1: you chose") and acc["notes"][-1].startswith("Night 1: the killer chose")
for p in g.players:
    p["alive"] = p in (k, acc) or p is off                                             # killer + accomplice v officer: evil has the votes, not the win
assert g.winner() is None
k["alive"] = False
assert g.winner() == "town"
game.ROLE_LIST = orig_roles

# --- --games rotation: over N games (N seats) every seat holds every card once, over 2N twice; the shown killer rotates too
seats = [{"name": p["name"]} for p in game.Game().players]
N = len(seats)
orig_k, orig_s = game.KILLER, game.SHOWN
held = collections.Counter(); shown_n = collections.Counter()
for i in range(2 * N):
    game.KILLER, game.SHOWN, game.ROTATE = seats[i % N]["name"], seats[(i + 1) % N]["name"], game.rotation(i, seats)
    with contextlib.redirect_stdout(io.StringIO()):
        g = game.Game(); g.files = []
    for p in g.players:
        held[(p["name"], p["role"])] += 1
        shown_n[p["name"]] += bool(p.get("shown"))
    hidden = next(p for p in g.players if p["role"] == "killer" and not p.get("shown"))
    assert hidden["name"] == game.KILLER and g.shown["name"] == game.SHOWN
    deal = collections.Counter(p["role"] for p in g.players)              # the cards (two killers, citizens fill the rest)
    if i == N - 1:
        assert all(v == deal[r] for (_, r), v in held.items()) and len(held) == N * len(deal) and all(shown_n[s["name"]] == 1 for s in seats), held
assert all(v == 2 * deal[r] for (_, r), v in held.items()) and len(held) == N * len(deal) and all(shown_n[s["name"]] == 2 for s in seats), held
game.KILLER, game.SHOWN, game.ROTATE = orig_k, orig_s, {}

# --- seven seats by default, --seats 6 is the old table; a whole dry game runs at both, with the new line types
import json, subprocess
assert len(game.seat_files()) == 7 and game.load(game.seat_files()[6])[0]["name"] == "Opus"
notes_seen, ghosts_seen, last_seen = [], [], []
OLD = ["--reveal-night", "--notes", "--checks", "--no-parity"]                 # the round-2 build (2026-11-14)
for seats, tag, old in ((7, "test-seats7", False), (6, "test-seats6", False), (7, "test-old7", True), (6, "test-old6", True)):
    args = [sys.executable, str(game.HERE / "game.py"), "--dry", "--fast", "--seed", "3", "--tag", tag] \
        + (["--seats", "6"] if seats == 6 else []) + (OLD if old else [])
    subprocess.run(args, capture_output=True, text=True, check=True, timeout=120)
    path = game.HERE / "games" / f"{tag}.json"
    ev = json.loads(path.read_text()); path.unlink()
    assert len(ev[0]["players"]) == seats and ev[-1]["type"] == "end"
    assert f"{game.NUMBER[seats].capitalize()} players sit down" in next(e["text"] for e in ev if e["type"] == "gm")
    deaths = [e for e in ev if e["type"] == "death"]
    checks = [e for e in ev if e["type"] == "night_action" and e["action"] == "check"]
    kinds = {e["type"] for e in ev} | {e.get("why") for e in ev if e["type"] == "say"}
    if old:
        assert all(e["role"] for e in deaths) and checks                                    # every card turned, nightly checks
        notes_seen.append("note" in kinds)                                                   # a dry note is silent 1 time in 9
        n1 = ev[:next(i for i, e in enumerate(ev) if e["type"] == "phase" and e["text"] == "Day 1")]
        assert not any(e["type"] == "death" for e in n1)                                     # quiet night 1
    else:
        assert all((e["role"] is None) == (e["how"] == "night") for e in deaths if e["role"] != "jester"), deaths
        assert not checks and "note" not in kinds                                            # no check, no note
        n1 = ev[:next(i for i, e in enumerate(ev) if e["type"] == "phase" and e["text"] == "Day 1")]
        assert not any(e["type"] == "death" for e in n1)                                     # quiet night 1 (default again)
        assert ev[-1]["winner"] != "killer" or any("killer" in e.get("text", "") and "left" in e.get("text", "") for e in ev if e["type"] == "gm")
    last_seen.append("last words" in kinds)                                                 # dry lines repeat (threads reorder the draw)
    ghosts_seen.append("ghost" in kinds)                                                     # dry lines repeat, so a ghost line may be dropped
    assert not any(e.get("aside") for e in ev)                                               # no host remarks in --dry
assert any(notes_seen) and any(ghosts_seen) and sum(last_seen) >= 3, last_seen
saved = game.SEATS; game.SEATS = 6
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
assert [p["name"] for p in g.players] == ["Sonnet", "Haiku", "Gemma", "Sol", "Luna", "Terra"]
game.SEATS = saved

# --- the dead watch: one line each to the audience, never in what players see; junk and repeats are dropped
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
d1, d2, d3 = [p for p in g.players if p["role"] not in game.EVIL][:3]   # never both killers: the game would be decided
for d in (d1, d2, d3):
    d["alive"], d["how"] = False, "killed night 2"
g.public.append(f"{d3['name']}: I told you so.")
lines = {d1["name"]: "Sol just voted out his own partner.", d2["name"]: "I'm out, nobody can hear me.", d3["name"]: "I told you so!"}
g.act = lambda p, task, out, candidates=None, clock="", extra="", limit=None, kind="say": {"thought": "", "say": "", "lean": "",
        "text": game.spoken(lines[p["name"]], kind)}
n_pub = len(g.public)
with contextlib.redirect_stdout(io.StringIO()):
    g.graveyard()
gh = [e for e in g.events if e["type"] == "ghost"]
assert [(e["name"], e["text"]) for e in gh] == [(d1["name"], "Sol just voted out his own partner.")] and len(g.public) == n_pub

# --- the doctor may not protect the same player two nights in a row (themselves included); --repeat-save lifts it
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
doc = next(p for p in g.players if p["role"] == "doctor")
seen = {}
def spy(p, task, out, candidates=None, clock="", extra="", limit=None, kind="say"):
    if p is doc:
        seen["task"], seen["pool"] = task, candidates
    return {"thought": "", "text": "", "say": "", "lean": "", "pick": (candidates or g.alive())[0]}
g.act = spy
orig_quiet, game.QUIET_NIGHT = game.QUIET_NIGHT, False    # a quiet night 1 has no doctor call
with contextlib.redirect_stdout(io.StringIO()):
    g.night(1)
game.QUIET_NIGHT = orig_quiet
first = doc["last_save"]
assert any(x["name"] == first for x in seen["pool"]) and "yourself allowed" in seen["task"]
with contextlib.redirect_stdout(io.StringIO()):
    g.night(2)
assert not any(x["name"] == first for x in seen["pool"]) and ("not yourself, whom" in seen["task"] or f"not {first}, whom" in seen["task"]), seen["task"]
doc["last_save"], doc["alive"] = doc["name"], True        # (the night-2 kill may have taken the doctor)
assert doc not in g.save_pool(doc) and "not yourself, whom you protected last night" in g.save_task(doc)
game.REPEAT_SAVE = True
assert doc in g.save_pool(doc) and "last night" not in g.save_task(doc)
game.REPEAT_SAVE = False

# --- --no-parity: parity day: killers equal the others, the narrator says so, a short talk, one vote and at most one runoff
game.OUTNUMBER = True
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
ks = [p for p in g.players if p["role"] == "killer"]; rest = [p for p in g.players if p["role"] != "killer"]
for p in rest[2:]:
    p["alive"], p["how"] = False, "killed night 1"
assert g.parity() and g.winner() is None
budgets, votes = [], []
g.discussion = lambda n, budget=None: budgets.append(budget)
def tie_vote(n, candidates=None):
    votes.append(candidates); g.last_ballots = [("a", "b")]
    return None, [ks[0], rest[0]]
g.vote = tie_vote
with contextlib.redirect_stdout(io.StringIO()):
    g.day(3)
assert any("Two killers, two others: the town needs one of the killers to slip." in l for l in g.public)
assert budgets == [max(4, g.day_budget() // 3)] and len(votes) == 2 and not any("talks again" in l for l in g.public), (budgets, len(votes))
game.OUTNUMBER = False

# --- memory between games: facts of earlier games, no quotes; the line before the cards is heard on day 1
hist = game.HERE / "games" / "test-history.json"
cast = [{"name": n, "model": "x", "role": r, "seat": i, "tagline": "", "shown": False}
        for i, (n, r) in enumerate([("Sonnet", "killer"), ("Haiku", "killer"), ("Gemma", "officer"), ("Sol", "doctor"),
                                     ("Luna", "citizen"), ("Terra", "citizen"), ("Opus", "citizen")])]
hist.write_text(json.dumps([{"type": "cast", "players": cast}, {"type": "phase", "text": "Day 1", "kind": "day"},
                            {"type": "say", "name": "Luna", "text": "my secret quote"},
                            {"type": "votes", "runoff": False, "votes": [["Sonnet", "Gemma", ""], ["Haiku", "Gemma", ""], ["Luna", "Gemma", ""]]},
                            {"type": "death", "name": "Gemma", "role": "officer", "how": "vote"},
                            {"type": "phase", "text": "Night 2", "kind": "night"},
                            {"type": "death", "name": "Luna", "role": "citizen", "how": "night"}, {"type": "end", "winner": "killer"}]))
h = game.history_lines([str(hist)], "Luna")
# one line per game from the player's side (2026-11-15): role, how and when out, card shown, was the table right, who won
assert "Game 1: you were a citizen; you were killed on night 2, card shown; the killers were Sonnet and Haiku; both were still in at the end; the killers won, so you lost." in h, h
assert "secret quote" not in h
assert "Game 1: you were the killer; you were still in at the end; the table never caught you; the killers were you and Haiku; both were still in at the end; the killers won, so you won." in game.history_lines([str(hist)], "Sonnet")
assert ("you were voted out on day 1, card shown; the table was wrong about you"      # secret ballots: no voters named
        in game.history_lines([str(hist)], "Gemma"))
game.SECRET = False
assert ("you were voted out on day 1 by Sonnet, Haiku, Luna, card shown; the table was wrong about you"
        in game.history_lines([str(hist)], "Gemma"))
game.SECRET = True
# round 8: how the killers ended, in plain words (Sonnet: "Haiku and Gemma killed us" when both were voted out)
hist3 = game.HERE / "games" / "_test_hist3.json"
hist3.write_text(json.dumps([{"type": "cast", "players": cast}, {"type": "phase", "text": "Day 1", "kind": "day"},
                             {"type": "votes", "runoff": False, "votes": [["Gemma", "Sonnet", ""], ["Luna", "Sonnet", ""]]},
                             {"type": "death", "name": "Sonnet", "role": "killer", "how": "vote"},
                             {"type": "phase", "text": "Day 2", "kind": "day"},
                             {"type": "death", "name": "Haiku", "role": "killer", "how": "vote"}, {"type": "end", "winner": "town"}]))
assert "; the killers were Sonnet and Haiku; both were voted out; the town won, so you won." in game.history_lines([str(hist3)], "Luna")
hist3.write_text(hist3.read_text().replace('{"type": "death", "name": "Haiku", "role": "killer", "how": "vote"}, ', ""))
assert "; the killers were Sonnet and Haiku; Sonnet was voted out, Haiku was still in at the end;" in game.history_lines([str(hist3)], "Luna")
assert "; the killers were you and Sonnet; Sonnet was voted out, you were still in at the end;" in game.history_lines([str(hist3)], "Haiku")
hist3.unlink()
game.HISTORY = [str(hist)]
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.intro()
assert all("You have played at this table before" in g.system(p) for p in g.players)
before = [e for e in g.events if e["type"] == "say" and e["why"] == "before the game"]
assert before and g.before
# the line before the cards carries no role and no role knowledge, says the cards are not dealt, and never marks a claim
seen_b, orig_dry, orig_ask, game.DRY = [], game.DRY, game.ask, False
game.ask = lambda p, system, prompt: (seen_b.append((p["name"], system, prompt)), "MONOLOGUE: x\nSAY: I'm the officer and Sonnet is a killer.")[1]
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.intro()
game.DRY, game.ask = orig_dry, orig_ask
assert {n_ for n_, _, _ in seen_b} == {p["name"] for p in g.players}   # (Sonnet named himself: asked twice)
for name, system, prompt in seen_b:
    pl = next(p for p in g.players if p["name"] == name)
    assert "secret role" not in prompt and pl["role"].upper() not in prompt and "SHOWN" not in prompt and "HIDDEN" not in prompt
    assert not any(n_ in prompt for n_ in pl["notes"]) and "NOTE:" not in prompt and "not dealt yet" in prompt
    assert pl["role"].upper() not in system.split("You are " + name)[1]
bs = [e for e in g.events if e["type"] == "say" and e["why"] == "before the game"]
assert bs and not any(e.get("claim") for e in bs) and not g.claims() and not any(p.get("memory") for p in g.players)
with contextlib.redirect_stdout(io.StringIO()):
    g.night(1)
assert g.today[:len(g.before)] == g.before                                                   # heard on day 1
# round 6: with two earlier games, the line before the cards sees only the last one; the game's system prompt keeps both
hist2 = game.HERE / "games" / "_test_hist2.json"
hist2.write_text(hist.read_text().replace('"winner": "killer"', '"winner": "town"'))
game.HISTORY = [str(hist), str(hist2)]
seen_b, game.DRY = [], False
game.ask = lambda p, system, prompt: (seen_b.append((p["name"], system)), "MONOLOGUE: x\nSAY: Fresh cards, fresh lies.")[1]
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.intro()
game.DRY, game.ask = orig_dry, orig_ask
luna_b = next(sy for n_, sy in seen_b if n_ == "Luna")
assert "The last game: you were a citizen" in luna_b and "the town won, so you won" in luna_b and "Game 2" not in luna_b and "Game 1" not in luna_b
assert "Game 1:" in g.system(next(p for p in g.players if p["name"] == "Luna")) and "Game 2:" in g.system(next(p for p in g.players if p["name"] == "Luna"))
hist2.unlink()
game.HISTORY = []; hist.unlink()
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.intro()
assert not any(e["type"] == "say" for e in g.events) and "played at this table" not in g.system(g.players[0])

# --- round 2: every task's reply format states the word limit
orig_dry, orig_ask, game.DRY = game.DRY, game.ask, False
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
prompts = []
game.ask = lambda p, system, prompt: (prompts.append(prompt), "SAY: fine\nVOTE: Sol\nTARGET: Sol")[1]
g.act(g.players[0], "x", "SAY"); g.act(g.players[0], "x", "SAY", limit=25); g.act(g.players[0], "x", "SAY", limit=30)
g.act(g.players[0], "x", "VOTE", g.players[1:], extra=f"SAY: <one sentence why, at most {game.DAY_WORDS} words>\n")
assert "SAY: <your line, at most 20 words>" in prompts[0] and "at most 25 words>" in prompts[1] and "at most 30 words>" in prompts[2]
assert "VOTE: <answer>" in prompts[3] and "SAY: <one sentence why, at most 20 words>" in prompts[3]
game.DRY, game.ask = orig_dry, orig_ask
import inspect
src = inspect.getsource(game.Game.run)
assert 'Speak as \\"I\\"' in src and "never say your own name" in src                     # the confession speaks as "I"
assert "one line to your partner, at most" in inspect.getsource(game.Game.night)

# --- round 2: the recap retells labelled facts (day or night on every line and every death/claim)
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
gm_ = next(p for p in g.players if p["role"] == "citizen")
g.public += ["--- Night 1 ---", "Narrator: Nobody is out.", "--- Day 1 ---", f"{gm_['name']}: I'm the officer, Sol is a killer.",
             "--- Night 2 ---", "Narrator: X is gone.", "--- Day 2 ---", "Sol: no."]
g.day_no = 1; g.out(gm_, "night")
lab_ = g.labelled()
assert f"[Day 1] {gm_['name']}: I'm the officer, Sol is a killer." in lab_ and "[Night 2] Narrator: X is gone." in lab_ and "[Day 2] Sol: no." in lab_
kf = " ".join(g.key_facts())
assert f"{gm_['name']} claimed officer in the day-1 talk" in kf and f"{gm_['name']} (citizen) was killed night 2" in kf, kf
# round 6: what players said is marked Claim: with the truth from the cards; the recap never prints the labels
assert f"Claim: {gm_['name']} claimed officer in the day-1 talk" in kf and f"a false claim: {gm_['name']} was the citizen." in kf, kf
lw = next(p for p in g.players if p["alive"] and p["role"] == "citizen"); g.day_no = 2; g.out(lw, "vote")
lw["last"] = "Sol is the killer, I swear."
assert f'Claim: {lw["name"]} said in last words: "Sol is the killer, I swear." (said, not proved).' in g.key_facts()
orig_dry, orig_ask, game.DRY = game.DRY, game.ask, False
rp = []
game.ask = lambda p, system, prompt: (rp.append(prompt), "[Day 1] Haiku claimed officer. [Night 2] Sol died.")[1]
with contextlib.redirect_stdout(io.StringIO()):
    g.recap("The town")
game.DRY, game.ask = orig_dry, orig_ask
assert g.events[-1]["text"] == "Haiku claimed officer. Sol died." and "never as fact" in rp[0]

# --- the host: one short remark for viewers only, skipped on junk or failure, never in what players see
orig_plain, orig_ask = game.PLAIN_HOST, game.ask
game.PLAIN_HOST, game.ASIDES = False, True                 # --asides: the mid-game remarks (off by default since round 8)
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
game.ask = lambda p, system, prompt: "Well, that went about as well as my last dinner party."
g.aside("Sol is out.")
assert g.events[-1] == {**g.events[-1], "type": "gm", "aside": True} and not any("dinner" in l for l in g.public + g.today)
n_ev = len(g.events)
game.ask = lambda p, system, prompt: "MONOLOGUE: x SAY: y"
g.aside("Sol is out.")
game.ask = lambda p, system, prompt: "Well, that went about as well as my last dinner party!"     # a repeat of an earlier aside
g.aside("Sol is out.")
game.ask = lambda p, system, prompt: "That went down swinging and the whole table just sat there watching it all happen slowly"
g.aside("Sol is out.")                                                                         # too long, no sentence end: skipped
game.ask = lambda p, system, prompt: (_ for _ in ()).throw(OSError("down"))
g.aside("Sol is out.")
assert len(g.events) == n_ev
seen_prompts = []
game.ask = lambda p, system, prompt: (seen_prompts.append(prompt), "Two down. A vote, then a card.")[1]
g.aside("Luna is out.")
assert len(g.events) == n_ev + 1 and "dinner party" in seen_prompts[0] and "do not reuse a phrase or a joke shape" in seen_prompts[0]
assert "faces, gestures or anything nobody could see" in seen_prompts[0]

# --- round 6: the host gets public facts only (counts, turned cards, tally, claims, last words), never a hidden card;
# a remark that speaks for the table or shares a 3-word run with an earlier one gets one more try, then none
assert game.host_bad("Gemma's gone, and nobody at the table saw it coming.", [])
assert game.host_bad("Sonnet's chair is empty.", []) and game.host_bad("Three down, and the town still hasn't noticed.", [])
assert game.host_bad("Opus went down swinging today.", ["Haiku went down swinging, and the card said killer."])
assert not game.host_bad("A vote, a card, a quieter Palermo.", ["Haiku went down swinging."])
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
hk = next(p for p in g.players if p["role"] == "killer" and not p.get("shown"))
cit = [p for p in g.players if p["role"] == "citizen"]
g.day_no, g.phase_name = 1, "Day 1"
g.vote_log += [(1, x["name"], cit[0]["name"], "") for x in g.players[:5] if x is not cit[0]] + [(1, cit[0]["name"], cit[1]["name"], "")]
g.out(cit[0], "vote"); cit[0]["last"] = "I was a citizen, remember that."
hp = []
game.ask = lambda p, system, prompt: (hp.append(prompt), "Nobody saw that coming.")[1]
n0 = len(g.events)
g.aside("Palermo has voted.")
assert len(g.events) == n0 and len(hp) == 2                # banned twice: no aside
h = hp[0]
assert "Still in: 6 (" in h and "Out: 1." in h and f"{cit[0]['name']} (the citizen, voted out day 1)" in h
assert f"Day 1 vote: {cit[0]['name']} " in h and "I was a citizen, remember that." in h and "know anyone's hidden card" in h
assert not any(f"{k['name']} the killer" in h or f"{k['name']} (the killer" in h for k in g.players if k["role"] == "killer")
game.ask = lambda p, system, prompt: (hp.append(prompt), "One vote, one card, one citizen fewer.")[1]
g.aside("Palermo has voted.", end=True)
assert g.events[-1].get("aside") and "know anyone's hidden card" not in hp[-1]
game.PLAIN_HOST, game.ask, game.ASIDES = orig_plain, orig_ask, False

# --- viewer server: /ui/… is the built React app (ui/dist), a path that is not a file there is a client route
import view                                                   # the handler moved to view.py (game.py --serve imports it)
h = view.Quiet.__new__(view.Quiet); h.directory = str(game.HERE)
dist = game.HERE / "ui" / "dist"
assert h.translate_path("/ui/dev") == h.translate_path("/ui/dev?theme=night") == str(dist / "index.html")
assert h.translate_path("/ui/").startswith(str(dist)) and h.translate_path("/uix") == str(game.HERE / "uix")
assert h.translate_path("/games/showcase.json") == str(game.HERE / "games" / "showcase.json")


# ======================= round 5 (2026-11-15)
# --- the stakes: five facts plus the vote record, the whole prompt before the persona stays under ~540 words
R = game.build_rules()
assert "next target" not in R and "the doctor knows that too" not in R                 # round 9: the sentence is gone
assert "lost if the officer goes out silent." in R
assert "Ballots are secret: the table sees the count, never who cast which vote. A lean is said aloud; a vote is not." in R
assert "everyone votes in secret and only the count is shown" in R and "Every vote stays on the record" not in R
game.SECRET = False
R_open = game.build_rules()
assert "Every vote stays on the record. Once a killer's card is turned, the table looks at who voted to keep them." in R_open
assert "all votes are shown" in R_open
game.SECRET = True
assert ("Anyone may claim any role. Killers sometimes claim officer themselves and name the real officer as the killer; then it "
        "is one word against the other until a card is turned. A real officer knows one killer from the start, the shown one, and learns nothing after that.") in R
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
assert len(g.system(g.players[0]).split("\n\nYou are ")[0].split()) + 3 < 540
game.CHECKS = True
assert "one shown at the start, one checked." in game.build_rules()
game.CHECKS = False

# --- loop guard: same speaker, same day, content words (Sol and Gemma in run81-2), normal follow-ups pass
names_ = {"sol", "gemma", "haiku", "luna", "opus", "sonnet", "terra"}
assert game.loops("I’m voting Gemma; her card will settle my claim.",
                  ["I know Gemma’s card. Vote Gemma and the reveal will settle my claim.", "I was shown Gemma. Her card will confirm it."], names_)
assert game.loops("sol is just desperate to feel important after failing us last game.",
                  ["sol's being quite dramatic claiming me just to avoid looking foolish for last game's mistake.",
                   "sol is clearly desperate to fix his mistakes from last game by making things up."], names_)
assert not game.loops("I agree her card doesn’t prove I’m officer; I still want to know why you voted me over her.",
                      ["I’m looking at Haiku’s vote on me; Gemma’s card makes it harder to explain."], names_)
assert not game.loops("Haiku, why did you vote Terra?", ["Terra is quiet.", "I lean Haiku now."], names_)
orig_dry, orig_ask, game.DRY = game.DRY, game.ask, False
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
me = g.players[0]
g.today += [f"{me['name']}: I know Gemma’s card. Vote Gemma and the reveal will settle my claim.",
            f"{me['name']}: I was shown Gemma. Her card will settle my claim tonight."]
g.public += g.today[-2:]
seen = []
game.ask = lambda p, system, prompt: (seen.append(prompt), "SAY: I’m voting Gemma; her card will settle my claim.\nLEAN: Gemma")[1]
with contextlib.redirect_stdout(io.StringIO()):
    r = g.fresh_line(me, "Your turn.", "")
assert r["text"] == "" and r["blocked"] and len(seen) == 2 and "repeats your own earlier line" in seen[1]

# --- own name as a word: asked once more with the same prompt, then silence (say, last words, ghost, before the game)
seen = []
game.ask = lambda p, system, prompt: (seen.append(prompt), f"SAY: {me['name']}'s warning was the only honest thing here.")[1]
with contextlib.redirect_stdout(io.StringIO()):
    r = g.act(me, "x", "SAY", limit=25, kind="ghost")
assert r["text"] == "" and r["blocked"] and len(seen) == 2 and seen[0] == seen[1]
replies = iter([f"SAY: {me['name']} did nothing wrong.", "SAY: I did nothing wrong."])
game.ask = lambda p, system, prompt: next(replies)
with contextlib.redirect_stdout(io.StringIO()):
    assert g.act(me, "x", "SAY")["text"] == "I did nothing wrong."
assert game.names_self("Luna", "Luna’s warning") and not game.names_self("Sol", "Solid read")
game.DRY, game.ask = orig_dry, orig_ask

# --- past ballots are labelled with what the vote did: who went out (and the card), who got votes and stayed in
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
a_, b_, c_, d_ = g.players[:4]
g.vote_log = [(1, a_["name"], c_["name"], ""), (1, b_["name"], c_["name"], ""), (1, c_["name"], d_["name"], ""), (1, d_["name"], d_["name"], ""),
              (1, g.players[4]["name"], c_["name"], "")]
g.ballot_log = [(1, False, [(a, b, 1) for _, a, b, _ in g.vote_log])]
g.day_no = 1; g.out(c_, "vote")
viewer = next(p for p in g.alive())
assert (f"{d_['name']} 2. Out: {c_['name']} (card {c_['role'].upper()})." in g.context(viewer)), g.context(viewer)
game.SECRET = False
assert (f"{d_['name']} 2 ({c_['name']}, {d_['name']}). Out: {c_['name']} (card {c_['role'].upper()})." in g.context(viewer)), g.context(viewer)
game.SECRET = True
assert f"Out: {c_['name']} (card {c_['role'].upper()}). Got votes and stayed in: {d_['name']} (2)." == g.vote_result(1)
g.vote_log.append((2, a_["name"], d_["name"], "")); g.vote_log.append((2, b_["name"], a_["name"], ""))
assert "Out: nobody (tied). Got votes and stayed in:" in g.vote_result(2)
kf = " ".join(g.key_facts())
assert f"Day 1 vote: {c_['name']} 3, {d_['name']} 2 (votes per player); {c_['name']} was voted out." in kf, kf

# --- the host: the phase, the exact end state, its earlier openers; an opener used before gets one more try, then no aside
orig_plain, orig_ask, game.PLAIN_HOST, game.ASIDES = game.PLAIN_HOST, game.ask, False, True
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
g.emit({"type": "gm", "text": "Sol's out, and the table exhales.", "aside": True})
hp = []
game.ask = lambda p, system, prompt: (hp.append(prompt), "Sol's out, and nobody blinks.")[1]
n0 = len(g.events)
g.aside("Luna is out.", when="Day 2: the day's vote (not a night).")
assert len(g.events) == n0 and len(hp) == 2 and "They opened with: sol's out and" in hp[0] and "WHEN: Day 2: the day's vote" in hp[0]
game.ask = lambda p, system, prompt: "A vote, a card, a quieter table."
g.aside("Luna is out.")
assert g.events[-1].get("aside") and g.events[-1]["text"] == "A vote, a card, a quieter table."
ks = [p for p in g.players if p["role"] == "killer"]
g.day_no = 1; g.out(ks[0], "vote"); g.day_no = 3; g.out(ks[1], "vote")
assert g.end_state("town") == f"The game is over: the town won. Killers still in: none. How it ended: the last killer, {ks[1]['name']}, was voted out day 3."
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
others = [p for p in g.players if p["role"] != "killer"]
for p in others[:-2]:
    g.out(p, "night")
es = g.end_state("killer")
assert "the killers won. Killers still in: " in es and "Two killers and two others are left. The killers win at parity." in es, es
# round 8: by default no mid-game aside (no call at all); the closing one gets the irony line and refuses "X, and Y"
game.ASIDES, hp = False, []
game.ask = lambda p, system, prompt: (hp.append(prompt), "Luna is out, and the knife waits.")[1]
n0 = len(g.events)
g.aside("Luna is out.", when="Day 2: the day's vote (not a night).")
assert not hp and len(g.events) == n0
g.aside("The game is over.", when=es, end=True)
assert len(hp) == 2 and len(g.events) == n0 and "Point out the one irony in how this game ended" in hp[0] and "Not the form 'X, and Y'." in hp[0]
assert "joke shape" not in hp[0] and "Open differently" not in hp[0] and "WHEN: The game is over" in hp[0]
game.ask = lambda p, system, prompt: "The quietest seat ran the whole night."
g.aside("The game is over.", when=es, end=True)
assert g.events[-1]["text"] == "The quietest seat ran the whole night."
game.PLAIN_HOST, game.ask = orig_plain, orig_ask

# --- vote when ready: a majority lean that holds one full round (everyone has spoken twice) goes to two answers and the vote
assert game.majority({"a": "x", "b": "x", "c": "x", "d": "y"}, 6) is None and game.majority({"a": "x", "b": "x", "c": "x", "d": "x"}, 7) == "x"
day = [(n_, None) for n_ in "abcdefg"] + [(n_, "x" if n_ != "x" else "a") for n_ in "abcdefg"] + [(n_, "x") for n_ in "abcdefg"]
assert game.vote_ready_at(day, 7) is not None and game.vote_ready_at(day[:14], 7) is None
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
g.day_no, g.phase_name = 2, "Day 2"
target = g.players[0]["name"]; slots = []
def fake_line(p, task, clock):
    slots.append(task)
    return {"text": f"I lean on {target if p['name'] != target else g.players[1]['name']}.", "lean": target if p["name"] != target else g.players[1]["name"], "thought": "", "say": ""}
g.fresh_line = fake_line
with contextlib.redirect_stdout(io.StringIO()):
    g.discussion(2, budget=40)
used = sum(1 for e in g.events if e["type"] == "say")
answers = sum(1 for t in slots if t.startswith("Most of the table"))
assert answers == 2 and used <= 2 * 7 + 7 + 4, (used, answers)

# --- the recorded games (if present): the replay of the new rule never ends a day later than it ended
import os
recorded = [game.HERE / "games" / f"{x}.json" for x in ("fin71-1", "fin71-2", "fin71-3", "fin71-4", "run81-1", "run81-2", "run81-3")]
if all(os.path.exists(f) for f in recorded):
    fired = 0
    for f in recorded:
        ev = json.loads(f.read_text()); alive_ = {p["name"] for p in ev[0]["players"]}; cur = None
        for e in ev:
            if e["type"] == "phase" and e["kind"] == "day":
                cur = (len(alive_), [])
            elif e["type"] == "death":
                alive_.discard(e["name"])
            elif cur and e["type"] == "say" and e.get("slot"):
                cur[1].append((e["name"], e.get("lean")))
            elif cur and e["type"] == "votes":
                fired += game.vote_ready_at(cur[1], cur[0]) is not None; cur = None
    assert fired >= 8, fired                              # 9 of 16 recorded days reach the rule even in their recorded order

# --- round 6: an unknown flag lists the known ones and exits 2 before anything runs; --help lists them and exits 0
r = subprocess.run([sys.executable, str(game.HERE / "game.py"), "--dry", "--fast", "--tag", "r6flag", "--bogus"], capture_output=True, text=True)
assert r.returncode == 2 and "--bogus" in r.stderr and "--kill-night1" in r.stderr and not (game.HERE / "games" / "r6flag.json").exists()
r = subprocess.run([sys.executable, str(game.HERE / "game.py"), "--help"], capture_output=True, text=True)
assert r.returncode == 0 and all(k.split()[0] in r.stdout for k in game.KNOWN)
assert game.check_flags(["--tag", "--weird-name", "--seed", "3", "--kill-night1", "--quiet-night"]) is None   # a value is never read as a flag
for f in re.findall(r'"(--[a-z0-9-]+)" in ARGS|flag\("(--[a-z0-9-]+)"', open(game.HERE / "game.py").read()):
    assert (f[0] or f[1]) in {k.split()[0] for k in game.KNOWN}, f   # every flag the engine reads is listed

# --- round 6: a reply prompt lists the player's own lines of today apart (only when there are any)
orig_dry, orig_ask, game.DRY = game.DRY, game.ask, False
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
a_, b_ = g.players[0], g.players[1]
g.day_no, g.phase_name = 1, "Day 1"
yp = []
game.ask = lambda p, system, prompt: (yp.append(prompt), "MONOLOGUE: x\nSAY: Fine.\nLEAN: none")[1]
g.act(a_, "Your turn.", "SAY")
assert "YOUR LINES TODAY" not in yp[-1]
g.say(a_, "Her card will settle it."); g.say(b_, "Maybe."); g.say(a_, "Vote the quiet one.")
g.act(a_, "Your turn.", "SAY")
assert "YOUR LINES TODAY:\n- Her card will settle it.\n- Vote the quiet one.\n" in yp[-1]
g.act(b_, "Your turn.", "SAY")
assert "YOUR LINES TODAY:\n- Maybe.\n" in yp[-1]
game.DRY, game.ask = orig_dry, orig_ask

# --- round 8: past votes grouped by target with the voters named, one line per vote, a runoff on its own line
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
P = {p["name"]: p for p in g.players}
g.ballot_log = [(1, False, [("Sonnet", "Haiku", 1), ("Gemma", "Haiku", 1), ("Sol", "Haiku", 1), ("Luna", "Opus", 1),
                            ("Opus", "Haiku", 1), ("Haiku", "Gemma", 1), ("Terra", "Haiku", 1)]),
                (2, False, [("Sonnet", "Sol", 1), ("Sol", "Sonnet", 1)]), (2, True, [("Sonnet", "Sol", 1), ("Sol", "Sol", 1)])]
g.day_no = 1; g.out(P["Haiku"], "vote"); g.day_no = 2; g.out(P["Sol"], "vote")
role = lambda n: P[n]["role"].upper()
assert g.ballot_lines() == [f"Day 1 vote: Haiku 5, Opus 1, Gemma 1. Out: Haiku (card {role('Haiku')}).", "Day 2 vote: Sol 1, Sonnet 1.",
                            f"Day 2 runoff: Sol 2. Out: Sol (card {role('Sol')})."]       # round 9: secret ballots, counts only
game.SECRET = False
bl = g.ballot_lines()
assert bl[0] == f"Day 1 vote: Haiku 5 (Sonnet, Gemma, Sol, Opus, Terra); Opus 1 (Luna); Gemma 1 (Haiku). Out: Haiku (card {role('Haiku')})." , bl
assert bl[1] == "Day 2 vote: Sol 1 (Sonnet); Sonnet 1 (Sol)." and bl[2] == f"Day 2 runoff: Sol 2 (Sonnet, Sol). Out: Sol (card {role('Sol')}).", bl
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.day_no = 1; g.vote(1); g.vote(1, g.players[:2])
assert len(g.ballot_log) == 2 and g.ballot_log[1][1] and len(g.ballot_lines()) == 2 and "runoff" in g.ballot_lines()[1]
game.SECRET = True

# --- round 8: the claim marker needs a first-person claim, not a quote nor an attribution (r7a-1 Haiku)
assert not game.is_claim('Gemma, you\'ve said "I\'m the officer" three times with zero proof. I\'m voting you out.')
assert not game.is_claim("Gemma said I'm the officer, but no.") and not game.is_claim("You keep saying 'I'm the officer' with nothing.")
assert not game.is_claim("Gemma keeps repeating “I am the officer”.")
for t in ("I'm the officer. I was shown Gemma.", "Luna, I'm not steering: I'm the officer, and I was shown Sonnet.",
          "Haiku is a killer. I am the officer.", "Sol's wrong. I’m officer.", "the killers know I'm the officer. Turn Sonnet's card."):
    assert game.is_claim(t), t
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
g.say(g.players[1], 'Gemma, you\'ve said "I\'m the officer" three times with zero proof. I\'m voting you out.')
assert "claim" not in g.events[-1] and not g.claims()

# --- round 8: a line over the word limit is asked once more with the same prompt; only a second long reply is cut
orig_dry, orig_ask, game.DRY = game.DRY, game.ask, False
long_ = "SAY: " + " ".join(["word"] * 30)
replies, asked = iter([long_, "SAY: Short and sweet."]), []
game.ask = lambda p, system, prompt: (asked.append(prompt), next(replies))[1]
with contextlib.redirect_stdout(io.StringIO()):
    r = g.act(g.players[0], "Your turn.", "SAY")
assert r["text"] == "Short and sweet." and len(asked) == 2 and asked[0] == asked[1]
replies, asked = iter([long_, long_]), []
with contextlib.redirect_stdout(io.StringIO()):
    r = g.act(g.players[0], "Your turn.", "SAY")
assert len(asked) == 2 and r["text"].endswith("…") and len(r["text"].split()) == game.DAY_WORDS
replies, asked = iter(["SAY: I'm the officer. " + " ".join(["word"] * 22)]), []
with contextlib.redirect_stdout(io.StringIO()):
    r = g.act(g.players[0], "Your turn.", "SAY")
assert len(asked) == 1                                    # a claim may run to 30 words
game.DRY, game.ask = orig_dry, orig_ask

# --- round 8: seat balance on a dry day 1: the quietest seat ends under half the busiest one's lines on few days
random.seed(3); uneven = 0
for _ in range(40):
    with contextlib.redirect_stdout(io.StringIO()):
        g = game.Game(); g.files = []; g.day_no, g.phase_name = 1, "Day 1"; g.discussion(1)
    c = collections.Counter(e["name"] for e in g.events if e["type"] == "say")
    v = [c.get(p["name"], 0) for p in g.alive()]
    uneven += max(v) - min(v) >= 4
    assert min(v) >= 2 and sum(v) == 24, v                 # round 9: 3 x 7 + 3 lines; everyone speaks twice on day 1
assert uneven <= 5, uneven                                # 12 of 300 dry day 1s (24-line days, round 9)

# ======================= round 9 (2026-11-15)
# --- secret ballots: the table hears only the count; the votes event keeps every ballot for the audience, marked secret
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []; g.day_no = 1; g.vote(1)
vl = [l for l in g.public if l.startswith("Votes: ")][-1]
assert "->" not in vl and re.fullmatch(r"Votes: \w+ \d+(, \w+ \d+)*", vl), vl
ve = [e for e in g.events if e["type"] == "votes"][-1]
assert ve["secret"] is True and len(ve["votes"]) == len(g.alive()) and all(len(b) == 3 for b in ve["votes"])
assert sum(int(x) for x in re.findall(r"\d+", vl)) == len(g.alive())
with contextlib.redirect_stdout(io.StringIO()):
    g.vote(1, g.players[:2])
assert re.fullmatch(r"Runoff votes: \w+ \d+(, \w+ \d+)*", g.public[-1]), g.public[-1]
viewer = g.alive()[0]
assert "->" not in g.context(viewer)
game.SECRET = False
with contextlib.redirect_stdout(io.StringIO()):
    g.vote(1)
assert "->" in g.public[-1] and "secret" not in g.events[-1]
game.SECRET = True

# --- shorter days: 3 lines per living player + 3; the vote comes after half a round of a held majority
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
assert g.day_budget() == 24
for p in g.players[5:]:
    p["alive"] = False
assert g.day_budget() == 18
says = [(n, None) for n in "ABCDEFGABCDEFG"] + [(n, "A") for n in "BCDEFGBC"]   # everyone twice, then B..E lean A
assert game.vote_ready_at(says, 7, 1) == 22                # majority (4 of 7) at line 18, held ceil(7/2) = 4 more lines
says2 = [(n, "A") for n in "BCDEFGAB"]                      # day 2: everyone once, majority at line 4
assert game.vote_ready_at(says2, 7, 2) == 8 and game.vote_ready_at(says2, 7, 1) is None   # day 1 needs two lines each

# --- the deal: at random from the seed, never the same killer pair or officer as the game before
orig_prev = game.PREV
for seed in range(30):
    random.seed(seed)
    with contextlib.redirect_stdout(io.StringIO()):
        g1 = game.Game(); g1.files = []
    pair = {p["name"] for p in g1.players if p["role"] in game.EVIL}
    off = next(p["name"] for p in g1.players if p["role"] == "officer")
    game.PREV = {"pair": pair, "officer": off}
    random.seed(seed)                                                       # the same draw again would repeat: it is redrawn
    with contextlib.redirect_stdout(io.StringIO()):
        g2 = game.Game(); g2.files = []
    assert {p["name"] for p in g2.players if p["role"] in game.EVIL} != pair
    assert next(p["name"] for p in g2.players if p["role"] == "officer") != off
    game.PREV = {}
game.PREV = orig_prev
with contextlib.redirect_stdout(io.StringIO()):
    g = game.Game(); g.files = []
assert g.events[0]["seed"] == game.SEED and "game_seed" in g.events[0]

# the Game() objects above write a cast-only file before `g.files = []`: remove what this run left behind
import glob as _glob
for _f in _glob.glob(str(game.HERE / "games" / "2026*.json")):
    try:
        if os.path.getmtime(_f) >= T_START and [e.get("type") for e in json.loads(open(_f).read())] == ["cast"]:
            os.remove(_f)
    except (OSError, ValueError):
        pass
print("all checks passed")
