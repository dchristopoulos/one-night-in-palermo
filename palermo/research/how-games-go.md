# How real Palermo / Mafia / Werewolf games go

Research note, 2026-10-23. Goal: a yardstick for judging and tuning the AI-played
game (`games/archive/p1.json`, Palermo rules, 6 players, 2 killers; `games/archive/tour-1.json`,
single-killer rules).

Method: WebSearch + WebFetch, primary material preferred (game threads, data
papers, rules pages). Every quote is under 15 words and attributed. Where a page
could not be fetched the Sources table says so and the claim rests on the search
engine's snippet of that page.

Evidence gaps, stated up front:

- **MafiaScum wiki** (the richest strategy source) is behind a Cloudflare
  challenge; direct fetch, curl, a headless browser tab and the Wayback Machine
  all failed. Claims from it below come from search-result snippets of the named
  pages and are marked *snippet*.
- **YouTube transcripts**: none found. Searches returned only rules-school videos.
- **Greek Palermo table talk**: no transcript, recap or anecdote with actual
  lines was found. Greek sources are rules pages and one app FAQ; they do contain
  role advice (section 4) but no quotes of play.
- **In-person play**: only short blog recaps (player counts, minutes) with no
  dialogue. All verbatim table talk below is from text-based play (forum games
  and a chat-room experiment), which is the closest analogue to the AI game.

## Sources

