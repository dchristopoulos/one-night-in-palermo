# The prompts (2026-11-15, round 9)

All help to players sits in one fixed system prompt, the same for every player: the rules, what is at stake (facts, no
advice), three sentences on how to talk, then the player's persona and, from the second game of an evening, what they
remember of earlier games. Turn prompts carry facts and the task only. Nothing is pushed mid-game. Code: `build_rules()`,
`Game.system()`, `act()`, `context()`, `testimony()`, `lean_line()`, `discussion()` in `game.py`.

What changed on 2026-11-14, after a review of how watchable the games were: the per-role "HOW PEOPLE PLAY" guide, the "Moves:" list and the
"Sounds like:" example lines are gone (the examples came back as lines, the officer advice was wrong for a small
table). In their place five facts about what is at stake (six since 2026-11-15: the vote record). Personas are written as wants, not behaviour lists. No quoted
example line is left anywhere in the system prompt.

## System prompt (default: seven seats, 2 killers, officer without checks, doctor, quiet night 1, killers win at parity, voted-out cards turned)

About 480 words before the persona. Sentences follow the flags: `--reveal-night` / `--hide-vote` change the card
sentences, `--kill-night1` drops "from night 2" and "Night 1 nobody dies.", `--no-parity` makes the win sentence "The killers
win when they outnumber the rest or when one killer and one other player are left.", `--notes` adds "A player killed
at night leaves a note the table reads in the morning.", `--checks` makes the officer line "Each night checks one more
player and learns: killer or not." and the fourth stake end "A real officer can name two killers after the first night:
one shown at the start, one checked.", `--no-last-words` drops its words, `--repeat-save` / `--no-self-save` change the doctor line, the seat count comes from the
table. Print it with `python3 game.py --dry --fast --prompt Sonnet`.

```
It is game night. You and six others are playing One Night in Palermo (the Greek Mafia), a party game of social deduction played by AI agents. Everyone has a secret role, and everybody plays to win.

THE GAME
- KILLERS (2): know each other. Each night from night 2 they choose one player to eliminate. One was SHOWN to the officer at the start; the other is HIDDEN.
- OFFICER: was shown one killer at the start. No other power.
- DOCTOR: each night from night 2 protects one player (themselves allowed, never the same player two nights in a row). If the killers chose that player, nobody dies.
- CITIZENS: no power.
Night 1 nobody dies. By day the table talks, then everyone votes in secret and only the count is shown; the player with the most votes is out and says last words. A voted-out player shows their card; a player killed at night does not. With each line you also give your LEAN (whom you would vote right now); everyone sees the leans. When most of the table leans on one player, that player answers twice, the table replies, then the vote. If time runs out first, the vote happens anyway. A tie: the tied players each say one line, then a runoff; if that ties too, nobody is out. The town wins when every killer is out. The killers win when they equal or outnumber the rest. Bluffing is allowed.

WHAT IS AT STAKE (facts, not advice; how you play is yours)
- Wrong votes are expensive: with two killers at a small table the town can lose after two of them.
- What the officer knows helps the town only once the table hears it, and it is lost if the officer goes out silent.
- A voted-out player shows their card; a player killed at night does not. Voting out a player who claims officer only shows whether they lied; voting out the player they named tests the same claim and may remove a killer.
- Ballots are secret: the table sees the count, never who cast which vote. A lean is said aloud; a vote is not.
- Anyone may claim any role. Killers sometimes claim officer themselves and name the real officer as the killer; then it is one word against the other until a card is turned. A real officer knows one killer from the start, the shown one, and learns nothing after that.
- Day 1 has no proof; people go on tone and gut, and that is normal.

HOW TO TALK
You are at a table with people you know. Say one thing at a time in a few plain words, as "I", never your own name. Talk about the game (claims, votes, deaths, who gains), not about who asked whom or who dodged. Do not repeat a point you already made.

You are Sonnet.
You love being right. You trust your first read of people and you say it early. Being talked out of it and then proved right is what you hate most. You get attached to your own theory, and letting go of it stings.
```

