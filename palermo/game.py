#!/usr/bin/env python3
"""One Night in Palermo: social deduction played by AI agents. No API keys, no credits.

Code enforces every rule (roles, nights, votes). The game master agent only narrates.
Each player is players/<seat>-<name>.md: frontmatter sets name/model/effort, body is the persona.
Models: claude:<model>, codex:<model>, local:<LM Studio model id>. Any seat can be given to any model you have:
edit its model line, or --model Gemma=claude:sonnet for one run (--check tries every seat once).
Backends run on the Claude and ChatGPT subscriptions; API-key variables are stripped from
their environment so a call can never bill credits.

  python3 game.py              # play, watch live at http://localhost:8765
  python3 game.py --dry        # scripted fake players, no model calls, watchable pace
  python3 game.py --dry --fast # same, instant, no server (engine check)
  python3 game.py --seed 7     # reproducible deal / dry answers (no seed: a fresh one, printed and stored in the cast)
  python3 game.py --seats 6    # only the first six seat files (the table before Opus)
  python3 game.py --help       # every flag, one line each; an unknown flag lists them and exits with code 2
Rules switches (each one changes a default): --kill-night1 (a kill on night 1), --no-parity (killers must outnumber),
--reveal-night (night victims show their card), --notes (night victims leave a note), --checks (the officer checks one
player a night), --hide-vote, --no-last-words, --no-ghosts, --repeat-save, --no-self-save, --plain-host, --asides,
--no-history / --history f1.json,f2.json. See docs/engine-rules.md.
Replay an old game: python3 game.py --serve, then open /?file=games/<name>.json
"""
import contextlib
import datetime
import difflib
import functools
import http.server
import json
import os
import pathlib
import random
import re
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

HERE = pathlib.Path(__file__).parent
ARGS = sys.argv[1:]
DRY = "--dry" in ARGS
FAST = "--fast" in ARGS
PORT = 8765
SECONDS_PER_MESSAGE = 10          # how the UI clock converts the message budget
# table talk (default): many short turns, any natural move; --classic = interrogation prompts
NATURAL = "--classic" not in ARGS
MAX_BUDGET = 26 if NATURAL else 15   # messages per day (capped at 3 or 5 per alive player)
LMSTUDIO = "http://localhost:1234/v1/chat/completions"
KEYS = ("MONOLOGUE", "SAY", "LEAN", "VOTE", "TARGET", "NOTE", "FORGET")
MAX_NOTES = 10                    # self-written memory entries kept per player
NOTE_TTL = {1: 1, 2: 3, 3: 99}    # days a note of each importance survives
def flag(name, default):
    return type(default)(ARGS[ARGS.index(name) + 1]) if name in ARGS else default
MAX_DAYS = flag("--days", 99)     # --days 1: stop after day 1 (fast test)
BUDGET_CAP = flag("--budget", 0)  # --budget 8: shorter discussion (fast test)
SHOW_PROMPT = flag("--prompt", "")  # --prompt Sonnet: print every prompt that player gets
# levels: facts + ranked notes + today | transcript: facts + everything said | short: facts + notes + last 6 lines
MEMORY = flag("--memory", "levels")
TAG = flag("--tag", "")             # --tag memtest-levels: name of the saved game file
# --games 7: play several games in a row, each dealt at random from --seed and its number; from game 2 on the table
# remembers
GAMES = flag("--games", 1)
# --first 8: with --games, start at game 8 (same rotation and numbering; to resume a batch)
FIRST = flag("--first", 1)
KILLER = flag("--killer", "")        # --killer Luna: force who draws the killer role
# default: scripted narration (facts as templates), the recap stays a model call
NARRATOR_AGENT = "--narrator-agent" in ARGS
# No kill on night 1: the killers only meet and the officer is shown one. A night-1 kill left a seven-seat town no
# spare vote. --kill-night1 turns it off; --quiet-night is a no-op.
QUIET_NIGHT = "--kill-night1" not in ARGS
KILLER_FIXED = bool(KILLER)
# No --seed gives a fresh seed, printed and stored in the cast event; each game of an evening is seeded from it and its
# number.
SEED = int(ARGS[ARGS.index("--seed") + 1]) if "--seed" in ARGS else random.SystemRandom().randrange(10 ** 9)
GAME_SEED = SEED                     # set per game by main() from SEED and the game number; stored in the cast event
# the previous game of the evening: {"pair": {names}, "officer": name}; set by main()
PREV = {}
SHOWN = ""                           # force the shown killer (lab.py and tests only)
ROTATE = {}                          # a fixed deal {seat name: role} (lab.py and tests only)
# Greek Palermo; the rest are citizens. The mayor (option C) is out by default: the ×2 tally names the mayor after the
# first vote and the killers take them that night. Back with --roles …,mayor
ROLES = flag("--roles", "killer=2,officer,doctor")
# --roles killer=2,officer,doctor --parity = option A (plain Greek Palermo, killers win at parity);
# --roles killer=1,officer,doctor = plain Mafia; add jester for a seat that wins alone if voted out.
# `mayor`: a citizen whose vote counts double, shown in the tally. `--parity`: killers win when they equal the rest
# (default: they must outnumber it, so 2 v 2 is a vote). `killer,accomplice,officer,doctor` = option B (the accomplice
# is the killer's partner: whispers, votes, lies, is the one shown to the officer, cannot kill, counts as town for
# parity).
# Default: the killers win at parity (as many killers as others), the standard rule. --no-parity: they must outnumber
# (1 v 1 is theirs). --parity is a no-op.
OUTNUMBER = "--no-parity" in ARGS
# Cards (research/greek-house-rules.md): a voted-out player shows the card, a player killed at night does not.
# --reveal-night turns night cards again; --hide-vote keeps voted-out cards face down; --hide-night and --show-vote are
# accepted as no-ops. With every card turned the town won too easily.
HIDE_VOTE = "--hide-vote" in ARGS
# Ballots are secret: the table sees only the count per player (the Greek house rule; public ballots solved day 2 in
# the dullest games). --open-ballots shows who voted whom again.
SECRET = "--open-ballots" not in ARGS
HIDE_NIGHT = "--reveal-night" not in ARGS
LAST_WORDS = "--no-last-words" not in ARGS   # a voted-out player says one line before the card is announced
# A night victim leaves one line the table reads in the morning. Off by default: the dead say nothing in the Greek
# game. --no-notes is a no-op.
NIGHT_NOTES = "--notes" in ARGS
# The officer also checks one player each night. Off by default: the Greek officer knows the shown killer and has no
# other power.
CHECKS = "--checks" in ARGS
# after each day's vote the dead say one line to the audience (players never see it)
GHOSTS = "--no-ghosts" not in ARGS
REPEAT_SAVE = "--repeat-save" in ARGS        # default: the doctor may not protect the same player two nights in a row
NO_SELF_SAVE = "--no-self-save" in ARGS      # the doctor may not protect themselves
PLAIN_HOST = "--plain-host" in ARGS or DRY   # default: the narrator adds one short model remark at the end
# Also one host remark after each death. Off by default: mid-game asides kept getting facts wrong.
ASIDES = "--asides" in ARGS
SEATS = flag("--seats", 0)                   # --seats 6: play with only the first 6 seat files
# --model Gemma=claude:sonnet,Opus=codex:gpt-6-sol: who plays a seat, without editing its file (any
# model can sit at the table). all=MODEL sets every seat, host=MODEL the narrator; a named seat wins over
# all. The seat keeps its name, tic and persona; the cast event stores the model that really played. The seat file's
# effort is dropped with its model (codex then uses "low", which every codex model accepts).
def model_flag(spec):
    picks = {}
    for part in filter(None, spec.split(",")):
        who, sep, model = part.partition("=")
        if not sep or model.partition(":")[0] not in ("claude", "codex", "local") or not model.partition(":")[2]:
            sys.exit(f"--model: write SEAT=BACKEND:MODEL (claude:…, codex:… or local:…), not {part!r}")
        picks[who.strip().lower()] = model.strip()
    return picks
MODELS = model_flag(flag("--model", ""))
CHECK = "--check" in ARGS                    # one short call per seat and the host, then stop: do the models answer?
NO_HISTORY = "--no-history" in ARGS          # --games: every game starts fresh (the stats run needs independent games)
# earlier games this table remembers (set per game by --games)
HISTORY = [f for f in flag("--history", "").split(",") if f]
# Every flag game.py takes: --help prints this list; an unknown flag prints it and exits with code 2
# before anything is called. Flags taking a value end in " VALUE".
KNOWN = {
    "--dry": "scripted fake players, no model calls, watchable pace",
    "--fast": "instant, no server (engine check)",
    "--seed N": "reproducible deals and dry answers (default: a fresh seed, printed and stored in the cast event)",
    "--seats N": "only the first N seat files",
    "--model SEAT=MODEL": "give a seat to another model: Gemma=claude:sonnet (several with commas; all=… every seat, "
                          "host=… the narrator)",
    "--check": "one short call to every seat's model and the host's, then stop (no game)",
    "--games N": "several games in a row, each dealt at random (no killer pair or officer twice running); "
                 "the table remembers",
    "--first N": "with --games, start at game N (to resume a batch)",
    "--tag NAME": "name of the saved game file",
    "--killer NAME": "force who draws the killer role",
    "--roles LIST": "the cards, default killer=2,officer,doctor (the rest are citizens)",
    "--days N": "stop after day N (fast test)",
    "--budget N": "shorter discussion (fast test)",
    "--memory MODE": "levels (default) | transcript | short",
    "--prompt NAME": "print every prompt that player gets",
    "--classic": "interrogation prompts instead of table talk",
    "--narrator-agent": "the narrator is a model call, not scripted",
    "--plain-host": "no model remark from the host at all",
    "--asides": "the host also remarks after each death (default: only at the end)",
    "--kill-night1": "a kill on night 1 (default: nobody dies night 1)",
    "--no-parity": "the killers must outnumber the others (default: they win at parity)",
    "--reveal-night": "night victims show their card",
    "--hide-vote": "voted-out cards stay face down",
    "--open-ballots": "the table sees who voted whom (default: secret ballots, only the count is shown)",
    "--notes": "night victims leave one line the table reads in the morning",
    "--checks": "the officer checks one player a night",
    "--no-last-words": "a voted-out player says nothing before the card",
    "--no-ghosts": "the dead say no line to the audience after each vote",
    "--repeat-save": "the doctor may protect the same player two nights in a row",
    "--no-self-save": "the doctor may not protect themselves",
    "--no-history": "with --games, every game starts fresh",
    "--history FILES": "earlier games this table remembers, f1.json,f2.json",
    "--serve": "replay an old game: open /?file=games/<name>.json",
    "--help": "this list",
    "--quiet-night": "no-op (the default)", "--parity": "no-op (the default)", "--no-notes": "no-op (the default)",
    "--hide-night": "no-op (the default)", "--show-vote": "no-op (the default)",
}


def check_flags(args):
    """--help: print KNOWN and exit 0. An unknown --flag: print KNOWN and exit 2. A flag's value is skipped."""
    takes = {k.split()[0] for k in KNOWN if " " in k}
    names = {k.split()[0] for k in KNOWN}
    listing = "Flags:\n" + "\n".join(f"  {k:<18} {v}" for k, v in KNOWN.items())
    if "--help" in args or "-h" in args:
        print(listing)
        sys.exit(0)
    bad, skip = [], False
    for a in args:
        if skip:
            skip = False
        elif a.startswith("-"):
            bad += [a] * (a not in names)
            skip = a in takes
    if bad:
        print(f"Unknown flag: {' '.join(bad)}\n{listing}", file=sys.stderr)
        sys.exit(2)


EVIL = ("killer", "accomplice")
NUMBER = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def seat_files():
    """The seats at the table: players/*.md in file order, the first N with --seats N."""
    files = sorted((HERE / "players").glob("*.md"))
    return files[:SEATS] if SEATS else files


# What each role IS, only for the roles in this game (all the help a player gets is in one fixed prompt).
ROLE_TEXT = {
    "killer": "- KILLER: each night chooses one player to eliminate.",
    "killers": "- KILLERS (2): know each other. Each night they choose one player to eliminate. One was SHOWN to the "
               "officer at the start; the other is HIDDEN.",
    "killer_b": "- KILLER (HIDDEN): has an accomplice; each night the two choose one player to eliminate.",
    "accomplice": "- ACCOMPLICE: the killer's partner: whispers with them at night, cannot kill, was SHOWN to the "
                  "officer at the start, counts with the town in the head count.",
    "mayor": "- MAYOR: a citizen whose vote counts double; the tally shows it.",
    "officer": "- OFFICER: each night checks one player and learns: killer or not.",
    "officer2": "- OFFICER: was shown one killer at the start. Each night checks one more player and learns: "
                "killer or not.",
    "police": "- OFFICER: was shown one killer at the start. No other power.",
    "doctor": "",   # built in build_rules(): it follows --no-self-save and --repeat-save
    "citizen": "- CITIZENS: no power.",
    "jester": "- JESTER: no team. Wins alone if the town votes them out.",
}


def parse_roles(spec):
    out = []
    for part in spec.split(","):
        name, _, count = part.strip().partition("=")
        if name not in ("killer", "officer", "police", "doctor", "citizen", "jester", "accomplice", "mayor"):
            sys.exit(f"--roles: unknown role {name!r} "
                     "(killer, officer, police, doctor, citizen, jester, accomplice, mayor)")
        out += [name] * int(count or 1)
    return out


ROLE_LIST = parse_roles(ROLES)
PAIR = sum(r in EVIL for r in ROLE_LIST) >= 2    # Palermo: a shown and a hidden one on the killer's side
CLAIM = re.compile(r"\bI(?:['’]m| am) (?:the )?(?:real |actual )?(?:officer|police(?:man)?|cop|detective)\b", re.I)
QUOTED = re.compile(r'"[^"]*"|“[^”]*”|‘[^’]*’|(?<!\w)\'(?:[^\']|\'(?=\w)){1,80}?\'(?!\w)')
SAID = re.compile(r"\b(?:said|says|say|saying|claim(?:s|ed|ing)?|told \w+|tells \w+|"
                  r"wrote|insist(?:s|ed)?)\b[\s:,—–-]*$", re.I)


def is_claim(text):
    """A first-person officer claim: CLAIM outside quotes and not attributed to someone else ("Gemma said I'm the
    officer"). Quoting another player's claim is not a claim."""
    t = QUOTED.sub(" ", text or "")
    for m in CLAIM.finditer(t):
        start = max(t.rfind(c, 0, m.start()) for c in ".!?;") + 1
        if not SAID.search(t[start:m.start()]):
            return True
    return False
if "police" in ROLE_LIST and not PAIR:
    sys.exit("--roles: police needs two killers (it is shown one of them)")