| # | URL | What it is | Trust |
|---|-----|------------|-------|
| S1 | https://aclanthology.org/2022.naacl-main.11.pdf | Ibraheem, Zhou, DeNero (NAACL 2022), "Putting the Con in Context": 44 real chat-room Mafia games, 460 MTurk players, 4–10 per game, 1–2 mafia. Dataset statistics and verbatim mafia lines. Read in full. | High (primary data) |
| S2 | https://arxiv.org/abs/2601.13709 | Kao, Vats, Davis (2026), "Hidden in Plain Text": Table I compares the S1 human games (7–12 players) with 35 GPT-4o games on length in days, utterances per game, words per utterance. Read in full. | High (primary data) |
| S3 | https://boards.straightdope.com/t/mafia-evil-dead-day-night-one/477854 (and `?page=2`) | Straight Dope forum Mafia, 27 players, Day 1 thread. Verbatim votes and talk. | High (primary) |
| S4 | https://boards.straightdope.com/t/mafia-simpletown/442974?page=17 and `?page=54` | Straight Dope forum Mafia. p17: Day 1 random voting; p54: cop claim debate. | High (primary) |
| S5 | https://boards.straightdope.com/t/random-mafia/532942?page=39 | Straight Dope forum Mafia, bandwagon talk. | High (primary) |
| S6 | https://boards.straightdope.com/t/screamers-mafia/510938?page=56 | Straight Dope forum Mafia, doctor claim with no counterclaim. | High (primary) |
| S7 | https://boards.straightdope.com/t/mafia-reunion-day-one/776577/114 | Straight Dope, Day 1 post discussing whether a real power role should counterclaim at once. | High (primary, opinion) |
| S8 | https://www.conquerclub.com/forum/viewtopic.php?p=4930086 | Conquer Club forum debate: lynch vs no-lynch on Day 1, with a 25-game tally. | Medium-high |
| S9 | https://dragonmount.com/forums/topic/75896-mafia/ | Dragonmount forum: experienced players describing Day 1 votes. | Medium |
| S10 | https://dragonmount.com/forums/topic/76698-new-player-tips-and-information/ | Dragonmount new-player tips (lurking, pressure, pace). | Medium |
| S11 | https://www.gog.com/forum/general/forum_game_conclave_mafia_gog_mafia_game_82/post309 | GOG forum Mafia game 82, wagon post-mortem. | High (primary) |
| S12 | https://www.planetcricket.org/forums/goto/post?id=2094890 | PlanetCricket "WWE Mafia II" end-of-game summary: 14 players, 7 days, cop guilty vs Miller claim, cross-claim. | High (primary recap) |
| S13 | https://forum.feed-the-beast.com/goto/post?id=719349 | Feed-the-Beast "Werewolf: Hope+1": 13 players, 5 days, fake seer claim by a wolf, real seer counterclaim, quoted wolf chat. | High (primary) |
| S14 | https://forums.anandtech.com/threads/are-you-a-werewolf-game-10-over-the-village-wins.2461067/post-37974536 | AnandTech Werewolf game 10: 12 players, Day 1–Day 5, night-kill list. | Medium (page partly visible) |
| S15 | https://www.eblong.com/zarf/werewolf.html | Andrew Plotkin's canonical Werewolf rules and play notes (2 wolves, 7+ players, seer behaviour, tells). | High (canonical) |
| S16 | https://www.eblong.com/zarf/werewolf-stats.html | Plotkin's simulated win rates under random lynching, per player/wolf count. | High (model, stated assumptions) |
| S17 | https://en.wikipedia.org/wiki/Mafia_(party_game) | Player counts, 15–90 min, game-theory results (Braverman et al.), live-play notes. | Medium-high |
| S18 | https://gameonfamily.com/blogs/tutorials/mafia | How-to blog: minutes per player count, 1 mafia per 3–4 villagers, mafia tips. | Medium |
| S19 | https://www.thegamegal.com/2014/10/29/mafia/ | How-to blog: detective should persuade, not announce. | Medium |
| S20 | https://werewolv.es/the-ultimate-werewolf-online-strategy-guide | Online Werewolf strategy guide: endgame parity rules, consistency. | Medium |
| S21 | https://20thcenturygames.substack.com/p/mafia-werewolf | Tao of Gaming essay on why base Werewolf gets tedious. | Medium (opinion) |
| S22 | https://thesystemisdown.substack.com/p/5-werewolf-strategies | "Five killer moves" wolf tactics. Fetch returned 404 twice; search snippet only. | Low-medium (snippet) |
| S23 | https://wiki.mafiascum.net/index.php?title=RVS | MafiaScum wiki, Random Voting Stage. Cloudflare-blocked; snippet only. | Medium (snippet) |
| S24 | https://wiki.mafiascum.net/index.php?title=VCA | MafiaScum wiki, Vote Count Analysis (distancing, OMGUS, wagon shopping, reaction tests). Snippet only. | Medium (snippet) |
| S25 | https://wiki.mafiascum.net/index.php?title=When_to_bus%3F | MafiaScum wiki on bussing. Snippet only. | Medium (snippet) |
| S26 | https://wiki.mafiascum.net/index.php?title=A_Beginner%27s_Guide_to_Being_Awesome_At_Mafia | MafiaScum beginner guide (bussing vs distancing, lurking, short posts). Snippet only. | Medium (snippet) |
| S27 | https://wiki.mafiascum.net/index.php?title=Umbrage%27s_Guide_on_How_to_Win_Scum_Games | MafiaScum scum guide (OMGUS, Day 1 wagon tests). Snippet only. | Medium (snippet) |
| S28 | https://wiki.mafiascum.net/index.php?title=Cop and `?title=Follow_the_Cop` and `?title=Doctor` and `?title=Neapolitan` | MafiaScum role pages (claim timing, breadcrumbing, guilty results, doctor targets). Snippet only. | Medium (snippet) |
| S29 | https://wiki.mafiascum.net/index.php?title=Interactive_Tells and `?title=Mastin%27s_Insane_Tells` and `?title=Mini%27s_Scumhunting_Kit` and `?title=Albert_B._Rampage%27s_Guide_on_How_to_Play_a_Large_Game` | MafiaScum tells pages (wagon position, chainsaw defence, "lol" defence, consensus is rare). Snippet only. | Medium (snippet) |
| S30 | https://epicmafia.fandom.com/wiki/Bus and `/wiki/Counter-claim` | EpicMafia wiki definitions. Fetch returned 402; snippet only. | Low-medium (snippet) |
| S31 | https://www.bulbagarden.net/goto/post?id=5853757 (and nearby posts) | Bulbagarden "Mafia – The 100": competing cop claims. Fetch returned 402; snippet only. | Low-medium (snippet) |
| S32 | https://bryantanner.blogspot.com/2009/02/werewolf-variations-on-game-mafia.html | Family blog: two in-person games, 10 and 11 players, 10–20 min each. | Medium-low |
| S33 | https://palermonights.gr/faqs/ and https://palermonights.gr/characters/ | Greek "Palermo Nights" app: rules FAQ and 26 role descriptions (shown/hidden killer, policeman, doctor). | Medium-high (official app site) |
| S34 | http://palermogame.blogspot.com/2014/04/blog-post.html?m=1 | Greek rules blog (11+ players, card roles, informer advice, how accusations sound). | Medium |
| S35 | https://cardgamesgr.blogspot.com/2014/03/blog-post_3402.html | Greek card-game blog: Palermo rules, 1 killer per 4 citizens, first night is identification only. | Medium |
| S36 | https://all4fun.gr/more-fun/afierwmata/4411-peftei-i-nyxta-sto-palermo | Greek feature: roles, endgame cases, what the shown/hidden killer and informer must do. | Medium |
| S37 | https://www.newsbeast.gr/entertainment/arthro/12273254/i-nychta-peftei-sto-palermo-kai-alla-paichnidia-choris-exoplismo-gia-na-paixete-oikogeneiaka-stis-giortes | Greek news feature: 7+ players, informer, visible/hidden killer, endgame cases. | Medium |
| S38 | https://kidsproject.gr/articles/470/impostor-sto-palermo-hdh-eteron | Greek article: policeman (Ace) version; killers' day goal is to find the policeman. | Medium |
| S39 | http://palermopaixnidi.blogspot.com/2013/11/blog-post_25.html | Greek rules blog with "informant", "courtesan" and fate cards (a commercial variant). | Medium-low |

