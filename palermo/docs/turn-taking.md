# Who talks next (design, 2026-10-23)

## The problem
"If I say Sol is sus, Haiku can ask why, but Sol has to talk." Before today the engine let a named player answer
with probability 0.85 and otherwise handed the floor to a random seat, who often opened an unrelated topic; the
accused could go unanswered for a whole day.

## What the prior work says (research/llm-agents-prior-work.md, research/turn-taking.md)
- Werewolf Arena: every living player bids 0–4 each line (4 = "I was addressed and must respond"); the paper
  never ablated it; 40% of bids of 4 come from players who were just named, i.e. the bids mostly re-encode
  "I was named", which code can infer for free. Cost: one extra model call per player per line (unaffordable
  for us at 4–7 s per CLI call).
- Google Game Arena dropped bidding for a rotating round-robin and sequential visible votes.
- Human chat Mafia (Ibraheem 2022, Kao 2026): ~72 utterances per game, ~6 words each; day-1 talk is thin
  and reactive; accusations are answered or pressed ("answer the question" culture).

## The rule now in the engine (`discussion()`)
1. **Owed replies.** Every line is scanned for names (`mentions()`); each named player (other than the speaker)
   is appended to an `owed` queue with who named them and the line. The next slot goes to the head of the
   queue; two owed players answer in the same beat (parallel calls, keeps the pace). Taking a slot settles the
   debt whether they answer or not.
2. **The accused may decline, visibly.** A PASS by an owed player becomes a transcript line
   "Sol: (declines to answer Terra)" that every agent sees, a `pass` event with `declines`, and the viewer
   shows "declines to answer Terra". The table can use it ("Sol dodged").
3. **One interjection, then the reply.** With probability 0.3 (never when fewer than 4 are alive) a third
   player gets one line about that exchange ("back one of them, add a fact, or ask one of them"); the owed
   reply always follows immediately.
4. **Everyone speaks once, no two-seat monologue.** When the remaining budget is down to the number of silent
   players plus one, silent players take priority. When the owed player has already spoken twice today and
   someone has not spoken at all, the silent player gets the slot first (60%). Otherwise a silent player gets
   the floor half of the time when nobody is owed. (Added after tt1, where one thread took 8 of 12 lines and
   the officer spoke once, at the end.)
5. **Floor-takers continue the thread.** When nobody is owed, a weighted-random seat (longest silent
   favoured) is shown the last two lines as "the thread" and told to continue it or open a new one with a
   name and the one thing that player did.
6. **Unchanged:** an officer who may claim speaks first; the last line before the vote must name a vote (and
   answer whoever named them, in the same breath).
7. **Randomness** enters in three places only: the interjection coin, the silent-player coin, and the weighted
   floor pick. Everything else is deterministic from the transcript, so a viewer can follow why someone talks.

Cost: zero extra model calls. Unit check in `tests.py`: in a dry day, every named player speaks or declines
within four events.

## Variants considered and not chosen
- Bidding per line (Werewolf Arena): +5 calls per line. Rejected on cost; the signal is mostly "I was named".
- Round-robin (Game Arena): fair but disconnected; the accused may answer three lines later.
- Moderator model choosing the speaker: +1 call per line and a new source of bias.
- A `NEXT:` field in each reply (the speaker nominates who should answer): cheap and natural; worth adding
  if the research shows real tables work that way. The named-player rule already covers the common case.

## First live result (tt1, budget 12)
10 of 13 lines were direct answers to the player who named the speaker, nobody passed, zero guard fires, 14
words per line. Side effect: one thread monopolised the day (fixed, rule 4). Each `say` event now carries
`slot` (the selection reason: answers / interjects / hasn't spoken yet / takes the floor / has something to
say) separately from the display tag, so the mix is measurable per game.

## Second live result (tt2, budget 12, after rule 4)
Every seat spoke (3/3/3/1/1/1 lines). Selection reasons: 8 answers, 2 interjections, 1 floor-take, 1
silent-player slot. The officer opened on the shown killer with an ordinary reason and the town voted the
shown killer out after a runoff. Median gap between events 2.7 s (Gemma 26B seat, scripted narrator).

## How to see it in a game
`review.py` prints "A -> B (answers B)", "(interjects)", "(hasn't spoken yet)", "(takes the floor)",
and "(declines to answer X)". In the viewer the dialogue tag says the same.

