# One Night in Palermo

**Seven language models sit down to play Mafia. Two of them are killers. Nobody scripted a word.**

Palermo is the Greek name for Mafia, the party game where a hidden minority lies and everyone else tries to catch them.
Here the players are language models: Claude Sonnet, Haiku and Opus, three GPT models, and Gemma running on a laptop.
A small Python engine deals the cards, enforces the rules and counts the votes. The models only talk, lie, remember and
vote. A React viewer replays every game with each line next to the private thought behind it, so you watch a lie being
planned before the table hears it.

![The home screen](palermo/docs/screenshot-home.jpg)

![A game in the viewer](palermo/docs/screenshot-table.jpg)

**Watch in the browser:** https://dchristopoulos.github.io/one-night-in-palermo/ (24 games, no account needed)

## One game, in six lines

Game `fun9-4`, quoted from the recording in [`palermo/games/fun9-4.json`](palermo/games/fun9-4.json):

1. Day 1. Luna, the officer, tells the truth: *"I'm the officer: Opus is the killer I saw."*
2. Opus thinks: *"She's the real officer, so I have to be the louder officer and point the table at Sol."*
3. Opus says: *"I'm the officer. I saw Sol."* The table votes 4 to 3 and removes Luna, the one telling the truth.
4. Day 2. Luna's card proves the lie and Opus is voted out. His last words: *"Fine, I'm the killer — and my partner
   is the one I never attacked: Terra."* Terra is innocent.
5. Day 3. The table argues about Terra and votes out its own doctor.
6. Haiku, the second killer, wins. Not one ballot named Haiku in the whole game.

The one-minute video of this game is in [`video/`](video/).

## How it works

```mermaid
flowchart LR
    S["Seat files<br/>name, model, character"] --> E
    E["Engine (game.py)<br/>deals, runs phases,<br/>enforces every rule"] -- "one question at a time" --> M["Models<br/>claude CLI, codex CLI,<br/>local LM Studio"]
    M -- "thought, line, note, lean" --> E
    E -- "appends every event" --> L["Game file (JSON)<br/>lines, thoughts, whispers,<br/>votes, deaths, memories"]
    L --> V["Viewer (React)<br/>Watch mode, Guess mode"]
    L --> F["Fun meter<br/>scores finished games"]
```

- **The engine owns the rules; the models own the talk.** [`palermo/game.py`](palermo/game.py) is one file of
  standard-library Python. It deals two killers, an officer who was shown one of them, a doctor and three citizens. It
  decides whose turn it is, counts the votes and ends the game. A model can say anything, but it cannot break a rule,
  because rules are code and never a request in a prompt.
- **One question at a time.** Each call asks one player for one thing: a line of talk, a vote, or a night choice. The
  reply has fixed parts: a private thought, the line said aloud, a note to keep, a note to drop, and who the player
  currently leans toward voting out.
- **Thoughts and speech are separate events.** The thought goes to the audience only. No other player ever sees it,
  which is what makes Watch mode work: you read the plan, then hear the lie.
- **The day ends when the table is ready.** Every line carries a lean. When a strict majority leans on the same
  player, the vote is called. Ballots are secret: the table sees the count, not who voted for whom.
- **Everything is an event.** Lines, thoughts, killer whispers, votes, deaths and memory notes are appended to one JSON
  file per game. The viewer and every analysis tool read that file and nothing else, so a game can be replayed,
  measured and quoted exactly.

## Memory

A game runs for about ten minutes and about seventy spoken lines. Giving every model the full transcript on every
turn works, but it makes them all remember everything equally, which is not how a table of people plays. So each prompt
is built from three layers:

| Layer | Who writes it | What it holds |
|---|---|---|
| **What you know for sure** | the engine | your role, your night results, who is out and which cards were shown, every officer claim so far, what the dead said, and each past vote with its count |
| **What you remember** | the player | its own notes, at most ten, each with an importance from 1 to 3 |
| **What you hear now** | the engine | today's lines, as they were said |

The middle layer is the interesting one. On each turn a player may write one note and drop one. The engine keeps the
notebook honest:

- **Importance decides how long a note lives.** Importance 1 fades after a day, 2 after three days, 3 stays for the
  game.
- **Duplicates are refused.** A note that names the same players and shares half its words with an older one is the
  same memory.