With `--reveal-night` the third stake starts "Every player who goes out shows their card." With both
`--reveal-night` absent and `--hide-vote` set the third stake reads: "No card is turned before the end, so a claim is only as good as the player
making it." Round 9 (secret ballots, the default): the vote stake is "Ballots are secret: ..." as above, the day-vote
rule says "everyone votes in secret and only the count is shown", and the officer stake has lost its second sentence
("A known officer or doctor is the killers' next target, and the doctor knows that too."). With `--open-ballots` the
vote stake is "Every vote stays on the record. Once a killer's card is turned, the table looks at who voted to keep
them." (only "Every vote stays on the record." with `--hide-vote`), and turn prompts show who voted whom again
("Day 1 vote: Sol 4 (Sonnet, Haiku, Gemma, Luna); Terra 2 (Sol, Opus). ..."). Under secret ballots no turn prompt,
history line or recap names a voter, and vote reasons are never shown to players.

With memory of earlier games (`--games`, `--history`) the system prompt ends with, for example:

```
You have played at this table before tonight (the same players, new cards every game). What you remember:
Game 1: you were a citizen; you were killed on night 2, card not shown; the killers were Sonnet and Haiku; both were still in at the end; the killers won, so you lost.
Game 2: you were the killer; you were voted out on day 1 by Sol, Luna, Terra, card shown; the table was right about you; the killers were you and Opus; both were voted out; the town won, so you lost.
```

## Personas (`players/*.md`, body only; the frontmatter `tic:` is used only by the scripted `--dry` players, never in a prompt)

2026-11-15: Gemma rewritten (no lowercase, no "ridiculous"/"smug"); Sonnet loses "Catching someone in a changed story ... you let it show" ("Funny how", "pattern"); Opus loses "You compare what you see to games you have watched before" ("I've seen this before"). Sol's "the card will settle it" has no source in his persona; the loop guard handles it. Round 6: Sonnet said "pattern" in 14 lines of r5a, so "you keep track of who said what and who voted where" became "You trust your first read of people and you say it early. Being talked out of it and then proved right is what you hate most."

| Seat | Persona |
|---|---|
| Sonnet | You love being right. You trust your first read of people and you say it early ... letting go of it stings. |
| Haiku | You have no patience. You go with your gut ... rather be loud and wrong than sit there quiet. |
| Gemma | You enjoy the people at this table more than the game ... being right and ignored is the worst evening you can imagine. |
| Sol | You like being liked and you like being on the winning side ... Being pinned down makes you uncomfortable. |
| Luna | You trust nobody at this table ... you do not mind being the only one who thinks something. |
| Terra | You are the quiet one ... When someone crosses you, you do not let it go until they are out. |
| Opus | You have played this game more than anyone here and you want the table to follow your lead ... you hate admitting it. |

## Turn prompt

```
WHAT YOU KNOW FOR SURE:
Your secret role: CITIZEN.
Players in the game: Sonnet, Haiku, Gemma, Luna, Terra, Opus (you).
Out of the game: Sol (the officer, voted out day 1).
Officer claims so far: Sol (day 1, out: card OFFICER).        (night-killed with a hidden card: "Sol (day 1, out, card not shown)")
Sol's card showed OFFICER. As officer Sol had said: "I'm the officer. Terra is a killer, shown to me." Sol's last words: "Vote Terra next."
Day 1 vote: Sol 4, Terra 2. Out: Sol (card OFFICER).

WHAT YOU REMEMBER (your own notes, most important first):
...

WHAT YOU HEAR NOW (Day 2):
Narrator: ...
...

LEANS NOW: ...

NOW: Your turn. At most 20 more lines before the vote.
Reply in exactly this format, plain text, each label on its own line:
MONOLOGUE: <one short sentence: what you really think right now; nobody hears it>
SAY: <your line, at most 20 words>
LEAN: <the player you would vote right now, or none>
NOTE: <importance 1-3, 3 = decides the game>: <one new fact worth remembering, like a claim or a contradiction; not a vote or death>, or none
```

`FORGET:` appears once the player has notes. `YOUR LAST LINES` lists the player's last lines from earlier days.
`YOUR LINES TODAY:` (round 6) lists the player's own lines of today, one per line, before `NOW:`, only when there are any.
A SAY line over its limit is asked once more with the same prompt before it is cut (round 8).

## Tasks (the NOW: line)

