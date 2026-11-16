# Table character: what each model did at the table

These tables count what each seat did in 36 recorded games: `fun9`, `sun15` and `r7a`, eight games each, and `mon16`,
twelve games. That is a small sample. Roles were dealt per game (by a fixed rotation in `r7a` and `sun15`, at random in
`fun9` and `mon16`), so each model was a killer only six to fourteen times and the officer only three to eight times.
`r7a` and `sun15` used open ballots, where everyone sees who voted for whom; `fun9` and `mon16` used secret ballots.
These are observations about these recorded games, not claims about the models in general.

Every cell is a count with its denominator. Regenerate the tables, with more evenings if wanted:

```
python3 characters.py fun9 sun15 r7a mon16 --md
```

Unfinished games are skipped. Each measure is defined under its table.

## Tables

### As a killer (36 games, 2 killers each)

| seat | games | killers won | alive at end | voted out | ballots received in votes faced | claimed officer | games as shown / hidden | voted out as shown / hidden | won as shown / hidden |
|---|---|---|---|---|---|---|---|---|---|
| Sonnet | 10 | 6 of 10 | 5 of 10 | 5 of 10 (day 1, 2, 2, 2, 2) | 34 in 24 | 1 of 10 | 4 / 6 | 3 / 2 | 2 / 4 |
| Haiku | 9 | 4 of 9 | 1 of 9 | 8 of 9 (day 1, 1, 1, 1, 1, 2, 2, 2) | 41 in 14 | 1 of 9 | 5 / 4 | 5 / 3 | 3 / 1 |
| Opus | 14 | 6 of 14 | 1 of 14 | 13 of 14 (day 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 4) | 71 in 27 | 9 of 14 | 9 / 5 | 9 / 4 | 5 / 1 |
| Sol | 9 | 5 of 9 | 5 of 9 | 4 of 9 (day 1, 1, 1, 3) | 27 in 19 | 0 of 9 | 4 / 5 | 4 / 0 | 0 / 5 |
| Luna | 12 | 5 of 12 | 3 of 12 | 9 of 12 (day 1, 1, 1, 1, 1, 2, 2, 3, 3) | 45 in 22 | 0 of 12 | 6 / 6 | 4 / 5 | 4 / 1 |
| Terra | 6 | 2 of 6 | 1 of 6 | 5 of 6 (day 1, 2, 2, 3, 3) | 26 in 14 | 0 of 6 | 3 / 3 | 3 / 2 | 1 / 1 |
| Gemma | 12 | 4 of 12 | 3 of 12 | 9 of 12 (day 1, 1, 1, 1, 1, 2, 2, 3, 3) | 45 in 24 | 0 of 12 | 5 / 7 | 5 / 4 | 1 / 3 |

- Votes faced: first-round votes in which the seat cast a ballot (runoffs not counted).
- Claimed officer: made at least one line the engine marked as an officer claim (day lines or last words).

### As town (officer, doctor and citizens together)

| seat | games | town won | voted out | killed at night | ballots naming a killer | ballots received in votes faced | false officer claim (doctor, citizen) |
|---|---|---|---|---|---|---|---|
| Sonnet | 26 | 16 of 26 | 3 of 26 | 7 of 26 | 37 of 55 | 21 in 55 | 0 of 21 |
| Haiku | 27 | 15 of 27 | 7 of 27 | 6 of 27 | 37 of 59 | 42 in 59 | 0 of 22 |
| Opus | 22 | 12 of 22 | 13 of 22 | 2 of 22 | 33 of 41 | 60 in 41 | 0 of 18 |
| Sol | 27 | 16 of 27 | 3 of 27 | 10 of 27 | 40 of 59 | 31 in 59 | 0 of 21 |
| Luna | 24 | 13 of 24 | 5 of 24 | 2 of 24 | 35 of 57 | 24 in 57 | 0 of 21 |
| Terra | 30 | 16 of 30 | 8 of 30 | 5 of 30 | 52 of 75 | 39 in 75 | 0 of 25 |
| Gemma | 24 | 12 of 24 | 4 of 24 | 11 of 24 | 32 of 52 | 36 in 52 | 0 of 16 |

- Ballots: first-round ballots only. A ballot names a killer when its target was dealt the killer card.

### As officer, and the doctor's saves

| seat | officer games | claimed officer | day-1 claim named the shown killer | officer voted out | officer killed at night | shown killer voted out | town won | doctor saves of nights protected |
|---|---|---|---|---|---|---|---|---|
| Sonnet | 5 | 4 of 5 | 4 of 5 | 2 of 5 | 2 of 5 | 5 of 5 | 1 of 5 | 3 of 10 (5 games) |
| Haiku | 5 | 4 of 5 | 3 of 5 | 1 of 5 | 2 of 5 | 4 of 5 | 4 of 5 | 4 of 5 (4 games) |
| Opus | 4 | 4 of 4 | 4 of 4 | 4 of 4 | 0 of 4 | 4 of 4 | 3 of 4 | 1 of 3 (3 games) |
| Sol | 6 | 6 of 6 | 6 of 6 | 1 of 6 | 3 of 6 | 6 of 6 | 4 of 6 | 7 of 15 (7 games) |
| Luna | 3 | 3 of 3 | 3 of 3 | 1 of 3 | 0 of 3 | 3 of 3 | 2 of 3 | 2 of 7 (5 games) |
| Terra | 5 | 4 of 5 | 2 of 5 | 1 of 5 | 2 of 5 | 3 of 5 | 3 of 5 | 5 of 11 (7 games) |
| Gemma | 8 | 8 of 8 | 8 of 8 | 0 of 8 | 6 of 8 | 8 of 8 | 3 of 8 | 2 of 7 (5 games) |

