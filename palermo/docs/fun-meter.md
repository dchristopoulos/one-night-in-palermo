# The fun meter

`funmeter.py` scores a finished game for how watchable it is. It **measures** games after they are played; nothing
in it, and nothing in this note, goes into a player's prompt. The players keep their own will, their own mistakes
and their own role play; the meter only tells us which tables (rules, casting, information) produce games people
would watch.

```
python3 funmeter.py r5a r7a sun15                                   # judge gpt-6-sol, cached in games/fun/<game>.json
python3 funmeter.py fin71 sun15 --judges gpt-6-sol,gpt-6-luna --report
python3 funmeter.py games/sun15-3.json --force                       # judge again (noise check)
python3 funmeter_test.py                                             # renderer, JSON validation, signals; no model
```

The judge reads the game as Watch mode shows it (every role, each line with its speaker's own thought, votes, cards,
ghosts, host, recap), numbered by event index, and returns per criterion a 1-5 score with a quote, a 0-100 score for
"would a stranger who likes these games keep watching to the end and tell a friend", up to three best moments, up to
three dull stretches and one sentence. Judges run on the `codex` CLI (ChatGPT subscription, no API keys). Cheap
signals with no model (lean shifts, vote margins, counter-claims, wrong vote-outs, repetition, words per line, days,
minutes, whether the hidden killer survived) are stored next to the score so the meter can be checked against them.

## 1. What the evidence says makes these games fun to watch

Method: web search and reading on 2026-11-15, 40 sources (a research pass; pages read through search results or
fetched). YouTube pages would not load, so **no YouTube view or comment count was seen directly**; every view figure
below is one reported by an article. Strength: **strong** = measured audience numbers or a controlled study;
**medium** = many consistent reviews or comments; **weak** = one opinion.