## 1. Day 1 with no information

What the sources agree on:

- **Day 1 lynches are near-random, and everybody knows it.** A 25-game tally on
  one forum found 8 Day-1 lynches hit scum (32%), i.e. about 68% hit town [S8].
  Plotkin's random-lynch simulation gives humans 13% (7 players) to 16% (10
  players) with two wolves, as a floor for "completely stupid" play [S16].
  Experienced players: "A lot of games start with votes that are cast for frivolous reasons." (WWWwombat) [S9].
- **The opening is social, then votes appear with thin reasons.** Conquer Club
  posters describe a "meet and greet" stretch of several pages before accusations,
  and accusations "based on feel, playstyle, typos, or lurking" [S8]. In the
  chat-room games, many utterances are social ("hi erybody") or vote chatter
  ("I bet it's Mandy...") [S1].
- **"Random" votes are a convention, and dice-random is frowned on.** The
  MafiaScum Random Voting Stage exists "to spur the game into action" and draw
  reactions; a provably random vote gives nothing to read [S23, snippet]. One
  essay: "the more you try to make it random the more you are helping scum" [S29
  snippet, Thor665]. Votes that are easily shaken off are "reaction tests";
  a vote nobody will move off becomes the wagon [S24, snippet].
- **Pressure on quiet players is standard and is itself argued about.** Lurking
  is treated as anti-town ("profoundly harmful to the Town") [S26, snippet];
  a player "who suddenly emerges from lurking to join a wagon" is extra suspect
  [S29, snippet]. But talkers complain: "you guys really seem to jump on people who talk" (peekercpa) [S4 p17].
- **Consensus is rare; votes stay scattered.** In S3 the Day 1 votes "stayed
  scattered" across four targets; Simpletown Day 1 "had no consensus" and ended
  with no lynch [S4]. A large-game guide: fast 8–10-vote wagons off the random
  stage are rare because "agreement and consensus are usually in short supply" [S29, snippet].
- **Demanding reasons is the main Day 1 activity.** Nearly every vote is met
  with "why?", and the voter's reply (or non-reply) is what people read.
- **Even the lynch/no-lynch question is argued at the table.** "No lynching makes no sense in my eyes" (nagerous) vs "there is very little reason to lynch day 1" (Samlen) [S8].

Verbatim Day 1 table talk (text play), each under 15 words:

1. "Gonna start with not-random vote: Pleonast." — JSexton [S3]
2. "JSexton, where's the reasoning for voting Pleonast?" — macey [S3]
3. "Any explaination for the not-randomness?" — Hockey_Monkey [S3]
4. "vote pedescribe" ... "as a random vote." — Pleonast [S3 p2]
5. "I'll withdrawal once I get adequate explanation." — Pleonast [S3 p2]
6. "Now just wait one cottin-picking minute!" — pedescribe, under a vote [S3 p2]
7. "I flew all day yesterday and had no computer access last night." — pedescribe, excusing silence [S3 p2]
8. "I'll keep my vote for lack of better one" — Natlaw [S3 p2]
9. "Kind of quiet in here…" — Thing_Fish [S3 p2]
10. "Vote Zuma" — MadTheSwine, on a lurker [S4 p17]
11. "Can you explain why switching votes three times is scummy?" — ShadowFacts [S4 p17]
12. "If you don't lynch me, then I can break out the claws." — Menocchio, at L-1 [S4 p17]
13. "We don't really have any sort of consensus" — fluiddruid [S4 p17]
14. "OK, what's with the bandwagon on One and Only?" — special_ed [S5]
15. "I'm not quite convinced of the case on OaOW" — GuiriEnEspana [S5]
16. "I still lean scum for my reluctance, though!?" — PookaMustard, on himself [S11]
17. "hi erybody" — chat-room player, opening [S1]
18. "I bet it's Mandy..." — chat-room player [S1]
19. "It's a little early to tell." — a mafioso, stalling [S1]
20. "It's a shot in the dark." — a mafioso, stalling [S1]

## 2. Officer (cop / seer / informer) play

- **Do not claim Day 1 without a result.** Cop page: avoid claiming
  "particularly Day 1"; a player with a useful result should "breadcrumb" so
  the result survives their night death [S28, snippet]. Plotkin: the seer
  "usually hides his identity" because revealing makes him the top kill target
  [S15]. Tao of Gaming: a seer who announces will "tend to be brutally mauled the next night" [S21].
  How-to blogs say the same for in-person detectives: persuade, don't announce [S19].
- **Claim when you hold a guilty, or when you are about to be lynched.** A
  guilty is the strongest thing in the game: "it is notoriously difficult to fakeclaim one's way out of a Guilty result" [S28, snippet].
  In S12 the cop reported a guilty on Day 3 and "many townies then turned on" the target.
  Players also expect a real role to claim rather than die: "the detective/cop hasn't counterclaimed, in which case he/she is an idiot" (Nanook) [S4 p54].
- **The deliberate exception: Follow the Cop.** With a doctor in the setup the
  cop may claim Day 1 and be protected while investigating nightly; mafia's
  counter is to kill the doctor or counterclaim cop [S28 Follow_the_Cop, snippet].
- **How the town reacts to a lone claim.** Default is provisional trust:
  "A cop should be trusted until a false result or a counterclaim." (ToeJam) [S4 p54];
  "NaF is the real deal, as there hasn't been a counter claim." (ToeJam) [S4 p54].
  The absence of a counterclaim is itself read as evidence: "Really, I can't see why Scum would want to be counter-claimed" (Chronos) [S6].
- **Fake cop / counterclaim, as it actually plays out.**
  - S13 (13 players): wolf Shazam08 claimed seer *with three named checks*; the
    real seer VikeStep then claimed, naming Shazam08 and Gideon as wolves.
    Post-game: "btw. Shazam08 I knew you would claim to be seer." (VikeStep) [S13].
    The village resolved it by lynching Shazam08 (Day 4) then Gideon (Day 5) and won.
  - S12 (14 players): the cop's guilty landed on a player who had pre-claimed
    Miller; a mafioso cross-claimed; "some lynched Spoobir and some stayed with their lynch on p23456789" — the split let mafia win [S12].
  - Timing heuristics players use: the one who claims first and unprompted is
    read as more town ("the first person to hard claim ... is automatically more townie", contested) [S31, snippet];
    a counterclaim that appears only after being named is distrusted:
    "A later claim by the true role will be distrusted" (nesta) [S7].
  - Whether a real role should counterclaim at once is debated:
    "consider whether staying hidden would be better than immediately counterclaiming." (Captain_Klutz) [S7].
- **Resolving cop vs cop.** Two patterns: (a) *Lynch All Liars*: lynch one
  claimant, and if they flip town lynch the other; players know this and note
  that under LAL even an honest claim can get you lynched [S28/S23 snippets of
  player pages]; (b) *lynch neither, make scum kill*: "not lynching is the correct play when you have competing cop claims" [S31, snippet],
  because the real cop keeps producing results and the night kill reveals whom scum fear.
  Checks are weighed by consistency with flips and vote history, exactly as
  our p1 town did (section 8).

