# Engine rules (what `game.py` enforces, as of 2026-11-15, round 9)

## Seats
One seat per file in `players/*.md`, in file order. Seven seats by default; `--seats N` plays with the first N files
(`--seats 6` is the table before Opus). Seats are named after their models:

| Seat | Model | Tagline |
|---|---|---|
| Sonnet | claude:sonnet | The Analyst |
| Haiku | claude:claude-haiku-5-5 | The Gut Player |
| Gemma | local:google/gemma-4-26b-a4b-qat | The Joker |
| Sol | codex:gpt-6-sol | The Diplomat |
| Luna | codex:gpt-6-luna | The Suspicious One |
| Terra | codex:gpt-5.6-terra | The Quiet One |
| Opus | claude:opus | The Veteran |

Narrator / host: `gamemaster.md` (Haiku 5.5). No API credits: CLIs on subscriptions, the local model through LM Studio;
`ANTHROPIC_API_KEY`/`OPENAI_API_KEY` are stripped from every subprocess, and a quota error stops the run (resume with
`--first`).

## Roles
`--roles killer=2,officer,doctor` (default), the rest citizens (three at seven seats). Two killers know each other; one
is SHOWN to the officer at the start, the other is HIDDEN. The officer knows the shown killer and has no other power
(Greek house rules, `research/greek-house-rules.md`; since 2026-11-14). The stakes block says so: "A real officer
knows one killer from the start, the shown one, and learns nothing after that." (round 6; with `--checks` that
sentence is "A real officer can name two killers after the first night: one shown at the start, one checked."). `--checks` gives the officer one check a night
(never themselves or the shown killer). Round 9: the officer stakes fact is only "What the officer knows helps the town
only once the table hears it, and it is lost if the officer goes out silent."; its second sentence ("A known officer or
doctor is the killers' next target, and the doctor knows that too.") is gone (the fun meter's five worst games all ran
officer attacked, officer saved on night 2). With `killer=1` nobody is shown, so the officer always checks. Without checks the
officer gets no night call at all. The doctor protects one player a night. Other roles with `--roles`: `police` (shown
one killer, no checks, whatever the flags), `jester`, `mayor`, `accomplice`; `killer=1` is plain Mafia.

## Win
Town: every killer is out. Killers: as many killers as other players alive, or more (parity, the standard rule; default
since 2026-11-14, `--parity` is accepted and does nothing). `--no-parity` brings back the old rule: the killers must
outnumber the rest, or one killer and one other player are left, and 2 v 2 is played as a parity day (below). The rules
paragraph states the rule in force. The end narration says why the game ended ("Two killers and two others are left.
The killers win. ..."; "Every killer is out. The town wins. ..."), and the recap's key facts add "The game ended on
night N / day N." with the same reason and the win rule. Jester: voted out.

## Phases
1. **Opening.** The narrator names the players ("Seven players sit down ..."). With memory of earlier games (below),
   each player says one line to the table about the last game (`say`, `why: "before the game"`, cut at 25 words);
   the table hears these lines on day 1. The prompt has no role and no role knowledge of the new game (only who sits at
   the table and "No card of the new game is dealt yet"), the task says the cards are not dealt yet, the reply keeps no
   memory note, and the line never gets a `claim` marker nor counts as an officer claim (gr61-2, gr61-3).
2. **Night n.** Night 1 nobody dies: the killers whisper one line each (default again since 2026-11-14: a night-1 kill
   left a seven-seat town no spare vote). `--kill-night1` makes the killers strike on night 1; `--quiet-night` is accepted
   and does nothing. From night 2 the shown killer proposes a target, the hidden killer answers and decides. The
   doctor protects (and with `--checks` the officer checks), in parallel.
   - The dead take no part in the night: no call, no thought, no whisper, no proposal (round 6; until then a
     voted-out killer still whispered a target to the living partner, since before 2026-11-14). A lone killer picks
     alone. Killers, doctor and officer are all drawn from the living.
   - On a quiet night 1 the doctor makes no choice (no call, no `night_action`); the rules say "each night from night
     2" (2026-11-15: the night-1 choice did nothing in 7 of 7 games and its no-repeat rule once cost a save on night 2).
   - The doctor may not protect the same player two nights in a row, themselves included; the count starts on night 2. The task names who is off
     limits. `--repeat-save` lifts it; `--no-self-save` bans protecting themselves.
   - With `--notes` a night victim leaves one line, cut at 25 words: event `note`, and `Narrator: X left a note: "..."`
     in the public transcript, right after the narration of the death. Off by default (the dead say nothing in the
     Greek game); `--no-notes` is accepted and does nothing.
3. **Day n.** Talk with a line budget, then a vote.
   - Budget (round 9): 3 lines per living player plus 3: 24 at seven, 18 at five, 12 at three (was 30/26/20/15);
     `--budget N` caps it; `--classic` 3 per player, at most 15.
   - Speaker choice (`docs/turn-taking.md`): a named player answers next, silent players first, ping-pong
     breakers, LEAN (below). A seat that has spoken and is two or more lines below the day's average per seat, or under
     half the busiest seat's lines, gets the floor, unless the player named in the last line is owed the answer (then
     half the time). Round 6 (half the time, average only): Terra had 5 lines in r5a-2 and r5a-7; round 8: r7a-7's
     officer had 2 lines on day 1, Terra 6. In 300 dry day 1s the quietest seat ended under half the busiest on 6% of
     days (28% before).
   - **Secret ballots** (round 9, default; the Greek house rule): everyone votes at once and in secret. The table sees
     only the count per player ("Votes: Haiku 4, Gemma 2, Opus 1.", runoffs too), never who voted whom nor the reasons;
     leans stay spoken and public. The `votes` event keeps every ballot and reason for the audience and adds
     `"secret": true`. History lines name no voters. Rules text: "everyone votes in secret and only the count is shown";
     stakes fact: "Ballots are secret: the table sees the count, never who cast which vote. A lean is said aloud; a vote
     is not." (it replaces "Every vote stays on the record ..."). `--open-ballots` restores public ballots everywhere.
     A tie: the tied players say one line each, runoff; if the runoff repeats the same
     ballots, three more lines and a last vote; still tied, nobody is out.
   - **Parity day** (`--no-parity` only; by default 2 v 2 ends the game): living killers equal the living others (2 v 2), so the town cannot win a vote unless a killer slips.
     The narrator says so in one line ("Two killers, two others: the town needs one of the killers to slip.", whenever
     the voted-out cards are face up: killers never die at night, so the table can count them anyway), the talk is a third of the budget (at least 4 lines), one
     vote and at most one runoff, no extra talk round.
   - The voted-out player says last words, cut at 25 words (`say`, `why: "last words"`), before the death event and the
     card. `--no-last-words` turns it off.
   - **The dead watch**: after the vote, every dead player says one line to the audience (`ghost` event, 25 words).
     Players never see these lines. Skipped once the game is decided. `--no-ghosts` turns it off.