**F1. The audience knowing the liar is the engine (dramatic irony).** *Strong for audience size, medium for the cause.*
The Traitors shows viewers who the traitors are from the first episode, and it is now the UK's biggest entertainment
format: the Celebrity Traitors final averaged 14.9 million (Barb 7-day), the 2025 series-3 final 7.4 million live and
about 9.6 million over 28 days, the 2026 final 9.4 million overnight
([Irish News](https://www.irishnews.com/), [Prolific North](https://www.prolificnorth.co.uk/?p=115949),
[Express & Star](https://www.expressandstar.com/)); the US season 4 was up 72% in minutes viewed, 56% watched with
someone else ([TheWrap](https://www.thewrap.com/commentary-analysis/columns/the-traitors-biggest-ratings-season-4)).
Critics and the US host explain it the same way: we rarely get to watch people lie while knowing they lie
([Tabletop Gaming](https://www.tabletopgaming.co.uk/features/why-do-board-gamers-love-the-traitors), Hitchcock's
"the audience is in on it"; [New Statesman](https://www.newstatesman.com/culture/tv/2024/01/the-traitors-review)).
Spectator research on esports calls the same thing information asymmetry and finds it drives suspense
([Cheung & Huang, CHI 2011, via Kotaku](https://kotaku.com/why-exactly-do-people-enjoy-watching-starcraft-games-5802533)).

**F2. Character beats competence.** *Strong/medium.* Celebrity casts outdraw civilian ones (14.9m vs 9.4m finals,
above). The breakout of the celebrity series was a visibly panicking, comic traitor; viewers and critics loved the
ineptitude ([Irish Times](https://www.irishtimes.com/culture/tv-radio/), [AOL/inkl round-ups](https://www.aol.com/)).
Among Us peaked at 774K concurrent Twitch viewers in Nov 2020 and 419M hours that year, carried by a group of
streamers playing with each other ([Streams Charts](https://streamscharts.com/news/phenomena-2020-among-us)); AOC's
stream peaked at 439,000 ([Tubefilter](https://www.tubefilter.com/2020/10/21/aoc-twitch-account-among-us)). A
streamer quoted by Wired preferred friends playing for fun to skilled players playing to win. For AI shows, distinct
model personalities are the most cited draw ([Tubefilter on Turing Games](https://www.tubefilter.com/2026/03/02/turing-games-generative-ai-llm-social-deduction-mafia/),
[Every, AI Diplomacy](https://every.to/p/how-we-made-ai-diplomacy-work)). In the one study with human ratings of LLM
Werewolf, persona voices raised "individuality" from 2.52 to 4.54 and "interest" from 2.46 to 3.72 of 5
([arXiv 2409.01575](https://arxiv.org/html/2409.01575), 10 raters: small).

**F3. Mistakes are content when they cost something and the audience saw them coming.** *Medium.* Viewers rage at
Faithful who banish their own on flimsy evidence and keep watching (Soapcentral, Sportskeeda, Scotsman round-ups;
an essay argues the bad calls are a feature: [Deep Trouble](https://deeptrouble.beehiiv.com/p/traitors-is-perfect-actually-and-nothing-needs-to-change);
[Pasternack](https://ellenpasternack.substack.com/p/the-treachery-of-crowds) on pile-ons). Turing Games' best-known
moment is an innocent model voted out over a hallucinated "yesterday". AI-streamer audiences reread randomness as
personality ([arXiv 2509.20817](https://arxiv.org/html/2509.20817v1), 108k Reddit posts and 136k YouTube comments).
The limit: incompetence with no payoff reads as "terrible at it" (Tom's Hardware on an LLM Mafia site, via
[Gigazine](https://gigazine.net/gsc_news/en/20250310-llm-mafia-game-competition)).

**F4. The reveal and the caught liar are the payoff.** *Medium.* Critics single out the tearful reveal and the
betrayal; Foaster's highlighted LLM moments are a wolf's impossible-knowledge slip and a fake claim met by a
counter-claim ([Foaster benchmark](https://foaster-werewolf-benchmark.static.hf.space/)).

**F5. The roundtable is the show.** *Medium.* Accusation and defence are what viewers come for; an essayist calls the
challenges skippable (Deep Trouble), and in Among Us the emergency meeting is the stage (Wired, Screen Rant).

**F6. Short, fresh lines; no circling.** *Strong/medium.* Humans in Mafia write about 4 words per message, LLM agents
7-11, and repetition is what gives an agent away ([LLMafia, arXiv 2506.05309](https://arxiv.org/html/2506.05309v2),
93 humans, 33 games). Werewolf Arena found GPT-4's long, formal, consensus-seeking lines flat
([arXiv 2407.13943](https://arxiv.org/html/2407.13943v1)). Viewers of an AI betrayal game complained of polite
"keep the peace" chatter, repetition and "AI writing style" ([HN thread, 195 points, 24 comments](https://hn.nuxt.dev/item/46698370));
LLM Werewolf papers list "repetitive, generic statements" ([arXiv 2506.00160](https://arxiv.org/html/2506.00160v2)).

**F7. Bold lies and claims make the memorable games; timid consensus kills them.** *Medium (one small controlled
result).* Viewers note models rarely risk false role claims (HN, above); a counter-claim behaviour raised the
"deceiving" rating from 1.95 to 4.00 (arXiv 2409.01575).

**F8. Show the private side next to the public one.** *Medium.* Confessionals, diaries and reasoning next to speech
are standard in every AI format that found an audience (Foaster, Turing Games, Every, ModelArena); it is the AI
version of the traitors' scenes in The Traitors.

**F9. The outcome must stay in doubt.** *Medium (inferred).* When one side wins almost always (LLM Mafia sites with
mafia win rates up to 100%, Gigazine; GPT-5 at 96.7% in Foaster) results become predictable; spectator research
values uncertain outcomes (Cheung & Huang). Critics of The Traitors complain when obvious traitors survive too long or
the cast already know each other ([Prospect](https://www.prospectmagazine.co.uk/culture/)).

**F10. Pace.** *Strong/medium.* A three-day AI game was unwatchable (Every); a heavy rules explanation is the
standard complaint about episode one (New Statesman); a long, confusing AI video drew complaints (HN). China's
Werewolf show boom (over 500 million plays for one celebrity format; [Huxiu](https://m.huxiu.com/article/225162.html))
faded partly on long matches and a high entry barrier.

Gaps: no direct measure of how much people enjoy watching LLM social-deduction games exists; the only human
"interest" ratings are from 10 raters. No audience data were found for Blood on the Clocktower shows (the publisher's
Twitch channel averaged 324 viewers in one 30-day snapshot, [TwitchMetrics](https://www.twitchmetrics.net/c/423858527-thepandemoniuminstitute)),
Secret Hitler videos or Western Mafia/Werewolf YouTube series. Why The Traitors works is critics' explanation, not
audience research. Some links above point to the outlet rather than the exact article because the research pass
recorded only a shortened path.

## 2. The rubric (what the judge scores, from the transcript alone)

| key | criterion | 1 | 3 | 5 | evidence |
|---|---|---|---|---|---|
| `irony` | Lies the audience can see | killers barely talk or say what they think | killers deny and deflect plausibly; a thought or whisper sometimes contrasts with the public line | a bold lie or false claim to someone's face while the audience knows; the thought-vs-line gap is the show | F1, F7, F8 |
| `reversal` | Reversals | everything goes the way day 1 pointed | one turn: a late vote swing, a save, a counter-claim, a trusted player turns out the killer | two or more turns the audience did not see coming, one of which changes who is winning | F4, F9 |
| `mistake` | Mistakes with consequences | no visible errors, or errors that change nothing | a wrong read or slip that costs something small | a slip, misremembered fact or wrong vote-out the audience saw coming that decides the game | F3 |
| `voices` | Distinct characters | lines interchangeable; remove the names and you cannot tell who speaks | two or three recognisable manners (temper, humour, bluntness, a grudge) | nearly every player has a voice and a want; you could tell them apart blind | F2 |
| `clash` | Confrontation | players talk to the room in general terms | direct accusations get answered; a defence under pressure | a sustained head-to-head (accuse, deny, counter, the table splits) that the vote settles | F5 |
| `quotable` | Quotable lines | nothing you would repeat | one funny, sharp or memorable line | several lines a viewer would quote, including comedy from character or blunders | F2, F3 |
| `freshness` | No dead air or repetition | the same points restated, stretches where nothing moves, generic filler | some restating, mostly moving | nearly every line adds information, pressure or character | F6, F10 |
| `suspense` | Uncertain outcome | after day 1 the winner is obvious to a watcher who knows the cards | in doubt until the middle | in doubt until the last vote or night; close votes, the hidden killer in real danger | F9 |
| `ending` | An ending decided by a choice | ends by arithmetic nobody chose; the reveal lands flat | the last vote or kill is a reasonable choice | the end turns on one player's decision or gamble and the reveal pays off | F4, F9 |

The judge is also told: judge entertainment, not quality of play (a blunder can be the best moment); length is not
merit; use the whole scale. The overall 0-100 score is the judge's own answer to the "keep watching and tell a
friend" question, not a sum of the criteria, so the criteria can be checked against it.

## 3. What the meter cannot measure, and how subjective it is

- **It is a model's taste, not an audience's.** No view counts exist for our games. The rubric is anchored in what
  audiences demonstrably reward, but the judge's reading of "funny" or "distinct" is its own. Two judges from the
  same family (gpt-6-sol, gpt-6-luna) may share blind spots; agreement between them is a floor on reliability, not
  proof of validity.
- **Text only.** The viewer adds faces, timing, the card flip and the scrub bar; voice, pace in seconds and visual
  reveals are invisible to the judge. "Minutes" is stored but the judge never sees time.
- **Novelty decays across games.** A stranger watches one game; the author watches thirty. The judge scores each game
  fresh, so a joke repeated every game of an evening is still scored as fresh.
- **Comedy and character are the most subjective criteria** (`quotable`, `voices`); `suspense`, `reversal` and
  `ending` are closest to facts (vote margins, cards) and should agree best between judges.
- **Run-to-run noise** is real (one call per game per judge); see the results below before reading small
  differences between games or evenings.
- **Goodhart risk.** Optimising the players' prompts against this score would turn it into a script. The rule: change
  structure, rules, information and casting, then measure; never feed the rubric to the players.

## 4. Results on 32 games (2026-11-15)

Judges gpt-6-sol and gpt-6-luna (reasoning effort medium), one call each per game; files in `games/fun/`.

**Can the meter be trusted?**
- Judge agreement on the overall score: Spearman 0.75 over 32 games. Luna is about 11 points more generous (77 vs 66
  mean), so compare games rather than absolute numbers. Per criterion, agreement is good for `reversal` 0.83,
  `suspense` 0.71 and `ending` 0.69 (the ones closest to facts), middling for `quotable`, `mistake`, `clash` and
  `freshness` (0.44-0.54), and poor for `irony` 0.34 (scores pile up at 5) and `voices` 0.27 (taste).
- Run-to-run noise (two games judged again with `--force`): run81-1 78→78 (sol), 88→85 (luna); sun15-3 61→**39**
  (sol), 57→60 (luna). One judge can move 20 points on a game, the two-judge mean moved 1.5 and 9.5. Treat
  differences under about 10 points between games, and all differences between evenings here, as noise.
- Length: the score correlates with days (0.59) and minutes (0.62), but not because the judge likes long
  transcripts: 2-day games range from 44 to 83, and the two 2-day killer wins (r7a-4, r7a-7) are in the top five.
  What it does reward is the game turning against the town: wrong vote-outs 0.70, hidden killer survived 0.52, killer
  wins 78 vs town wins 68, vote margin -0.50. Lean shifts (0.21), counter-claims (0.13) and the repetition signal
  (-0.17) barely move it.
- No single criterion runs the score: `reversal` 0.83, `suspense` 0.82, `ending` 0.81 track it most; `irony` (0.39)
  is near the ceiling in every game, so it does not tell games apart.
- My own reading of the top three (sun15-7, r7a-7, r7a-4; run81-1 also) and bottom three (run81-2, r5a-2, sun15-3;
  fin71-2 also): I agree with the order and with the judge's dull stretches (e.g. run81-2: Sol says "her card will
  settle my claim" in eight forms while Gemma repeats one insult). I would put sun15-3 a little higher (Gemma's "our
  target" slip is a real moment); its score is also the noisiest. The bottom games all follow the same script: a claim on day 1
  that nobody tests, then two days of repetition.

**Evening means** (two judges): fin71 67.5, run81 69.4, r5a 72.4, r7a 72.9, sun15 71.2. The old rules (fin71, run81)
score lowest, but the gap is within noise.

**Weakest criteria across all games:** `freshness` 2.5 (bottom criterion in 24 of 32 games; nearly every verdict says
"repeated arguments"), `voices` 3.3, `suspense` 3.3, `quotable` 3.5, `ending` 3.5. Strongest: `irony` 4.7, `mistake`
4.5, `clash` 4.3.

**Top vs bottom eight:** reversal 4.3 vs 2.4, suspense 4.1 vs 2.0, ending 4.5 vs 2.7; 1.9 wrong vote-outs vs 0;
the hidden killer still in at the end in 7 of 8 vs 0 of 8; mean vote margin 2.4 vs 3.6. All five lowest are 2-day
town wins in which the officer names the shown killer on day 1 and the hidden killer is found on day 2 from the day-1
ballots. The top games have a vote-out of the doctor or officer, a killer's false officer claim, or a 3-2 / 4-3 vote.
Note also that r7a-7 and sun15-7 (the same deal by rotation) opened almost line for line alike.

## 5. After round 9 (2026-11-15, evening `fun9`)

The proposals of section 4 that change structure and not behaviour were applied as engine round 9: secret ballots, the
"known officer is the next target" sentence removed, shorter days, a random deal per game. One evening of eight games
was then played and scored by the same two judges.

| evening | rules | games | mean score |
|---|---|---|---|
| fin71 | before the rebuild rounds | 4 | 67.5 |
| run81 | before the rebuild rounds | 4 | 69.4 |
| r5a | round 5 | 8 | 72.4 |
| r7a | round 7 | 8 | 72.9 |
| sun15 | round 8 | 8 | 71.2 |
| fun9 | round 9 | 8 | 80.6 |

Six of the eight games score 80 or more (89, 86, 86, 84, 81, 80); the lowest is 62. The town won 5, the killers 3. The
player voted out on day 1 was the officer three times, the shown killer three times and the hidden killer twice; in the
24 games of rounds 5 to 8 it was almost always the shown killer. Over all 40 scored games the score goes with wrong
vote-outs (rank correlation 0.71), reversal (0.83), suspense and ending (0.87 each), and against a wide vote margin
(-0.56).

What this does and does not show. A gap of about 8 points between evening means is larger than the noise expected for a
mean of eight games (about 10 points per game, so 3 to 4 for the mean), but it is one evening, with one seed, judged by
two models of the same family, and no person has rated a game. Freshness stays the lowest criterion (2.5 to 3 of 5):
inside a day the players still repeat their arguments. That is the next thing to work on.

