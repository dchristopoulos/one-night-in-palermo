# How people actually talk at a social-deduction table

Research note, 2026-10-23. Companion to `how-games-go.md` (which covers structure and
strategy). This one is about **utterances**: what gets said, in what order, how long, how
fast, and what a reply to an accusation looks like. Goal: tune the AI table
(`players/*.md`, `game.py` `discussion()`) so it sounds like people.

Method: four public corpora were downloaded and counted locally (four small counting
scripts, one per corpus, not kept in this repository), one forum
thread was pulled as Discourse JSON, and one Greek YouTube game was read through its
auto-caption transcript panel. Every quoted line is under 15 words and attributed; longer
lines are paraphrased and marked *(paraphrase)*. Numbers marked "my count" come from the
scripts, not from the papers.

## 0. Evidence gaps, up front

- **Greek Palermo**: exactly one usable recording was found (S5, a comedy-family YouTube
  episode, 8 players, Greek auto-captions, no speaker labels, ASR errors, played for camera).
  A second Greek play video (S6) has no caption track at all. No Greek written transcript,
  forum game, or write-up with actual lines exists as far as search can tell; Greek pages are
  rules and listicles. Treat the Greek lines below as one anecdote, not a sample.
- **In-person Mafia/Werewolf with elimination**: no transcript corpus exists. The spoken
  corpora are One Night Ultimate Werewolf (no elimination, one 5–7 minute day) and Avalon
  (quests, no night kills). The chat corpora (S1, S3) are text, not speech.
- **Interruptions/overlap** are only visible through proxies (lines ending in `-`, two
  speakers with the same timestamp). No source marks overlaps explicitly.
- **Blocked**: MafiaScum forum and wiki (Cloudflare), Bay12 forums (bot check), the original
  Werewolf-Among-Us site (bot check; the HuggingFace mirror works). **Not found**: any
  Dropout/TableTop/Geek & Sundry Werewolf transcript, any Town of Salem chat dataset. The
  Among Us "sandbox" (arXiv 2504.04072) is LLM-only. The 700-game MafiaScum corpus
  (arXiv 1811.07851, Bitbucket) was not pulled; the forum register is covered by S4.

## 1. Sources

| # | URL | What it is | Dialogue it contains | Trust |
|---|-----|------------|----------------------|-------|
| S1 | https://github.com/sstepput/Avalon-NLU (dataset/*.json) | Stepputtis et al., EMNLP Findings 2023. 20 online Avalon games, 6 players each, text chat, every message labelled with a persuasion strategy and (if a lie) a deception strategy, ground-truth roles. | 2,384 player messages (my count), full games. | High, primary |
| S2 | https://huggingface.co/datasets/bolinlai/Werewolf-Among-Us | Lai et al., ACL Findings 2023 "Werewolf Among Us". Speech transcripts with speaker, timestamp and persuasion labels. YouTube ONUW: 151 games (train split used: 105 games, 12,746 utterances). Ego4D in-person ONUW: train 28 games, 3,746 utts. Ego4D in-person Avalon: 8 games, 2,841 utts. | ~19,300 utterances used, full games. | High, primary (transcription-service text, corrected by annotators) |
| S3 | https://github.com/omonida/mafia-dataset (mafia_dataset.zip) | Ibraheem, Zhou, DeNero, NAACL 2022 "Putting the Con in Context". 44 MTurk chat-room Mafia games, 4–10 players, 1–2 mafia, timestamps, roles, votes. | 1,825 daytime text lines + votes (my count; paper counts 2,162 incl. night mafia chat). | High, primary |
| S4 | https://boards.straightdope.com/t/mafia-evil-dead-day-night-one/477854 (read as `/t/477854.json?page=N`) | Forum Mafia, 27 players, the whole Day One thread, Dec 2008. | 304 player posts, 317 total. | High, primary; forum register (essays, not table talk) |
| S5 | https://www.youtube.com/watch?v=U1VaRu5EoOk | "ΜΟΥ ΤΗΝ ΠΕΦΤΕΙ ΝΥΧΤΑ ΣΤΟ ΠΑΛΕΡΜΟ #1", Kritikos Family, Jan 2025, 35:26. 8 players: 4 citizens, officer, open killer, hidden killer, snitch (χαφιές), plus one-shot property cards. Three days, three votes. Greek auto-captions read via the transcript panel. | ~3,500 ASR words, no speaker labels, edited for TV. | Medium (ASR, performers, cut) |
| S6 | https://www.youtube.com/watch?v=FeST2pFP_e8 | "H νύχτα πέφτει στο Παλέρμο - Bar Games Andante edition", 47 min. | No caption track; not read. | n/a |
| S7 | https://arxiv.org/abs/2212.08279 | The S2 paper (label definitions, utterance lengths per label). | Nine example lines. | High |
| S8 | https://arxiv.org/abs/2207.02253 | The S3 paper (mafia strategies, hand-coded feature table). | Six example lines. | High |
| S9 | https://arxiv.org/abs/2601.13709 and https://github.com/cocochief4/llm-mafia | Kao et al. 2026: human baseline recomputed from S3: 72.5 utterances/game, 5.93 words/utterance, vs 268.6 and 110 for GPT-4o games. | Secondary stats only. | Medium-high |