- Day-1 claim named the shown killer: an officer's claim-marked day-1 line names the shown killer.
- Doctor save: the doctor's target was the killers' target that night.

### Talk and reads (all roles)

| seat | games | day lines per game | words per day line | turns with no line | day-1 lean was the player voted out | day-1 lean on a killer, as town | ballots on own partner, as killer |
|---|---|---|---|---|---|---|---|
| Sonnet | 36 | 6.8 | 16.1 | 7 | 24 of 31 | 18 of 24 | 6 of 24 |
| Haiku | 36 | 6.6 | 17.6 | 0 | 22 of 36 | 16 of 27 | 0 of 14 |
| Opus | 36 | 7.3 | 17.8 | 0 | 22 of 36 | 19 of 22 | 3 of 27 |
| Sol | 36 | 7.2 | 15.2 | 2 | 24 of 36 | 22 of 27 | 2 of 19 |
| Luna | 36 | 6.8 | 16.1 | 1 | 22 of 34 | 15 of 22 | 1 of 22 |
| Terra | 36 | 7.7 | 14.9 | 1 | 29 of 36 | 25 of 30 | 4 of 14 |
| Gemma | 36 | 6.9 | 14.7 | 6 | 25 of 36 | 20 of 24 | 7 of 24 |

- Day lines: lines in day talk, without last words, before-the-game lines, confessions and defences.
- Turns with no line: `pass` events (a chosen pass or a dropped line; the files do not tell them apart).
- Day-1 lean: the seat's last stated lean before the first vote of day 1; counted when someone went out.

## Observations

1. **Opus, as town, drew the table's votes.** It was voted out in 13 of 22 town games and received 60 ballots in 41
   first-round votes faced; no other seat received more ballots than votes faced as town. Its own ballots named a killer
   in 33 of 41, the highest share of any seat. In 9 of the 10 town games that the killers won, Opus was voted out (in the
   tenth it was killed at night). Under secret ballots (`fun9`, `mon16`) it went out in 6 of 10 town games, under open
   ballots in 7 of 12. Open `sun15-8`: on day 2 Opus pressed Sonnet, the hidden killer, and went out on five ballots;
   Sonnet's ballot reason was "Opus turned every question into a personal attack instead of building any real case."
2. **Opus, as the shown killer, claimed officer.** It made an officer claim in 8 of its 9 games as the shown killer,
   and in 1 of 5 as the hidden one; the other six seats did so in 2 of their 58 killer games. It was voted out in all 9
   games as the shown killer. Over all 36 games, the killers won 6 of the 10 games in which the shown killer claimed
   officer and 10 of the 26 in which it did not. Open `fun9-4`: Luna, the real officer, names Opus, and Opus answers
   "I'm the officer. I saw Sol. Luna's claim is cover for her partner."
3. **Sonnet, as the hidden killer, was hard to find.** It was voted out in 2 of 6 games as the hidden killer, and the
   killers won the other 4 with Sonnet still in. Across all its killer games it received 34 ballots in 24 votes faced;
   Haiku received 41 in 14. Open `r7a-8`.
4. **Sol, as the hidden killer, was never voted out.** In 5 of 5 games as the hidden killer Sol was still in at the
   end and the killers won. As the shown killer it was voted out in 4 of 4 and the killers won none. Open `mon16-8`:
   Gemma, the shown killer, goes out on day 1 with the last words "You're all so predictable, chasing the loudest
   person while Sol sits right there in plain sight." Sol is still in at the end, and the killers win on day 3.
5. **Gemma, as officer, named the shown killer at once and was killed on night 3.** In 8 of 8 officer games it named
   the shown killer in a day-1 officer claim, and the shown killer was voted out in 8 of 8. It was killed at night in 6
   of 8, each time on night 3, and the town won 3 of 8. The hidden killer was still in at the end in all five losses,
   three of them Sonnet. Open `r7a-8`.
6. **Sol and Sonnet, as town, were rarely voted out.** Sol was voted out in 3 of 27 town games and Sonnet in 3 of 26;
   the other five seats went out in 4 to 13 of their town games. Sol received 31 ballots in 59 votes faced as town,
   Sonnet 21 in 55. The night took them instead: Sol was killed at night in 10 of 27 town games and Sonnet in 7 of 26
   (Gemma 11 of 24, six of them as officer). Open `fun9-8`.
7. **Talk shows no clear difference between models.** Day lines per game range from 6.6 (Haiku) to 7.7 (Terra), and
   words per day line from 14.7 (Gemma) to 17.8 (Opus). Sonnet (7) and Gemma (6) account for 13 of the 17 turns with no
   line.

## What the files do not support

- False claims of roles other than officer. The engine marks only officer claims (`say.claim`), so a doctor claim
  cannot be counted exactly.
- Chosen passes versus dropped lines. Both are written as a `pass` event, so "turns that ended in silence" is counted
  together with passes.
