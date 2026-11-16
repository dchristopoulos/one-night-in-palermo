# Balance at six seats (analysis, 2026-10-23)

Constraint: six seats, no more models (usage and readability). Two killers "feel too OP".

## What the numbers say
- Under random voting the current default (two killers, one shown to the officer, no kill on night 1, hidden
  night roles) gives the killers 41–44% and games of ~2.5 days (measurements.md §5). That is balanced on paper,
  and town-favoured (22–24%) once the town votes a little better than chance.
- The AI town votes at about chance on day 1 (3/15 in the first games, 0/6 in the fair tournament, 1/4 under
  Palermo rules; humans ~32%). The killers actively frame, which cancels the town's nose.
- The real problem is structure, not win rate: with two evil votes out of six, one wrong lynch on day 1 means
  2 v 2 at dawn of day 2 and the killers win (parity). Three of four Palermo rounds ended that way, all with
  the same seed (officer = Haiku, the loud seat, lynched for pushing the shown killer).
- Buffs that only add a day (killers must outnumber) are hollow: at 2 v 2 the vote ties.
- Buffs that stop the night kill at 4 alive over-correct (killers 25% / 9% / 4%).

## Options (all six seats)
| option | killer win % (nose 0/.3/.5) | days | what it feels like | cost |
|---|---|---|---|---|
| A. two killers, as now | 41 / 22 / 12 | 2.5 | one wrong day-1 vote loses; day 2 needs a second hit or a doctor save | done |
| B. one killer + one accomplice (shown to the officer; whispers, votes, lies, cannot kill, does not count for the evil win; town wins when the killer is out) | 39 / 20 / 11 | 2.4 | the pair still conspires and vouches; the town needs ONE correct lynch; a day-1 miss does not end the game at dawn | medium: a role, win rule, facts, tests |
| C. two killers + mayor (double vote) + killers must outnumber | 25 / 15 / 8 | 2.7 | the mayor becomes the killers' must-kill; town-favoured | medium |
| D. two killers, nights stop at 4 alive | 25 / 9 / 4 | 2.6 | pure deduction endgame; too town-favoured | cheap |
| E. one killer, plain game | 40 / 13 / 4 | 1.8 | no pair, no secret for the officer; games end on day 2 | done |

## The structural fact behind the failures (5-seed batch, 2026-10-23)
When the officer claims early and names both killers, both killers counter-claim officer. Three claims, a jury
of three townies, and the two killers vote too: one confused townie makes it 3 v 3 (tie, nobody out) or 4 v 2
against the real officer. "Lynch all liars" would resolve it in two days, but six seats with two evil votes
give the town one day. Any pair design with two evil votes among six has this shape; the random-play sims
understate it because simulated killers do not coordinate their votes.
What helps: (1) the officer gets the shown killer lynched quietly on day 1 and claims the guilty on day 2,
when only one liar is left to counter-claim (now the engine's coaching); (2) a tie-breaker on the town side
(mayor with a double vote), which also gives the killers a real night dilemma (officer or mayor) and the doctor
a real choice; with the mayor, "killers must outnumber" stops the 2 v 2 auto-loss. Option B (accomplice) has
the same two evil votes and only delays the loss by a day after a mislynch.

## What the roles research adds (research/roles-catalog.md)
With quiet night 1 every vote happens at an even count (6, then 4), so the town gets exactly two votes and any tie
resolved as "nobody out" is a killer win; Plotkin's random-lynch arithmetic gives the town ~13% with two wolves at
this size. No published six-player setup has two killers + checking officer + doctor. The sourced fixes, cheapest
first: mayor as reveal-to-activate tie-breaker (Δήμαρχος); hunter who shoots when voted out (a day-1 mislynch is
not fatal); the Greek votes-only endgame at 4 and 3 with mayor-then-lot tie-break; witch instead of doctor;
neighbour (told two names, one the shown killer). The jester's win should not end the game at six.

## Recommendation (revised after the batch)
Keep the authentic pair (A) and fix the vote arithmetic rather than the pair: deferred officer claim (done)
plus option C, a secret mayor whose vote counts double and "killers win only when they outnumber the town".
With it a day-1 mislynch is survivable (2 v 2 becomes a town lynch), the killers must choose between the
officer and the mayor at night, and the doctor's protection finally matters. Random-play numbers 25/15/8 are
town-favoured, but against coordinated AI killers the real figure will sit higher; measure with one-day and
two-day rounds before a tournament. Option B (accomplice) is the fallback if the pair must be weaker.
Pending: the roles-catalog research may offer a better-sourced tie-breaker than the mayor.

## Officer play (does our officer play it right?)
Research consensus (how-games-go.md §2, §4): don't claim on day 1 without a result; steer the vote onto the
shown killer with ordinary reasons; claim when holding a guilty or when about to be lynched; a lone claim is
trusted until a counter-claim; "Follow the Cop" (claim day 1 and let the doctor guard you) is a legitimate
alternative when a doctor exists. Our officer now gets exactly these as facts and coaching. What still fails is
persona: the Haiku seat opens by pushing someone and the table lynches the pusher. p1 (Gemma as officer)
played the textbook game. Open: measure the day-1 outcome over several seeds (batch running), and consider
a seat-independent rule that the officer never takes the floor first on day 1.