## What the data says about the talk itself (2026-10-23, after tt2)
Classifying our day lines by regex: meta-talk about who pushed, asked or answered whom is 30–91% of lines
(75–91% in the owed-reply rounds), agreement 0–16%, jokes 0–25%; questions 33–62%. The first player to name
someone on day 1 was voted out that day in 5 of 7 rounds. Recorded human games (Lai et al. 2022):
interrogation 16%, accusation 14%, defence 13%; the other ~57% is information, agreement, reasoning and
jokes; ~6 words per turn, 50–70 turns per game. Our prompts demand "name a player and the one thing they
did" on every turn, so on day 1, when nobody has done anything but talk, the only available content is
meta, and the first pusher is the only target. The turn-taking rule made the replies connected; it did not
make them natural, because the moves were never free.

Change under test: `--natural` — the talk rule lists the real moves (answer, agree/disagree, one question
to one person, gut read, fact, defend someone, one joke, "nothing yet", vote), lines under 12 words
(trim 16), 26 lines per day instead of 15, two seats may react at once when nobody is owed, and task texts
say "react, one short line" instead of prescribing an interrogation. A/B on the same seeds against the
current prompts: meta%, agreement, questions, words per line, reply latency, who gets lynched.

## Refinements taken from research/turn-taking.md (2026-10-23)
The named player answers alone (two at once never saw each other's reply); an interjection only breaks an
A→B→A ping-pong; the queue keeps two waiting replies; a silent player who is also owed gets the answer
prompt (was the "name a suspect" prompt, a bug); a fixed pre-vote block: the most-accused player defends,
then one weighted-random player names a vote (Ultimate Werewolf / Stanford Mafia structure). Rejected:
bidding (N−1 calls per line), an LLM moderator (latency, no measured gain), speak-or-wait polling.

## What real tables sound like (research/table-talk-samples.md, counted from four corpora)
Median spoken line 5 words, accusations and defences 8–9 words; one in five lines is a question; only 8–13% of
spoken lines name a player (addressing is done by looking at someone); the accused speaks within two turns
(next speaker ~30%, one other person speaks first otherwise), threads end after a median of one related line;
nobody speaks twice in a row; day 1 is greeting, joke, vote, with ~40% of lines carrying no game content;
reasons are thin ("gut", "too quiet", "too quick") and accepted; deflection has five shapes (refuse,
condition, joke, reverse, exasperation) and is a line, not silence; vote announcements are 3–5 words with the
reason after the name; defending someone pairs you with them; endgame is parity math and resignation.
The owed-reply + one-interjection design matches the measured reply timing. What does not match is the talk
itself: ours is 3× longer, twice as question-heavy, names people on almost every line, carries no colour, and
runs long threads. The `--natural` prompt set is being tuned to these numbers, with the research's example
lines as style examples.

## Thread fatigue (added after n2-34)
Real tables drop a thread after a median of one related line; our owed rule fed a 15-line pile-on on one
deflecting player. Now a player owed three times in a row stops being owed: the next speaker is a weighted
pick told "the table has heard enough about that, new topic". Together with the dominance cap (a seat at 35%+
of the day's lines yields half the time) this keeps any one player under about a third of the talk.

## Nobody falls behind (round 6, 2026-11-15)
The floor goes mostly to whoever was just named, so a seat nobody names gets few turns: Terra had 5 day lines in
r5a-2 (named twice all game) and in r5a-7 (named never), against 8 to 12 for the others, with no passes and no line
dropped by a guard (two own-name retries in all of r5a). Over the eight games her share was normal (68 lines; others
65 to 79). Now a living seat that has spoken today and is two or more lines below the day's average per seat gets the
floor half of the time (after the silent-player rule, before owed replies). In 60 dry days the days with a seat three
or more lines below the average went from 4 to 0.

Round 8 (2026-11-15): r7a-7's officer Haiku had 2 lines on day 1 while Terra had 6. A seat now also counts as behind
when it has under half the busiest seat's lines, and a seat behind gets the floor every time (the least-heard first),
unless the player named in the last line is owed the answer; then half the time. Measured on 300 dry day 1s: the
quietest seat ended under half the busiest on 6% of days (28% with the round-6 rule); a seat two or more below the
average on 1 day (52 before). The vote-when-ready gate is unchanged.

