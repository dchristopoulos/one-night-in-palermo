# Who talks next: turn-taking in social-deduction games, at tables and in code

Research notes, 2026-10-23. Read-only survey; no code changed. Question: how do real tables and AI implementations decide who speaks next in Palermo / Mafia / Werewolf / Resistance-type games, and what makes the talk *connected* (an accusation gets a defence, a question gets an answer)? Every claim carries a source id from the table in section 1; where a page could not be read and only a search snippet was available, the row says so. Quotes are short and attributed. Evidence is explicitly thin in three places (marked **thin**): sequence-level statistics on "accusation → answer" in human games, Greek Palermo day procedure, and forum-Mafia conventions (MafiaScum wiki is behind a bot check).

Engine under comparison: `palermo/game.py`, `discussion()` at lines 674–780 (`MAX_BUDGET = 15`, line 41). What the code does today (read, not the brief): budget = min(15, 3 × alive); an officer holding a killer result goes first; every line's named players become "owed" a reply; an owed player answers with p = 0.7 (two owed players at once, in parallel), otherwise one weighted-random "interjects" line precedes the reply; silent players get the floor with p = 0.5 or when `left ≤ silent + 1`; otherwise a weighted-random "takes the floor" pick favouring the longest silent; a PASS is shown as "(declines to answer X)"; the last line is prompted to name a vote. Taking any slot clears the debt "answer or not" (line 763). The brief's 0.85 figure is not in the current code.

---

## 1. Sources

