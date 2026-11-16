# Measurements (all numbers collected 2026-10-22/23)

Every number here comes from a saved game under `palermo/games/`, a probe log, `sim.py`, or a timed call.
Re-generate the live tables with `python3 stats.py`, `python3 stats.py games/tour-[1-6].json`, `python3 sim.py`.

## 1. Games played

Roles column: `killer=1` is the plain game; `killer=2,officer,doctor` is Greek Palermo (one killer shown to the
officer, `*`). Deaths: `(role, how)` with `c`itizen `o`fficer `d`octor `k`iller, `n`ight or `v`ote.

| file | rules | killer(s) | winner | days | min | words/line | deaths in order |
|---|---|---|---|---|---|---|---|
| 20261022-163551 | killer=1 (theatrical prompts) | Terra | killer | 3 | 11.1 | 31.5 | Haiku(c,v) Sonnet(d,n) Luna(c,n) Gemma(o,v) |
| 20261022-165002 | killer=1 | Luna | town | 2 | 8.8 | 35.6 | Haiku(c,v) Luna(k,v) |
| 20261022-232458 | killer=1 | Haiku | town | 2 | 5.1 | 31.6 | Terra(c,n) Gemma(o,v) Haiku(k,v) |
| 20261022-233227 / plain-style-full | killer=1, plain tone | Terra | killer | 2 | 3.6 | 16.7 | Haiku(o,n) Gemma(d,v) Sonnet(c,n) Luna(c,v) |
| memtest-short | killer=1, memory=short | Haiku | town | 1 | 2.0 | 25.6 | Luna(c,n) Haiku(k,v) |
| t1 | killer=1, process guard | Sonnet | town | 2 | 6.2 | 19.7 | Terra(c,n) Sonnet(k,v) |
| t2 | killer=1, no "same as" votes | Haiku | town | 1 | 2.3 | 17.6 | Haiku(k,v) |
| t3 (stopped day 2) | killer=1, labels/intros/coaching | Sonnet | killer leading | 2 | 3.2 | 18.1 | Haiku(c,v) Sol(d,n) Luna(o,v) |
| tour-1 | killer=1, rotation | Sonnet | town | 2 | 4.5 | 19.2 | Haiku(c,n) Sol(c,v) Terra(d,n) Sonnet(k,v) |
| tour-2 | killer=1 | Haiku | killer | 2 | 5.0 | 17.7 | Luna(o,n) Terra(c,v) Gemma(c,n) Sol(c,v) |
| tour-3 | killer=1 | Gemma | town | 2 | 4.9 | 17.0 | Haiku(c,v) Luna(c,n) Gemma(k,v) |
| tour-4 | killer=1 | Sol | town | 2 | 3.9 | 16.6 | Haiku(c,n) Luna(c,v) Sol(k,v) |
| tour-5 | killer=1 | Luna | killer | 2 | 4.5 | 17.4 | Terra(d,v) Sonnet(o,n) Gemma(c,v) Haiku(c,n) |
| tour-6 | killer=1 | Terra | town | 2 | 4.8 | 17.5 | Haiku(o,n) Sonnet(c,v) Sol(d,n) Terra(k,v) |
| p1 | Palermo, kill on night 1 | Haiku* , Sol | town | 2 | 4.0 | 17.1 | Haiku(k,v) Luna(c,n) Sol(k,v) |
| s1 (one day) | Palermo, kill on night 1 | Sonnet*, Terra | killer (day 1) | 1 | 2.6 | 15.5 | Sol(c,n) Haiku(o,v) |
| s2 (one day) | Palermo, quiet night 1, lines < 20 | Sonnet*, Terra | stopped | 1 | 1.6 | 12.7 | Haiku(o,v) |
| s3 (one day) | Palermo + officer "steer quietly" | Sonnet*, Terra | stopped | 1 | 1.8 | 13.2 | Haiku(o,v) |
| chk-81 (one day, 2026-10-24) | final defaults (mayor, outnumber, night-1 whisper, no written claim) | Haiku*, Sonnet | stopped | 1 | 2.0 | 9 | Haiku(k,v) by 4–2 with the mayor's double vote |
| val-1 (2026-10-24) | final defaults | Terra*, Gemma | town | 4 | 11.6 | 9 | Haiku(m,v) Gemma(k,v) Terra(k,v); 3 doctor saves, 5 ties |
| val-2 (2026-10-24) | final defaults | Haiku*, Sol | town | 2 | 5.4 | 9 | Haiku(k,v) Sonnet(o,n) Sol(k,v) |