## 3. Killer (mafia / wolf) play

- **Night-kill targets.** Sources split between "kill the threat" and "stay
  boring". Power roles first: scum "should be on the lookout for power roles" because a cop catch "can ruin the whole game" [S28 Mafia page, snippet];
  doctor pages assume mafia will spend a kill on a claimed role [S28, snippet].
  But real wolf chat on night 1: "Right then, wolves, we need to avoid high-priority targets for the first night." (Shazam08) [S13],
  and "I like Real. Let's go with Carbon, for now." (Gideonseymour) [S13] — a low-profile pick.
  In Greek Palermo the killers' day job is explicit: find and kill the policeman/informer [S38, S36].
- **Stalling and misdirection, as recorded in real chat.** Mafia "suggest that there is not enough information" ("Should we wait to eliminate someone?"),
  raise suspicion on a known bystander ("I'm going to vote bianca. she's so casual with life and death"),
  and invent motives ("It might be Jonathan Kim... killing off Erin who accused him") [S1].
- **Defending when accused.** Advice converges on: don't over-defend, redirect.
  "overreacting draws attention"; "Accuse active Villagers to shift suspicion." [S18].
  The classic scum tell is OMGUS (voting whoever voted you): "never ever ever use OMGUS" [S27, snippet];
  a "lol, that case is hilarious" defence "should warrant a vote every time" [S29, snippet];
  defending a partner by attacking their accuser ("chainsaw defence") is a tell once the partner flips scum [S29, snippet].
  Consistency matters: "If you are evil, commit to a worldview from the start." [S20].
- **Wagon position.** Scum prefer the middle of a wagon, the "Butter Zone", not
  its start or its hammer [S29, snippet]. S11's post-mortem calls a wrong lynch
  "a not well thought out wagon" (PookaMustard) [S11].
- **Distancing.** Mafia vote each other early "to appear that they don't know each other" [S24, snippet];
  in the current meta distancing (scum attacking each other by day) is more
  common than a real bus, and sloppy distancing is obvious [S26, snippet].
- **Bussing.** Voting out a partner to buy credit: "betraying a teammate to win town's trust" [S30, snippet].
  It pays only when you win more easily with fewer partners [S25, snippet];
  losing a partner "is a major dent to the Mafia's power" and the busser often
  gets no credit anyway [S26, snippet]. Advice: be exactly as aggressive as you
  would be as a villager [S30, snippet]; "Occasionally vote against your fellow Mafia" [S18].
- **Fake seer/cop claim as a wolf.** Claim after a few rounds, name real
  villagers as "cleared", and consider having your partners kill you so the
  village trusts your fake results [S22, snippet]. S13 is a real instance (three named checks).
- **Last words.** Plotkin: a lynched player "must make his defense before the vote is final" [S15];
  in Greek card Palermo the eliminated player "may declare innocent or guilty" and "is not required to tell the truth" [S34].

## 4. Palermo-specific: the shown/hidden pair and a policeman who knows one killer

Greek sources found (rules and role advice only; no play transcripts):

- **Structure.** Two killers, one φανερός (shown) and one κρυφός (hidden); they
  know each other ("Γνωρίζει τον κρυφό δολοφόνο." — shown-killer card) [S33 characters].
  The policeman/informer sees the shown killer on night 1 and nothing else
  [S33, S34, S35, S36, S38]. Classic ratio: about one killer per four citizens [S35];
  7+ players [S37] or 11+ [S34]. In the card game the *first night is
  identification only* and the first kill happens on night 2 [S35, S34]; the app
  version starts with a Day [S33 FAQ].
- **Policeman play.** All sources say: steer the vote onto the shown killer
  *without* revealing. The app FAQ: the police "can claim the role publicly, but others are not obliged to believe it" and "suggests not revealing it" [S33 FAQ].
  Blog: naming the open mafioso outright is "considered poor play but is allowed",
  others need not believe it, and "it may be a Mafia bluff" [S34].
  The role card itself: help others eliminate the shown killer "without revealing their identity" [S33 characters].
  Citizens are expected to "risk their own safety to protect the snitch" [S36].