| id | URL | What it is | Read | Trust |
|---|---|---|---|---|
| T1 | https://en.wikipedia.org/wiki/Turn-taking | Summary of Sacks, Schegloff & Jefferson 1974, *Language* 50(4):696–735, the turn-allocation rules | full | High for the rules (secondary); emcawiki.net was 403 |
| T2 | https://eblong.com/zarf/werewolf.html | Plotkin's original Werewolf rules and play notes | full | High (primary) |
| T3 | https://rulespal.com/ultimate-werewolf/rulebook | Ultimate Werewolf (Bezier) rulebook transcription | full | Medium-high |
| T4 | https://stanford.learningu.org/download/fb72d841-448e-4bf1-a370-225e2cfd41a9/H4869_Rules.pdf | Stanford Splash Mafia rules (2016): timed days, top-2/3 defence statements | full (PDF text extracted) | Medium (one club's rules, explicit) |
| T5 | https://ru.wikipedia.org/wiki/Мафия_(игра) | Russian Wikipedia, section on «спортивная мафия» (tournament Mafia): numbered seats, 1-minute speeches, fouls | full | Medium-high (secondary, detailed) |
| T6 | https://mindsportsolympiad.com/wp-content/uploads/2025/07/How-to-Play-Mafia-16-May-2025.pdf | Mind Sports Olympiad Mafia rules 2025 | **snippet only** (Cloudflare) | Medium |
| T7 | https://mafia42.fandom.com/wiki/Mafia42_Wiki?oldid=168 ; https://www.dekudeals.com/items/unknown-faces | App rules: "Last Argument", "Explain Time" | **snippet only** | Low-medium |
| T8 | https://cardgamesgr.blogspot.com/2014/03/blog-post_3402.html | Greek classic «Πέφτει η νύχτα στο Παλέρμο» rules (S1 in `palermo-rules.md`) | full | High for the classic game |
| T9 | http://palermogame.blogspot.com/2014/04/blog-post.html | Greek house rules with explicit day procedure (S11 in `palermo-rules.md`) | full | Medium-low (one group) |
| T10 | `palermo/research/palermo-rules.md` §4 | Earlier internal survey of 27 Greek/English sources; day and vote notes (S9: voters justify as they vote; S21: 9 players, 3 days in 34 min) | full | Internal |
| T11 | https://rulespal.com/resistance-avalon/rulebook ; https://en.wikipedia.org/wiki/The_Resistance_(game) | Avalon rulebook; Resistance overview | full | Medium-high |
| T12 | https://sockmafia.readthedocs.io/en/latest/player/ | Forum-Mafia bot's player guide | full | Medium |
| T13 | https://dragonmount.com/forums/topic/76698-new-player-tips-and-information/ | Dragonmount forum-Mafia new-player tips (2012–13) | full | Medium |
| T14 | https://forum.mafiascum.net/viewtopic.php?f=50&t=61262 and other game threads found by search | MafiaScum moderators' prod/replacement rules | **snippet only** (403) | Medium (consistent across threads) |
| T15 | https://aclanthology.org/2022.naacl-main.11.pdf | Ibraheem, Zhou, DeNero, NAACL 2022, "Putting the Con in Context": 44 chat-room Mafia games | full (PDF text) | High (primary data) |
| T16 | https://arxiv.org/pdf/2601.13709 | Kao, Vats, Davis, "Hidden in Plain Text" (IEEE ICA 2025 / arXiv 2026): 35 GPT-4o games vs 28 human games from T15 | full (PDF text) | High (primary data) |
| T17 | https://publications.idiap.ch/attachments/papers/2010/Chittaranjan_ICASSP2010_2010.pdf | Chittaranjan & Hung, ICASSP 2010, "Are you a Werewolf?": audio turn features in 8 live games | full (PDF text) | High (primary data, small n) |
| T18 | https://arxiv.org/html/2212.08279 | Lai et al. 2022, "Werewolf Among Us": 26,647 utterances from 191 recorded ONUW games, persuasion-strategy labels | full | High (primary data) |
| T19 | https://arxiv.org/html/2405.19946 | Jin et al. 2024, "Learning to Discuss Strategically" (ONUW with LLMs): tactic counts incl. defence | first 100k chars | High for its own logs |
| T20 | https://arxiv.org/abs/2609.12446 | Yang et al. (EMNLP 2026), "Do LLMs Trust the Accuser or the Accusation?" | abstract | Medium (abstract only) |
| T21 | https://arxiv.org/html/2407.13943v1 ; https://github.com/google/werewolf_arena (`werewolf/game.py`, `prompts.py`, `config.py`) | Werewolf Arena paper and code (bidding) | paper full; code read | High (primary) |
| T22 | https://arxiv.org/html/2609.31473 | Game Arena paper (Kaggle / Google DeepMind), Werewolf appendix | full | High (primary); kaggle.com pages are JS-only and unreadable |
| T23 | https://arxiv.org/html/2309.04658v2 | Xu et al. 2023, "Exploring LLMs for Communication Games: Werewolf" | first 100k chars | High |
| T24 | https://www.aclweb.org/portal/content/international-aiwolf-competition-2026-and-aiwolfdial-2026-international-workshop ; https://aclweb.org/anthology/2023.inlg-genchal.13.pdf ; https://github.com/ehauckdo/AIWoof | AIWolf competition tracks (2026 CFP read in full; 2023 rules and Skip/Over tokens **snippet only**) | mixed | Medium-high |
| T25 | https://arxiv.org/html/2412.04937 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12209177 | Nonomura & Mori 2025, *Frontiers in AI* 8:1582287, "Who speaks next?" (murder-mystery agents, adjacency-pair next-speaker rule) | full | High (primary; authors self-evaluated) |
| T26 | https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/selector-group-chat.html | AutoGen 0.4 SelectorGroupChat docs | full | High (docs) |
| T27 | https://docs.ag2.ai/docs/api-reference/autogen/GroupChat | AG2 / AutoGen 0.2 `speaker_selection_method` | **search summary of docs** | High (docs) |
| T28 | https://raw.githubusercontent.com/Farama-Foundation/chatarena/main/README.md | ChatArena README (deprecated Aug 2025) | full | High (docs) |
| T29 | https://arxiv.org/abs/2303.17760 | CAMEL abstract | abstract | High for what it says |
| T30 | https://arxiv.org/html/2304.13835v3 | Wei et al. 2023, "Multi-Party Chat" (MultiLIGHT): next-speaker prediction numbers | full | High (primary) |
| T31 | https://arxiv.org/abs/2606.17542 | Fukuda et al. 2026, LLMs on addressee / next-speaker prediction (AMI) | abstract | Medium (no numbers on page) |
| T32 | https://arxiv.org/abs/2501.16643 | Inoue et al. 2025, addressee-recognition benchmark (triadic) | abstract | Medium |
| — | https://wiki.mafiascum.net/… (Lurking, Pressure) ; https://medium.com/@slava.me/the-mafia-game-2bbc21ce38f9 ; https://www.kaggle.com/blog/game-arena-werewolf ; https://doc.agentscope.io/zh_CN/tutorial/104-usecase.html | Wanted, **not readable** (403 / JS-only / 404) | — | — |