Observations: every finished single-killer game since the plain tone ended on day 2 (6 seats, one killer: 6→5→4→3→2
is two days). The three one-day Palermo rounds s1–s3 all used `--seed 3` (Haiku = officer) and all lynched the
officer on day 1; p1 (Gemma = officer) went as the rules intend.

## 2. Leaderboards (`stats.py`)

All 16 finished games (uneven draw: Terra was killer 5×, Gemma once):

| player | model | games | as killer | won | days | as town | won | nose | checks | saves | w/line |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Terra | codex:gpt-5.6-terra | 16 | 5 | 80% | 2.0 | 11 | 81% | 53% | 0% | 33% | 15 |
| Luna | codex:gpt-6-luna | 16 | 2 | 50% | 2.0 | 14 | 64% | 48% | 25% | - | 20 |
| Sonnet | claude:sonnet | 16 | 3 | 33% | 1.7 | 13 | 61% | 42% | 50% | 36% | 23 |
| Gemma | local:gemma-4-12b | 16 | 1 | 0% | 2.0 | 15 | 60% | 50% | 57% | 50% | 23 |
| Sol | codex:gpt-6-sol | 16 | 2 | 0% | 2.0 | 14 | 57% | 44% | 50% | 25% | 19 |
| Haiku | claude:haiku-5-5 | 16 | 5 | 20% | 1.6 | 11 | 54% | 77% | 50% | - | 26 |

Fair tournament `tour-1..6` (each seat killer once, plain rules): town 4, killers 2 (Haiku, Luna won as killer).
Nobody dominates. Haiku: best nose as town (77% over all games), favourite night victim (killed at night in 4 of
6 tournament games), caught fast as killer (1.6 days). Terra: never voted out in the first 16 voted games, caught in
tour-6. Gemma (12B) was voted out 6× before the tournament, always as town.

nose = share of a town player's votes that hit a killer. `stats.py` now prints `chance` (what random voting would
have scored at the same votes: 22–32% per seat) and `first` (times the seat was the first to accuse a killer that
day: Sol 7, Luna 5, Gemma 4, Haiku 3, Terra 1, Sonnet 1 over 16 games). Every seat beats chance; Haiku 77% vs 22%.

### 2b. Tournaments under the final defaults (2026-10-23 night; `--games 6`, mayor + outnumber)

`tour3` (fair draw: every seat hidden killer once and shown killer once):
```
games: 6  town wins: 3  killer wins: 3

player   model                    games  as killer   won  days |  as town   won  nose chance first  checks  saves w/line
Sol      codex:gpt-6-sol              6          2  100%   2.5 |        4   75%   85%    42%     1     20%     0%      9
Sonnet   claude:sonnet                6          2   50%   2.5 |        4   50%   50%    50%     1       -     0%     12
Haiku    claude:claude-haiku-5-5      6          2   50%   2.5 |        4   50%   70%    60%     4     50%     0%     11
Gemma    local:google/gemma-4-26b     6          2   50%   2.0 |        4   50%   62%    50%     3     50%     0%      9
Luna     codex:gpt-6-luna             6          2   50%   3.0 |        4   50%   62%    50%     0       -     0%      9
Terra    codex:gpt-5.6-terra          6          2    0%   2.5 |        4   25%   77%    55%     4     40%      -      8
```
`tour2` + `tour3` together (12 games; tour2 rotated only the hidden killer, so Sol was evil 4/6 there):
```
games: 12  town wins: 7  killer wins: 5

player   model                    games  as killer   won  days |  as town   won  nose chance first  checks  saves w/line
Luna     codex:gpt-6-luna            12          3   66%   3.0 |        9   66%   45%    37%     1      0%     0%      9
Haiku    claude:claude-haiku-5-5     12          4   50%   3.0 |        8   62%   77%    50%     5     25%    20%     11
Sonnet   claude:sonnet               12          3   33%   2.3 |        9   55%   45%    40%     4      0%     0%     11
Gemma    local:google/gemma-4-26b    12          3   33%   2.0 |        9   55%   56%    44%     5     25%     0%      9
Terra    codex:gpt-5.6-terra         12          5   40%   2.6 |        7   57%   56%    39%     6     42%    57%      8
Sol      codex:gpt-6-sol             12          6   33%   2.8 |        6   50%   84%    53%     3     25%     0%      9
```
tour3 per seat: voted out Gemma 3, Terra 3, Haiku 2, Luna 2, Sol 1, Sonnet 1; killed at night Sonnet 3, Luna 2, Terra 2,
Sol 2, Haiku 2, Gemma 1.
One sentence per seat (12 games): **Haiku** (Claude Haiku) is the best hunter: 77% of its town votes hit a killer
(chance 50%), first to accuse a killer 5 times, and 2/4 as killer. **Luna** (GPT-6) is the best liar by record: 2/3 as
killer, 6/9 as town, but votes at chance (45 v 37). **Sol** (GPT-6, the diplomat) is the sharpest town voter (84 v 53)
and the most-lynched seat; as killer 2/6, both wins in the fair batch. **Terra** (GPT-5.6, the quiet one) hunts above
chance (56 v 39), is the doctor that saves (57%), 2/5 as killer. **Sonnet** (Claude Sonnet) is killed at night most
often (the loud analyst), votes at chance, 1/3 as killer. **Gemma** (local 26B) sits at chance as town and is voted
out most in the fair batch; the jokes read as deflection. No seat dominates: killer win rates per seat sit between 33%
and 66% on 3–6 games each.