- **Shown killer play.** "The police already know this role's identity, so the player must act carefully" [S33 characters];
  the visible killer "must stay under the radar" [S36]. The shown killer is the
  one who should be quiet and bland; the hidden killer carries the team and is
  "considered the killers' biggest advantage" [S37, S36].
- **Killers' day objective.** The killers' "main goal during the day is to identify the policeman" and kill them at night [S38].
  So killers read the table for *who is pushing the shown killer too knowingly*.
- **Fake-police counterclaim is expected.** "A killer who is revealed can claim to be police" [S33 FAQ].
- **Endgame cases are spelled out.** With 2 killers + informer + 1 citizen left,
  voting out a non-killer loses; with 1 killer + informer + citizen, voting the
  citizen is a draw [S36, S37].
- **What day talk sounds like (only description found).** Players open with
  "suspicious glances", and accusations are often weak, e.g. claiming "to feel a neighbor move during the night" [S36, S34].

Not found: any Greek thread, video or recap with actual lines of Palermo table talk.

## 5. Pace and length

Measured human data (text chat, S1/S2 Table I; 7–12 players, mean 9.5, 1–2 mafia):

| Metric | Humans | GPT-4o agents (S2) | Our p1 (6 players) |
|---|---|---|---|
| Game length, days | 2–4, mean **3.11**; 82% end by Day 3 | 2–4, mean 3.17 | 2 |
| Utterances per game | **72.5** (S1 reports 49 over 44 games) | 268.6 | 34 lines + 31 memory notes |
| Words per utterance | **5.9** | 110 | 17 |
| Utterances per day | ≈23 for ≈9.5 players (≈2.5 per player per day) | ≈85 | 17 per day (≈3 per player per day) |

Other length evidence:

- In-person: 7–10 players ≈15 min, 10–15 players ≈30 min [S18]; two family
  games of 10 and 11 players took 10–20 min each [S32]; Wikipedia: 15–90 min [S17].
- Forum: 12 players → 5 days [S14]; 13 players → 5 days [S13]; 14 players with
  5 anti-town → 7 days [S12]. Forum days last real days ("later Days last five real-life days, and Nights last two" in one ruleset) [S3 rules post].
- Parity arithmetic (each full cycle removes 2 players: one vote, one kill;
  killers win at parity, town wins when all killers are gone), with 2 killers:

| Players | Composition | Town must hit a killer by | Days if town plays well | Days if town misses |
|---|---|---|---|---|
| 6 | 2K + 4T | Day 1 | 2 | 1 (killers win at dawn of Day 2) |
| 7 | 2K + 5T | Day 2 | 2–3 | 2 |
| 8 | 2K + 6T | Day 2 | 2–4 | 2 |
| 10 | 2K + 8T | Day 3 | 3–5 | 3 |

  Plotkin recommends two wolves and 9 or 11 players for this reason: 6–8
  players with two killers gives town one or two shots [S15]. With *one* killer
  (tour-1 rules) 6 players gives town up to 3 days. Endgame rule of thumb from
  Werewolf: execute on odd counts, skip on even [S20]; abstaining generally
  favours mafia except when survivors are even [S17].

- Line pace: in forum play a post is often one sentence; in the chat-room data
  six words is the mean. Dragonmount's advice to newcomers: "The game will be way slower than you think it should be." (peacesells) [S10].

## 6. Clichés and mistakes that make games boring or unreadable

- **Repeated bare denial.** The base game "consisted of repeated denials" — "But I'm not a Werewolf!" — which the essayist found tedious [S21].
- **Pure random voting.** Gives nothing to read; "strictly frowned upon" [S23, snippet]; "a demonstrably random vote gives others nothing" [S23, snippet].
- **No-lynch by consensus.** An early no-lynch consensus "leads to people not really talking about much." (strike wolf) [S8].
- **Everyone lurking to avoid being a target.** Day 1 lurking and "submarining" are common "because nobody wants to be a target" [S8]; "lurking under pressure never works out in your favor" [S29, snippet].
- **OMGUS and vote flip-flopping.** Voting back at your accuser [S24, S27 snippets]; "Can you explain why switching votes three times is scummy?" [S4 p17] shows how the table polices it.
- **Over-long posts.** "succinct posts will do you wonders; keep things as short and coherent as possible" [S26, snippet].
- **Accusations on noise.** Typos, tone, "feel" [S8]; Plotkin's catalogue of
  "suspicious" behaviours (accusing, not accusing, agreeing, disagreeing) shows
  how every action can be read either way [S15].