## 2. Exchange excerpts

Speaker labels are as in the source. `(m)`/`(b)` in S3 = mafia/bystander (ground truth,
unknown to the table). In S5 real first names are replaced by [X]/[Y]; an English gloss follows
in italics.

### E1. Day-1 small talk turning into suspicion (S3, game dbecdd48, day 1, chat)

1. Amanda (b): "really"
2. Autumn (b): "Agreed. Amanda is mafia."
3. Amanda (b): "Im just talkative LOL"
4. Vanessa (b): "I assumed it was a male"
5. Jodi (b): "matthew is mafia"
6. Autumn (b): "Amanda, who should we vote out then?"
7. Amanda (b): "Trying too hard" … "I'll vote Matthew"
8. Matthew (m): "im gonna make you an offer you cant refuse"

The first accusation lands 30 seconds after "hello"; the reason is "talkative". Same corpus,
game f0ac69d0, day 1 opens: "hello" / "hi" / two votes with no words / Jason (m): "Im too nice
to be mafia" / Robert (m): "One name is as good as another at this point, I guess".

### E2. Accusation and the accused's reply (S2 YouTube ONUW, "Retro 1" Game 5, 04:25)

1. Caitlynn: "Justin is the werewolf." `Accusation`
2. Mike: "So Justin is still saying he was a seer." `Accusation`
3. Justin: "At the beginning I was." `Defense`
4. Mike: "So then... I definitely switched these two." `Evidence`
5. Dan: "What is the order of everything?"

Two lines of accusation, a five-word reply that concedes a detail, and the thread moves on.

### E3. A question answered, then pushed (S2 YouTube ONUW, "Retro 1" Game 4, 01:21–01:45)

1. James: "I'm willing to bet you're a villager."
2. Mitchell: "Why? What are you going off of?"
3. James: "Gut."
4. Mitchell: "So, that is just pure gut."
5. James: "Yeah." … "Prove me wrong Mitchell."
6. Mitchell: "I have no information because I was a villager."

Then the claim chain starts at once: Alvin "I was a villager...." / Mitchell: "Mitchell's
lying." *(about himself, joking)* / Alvin: "You were a villager when you started?"

### E4. Pile-on (S2 YouTube ONUW, game 6, 01:30; and S2 Ego4D in-person Game 9, 03:29)

1. Mitchell: "I'm not, I'm not a werewolf." `Defense`
2. Caitlynn: "It's always Mitchell." `Accusation`
3. Mike: "It's always Mitchell." `Accusation`
4. Mitchell: "I am almost always a werewolf."
5. Caitlynn: "Hashtag kill Mitchell." / Mike: "Hashtag kill Mitchell."

In-person version:

1. Elliot: "I'm actually a Villager. Chris is lying I think, or Sue's lying."
2. Sian: "I think it could be James or Sukeshi."
3. James: "Sukeshi's not lying." `Defense`
4. Sukeshi: "I'm not lying, I was the villager." `Identity Declaration/Defense`
5. Sian: "Says the two Werewolves." `Accusation`