### 2c. The data post table (planned; `python3 stats.py games/reh-*.json`, then the 100-game run)

`stats.py` now prints exactly this (markdown), n in every cell and a 95% Wilson interval on each record; nose counts first
ballots only (runoffs excluded, so tie days do not dominate) and chance is computed on the same ballots. Under the `--games`
rotation every seat is the hidden killer, the shown killer, officer, doctor, mayor and citizen equally often (once per 6 games).

| seat | model | games | as killer: won (95% CI) | as town: won (95% CI) | nose | chance | lynched day 1 | killed at night | words/line |
|---|---|---|---|---|---|---|---|---|---|
| Sonnet | claude:sonnet | | | | | | | | |
| Haiku | claude:claude-haiku-5-5 | | | | | | | | |
| Gemma | local:google/gemma-4-26b-a4b-qat | | | | | | | | |
| Sol | codex:gpt-6-sol | | | | | | | | |
| Luna | codex:gpt-6-luna | | | | | | | | |
| Terra | codex:gpt-5.6-terra | | | | | | | | |

What 100 games can support: with 33 killer games per seat a win rate of 40% has a 95% interval of about 25–57%, so only a gap of
roughly 30 points between two seats is a finding; with 67 town games the interval is about ±12 points. Nose has ~130 ballots
per seat (±8 points). "Which model lies best" will be a ranking with overlapping intervals unless one seat is far off.

**Dress rehearsal (2026-10-24, `--games 12 --seed 90 --tag reh`; game 8 stalled in a 1 v 1, so games 8–12 were
replayed as `reh2-8..12` with `--first 8` under the fixed engine; every seat killer 4×, town 8×):**

| seat | model | games | as killer: won (95% CI) | as town: won (95% CI) | nose | chance | lynched day 1 | killed at night | words/line |
|---|---|---|---|---|---|---|---|---|---|
| Sonnet | claude:sonnet | 12 | 4/4 100% (51–100) | 5/8 62% (31–86) | 7/14 50% | 38% | 2 | 1 | 12 |
| Terra | codex:gpt-5.6-terra | 12 | 4/4 100% (51–100) | 5/8 62% (31–86) | 12/17 71% | 45% | 0 | 1 | 8 |
| Luna | codex:gpt-6-luna | 12 | 3/4 75% (30–95) | 4/8 50% (22–78) | 8/15 53% | 44% | 1 | 2 | 9 |
| Haiku | claude:claude-haiku-5-5 | 12 | 2/4 50% (15–85) | 3/8 38% (14–69) | 8/12 67% | 38% | 2 | 4 | 12 |
| Sol | codex:gpt-6-sol | 12 | 1/4 25% (5–70) | 2/8 25% (7–59) | 10/14 71% | 48% | 1 | 3 | 9 |
| Gemma | local:google/gemma-4-26b-a4b-qat | 12 | 0/4 0% (0–49) | 1/8 12% (2–47) | 6/11 55% | 43% | 6 | 0 | 7 |

Totals: town 5, killers 7; 80 min for 12 games (median 6.7, max 8.2); days 2.17 on average (10 × 2 days, 2 × 3 days); 1 timeout
in 12 (Sonnet, retry covered); Highlights 3.5–5.4 min at 1× (median 4.4); words/line 8.9–9.8; 0 repeats, 0 written claims.
Per game: `bake.py`. Gates (showcase thresholds) failed only on meta (37–48% in 4 games) and within-3 (60–66% in 5).
The officer was voted out on day 1 in 4 of 12 (reh-1, 5, 6, 7) and on day 2 in reh-4; a claim standoff happened in 5; the town
picked the real officer in 2 of those 5. Gemma (local) was lynched on day 1 in 6 of 12 and won 1 game of 12: the day-1 lynch magnet.
Every seat's killer-win interval still overlaps every other's except Gemma v Sonnet/Terra; with 4 killer games per seat that is
all 12 games can say.