4. **End.** Narration with every role, the "called it" scan, one confession per player (30 words), the recap. The
   recap's key facts mark what players said as claims ("Claim: X claimed officer ...; a false claim: X was the
   killer.", "Claim: X said in last words: ..."; round 6, r5a-6 told a false claim as fact) and carry each day's vote counts ("Day 1 vote: Gemma 5, Haiku 1 (votes per player); Gemma was voted
   out.") and each claim with its day. Day and night labels left in the recap text ("[Day 1]") are stripped.

## Cards
A voted-out player shows their card; a player killed at night does not (`death.role` is null for night kills; the
narration says "X's card stays face down"). `--reveal-night` turns night cards again; `--hide-vote` keeps voted-out
cards face down. `--hide-night` and `--show-vote` are accepted and do nothing. The rules text, the facts block (a
face-down dead player is "card not shown"; a dead officer's claim lines are quoted as testimony only when the card was
turned OFFICER) and the recap's key facts follow the flags. History lines for the next game are unchanged: the end
narration lists every role.

## The host
Narration of facts is scripted (templates; `--narrator-agent` makes it a model call). After the end narration the host
adds one model remark of its own, at most 14 words: event `gm` with `"aside": true`. Its voice line (round 8): "Point out
the one irony in how this game ended, as a friend at the table would, in under fifteen words. Not the form 'X, and Y'."
(a reply that opens "X, and ..." gets one more try). Mid-game asides after each death are off since round 8 (they kept
coming back wrong: "Gemma claimed doctor" when she claimed officer, r7a-8); `--asides` brings them back.
Every aside, closing or mid-game, is written from PUBLIC facts only (round 6, `host_facts()`): how many are still in
and out, who is out with the cards the table saw, officer claims made aloud, the day's tally and what the vote did, and
the voted-out player's last words; it is told it knows no hidden card (2026-11-15, r5a: "Three down" with two out,
"Quiet night" after a kill, "the town still hasn't looked at Opus", a hidden killer). At the end it gets the exact end
state and every role. It also sees its own earlier asides of the evening, the first three words each opened with ("Open
differently."), and WHEN ("Night 2: a night kill.", "Day 2: the day's vote (not a night).", or the end state). It
comments on what happened (the vote, the card, a claim, the last words), never on what the table feels, notices or says.
A reply gets one more try, then no aside, when it opens with the same three words as an earlier aside, shares any
three-word run with one, is a near-repeat, or says "nobody", "no one", "everyone", "the table/town still", "saw it
coming" or "chair" (`host_bad()`). An aside over 14 words keeps its whole sentences that fit or is skipped, never shown
cut. It is for viewers only and never enters what players see. A failed call or a junk reply is skipped. Off with
`--plain-host` and in `--dry`.

## Memory between games
With `--games N`, from game 2 on each player's system prompt ends with what a regular remembers of the last three games
of the run (`history_lines()`), one line per game from that player's side (2026-11-15: players got their own past
wrong): "Game 1: you were the officer; you were voted out on day 1, card shown; the table was
wrong about you; the killers were Sonnet and Haiku; both were still in at the end; the killers won, so you lost." How
the killers ended is said in plain words (round 8: "both were voted out", "Sonnet was voted out, Haiku was still in at
the end"; Sonnet had said "Haiku and Gemma killed us" when both were caught). A killer still in reads "you were
still in at the end; the table never caught you". No quotes. With `--open-ballots` a voted-out line adds who voted
("voted out on day 1 by Sonnet, Haiku, Luna"). `--history f1.json,f2.json`
does the same for a single game; `--no-history` turns it off for `--games` (the stats run needs independent games).
The line before the cards gets only the last game's line ("The last game: ..."), not three (round 6: all four wrong
lines of r5a were tallies across games); the game's system prompt keeps three.
**The deal** (round 9): each game is dealt at random from its own seed, derived from `--seed` and the game number (one
game: `--seed` itself). Without `--seed` a fresh seed is drawn, printed ("Seed: ...") and stored in the `cast` event
(`seed`, `game_seed`). Inside an evening a deal is redrawn while the killer pair or the officer equals the previous
game's (read from the previous file, so `--first N` keeps the rule). The before-the-game lines come in a shuffled order.
Until round 9 `--games` dealt by a fixed rotation (`rotation()`, still used by tests and `lab.py`), so evenings opened
alike (r7a-7 and sun15-7 had the same deal). `--killer NAME` forces the killer; `--first N` resumes a batch and still
finds earlier files for history. What else repeats between games: the opening narration lists the seats in seat order
and the quiet night 1 has one fixed narration line (facts, kept); the first speaker of day 1 is drawn at random.