A defence of someone else is immediately read as "you two are together".

### E5. Deflection / refusal to answer (S2 Ego4D in-person ONUW, Game 6, 01:51)

1. Sukeshi: "Stop trying to be confusing to draw attention" `Call for Action`
2. James: "Elliot's first claim was to be the Insomniac." `Accusation`
3. Elliot: "No, I said I'm the Doppelganger and I saw the Insomniac."
4. Chris: "No one is claiming to be the Insomniac." `Evidence`
5. Elliot: "Why do I have to tell you who it was?" `Interrogation/Defense`

Conditional refusal, same corpus (YouTube Retro 1 Game 4, 04:08): Alvin: "Do you want to say
who you swapped with?" / Mitchell: "I want to know first if there was a troublemaker." /
Alvin: "Well, I was a villager." / Mitchell: "I was a villager." / James: "I was a villager."

Greek version (S5, 30:17, third vote): narrator asks who [X] votes; [X]: "τον [Y]"; someone:
"γιατί;"; [X]: "θα με τρελάνεις, πρέπει να το εξηγήσω κιόλας;" *(you'll drive me mad, do I have
to explain it too?)*.

### E6. Role claim and the reaction (S5 Greek, 7:41–8:40, day 1)

1. Father of the accused: "τον έχω γεννήσει, δυστυχώς ρε φίλε" *(I gave birth to him,
   sadly)*; he has been naming his son for minutes.
2. Another: "ή έχεις κάποιον άλλο λόγο που μας το λες;" *(or do you have another reason
   for telling us?)* … "μίλα ξεκάθαρα" *(speak plainly)*.