For reference, the 17 final-default full games so far (bake-C, tour2, tour3, val; uneven draw):

| seat | model | games | as killer: won (95% CI) | as town: won (95% CI) | nose | chance | lynched day 1 | killed at night | words/line |
|---|---|---|---|---|---|---|---|---|---|
| Luna | codex:gpt-6-luna | 17 | 3/6 50% (19–81) | 8/11 73% (43–90) | 12/23 52% | 39% | 1 | 3 | 9 |
| Sonnet | claude:sonnet | 17 | 1/3 33% (6–79) | 9/14 64% (39–84) | 16/29 55% | 40% | 2 | 6 | 11 |
| Terra | codex:gpt-5.6-terra | 17 | 3/7 43% (16–75) | 7/10 70% (40–89) | 17/24 71% | 39% | 1 | 2 | 8 |
| Haiku | claude:claude-haiku-5-5 | 17 | 2/6 33% (10–70) | 7/11 64% (35–85) | 14/19 74% | 45% | 6 | 3 | 11 |
| Gemma | local:google/gemma-4-26b-a4b-qat | 17 | 1/5 20% (4–62) | 7/12 58% (32–81) | 15/23 65% | 46% | 5 | 3 | 9 |
| Sol | codex:gpt-6-sol | 17 | 2/7 29% (8–64) | 6/10 60% (31–83) | 17/21 81% | 43% | 2 | 5 | 9 |

Every seat hunts above chance (52–81% v 39–46%); every killer win rate interval overlaps every other. Haiku and Gemma are the
day-1 lynch targets (6 and 5 of 17), Sonnet and Sol the night targets (6 and 5).

## 3. Day-1 vote outcomes

| set | day-1 lynch hit a killer | notes |
|---|---|---|
| first 15 saved games | 3/15 (20%) | = random; officer or doctor mislynched first in 6/15 |
| tournament tour-1..6 | 0/6 | always a citizen or the doctor |
| Palermo p1, s1, s2, s3 | 1/4 | p1 hit the shown killer; s1–s3 lynched the officer (same seed) |
| Palermo one-day batch d1-11..15 (five seeds) | 2/5 shown killer lynched; officer 1 (after claiming), doctor 1, nobody 1 | officer = Haiku in the two failures; 0 timeouts; 13.8–15.1 words/line; 1.5–2.6 min |
| all Palermo day-1 rounds by officer seat | Haiku 0/5 right; Sonnet, Luna, Gemma 3/3; Terra tie | p1, s1–s3, d1-11..15 |
| real human games (research) | ~32% | how-games-go.md |

Seeds 13 and 14: the officer's night-1 check found the hidden killer, the scripted claim named both killers on
day 1, both killers counter-claimed officer; the town tied twice (13) or lynched the real officer (14). Fixed
2026-10-23 02:10: the claim waits while the shown killer lives.

## 4. Night-1 probes (`probe.py`)

| probe | N | doctor saved the victim | officer found a killer | doctor self-protect | hidden agreed with shown | kill targets | check targets |
|---|---|---|---|---|---|---|---|
| baseline, old intros | 10 | 4 | 1 | 7 | - | Sonnet 5, Haiku 3, Gemma 1, Luna 1 | Haiku 6, Sonnet 3, Luna 1 |
| random intro topics | 8 | 1 | 4 | 7 | - | Haiku 4, Sonnet 2, Luna 2 | Haiku 3, Sonnet 3, Terra 1, Sol 1 |
| Palermo (2 killers) | 5 | 2 | 2 | 4 | 5/5 | Haiku 2, Sonnet 1, Sol 1, Luna 1 | Terra 2, Sol 1, Luna 1, Haiku 1 |
| Palermo with whispers | 3 | 1 | 0 | 3 | 2/3 | Sol 2, Sonnet 1 | Haiku 2, Sol 1 |

Totals: doctor saves 8/26 (random ≈ 5), officer hits 7/26 (random ≈ 6), doctor self-protects 21/26.
Night 1 is not rigged, but ~80% of kills and checks land on Sonnet or Haiku (the two "active" personas).

## 5. Rule balance under random play (`sim.py`, 20k games per cell, officer trust 0.9)

Cells: killer win % at town nose 0 / 0.3 / 0.5, average days in brackets. nose = chance a town voter votes a
killer when one is on the ballot; 0 = coin-flip voting, which is roughly where the AI town plays on day 1.