def officer_checks():
    """Does the officer check one player a night? Only with --checks, and always with one killer: nobody is
    shown then, so without the check the officer would have no power at all."""
    return CHECKS or not PAIR


def role_keys():
    """Which ROLE_TEXT lines this game's rules show (read at call time, so tests can flip the flags)."""
    officer = ("officer2" if CHECKS else "police") if PAIR else "officer"
    return list(dict.fromkeys(
        (["killer_b", "accomplice"] if "accomplice" in ROLE_LIST else ["killers" if PAIR else "killer"])
        + [officer] * ("officer" in ROLE_LIST) + ["police"] * ("police" in ROLE_LIST)
        + ["doctor"] * ("doctor" in ROLE_LIST) + ["mayor"] * ("mayor" in ROLE_LIST)
        + ["citizen"] + ["jester"] * ("jester" in ROLE_LIST)))


def card_rules(officer):
    """Which cards are turned, told once in THE GAME (`cards`) and once as a stake (`stake`)."""
    if HIDE_VOTE and HIDE_NIGHT:
        cards, stake = ("No card is shown until the game ends. ",
                        "No card is turned before the end, so a claim is only as good as the player making it.")
    elif HIDE_VOTE:
        cards, stake = ("A player killed at night shows their card; a voted-out card stays face down until the end. ",
                        "A voted-out card stays face down, so a vote never proves or disproves a claim.")
    else:
        cards = ("Every player who goes out, by vote or at night, shows their card. " if not HIDE_NIGHT else
                 "A voted-out player shows their card; a player killed at night does not. ")
        stake = (("Every player who goes out shows their card. " if not HIDE_NIGHT else
                  "A voted-out player shows their card; a player killed at night does not. ")
                 + ("Voting out a player who claims officer only shows whether they lied; voting out the player they "
                    "named tests the same claim and may remove a killer." if officer else
                    "A vote shows what the player was."))
    return cards, stake


def rule_stakes(officer, stake):
    """WHAT IS AT STAKE: facts about the game, never advice on how to play it."""
    stakes = ["Wrong votes are expensive: with two killers at a small table the town can lose after two of them."
              if PAIR else "Wrong votes are expensive at a small table."]
    if officer:
        stakes.append("What the officer knows helps the town only once the table hears it, and it is lost if the "
                      "officer goes out silent.")
    stakes.append(stake)
    if SECRET:
        stakes.append("Ballots are secret: the table sees the count, never who cast which vote. "
                      "A lean is said aloud; a vote is not.")
    elif not HIDE_VOTE:
        stakes.append("Every vote stays on the record. Once a killer's card is turned, the table looks at who voted to "
                      "keep them.")
    else:
        stakes.append("Every vote stays on the record.")
    if officer:
        if not PAIR:
            knows = ""
        elif CHECKS:
            knows = " A real officer can name two killers after the first night: one shown at the start, one checked."
        else:
            knows = " A real officer knows one killer from the start, the shown one, and learns nothing after that."
        stakes.append("Anyone may claim any role. Killers sometimes claim officer themselves and name the real officer "
                      "as the killer; then it is one word against the other until a card is turned." + knows)
    else:
        stakes.append("Anyone may claim any role.")
    stakes.append("Day 1 has no proof; people go on tone and gut, and that is normal.")
    return stakes


def build_rules(seats=None):
    """The one fixed system prompt before the persona: rules, what is at stake (facts, no advice), how to
    talk. It follows the flags; the seat count comes from the table. No example lines anywhere (they got copied)."""
    n = seats or len(seat_files())
    officer = "officer" in ROLE_LIST or "police" in ROLE_LIST
    cards, stake = card_rules(officer)
    stakes = rule_stakes(officer, stake)

    # THE GAME: the role lines, then how a day and the game end.
    killers_text = ROLE_TEXT["killers"]
    if QUIET_NIGHT:
        killers_text = killers_text.replace("Each night", "Each night from night 2")
    doctor_text = ("- DOCTOR: each night" + (" from night 2" if QUIET_NIGHT else "") + " protects one player ("
                   + ("not themselves" if NO_SELF_SAVE else "themselves allowed")
                   + ("" if REPEAT_SAVE else ", never the same player two nights in a row")
                   + "). If the killers chose that player, nobody dies.")
    text = dict(ROLE_TEXT, killers=killers_text, doctor=doctor_text)
    if SECRET:
        voting = ("By day the table talks, then everyone votes in secret and only the count is shown; the player with "
                  "the most votes is out")
    else:
        voting = ("By day the table talks, then everyone votes at once and all votes are shown; the player with the "
                  "most votes is out")
    leans = ("With each line you also give your LEAN (whom you would vote right now); everyone sees the leans. When "
             "most of the table leans on one player, that player answers twice, the table replies, then the vote. If "
             "time runs out first, the vote happens anyway. " if NATURAL else "")
    town_wins = ("The town wins when the killer is out. " if "accomplice" in ROLE_LIST else
                 "The town wins when every killer is out. ")
    killers_win_at = f"The killers win when they {'outnumber' if OUTNUMBER else 'equal or outnumber'} the rest"
    if OUTNUMBER:
        killers_win_at += (" or when one killer and one other player are left"
                           + (", unless that player is the mayor" if "mayor" in ROLE_LIST else ""))

    return (f"It is game night. You and {NUMBER.get(n - 1, n - 1)} others are playing One Night in Palermo (the Greek "
            "Mafia), a party game of social deduction played by AI agents. Everyone has a secret role, and everybody "
            "plays to win.\n\n"
            "THE GAME\n" + "\n".join(text[k] for k in role_keys()) + "\n"
            + ("Night 1 nobody dies. " if QUIET_NIGHT else "")
            + voting
            + (" and says last words. " if LAST_WORDS else ". ")
            + ("A player killed at night leaves a note the table reads in the morning. " if NIGHT_NOTES else "")
            + cards
            + leans
            + "A tie: the tied players each say one line, then a runoff; if that ties too, nobody is out. "
            + town_wins
            + killers_win_at + ". Bluffing is allowed.\n\n"
            "WHAT IS AT STAKE (facts, not advice; how you play is yours)\n"
            + "\n".join(f"- {s}" for s in stakes) + "\n\n"
            "HOW TO TALK\nYou are at a table with people you know. Say one thing at a time in a few plain words, as "
            "\"I\", never your own name. Talk about the game (claims, votes, deaths, who gains), not about who asked "
            "whom or who dodged. Do not repeat a point you already made.")


RULES = build_rules()

LEAN_FIELD = "LEAN: <the player you would vote right now, or none>\n" if NATURAL else ""
FORMAT = ("Reply in exactly this format, plain text, each label on its own line:\n"
          "MONOLOGUE: <one short sentence: what you really think right now; nobody hears it>\n")

DRY_SAY = ["{x}, why so quiet? Quiet people worry me.", "I don't trust {x}. Something is off.",
           "I'm just a citizen, stop looking at me.", "{x} and {y} keep agreeing. Suspicious.",
           "Vote {x}. I said what I said.", "PASS", "{x}, answer the question. Where were you?",
           "If {x} is innocent I'll eat my hat.", "I believe {y}. {x}, not so much."]
DRY_THINK = ["If I push {x}, nobody looks at me.", "{y} might actually be on my side.",
             "I have no idea. Act confident.", "{x} is lying, I can feel it."]


def load(path):
    meta, body = {}, path.read_text()
    if body.startswith("---"):
        head, body = body[3:].split("---", 1)
        for line in head.strip().splitlines():
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    pick = MODELS.get(meta.get("name", "").lower() if path.parent.name == "players" else "host") or \
        (MODELS.get("all") if path.parent.name == "players" else None)
    if pick and "model" in meta:
        meta["model"] = pick
        meta.pop("effort", None)
    return meta, body.strip()


def clean_env():
    """Subscription CLIs only: an API key in the environment would switch them to billing."""
    return {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY")}


CLAUDE_LOCK = threading.Lock()    # the claude CLI hangs now and then when several copies start at once
TIMEOUT = 30                      # a normal call takes 4-10s; a hung one is cut here and retried


def run(cmd, prompt):
    lock = CLAUDE_LOCK if cmd[0] == "claude" else contextlib.nullcontext()
    debug = pathlib.Path(tempfile.gettempdir()) / f"palermo-claude-{threading.get_ident()}.log"
    if cmd[0] == "claude":
        cmd = cmd + ["--debug-file", str(debug)]
    try:
        with lock:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=TIMEOUT,
                               cwd=tempfile.gettempdir(), env=clean_env())  # no project files in context
        debug.unlink(missing_ok=True)
    except subprocess.TimeoutExpired as e:
        err = (e.stderr or b"")[-300:] if isinstance(e.stderr, bytes) else str(e.stderr or "")[-300:]
        stamp = datetime.datetime.now().strftime("%H%M%S")
        dbg = debug.read_text()[-3000:] if debug.exists() else "(no debug log)"
        (HERE / "games" / f"timeout-{stamp}.txt").write_text(
            f"CMD: {cmd}\nSTDERR: {err!r}\n\nDEBUG TAIL:\n{dbg}\n\nPROMPT:\n{prompt}\n")
        print(f"   [{cmd[0]} {cmd[3] if len(cmd) > 3 else ''} timed out after {TIMEOUT}s; see "
              f"games/timeout-{stamp}.txt]", flush=True)
        return ""
    out = r.stdout.strip()
    if r.returncode != 0 or out.startswith("API Error"):
        print(f"   [{cmd[0]} error: {(r.stderr or out)[-200:].strip()}]", flush=True)
        # A quota limit is not transient: the seat would sit silent all game.
        if re.search(r"usage limit|hit your limit", r.stderr + out, re.I):
            sys.exit(f"{cmd[0]} is out of quota; stopping so no game is played with a silent seat. "
                     "Resume with --first.")
        return ""
    return out