3. Father: "είμαι ο χαφιές και για ξεκάρφωμα δίνω τον [X]" *(I'm the snitch, and to throw you
   off I'm giving you [X])*. He is in fact a citizen.
4. Someone: "εγώ τον πιστεύω" *(I believe him)*.
5. Another: "είναι ο χαφιές διότι είπε 'είμαι ο χαφιές'" *(he's the snitch because he said
   "I'm the snitch")*.
6. The actual killer, to him: "περίμενε λίγο ... δίνεις σε μένα που είμαι δολοφόνος;" *(hold on,
   you're giving me, the killer?)* (said as a joke; nobody takes it as a confession).
7. Later: "he has a point" / "ναι αλλά θα μπορούσε να το πει και ο δολοφόνος αυτό" *(yes, but
   a killer could say that too)*.

Chat version (S3, game 1603d677, day 1): Alicia: "Bystander here" / Chad: "i am a bystander
too." / Gabriel: "Bystander too." / Alicia: "Wow isn't that convenient" / Stephen: "Right."

ONUW version (S2 YouTube, game 43 Game 4, 01:08): Mitchell: "Mike, I robbed from you and I know
your role." / Justin *(paraphrase: claims troublemaker, says he switched those two)* / Paul:
"I'm the troublemaker. I switched the cards." / Mitchell: "He was so stupid." / Mike: "Mitch, do
you want to say what the actual truth was if you were the robber?" *(paraphrase: asks Mitch for
the real story)*.

### E7. Vote announcements (three registers)

Spoken, timer running out (S2 YouTube ONUW, game 28 Game 3, 06:35):

1. Mitchell: "Who are we voting with 10 seconds left? Is it Mike?"
2. Mike: "It's Paul or it's Justin."
3. Mitchell: "I'm voting Mike."
4. Alysha: "I'm voting Justin."
5. Paul *(paraphrase: says he is actually the Tanner and everyone should vote left)*.

Chat (S3, game 33e35e0b, day 1, within 25 seconds): Jason: "Hi!" / "lol" / "I vote for JOhn" /
Gregory casts vote John / Jason casts vote John. Day 2 of the same game: Gregory: "thats sus" /
Jean: "well we have to make a decision." / Gregory: "^" / Jason casts vote / Gregory: "no".

Forum (S4, posts #3–#7): JSexton: "Gonna start with not-random vote: Pleonast." /
Hockey_Monkey: "Any explaination for the not-randomness?" … "If it's not random what are
you basing it on?" / macey *(paraphrase: where is the reasoning for voting Pleonast, if it's not
random?)*. Later, #165, Hawkeyeop: "Naf, can you explain why you are voting Chucara over Macey."

Greek (S5, 12:26, first vote): narrator: "εγώ ψηφίζω τον [X]. Εσύ τι ψηφίζεις;" / "[Y]" /
"ποιος είναι [Y]; δεν υπάρχει [Y] εδώ" *(who is [Y]? there's no [Y] here)* (wrong surname,
laughter, vote stands).

### E8. Endgame argument (S2 Ego4D in-person Avalon, Game 7, 04:47)

1. Alex: "Alvin's really thought about this." `Accusation`
2. Shiyu: "Yeah, it still sounds like Alvin's trying to throw-" `Accusation`
3. Alex: "I don't know. All I know is-"
4. Alvin: "You've gotten really quiet too." `Accusation`
5. Davis: "I know." `Defense`
6. Alex: "Real quiet over there."

Chat Avalon (S1, game DdwRb1, last lines): player-6 [Percival]: "over" / player-1 [Merlin]
*(paraphrase: glad everyone finally agrees player-2 is bad, I've said so since round one)* /
player-2 [Assassin]: "it seems that the hate with passion has turned towards me right now" /
"although i'm good, i will approve whatever party you suggest to gain credit". Other S1
endgames: "i no longer have the will to live." (game 1aKReQ, Servant), "let's just vote and
everything will be sunshine and rainbows" (game 6dBXa7, Servant).

Greek (S5, 23:20–23:50, second vote): "ο μόνος τρόπος να κερδίσουμε είναι να ψηφίσουμε όλοι
τον [X]" *(the only way we win is all voting [X])* / "αν είναι δολοφόνος και πεθάνει τώρα,
θεωρητικά κερδίζουμε" *(if he's the killer and dies now we theoretically win)* / "μπορεί να
'σαι κι εσύ δολοφόνος ρε" *(you could be a killer too)*.

### E9. Accused reverses it (S3, game de2ac94e, day 1; and game c21a71b0, day 1)

1. Ryan (b): "I have no rationale just speeding things up"
2. Andrew (b): "Cathy is Mafia I think"
3. Clayton (b): "agree how are we supposed to play this game over a chat box haha"
4. Cathy (b): "Lets eliminate Ryan"
5. Regina (b): "whats the prize if we win?"
6. Ryan (b): "Don't you turn this on me"

Second game: Danielle (m): "Jill Mcdonald AFTER CORY" / Cory (b): "I think you all should worry
about Ashley. Why would she single me out?" / Jill (b) *(paraphrase: fine, eliminate me so I get
paid and leave you losers)* / Nicholas (b): "There doesn't seem to be any evidence for it." /
Ashley (b): "I go with my gut instinct" / Nicholas (b): "LOL I hope your doctor doesn't do the
same".

### E10. Officer claim, counter-claim invited (S5 Greek, 15:48 and 18:49)

1. [X] to [Y]: "εσύ είσαι ο χαφιές; εγώ είμαι αστυνομικός" *(you're the snitch? I'm the
   officer)*.
2. Day 2, [X]: "δεν είμαι πολίτης, δεν είμαι δολοφόνος, είμαι από την αρχή αστυνομικός"
   *(not a citizen, not a killer, officer from the start)*.
3. [X]: "έχει κάποιος άλλος να πει 'λέει ψέματα, δεν είναι αστυνομικός';" *(does anyone
   else want to say "he's lying, he's not the officer"?)*. Nobody counter-claims.
4. [Z], pressed for a reason to vote someone: "πες ένα επιχείρημα" *(give one argument)* is
   answered with "η φάτσα σου" *(your face)*; reply: "η φάτσα μου είναι πάντα ίδια" *(my face
   is always the same)*.

### E11. Silent player pulled in; round-robin opening (S5 Greek, 4:00 and 6:21)

Day 1 opens with the narrator going round: "[name], εσύ ποιος πιστεύεις ότι είναι ο
δολοφόνος;" *(who do you think the killer is?)*. Each answer is one name plus one clause:
"θα πω [X], έχει μπει πολύ επιθετικά" *([X], he came in very aggressive)*; "ο [Y] δεν είναι
ήρεμος" *([Y] isn't calm)*; "οι τρεις τους μου βγάζουνε μία περίεργη συμπεριφορά" *(those three
give off odd behaviour)*; one names a brother "μπας και βάλω ψήφους εκεί" *(to pile votes there)*
because he wants him to lose. Then: "[X], είχες κάτι να πεις και δεν έχεις μιλήσει τόση ώρα"
*([X], you had something to say and you haven't spoken all this time)* → "θεωρώ ότι είναι
δολοφόνος, θέλω απλά να με πιστέψουν οι υπόλοιποι" *(I think he's the killer, I just want the
rest to believe me)*.