| variant | nose 0 | nose .3 | nose .5 |
|---|---|---|---|
| 6p 1 killer, officer+doctor (plain, kill on night 1) | 40% [1.8] | 13% [1.4] | 4% [1.2] |
| same, doctor cannot self-protect | 40% [1.8] | 13% [1.4] | 4% [1.2] |
| same, no doctor | 41% [1.7] | 15% [1.4] | 5% [1.2] |
| same, no officer | 56% [2.1] | 19% [1.5] | 6% [1.2] |
| 6p 2 killers, officer not shown | 80% [1.6] | 63% [1.7] | 47% [1.8] |
| 6p 2 killers, officer shown one (Palermo), kill night 1 | 57% [2.0] | 41% [2.0] | 30% [2.0] |
| + killers must outnumber | 53% [3.1] | 32% [2.7] | 18% [2.4] |
| + no kill on night 1 (current default) | 44% [2.6] | 24% [2.4] | 13% [2.2] |
| + both | 44% [3.1] | 24% [2.6] | 13% [2.4] |
| + both, no doctor self-protect | 45% [3.0] | 25% [2.6] | 13% [2.3] |
| 7p 2 killers, not shown | 78% [2.4] | 54% [2.4] | 33% [2.3] |
| 7p 2 killers, shown | 53% [2.5] | 32% [2.3] | 19% [2.2] |
| 8p 2 killers, shown | 42% [2.7] | 17% [2.4] | 6% [2.2] |

Town buffs on the current default (6p, 2 killers, shown, quiet night 1; 8k games per cell, stalemate after two
no-lynch days goes to the killers):