def call(model, effort, system, prompt):
    backend, _, name = model.partition(":")
    if backend == "claude":
        cmd = ["claude", "-p", "--model", name, "--system-prompt", system, "--tools", "",
               "--no-session-persistence", "--setting-sources", "", "--strict-mcp-config"]
        return run(cmd + (["--effort", effort] if effort else []), prompt)
    if backend == "codex":  # codex exec has no system prompt flag; skills/docs kept out of context
        cmd = ["codex", "exec", "--skip-git-repo-check", "--ephemeral", "-s", "read-only",
               "-c", f'model_reasoning_effort="{effort or "low"}"', "-c", 'model_verbosity="low"',
               "-c", "project_doc_max_bytes=0"]
        return run(cmd + (["-m", name] if name else []) + ["-"], f"{system}\n\n{prompt}")
    if backend == "local":
        # LM Studio: no hidden reasoning
        body = json.dumps({"model": name, "max_tokens": 300, "reasoning_effort": "none",
                           "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]})
        req = urllib.request.Request(LMSTUDIO, body.encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as r:
            text = json.load(r)["choices"][0]["message"]["content"]
        return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()
    raise ValueError(f"unknown model backend: {model}")


def ask(p, system, prompt):
    for attempt in range(2):  # one retry on a failed/empty call
        try:
            reply = call(p["model"], p.get("effort"), system, prompt)
        except (OSError, subprocess.SubprocessError, KeyError, ValueError, IndexError, TypeError) as e:
            print(f"   [{p['model']} failed: {e}]", flush=True)
            reply = ""
        if reply:
            return reply
    return ""


def field(reply, name):
    """Value after `NAME:` up to the next known label (same line or next line)."""
    m = re.search(rf"\b{name}:\s*(.*?)(?=\s*\**\b(?:{'|'.join(KEYS)}):|\Z)", reply, re.S)
    return m.group(1).strip().strip("*").strip().strip('"') if m else ""


def pick_name(text, candidates, fallback=None):
    """Exact name, else the candidate mentioned first. A reply that names nobody falls back to `fallback` (for a vote:
    the lean the player last said aloud) when that is a candidate, else to a random candidate."""
    word = re.sub(r"[^a-z]", "", text.lower())
    for c in candidates:
        if word == c["name"].lower():
            return c
    hits = [(m.start(), c) for c in candidates
            for m in [re.search(rf"\b{c['name']}\b", text, re.I)] if m]
    if hits:
        return min(hits, key=lambda h: h[0])[1]
    return next((c for c in candidates if c["name"] == fallback), None) or random.choice(candidates)


def plurality(choices):
    """(most-picked player, tied players). Tie -> (None, [tied...])."""
    counts = Counter(c["name"] for c in choices)
    top = counts.most_common()
    tied = [c for c in {c["name"]: c for c in choices}.values() if counts[c["name"]] == top[0][1]]
    return (None, tied) if len(tied) > 1 else (tied[0], [])


def grams(text, n=3):
    w = re.findall(r"[a-z']+", text.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


STOP = set("the a an and or but to of in on at is are was were be been it its this that these those i you he she "
           "we they me him her us them my your his our their not no so if then than as for with by from about "
           "just very too also do does did have has had can could would should will am what who why how when "
           "where which there here".split())


def words(text):
    return {w.rstrip("s") for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP and len(w) > 2}


def too_similar(text, previous):
    """True when a line mostly re-uses the content words or word triples of an earlier line
    (same joke, same accusation, same vote speech)."""
    w, g = words(text), grams(text)
    if len(w) < 6:          # short natural lines share names and verbs by nature; only a real re-run counts
        # the same few words said again, almost unchanged
        return len(w) >= 3 and any(len(w ^ words(q)) <= 1 for q in previous)
    return any(len(w & words(q)) / len(w) >= 0.6 or (g and len(g & grams(q)) / len(g) >= 0.35) for q in previous)


LOOP_STOP = set("""a an the and or but if so of to in on at by for with from as is are was were be been being am i me
my mine you your yours he him his she her hers it its we us our they them their this that these those what which who
whom whose do does did done not no nor than then there here just only also too very can could would should will shall
may might must have has had having one get got let lets dont didnt isnt wasnt wont cant about all any some more most
again still now yes yeah well really even ever every much many like say said quite clearly""".split())


def content_words(text, names=()):
    """A line's content words in order: lowercase, no stop words, no player names, crude stems (voting -> vot)."""
    t = re.sub(r"['’](s|re|m|ve|ll|d|t)\b", "", text.lower())
    out = []
    for w in re.findall(r"[a-z]+", t):
        if len(w) < 3 or w in LOOP_STOP or w in names:
            continue
        for suf in ("ing", "ed", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 4:
                w = w[:-len(suf)]
                break
        out.append(w)
    return out


def loops(text, earlier, names=()):
    """A day line that circles back to the speaker's own earlier lines of the same day (one player said "her card will
    settle my claim" five times): 60% or more of its content words (at least four) are in one earlier line, or it uses a
    pair of adjacent content words for the third time that day. Tuned on recorded games to catch about 2% of day
    lines."""
    seq = content_words(text, names)
    a = set(seq)
    prev = [content_words(q, names) for q in earlier]
    if len(a) >= 4 and any(len(a & set(b)) / len(a) >= 0.6 for b in prev):
        return True
    used = Counter(pair for b in prev for pair in set(zip(b, b[1:])))
    return any(used[pair] >= 2 for pair in set(zip(seq, seq[1:])))


def opener(text):
    """The first three words of a host remark, lowercase, for the opener check ("sol's out, and")."""
    return " ".join(re.findall(r"[a-z0-9']+", (text or "").lower().replace("’", "'"))[:3])


HOST_BAN = re.compile(r"\b(nobody|no one|no-one|everyone|everybody)\b|\bthe (table|town)(['’]s)? still\b|"
                      r"saw (it|that) coming|\bchairs?\b", re.I)


def host_bad(text, before):
    """A host remark that speaks for the table or repeats itself ("nobody saw it coming" five times in one game,
    "chair", "the town still hasn't ..."): a banned phrase, or a run of three words shared with an earlier remark."""
    if HOST_BAN.search(text):
        return True
    w = re.findall(r"[a-z0-9']+", text.lower().replace("’", "'"))
    runs = {tuple(w[i:i + 3]) for i in range(len(w) - 2)}
    for t in before:
        v = re.findall(r"[a-z0-9']+", t.lower().replace("’", "'"))
        if runs & {tuple(v[i:i + 3]) for i in range(len(v) - 2)}:
            return True
    return False


def names_self(name, text):
    """The speaker uses their own name as a word ("Luna's warning was the only honest thing she said", said by Luna)."""
    return bool(re.search(rf"\b{re.escape(name)}\b", text or "", re.I))


# a day line; claims 30, last words / notes / ghost / before the game 25, confessions 30
DAY_WORDS = 20 if NATURAL else 30


def trim(text, limit=DAY_WORDS):
    """Cut a rambling line to `limit` words; the reply format tells every player the limit.
    Day lines 20, claims, last words, notes, ghost lines and confessions 25 to 30.
    Over the limit (a hard cut left many lines ending in "…"): cut at the last sentence end; else at the last
    clause break (comma, semicolon, colon, dash) in the second half of the limit, closed with a full stop; only if there
    is neither, cut hard with "…"."""
    w = text.split()
    if len(w) <= limit:
        return text
    head = " ".join(w[:limit])
    m = list(re.finditer(r"[.!?][\"')\]”’]*(?=\s|$)", head))
    if m:
        return head[:m[-1].end()]
    half = len(" ".join(w[:max(1, limit // 2)]))
    breaks = [b for b in re.finditer(r"\s*(?:[,;:]|\s[—–-]{1,2})(?=\s|$)", head) if b.start() >= half]
    if breaks:
        return head[:breaks[-1].start()].rstrip(" ,;:—–-") + "."
    return head + "…"


def over_limit(text, limit=None):
    """A SAY line longer than its limit (a claim may run to 30), so act() asks once more before trim() cuts it (cut
    lines ending in "…" read badly)."""
    lim = limit or DAY_WORDS
    return len((text or "").split()) > (max(lim, 30) if is_claim(text) else lim)


def fit(text, limit):
    """`text` if it fits in `limit` words, else its longest run of whole sentences that fits, else "" (the host is never
    shown cut)."""
    w = text.split()
    if len(w) <= limit:
        return text
    head = " ".join(w[:limit])
    m = list(re.finditer(r"[.!?][\"')\]”’]*(?=\s|$)", head))
    return head[:m[-1].end()] if m else ""


def spoken(text, kind="say"):
    """A line a viewer can read, or "" (silence). act() falls back to the whole raw reply when SAY is empty, so a line
    could read "MONOLOGUE: ... SAY: NOTE: none"; Gemma also wrote "[death remains]". Dropped: a format label, no word of
    three letters, a line wholly in brackets, parentheses or asterisks, "none"; for ghost and note lines also a line
    that only says nobody can hear them."""
    text = (text or "").strip().strip('"').strip()
    if (re.search(r"\b(MONOLOGUE|SAY|NOTE|FORGET|LEAN)\s*:", text) or not re.search(r"[A-Za-z]{3}", text)
            or re.fullmatch(r"\[[^\]]*\]|\([^)]*\)|\*[^*]*\*", text) or re.fullmatch(r"(none|n/?a)\W*", text, re.I)):
        return ""
    if kind in ("ghost", "note") and (re.search(r"can(no|['’])?t hear|(nobody|no one)( here)? (can )?hears?\b|"
                                                r"(nobody|no one) is listening", text, re.I)
                                      or re.fullmatch(r"(nothing|no note|nothing to say)\W*", text, re.I)):
        return ""
    return text


def near_verbatim(text, previous, ratio=0.8):
    """True when a line says one of `previous` again almost word for word (the repeat guard for claims: restating a
    claim in new words passes, saying the same sentence again does not)."""
    w = re.findall(r"[a-z']+", text.lower())
    return any(difflib.SequenceMatcher(None, w, re.findall(r"[a-z']+", q.lower())).ratio() >= ratio for q in previous)


def overused(lines, n=3):
    """Word pairs that appear in three or more of a player's lines (their tics)."""
    seen = Counter()
    for l in lines:
        w = [x for x in re.findall(r"[a-z']+", l.lower())]
        seen.update({" ".join(w[i:i + 2]) for i in range(len(w) - 1)})
    return [b for b, c in seen.most_common() if c >= n and not all(x in STOP for x in b.split())][:5]


def majority(leans, alive):
    """The player a strict majority of the `alive` players leans on, or None. `leans`: {who: on whom}."""
    top = Counter(leans.values()).most_common(1)
    return top[0][0] if top and top[0][1] >= alive // 2 + 1 else None


def vote_ready_at(says, alive, day=1):
    """Replay of the vote-when-ready rule on a day's lines [(speaker, lean or None)] with `alive` living players: the
    line (1-based) after which the vote would start its two answers, or None. Used by tests.py on the recorded games.
    The rule: the majority holds for half a round (ceil(alive / 2) lines), everyone has spoken twice on day 1, once
    later."""
    leans, spoke, held, heat = {}, Counter(), 0, None
    for i, (who, lean) in enumerate(says, 1):
        spoke[who] += 1
        if lean:
            leans[who] = lean
        else:
            leans.pop(who, None)
        hot = majority(leans, alive)
        # the line that forms the majority starts the count
        held = held + 1 if hot is not None and hot == heat else 0
        heat = hot
        if heat and held >= -(-alive // 2) and len(spoke) >= alive and min(spoke.values()) >= (2 if day == 1 else 1):
            return i
    return None


def killers_win(killers, others, mayor=False):
    """The killers' win by the numbers: they outnumber the rest (or equal it with --parity), or it is 1 v 1 without the
    mayor (the vote ties forever and a self-saving doctor never dies: one game ran to day 18; the Greek parity ending
    decides it, and the mayor's double vote still wins a 1 v 1). winner() and the ENDGAME warning both ask this."""
    return killers > others or (not OUTNUMBER and killers == others) or (killers == 1 == others and not mayor)


def accuses(line, name):
    """True when a line actually accuses `name` (not merely addresses them)."""
    n = re.escape(name)
    return bool(re.search(
        rf"\b{n}\b[^.?!]{{0,40}}\b(is|was|'s)\b[^.?!]{{0,25}}\b(killer|lying|hiding|suspicious|the one)\b"
        rf"|\b(vote|voting|vote for|voting for|it'?s|watch|suspect|on)\s+{n}\b|\bit'?s you,?\s+{n}\b"
        rf"|\bkiller\b[^.?!]{{0,20}}\b{n}\b", line, re.I))



def agrees(say, proposal, players):
    """A partner's whisper that says yes and names nobody but the proposal means the proposal."""
    others = [p for p in mentions(say, players) if p is not proposal]
    return bool(re.search(r"\b(agree|agreed|fine|works|yes|ok|okay|deal|sure)\b", say, re.I)) and not others


def rotation(i, seats):
    """--games: the draw for game i, a cyclic Latin square: seat j holds card (j - i) mod n of the deal, so over n games
    (n = seats at the table) every seat holds every card (hidden killer, shown killer, officer, doctor, each citizen
    card) exactly once. --killer NAME disables it."""
    n = len(seats)
    ordered = ROLE_LIST + ["citizen"] * (n - len(ROLE_LIST))
    return {s["name"]: ordered[(j - i) % n] for j, s in enumerate(seats)}


def mentions(text, players):
    """Players named in text, in order of first mention."""
    hits = [(m.start(), p) for p in players for m in [re.search(rf"\b{p['name']}\b", text, re.I)] if m]
    return [p for _, p in sorted(hits, key=lambda h: h[0])]


def history_lines(files, me):
    """What a regular remembers of the earlier games of this evening (last three at most): who the killers were, which
    side won and whether `me` won, the officer and what happened to them, and what happened to `me` and who voted `me`
    out. Facts only, no quotes of anyone's lines. "" when there is nothing to remember."""
    rows = []
    for f in files[-3:]:
        try:
            ev = json.load(open(f))
        except (OSError, ValueError):
            continue
        cast = {p["name"]: p["role"] for p in ev[0]["players"]}
        end = [e for e in ev if e["type"] == "end"]
        if me not in cast or not end or end[-1]["winner"] not in ("town", "killer", "jester"):
            continue
        day, fate, last = "", {}, []
        for e in ev:
            if e["type"] == "phase":
                day = e["text"].lower()
            if e["type"] == "votes":
                last = e["votes"]                   # the deciding ballots (the runoff, if there was one)
            if e["type"] == "death":
                voters = [a for a, b, _ in (last or []) if b == e["name"]]
                by = f" by {', '.join(voters)}" if voters and not SECRET else ""
                fate[e["name"]] = f"killed on {day}" if e["how"] == "night" else f"voted out on {day}" + by
        shown = {e["name"]: e.get("role") is not None for e in ev if e["type"] == "death"}
        killers = [n for n, r in cast.items() if r in EVIL]
        winner = end[-1]["winner"]
        won = (winner == "killer") == (cast[me] in EVIL) if winner != "jester" else cast[me] == "jester"
        mine = cast[me]
        # One line per game from this player's side (a player said the table "still got it wrong" when it had been
        # right about him; Gemma said "face down like last time" when her card had been turned): role, how and when out,
        # whether the card was shown, whether the table was right about them, who won.
        row = f"Game {len(rows) + 1}: you were {'a citizen' if mine == 'citizen' else 'the ' + mine}"
        if me in fate:
            row += f"; you were {fate[me]}, card {'shown' if shown.get(me) else 'not shown'}"
            if fate[me].startswith("voted"):
                row += ("; the table was right about you" if mine in EVIL else "; the table was wrong about you")
        else:
            row += "; you were still in at the end" + ("; the table never caught you" if mine in EVIL else "")
        others = [k for k in killers if k != me]
        row += (f"; the killers were you and {' and '.join(others)}" if mine in EVIL and others else
                f"; the killers were {' and '.join(killers)}" if mine not in EVIL else "")
        # how the killers ended, in plain words (a player said "Haiku and Gemma killed us" when both had been voted out
        # and the town had won)
        ends = {k: ("voted out" if fate.get(k, "").startswith("voted") else
                    "killed" if k in fate else "still in at the end")
                for k in killers}
        if len(killers) > 1 and len(set(ends.values())) == 1:
            row += f"; {'both' if len(killers) == 2 else 'all'} were {ends[killers[0]]}"
        elif killers:
            row += "; " + ", ".join(f"{'you' if k == me else k} {'were' if k == me else 'was'} {e}"
                                    for k, e in ends.items())
        row += "; " + {"town": "the town won", "killer": "the killers won", "jester": "the jester won"}[winner] \
               + f", so you {'won' if won else 'lost'}."
        rows.append(row)
    return ("You have played at this table before tonight (the same players, new cards every game). "
            "What you remember:\n" + "\n".join(rows)) if rows else ""


class DayFloor:
    """The state of one day's open talk: who has spoken, who is owed an answer, and how the majority lean holds.

    Vote when ready: once most of the table leans on one player, that player answers twice, someone replies, and the
    talk ends early. Otherwise the day runs until its line budget is spent.
    """

    def __init__(self, alive, budget):
        self.alive = alive
        self.budget = budget
        self.left = budget          # lines left before the vote
        self.beat = 0               # turns handed out so far, passes included
        self.last = None            # who took the last turn
        self.spoke_at = {}          # name -> beat of their last turn
        self.spoke_n = {}           # name -> lines said today
        self.owed = []              # [(player, by, line)]: a player just named gets the next slot
        self.owed_streak = {}       # how many times in a row the same player has been owed
        self.interjected = False    # a third voice just broke a ping-pong
        self.heat = None            # the player most of the table leans on, if any
        self.held = 0               # lines in a row the current majority lean has held
        self.answered = 0           # answers the leaned-on player has given since the table could vote
        self.answered_for = None    # the player those answers count for
        # Worked out again at the start of every turn by begin_turn.
        self.silent, self.owed_by, self.pingpong, self.quiet, self.behind, self.ready = [], {}, False, [], [], False

    def weight(self, pool):
        """A random player from the pool, favouring whoever has waited longest since their last turn."""
        return random.choices(pool, [1 + self.beat - self.spoke_at.get(x["name"], -2) for x in pool])[0]

    def others(self):
        """Everyone but the last speaker (everyone, if that leaves nobody)."""
        return [p for p in self.alive if p is not self.last] or self.alive

    def begin_turn(self, n, today, leans):
        """Count a new turn and work out how the table stands before anyone is picked."""
        self.beat += 1
        alive = self.alive
        self.silent = [p for p in alive if p["name"] not in self.spoke_at]
        self.owed_by = {o[0]["name"]: o for o in self.owed}
        recent = [l.partition(": ")[0] for l in today if not l.startswith("Narrator:")][-3:]
        self.pingpong = (bool(self.owed) and len(recent) == 3 and recent[0] == recent[2]
                         and self.owed[0][0]["name"] == recent[1])
        hot = next((x for x in alive if x["name"] == majority(leans, len(alive))), None)
        if hot is not self.heat:
            self.held = 0
            # A majority that drops for a line and comes back keeps its answers.
            if hot is not None and hot is not self.answered_for:
                self.answered, self.answered_for = 0, hot
            self.heat = hot
        # Quiet: has not yet had a fair share (twice on day 1, once on later days).
        self.quiet = [p for p in alive if self.spoke_n.get(p["name"], 0) < (2 if n == 1 else 1)]
        # Behind: the floor goes mostly to whoever was just named, so a seat nobody names falls behind. A player two
        # lines under the day's average, or under half the busiest seat, is behind.
        mean = sum(self.spoke_n.values()) / len(alive)
        top = max(self.spoke_n.values(), default=0)
        low = [p for p in alive if p["name"] in self.spoke_at
               and (self.spoke_n.get(p["name"], 0) <= mean - 2 or 2 * self.spoke_n.get(p["name"], 0) < top)]
        self.behind = [p for p in low if p is not self.last]
        # Ready: the majority lean has held for half a round (a line per two living players) and nobody is quiet.
        # A stricter gate fired on few days, and most days ran to the budget with the leans long settled.
        self.ready = NATURAL and self.heat is not None and not self.quiet and self.held >= -(-len(alive) // 2)


class Game:
    def __init__(self):
        self.players = []
        for seat, path in enumerate(seat_files()):
            meta, persona = load(path)
            self.players.append({"name": meta["name"], "model": meta["model"], "persona": persona,
                                 "effort": meta.get("effort"), "tic": meta.get("tic", ""),
                                 "tagline": meta.get("tagline", ""), "seat": seat,
                                 "alive": True, "notes": []})
        self.rules = RULES                           # build_rules() at import: the flags and the seat count
        # earlier games of this evening (--games, --history): in the system prompt
        for p in self.players:
            p["history"] = history_lines(HISTORY, p["name"]) if HISTORY else ""
            # the line before the cards sees only the last game (tallies across games came out wrong, "two killer wins
            # for Haiku's team" when the killers had lost both)
            p["history_last"] = (history_lines(HISTORY[-1:], p["name"]).replace("\nGame 1:", "\nThe last game:")
                                 if HISTORY else "")
        self.before = []                             # the one line each player says before the cards (with history)
        gm_meta, self.gm_persona = load(HERE / "gamemaster.md")
        self.gm = {"name": "Narrator", "model": gm_meta["model"], "effort": gm_meta.get("effort")}

        self.deal()
        self.shown = None
        killers = [p for p in self.players if p["role"] in EVIL]
        if len(killers) > 1:                       # Palermo: the officer is shown one of the killer's side at the start
            self.show_one_killer(killers)
        for p in self.players:
            if p["role"] == "mayor":
                p["notes"].append("You are the MAYOR: your vote counts double and the tally shows it, so after the "
                                  "first vote everyone knows. The killers will want you gone; the doctor may guard "
                                  "you.")
        self.jester_won = None

        self.public, self.events, self.t0 = [], [], time.time()
        self.today, self.vote_log, self.day_no, self.last_victim = [], [], 0, None
        self.ballot_log = []                         # every vote, runoffs too: (day, runoff, [(voter, target, weight)])
        stamp = TAG or datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ("-dry" if DRY else "")
        self.files = [HERE / "games" / f"{stamp}.json"] + ([] if FAST else [HERE / "games" / "latest.json"])
        self.files[0].parent.mkdir(exist_ok=True)
        self.lock = threading.Lock()
        self.phase_name = "opening"
        self.emit({"type": "cast", "dry": DRY, "roles": ROLES, "seed": SEED, "game_seed": GAME_SEED,
                   "outnumber": OUTNUMBER, "hide_night": HIDE_NIGHT, "hide_vote": HIDE_VOTE,
                   "players": [{**{k: p[k] for k in ("name", "model", "role", "seat", "tagline")},
                                "shown": p.get("shown", False)}
                               for p in self.players]})

    def deal(self):
        """Give every seat a card. The deal is at random from the game's seed (main() seeds each game from --seed and
        the game number), redrawn while the killer pair or the officer is the same as in the previous game of the
        evening (PREV). A fixed rotation made two evenings open almost line for line alike."""
        n = len(self.players)
        if len(ROLE_LIST) > n:
            sys.exit(f"--roles: {len(ROLE_LIST)} roles for {n} players")
        for _ in range(200):
            roles = ROLE_LIST + ["citizen"] * (n - len(ROLE_LIST))
            random.shuffle(roles)
            if ROTATE:                                 # a fixed draw (rotation(), tests only)
                roles = [ROTATE[p["name"]] for p in self.players]
            for p, role in zip(self.players, roles):
                p["role"], p["checks"] = ("officer", False) if role == "police" else (role, officer_checks())
            if KILLER:
                forced = (next((p for p in self.players if p["name"] == KILLER), None)
                          or sys.exit(f"--killer: no player named {KILLER}"))
                current = next(p for p in self.players if p["role"] == "killer")
                forced["role"], current["role"] = "killer", forced["role"]
            pair = {p["name"] for p in self.players if p["role"] in EVIL}
            officer = next((p["name"] for p in self.players if p["role"] == "officer"), None)
            if ROTATE or not PREV or (pair != PREV.get("pair") and (officer is None or officer != PREV.get("officer"))):
                break

    def show_one_killer(self, killers):
        """Pick the killer shown to the officer (the accomplice, if there is one) and tell the killers and the officer
        what they know from the start."""
        acc = next((k for k in killers if k["role"] == "accomplice"), None)
        self.shown = acc or random.choice([k for k in killers if k["name"] != KILLER] or killers)
        if SHOWN:                                  # a forced shown seat (lab.py, tests)
            forced = next((p for p in self.players
                           if p["name"] == SHOWN and p is not self.shown and p["name"] != KILLER), None)
            if forced and forced["role"] != "killer":
                forced["role"], self.shown["role"] = "killer", forced["role"]
                self.shown = forced
            killers = [p for p in self.players if p["role"] in EVIL]
        self.shown["shown"] = True
        for p in killers:
            mates = ", ".join(k["name"] for k in killers if k is not p)
            if p is acc:
                p["notes"].append(f"The killer is {mates}; you are the ACCOMPLICE, SHOWN to the officer from the "
                                  "start, so the officer will steer votes at you. You cannot kill, but you whisper "
                                  f"with {mates} at night, vote and lie for them. Stay under the radar, give the "
                                  "table no reason, and work out who the officer is: that is the night target.")
            elif p is self.shown:
                p["notes"].append(f"The killers are you and {mates}. You are the SHOWN killer: the officer knows "
                                  f"you from the start. {mates} is HIDDEN.")
            else:
                p["notes"].append(f"The killer{'s are you and' if not acc else ' is you, with'} {mates}. "
                                  f"{self.shown['name']} is the SHOWN {'accomplice' if acc else 'killer'}: the "
                                  f"officer knows {self.shown['name']} from the start. You are HIDDEN.")
        for p in self.players:
            if p["role"] == "officer":
                p["notes"].append(f"At the start you were shown {self.shown['name']}: {self.shown['name']} is "
                                  f"{self.shown_word()}. The {'' if acc else 'other '}killer is hidden.")

    # ---------------------------------------------------------------- events -> UI file + console
    def emit(self, event):
        event["t"] = round(time.time() - self.t0, 1)
        with self.lock:
            self.events.append(event)
            data = json.dumps(self.events, indent=1)
            for f in self.files:
                f.write_text(data)
        text = event.get("text", "")
        if event["type"] == "thought":
            print(f"\033[2m   ({event['name']} thinks: {text})\033[0m", flush=True)
        elif event["type"] == "say":
            print(f"{event['name']}: {text}", flush=True)
        elif event["type"] == "whisper":
            print(f"\033[2m   {event['name']} whispers to {event['to']}: {text}\033[0m", flush=True)
        elif event["type"] == "gm" and event.get("aside"):
            print(f"\033[1m   (host) {text}\033[0m", flush=True)
        elif event["type"] in ("gm", "phase"):
            print(f"\033[1m{text}\033[0m", flush=True)
        elif event["type"] == "note":
            print(f"{event['name']} (note): {text}", flush=True)
        elif event["type"] == "ghost":
            print(f"\033[2m   {event['name']} (out, to the audience): {text}\033[0m", flush=True)
        elif event["type"] not in ("cast", "clock"):
            print(f"   [{event['type']}] {json.dumps({k: v for k, v in event.items() if k not in ('type', 't')})}",
                  flush=True)
        if DRY and not FAST and event["type"] in ("say", "gm", "thought", "votes", "death", "note", "ghost"):
            time.sleep(1.2 if event["type"] != "thought" else 0.6)

    def say(self, p, text, reply_to=None, why="", slot=None, lean=None, claim=True):
        self.public.append(f"{p['name']}: {text}")
        self.today.append(f"{p['name']}: {text}")
        # a living player or absent
        lean = lean if any(x["name"] == lean and x["alive"] for x in self.players) else None
        ev = {"type": "say", "name": p["name"], "text": text, "why": why, **({"slot": slot} if slot else {}),
              **({"lean": lean} if lean else {}), **({"claim": "officer"} if claim and is_claim(text) else {})}
        if reply_to:
            ev["reply_to"] = reply_to["name"]
        self.emit(ev)

    def alive(self, exclude=None):
        return [p for p in self.players if p["alive"] and p is not exclude]

    def dead_line(self):
        dead = [f"{p['name']} "
                f"({'card not shown, ' if self.face_down(p) else 'the ' + p['role'] + ', '}{p.get('how', 'out')})"
                for p in self.players if not p["alive"]]
        return "Out of the game: " + ", ".join(dead) if dead else ""

    # ---------------------------------------------------------------- one model call for a player
    def system(self, p, blind=False):
        """The one fixed system prompt: rules, stakes, how to talk, the persona, and earlier games of the evening (for
        the line before the cards, `blind`, only the last game)."""
        hist = p.get("history_last" if blind else "history")
        return f"{self.rules}\n\nYou are {p['name']}.\n{p['persona']}" + (f"\n\n{hist}" if hist else "")

    def act(self, p, task, out, candidates=None, clock="", extra="", limit=None, kind="say", blind=False,
            fallback=None):
        """Ask p to do `task`; returns {"thought", "text", "pick"}. Bad/empty answers degrade safely. `kind` (say, note,
        ghost) picks the junk filter for a SAY line; a dropped line is silence with r["junk"] set. `blind`: the line
        before the cards gets no role, no role knowledge and no notes, only who sits at the table."""
        prompt = self.act_prompt(p, task, out, clock, extra, limit, blind)
        if SHOW_PROMPT == p["name"]:
            if not p.get("system_shown"):
                p["system_shown"] = True
                system = self.system(p)
                print(f"\033[35m----- system prompt for {p['name']} ({len(system.split())} words) "
                      f"-----\n{system}\n-----\033[0m", flush=True)
            print(f"\033[36m----- prompt for {p['name']} -----\n{prompt}\n-----\033[0m", flush=True)
        if DRY:
            return self.dry(p, out, candidates)
        reply = ask(p, self.system(p, blind), prompt)
        # One more try with the same prompt, no new text, for a line that names its speaker or runs too long. A line
        # still too long is cut by trim().
        if out == "SAY" and names_self(p["name"], field(reply, "SAY") or reply):
            print(f"   [{p['name']} named themselves; asking again] {field(reply, 'SAY')[:80]!r}", flush=True)
            reply = ask(p, self.system(p, blind), prompt)
        if out == "SAY" and over_limit(spoken(field(reply, "SAY") or reply, kind), limit):
            print(f"   [{p['name']} over the word limit; asking again] "
                  f"{(field(reply, 'SAY') or reply)[:80]!r}", flush=True)
            reply = ask(p, self.system(p, blind), prompt)
        r = self.read_reply(p, reply, out, limit, kind)
        if r["thought"] and not too_similar(r["thought"], p.setdefault("thoughts", [])):
            p["thoughts"].append(r["thought"])
            self.emit({"type": "thought", "name": p["name"], "text": r["thought"]})
        if p["alive"] and not blind:                     # the dead keep no notes
            self.remember(p, field(reply, "NOTE"), field(reply, "FORGET"))
        if candidates:
            r["pick"] = pick_name(r["text"] or reply, candidates, fallback)
        return r

    def act_prompt(self, p, task, out, clock, extra, limit, blind):
        """The prompt for one act() call: what p knows, the task, and the reply format."""
        if blind:
            players = ", ".join(x["name"] + (" (you)" if x is p else "") for x in self.players)
            return (f"WHAT YOU KNOW FOR SURE:\nPlayers at the table: {players}."
                    f"\nNo card of the new game is dealt yet: you have no role yet.\n\nNOW: {task}\n" + FORMAT
                    + f"SAY: <your line, at most {limit or DAY_WORDS} words>")
        # earlier days' own lines (today's are in the transcript), and today's own lines listed apart
        own = [l.split(": ", 1)[1] for l in self.public if l.startswith(p["name"] + ": ") and l not in self.today][-3:]
        mine = [l.split(": ", 1)[1] for l in self.today if l.startswith(p["name"] + ": ")]
        say = out == "SAY"
        return (self.context(p)
                + ("\n\nYOUR LAST LINES (never repeat them):\n" + "\n".join(f"- {l}" for l in own)
                   if own and say else "")
                + ("\n\nYOUR LINES TODAY:\n" + "\n".join(f"- {l}" for l in mine) if mine and say else "")
                + f"\n\nNOW: {task}" + (f" {clock}" if clock else "") + "\n" + FORMAT
                + (f"SAY: <your line, at most {limit or DAY_WORDS} words>\n" if say else f"{out}: <answer>\n") + extra
                + "NOTE: <importance 1-3, 3 = decides the game>: <one new fact worth remembering, like a claim or a "
                  "contradiction; not a vote or death>, or none"
                + ("\nFORGET: <one of your notes that is now wrong>, or none" if p.get("memory") else ""))

    def read_reply(self, p, reply, out, limit, kind):
        """Pull the fields out of a reply. A SAY line is cleaned: PASS and junk become silence, a line that still names
        its speaker is blocked, and the rest is trimmed to the word limit (a claim may run to 30)."""
        text = field(reply, out) or (reply if reply and out == "SAY" else "")
        r = {"thought": field(reply, "MONOLOGUE"), "text": text, "say": spoken(field(reply, "SAY")),
             "lean": field(reply, "LEAN")}
        if re.match(r"pass\b", r["text"], re.I) or len(r["text"]) > 900:
            r["text"] = "" if out == "SAY" else r["text"]
        if out == "SAY":
            raw, r["text"] = r["text"], spoken(r["text"], kind)
            r["junk"] = bool(raw) and not r["text"]
            if r["junk"]:
                print(f"   [{p['name']} junk line dropped: {raw[:80]!r}]", flush=True)
            if names_self(p["name"], r["text"]):          # still in the third person: silence, like a blocked repeat
                r["text"], r["blocked"] = "", True
            # a claim is the game's key line: never cut short
            limit = max(limit or 0, 30) if is_claim(r["text"]) else limit
            r["text"] = trim(r["text"], limit) if limit else trim(r["text"])
        return r

    # ---------------------------------------------------------------- memory: three context levels
    def context(self, p):
        """What a human player has in their head: hard facts, their own notes by importance, and what
        they are hearing right now (today's talk). Earlier days survive only as notes and vote history."""
        facts = [f"Your secret role: {p['role'].upper()}."] + p["notes"]
        facts.append("Players in the game: "
                     f"{', '.join(x['name'] + (' (you)' if x is p else '') for x in self.alive())}.")
        if self.dead_line():
            facts.append(self.dead_line() + ".")
        facts += self.testimony()
        killers = sum(x["role"] == "killer" for x in self.alive())
        # the town counts only the killers it has seen leave (a face-down card gives nothing away)
        if p["role"] not in EVIL:
            seen_out = sum(x["role"] == "killer" and not x["alive"] and not self.face_down(x) for x in self.players)
            killers = ROLE_LIST.count("killer") - seen_out
        # one wrong vote and one night kill away from the killers' win (the mayor may be the one lost)
        others = len(self.alive()) - killers
        if killers and self.phase_name.startswith("Day") and self.winner() is None and killers_win(killers, others - 2):
            facts.append(f"ENDGAME: {len(self.alive())} players left. If the town votes wrong "
                         f"today{', or nobody is voted out' if killers_win(killers, others - 1) else ''}, the "
                         f"killer{'s' if killers > 1 else ''} can win.")
        if self.claims():
            facts.append("Officer claims so far: "
                         + ", ".join(f"{who} (day {d}{self.card(who)})" for who, d in self.claims().items()) + ".")
        facts += self.ballot_lines()
        notes = sorted(p.get("memory", []), key=lambda m: (-m["level"], m["day"]))
        heard = self.today
        if MEMORY == "transcript":   # variant B: a perfect transcript, no notes (the first memory design)
            return ("WHAT YOU KNOW FOR SURE:\n" + "\n".join(facts)
                    + "\n\nEVERYTHING SAID SO FAR:\n" + ("\n".join(self.public[-80:]) or "(nothing yet)"))
        if MEMORY == "short":        # variant C: only the last few lines are 'heard'; notes carry the rest
            heard = heard[-6:]
        return ("WHAT YOU KNOW FOR SURE:\n" + "\n".join(facts)
                + "\n\nWHAT YOU REMEMBER (your own notes, most important first):\n"
                + ("\n".join(f"[{'!' * m['level']}] {m['text']}" for m in notes) or "(nothing yet)")
                + f"\n\nWHAT YOU HEAR NOW ({self.phase_name}" + (", last lines only" if MEMORY == "short" else "")
                + "):\n"
                + ("\n".join(heard) or "(nothing yet)") + self.lean_line())

    def remember(self, p, note, forget):
        mem = p.setdefault("memory", [])
        if forget and forget.lower().strip(".") not in ("none", "nothing", "n/a", "-"):
            words = set(re.findall(r"\w+", forget.lower()))
            scored = [(len(words & set(re.findall(r"\w+", m["text"].lower()))) / max(1, len(words)), m) for m in mem]
            if scored and max(scored, key=lambda x: x[0])[0] >= 0.5:
                mem.remove(max(scored, key=lambda x: x[0])[1])
        m = re.match(r"(?:importance\s*)?([123])(?:\s*[:\-\u2013,]\s*|\s+)(.+)", note or "", re.S)
        text = (m.group(2) if m else note or "").strip()
        # the vote log already holds who voted whom; a note about a vote is kept only if it is about a claim or a lie
        if (re.search(r"\bvot(e|ed|es|ing)?\b", text, re.I) and self.vote_log
                and not re.search(r"\b(claim|officer|doctor|lie|lied|switch|flip|chang)", text, re.I)):
            text = ""
        if text and text.lower().strip(".") not in ("none", "nothing", "n/a", "-") and len(text) < 220:
            w = set(re.findall(r"\w+", text.lower())) - {"the", "a", "is", "and", "to", "of", "was", "that", "not"}
            known = [m2["text"] for m2 in mem] + p["notes"]
            names = {x["name"].lower() for x in self.players}
            def dup(other):   # same people, mostly the same words -> the same memory
                o = set(re.findall(r"\w+", other.lower()))
                return (w & names) == (o & names) and len(w & o) / max(1, len(w)) >= 0.5
            if not any(dup(k) for k in known):
                mem.append({"text": text, "level": int(m.group(1)) if m else 2, "day": self.day_no})
                self.emit({"type": "memory", "name": p["name"], "text": text, "level": mem[-1]["level"]})
        mem.sort(key=lambda x: (-x["level"], -x["day"]))
        del mem[MAX_NOTES:]

    def forget_stale(self):
        """Start of a day: low-importance notes fade, notes only about the dead fade (unless vital)."""
        dead = [x["name"] for x in self.players if not x["alive"]]
        alive = [x["name"] for x in self.alive()]
        for p in self.players:
            keep = []
            for m in p.get("memory", []):
                expired = self.day_no - m["day"] >= NOTE_TTL[m["level"]]
                only_dead = any(re.search(rf"\b{d}\b", m["text"]) for d in dead) and \
                    not any(re.search(rf"\b{a}\b", m["text"]) for a in alive) and m["level"] < 3
                if not expired and not only_dead:
                    keep.append(m)
            p["memory"] = keep

    def dry(self, p, out, candidates):
        others = [x["name"] for x in self.alive(exclude=p)] or ["nobody"]
        x, y = (random.sample(others, 2) if len(others) > 1 else others * 2)
        r = {"thought": random.choice(DRY_THINK).format(x=x, y=y)}
        self.emit({"type": "thought", "name": p["name"], "text": r["thought"]})
        text = random.choice(DRY_SAY).format(x=x, y=y)
        r["text"] = "" if text == "PASS" else f"{p['tic']} {text}".strip()
        r["say"], r["lean"] = "", random.choice([x, "none"])
        if p["alive"]:
            self.remember(p, f"{random.choice((1, 2, 3))}: {x} pushed {y} hard", "none")
        if candidates:
            r["pick"] = random.choice(candidates)
            r["say"] = f"{r['pick']['name']} talks too much." if out == "TARGET" else ""
            r["text"] = f"{p['tic']} I vote {r['pick']['name']}." if out == "VOTE" else r["pick"]["name"]
        return r

    def narrate(self, facts, transcript=True):
        if DRY or not NARRATOR_AGENT:
            text = facts                 # the call sites already carry the final sentences
        else:
            system = f"You are the game master of One Night in Palermo, a party game played by AIs.\n{self.gm_persona}"
            prompt = (("TRANSCRIPT SO FAR:\n" + "\n".join(self.public[-30:]) if transcript else "")
                      + f"\n\nNEW FACTS TO NARRATE: {facts}\nSay this in one or two short plain sentences. "
                        "State every fact above; add nothing beyond them. Reply with the narration only.")
            text = ask(self.gm, system, prompt) or facts
        self.public.append(f"Narrator: {text}")
        self.today.append(f"Narrator: {text}")
        self.emit({"type": "gm", "text": text})

    def aside(self, what, when="", end=False):
        """The host's own voice: one short model remark after a death announcement and at the end, for the viewers only
        (never in what players see). Off in --dry and with --plain-host; a failed call or a junk reply is skipped
        silently. During the game it gets PUBLIC facts only (with more it got counts wrong, invented table moods and
        pointed at a hidden killer): counts, turned cards, the day's tally, claims made aloud, last words; it is told it
        knows no hidden card. At the end (`end`) it gets the full end state. A reply is tried twice and then skipped
        when it reuses an opener or a 3-word run of an earlier aside, or speaks for the table (host_bad())."""
        if PLAIN_HOST or not (end or ASIDES):            # only the closing aside unless --asides
            return
        system = ("You are the host of One Night in Palermo, a party game played by AIs, watched by an audience.\n"
                  f"{self.gm_persona}")
        before = self.earlier_asides() + [e["text"] for e in self.events if e["type"] == "gm" and e.get("aside")]
        openers = list(dict.fromkeys(opener(t) for t in before if opener(t)))
        if end:                                          # one voice line in place of the shape guidance
            prompt = ("WHAT THE TABLE KNOWS (public facts only):\n" + "\n".join(self.host_facts())
                      + ("\n\nYOUR EARLIER REMARKS TONIGHT (do not repeat them):\n"
                         + "\n".join(f"- {t}" for t in before[-12:]) if before else "")
                      + (f"\n\nWHEN: {when}" if when else "") + f"\n\nYou just announced: {what}\n"
                      + "Point out the one irony in how this game ended, as a friend at the table would, in under "
                        "fifteen words. Not the form 'X, and Y'.\nReply with the remark only.")
        else:
            prompt = ("WHAT THE TABLE KNOWS (public facts only):\n" + "\n".join(self.host_facts())
                      + "\nYou do not know anyone's hidden card: only the cards turned above."
                      + ("\n\nYOUR EARLIER REMARKS TONIGHT (do not reuse a phrase or a joke shape from them):\n"
                         + "\n".join(f"- {t}" for t in before[-12:]) if before else "")
                      + (f"\nThey opened with: {'; '.join(openers[-12:])}. Open differently." if openers else "")
                      + (f"\n\nWHEN: {when}" if when else "")
                      + f"\n\nYou just announced: {what}\nOne remark of your own to the audience about what happened: "
                        "the vote, the card, a claim, the last words. Never about what the table feels, notices or "
                        "says. Add no fact, reveal nothing, and do not describe faces, gestures or anything nobody "
                        "could see at this table.\nReply with the remark only, at most 14 words.")
        text = ""
        # a reply that fails a check gets one more try, then no aside
        for _ in range(2):
            try:
                text = spoken(ask(self.gm, system, prompt).strip().strip('"'))
            except Exception:                                   # the host is colour: never let it stop a game
                text = ""
            text = fit(text, 14) if "\n" not in text else ""
            if not text:
                break
            # "Sol's out, and ...": the shape it fell into
            x_and_y = end and re.match(r"\W*[^,.;!?]{1,40}, and\b", text)
            fresh = opener(text) not in openers and not host_bad(text, before) and not near_verbatim(text, before, 0.7)
            if fresh and not x_and_y:
                self.emit({"type": "gm", "text": text, "aside": True})
                return

    def host_facts(self):
        """What the whole table knows, for the host: counts, who is out (cards as shown), claims made aloud, the day's
        tally and what it did, and the last words just said."""
        alive, dead = self.alive(), [p for p in self.players if not p["alive"]]
        rows = [f"Still in: {len(alive)} ({', '.join(p['name'] for p in alive)}). Out: {len(dead)}."]
        if dead:
            rows.append(self.dead_line() + ".")
        if self.claims():
            rows.append("Officer claims made aloud: "
                        + ", ".join(f"{w} (day {d})" for w, d in self.claims().items()) + ".")
        d = self.day_no
        if self.phase_name.startswith("Day") and any(v[0] == d for v in self.vote_log):
            tally = Counter(b for dd, _, b, _ in self.vote_log if dd == d)
            rows.append(f"Day {d} vote: " + ", ".join(f"{n} {c}" for n, c in tally.most_common()) + ". "
                        + self.vote_result(d))
            out = next((p for p in self.players if p.get("how") == f"voted out day {d}"), None)
            if out and out.get("last"):
                rows.append(f'{out["name"]}\'s last words: "{out["last"]}"')
        return rows

    def end_state(self, result):
        """The exact end of the game for the host (it once said "Two killers walked out with the win" when one had
        been voted out): winner, which killers are still in, how it ended."""
        alive_k = [p["name"] for p in self.alive() if p["role"] == "killer"]
        last = self.players and max(self.players, key=lambda p: p.get("out_seq", -1))
        if result == "town" and last.get("out_seq") is not None:
            how = "the last killer, " + last["name"] + ", was " + last.get("how", "out")
        else:
            how = self.why_over(result).strip() + (" The killers win at parity." if not OUTNUMBER else "")
        return ("The game is over: "
                f"{'the town' if result == 'town' else 'the killers' if result == 'killer' else 'the jester'} won. "
                f"Killers still in: {', '.join(alive_k) or 'none'}. How it ended: {how}.").replace("..", ".")

    def earlier_asides(self):
        """The host's remarks in the earlier games of this evening (--games / --history), so it does not repeat a
        joke."""
        out = []
        for f in HISTORY[-3:]:
            try:
                out += [e["text"] for e in json.load(open(f)) if e.get("type") == "gm" and e.get("aside")]
            except (OSError, ValueError):
                continue
        return out

    def recap(self, side):
        """The narrator tells the story of the whole game in a few sentences (for the final card / a post)."""
        if DRY:
            text = f"{side} won. A short game, a long night."
        else:
            system = f"You are the narrator of One Night in Palermo, a party game played by AIs.\n{self.gm_persona}"
            prompt = ("KEY FACTS (each labelled with its day or night; a line marked Claim: is what a player said, "
                      "true or not: tell it as a claim, never as fact):\n"
                      + "\n".join(f"- {f}" for f in self.key_facts())
                      + "\n\nTRANSCRIPT (every line labelled with its day or night):\n"
                      + "\n".join(self.labelled()[-120:])
                      + f"\n\n{side} won. Tell the story of this game in 4-5 short sentences for someone who did "
                        "not watch: the key claim, the big mistake or the brilliant move, the turning point, the "
                        "ending. Name the players. Use the day and night labels exactly as given: talk, claims and "
                        "votes happen by day, kills by night. Plain text, no markdown, no spoilers held back (the game "
                        "is over).")
            text = ask(self.gm, system, prompt) or f"{side} won."
        # the recap once printed the [Day N] labels of the facts it was given
        text = re.sub(r"\s*\[(?:Day|Night|Before night) \d+\]\s*", " ", text).strip()
        self.emit({"type": "recap", "text": text})

    def labelled(self):
        """The public transcript with each line prefixed by its phase ("[Day 2] Gemma: ..."). The night narration that
        announces a death opens the next morning, so it is labelled with the night it happened."""
        rows, phase = [], "Before night 1"
        for l in self.public:
            m = re.match(r"--- (Day|Night) (\d+) ---", l)
            if m:
                phase = f"{m.group(1)} {m.group(2)}"
                continue
            rows.append(f"[{phase}] {l}")
        return rows

    def ballot_lines(self):
        """Every past vote, one line each, grouped by target with the voters named (players misread who voted whom, and
        each misreading cost a citizen): "Day 1 vote: Haiku 5 (Sonnet, Gemma, Sol, Luna, Opus); Gemma 1 (Haiku). Out:
        Haiku (card KILLER)." A runoff has its own line; the last vote of a day says what it did."""
        rows = []
        for i, (d, runoff, ballots) in enumerate(self.ballot_log):
            by = {}
            for a, b, w in ballots:
                by.setdefault(b, [0, []])
                by[b][0] += w
                by[b][1].append(a + (" (mayor, x2)" if w == 2 else ""))
            last = i + 1 == len(self.ballot_log) or self.ballot_log[i + 1][0] != d
            rows.append(f"Day {d} {'runoff' if runoff else 'vote'}: "
                        + ("; " if not SECRET else ", ").join(
                            f"{b} {c}" + ("" if SECRET else f" ({', '.join(v)})")
                            for b, (c, v) in sorted(by.items(), key=lambda kv: -kv[1][0]))
                        + "." + (" " + self.vote_result(d).split(" Got votes")[0] if last else ""))
        return rows

    def vote_result(self, d):
        """What a day's vote did, so ballots cannot be misread (players said "voted out the officer"
        about someone who only got votes): "Out: Gemma (card KILLER). Got votes and stayed in: Sol (2)."."""
        out = next((p for p in self.players if p.get("how") == f"voted out day {d}"), None)
        got = Counter(b for dd, _, b, _ in self.vote_log if dd == d)
        stayed = [f"{n} ({c})" for n, c in got.most_common() if not out or n != out["name"]]
        if out:
            card = "card not shown" if self.face_down(out) else f"card {out['role'].upper()}"
            text = f"Out: {out['name']} ({card})."
        else:
            text = "Out: nobody (tied)."
        return text + (f" Got votes and stayed in: {', '.join(stayed)}." if stayed else "")

    def why_over(self, result):
        """The reason the game ended, for the end narration and the recap ("Two killers and two others are left. ")."""
        k = sum(p["role"] == "killer" for p in self.alive())
        o = len(self.alive()) - k
        if result == "town":
            return "Every killer is out. "
        if result == "killer":
            return (f"{NUMBER.get(k, k).capitalize()} killer{'s' if k > 1 else ''} and {NUMBER.get(o, o)} "
                    f"other{'s' if o != 1 else ''} {'are' if k + o > 1 else 'is'} left. ")
        return ""

    def key_facts(self):
        """What the recap retells: roles, every death with its day or night, every officer claim with its day."""
        facts = ["Roles: " + ", ".join(f"{p['name']} the {p['role']}"
                                       + (" (shown to the officer)" if p.get("shown") else "")
                                       for p in self.players) + "."]
        for p in self.players:
            if not p["alive"]:
                facts.append(f"{p['name']} ({p['role']}) was {p.get('how', 'out')}"
                             + (" (the card was not shown to the table)." if self.face_down(p) else "."))
        # what players said is marked as a claim, what the cards showed as fact (a recap once told a false claim as
        # fact)
        role = {p["name"]: p["role"] for p in self.players}
        facts += [f"Claim: {who} claimed officer in the day-{d} talk (claims are made by day, never at night); "
                  + (f"{who} really was the officer." if role.get(who) == "officer" else
                     f"a false claim: {who} was the {role.get(who)}.")
                  for who, d in self.claims().items()]
        facts += [f'Claim: {p["name"]} said in last words: "{p["last"]}" (said, not proved).' for p in self.players
                  if not p["alive"] and p.get("last") and p.get("how", "").startswith("voted")]
        for d in sorted({v[0] for v in self.vote_log}):
            got = Counter(b for dd, _, b, _ in self.vote_log if dd == d)
            out = next((p["name"] for p in self.players if p.get("how") == f"voted out day {d}"), None)
            facts.append(f"Day {d} vote: " + ", ".join(f"{n} {c}" for n, c in got.most_common())
                         + " (votes per player); " + (f"{out} was voted out." if out else "nobody was voted out."))
        result = self.winner()
        if result in ("town", "killer"):
            killer_rule = ("The killers win when they " + ("outnumber" if OUTNUMBER else "equal or outnumber")
                           + " the rest" + (" or when one killer and one other player are left." if OUTNUMBER else "."))
            rule = {"town": "The town wins.", "killer": killer_rule}[result]
            facts.append(f"The game ended on {self.phase_name.lower()}. {self.why_over(result)}{rule}")
        return facts

    def out(self, p, how):
        p["alive"] = False
        p["out_seq"] = sum(x.get("out_seq") is not None for x in self.players)   # the order players went out
        p["how"] = f"killed night {self.day_no + 1}" if how == "night" else f"voted out day {self.day_no}"
        self.emit({"type": "death", "name": p["name"], "role": None if self.face_down(p) else p["role"], "how": how})

    @staticmethod
    def face_down(p):
        """A dead player whose role nobody learns (until the end): night victims with two killers, voted-out players
        with --hide-vote. A jester voted out always shows the card: that is their win."""
        how = p.get("how", "")
        return (HIDE_NIGHT and how.startswith("killed")
                or HIDE_VOTE and how.startswith("voted") and p["role"] != "jester")

    def parallel(self, jobs):
        # scripted answers draw from one seeded generator: keep the order fixed
        if DRY:
            return [job() for job in jobs]
        with ThreadPoolExecutor(max_workers=8) as pool:
            return list(pool.map(lambda job: job(), jobs))

    def winner(self):
        if self.jester_won:
            return "jester"
        killers = sum(p["role"] == "killer" for p in self.alive())
        if killers == 0:
            return "town"
        if not any(p["role"] not in EVIL for p in self.alive()):
            return "killer"
        if killers_win(killers, len(self.alive()) - killers, any(p["role"] == "mayor" for p in self.alive())):
            return "killer"
        return None

    # ---------------------------------------------------------------- phases
    def intro(self):
        self.phase_name = "opening"
        self.narrate(f"The game begins. {NUMBER.get(len(self.players), str(len(self.players))).capitalize()} players "
                     "sit down at the table: "
                     + ", ".join(p["name"] for p in self.players)
                     + (". Nobody knows who the killers are." if PAIR else ". Nobody knows who the killer is."))
        # no small-talk round (real games go cards → night 1 → day 1); day 1 opens cold, see discussion().
        # With earlier games this evening, each player says one line about the last game before the cards;
        # the table hears these on day 1.
        if any(p.get("history") for p in self.players):
            task = ("The cards for the next game are not dealt yet; nobody has a role. One line to the table about the "
                    "game you all just played.")
            order = random.sample(self.players, len(self.players))   # not seat order every game
            replies = self.parallel([lambda p=p: self.act(p, task, "SAY", limit=25, blind=True) for p in order])
            for p, r in zip(order, replies):
                if r["text"]:
                    self.say(p, r["text"], why="before the game", claim=False)
                    self.before += (["(Said before the cards were dealt:)"] * (not self.before)
                                    + [f"{p['name']}: {r['text']}"])

    def night(self, n):
        """The killers choose, the doctor guards and the officer checks, all at once; then the morning is told."""
        self.phase_name = f"Night {n}"
        self.emit({"type": "phase", "text": f"Night {n}", "kind": "night"})
        self.public.append(f"--- Night {n} ---")
        self.today = list(self.before) if n == 1 else []      # the lines said before the cards are heard on day 1
        # The dead take no part in the night: a voted-out killer cannot whisper a target to a living partner, so a
        # shown card really silences a killer.
        killers = [p for p in self.alive() if p["role"] in EVIL]
        doctors = [p for p in self.alive() if p["role"] == "doctor"]
        officers = [p for p in self.alive() if p["role"] == "officer" and p["checks"]]
        town = [p for p in self.alive() if p["role"] not in EVIL]
        whisper = f"SAY: <one line to your partner, at most {DAY_WORDS} words>\n"   # reply format between the killers
        jobs = self.night_jobs(n, killers, doctors, officers, town, whisper)
        results = [x for r in self.parallel(jobs) for x in (r if isinstance(r, list) else [r])]
        victim, saved = self.night_outcome(results)
        self.night_notes(n, results, victim, saved)
        self.morning(n, victim, saved, killers)

    def night_jobs(self, n, killers, doctors, officers, town, whisper):
        """The night's moves, run together. Each job returns (kind, player, reply) or a list of them."""
        quiet = QUIET_NIGHT and n == 1
        if killers and town and not quiet:
            jobs = [lambda: self.killers_choose(killers, town, whisper)]
        elif killers and len(killers) > 1 and quiet:
            jobs = [lambda: self.killers_meet(killers)]
        else:
            jobs = []
        # A quiet night 1 needs no guard: nobody can die, and the doctor's no-repeat rule would then cost a save on
        # night 2.
        jobs += [lambda p=p: ("save", p, self.act(p, self.save_task(p), "TARGET", self.save_pool(p)))
                 for p in doctors if not quiet]
        jobs += [lambda p=p: ("check", p, self.act(p, "Choose a player to investigate tonight.",
                                                     "TARGET", self.check_pool(p)))
                 for p in officers if self.check_pool(p)]
        return jobs

    def killers_meet(self, killers):
        """Night 1, no kill: the pair meet and plan (one line each; the viewer sees it, the town never)."""
        a, b = sorted(killers, key=lambda k: not k.get("shown"))[:2]
        ra = self.act(a, f"Night 1, nobody dies tonight. Whisper one line to {b['name']}, your partner: your plan for "
                         f"tomorrow.", "SAY")
        self.whisper(a, b, ra)
        rb = self.act(b, f"{a['name']} whispers to you: \"{ra.get('say') or ra['text']}\". One line back.", "SAY")
        self.whisper(b, a, rb)
        return []

    def killers_choose(self, killers, town, whisper):
        """The killers whisper: the shown one proposes, the hidden one answers and gives the final sign."""
        order = sorted(killers, key=lambda k: not k.get("shown"))
        if len(order) == 1:
            return [("kill", order[0], self.act(order[0], "Choose the player to eliminate tonight.", "TARGET", town))]
        a, b = order[0], order[-1]
        ra = self.act(a, f"Whisper to {b['name']}, your partner: who do we eliminate tonight, and why? One line, then "
                         f"your pick.", "TARGET", town, extra=whisper)
        self.whisper(a, b, ra)
        self.emit({"type": "night_action", "name": a["name"], "action": "propose", "target": ra["pick"]["name"]})
        rb = self.act(b, f"{a['name']} whispers to you: \"{ra.get('say') or ra['text']}\" and points at "
                         f"{ra['pick']['name']}. Answer in one line, then your pick. If you disagree, your pick "
                         "stands: the hidden killer gives the final sign.", "TARGET", town, extra=whisper)
        if agrees(rb.get("say", ""), ra["pick"], town):
            rb["pick"] = ra["pick"]                  # "agreed" means the proposal, whatever the pick line said
        self.whisper(b, a, rb)
        if rb["pick"] is not ra["pick"]:
            rc = self.act(a, f"{b['name']} whispers back: \"{rb.get('say') or rb['text']}\" and points at "
                             f"{rb['pick']['name']} instead. One line back; their pick stands.", "SAY")
            self.whisper(a, b, rc)
        return [("kill", k, {"pick": rb["pick"]}) for k in order]

    @staticmethod
    def night_outcome(results):
        """The victim (None if nobody was chosen) and the players the doctor protected."""
        kills = [r[2]["pick"] for r in results if r[0] == "kill"]
        victim, tied = plurality(kills) if kills else (None, [])
        victim = victim or (random.choice(tied) if tied else None)   # killers disagree: random pick among their choices
        saved = [r[2]["pick"] for r in results if r[0] == "save"]
        return victim, saved

    def night_notes(self, n, results, victim, saved):
        """Each night actor remembers what they did and learned; the viewer gets one event per action."""
        for kind, p, r in results:
            t = r["pick"]
            result = {}
            if kind == "kill":
                who = "you" if p["role"] == "killer" else "the killer"
                if any(x is victim for x in saved):
                    end = "."
                elif HIDE_NIGHT:
                    end = " and killed them."
                else:
                    end = f" and killed them: they were the {victim['role']}."
                p["notes"].append(f"Night {n}: {who} chose {victim['name']}" + end)
            elif kind == "save":
                p["notes"].append(f"Night {n}: you protected {t['name']}.")
                p["last_save"] = t["name"]
            else:
                if t["role"] == "killer":
                    verdict = "a KILLER" if PAIR else "the KILLER"
                else:
                    verdict = "NOT a killer" if PAIR else "NOT the killer"
                p["notes"].append(f"Night {n}: you checked {t['name']}: {verdict}.")
                result = {"result": verdict}
            self.emit({"type": "night_action", "name": p["name"], "action": kind, "target": t["name"], **result})

    def morning(self, n, victim, saved, killers):
        """Tell the town how the night went: nobody chosen, a save, or a death with an optional note left behind."""
        if victim is None:
            self.last_victim = None
            shown = any(p["role"] == "officer" for p in self.players)
            self.narrate("Night falls on Palermo and everyone closes their eyes. The killers meet in the dark"
                         + (", and the officer is shown one of them" if shown else "")
                         + ". A new day dawns in Palermo. Nobody is out.")
        elif any(s is victim for s in saved):
            for p in killers:
                p["notes"][-1] += f" The doctor protected {victim['name']}."
            self.last_victim = None
            self.narrate(random.choice(["Night falls on Palermo. The killers strike, but the doctor got there first. "
                                        "A new day dawns in Palermo, and nobody is out.",
                                        "Night falls on Palermo. Somebody was marked tonight, and somebody else was "
                                        "watching over them. A new day dawns in Palermo. Nobody is out."]))
        else:
            self.last_victim = victim
            note = ""
            if NIGHT_NOTES:                                # the victim leaves one line for the morning
                note = self.act(victim, "The killers came for you tonight; you are out. You can leave one line behind "
                                        "for the table to find in the morning.", "SAY", limit=25, kind="note")["text"]
            self.out(victim, "night")
            told = (random.choice([f"Night falls on Palermo. A new day dawns in Palermo without {victim['name']}.",
                                   f"Night falls on Palermo and everyone closes their eyes. Not everyone opens them: "
                                   f"{victim['name']} is gone."])
                    + (f" {victim['name']}'s card stays face down." if HIDE_NIGHT
                       else f" {victim['name']} was the {victim['role']}."))
            self.narrate(told)
            if note:
                victim["last"] = note
                self.public.append(f'Narrator: {victim["name"]} left a note: "{note}"')
                self.today.append(self.public[-1])
                self.emit({"type": "note", "name": victim["name"], "text": note})
            self.aside(told + (f' {victim["name"]} left a note: "{note}"' if note else ""),
                       when=f"Night {n}: a night kill.")

    def discussion(self, n, budget=None):
        """One day's open talk: hand out turns until the budget runs out or the table is ready to vote."""
        floor = DayFloor(self.alive(), budget or self.day_budget())
        self.leans = {}
        self.emit_clock(floor)
        while floor.left > 0 and floor.beat < 2 * floor.budget:
            floor.begin_turn(n, self.today, self.leans)
            pick = self.next_speakers(floor, n)
            if pick is None:
                break
            speakers, why = pick
            addressed = [p for p in speakers if p["name"] in floor.owed_by]
            clock = "" if why == "the table leans on them" else f"At most {floor.left} more lines before the vote."
            replies = self.parallel([lambda p=p: self.fresh_line(p, self.turn_task(floor, n, p, why, addressed), clock)
                                     for p in speakers])
            for p, r in zip(speakers, replies):
                self.take_reply(floor, p, r, why)

    def emit_clock(self, floor):
        self.emit({"type": "clock", "left": floor.left, "total": floor.budget, "seconds": SECONDS_PER_MESSAGE})

    def day_not_started(self, n):
        """Day 1 and nobody has spoken yet (only the narrator and the lines said before the cards)."""
        return n == 1 and all(l.startswith("Narrator:") or l in self.before for l in self.today)

    def next_speakers(self, floor, n):
        """Who takes the next turn and why, or None when the table is ready to vote. The rules apply in this order."""
        alive, last, owed, spoke_n, left = floor.alive, floor.last, floor.owed, floor.spoke_n, floor.left
        heat, ready, silent, quiet, behind = floor.heat, floor.ready, floor.silent, floor.quiet, floor.behind
        named = owed[0][0] if owed else None
        # Ready to vote: the leaned-on player has answered twice and someone else spoke last.
        if heat and ready and floor.answered >= 2 and last is not heat:
            return None
        # The majority lean has held: the player it falls on answers.
        if heat and ready and last is not heat:
            return [heat], "the table leans on them"
        # The table is close to a vote: the quiet ones first.
        if heat and quiet and not silent:
            return [random.choice(quiet)], "takes the floor"
        # Everyone gets the floor before the budget runs out, picked at random rather than in seat order (seat 0 used
        # to open most first days). A player still silent may also cut in on a named player who has spoken twice.
        if silent and (left <= len(silent) + 1
                       or (owed and spoke_n.get(named["name"], 0) >= 2 and random.random() < 0.6)):
            return [random.choice(silent)], "hasn't spoken yet"
        # Nobody stays far behind the day's average, unless the player just named is owed the answer.
        if behind and left > 1 and (not (owed and owed[0][1] is last) or random.random() < 0.5):
            furthest = min(behind, key=lambda x: (spoke_n.get(x["name"], 0), floor.spoke_at[x["name"]]))
            return [furthest], "takes the floor"
        if left == 1:
            return [floor.weight(floor.others())], "last word before the vote"
        # Thread fatigue: the same player owed three times running, or holding too much of the day. The table moves on.
        if owed and (floor.owed_streak.get(named["name"], 0) >= 3
                     or (spoke_n.get(named["name"], 0) >= 4
                         and spoke_n[named["name"]] >= 0.35 * max(1, sum(spoke_n.values()))
                         and random.random() < 0.5)):
            floor.owed_streak[named["name"]] = 0
            owed.pop(0)
            return [floor.weight(floor.others())], "moves on"
        # The named player answers, alone.
        if owed and (floor.interjected or not floor.pingpong or random.random() < 0.5 or len(alive) < 4):
            floor.interjected = False
            return [named], f"answers {owed[0][1]['name']}"
        # A third voice breaks an A->B->A ping-pong.
        if owed:
            floor.interjected = True
            return [floor.weight([x for x in alive if x is not last and x is not named])], "interjects"
        if silent and random.random() < 0.5:
            return [random.choice(silent)], "hasn't spoken yet"
        # Open floor. In table talk, sometimes two players react at once, like a real table.
        pool = floor.others()
        speakers = [floor.weight(pool)]
        if NATURAL and left > 3 and len(pool) > 1 and random.random() < 0.5 and not self.day_not_started(n):
            speakers.append(floor.weight([p for p in pool if p is not speakers[0]]))
        return speakers, "takes the floor"

    def turn_task(self, floor, n, p, why, addressed):
        """Whose turn it is and why, never which move to make: the strategy is in RULES."""
        owed, owed_by, left = floor.owed, floor.owed_by, floor.left
        named = f"{owed_by[p['name']][1]['name']} just named you. " if p in addressed else ""
        if why == "the table leans on them":
            return (f"Most of the table leans on you (see LEANS NOW). Answer {floor.answered + 1} of 2, then the vote."
                    if floor.answered < 2 else
                    "Most of the table still leans on you, and you were just named. Your last answer before the vote.")
        if left == 1:
            return named + "Last line before the vote."
        if NATURAL:
            if self.day_not_started(n):
                return "Day 1 just started. Nobody knows anything yet. Open the table."
            if named:
                return named + "Answer in a few words, or PASS (the table sees it)."
            if why == "moves on":
                return "The table is tired of that thread. Bring something new."
            if why == "interjects":
                return f"{owed[0][1]['name']} and {owed[0][0]['name']} are going back and forth. Jump in."
            return "You haven't spoken yet today. Your turn." if p["name"] not in floor.spoke_at else "Your turn."
        # --classic: interrogation prompts that suggest a move.
        if p in addressed:
            _, by, line = owed_by[p["name"]]
            return (f"{by['name']} said: \"{line[:140]}\" and named you. Answer them in one line: deny with a fact, "
                    "turn it around, or ask back. Or PASS, and the table sees that you declined.")
        if p["name"] not in floor.spoke_at and left > 2:
            return ("You haven't spoken today. Name who you suspect and the one thing they DID (a vote, a line, a "
                    "night death), or ask one pointed question. Do not announce a vote yet.")
        if left <= 3:
            return "The vote is close. Say who you vote and the one thing they did, or PASS."
        if why == "interjects":
            target, by, line = owed[0]
            return (f"{by['name']} said to {target['name']}: \"{line[:140]}\". One line about THAT exchange: back one "
                    f"of them, add a fact, or ask one of them a question. {target['name']} answers next.")
        thread = [l for l in self.today if not l.startswith("Narrator:")][-2:]
        if thread:
            return ("The thread right now: " + " / ".join(thread) + ". Stay on it: agree, disagree, or ask one of them "
                    "a question. Only if it is exhausted, bring a new fact (a vote, a line, a night death). Or PASS.")
        return ("You have the floor. Name who you suspect and the one thing they DID (a vote, a line, a night death), "
                "defend yourself with a fact, or claim a role. Or PASS if you have nothing.")

    def take_lean(self, p, r, alive):
        """Read the LEAN line of a reply: a living player's name, or none. Anything else keeps the old lean."""
        lean_line = r.get("lean", "").split("\n")[0]
        lean = next((x for x in alive if x is not p and re.search(rf"\b{x['name']}\b", lean_line, re.I)), None)
        if lean or re.match(r"\W*(none|nobody|no one)\b", r.get("lean", ""), re.I):
            self.leans[p["name"]] = lean["name"] if lean else None
            self.leans = {k: v for k, v in self.leans.items() if v}

    def take_reply(self, floor, p, r, why):
        """Apply one reply: the turn is spent, the lean is read, then either a pass or a line that may name others."""
        alive, owed_by = floor.alive, floor.owed_by
        floor.spoke_at[p["name"]] = floor.beat
        floor.answered += p is floor.heat and floor.ready      # only answers given once the table could vote count
        floor.held += floor.heat is not None
        # a pass is a turn too, so it cannot keep the vote waiting
        floor.last = p
        floor.owed = [o for o in floor.owed if o[0] is not p]  # a slot taken settles the debt, answer or not
        self.take_lean(p, r, alive)
        if not r["text"]:
            # Only a chosen PASS declines; a blocked or junk reply does not.
            declined = p["name"] in owed_by and not r.get("blocked") and not r.get("junk")
            by = owed_by[p["name"]][1] if declined else None
            self.emit({"type": "pass", "name": p["name"], **({"declines": by["name"]} if by else {})})
            if by:
                self.public.append(f"{p['name']}: (declines to answer {by['name']})")
                self.today.append(f"{p['name']}: (declines to answer {by['name']})")
            return
        # A line that opens with a name answers that player; otherwise it answers whoever named the speaker.
        opens_with = next((x for x in alive if x is not p
                           and re.match(rf"(?:\w+(?: \w+)?[.!]\s+)?\W*{x['name']}\b", r["text"], re.I)), None)
        to = opens_with or (owed_by[p["name"]][1] if p["name"] in owed_by else None)
        if floor.left == 1:
            shown_why = "last word before the vote"
        else:
            shown_why = f"answers {to['name']}" if to else why
        self.say(p, r["text"], reply_to=to, lean=self.leans.get(p["name"]), why=shown_why, slot=why)
        floor.left -= 1
        floor.spoke_n[p["name"]] = floor.spoke_n.get(p["name"], 0) + 1
        floor.last = p
        # Players named in the line are owed the next slots (two at most).
        queued = {o[0]["name"] for o in floor.owed}
        named = [x for x in mentions(r["text"], alive) if x is not p and x["name"] not in queued]
        for x in named:
            floor.owed_streak[x["name"]] = floor.owed_streak.get(x["name"], 0) + 1
        for x in alive:
            if x not in named and x is not p and x["name"] not in queued:
                floor.owed_streak[x["name"]] = 0
        floor.owed += [(x, p, r["text"]) for x in named]
        del floor.owed[2:]
        self.emit_clock(floor)

    def lean_line(self):
        """LEANS NOW: who each player would vote right now (public, like hands half-raised at a real table)."""
        if not getattr(self, "leans", None) or not self.phase_name.startswith("Day"):
            return ""
        by = {}
        for who, on in self.leans.items():
            by.setdefault(on, []).append(who)
        rows = sorted(by.items(), key=lambda kv: -len(kv[1]))
        need = len(self.alive()) // 2 + 1
        none = [x["name"] for x in self.alive() if x["name"] not in self.leans]
        return ("\n\nLEANS NOW: " + "; ".join(f"{on} {len(w)} ({', '.join(w)})" for on, w in rows)
                + (f"; no lean: {', '.join(none)}" if none else "") + f". {need} on one player ends the talk soon.")

    def whisper(self, a, b, r):
        """A killer's night line to their partner: the town never hears it, the viewer does."""
        text = r.get("say") or ("" if r.get("pick") and r["text"] == r["pick"]["name"] else r["text"])
        if text:
            self.emit({"type": "whisper", "name": a["name"], "to": b["name"], "text": text})

    def claims(self):
        """Players who said 'I am the officer' in public, with the day they first said it (a fact, so a day-1 claim is
        not forgotten on day 2 and a counter-claim is visible as such). Dead claimants stay: context() adds what their
        card showed."""
        out, day = {}, 0
        for l in self.public:
            m = re.match(r"--- Day (\d+) ---", l)
            if m:
                day = int(m.group(1))
            who, _, text = l.partition(": ")
            # day is 0 until the first day starts: lines said before the cards are not claims
            if day and is_claim(text) and who not in out and any(p["name"] == who for p in self.players):
                out[who] = day
        return out

    def card(self, name):
        """", out: card OFFICER" for a dead player in the claims fact (", out" when the card is face down)."""
        p = next(x for x in self.players if x["name"] == name)
        if p["alive"]:
            return ""
        return ", out, card not shown" if self.face_down(p) else f", out: card {p['role'].upper()}"

    def testimony(self):
        """What the dead said stays known (without it a town player called a dead officer's check "just a story
        now"): each dead player's last words or note, and for a turned OFFICER card the lines in which they claimed or
        named players. At most three short quotes per dead player."""
        rows = []
        for d in self.players:
            if d["alive"]:
                continue
            quotes = []
            if d["role"] == "officer" and not self.face_down(d):
                said = [l.split(": ", 1)[1] for l in self.public if l.startswith(d["name"] + ": ")
                        and (CLAIM.search(l) or re.search(r"\b(checked|shown to me|clean)\b", l, re.I))
                        and mentions(l.split(": ", 1)[1], [x for x in self.players if x is not d])]
                quotes = list(dict.fromkeys(q[:160] for q in said))[-2:]
            row = (f"{d['name']}'s card showed OFFICER. As officer {d['name']} had said: "
                   + " / ".join(f'"{q}"' for q in quotes) if quotes else "")
            if d.get("last"):
                kind = "note" if d.get("how", "").startswith("killed") else "last words"
                row = (row + " " if row else "") + f"{d['name']}'s {kind}: \"{d['last']}\""
            if row:
                rows.append(row)
        return rows

    def shown_word(self):
        return "the killer's accomplice" if self.shown and self.shown["role"] == "accomplice" else "a killer"

    @staticmethod
    def ballots(votes):
        """One ballot per vote, two for the mayor's (the double vote is a rule, not a claim)."""
        return [b for a, b, _ in votes for _ in range(2 if a["role"] == "mayor" else 1)]

    def save_pool(self, p):
        """Whom the doctor may protect: not the player protected last night (themselves included; --repeat-save lifts
        it), not themselves with --no-self-save."""
        pool = [x for x in self.alive() if not (NO_SELF_SAVE and x is p)
                and (REPEAT_SAVE or x["name"] != p.get("last_save"))]
        return pool or self.alive()

    def save_task(self, p):
        rule = "not yourself" if NO_SELF_SAVE else "yourself allowed"
        if not REPEAT_SAVE and p.get("last_save") and any(x["name"] == p["last_save"] for x in self.alive()):
            last = "yourself" if p["last_save"] == p["name"] else p["last_save"]
            rule += f"; not {last}, whom you protected last night"
        return f"Choose a player to protect tonight ({rule})."

    def check_pool(self, p):
        """Who the officer may check: not themselves, not the killer they were shown."""
        checked = {m.group(1) for note in p["notes"] for m in [re.match(r"Night \d+: you checked (\w+)", note)] if m}
        pool = [x for x in self.alive() if x is not p and not x.get("shown")]
        # a second check of the same player is wasted (4 of 78)
        return [x for x in pool if x["name"] not in checked] or pool

    def fresh_line(self, p, task, clock):
        """One SAY call; if the line repeats one of the player's earlier lines (any day of this game), ask once more,
        else stay silent. A role claim or check result may be restated in new words; only a near-verbatim repeat of it
        is blocked (exempt claims got repeated word for word)."""
        own = [l.split(": ", 1)[1] for l in self.public if l.startswith(p["name"] + ": ")]
        today = [l.split(": ", 1)[1] for l in self.today if l.startswith(p["name"] + ": ")]
        names = {x["name"].lower() for x in self.players}
        def repeats(text):
            # the officer's evidence (a claim or a check result) is blocked only when near verbatim
            if CLAIM.search(text) or re.search(r"\bchecked\b|\bshown to me\b|\bI was shown\b", text, re.I):
                return near_verbatim(text, own)
            return too_similar(text, own) or loops(text, today, names)
        r = self.act(p, task, "SAY", clock=clock, extra=LEAN_FIELD)
        if r["text"] and repeats(r["text"]):
            print(f"   [{p['name']} repeated themselves; asking again] blocked: {r['text']!r}", flush=True)
            worn = overused(own)
            again = (f"{task} (You were about to say \"{r['text']}\", which repeats your own earlier line. "
                     "Say something new, or PASS." + (f" Avoid: {', '.join(worn)}." if worn else "") + ")")
            r = self.act(p, again, "SAY", clock=clock, extra=LEAN_FIELD)
            if r["text"] and repeats(r["text"]):
                r["text"] = ""
            r["blocked"] = not r["text"]
        return r

    def vote(self, n, candidates=None):
        voters = self.alive()
        cands = candidates or voters
        runoff = candidates is not None
        task = (f"RUNOFF between {', '.join(c['name'] for c in cands)}: vote for one of them. "
                "If the ties hold, nobody leaves today, which only helps the killer. Pick one."
                if runoff else "Vote to eliminate one player: the name in VOTE.")
        task += " In SAY, one sentence: the thing they did. Don't repeat the name or say 'I'm voting'."
        def vote_task(p):
            """The ballot task; a player who spoke of a vote today is reminded of it."""
            said = [l.split(": ", 1)[1] for l in self.today
                    if l.startswith(p["name"] + ": ") and re.search(r"\bvot", l, re.I)]
            if not said:
                return task
            return task + f' You said today: "{said[-1][:120]}". If you change your mind now, say why in SAY.'
        why_format = f"SAY: <one sentence why, at most {DAY_WORDS} words>\n"
        results = self.parallel([
            lambda p=p: (p, self.act(p, vote_task(p), "VOTE", [c for c in cands if c is not p] or cands,
                                    extra=why_format,
                                    # an unreadable ballot counts as the stated lean
                                    fallback=getattr(self, "leans", {}).get(p["name"])))
            for p in voters])
        votes = [(p, r["pick"],
                  r.get("say") or re.sub(rf"^\W*{r['pick']['name']}\W*", "", r["text"], flags=re.I).strip())
                 for p, r in results]
        tag = lambda a: a["name"] + (" (mayor, counts double)" if a["role"] == "mayor" else "")
        if SECRET:                                   # the table hears only the count per player
            count = Counter()
            for a, b, _ in votes:
                count[b["name"]] += 2 if a["role"] == "mayor" else 1
            line = ("Runoff votes: " if runoff else "Votes: ") + ", ".join(f"{b} {c}" for b, c in count.most_common())
        else:
            line = ("Runoff votes: " if runoff else "Votes: ") + ", ".join(f"{tag(a)} -> {b['name']}"
                                                                           for a, b, _ in votes)
        self.public.append(line)
        self.today.append(line)
        if not runoff:
            self.vote_log += [(n, tag(a), b["name"], why) for a, b, why in votes]
        self.ballot_log.append((n, runoff, [(a["name"], b["name"], 2 if a["role"] == "mayor" else 1)
                                            for a, b, _ in votes]))
        self.last_ballots = [(a["name"], b["name"]) for a, b, _ in votes]
        self.emit({"type": "votes", "runoff": runoff, **({"secret": True} if SECRET else {}),
                   "votes": [[a["name"], b["name"], why] for a, b, why in votes],
                   "weights": {a["name"]: 2 for a, _, _ in votes if a["role"] == "mayor"}})
        return plurality(self.ballots(votes))

    def defend(self, tied):
        """Before a runoff each tied player says one line (at once, like the accused in a Greek game); before this, a
        doctor or officer was told to claim in a runoff vote reason nobody ever heard."""
        task = lambda p: (f"You are tied with {' and '.join(t['name'] for t in tied if t is not p)}; "
                          "the runoff vote is next. One line to the table.")
        for p, r in zip(tied, self.parallel([lambda p=p: self.act(p, task(p), "SAY") for p in tied])):
            if r["text"]:
                self.say(p, r["text"], why="defends before the vote")

    def day_budget(self):
        """Lines per day: 3 per living player plus 3 (24 on a seven-seat day 1, 18 with five, 12 with three); --classic
        keeps 15 at most, 3 per player; --budget caps it."""
        alive = len(self.alive())
        return BUDGET_CAP or (3 * alive + 3 if NATURAL else min(MAX_BUDGET, 3 * alive))

    def parity(self):
        """Living killers equal the living others (killers must outnumber, so it is not over): the town cannot win a
        vote unless a killer slips."""
        k = sum(p["role"] == "killer" for p in self.alive())
        return OUTNUMBER and k >= 2 and k == len(self.alive()) - k

    def day(self, n):
        self.day_no, self.phase_name = n, f"Day {n}"
        self.forget_stale()
        self.emit({"type": "phase", "text": f"Day {n}", "kind": "day"})
        self.public.append(f"--- Day {n} ---")
        # no dead air: at parity the day is short and the vote has one runoff at most (2 v 2 once ran to nine tied
        # votes)
        parity = self.parity()
        if parity:
            k = sum(p["role"] == "killer" for p in self.alive())
            voted_out = [p for p in self.players if not p["alive"] and p.get("how", "").startswith("voted")]
            if not any(self.face_down(p) for p in voted_out):
                # the table can count: killers never die at night, so the shown voted-out cards give the killers left
                self.narrate(f"{NUMBER[k].capitalize()} killers, {NUMBER[k]} others: "
                             "the town needs one of the killers to slip.")
            self.discussion(n, budget=max(4, self.day_budget() // 3))
        else:
            self.discussion(n)
        out, tied = self.vote(n)
        for _ in range(1 if parity else 2):                   # parity: one vote and at most one runoff
            if out is not None:
                break
            before = self.last_ballots
            self.narrate(f"The vote is tied between {' and '.join(t['name'] for t in tied)}. Palermo votes again.")
            self.defend(tied)
            out, tied = self.vote(n, tied)
            # nobody flipped: Palermo talks again, then one last vote
            if out is None and self.last_ballots == before and not parity:
                self.narrate("Nobody changes their mind. Palermo talks again before the last vote.")
                self.last_victim = None                       # the round is about the tie, not last night's death
                self.discussion(n, budget=3)
                out, tied = self.vote(n, tied)
                break
        if out is None:
            self.narrate("Tied again. Nobody leaves today, and Palermo goes to sleep nervous.")
        else:
            if LAST_WORDS:                                    # last words before the card
                r = self.act(out, "The votes are in and you are out. Your last words to the table, one line.", "SAY",
                             limit=25)
                if r["text"]:
                    out["last"] = r["text"]
                    self.say(out, r["text"], why="last words")
            self.out(out, "vote")
            if out["role"] == "jester":
                card = f" {out['name']} was the jester, and the jester wanted exactly that."
            elif HIDE_VOTE:
                card = f" {out['name']}'s card stays face down."
            else:
                card = f" {out['name']} shows the card: {out['role']}."
            told = random.choice([f"Palermo has voted: {out['name']} is out.",
                                  f"The town turns on {out['name']}, and {out['name']} is out."]) + card
            self.narrate(told)
            if out["role"] == "jester":
                self.jester_won = out
            self.aside(told, when=f"Day {n}: the day's vote (not a night).")
        self.graveyard()

    def graveyard(self):
        """The dead watch: after the day's vote each dead player says one line to the audience. Viewer only:
        a `ghost` event, never in what players see. Skipped once the game is decided (the confessions follow)."""
        dead = [p for p in self.players if not p["alive"]]
        if not GHOSTS or not dead or self.winner() is not None:
            return
        task = ("You are out of the game and watching from the side with the audience. One line to the audience about "
                "what the table just did.")
        replies = self.parallel([lambda p=p: self.act(p, task, "SAY", limit=25, kind="ghost") for p in dead])
        for p, r in zip(dead, replies):
            said = [l.split(": ", 1)[1] for l in self.public if l.startswith(p["name"] + ": ")]
            own = p.setdefault("ghost_lines", []) + said
            # a ghost line close to an earlier line of theirs (last words included) is dropped
            if r["text"] and not near_verbatim(r["text"], own, 0.7):
                p["ghost_lines"].append(r["text"])
                self.emit({"type": "ghost", "name": p["name"], "text": r["text"]})

    def run(self):
        self.intro()
        n, result = 1, None
        while result is None:
            self.night(n)
            result = self.winner()
            if result is None:
                self.day(n)
                result = self.winner()
            if n >= MAX_DAYS and result is None:
                self.emit({"type": "end", "winner": "stopped"})
                print(f"Stopped after day {n} (--days).", flush=True)
                return "stopped"
            n += 1
        side = {"town": "The town", "jester": "The jester"}.get(
            result, "The killers" if ROLE_LIST.count("killer") > 1 else "The killer")
        told = (f"The game is over. {self.why_over(result)}{side} win{'' if side.endswith('s') else 's'}. "
                "The roles were: "
                + ", ".join(f"{p['name']} the {p['role']}" for p in self.players) + ".")
        self.narrate(told, transcript=False)
        self.aside(told, when=self.end_state(result), end=True)
        killers = [k["name"] for k in self.players if k["role"] in EVIL]
        for p in self.players:
            if p["alive"] or p["role"] in EVIL:
                continue
            own = [l.split(": ", 1)[1] for l in self.public if l.startswith(p["name"] + ": ")]
            for line in reversed(own):
                if any(accuses(line, k) for k in killers):
                    self.emit({"type": "vindicated", "name": p["name"], "text": line})
                    break
        task = ("The game is over and every role is public. One sentence to the table: the move you are proud of "
                "or the mistake you regret. Honest, no sulking. Speak as \"I\" and \"my\"; never say your own name.")
        replies = self.parallel([lambda p=p: self.act(p, task, "SAY", limit=30) for p in self.players])
        for p, r in zip(self.players, replies):
            said = [l.split(": ", 1)[1] for l in self.public if l.startswith(p["name"] + ": ")]
            if r["text"] and not too_similar(r["text"], said):
                self.say(p, r["text"], why="confession")   # a confession that copies an earlier line is dropped
        self.recap(side)
        self.emit({"type": "end", "winner": result})
        return result


def serve():
    """The viewer, the saved games and /games/index.json: the same handler as view.py (one place for both)."""
    from view import handler
    server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler(HERE))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f"Watch: http://localhost:{PORT}/", flush=True)


def ensure_local(seats):
    """Start LM Studio's server and load the local models a seat needs (lms CLI). The local model is optional: without
    LM Studio this says which seats wanted it and how to give them to a model you do have."""
    lms = pathlib.Path.home() / ".lmstudio" / "bin" / "lms"
    local = [m for m in seats if m["model"].startswith("local:")]
    if local and not lms.exists():
        names = [m["name"] for m in local]
        sys.exit(f"{' and '.join(names)} {'plays' if len(names) == 1 else 'play'} on a local model (LM Studio), which "
                 "is not installed here.\nGive the seat to any model you have, for example:\n"
                 f"  python3 game.py --model {','.join(n + '=claude:sonnet' for n in names)}\n"
                 "or change the model line in the seat's file in players/ (see README, \"Use your own models\").")
    for name in {m["model"].partition(":")[2] for m in local}:
        try:   # `lms ps` lists LOADED models (the /v1/models endpoint lists every downloaded one)
            ps = subprocess.run([str(lms), "ps", "--json"], capture_output=True, text=True, timeout=30)
            loaded = json.loads(ps.stdout or "[]")
            if any(name in (m.get("identifier"), m.get("modelKey")) for m in loaded):
                continue
        except (OSError, ValueError, subprocess.SubprocessError):
            pass
        if not lms.exists():
            sys.exit(f"Local model {name} needs LM Studio running with it loaded (lms CLI not found).")
        print(f"Starting LM Studio and loading {name}…", flush=True)
        subprocess.run([str(lms), "server", "start"], capture_output=True, timeout=60)
        # one local model at a time fits
        subprocess.run([str(lms), "unload", "--all"], capture_output=True, timeout=120)
        r = subprocess.run([str(lms), "load", name, "--context-length", "8192", "-y"],
                           capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            sys.exit(f"Could not load {name} in LM Studio: {r.stderr[-300:]}")


def check_models(seats):
    """--check: one short call per seat and the host, in parallel; prints who answered and how fast. 0 if all did."""
    host = load(HERE / "gamemaster.md")[0]
    todo = [(m["name"], m["model"], m.get("effort")) for m in seats] + [("the host", host["model"], host.get("effort"))]
    def one(item):
        name, model, effort = item
        t0 = time.time()
        try:
            reply = call(model, effort, "You answer with one word.", "Say: ready")
        except (Exception, SystemExit) as e:         # any failure is the answer here (a quota error exits)
            reply, err = "", str(e)[:120]
        else:
            err = "empty reply"
        return name, model, bool(reply), time.time() - t0, err
    with ThreadPoolExecutor(len(todo)) as pool:
        rows = list(pool.map(one, todo))
    for name, model, ok, secs, err in rows:
        print(f"  {'ok  ' if ok else 'FAIL'}  {name:<9} {model:<40} {secs:4.1f}s" + ("" if ok else f"   {err}"),
              flush=True)
    bad = [name for name, _, ok, _, _ in rows if not ok]
    print("Every seat answers." if not bad else
          f"No answer from: {', '.join(bad)}. Pick another model for them: --model NAME=claude:sonnet", flush=True)
    return 1 if bad else 0


def check_subscriptions():
    try:
        auth = json.loads((pathlib.Path.home() / ".codex" / "auth.json").read_text())
        if auth.get("auth_mode") != "chatgpt":
            print("WARNING: codex is not in ChatGPT-subscription mode; it may bill API credits.", flush=True)
    except (OSError, ValueError):
        print("WARNING: codex auth not found; run `codex login`.", flush=True)
    stripped = [k for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY") if k in os.environ]
    if stripped:
        print(f"Note: {', '.join(stripped)} hidden from the agents so nothing is billed to an API key.", flush=True)


if __name__ == "__main__":
    # only as a script: lab.py, probe.py and check_roles.py pass their own flags
    check_flags(ARGS)
    if "--serve" in ARGS:
        serve()
        input("Press Enter to stop.\n")
        sys.exit()
    if not DRY:
        check_subscriptions()
    seats = [load(f)[0] for f in seat_files()]
    if not DRY:
        ensure_local(seats)
    if CHECK:
        sys.exit(check_models(seats))
    if not FAST:
        serve()
    base = TAG or (datetime.datetime.now().strftime("%Y%m%d-%H%M%S") if GAMES > 1 else "")
    print(f"Seed: {SEED}" + ("" if "--seed" in ARGS else " (fresh; replay with --seed)"), flush=True)
    for i in range(FIRST - 1, GAMES):
        # each game its own deal
        GAME_SEED = SEED if GAMES == 1 else random.Random(f"{SEED}:{i + 1}").randrange(10 ** 9)
        random.seed(GAME_SEED)
        if GAMES > 1:
            TAG = f"{base}-{i + 1}"
            prev = HERE / "games" / f"{base}-{i}.json"   # also after --first N: the file of the game before
            try:
                cast = json.load(open(prev))[0]["players"] if i else []
            except (OSError, ValueError, IndexError, KeyError):
                cast = []
            PREV = {"pair": {c["name"] for c in cast if c["role"] in EVIL},
                    "officer": next((c["name"] for c in cast if c["role"] == "officer"), None)} if cast else {}
            # what the table remembers of this evening's earlier games (last three)
            if not NO_HISTORY:
                HISTORY = [str(f) for j in range(max(0, i - 3), i)
                           for f in [HERE / "games" / f"{base}-{j + 1}.json"] if f.exists()]
        game = Game()
        try:
            print(f"Winner: {game.run()}  (saved {game.files[0].name})", flush=True)
        except Exception:
            traceback.print_exc()
    if not FAST:
        input("Press Enter to stop the viewer server.\n")