### E12. Forum pressure and the ask for elaboration (S4, posts #78–#79, #153–#156)

1. Hawkeyeop (#78, 56 words) *(paraphrase: no, power-role fake-claims hurt scum more than town;
   votes pedescribe for the slip and the attempts to explain it)*.
2. bufftabby (#79): "Would you mind elaborating?"
3. Thing_Fish (#80, 406 words) *(paraphrase: too quiet in here, lots of lurkers at the halfway
   mark of Day One)*.

Forum replies arrive hours later and run to hundreds of words; the register is wrong for a
table but the moves (vote, "why?", "lurkers") are the same.

## 3. Quantitative table

All "my count" from the scripts over the files above. Accusation = a line labelled Accusation
(S2), critique/opposition with a suspicion word (S1), or a line naming another player with a
vote/suspicion word (S3, S4). "Accused replies" = the named player is the next speaker.

| Metric | ONUW on YouTube (S2) | ONUW in person (S2 Ego4D) | Avalon in person (S2 Ego4D) | Mafia chat (S3) | Avalon chat (S1) | Forum Mafia (S4) |
|---|---|---|---|---|---|---|
| Games / units | 105 games | 28 games | 8 games | 44 games, 128 days | 20 games | 1 day thread |
| Players speaking | 4 (median) | 4–5 | 5 | 6 per day (median) | 6 | 27 |
| Utterances per game | 118 (median) | 135 | 379 | 13 per day, 2.9 days/game; 72.5/game per S9 | 119 (35–302) | 304 posts |
| Minutes of talk | 6.0 per game | 2.7 per clip | 6.2 per clip | 2.7 per day | n/a (async) | 207 hours |
| Utterances per minute | 21 (p25–p75 18–24) | 47 (43–83) | 51 | 6.2 | n/a | 1.5 per hour |
| Words per utterance, median (p25–p75; p90) | 5 (3–9; 15) | 5 (2–9; 15) | 4 (2–8; 14) | 3 (2–6; 10); 5.9 mean per S9 | 14 (9–22; 30) | 89 (42–162; 263) |
| Share of lines of 5 words or fewer | 52% | 56% | 61% | 67% | — | — |
| Words per line by label, median | accusation 9, defence 8, claim 8, no-strategy 4 | 8 / 7 / 8 / 3 | 9 / 7 / 7 / 3 | — | — | — |
| Share of lines containing "?" | 21% | 17% | 16% | 12% | 4% (but 11% labelled "questioning") | 45% |
| Share naming another player | 13% | 8% | 7% | 26% | 50% | 70% |
| Accusations with a named target | 568 | 141 | 95 | 130 | 158 | 340 |
| Accused is the very next speaker | 34% | 30% | 27% | 21% | 4% | 6% |
| Turns until accused speaks, median (p75) | 2 (4) | 2 (5) | 3 (6) | 2 (3) | 9 (13) | 8 (18) |
| Accused never speaks again in window | 11% (20 lines) | 7% | 15% | 41% (same day) | 20% | 39% (39 posts) |
| Thread length after a named accusation: related lines before topic changes, median (p75) | 1 (3); 32% zero | — | — | 0 (0); 79% zero | — | — |
| Same speaker twice in a row | 2% of turns | 3% | 1% | — | 65% of runs are 2+ messages (people split one thought) | — |
| Lines cut off (end in "-" or "...") | 8% | 9% | 11% | — | — | — |
| Two speakers on the same second (overlap proxy) | 17% | 19% | 29% | — | — | — |
| Top speaker's share of lines | 31% (p75 35%) | — | — | 44% per day (p75 60%) | — | 10% |
| Label mix (share of lines) | no strategy 42, interrogation 18, accusation 15, defence 14, evidence 9, call to action 6, identity claim 6 | 53 / 13 / 14 / 11 / 9 / 5 / 6 | 56 / 11 / 15 / 9 / 8 / 7 / 1 | — | assertion 27, deduction 14, suggestion 13, critique 11, questioning 11, agreement 10, defence 10, concession 5; 18% of lines are labelled lies | — |

Notes on reading it:

- The YouTube games are mostly one recurring friend group (Justin, Mitchell, Paul, James,
  Mike), so the profanity and in-jokes are theirs, not the game's.
- S3 "never replies" is high partly because many MTurk players said nothing all game (349 of
  421 spoke at all, per S8).
- Avalon chat (S1) is the one text corpus with long lines (median 14 words): players have time,
  no timer, and six quests of state to reason about. Day-phase Mafia chat (S3) is the closest
  text analogue to a quick table: median 3 words, 13 lines per day, 6 speakers.

## 4. What natural sounds like: rules for the AI table

Each rule is testable on a transcript. Evidence in brackets.

1. **Median line 5–8 words; one in two spoken lines is 5 words or fewer; 90th percentile
   15.** Keep the current 30-word persona cap, but most lines should be far under it, and
   one-to-three-word lines ("Gut.", "What?", "Same.") must be allowed. [table, S2 all three
   splits; S3 median 3]
2. **Accusations and defences are the long lines, and they are still under 10 words**
   (median 8–9). A 25-word accusation is forum register. [S2 per-label medians; S4 vs S2]
3. **The accused speaks within two turns** (median 2 in every spoken corpus), is the very next
   speaker about a third of the time, and otherwise one other person says one thing first.
   The engine's "one interjection, then the owed reply" matches this; do not let the
   interjection become two. [table rows "next speaker" and "turns until accused speaks"]
4. **A reply to an accusation is a denial, a counter-question, or a conceded detail, in under
   10 words**: "At the beginning I was.", "Why? What are you going off of?", "Because why?",
   "I'm not lying, I was the villager.", "No, I saw a werewolf.", "Don't you turn this on
   me". Never a paragraph. [E2, E3, E4, E9; S2 Defense median 8 words]
5. **Threads are short.** After a named accusation the median number of related lines before
   the table moves on is 1 (p75 3); in chat Mafia the topic changes immediately 79% of the
   time. A 6–8 line thread on one player is rare and should feel like a pile-on, not the norm.
   [thread-length rows]
6. **About one line in five is a question, and the question is short and concrete**: "Who did
   you switch?", "What were you?", "Who did you rob?", "Would you mind elaborating?", "γιατί;".
   [21%/17% "?" in S2; S7 examples; E12]
7. **Reasons are thin and that is fine**: "gut", "your face", "too talkative", "too quick to
   vote", "too quiet", "he came in aggressive", "I know him". Players ask for reasons ("πες ένα
   επιχείρημα", "what are you going off of?") and accept weak ones. [E3, E10, E11, E1; S8
   Table 4: mafia refer to others 2× as often as bystanders]