- **Predictable endings.** Even player counts end in an anticlimactic night
  kill everyone can see coming at sundown [S15].
- **Claiming too early.** "burned the friggin seer day 1" is the complaint when a seer reveals Day 1 [FOFC thread snippet, page blocked: https://forums.operationsports.com/fofc/showthread.php?p=1539386].
- **Split town on cross-claims.** The S12 game was lost because the town split
  between two claimants instead of resolving in order.

## 7. Comparison with our p1 game

p1: 6 players, 2 killers (Haiku shown, Sol hidden), Gemma officer, Sonnet doctor,
Luna and Terra citizens. 4.0 min, 34 spoken lines, 17 words/line, median gap 4.9 s.
Night 1 kill blocked by doctor self-save; Haiku voted out Day 1; Luna killed
Night 2; Gemma claimed officer with a guilty on Sol, Sol counterclaimed, Sol
voted out Day 2. Town wins.

| # | Observation in p1 | What real play does | Evidence | Suggested minimal change |
|---|---|---|---|---|
| 1 | Lines average 17 words; every Day 1 line is a full read with a reason. | Human chat lines average 5.9 words; Day 1 is mostly short votes, "why?", jokes, excuses. | S2 Table I; S1; S3 lines 1–9 | Prompt fact: "A normal line is one short sentence (under 12 words). Save a paragraph for a claim or a case." Test: words/line in `review.py` falls under 10. |
| 2 | No "random-vote" phase: the first speaker (Haiku) opens with a hard push on Terra, and the whole table immediately argues about that push. | Day 1 opens with admitted thin votes ("as a random vote", "for lack of better one"), reaction tests, then a wagon forms late. | S3, S4 p17, S23/S24 snippets | Engine: allow a "pressure vote" line type with no reason required early on Day 1; prompt fact: "An early vote may be a reaction test; say so." Test: at least one vote on Day 1 is placed before any read is given. |
| 3 | Five of six players wrote the same memory note ("Haiku pressed Terra without giving a read") and four voted Haiku with the same wording. | Consensus is rare; Day 1 votes stay scattered, and at least one player argues against the wagon. | S3 ("votes stayed scattered"), S4 ("no consensus"), S29 snippet | Prompt fact for citizens: *if you agree with the leading wagon, add a new reason or say what would change your mind; one player should test the wagon.* Test: count distinct vote rationales per day. |
| 4 | Haiku, the *shown* killer whom the officer already knows, is the loudest player on Day 1 and OMGUS-switches his vote onto Terra after she votes him. | Shown killer "must stay under the radar"; OMGUS is the canonical scum tell. | S33, S36; S27 snippet | Prompt fact for the shown killer: *the officer knows you; be bland, vote with the room, never vote back at your accuser.* Test: shown killer's share of Day 1 lines is below average. |
| 5 | Killers never try to identify the officer; Sol's Night 2 pick is "pressed Haiku without drawing attention" (Luna, a citizen). Gemma's only Day 1 line was a jab at Haiku and she voted him: the obvious officer tell went unused. | In Palermo the killers' day objective is to find the policeman; in Werewolf, wolves hunt the seer and note who pushes a partner "too knowingly". | S38, S36; S28 Mafia snippet | Prompt fact for killers: *at night, rank survivors by how likely each is the officer (who voted the shown killer earliest, with least argument); kill the top one unless the doctor is the bigger threat.* Test: night proposals name an officer suspect. |
| 6 | Sol counterclaims officer with no history, a result on the accuser, and the admission that he waited; Sonnet resolves it using Day 1 vote history. | Real fake claims come with pre-built results (three named checks in S13); a claim that appears only after being named is distrusted; towns resolve by claim order, result consistency, or LAL. | S13, S7 ("later claim ... will be distrusted"), S12, S31 snippet | Prompt fact for the hidden killer: *if you may need to fake officer, decide at night and plant a 'check' result the day before.* Engine: nothing. Test: does a hidden killer ever breadcrumb a fake result before claiming? |
| 7 | Doctor self-protects both nights, including after the officer is publicly claimed. | Doctor targets are claimed roles and obvious town; Follow-the-Cop depends on it. | S28 Doctor/Follow_the_Cop snippets | Prompt fact: "Once someone has claimed officer and the town believes them, protect the claimant." Test: doctor's Night 2 target equals the claimed officer. |
| 8 | Night 1 kill happens before any day discussion (Sonnet chosen because his intro "was a comment on the room"). | Classic card Palermo: night 1 is identification only, first kill on night 2; the app starts with a Day; Werewolf proper does kill first. | S35, S34, S33 FAQ, S15 | Engine option: `first_night_kill=false` for Palermo rules, so Day 1 happens with everyone alive and killers choose after hearing the table. Test: compare officer survival and game length across the two settings. |
| 9 | Introductions are pure small talk (coffee, cactus, tacos); killers read them as tells ("Sonnet talks like they're already watching the table"). | Social openers exist ("hi erybody") but real Day 1 reads are about votes and reasons, not intros. | S1, S8 | Prompt fact: "Intros are not evidence." Or drop the intro round under Palermo rules. Test: memory notes written during intros should be empty or marked low-weight. |
| 10 | Eliminated killers confirm everything ("You got me. I was the hidden killer."). | Lynched players give a defence before the vote; after it, Greek rules let them lie or stay silent; in Werewolf the flip is announced by the moderator, not the player. | S15, S34 | Prompt fact: *last words come before the vote and are a defence; after elimination you may keep your secret.* Test: last-words line is produced before VOTES. (Low priority; mostly flavour.) |

What p1 already matches real play:

- Officer steers onto the shown killer without claiming on Day 1 (Gemma voted Haiku) — exactly the Greek advice [S33, S34].
- Officer claims the moment she holds a guilty and the game is on the line (Day 2, four alive) — the textbook claim trigger [S28, S4 p54].
- Town extends provisional trust to the first claim and then weighs the counterclaim by timing and vote history — the same heuristics players state [S4 p54, S7, S31].
- The table punishes OMGUS and pressure-without-a-read; Haiku's Day 1 behaviour is a real scum tell and a real town would have voted it too [S27, S29].
- Killers coordinate a single target and the shown killer proposes it [S15].
- Line gaps (median 4.9 s) are a believable table rhythm; the 4-minute total is shorter than the 15–20 minutes of a 7–10 player live game but 6 players and a Day 1 hit explain most of that [S18, S32].

tour-1 (single killer) in one line each: the Day 1 mislynch of a citizen who
pushed a quiet player is the statistically normal outcome [S8]; the killer hid
by joining an existing wagon mid-way, the "Butter Zone" [S29]; the officer
claimed only when it decided the game and was believed partly because the
killer's attack on the claim offered no counterclaim [S4 p54]; the killer's
post-mortem "should've killed Luna" is the kill-the-cop rule [S28].

## 8. Suggested changes, ranked

1. **Shorten lines** (table row 1). Biggest readability gap: 17 words vs 5.9. One prompt sentence; measurable immediately with `review.py`.
2. **Shown killer plays bland** (row 4). One prompt sentence; fixes the main reason p1 was over in two days and makes the officer's job real.
3. **Killers hunt the officer** (row 5). One prompt sentence at night; turns Palermo's defining asymmetry into actual play.
4. **Break the unanimity** (row 3). One prompt sentence for citizens; cheapest way to get scattered Day 1 votes and real wagons.
5. **Early reaction-test votes** (row 2). Small engine change plus one prompt fact; gives Day 1 the shape real games have.
6. **Fake-officer prep by the hidden killer** (row 6). Prompt only; makes counterclaims resolvable on evidence rather than on timing alone.
7. **Doctor follows the claim** (row 7). Prompt only; without it, claiming is strictly worse than in real play.
8. **No kill on Night 1 under Palermo rules** (row 8). Engine flag; run both and compare days-per-game against the parity table in section 5.
9. **Intros are not evidence** (row 9). Prompt only.
10. **Last words before the vote** (row 10). Engine ordering; flavour.

Things to test rather than change: whether 6 players with 2 killers is the
right table at all (section 5 says town gets exactly one shot), and whether the
engine's unanimous-wagon behaviour persists at 8 players.