---

## 2. Real tables: rules and conventions

### 2.1 The general mechanism (conversation analysis)

Sacks, Schegloff & Jefferson (1974) describe ordinary conversation as an ordered set of rules applied at each point where a turn could end: (1) "The current speaker selects the next speaker and transfers the turn to them" (T1 wording); (2) if not, anyone may self-select, first starter wins; (3) if nobody does, the current speaker continues. The system is said to minimise gaps and overlap and is "not optimized for fairness or efficiency" (T1). Rule 1 is the one that produces connected talk: an addressed question or accusation hands the floor to its target. Everything below is a game-specific variant of these three rules, usually adding a timer and a vote.

### 2.2 Free-for-all with a vote (Plotkin, Greek Palermo, Resistance/Avalon)

- **Plotkin's Werewolf** (T2): "There are no restrictions on speech." The vote closes the instant a majority forms, so an accused player who wants to answer "has to do it before the vote goes through." Silence is itself a tell: "Not accusing anyone is also suspicious." The moderator does not run the discussion. A listed variant gives the lynched player "a short speech in defense of himself" (T2, Beer variant).
- **Greek Palermo** (T8, T9, T10 — **thin**: two rule pages and one earlier survey). No speaking order and no defence phase in the classic rules: «Αφού αρχίσετε όλοι να κατηγορείτε όλους στο τέλος του γύρου αρχίζει η ψηφοφορία» (T8). T9 starts the day «ξεκινώντας από όποιον αποφασιστεί», describes accusations countered by accusing the accuser of lying, votes cast in a circle («ψηφίζει κυκλικά…») with the accused holding up fingers for votes received, and a farewell speech *after* elimination in which the player may claim innocent or guilty without any duty to tell the truth. The earlier survey adds that voters justify their choice as they vote (T10, S9) and that no Greek source has a formal defence before the vote (T10 §4). On camera, a 9-player game runs three days and three votes in 34 edited minutes (T10, S21), i.e. a day is a few minutes of overlapping talk, not a sequence of speeches.
- **The Resistance / Avalon** (T11): no moderator, no order, no timer; the Leader assigns the team and calls the vote "after appropriate discussion"; players may make claims at any point. Connectedness comes from the agenda: every discussion is about one concrete proposal and the vote on it is public and simultaneous.

### 2.3 Nominate → second → defend → vote (Ultimate Werewolf, club Mafia)