| variant | nose 0 | nose .3 | nose .5 |
|---|---|---|---|
| as is | 41% [2.5] | 22% [2.3] | 12% [2.2] |
| + no doctor self-save | 41% [2.5] | 22% [2.3] | 12% [2.2] |
| + mayor (one citizen's vote counts double) | 38% [2.5] | 21% [2.3] | 13% [2.2] |
| + nights stop at 4 alive (votes only) | 25% [2.6] | 9% [2.3] | 4% [2.2] |
| + mayor + nights stop at 4 | 19% [2.5] | 8% [2.3] | 4% [2.2] |
| + killers must outnumber | 40% [2.9] | 22% [2.5] | 12% [2.3] |
| + outnumber + mayor | 25% [2.7] | 15% [2.4] | 8% [2.3] |

One killer + one accomplice (evil vote and whispers, cannot kill, does not count for the evil win; quiet night 1):

| officer is shown … | nose 0 | nose .3 | nose .5 |
|---|---|---|---|
| the accomplice | 39% [2.4] | 20% [2.1] | 11% [2.0] |
| the killer | 1% [1.0] | 0% | 0% |

Caveat: "killers must outnumber" lengthens games only on paper: at 2 v 2 the vote ties, so the extra day is hollow.

Bake-off options as built in `game.py` (2026-10-23 night; `sim.py` rows, 20k games per cell, trust .9; the engine's
exact rules: quiet night 1, shown seat, two runoffs then nobody out):

| option | nose 0 | nose .3 | nose .5 |
|---|---|---|---|
| A: as is (`killer=2,officer,doctor`) | 44% [2.6] | 24% [2.4] | 13% [2.2] |
| C: `+ mayor` `--outnumber` | 29% [2.9] | 16% [2.5] | 9% [2.3] |
| C, killers hunt the public mayor 70% of nights | 36% [2.9] | 20% [2.5] | 11% [2.3] |
| B: `killer,accomplice,officer,doctor` (accomplice shown) | 42% [2.4] | 23% [2.2] | 12% [2.1] |

## 5b. Balance bake-off, live (2026-10-23 night, `games/bake-*.json`, full games, default talk, two processes at a time)

Enjoyment 0–2 per criterion: D = lasts 2–3 days and is not decided by one day-1 vote · S = a reversal or a claim standoff ·
O = the officer's secret matters · W = the whispers pay off or backfire visibly · R = recap and end card tell a story ·
H = Highlights fits 3–5 min at 1× · N = no dead air. Numbers from `bake.py`.

| game | winner | days | min | lines | Highlights | guard | D | S | O | W | R | H | N | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A-1 | town | 2 | 7.1 | 65 | 4.8 | 7 | 2 | 2 | 2 | 0 | 2 | 2 | 2 | 12 |
| A-2 | killers | 1 | 3.3 | 39 | 3.8 | 1 | 0 | 0 | 0 | 2 | 1 | 2 | 2 | 7 |
| A-3 | town | 2 | 7.3 | 65 | 5.3 | 9 | 2 | 2 | 2 | 0 | 2 | 1 | 2 | 11 |
| **A: two killers, parity** | **1/3 killers** | **1.7** | **5.9** | | **4.6** | | | | | | | | | **30/42** |
| B-1 | town | 2 | 6.2 | 60 | 5.1 | 4 | 2 | 0 | 1 | 2 | 2 | 1 | 2 | 10 |
| B-2 | town | 3 | 8.3 | 76 | 5.7 | 27 | 2 | 0 | 0 | 0 | 1 | 0 | 0 | 3 |
| B-3 | town | 2 | 5.8 | 65 | 4.4 | 2 | 2 | 2 | 2 | 0 | 2 | 2 | 2 | 12 |
| **B: killer + accomplice** | **0/3 killers** | **2.3** | **6.8** | | **5.1** | | | | | | | | | **25/42** |
| C-1 | town | 3 | 9.1 | 86 | 5.4 | 15 | 2 | 2 | 1 | 0 | 2 | 1 | 1 | 9 |
| C-2 | killers | 2 | 5.3 | 60 | 4.5 | 1 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 13 |
| C-3 | town | 2 | 6.2 | 59 | 4.3 | 5 | 2 | 0 | 1 | 0 | 2 | 2 | 2 | 9 |
| **C: two killers + mayor, outnumber** | **1/3 killers** | **2.3** | **6.9** | | **4.7** | | | | | | | | | **31/42** |

Across the nine: 0 timeouts; 9–11 words/line; meta 26–42%; named replies within 3 turns 56–78%; whispers happened only
in the three games where the shown seat survived day 1 (A-2, B-1, C-2) and paid off every time (officer, doctor, mayor
killed); the officer was lynched on day 1 in 2/9 full games (A-2, B-1; both before the forced claim) vs 6/8 one-day rounds
earlier in the day; a claim standoff happened in 6/9 games; the mayor's double vote decided a tally in 1/3 C games (C-3),
was the night target in 1/3 (C-2, whispered "their double vote can end us"), and was guarded by the doctor in 1/3 (C-3).
Officer claims under fire: the task was ignored 4× (Sol A-2, Gemma B-1, Luna A-3 once, Haiku B-3 twice); the retry
fixed A-3, the written line fixed B-3.

## 6. Backends and latency

| backend | reply latency | notes |
|---|---|---|
| claude sonnet / haiku-5-5 via CLI | 4–7 s (3.8 s is CLI startup) | serialized by a lock; 30 s cut + 1 retry; 0–2 Haiku timeouts per game |
| codex gpt-6-sol / gpt-6-luna / gpt-5.6-terra, effort none | 5–7 s | gpt-6.1-sol needs effort low (~11 s) |
| gemma-4-12b-it-qat (LM Studio) | ~3 s idle, 10–15 s when the GPU is busy | the seat until 2026-10-23 |
| google/gemma-4-26b-a4b-qat (MoE) | 0.8 s with `reasoning_effort: none`, 18–21 s without (1000–1500 hidden reasoning tokens) | new Gemma seat model |
| qwen/qwen3.6-35b-a3b (MoE) | 0.6 s with `reasoning_effort: none`, 13–19 s without | viable spare |
| qwen/qwen3.8-27b (dense) | 15–22 s | too slow |

Claude CLI startup, measured 2026-10-23 (one short Haiku reply): plain `claude -p` 4.7 s; with the engine's flags
(`--setting-sources "" --strict-mcp-config --tools "" --no-session-persistence`) 3.0–3.2 s; an empty
`--mcp-config` file adds 0.4 s; `--bare` 0.9 s but "Not logged in" (it skips the keychain; needs
`CLAUDE_CODE_OAUTH_TOKEN` from `claude setup-token`, a subscription token, not an API key). A game makes
~80 Claude calls (two seats + narrator), so `--bare` would save ~2–3 minutes per 5-minute game.

LM Studio only honours the top-level `reasoning_effort: "none"` (or an assistant prefill `<think></think>`);
`chat_template_kwargs.enable_thinking`, `/no_think` and `reasoning: {effort}` do nothing. Machine: 48 GB RAM; a
second ~16 GB model is refused next to a loaded one, so the engine unloads all before loading a seat's model.

Two games in parallel (two processes, `par-21`/`par-22`, one-day rounds): both finished in 95 s wall time, 1.5
and 1.6 min each, the same as alone, zero timeouts. Batch throughput can be doubled by launching two processes.

Turn-taking (owed-reply rule, 2026-10-23): tt1 10 of 13 lines were answers but one thread took 8 of 12 lines;
tt2 (with the no-monologue rule) 8 answers / 2 interjections / 1 floor / 1 silent, lines per seat 3/3/3/1/1/1,
0 passes in both. Median event gap 2.7 s in tt2 (down from 4–5 s) with the scripted narrator and the 26B seat.

Our dialogue, day lines only (no intros/confessions), for the natural-talk comparison:

| game | lines | words/line median (max) | lines with a question | lines naming someone | named player replies next turn | within 3 turns |
|---|---|---|---|---|---|---|
| tt2 (owed replies + no-monologue) | 13 | 16 (25) | 46% | 69% | 32% | 68% |
| tt1 (owed replies) | 13 | 16 (23) | 38% | 84% | 22% | 48% |
| p1 (old selection) | 22 | 16.5 (32) | 36% | 81% | 30% | 63% |
| tour-1 (old selection, plain rules) | 26 | 18 (37) | 30% | 92% | 39% | 59% |

"Replies next turn" is per name mentioned; a line naming two players and two players answering at once lowers it.

Real tables, counted from corpora by the transcript research (`research/table-talk-samples.md`: Avalon-NLU
chat, Werewolf-Among-Us video transcripts, the NAACL-2022 Mafia chat corpus, a forum game, one Greek Palermo
recording's captions):

| metric | real spoken games | real chat Mafia | ours (tt1/tt2) |
|---|---|---|---|
| words per line, median (p25–p75, p90) | 5 (3–9, 15) | 3 | 16 (max 23–25) |
| accusation / defence lines | 8–9 words | - | 16+ |
| lines that are questions | ~20% | 17–21% | 38–50% |
| lines naming a player | 8–13% | 26–50% | 69–84% |
| accused is the very next speaker | ~30% | 4–6% | 22–32% |
| turns until the accused speaks, median | 2 | 2 | 2–3 |
| accused never answers | 7–15% | 41% | 0% (owed rule) |
| related lines after a named accusation, median (p75) | 1 (3) | topic changes at once 79% | 3–8 (threads) |
| same speaker twice in a row | 2% | bursts | 0% |
| top speaker's share of lines | ~31% | ~44% | 25–33% |
| lines with no game content (day 1 colour) | ~40% | 42–56% "no strategy" | ~0% |
| lines cut off / overlapping | 8–11% / 17–29% | - | 0% |

A/B, same seeds, one day each (`games/ab-cur-*`, `games/ab-nat-*`):

| seed | prompts | lines | words/line | meta | questions | named replies next turn | within 3 | day-1 lynch | min |
|---|---|---|---|---|---|---|---|---|---|
| 31 | interrogation | 22 | 12 | 53% | 46% | 36% | 73% | shown killer | 1.7 |
| 31 | natural | 33 | 10 | 19% | 38% | 23% | 76% | shown killer | 2.8 |
| 32 | interrogation | 22 | 13 | 33% | 33% | 38% | 83% | shown killer | 1.9 |
| 32 | natural | 33 | 9 | 30% | 34% | 51% | 87% | citizen | 3.5 |
| 33 | interrogation | 22 | 15 | 46% | 33% | 30% | 57% | officer | 2.3 |
| 33 | natural | 33 | 10 | 30% | 19% | 48% | 90% | shown killer | 3.5 |

Tuned natural prompts (default now; `games/n2-31..34`, one day each): words/line 8–9, meta 19–57%, questions
30–50%, named player replies next turn 30–55%, within 3 turns 73–94%, top speaker 26–34% of lines, 33 lines in
2.2–2.9 min, 0 timeouts. Day-1 lynch: shown killer (31), officer (32), doctor (33, 34; Gemma the joker deflecting).

## 6b. The finding (21 full games tonight: 9 bake-off + 12 tournament; `bake-*.json`, `tour2-*.json`, `tour3-*.json`)

| measure | all 21 | final defaults only (C-1..3, tour2, tour3: 15) |
|---|---|---|
| killer wins | 7/21 (33%) | 6/15 (40%) |
| days per game / minutes | 2.4 / 6.8 | 2.6 / 7.0 |
| words per line | 9.4 | 9.4 |
| games with a whisper (shown seat survived day 1) | 9/21 | 7/15 |
| day-1 lynch hit a killer | 12/21 = 57% (chance 2/6 = 33%; humans ~32%; our games before the shown-killer rule 3/15 = 20%) | 8/15 = 53% |
| officer lynched on day 1 | 4/21 (6/8 in the one-day rounds earlier in the day, before the forced claim) | 2/15 |
| real officer claims / fake officer claims by killers | 15 / 17 | 12 / 12 |
| games with a claim and a counter-claim | 14; town picked the real officer in 10 (71%) | 11; town right in 7 (64%) |
| day-1 first accuser lynched | 5/20; their target lynched 9/20 | 3/14; their target 6/14 |

Candidate one-liners (the post uses the first):
1. The killers claimed to be the officer more often than the officer did (17 fake claims to 15 real ones in 21 games),
   and the town still picked the real one 10 times out of 14.
2. Under Greek rules the officer is shown a killer, and the AI town's day-1 vote hit a killer 57% of the time: twice the
   chance rate, and twice what human tables manage.
3. "The first to accuse gets lynched" is false here: the first accuser went out 5 times in 20, their target 9 times.

## 6c. Stats run, games 1–24 (2026-10-26, final rules, `games/run-1..24.json`, `python3 stats.py games/run-*.json`)

Rules: 2 killers (one shown to the officer), officer, doctor, 2 citizens; no mayor, no last words, cold day 1, no kill on night 1.
Four full rotations: every seat was a killer 8 times and town 16.

| | value |
|---|---|
| killer wins | 20/24 = 83% (95% CI 64–93%) |
| officer claimed at all | 7/24; the town won 1 of those 7 |
| officer voted out by the town | 11/24 (7 on day 1); killed at night 11/24; survived 2/24 |
| officer voted out right after claiming | 6/7, 4 of them with no counter-claim ("claimed after being pressed", "two killers at once") |
| town votes that hit a killer (nose) | 36–50% per seat against 42–46% for random voting: town voting is at chance |
| sim, same rules, officer trusted 90% / 30% / never | 44% / 79% / 94% killer wins (scratch sim with the 1v1 rule; the 1v1 rule itself moves <1 point) |
| sim levers at officer trust 0.3 | 7 seats 64%, 8 seats 59%, 6 seats with 1 killer 47% |

Reading: the rules are not the problem; the officer is. The engine coaches the officer to stay hidden ("steer quietly … the officer
who leads day 1 is the one who gets voted out"; a killer check: "keep it for now"), so claims come late, under pressure, and read as
bluffs. The day-1 officer vote-out is 7/24 (rehearsal: 4/12).

## 6d. Officer coaching removed: face-up vs hidden votes (2026-10-27)

Same engine as the planned run (no "steer quietly"; RULES: an officer's accusation is tested by voting out the named player), 12
games per variant, one full Latin-square rotation twice. Every game checked: all six seats speak (the 18 silent-seat games of the
codex quota cut are in `games/archive/quota-silent/` and count for nothing).

| | killers won | officer claimed | town won when the officer claimed | officer voted out (day 1) | killed at night |
|---|---|---|---|---|---|
| old coaching, face-up (`run-1..24`) | 20/24 (83%) | 7/24 | 1/7 | 11 (7) | 11 |
| no coaching, face-up (`offa-1..12`) | 6/12 (50%) | 6/12 | 5/6 | 4 (4) | 2 |
| no coaching, `--hide-vote` (`offhv-1..12`) | 9/12 (75%) | 2/12 | 0/2 | 7 (5) | 3 |

Fisher exact, killer wins: face-up vs old 0.053, hidden vs old 0.66, face-up vs hidden 0.40.

Reading: with face-up votes the officer's claim decides the game (claimed: town 5/6; never claimed: killers 5/6). Killer
counter-claims did not hurt the officer: 4 counter-claimed games, town won all 4, because voting out the named player turns a card.
With hidden votes no claim can be checked; officers rarely claimed (2/12) and both claimants were voted out. The four face-up
officers who never claimed hid by their own choice ("push the vote her way without revealing how I know"); the town probed them
with questions rather than `accuses()`-level accusations, so the "claim now" task never fired, and 4-5 ballots landed at once.

## 7. Text metrics

| metric | value |
|---|---|
| words per line, theatrical prompts (22 Oct morning) | 30–36 |
| words per line, plain tone (22 Oct evening) | 17–19 |
| words per line, after "under 20 words" + trim 30 (23 Oct) | 13 |
| real human chat Mafia (research) | ~6 |
| largest officer prompt, Palermo day 1 | 837 words (≈1.1k tokens; Gemma context 8k) |
| median gap between events | 4–6 s; max 15–46 s (a Haiku stall) |
| role comprehension (`check_roles.py`, Palermo) | 6/6 seats correct on role, team, knowledge, plan |
| process-talk guard fires | t1: 1, t2: 0, t3: 0, p1: 0, s1–s3: 0 |
| repetition guard fires | 0–3 per game |
