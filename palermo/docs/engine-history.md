# Engine history

This file lists the dated reasons behind rules and checks in `game.py`, newest first, moved out of the code comments so the code keeps only the reason.

## 2026-11-16

- `--model SEAT=BACKEND:MODEL`: any model can take any seat for one run without editing the seat file.

## 2026-11-15

- Round 9: ballots are secret by default and the table sees only the count per player (the Greek house rule). Public ballots solved day 2 in the five worst games of the fun meter. `--open-ballots` brings them back.
- Round 9: the deal is random from the game's seed, redrawn while the killer pair or the officer repeats the previous game. Before, `--games` dealt by a fixed rotation and two evenings opened almost line for line alike (r7a-7, sun15-7). `SHOWN` and `ROTATE` became lab and test hooks only.
- Round 9: without `--seed` a fresh seed is drawn, printed and stored in the cast event.
- Round 9: the day budget became 3 lines per living player plus 3 (24 on a seven-seat day 1, 18 with five, 12 with three), down from 30/26/20/15.
- Round 9: the vote-when-ready gate waits for the majority lean to hold half a round (it was one full round). A quiet player is one who has spoken fewer than twice on day 1, once on later days.
- Round 9: the stake line "A known officer or doctor is the killers' next target ..." was removed from the rules.
- Round 9: the lines said before the cards no longer go in seat order.
- Vote when ready, reworked: the gate fires once the majority lean has held and everyone has spoken. The old gate also waited on 2n lines and owed replies, and quiet players got the floor only when nobody was owed, so it fired on 2 of 15 days and most days ran to the budget with the leans long settled.
- Round 8: `is_claim` ignores quoted claims and claims attributed to someone else. In r7a-1 Haiku was marked as a claimant for quoting Gemma's "I'm the officer".
- Round 8: a SAY line over its word limit gets one more try before it is cut. Three lines of r7a ended in "…", all Luna's.
- Round 8: past votes are listed grouped by target with the voters named. Two players misread who voted whom in r7a, and each misreading cost a citizen.
- Round 8: mid-game host asides are off by default (`--asides` brings them back); they kept getting facts wrong. The closing aside gets one voice line in place of the shape guidance.
- Round 8: a player under half the busiest seat's lines counts as behind. In r7a-7 the officer Haiku had 2 lines on day 1, Terra 6.
- Round 8: the history line says how the killers ended in plain words. Sonnet said "Haiku and Gemma killed us" when both had been voted out and the town had won.
- Round 6: the dead take no part in the night. Until then a voted-out killer whispered a target to the living partner (a "Greek folk rule" kept since before 2026-11-14), so a shown card never silenced a killer.
- Round 6: the floor goes to players who fall behind the day's average. Terra had 5 lines in r5a-2 (named twice) and in r5a-7 (named never), against 8 to 12 for the others.
- Round 6: `host_bad` bans host remarks that speak for the table or repeat themselves. r5a had "nobody saw it coming" five times, "chair" three times, and "the town still hasn't ...".
- Round 6: during the game the host gets public facts only. r5a had wrong counts, invented table moods and "the town still hasn't looked at Opus", a hidden killer.
- Round 6: the recap's `[Day N]` labels are stripped (r5a-5 printed them), and claims are told as claims (r5a-6's recap told a false claim, "named Haiku as his partner", as fact).
- Round 6: the line before the cards sees only the last game. All four wrong lines of r5a were tallies across games, "two killer wins for Haiku's team" when the killers had lost both.
- Round 6: `--help` lists every flag, and an unknown flag prints the list and exits with code 2.
- Round 6: a player's own lines from today are listed apart in the prompt.
- Quiet night 1 is the default again: a night-1 kill left a seven-seat town no spare vote (gr61, killers won 3 of 3). `--kill-night1` turns it off.
- On a quiet night 1 the doctor makes no choice. The choice did nothing in 7 of 7 games, and its no-repeat rule then cost a save on night 2.
- The killers win at parity by default, the standard rule. `--no-parity` makes them outnumber.
- Cards follow research/greek-house-rules.md: a voted-out player shows the card, a night victim does not. On 2026-11-14 every card was turned and the town won 4 of 4.
- Night notes are off by default: the dead say nothing in the Greek game.
- Officer checks are off by default: the Greek officer knows the shown killer and has no other power.
- `loops()` catches a day line that circles back to the speaker's own earlier lines. Sol said "her card will settle my claim" five times, Gemma "sol is desperate ... last game" four. Tuned on fin71-1..4 and run81-1..3: 8 of 399 day lines.
- `names_self()` catches a speaker using their own name: "Luna's warning was the only honest thing she said", said by Luna.
- `end_state()` gives the host the exact end. The host said "Two killers walked out with the win" when one had been voted out.
- `vote_result()` says what a day's vote did. Five times a player said "voted out the officer" about someone who only got votes.
- `history_lines()` writes one line per game from the player's side. Haiku said the table "still got it wrong" when it had been right about him; Gemma said "face down like last time" when her card had been turned.

## 2026-11-14

- All of a player's help is in one fixed system prompt before the persona.
- Round 2: the reply format states the word limit for every task. Day lines went from 14 to 20 words; claims, last words, notes, ghost lines and confessions 25 to 30. Over the limit, a line is cut at a sentence or clause end: 36 of 157 lines had ended in "…".
- The host got its own voice: one short model remark after a death and at the end, for viewers only.
- Officer claims of dead players stay in the claims fact, with what their card showed.
- What the dead said stays known. A town player had called a dead officer's check "just a story now".
- A restated claim is blocked only when near verbatim. Claims had been exempt and got repeated word for word.
- At parity the day is short and the vote has at most one runoff. fun6t-35 ran 22 minutes and nine tied votes at 2 v 2.
- A voted-out player says last words before the card.
- The dead watch: after each day's vote every dead player says one line to the audience.
- With earlier games in the evening, each player says one line about the last game before the cards.
- A night victim can leave one line for the morning (`--notes`; off by default since 2026-11-15).

## 2026-10-27

- Vote when ready: once most of the table leans on one player, that player answers twice, the table replies, then the vote.
- All the help a player gets is in one fixed prompt; a turn's task says whose turn it is and why, never which move to make.

## 2026-10-26

- The mayor is out of the default roles: the ×2 tally names the mayor after the first vote and the killers take them that night.
- A quota error stops the run instead of leaving a seat silent all game (offa-4..12).

## 2026-10-23

- The mayor (option C) was added: a citizen whose vote counts double, shown in the tally.

## Undated

- Short lines that repeat almost the same words count as repeats (lean2-2: Gemma said the same 8 words 3 times).
- A 1 v 1 without the mayor is a killer win (reh-8 ran to day 18: the vote tied forever and a self-saving doctor never died).
- Before a runoff each tied player says one line. Before, a doctor or officer was told to claim in a runoff vote reason that nobody ever heard (reh-8).
- A ghost line close to the player's earlier lines is dropped (smoke1: Gemma's ghost line was her last words again).
- Who has not spoken yet is picked at random, not in seat order: seat 0 had opened 27 of 38 first days.