- **Ultimate Werewolf** (T3): nomination by pointing and naming, a second is required, then the accused defends ("Bob may defend himself"), then a thumbs vote needing more than half. The first day may have a predetermined limit (the rulebook's example is 5 minutes), and the moderator warns when time is short. Introductions on day one go around the circle, one by one.
- **Stanford Splash Mafia** (T4): the day is timed (3 min first day, 4 then 5 min later); at the bell everyone points; "the 2-3 people with the most votes get a statement of defense"; then a revote among only those, needing 50 % + 1. If one player is far ahead, only they defend. The stated purpose is to "give complete control to the people on the chopping block" (T4). This is the cleanest table rule guaranteeing that the people the vote is about get the last word before it.
- Online apps (T7, snippets only): Mafia42's "Last Argument" gives the leading vote-getter a short solo slot in which only they can chat; Unknown Faces has an "Explain Time" for the accused followed by a repeat vote.

### 2.4 Numbered seats, one minute each, fouls (sport Mafia)

Tournament ("sport") Mafia replaces free talk with a strict rotation (T5, §«Стандартный день»): seats are numbered; player 1 speaks first on day 0 and the right of first speech moves up one seat each day; the minute passes to living players in order («право минутной речи передаётся живым игрокам»); a player may nominate others only during their own minute; the host then calls the vote in nomination order; a tie gives each tied player «30 секунд речи» and a revote; the eliminated player gets a last minute. Speaking outside your minute is a foul («речь не в свою минуту ведущим ставится замечание»): two are free, the third costs your next speech, the fourth removes you. Some non-tournament variants give nominees an «оправдательную минуту» (justification minute) before the vote (T5, §«Другие виды»). The Mind Sports Olympiad 2025 rules (T6, snippet) match: one-minute speeches with fist-on-table nominations, a public vote, and 30-second speeches on ties. Connectedness here is *positional*: you answer the accusation in your own minute, which may be several speakers later, and the nominee's defence is the 30-second tie speech or the justification minute.

### 2.5 Forum Mafia: everyone posts freely, lurkers are prodded

- Everyone may post at any time: "During the day, all players may converse openly." (T12). Votes are explicit commands and the tally is public (T12).
- Activity is enforced socially and by the moderator. Dragonmount's guide tells newcomers "Try and get around 3 solid posts per game day", calls posting the bare minimum "Active Lurking" (unethical), and advises "say what you have to say then go away for awhile" rather than answering everything (T13). MafiaScum game threads (T14, snippets) show the standard mechanics: a prod after 36–48 hours without a post, replacement after a further 24 hours or after three prods, and a bare "prod dodge" post does not reset the clock; the fix is a content post such as a vote with a reason.
- "Answer the question" culture: the earlier survey (T10's sibling `how-games-go.md`, S10/S29) records that lurking under pressure "never works out" and that a player who emerges from lurking only to join a wagon is extra suspect. The MafiaScum wiki pages on *Pressure* and *Lurking* could not be read (403), so this is **thin**; what is well attested is that an unanswered direct question is treated as evidence against the silent player.

### 2.6 What these have in common

1. A named player gets a reply slot — immediately (free-for-all, Plotkin's "before the vote goes through"), or structurally (nominate-second-defend; the sport-Mafia justification minute; the Stanford top-2/3 defence).
2. The pre-vote moment belongs to the accused, not to whoever happens to be next.
3. Silence is visible and costs something (Plotkin; forum prods; sport-Mafia fouls).
4. Rotation is used only to guarantee fairness (sport Mafia; UW introductions), never to carry argument.

---

## 3. Measured dynamics (numbers with sources)

**Human chat Mafia (T15).** 44 games, 421 players (87 mafia, 334 bystanders), 2,162 utterances; 9.57 players and 49.14 utterances per game on average (Table 1). 72 players never spoke, and 95.8 % of those were bystanders. Computed from Table 1: mafia are 20.7 % of players but produce 35.6 % of utterances (8.9 per mafioso vs 4.2 per bystander). The game ran with free chat in phases; votes were public. The paper reports no accusation→answer statistics.

**Humans vs GPT-4o in the same game (T16, Table I).** Human games (28 kept of 44): 72.5 utterances per game, 5.93 words per utterance, 3.11 days. GPT-4o games (35): 268.6 utterances, 110 words each, 3.17 days. The authors' reading: "humans are generally less talkative than the LLM player agents". The LLM framework was asynchronous: at every timestep each agent chose `<send>` or `<wait>` with no bias either way, so "who talks next" was self-selection only (T16 §B).

**Live Werewolf audio (T17).** 8 games, 18 people (groups of 10 and 8). Features per game-day: total speaking length, number of turns, successful and unsuccessful interruptions. Ranking players by these predicted who got lynched: interruption-based ranking put the lynched player in the top 2 in 63.2 % and the top 3 in 73.7 % of game-days (Table 5); the authors' reading is that the most-interrupted players are "justifying their position as non-liars" or accusing others. Liars spoke less ("liars tend to speak less, in order to avoid attention"); the table lynched a liar 52.3 % of the time.

**Recorded ONUW/Avalon games (T18).** 191 Werewolf games (4–6 players), 26,647 utterances, 7.6–11.5 words each. Strategy labels (counts from Table 2; percentages computed here, multi-label): YouTube set — Interrogation 16.4 %, Accusation 13.6 %, Defense 12.9 %, Evidence 8.4 %, Call for Action 5.6 %, Identity Declaration 5.1 %, No Strategy 37.9 %; Ego4D set — Interrogation 12.0 %, Accusation 11.5 %, Defense 9.8 %, No Strategy > 49.2 %. So in human play there are roughly **0.85–0.95 defence utterances per accusation utterance** and questions ("Interrogation") are the single most common move. Defense is defined as "Defend oneself or someone else against an accusation" (T18 §3.2). The paper does not analyse sequences, so the lag between accusation and answer is **not measured** anywhere I found.

**LLM play without a reply rule (T19, T21, T22).**
- GPT-4 agents in ONUW with three fixed discussion rounds: "GPT-4 rarely defends itself"; honest defence 1.1–4.3 % and deceptive defence 0.5–11.9 % of utterances across roles (T19, Table 2), against ~13 % in human games (T18).
- Werewolf Arena with bidding: "around 40% of bids from mentioned players consistently remain at the maximum value (4)"; early in a debate most players bid 0; majority consensus forms between debate turns 2 and 5 of 8; GPT-4 villagers spoke 6.25 times per round vs 4.86 for Gemini, and verbosity drew suspicion (T21).
- Kaggle Game Arena with round-robin and sequential votes: "capable models quickly learn to converge on a consensus target during the discussion phase", so the vote "largely reflects group conformity rather than private deductive accuracy" (T22 §A.8).
- Belief shifts (T20, abstract): an accusation makes an observing model more suspicious of the accused and less of the accuser, "especially when the accuser is trusted", even when the accuser is a wolf. An unanswered accusation therefore stands.

**Next-speaker prediction in general multi-party chat.**
- MultiLIGHT (T30; three-party chats, 28.7 utterances each): predicting the next speaker from history alone reached 49–54 % vs 33 % random; adding the *current* utterance lifted it to 82–85 % (the addressing line nearly determines the answerer). But a trained speaker-choice model gave "insignificant contribution to the quality" in human evaluation versus random choice, in open-ended chat.
- Meeting data (T31, abstract): text-only LLMs beat supervised models and humans at next-speaker prediction on AMI; context mattered most.
- Triadic discussions (T32, abstract): explicit addressees occur in "approximately 20% of conversational turns"; GPT-4o's addressee recognition was only marginally above chance.
- Murder-mystery agents (T25): with four agents and 10-turn discussions (50 runs per condition), random-order turns (EQUAL) and pure self-selection (SS) produced 1–8 breakdowns per dialogue; adding the adjacency-pair rule (CSSN-or-SS) centred breakdowns near 1 (Kruskal–Wallis χ² = 42.2, p < 0.001) and "significantly reduced utterances that led to dialogue breakdowns"; LLM-judge coherence/cooperativeness/diversity rose (all p < 0.01 except coherence vs EQUAL, p = 0.084). "Ignore question" still occurred "approximately 40 instances" across 500 turns (~0.08 per turn). Side effect: topic fixation (six of ten turns on one object).

**Summary of what is measured and what is not.** Measured: humans answer accusations about as often as they make them (T18); LLMs without a rule rarely defend (T19); a mention rule roughly halves breakdowns (T25); mentioned players want to speak (T21); round-robin and visible sequential votes push conformity (T22); LLMs talk 4–20× more than humans per game (T16). **Not measured anywhere found:** the number of utterances between an accusation and the accused's reply in human games, and who-speaks-after-whom matrices for social-deduction games. The two conversation-dynamics corpora (T15, T18) do not report them.

---

## 4. AI implementations

| System | Who speaks next | Extra model calls per spoken line | Reported effect |
|---|---|---|---|
| Xu et al. 2023 (T23) | One pass per day: "The talking order is randomly determined."; the moderator names each speaker; vote pass afterwards | 0 | Strategic behaviours emerge; hallucination and forgetting noted; sample day turns are generic and repetitive (my reading of App. A.7) |
| AIWolf competition (T24) | Turn-based track: agents speak only when the server requests, synchronized turns (2023: max 10 per day, same-turn talks invisible to each other, snippet); Anytime track: speak when you like, "upper limit… (4 times)" per day; `Skip` / `Over` tokens to decline (snippet) | 0 (turn-based) / 1 poll per agent per tick (anytime) | No coherence numbers found |
| Werewolf Arena (T21) | Every non-previous speaker bids 0–4 in parallel each turn; "The highest bidder speaks next."; ties: a random draw in which mentioned players are listed twice (`game.py`); bid 4 = "Someone has addressed me directly and I must respond."; `MAX_DEBATE_TURNS = 8`, 8 players | N − 1 bid calls per line (+ 1 to speak) | ~40 % of mentioned players bid 4; tie rule "encouraging agents to respond to direct mentions or accusations"; consensus by turn 2–5; verbose model dominated the floor. No direct coherence metric |
| Kaggle Game Arena Werewolf (T22) | "a Round-Robin protocol constrained to a maximum of two full cycles"; "The speaking order rotates systematically each day."; sequential exile vote, order rotating, plurality, tie = no exile; rotation "to eliminate positional bias" | 0 | Villager win rate 73.4 % → 56.7 % after rule fixes; votes reflect "group conformity"; no accusation-answer analysis |
| Kao et al. 2026 (T16) | Asynchronous: each timestep every agent outputs `<send>` or `<wait>` | 1 scheduler call per alive agent per timestep (+ 1 generator) | 268.6 utterances per game vs 72.5 human; deception judged harder to detect than humans' |
| Nonomura & Mori 2025 (T25) | After each line an LLM (`detectDesignation`, GPT-4o) checks for a first pair part (question, address, request) and its addressee; the addressee "has both the right and obligation to become the next speaker"; otherwise each agent's `think()` returns speak/listen + importance 0–9, highest wins, random tie-break; if all listen the current speaker continues | 1 detector + N `think()` calls per line (+ 1 to speak) | Breakdowns per 10-turn dialogue fell from a 1–8 spread to ~1; human score ~8 vs ~4; residual "ignore question" ~0.08 per turn; topic fixation |
| AutoGen 0.2 / AG2 `GroupChat` (T27) | `speaker_selection_method`: `auto` (an LLM picks, re-queried up to 2× if it returns zero or several names), `round_robin`, `random`, `manual`, or a callable | 1 (auto) / 0 (others) | None reported for games |
| AutoGen 0.4 `SelectorGroupChat` (T26) | Model prompt with `{participants}`, `{roles}`, `{history}` picks the next speaker; by default "will not select the same speak consecutively" [sic]; `selector_func` / `candidate_func` override or narrow | 1 (0 with `selector_func`) | None reported; docs advise simple prompts and custom functions once rules multiply |
| ChatArena (T28) | Environment-defined turn order (conversation: players take turns; "Moderator Conversation": an LLM moderator "controls the game dynamics"; Chameleon: hard-coded rules) | 0 or 1 (moderator) | None; project deprecated Aug 2025 |
| CAMEL (T29) | Two-agent role-play (AI user ↔ AI assistant) under inception prompting; turns alternate by construction | 0 | Not a multi-party system |
| MultiLIGHT models (T30) | Trained "speaker only" / "speaker and utterance" / silence-token models | 1 small model call | Next-speaker accuracy 49–85 %; no quality gain over random in open-ended chat |
| **Ours** (`game.py` 674–780) | Officer-with-result first; named players owed a slot, served with p = 0.7 (two at once) else one interjection then the reply; silent players p = 0.5 or when the budget is nearly spent; else weighted random by silence; last line names a vote; PASS shown as "(declines to answer X)" | 0 | Observed: accused sometimes never replies; "takes the floor" opens unrelated topics |

Why the accused never replies in our loop (from the code): (a) the debt is cleared whenever the owed player takes *any* slot, including a "hasn't spoken yet" slot with a prompt that tells them to name a suspect rather than answer (line 763 with the prompt at 741); (b) when `left ≤ len(silent) + 1` the silent-player rule pre-empts the reply for the rest of the day (line 688–690), so a late accusation is never answered before the vote; (c) with p = 0.3 the reply is deferred behind an interjection, and the interjector's own mentions are appended to the same queue; (d) two owed players answer in parallel, so neither sees the other's line. Why topics wander: the "takes the floor" and "hasn't spoken" prompts both offer "or open a new one" / "Name who you suspect" (lines 741, 756–757), which is the self-selection rule with an invitation to change subject.

---

## 5. Design options for us

Costs are extra model calls *per spoken line*, beyond the one call that produces the line. N = alive players (6 at the start).

| # | Rule | Extra calls / line | Expected effect | Risk |
|---|---|---|---|---|
| A | **Adjacency-pair obligation** (SSJ rule 1; T25): the first living player named in a line gets the next slot, p = 1, sequentially; only if nobody is named does self-selection run | 0 (regex `mentions()` exists) | The one mechanism with a measured effect on coherence (T25: breakdowns ~1 per 10 turns vs 1–8); matches every table rule in §2 | Ping-pong between two players and topic fixation (T25's own limitation); needs a cap and an interjection rule |
| B | **Bidding** (T21) | N − 1 | Mentioned players self-report the urge to answer (40 % bid 4); flexible | Multiplies cost by N; verbose models win the floor (T21); still only a tie-break for the mentioned player |
| C | **LLM moderator picks the speaker** (T26/T27 `auto`; T28) | 1 | Can weigh "who has been asked", "who hasn't spoken", "vote is near" together | Hallucinated or repeated names need retries (T27 re-queries up to 2×); no measured quality gain over random choice in open-ended chat (T30); adds latency on every line, which the few-seconds-per-turn target cannot afford |
| D | **Round-robin with rotating first speaker** (T22, T5, T24 turn-based) | 0 | Everyone speaks equally; no starvation; trivially fair | Highest breakdown rate in T25's EQUAL condition; conformity in T22; the accused answers only when their seat comes up |
| E | **Speak-or-wait polling** (T16, T24 anytime, T30 silence token) | N per tick | Natural asynchrony; players decide for themselves | 2/3 of decisions are silence (T30), LLMs then talk 4× too much (T16); cost; order of simultaneous sends is arbitrary |
| F | **Pre-vote defence slot** (T4 top-2/3 defence; T5 justification minute; T3 "may defend himself") | 0 (reuse `accuses()` / `heat`) | The player the vote is about always gets the last word before it, whatever happened earlier | If accusations are spread thin there is no clear "accused"; then fall back to the longest-silent |
| G | **Visible decline** (T24 `Skip`/`Over`; T2 "Not accusing anyone is also suspicious"; our PASS) | 0 | A refusal becomes evidence other players can use; prevents forced filler | A model that passes too often; cap passes per day |
| H | **Interjection only after a two-line exchange** (SSJ rule 2 bounded) | 0 | Keeps third parties in the thread without letting them restart it | Picks the interjector at random; prompt must bind them to the exchange |
| I | **Silent players speak on the thread, not on a new topic** (prompt change only) | 0 | Fixes the "unrelated topics" symptom at its source (prompt lines 741, 756–757) | None beyond slightly less variety |

Option C is the only one that would need a new model call; everything else is slot allocation plus prompt wording.

---

## 6. Recommendation

One design, zero extra model calls per line: **deterministic adjacency pairs with a bounded interjection, a reserved "everyone speaks" pass, and a sport-Mafia pre-vote in which the accused defends and the last line votes.** Concretely, for `discussion()`:

**Slot assignment, in priority order, evaluated before every line**

1. **Officer with an unspoken guilty result** goes first (unchanged).
2. **Pre-vote block (last 2 lines of the budget).** Penultimate slot: the living player with the highest `heat` today (count of lines accusing them, existing `accuses()`), with a defence prompt ("A and B are voting you out: answer with one fact, or counter-claim"); if nobody has heat ≥ 1, the longest-silent speaker. Final slot: a player who is *not* the defender and not the previous speaker, weighted by silence, prompted to name a vote and the one thing the target did (today's `left == 1` prompt). An owed reply that is still open when the block starts is served by the penultimate slot if the owed player is the top-heat player, otherwise it is dropped; the drop is narrated ("X never answered Y") so it is visible.
3. **Owed reply.** If the last line named one or more living players other than its speaker, the **first-named** gets the next slot, p = 1, alone (no parallel answers); the others are queued FIFO, max queue length 2, older entries dropped when the pre-vote block begins. Exceptions: the named player already declined this accuser today (no re-obligation; treat as unnamed), or the named player is the previous-but-one speaker and this would be the third consecutive line between the same two players (see 4).
4. **Interjection.** When the same two players have produced two consecutive lines (A→B→A), the next slot goes to a third player chosen by the existing silence-weighted random pick, with today's "interjects" prompt (bound to THAT exchange: back one of them, add a fact, or ask one of them a question). After the interjection the owed player (if any) answers; then the pair rule resets.
5. **Everyone speaks once.** Reserve `len(silent)` slots: when `left - 2 == len(silent)` (2 = pre-vote block), silent players take the remaining non-reserved slots in seat order. Their prompt is **on the thread**: "The thread right now: … Continue it, or say whom you'd vote and why" — delete "open a new one" and "Name who you suspect" from that prompt. If a silent player is also the owed player, one slot settles both.
6. **Self-selection** (nobody named, no reserve due): the existing silence-weighted random pick, but with the thread prompt of (5) rather than "You have the floor… name who you suspect". A new topic is still possible, but it is no longer the default instruction.

**When an interjection is allowed.** Only by rule 4 (after a two-line exchange), never between a naming line and its reply. A player can never take two consecutive slots except the officer claim.

**How a decline is shown.** Keep PASS → "(declines to answer X)" in `public` and `today` (lines 768–769), and make it free (no budget decrement, as now). Add two guards: a player may decline at most once per day (second PASS is re-asked once, then narrated as silence), and a decline closes that accuser's claim on them for the day (rule 3 exception). The pre-vote dropped reply is narrated the same way.

**Where randomness enters.** Only in self-selection (rule 6) and in the choice of interjector (rule 4) and of the final voter (rule 2), each weighted by silence as today. Whether a named player answers is never random, and whether the accused gets the floor before the vote is never random.

**How every player still speaks once a day.** Rule 5 reserves exactly `len(silent)` slots ahead of the two pre-vote lines, computed every beat, so no sequence of replies can consume them. With budget 15 and 6 players that leaves 15 − 2 − 6 = 7 free slots for pairs and interjections on a full day.

**How the pre-vote lines work.** Two lines, fixed: the accused defends (sport Mafia's justification minute, Stanford's "statement of defense"), then one voter names a vote with a reason (the engine's existing last-line prompt; Greek tables justify the vote as they cast it, T10 S9). Then the vote.

**Cost.** Zero extra calls; `mentions()`, `accuses()`, `heat`, the silence weights and the PASS path all exist. The whole change is the priority ladder in `discussion()` plus three prompt strings.

**What to measure after the change** (so the design is tested, not assumed): share of naming lines answered by the named player within 1 line (target > 0.9; T25 residual was ~0.08 unanswered per turn), share of days where the top-heat player spoke in the last three lines (target 1.0), and number of lines whose first mention is a player not named in the previous five lines (the "unrelated topic" count; expect it to fall). The transcript stats in `stats.py` are the natural place.

**Deliberately not recommended.** Bidding (×N cost for a tie-break effect we can get for free), an LLM moderator (latency on every line, no measured quality gain in T30, repeat-name failure modes in T27), and speak-or-wait polling (T16's 268 utterances per game is the opposite of a 15-line budget).
