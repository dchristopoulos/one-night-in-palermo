# One Night in Palermo

Seven language models sit at one table and play Palermo, the Greek take on Mafia: two of them are secretly killers,
the rest try to vote them out by talking. The engine (`game.py`, one Python file, standard library only) enforces every
rule and writes each game as a list of events; the models only talk, vote and choose at night. A React viewer replays
those files, or follows a game while it is being played.

## Watch a game

```
python3 view.py            # then open http://localhost:8766/ui/   (another port: python3 view.py 8800)
```

- **Home** lists what is playing now, then the evenings (a tag such as `fin71`), newest first, each with its games
  and a scoreboard; single games are folded at the bottom. "Results: Hidden / Shown" decides whether winners are
  printed; a game you watched to its end card shows its result either way. One click opens a game.
- **Watch** (default): every role and every private thought is visible, so you can watch the liars lie.
  **Guess**: only what the table knows; roles and thoughts come out at the end. Switch in the header at any time.
- **Live**: a game being written right now is marked live on Home and in the header; the viewer polls it every second
  and has no replay controls until it ends (a `Jump to the end` button appears when it falls far behind). A file
  the index does not list: `?file=games/x.json&live=1`.
- **Controls**: Space play/pause, Left/Right previous/next line, Enter on a log entry jumps there. Buttons for the
  same, a speed button (1x, 1.5x, 2x), a scrub bar with marks for phases and deaths, ‹ › for the previous/next game of
  the evening, Log to show or hide the log (wide screens), Games to go home. The end card has who was who, the recap
  and "The evening so far".
- **URL**: `?file=games/run81-2.json`, `&mode=guess`, `&at=N` (a still at event N).

`python3 game.py --serve` serves the same viewer on port 8765. The viewer must be built first (`cd ui && npm ci && npm run
build`; `ui/dist` is not in the repository).

**A static copy** for any web host: `python3 view.py --export DIR [--tags r7a,sun15] [--best N]` writes the built viewer,
the avatars, the chosen games and a prebuilt `games/index.json` into DIR (default: the two newest evenings; `--best N`:
the N games with the highest score in `games/fun/`, else the newest evening). It works from any folder of a host, such as
`https://example.github.io/some-repo/`, and with `python3 -m http.server`; nothing is live there.

## Play an evening

```
python3 game.py --fast --games 4 --tag mynight      # writes games/mynight-1.json ... mynight-4.json
python3 game.py --dry --fast                       # no models, scripted players, one second; writes games/<time>-dry.json
```

What the seats need (no API keys anywhere: `ANTHROPIC_API_KEY` and `OPENAI_API_KEY` are stripped from every subprocess,
everything runs on subscriptions or locally):

| Seat | Runs on |
|---|---|
| Sonnet, Haiku, Opus, and the host | the `claude` CLI (Claude subscription) |
| Sol, Luna, Terra | the `codex` CLI, logged in with ChatGPT (`codex login`; it warns if not in subscription mode) |
| Gemma | LM Studio with `google/gemma-4-26b-a4b-qat`; the engine starts it and loads the model through `lms` if it can (optional) |

Any seat can be given to any model you have: `--model Gemma=claude:sonnet` for one run (`all=` every seat, `host=` the
narrator), or edit the seat's file in `players/`. `python3 game.py --check` calls every seat once and says who answers.
Without LM Studio the engine stops before the game and prints the `--model` line to use.

- A game takes about 8 to 15 minutes (up to 20 when it runs to day 4); an evening of 4 about an hour.
- `--fast` skips the built-in server and the pauses; watch with `python3 view.py` in another terminal. Without
  `--fast` the engine serves the viewer on 8765 and waits for Enter at the end.
- With `--games N` each game is dealt at random from `--seed` and the game number (no seed: a fresh one, printed and
  stored in the `cast` event); the same two players are never the killer pair twice running, nobody is officer twice
  running. Players remember the earlier games of the evening; `--no-history` makes every game fresh.
- Codex quota: roughly 30 games per window. On a quota error the engine stops. Resume with the same command plus
  `--first N` (N = the game to play next, e.g. `--games 8 --first 5 --seed S --tag mynight`, with the seed printed at
  the start); the deal and the memory of the earlier files carry on.

## The rules in ten lines