- **Vote tallies are not stored.** The facts layer already has them, and notes that only restate a count pushed out
  better ones.
- **Notes about players who are out expire**, unless they were marked importance 3.

Real notes from game `fun9-4` (the number is the importance the player chose):

```
Opus   3  I am the shown killer, so the real officer will name me; I preempt by claiming officer and accusing Sol.
Haiku  3  Opus whispered that he will claim officer and name Sol as the killer, so Opus's officer claim is a bluff.
Luna   3  Opus wants my card turned while his own stays hidden.
Terra  2  Gemma named Terra without giving a case.
Opus   3  Luna's card came up OFFICER, so my officer counterclaim naming Sol is publicly false and I must survive
          day 2 by pivoting, not repeating it.
```

Facts and beliefs never mix: a player can be wrong in its notes, but it cannot be wrong about a card that was turned.

**Between games.** In an evening of several games the table remembers the earlier ones. Each player gets one line per
past game, written from its own side ("you were the officer; you were voted out on day 1; the table was wrong about
you; the killers won"), for the last three games. Grudges and reputations carry over; the cards are dealt fresh.

Two other memory modes exist for comparison: `--memory transcript` (everything said, no notes) and `--memory short`
(notes plus only the last six lines).

## What the games taught the rules

The rules changed many times, each time because recorded games showed a problem:

- **Public ballots solved the game.** When everyone saw who voted for whom, the town worked out the killers on day 2.
  Ballots became secret, as in the Greek house rule.
- **Turning every card made the town unbeatable** (four wins out of four in one evening). Now a voted-out player shows
  the card; a player killed at night does not.
- **A mayor with a double vote lasted one night.** The first tally exposed the double vote and the killers removed the
  mayor at once. The role is off by default.
- **Players misremembered their own past games.** The between-games memory is now written per player, as plain facts.
- **Models repeat a line that worked.** A line that reuses most of the words of the speaker's earlier lines is
  rejected.
- **A quota error once left three seats silent** and the game played on without them. The engine now stops instead.

In the 24 published games the town wins 14 and the killers 10.

## The fun meter

A game can be correct and still dull. [`palermo/funmeter.py`](palermo/funmeter.py) asks a model to watch a finished game
as a viewer would and score it from 0 to 100 on nine things that make social deduction watchable: dramatic irony,
reversals, real mistakes, distinct voices, clashes, quotable lines, freshness, suspense, and an ending decided by a
choice. It quotes the moments it liked and names the dull stretches. The scores choose which games the home screen
offers first, and they informed rule changes. They are never used to tell a player what to say.

One judge is noisy by about ten points per game, so the scores rank games; they do not prove anything. Method, sources
and limits: [`palermo/docs/fun-meter.md`](palermo/docs/fun-meter.md).

## Run it

Watch the bundled games locally (Python 3 and nothing else):

```
cd palermo
python3 view.py            # then open http://localhost:8766/
```

Play your own:

```
cd palermo
python3 game.py --dry --fast                      # scripted players, no model calls: checks the engine in a second
python3 game.py --check                           # one short call per seat: do my models answer?
python3 game.py --fast --games 4 --tag mynight    # four real games: games/mynight-1.json to mynight-4.json
```

A game takes 8 to 15 minutes. Every flag: `python3 game.py --help`. Rules, tools and the event format:
[`palermo/README.md`](palermo/README.md).

## Use your own models

Nothing in the repository is tied to an account. The engine calls command-line tools on **your** machine, so every call
uses whichever account is logged in there. No API keys are used anywhere: the engine removes `ANTHROPIC_API_KEY` and
`OPENAI_API_KEY` from every model call, so nothing is billed as API credits. Watching the bundled games needs no account.

A model is written as `backend:model`:

| Backend | Runs through | Examples |
|---|---|---|
| `claude:` | the `claude` CLI (Claude Code), logged in with a Claude subscription | `claude:sonnet`, `claude:opus`, `claude:claude-haiku-5-5` |
| `codex:` | the `codex` CLI, logged in with ChatGPT (`codex login`) | `codex:gpt-6-sol`, `codex:gpt-6-luna`, `codex:gpt-5.6-terra` |
| `local:` | LM Studio on this machine (optional) | `local:google/gemma-4-26b-a4b-qat` |

The recorded games were played with the seven seats in `palermo/players/` (Sonnet, Haiku, Gemma, Sol, Luna, Terra,
Opus). That is only the table we tested. Seat whatever you like:

```
python3 game.py --check                                   # one short call per seat: do my models answer, how fast?
python3 game.py --model Gemma=claude:sonnet               # no LM Studio: give the local seat to a model you have
python3 game.py --model all=claude:sonnet                 # only a Claude subscription: every seat on one model
python3 game.py --model all=codex:gpt-6-luna,host=codex:gpt-6-luna   # only ChatGPT (the host is the narrator)
```

`--model` changes who plays for that run; the seat keeps its name, face and character, and the saved game records the
model that really played (the viewer shows it under the name). To change a seat for good, edit its file in
`palermo/players/`: `name`, `model`, a `tagline`, and a few lines of character. A new name without a portrait in
`palermo/avatars/<Name>.png` gets a plain stand-in face.

Things worth knowing:

- The local model is optional. Without LM Studio the engine stops before the game and prints the `--model` line to use.
- Bigger models cost more of your subscription and are slower; small fast ones play fine.
- A ChatGPT subscription lasts roughly 30 games with three GPT seats per quota window; on a quota error the engine
  stops, resume with `--first N`.
- Any model works with the engine, but the rules and prompts were tuned on the seven above; another table may play a
  little differently.

## Publish the viewer as a static site

```
cd palermo
python3 view.py --export ../../palermo-site                  # the two newest evenings
python3 view.py --export ../../palermo-site --tags r7a,sun15  # chosen evenings
python3 view.py --export ../../palermo-site --best 6          # the six best-scored games (games/fun/), else the newest evening
```

The folder holds `index.html`, the built assets, fonts, avatars, the chosen games and a prebuilt `games/index.json`. All
URLs are relative and routing uses `?file=` query parameters, so it works on any static host, in any sub-folder
(`https://example.github.io/some-repo/`), and locally with `python3 -m http.server` run in the folder. Upload the
folder's contents as they are: for GitHub Pages, push them to a `gh-pages` branch (or use a Pages workflow that uploads
the folder); for Netlify, Cloudflare Pages, S3 and the like, deploy the folder with no build step. Rebuild the viewer
(`npm run build`) before exporting after a change to `palermo/ui/src`.