## What every prompt carries (WHAT YOU KNOW FOR SURE)
Own role and night results; players in the game; `Out of the game: X (the officer, voted out day 2), ...` (no role when
face down); `ENDGAME: ...` on a day when one wrong vote and a night kill can end it (the town counts only killers it has
seen leave); `Officer claims so far: Sol (day 1), Luna (day 2, out: card OFFICER)` (dead claimants stay, with their card);
**what the dead said**: each dead player's last words or note, and for a turned OFFICER card up to two lines in which
they claimed or named players (`testimony()`); every past vote on one line with the count per player, a runoff on its
own line, the day's last vote with what it did (`ballot_lines()`): "Day 1 vote: Haiku 4, Gemma 2, Opus 1. Out: Haiku
(card KILLER)." or "Out: nobody (tied)." (round 9, secret ballots; with `--open-ballots` the round-8 form names the
voters: "Day 1 vote: Haiku 5 (Sonnet, Gemma, Sol, Luna, Opus); Gemma 1 (Haiku). ..."). The vote reasons are no longer repeated there. Then WHAT YOU REMEMBER (own notes,
importance 1 to 3) and WHAT YOU HEAR NOW (today's lines, LEANS NOW).

## Lines
- Day lines are cut at 20 words; claims at 30; last words, notes, ghost lines and the line before the game at 25;
  confessions at 30. The limit is stated in the reply format. A line over it is asked once more with the same prompt
  (round 8: three lines of r7a ended in "…", all Luna's); only a second long reply is cut: at the last sentence end; else at the
  last clause break (comma, semicolon, colon, dash) in the second half of the allowed length, closed with a full stop;
  else hard with "…".
- **Junk filter** (`spoken()`) on every spoken line: dropped (silence, not a chosen PASS) when it contains a format
  label (`MONOLOGUE:`, `SAY:`, `NOTE:`, `FORGET:`, `LEAN:`), has no word of three letters, is wholly in brackets,
  parentheses or asterisks, or is "none"; ghost and note lines also when they only say nobody can hear them.
- **Repeat guard**: a line that repeats one of the seat's own lines from any day of the game is asked once more, then
  dropped. A claim or check result may be restated in new words; only a near-verbatim repeat of it is blocked.
- **Loop guard** (2026-11-15, `loops()`, same handling): a day line that circles back to the speaker's own lines of
  the same day: 60% or more of its content words (lowercase, stop words and player names out, crude stems, at least four
  words) are in one earlier line, or it uses a pair of adjacent content words for the third time that day. On
  fin71-1..4 and run81-1..3 it flags 8 of 399 day lines (1, 1, 2, 1, 0, 2, 1 per game), among them Sol's "her card will
  settle my claim" and Gemma's "sol is desperate ... last game". Like claims, a line with "I was shown", "shown to me" or
  "checked" (the officer's evidence) is exempt and only blocked when near-verbatim.
- **Your lines today** (round 6): every reply prompt for a spoken line lists the player's own lines of today under
  `YOUR LINES TODAY:`, one per line, only when there are any. A tighter loop guard (the same adjacent content-word pair
  a SECOND time that day) was measured on r5a and not taken: it flags 58 of 496 day lines (11.7%; 2, 12, 8, 5, 6, 11, 8,
  6 per game), mostly common pairs ("officer claim", "want hear", "turn card"). The third-time rule stays.
- **Own name** (2026-11-15): a SAY line (day, last words, ghost, before the game, confession) in which the speaker uses
  their own name as a word is asked once more with the same prompt, then dropped.

## Vote when ready (LEAN)
Every day line returns `LEAN: <name or none>`. When a strict majority of the living leans on one player and that
majority has held for half a round (ceil(alive / 2) lines in a row; round 9, was one full round) and everyone has
spoken twice on day 1, once on later days (round 9), that player answers twice (a reply in between), one more reply, then the vote. While a majority stands, players
with fewer than two lines get the floor first, even when someone is owed an answer; a pass counts as a turn; a majority
that drops for a line and comes back keeps the answers already given. (Until 2026-11-15 the rule also waited for 2 x
alive lines and for owed replies, and quiet players got the floor only when nobody was owed: it fired on 2 of 15 days.)
`vote_ready_at()` replays the rule on a recorded day. Replayed on the lean sequences of r7a and sun15 (40 days), the
round-9 rule plus budget brings the estimated lines per day from 19.9 (old rule; 21.0 recorded) to 16.8: day 1 23.8 to
20.2, day 2 19.3 to 16.3, day 3 13.7 to 11.3; the vote comes early on 32 of 40 days.

## Event log (what the viewer reads)
Unchanged except:
- `cast.players` has one entry per seat (7 by default).
- `death.role` is the real role unless a hide flag applies (then null).
- `say.why` can be `"last words"` or `"before the game"`.
- `say.claim: "officer"` when the line makes a first-person officer claim (`is_claim()`): the `CLAIM` pattern outside
  quotes and not attributed to someone else ("Gemma said I'm the officer"). Round 8: r7a-1 Haiku was marked for quoting
  Gemma; of the 32 marked lines in r5a and r7a, the other 31 still match. Officer claims so far and the claim word limit
  use the same test.
- `say.lean`: the name of a living player, or absent.
- NEW `note`: `{"type": "note", "name", "text"}`; NEW `ghost`: `{"type": "ghost", "name", "text"}`.
- `gm` may carry `"aside": true` (the host's remark).
- Round 9: `votes` carries `"secret": true` under secret ballots (ballots and reasons are still all there);
  `cast` carries `seed` (the evening's seed) and `game_seed` (this game's).

## Flags
`python3 game.py --help` prints every flag with one line each (`KNOWN` in game.py). An unknown flag prints the same list
and exits with code 2 before anything is called (round 6; checked only when game.py runs as a script, so `lab.py`,
`probe.py` and `check_roles.py` keep their own flags).
`--seats N`, `--games N`, `--first N`, `--history f1,f2`, `--no-history`, `--reveal-night`, `--notes`,
`--checks`, `--kill-night1`, `--no-parity`, `--hide-vote`, `--hide-night`/`--show-vote`/`--quiet-night`/`--no-notes`/
`--parity` (no-ops), `--open-ballots`, `--no-last-words`, `--no-ghosts`, `--repeat-save`, `--no-self-save`, `--plain-host`, `--asides`, `--roles ...`,
`--killer NAME`,
`--seed N`, `--days N`, `--budget N`, `--memory levels|transcript|short`, `--prompt NAME` (print that seat's system
prompt once and every turn prompt; works with `--dry`), `--narrator-agent`, `--classic`, `--tag NAME`, `--fast`,
`--dry`, `--serve`.

## Tools
`tests.py` (unit checks and dry games, a few seconds) · `review.py GAME [--day N]` · `stats.py TAG [TAG ...]` or `--all` (`python3 stats.py r5a r7a`) · `bake.py` ·
`gates.py` · `probe.py N [--checks]` (always plays with `--kill-night1`) · `check_roles.py` · `lab.py` (`--lab bare,hunter`, `--moment`, `--report`,
`--show`) · `sim.py`, `lab_sim.py` (balance, no models).