8. **"Too quiet" and "too quick" are the default accusations**, in every register: "You've
   gotten really quiet too", "was pretty quick to cast her vote, seems suspicious", "Still too
   damn quiet in here", "δεν έχεις μιλήσει τόση ώρα". The AI should both use and expect them.
   [E8, S3 game 1c69552e, S4 #80, E11]
9. **Nobody speaks twice in a row at a table** (98% of turns change speaker). Multi-message
   bursts belong to chat, where people split one thought into 2–4 short messages. One line
   per turn, then yield. [same-speaker rows]
10. **Role claims come in clusters and get tested at once.** One claim triggers the next
    ("I was a villager." ×3; "Bystander here" / "too" / "too"), and the reaction is either
    "convenient" or a direct test ("Say you're a villager one more time", "did you switch me
    and Mike?"). Claims are about 6% of lines and 8 words. [E3, E6; S2 Identity Declaration
    share and length; Ego4D Game 6: "Say you're a villager one more time."]
11. **A claim invites a counter-claim explicitly, and silence confirms it.** "έχει κάποιος
    άλλος να πει 'λέει ψέματα';" (nobody does, the claim is accepted). The engine's
    officer-first-speaks rule should include a beat where the table can counter. [E10]
12. **Vote announcements are three to five words and chain**: "I'm voting Mike." / "I'm voting
    Justin."; "I'll vote Matthew"; "ψηφίζω τον [X]"; forum: "Gonna start with not-random vote:
    Pleonast." The next speaker often copies the vote verbatim. A reason is optional and comes
    after the name, not before. [E7]
13. **Day 1 is greeting, joke, vote.** In chat Mafia the first votes land 20–60 seconds after
    "hello" with no reason or a joke reason; in person the first minute is banter. About 40%
    of spoken lines carry no game content at all. Let a third of day-1 lines be colour. [E1;
    S2 "No Strategy" 42–56%; S3 openings]
14. **Deflection has five shapes**: refuse ("Why do I have to tell you who it was?"),
    condition ("I want to know first if there was a troublemaker"), joke ("Im just talkative
    LOL"), reverse ("Why would she single me out?"), exasperation ("πρέπει να το εξηγήσω
    κιόλας;"). The engine's visible "(declines to answer)" should be rendered as one of these,
    not as silence. [E5, E9, E1]
15. **Defending someone gets you paired with them** ("Says the two Werewolves."; "you two are
    in cahoots"). Expect the table to punish defences, and let killers use it. [E4; S1 game
    penRe7: "it seems like they are in cahoots"]
16. **Endgame shrinks to parity math and resignation**, not long cases: "if he's the killer and
    dies now we win", "We're all voting James.", "let's just vote", "i no longer have the will to
    live". [E8]
17. **Overlap and half-lines are normal in speech**: 8–11% of lines are cut off, 17–29% share a
    second with another speaker. One unfinished line per day ("All I know is-") reads as human.
    [cut-off and overlap rows]
18. **One voice dominates but under a third of lines** (31% median on YouTube; 44% per day in
    chat, where some players say nothing). The engine's "everyone speaks once" rule is
    consistent with speech, not with chat. [top-speaker row]

## 5. Example lines in the six-seat voice

Written for this note, not copied; plain words, under 15 words, placeholders for names.

**Deny**
- "Not me. I was quiet because I had nothing."
- "No. Say what I actually did."
- "That's a gut call, not a reason."

**Counter-question**
- "Why me? What am I supposed to have done?"
- "Who did you check, then?"
- "You voted first. What was that about?"

**Pile-on**
- "Same. [name] has dodged this twice."
- "Yeah, that's a tell. I'm with [name]."

**Defend someone**
- "Leave [name] alone, that vote was random, like everyone's."
- "[name] has given names every round. That's not a killer."

**Vote announcement**
- "I'm voting [name]. Too quick on day one."
- "[name]. Final answer."
- "Fine, [name], until someone gives me better."

**Decline to answer**
- "Not telling you who I checked. Not yet."
- "I'll answer after you say who you are."
- "Do I really have to explain that again?"

**Claim**
- "I'm the officer. I checked [name]: clean."
- "Plain citizen. That's all I've got."

**Counter-claim**
- "That's a lie. I'm the officer, and I checked you."
- "Two officers? One of you is a killer. Vote the second claim."

## 6. Where the evidence is thin

- Greek: one episode, ASR, no speaker labels, a TV-style cut. The round-robin opening, the
  "you haven't spoken" pull-in, the one-word "γιατί;" pushes and the three-word votes are
  consistent with the English corpora, which is the only reason they are given weight.
- Elimination-style Mafia in person: no spoken corpus. The "accused replies within two turns"
  figure is from ONUW and Avalon tables; the chat Mafia figure (also 2) is the cross-check.
- Thread length and overlap are heuristics (named-player chains; same-second timestamps),
  not annotations.
- The YouTube ONUW set is one friend group; the Ego4D sets are lab recruits playing for a study.
  Neither is a Greek παρέα, but both are people who know each other, as our six seats should be.