1. Seven seats: two killers, one officer, one doctor, three citizens (`--roles` changes this).
2. The killers know each other. One is SHOWN to the officer at the start, the other stays HIDDEN.
3. The officer has no other power (`--checks` adds one check a night).
4. Night 1 is quiet: the killers whisper, nobody dies.
5. From night 2 the killers kill one player; the doctor protects one (never the same player two nights running; the
   doctor does nothing on night 1).
6. Each day the table talks with a line budget (3 per living player plus 3: 24 at seven), then votes in secret; the
   table sees only the count per player (`--open-ballots` shows who voted whom).
7. When a majority leans on one player and holds for half a round, that player answers twice and the vote comes early
   (everyone speaks twice on day 1, once on later days).
8. A tie: the tied players speak, runoff; still tied after one more round, nobody is out.
9. A voted-out player says last words and shows the card; a night victim's card stays face down. The dead take no
   part in the night and talk to the audience only.
10. The town wins when both killers are out; the killers win at parity (as many killers as others).

Full detail: `docs/engine-rules.md`.

## Flags

| Purpose | Flags |
|---|---|
| Run | `--fast` (no server, no pauses), `--dry` (fake players), `--tag NAME`, `--games N`, `--first N`, `--seed N` (default: fresh, printed), `--serve` |
| Table | `--seats N` (first N seat files), `--roles killer=2,officer,doctor` (also `police`, `jester`, `mayor`, `accomplice`), `--killer NAME` |
| Rules back to older builds | `--open-ballots`, `--checks`, `--kill-night1`, `--reveal-night`, `--hide-vote`, `--notes`, `--no-parity`, `--no-last-words`, `--no-ghosts`, `--repeat-save`, `--no-self-save` |
| Memory | `--no-history`, `--history f1.json,f2.json`, `--memory levels\|transcript\|short` |
| Length | `--days N` (stop after day N), `--budget N` (lines per day), `--classic` |
| Host | by default the host adds one remark at the end; `--asides` (also one after each death), `--plain-host` (no model remarks), `--narrator-agent` (narration by the model) |
| Debug | `--prompt NAME` (print that seat's prompts; works with `--dry`), `--help` (every flag, one line each) |
| Accepted, do nothing | `--quiet-night`, `--hide-night`, `--show-vote`, `--no-notes`, `--parity` |

An unknown flag prints the flag list and exits with code 2 before any model is called, so a typo never plays a game.

## Tools

| Command | What it does |
|---|---|
| `python3 stats.py mynight [more tags]`, `--all` | judge evenings: wins, how games ended, days, officer, doctor, hidden killer, talk, per seat |
| `python3 games/lab/digest.py games/x.json` | one game in short: roles (`*` = shown killer), claims, votes, deaths, recap |
| `python3 review.py games/x.json [--day N]` | one game as a full transcript with secrets and notes |
| `python3 tests.py` | engine checks plus four dry games, a few seconds |
| `python3 stats_test.py`, `python3 view_test.py` | unit tests for `stats.py` and `view.py` |
| `cd ui && npm test` | viewer unit tests |
| `cd ui && npm run build` | type-check and build the viewer into `ui/dist` (what `view.py` serves and `--export` copies) |

## Where things are

| Path | What |
|---|---|
| `game.py` | the engine: rules, prompts, model calls, event log |
| `players/*.md` | one seat per file: model, tagline, persona |
| `gamemaster.md` | the host's persona and model |
| `view.py` | static server for the viewer and `games/index.json` |
| `ui/` | the React viewer (`src/`, built to `dist/`) |
| `index.html` | forwards `/` to `/ui/` |
| `games/` | the evenings on the current engine (`tag-N.json`), viewer fixtures, `games/fun/` scores (funmeter.py), `games/lab/` small tools, `games/archive/` older games (not comparable, not listed) |
| `stats.py`, `review.py`, `games/lab/digest.py` | reading games |
| `lab.py`, `lab_sim.py`, `sim.py`, `probe.py`, `check_roles.py`, `bake.py`, `gates.py` | experiments and older checks |
| `art/`, `avatars/` | table backgrounds and seat portraits |
| `docs/`, `research/` | notes, below |

## Docs

- `docs/engine-rules.md`: what the engine enforces, flags, event format (current).
- `docs/prompts.md`: the prompts every seat gets (current).
- `docs/DESIGN.md`: the viewer's look, layout and controls.
- `docs/turn-taking.md`: who speaks next.
- `docs/balance.md`, `docs/measurements.md`: numbers from the test evenings.
- `docs/fun-meter.md`: how the fun meter scores a game, its sources and limits.
- `research/`: rules, real transcripts, prior work on LLM agents.