## Tests

```
cd palermo && python3 tests.py && python3 view_test.py && python3 stats_test.py && python3 funmeter_test.py
cd palermo/ui && npm ci && npm test && npm run build
```

The engine tests include full scripted games. The viewer tests cover the replay logic and the colour contrast of
the text and background pairs.

## Repository

| Path | What |
|---|---|
| [`palermo/game.py`](palermo/game.py) | the engine: rules, prompts, memory, model calls, event log |
| [`palermo/players/`](palermo/players/) | one seat per file: name, model, character |
| [`palermo/ui/`](palermo/ui/) | the viewer (React, TypeScript, Vite) |
| [`palermo/view.py`](palermo/view.py) | serves the viewer and exports it as a static site |
| [`palermo/funmeter.py`](palermo/funmeter.py), [`stats.py`](palermo/stats.py), [`review.py`](palermo/review.py) | scoring and reading games |
| [`palermo/games/`](palermo/games/) | the recorded games |
| [`palermo/docs/`](palermo/docs/), [`palermo/research/`](palermo/research/) | engine rules, prompts, design, measurements, sources |
| [`video/`](video/) | the one-minute video as an HTML project |

## The video

`video/` holds a one-minute vertical video about game `fun9-4`, built as HTML and rendered with
[HyperFrames](https://github.com/heygen-com/hyperframes). A script checks every quote in it against the game file.
How to render it: [`video/README.md`](video/README.md).

![A frame from the video](video/out/poster.jpg)

## Credits

Palermo is a traditional party game, the Greek take on Mafia, the social deduction game created by Dmitry Davidoff in
Moscow in 1986 and played at tables everywhere since (also known as Werewolf). This project only seats language models
at the table. The fonts (Bodoni Moda, Instrument Sans) are under the SIL Open Font License; see
`palermo/ui/public/fonts/`.

## License

MIT: see [`LICENSE`](LICENSE). The seat portraits and table art in `palermo/avatars/` and `palermo/art/` were made with
an image model for this project and are covered by the same license.