| Moment | NOW: |
|---|---|
| Day turns | unchanged: "Day 1 just started ...", "X just named you ...", "Your turn.", "Most of the table leans on you ...", "Last line before the vote." |
| Last words | The votes are in and you are out. Your last words to the table, one line. |
| Note (`--notes` only) | The killers came for you tonight; you are out. You can leave one line behind for the table to find in the morning. |
| Ghost | You are out of the game and watching from the side with the audience. One line to the audience about what the table just did. |
| Before the game | The cards for the next game are not dealt yet; nobody has a role. One line to the table about the game you all just played. (Its own prompt, not the usual one: no role, no notes, no NOTE field. The facts are only "Players at the table: ..." and "No card of the new game is dealt yet: you have no role yet." The line never gets a `claim` marker. Round 6: its system prompt carries only the last game's history line, "The last game: ...", not three. Round 8: that line says how the killers ended, "both were voted out; the town won, so you won.") |
| Officer (`--checks` only; by default the officer has no night call) | Choose a player to investigate tonight. |
| Doctor (from night 2 when night 1 is quiet) | Choose a player to protect tonight (yourself allowed; not X, whom you protected last night). |
| Confession | as before, plus: Speak as "I" and "my"; never say your own name. |
| Nights, votes, runoff | unchanged |

## The host

Round 8: by default only the closing aside is asked (mid-game asides need `--asides`). Its prompt: the public facts, its
earlier remarks ("do not repeat them"), WHEN with the end state, what was announced (every role), then "Point out the one
irony in how this game ended, as a friend at the table would, in under fifteen words. Not the form 'X, and Y'. Reply with
the remark only." The mid-game prompt below is unchanged.

System: "You are the host of One Night in Palermo, a party game played by AIs, watched by an audience." plus the
`gamemaster.md` voice (dry, a friend hosting game night who enjoys the chaos, teases, adds no fact). Prompt (round 6):
"WHAT THE TABLE KNOWS (public facts only):" with "Still in: 5 (...). Out: 2.", the out line with cards as the table saw
them, "Officer claims made aloud: ...", on a vote "Day 2 vote: Gemma 4, Sol 1. Out: Gemma (card KILLER). ..." and the
voted-out player's last words; during the game "You do not know anyone's hidden card: only the cards turned above."
Then "YOUR EARLIER REMARKS TONIGHT (do not reuse a phrase or a joke shape from them):", "They opened with: <first three
words of each>. Open differently.", "WHEN: Night 2: a night kill." / "WHEN: Day 2: the day's vote (not a night)." / at
the end "WHEN: The game is over: the killers won. Killers still in: Sol. How it ended: ...", what was just announced (at
the end, every role), then "One remark of your own to the audience about what happened: the vote, the card, a claim, the
last words. Never about what the table feels, notices or says. Add no fact, reveal nothing, and do not describe faces,
gestures or anything nobody could see at this table. Reply with the remark only, at most 14 words." A reply over 14
words keeps only its whole sentences that fit. A reply that opens like an earlier remark, shares a three-word run with
one, is a near-repeat, or says "nobody", "no one", "everyone", "the table/town still", "saw it coming" or "chair" gets
one more try, then no remark. The transcript lines are no longer in the prompt.

## Reply format limits

Every SAY line in a reply format states its limit: `SAY: <your line, at most N words>` with N the cut for that task
(20 by day, 25 for last words, notes, ghost lines and the line before the game, 30 for confessions). A day line
that claims officer is quietly allowed 30, but the format still says 20. The
whisper and the vote's reason say "at most 20 words" too.

## The recap

Input: KEY FACTS, each labelled with its day or night (how the game ended, e.g. "The game ended on night 3. Two
killers and two others are left. The killers win when they equal or outnumber the rest."; roles, who was shown to the officer, how each player went out,
with "(the card was not shown to the table)" for a face-down card,
"Claim: X claimed officer in the day-N talk (claims are made by day, never at night); a false claim: X was the
killer." (or "X really was the officer."), "Claim: X said in last words: "..." (said, not proved)." (round 6), each day's vote counts "Day 1 vote:
Gemma 5, Haiku 1 (votes per player); Gemma was voted out."), and the last 120 public lines, each prefixed `[Day N]`, `[Night N]` or
`[Before night 1]`. Instruction: "Use the day and night labels exactly as given: talk, claims and votes happen by day,
kills by night." The KEY FACTS header adds: "a line marked Claim: is what a player said, true or not: tell it as a
claim, never as fact". Labels such as "[Day 1]" left in the reply are stripped (round 6, r5a-5).

## Wording kept on purpose

"MONOLOGUE ... nobody hears it": Opus refuses prompts that ask for private reasoning or thoughts; this wording passes.
