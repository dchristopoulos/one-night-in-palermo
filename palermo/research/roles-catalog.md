# Extra roles and rule variants for a six-seat AI Palermo

Research notes, 2026-10-23. Read-only survey: every role in the Palermo Nights app, the Greek evil helper (Τσιράκι) and other folk extras, the Mafia and Werewolf role families, the named rule variants, and whatever six-player setups exist in print. Each row carries its source. The fit judgements (balance, drama, cost) are mine, reasoned from the six-seat arithmetic in section 2, and are not citations. Companion notes: `palermo-rules.md` (Greek rules consensus, cited below as PR-S*n*) and `how-games-go.md`.

Scales used in the tables. **Frequency**: core (nearly every source), common (several sources or apps), app-only (Greek apps only), one source, snippet (seen only in a search-engine snippet). **Balance at 6**: whom it helps at a six-seat table with two killers, with the vote/parity reason. **Drama**: what a viewer sees. **Cost** in our engine (roles code-enforced, agents only talk): cheap = a flag plus a prompt line inside existing night/day code; medium = a new night step, a visit model or an extra vote round; hard = a new phase or information channel.

## 0. Evidence gaps, stated first

- **MafiaScum wiki and forum**: Cloudflare 403 on every page, also through a reader proxy. Only search snippets of the `GF` and `RB` pages and of the thread "Help create 6-player setup" were seen. Marked *snippet*.
- **Town of Salem and EpicMafia fandom wikis**: HTTP 402. EpicMafia's own role pages (`epicmafia.com/roles/N`) were readable and are used instead; they are the house rules of a site built around 7-player games.
- **Icy Hippo «ΠΑΛΕΡΜΟ» app**: role names only (Δήμαρχος, Ερωτευμένοι, Καμικάζι, Αλεξίσφαιρος, Ρουφιάνος, Τρέλα, Εκδικητής, Μητέρα Τερέζα). No mechanics for Εκδικητής were found anywhere.
- **Kaissa «Παλέρμο: Το Μεγάλο Ξεκαθάρισμα»** (board game, 5–10 players): only a shop title surfaced; the shop page returned 403; no rules found.
- **Ultimate Werewolf**: the rulebook transcription covers few roles; Bezier's role page is 404. Mayor, Prince and Apprentice Seer rest on snippets of fan lists. Cursed, Lycan, Tough Guy, Old Hag, Diseased: no readable source, so they are left out.
- **Blood on the Clocktower**: rulebook and wiki say five or more players for Trouble Brewing, but the per-count distribution table is only on the physical setup sheet. No numbers are quoted.
- **BGG threads on Palermo**: Cloudflare, not read.
- **No source, Greek or English, publishes a tested six-player setup with two killers plus two town power roles.** Every judgement about six seats below is reasoning from parity, not a citation.

## 1. Sources

| # | URL | What it is | Trust |
|---|-----|-----------|-------|
| R1 | https://palermonights.gr/characters/ | Palermo Nights app, all 27 characters with Greek descriptions (the page has 27, not 26) | High for the app |
| R2 | https://palermonights.gr/faqs/ | Same app: phases, votes, ties, reveals, win conditions, Classic set | High for the app |
| R3 | https://www.newsbeast.gr/entertainment/arthro/12273254/i-nychta-peftei-sto-palermo-kai-alla-paichnidia-choris-exoplismo-gia-na-paixete-oikogeneiaka-stis-giortes | Newsbeast feature: Τσιράκι, Δήμαρχος, Γιατρός, endgame at 4 and 3, 7+ players | Medium-high |
| R4 | https://www.all4fun.gr/portal/afierwmata/4411-peftei-i-nyxta-sto-palermo.html | all4fun feature: Τσιράκι, Δήμαρχος, Γιατρός, endgame; 2024–25 reader comments disputing the 4-player rule | Medium |
| R5 | https://cardgamesgr.blogspot.com/2015/03/palermo2.html | cardgamesgr «Με περισσότερους Ρόλους»: role table 4–24 players, Διεφθαρμένος Αστυνομικός, Πουλημένος Δολοφόνος, Ντετέκτιβ, Συγκάτοικοι, property cards, night scripts | Medium (one author) |
| R6 | http://offtherecordnewsgr.blogspot.com/2015/07/blog-post_53.html | Blog role list: Εταίρα (evil), Νοσοκόμα, Κυνηγός, Δήμαρχος (tie-only) | Medium-low |
| R7 | http://palermopaixnidi.blogspot.com/2013/11/blog-post_25.html | «Παλέρμο by Qbrain»: Εταίρα (good, 8+), 10 described Κάρτες Τύχης, night order | Medium-low |
| R8 | http://palermogame.blogspot.com/2014/04/blog-post.html | Palermo Game Team: Πουτάνα (evil), Μάντης, Άγγελος, no reveal on death, claims not binding | Medium-low |
| R9 | https://mwm.ai/apps/palermo/949582134 | Icy Hippo «ΠΑΛΕΡΜΟ» App Store mirror: role names, 5–30 players | Low (names only) |
| R10 | https://apps.apple.com/gr/app/%CE%BC%CE%AF%CE%B1-%CE%BD%CF%8D%CF%87%CF%84%CE%B1-%CF%83%CF%84%CE%BF-%CF%80%CE%B1%CE%BB%CE%AD%CF%81%CE%BC%CE%BF/id6759204428?l=el | Artemis Codes «Μία Νύχτα στο Παλέρμο»: Κρυφός/Φανερός, Ντετέκτιβ, Γιατρός, Πληροφοριοδότης, Ερωτευμένοι; 5–20 players; one vote per living player | Medium |
| R11 | https://en.wikipedia.org/wiki/Mafia_(party_game) | Reference article: role glossary (Godfather, Vigilante, Jester, Masons, Miller, Roleblocker, Lawyer, Lovers, Bodyguard, Tracker, Watcher, Mayor, Traitor, Witch, Hunter, Bomb, Silencer), ratios, no-lynch, majority vs plurality, ties, minimum players | High |
| R12 | https://eblong.com/zarf/werewolf.html | Plotkin's original Werewolf rules: 7+ players, odd count, two wolves, night start, majority, Seer, Cupid and other variants | High (primary) |
| R13 | https://www.eblong.com/zarf/werewolf-stats.html | Plotkin's simulated human win rates under random lynching by player and wolf count | High (model, stated assumptions) |
| R14 | https://rulespal.com/ultimate-werewolf/rulebook | Ultimate Werewolf rulebook: one wolf at 6–8 players; Bodyguard, Hunter, Mason, Sorceress, Spellcaster, Tanner, Witch; majority vote | Medium-high |
| R15 | https://ultraboardgames.com/the-werewolves-of-millers-hollow/game-rules.php | Werewolves of Millers Hollow rules: Cupid and lovers, Witch, Hunter, Little Girl, Thief, Sheriff (elected, double vote, successor), night order, tie = nobody | Medium-high |
| R16 | https://rulespal.com/one-night-ultimate-werewolf/rulebook | ONUW rulebook: Minion, Tanner, Hunter, Insomniac, Drunk, Masons, voting | Medium-high |
| R17 | https://ultraboardgames.com/one-night-ultimate-werewolf/game-rules.php | ONUW: 3–10 players, role sets for 3–5, Seer/Robber/Troublemaker, voting | Medium |
| R18 | https://epicmafia.com/roles/144 (Godfather), /145 Framer, /150 Lawyer, /146 Hooker, /139 Fool, /154 Survivor, /141 Killer, /127 Tracker, /126 Watcher, /121 Bodyguard, /128 Vigilante, /129 Miller, /136 Mason, /12513 Cupid, /159 Traitor, /15533 Sidekick, /134 Hunter | EpicMafia role cards, exact text | Medium-high (one site's rules) |
| R19 | https://dragonmount.com/forums/topic/62213-basic-roles/ | Forum thread defining "basic" roles; notes on Miller + Godfather, Tracker/Watcher being for power-heavy games | Medium |
| R20 | https://wiki.bloodontheclocktower.com/Setup and https://rulespal.com/blood-on-the-clocktower/rulebook | BotC: 5+ players for Trouble Brewing, 7+ for other scripts; execution needs at least half the living players, ties execute nobody, one execution a day, execution optional | High for BotC |
| R21 | https://mafiarole.com/how-to-play/6-players | Role-assigner site's 6-player page: 1 Mafia, 1 Doctor, 1 Detective, 3 Villagers | Low-medium (hobby site) |
| R22 | https://arxiv.org/html/2407.13943v1 | Werewolf Arena (Google, 2024): 8-player LLM setup, bidding to speak, majority vote, results | High (primary) |
| R23 | https://arxiv.org/html/2510.11389v1 | "Beyond Survival" (2025): WereBench, 15 rule variants, 30 roles; LLMs best as Witch, Seer harder | High (primary) |
| R24 | https://arxiv.org/html/2408.17177v1 | Game-theoretic Werewolf with a prophet: citizen win table by villagers × wolves | Medium (model) |
| R25 | https://arxiv.org/abs/1009.1031 | Braverman, Etesami, Mossel: mafia ∝ √n gives even odds without a detective; parity matters | High (abstract only read) |
| R26 | https://wiki.mafiascum.net/index.php?title=GF and `?title=RB` | MafiaScum Godfather and Roleblocker pages | *Snippet only* (403) |
| R27 | https://forum.mafiascum.net/viewtopic.php?f=5&t=8437 | MafiaScum thread "Help create 6-player setup" | *Snippet only* (403) |
| R28 | https://forums.lusternia.com/discussion/2695/how-to-build-a-mafia-a-guide | Guide with Framer/Lawyer definitions | *Snippet only* (page returned empty) |
| R29 | `palermo/game.py`, `palermo/stats.py`, `palermo/games/*.json` | The engine and 16 finished saved games | Primary for the engine |
| — | https://www.skroutz.gr/s/4307379/… (Kaissa Παλέρμο), https://play.google.com/store/apps/details?id=com.icyhippo.MiaNyxtaStoPalermo, https://beziergames.com/pages/ultimate-werewolf-roles, https://www.ratpack.gr/… | 403 / truncated / 404 / dead | Not read |

## 2. The six-seat arithmetic every judgement rests on

Engine facts (R29): six seats; default `--roles killer=2,officer,doctor` plus two citizens; quiet night 1 (killers meet, officer is shown one killer); `winner()` gives the killers the game when `killers >= alive - killers`; plurality vote; a tie goes to two runoffs, then nobody is out; a voted-out jester ends the game. (The role text at `game.py:112` still tells agents a night victim's role is revealed; the brief says it is not. Worth a check.)

**Two killers.** Day 1 is voted at 6 alive. If a citizen goes out: 5 alive (2K+3T), Night 2 kills one unless the doctor saves, 4 alive (2K+2T), killers win before Day 2 starts. If a killer goes out: 5 alive (1K+4T), Night 2, 4 alive (1K+3T), Day 2 vote, and if that misses, Night 3 leaves 2 alive and the killer wins at parity. So the town has **two votes**, Day 1 among six and Day 2 among four, and must hit a killer on Day 1 (or be saved by the doctor) to see Day 2 at all. Every vote happens at an **even count** (6, then 4), because the quiet night pushes the first death after the first vote. Plotkin's simulation for a 7-seat game (six players plus moderator) with two wolves and random lynching gives humans 13%; at 8 seats 8% (R13). The officer's knowledge of the shown killer is what lifts that.

**One killer.** Votes at 6 and 4, parity at 2: again two votes. The saved games agree: in the 15 finished single-killer games the town won 9, the killer 6, almost all in two days; only two two-killer games ever finished (one each) and seven stopped after Day 1 (R29, `stats.py`).

Consequences used in every row below:

- (a) A tied Day 1 that ends in "nobody out" is a free night for the killers; two such days are a killer win. A tie-breaker is worth more here than at ten seats.
- (b) Any extra evil seat makes three evil of six: Day 1 is 3v3 and the killers can force a tie at will.
- (c) Any role that removes a town seat outside the vote (Lovers, Gambler, Kamikaze, double night kills) ends the game.
- (d) Anything that makes the officer's result unreliable (Godfather, Miller, Framer) removes the town's only edge.
- (e) A role that softens a mislynch (Hunter, Prince, Bulletproof) is a second chance in a game that otherwise has none.
- (f) Majority voting (4 of 6, 3 of 4) lets two killers block every lynch; plurality is the only workable threshold (section 4).

## 3. Roles

### 3.1 Palermo Nights, all 27 characters (R1; win rules R2)

Night order in the app is not published (R2). Teams are the app's own labels.

| Greek (English) | Team | Mechanics (R1 unless noted) | Frequency | Balance at 6 | Drama | Cost | Fit |
|---|---|---|---|---|---|---|---|
| Φανερός Δολοφόνος (Shown Killer) | Evil | Known to the Αστυνομικός from the start; each night confers with the other killer and points out the victim | Core | In engine | — | — | In engine |
| Κρυφός Δολοφόνος (Hidden Killer) | Evil | Unknown to all but the shown killer; joint nightly kill | Core | In engine | — | — | In engine |
| Αστυνομικός (Policeman) | Good | Knows the shown killer from the start; must get them voted out without exposing himself; no nightly check | Core | In engine as `police` | — | — | In engine |
| Βοηθός Αστυνομικού (Police Assistant) | Good | Knows who the policeman is and follows his lead | App-only | Town+: a seat that can certify the officer when a killer counter-claims; at 6 that is 2 of 4 town seats informed | Medium: a public vouch the killers must call a lie | Cheap (one name in the prompt) | Maybe, with `police` (no checks) |
| Πολίτης (Citizen) | Good | No ability, knows nobody | Core | — | — | — | In engine |
| Γιατρός (Doctor) | Good | Each night picks one living player, self allowed; if the killers chose that player, nobody dies | Common | In engine | — | — | In engine |
| Μητέρα Τερέζα (Mother Teresa) | Good | If voted out or removed by an ability, "night never falls again": no more night kills | App-only | Town++: once out, the killers can only win votes they lose 2v3; a town seat that wants to be lynched; killers must counter-claim | Medium: a self-lynch claim contest, odd to watch | Cheap (skip `night()` on a flag) | No |
| Αλεξίσφαιρος (Bulletproof) | Good | Cannot die at night; leaves only by vote or ability | Common (R1; card in R7; R9) | Town+: one wasted killer night is one extra day, and the next vote lands on an odd count (5), tie-free | Medium: a "no murder" morning the doctor cannot explain; the killers know whom they hit | Cheap (skip the kill; narrate «χωρίς δολοφονία») | Honourable mention |
| Ερωτευμένοι (Lovers) | Good (both) | A pair who know each other; if one leaves, the other leaves too | App-only in Greek (R1, R9, R10); core in Werewolf (Cupid, R12, R15) | Killer++: the first hit on a lover removes 2 of 4 town seats, instant parity (c) | High: a double funeral | Medium (cascade in `out()`) | No at 6 |
| Φίλοι (Friends) | Good | A pair who know each other and that both are good | App-only in Greek; common in Mafia/Werewolf as Masons (R11, R14, R16) | Town+: two mutually confirmed townies plus the officer leaves one unknown town seat; fake claims die to the real pair's counter-claim | Medium: a vouch pair hardens votes fast, games get shorter | Cheap (names in prompt) | Only with one killer |
| Ρουφιάνος (Snitch, PN sense: evil) | Evil | Knows both killers; protects them by misleading; no kill | Common as a family (Τσιράκι R3/R4, Εταίρα R6, Πουτάνα R8, Minion R16, Traitor R11/R18) | See the Τσιράκι row in 3.2 | | | |
| Πληρωμένος Δολοφόνος (Paid Killer) | Evil | Knows both killers; after their kill, opens eyes and kills another; same target = one death, else two | App-only | Killer+++: 6 to 3 after one night | High, once | Medium | No |
| Δικηγόρος (Lawyer, PN sense) | Evil | Knows only the shown killer; defends them without being exposed | App-only | A lighter Τσιράκι; same 3-of-6 problem (b) | | | No at 6 |
| Τρέλα (Madness) | None | Plays alone; goal is to be voted out; if voted out, identity revealed and the game ends | App-only (R1, R9); common elsewhere as Jester/Fool/Tanner | In engine. At 6 with two killers a Day-1 jester lynch is 5 alive (2K+3T), Night 2, 4 alive, killers win: the jester soaks the town's only spare vote (a). EpicMafia's Fool "Wins the game upon being lynched" but play continues and the Fool may instead win with town for fewer points (R18); ONUW: if a Tanner and a wolf both die, the village also wins (R16) | High | Cheap change: jester wins, game continues | Change, don't remove |
| Κλόουν (Clown) | With Τρέλα | Knows the Τρέλα and tries to get it voted out | App-only | Two of six seats outside the team game | Low | Cheap | No |
| Άρρωστος (Sick) | Good | Contagious; immediately on dying may infect one player, who dies too; if declined, never | App-only | Swingy: a Hunter that also fires on a night death; a wrong pick is two town seats gone (c) | High | Cheap | Prefer Κυνηγός |
| Στρατιώτης (Soldier) | Good | Once per game, by day, shoots a player who leaves immediately; R2: good also win if the soldier is left with one killer | App-only; cf. one-shot Vigilante (R11) | Swingy: a right shot removes a killer without a vote; a wrong one costs a town seat on a table that cannot spare it (c). AI agents fire early | Very high (a live shooting) | Cheap (day action with TARGET) | Maybe, Day 2 onward only |
| Καμικάζι (Bomber) | Evil | Knows the killers; any day may detonate: picks one good player who dies, and leaves too | App-only (R1, R9) | Killer++: a third evil seat that trades 1-for-1 into parity (b, c) | High, once | Cheap | No |
| Τζογαδόρος (Gambler) | Good | Day 1 only, optional: name a player; if a killer, their identity is revealed to the gambler; otherwise the gambler dies | App-only | At 6: 2-in-5 to become a second officer, 3-in-5 to hand the killers a free seat on Day 1 (c); negative expectation | High: a coin flip on camera | Cheap | No |
| Δήμαρχος (Mayor) | Good | By day may activate: identity revealed to everyone at once; from then on the vote counts double | Common: R1 reveal-to-activate; R3/R4 chosen openly before the deal, double on every vote; R6 hidden, double only in ties; R9 listed; R11 Mayor "elected each morning", two votes; R15 Sheriff elected, double vote, names a successor; UW Mayor counts as two (*snippet*) | Town+: every engine vote is at an even count; the mayor turns a 3v3 Day 1 into 4v3 and a 2v2 into 3v2 (a); code-certified, so a killer cannot fake the activation | High: a public claim with a stamp on it, and a new night target competing with the officer for the doctor | Cheap (vote weight 2 after a flag) | **#1** |
| Ντετέκτιβ (Detective, PN) | Good | Once per game, picks a player and learns their team | App-only; R5 has a nightly one from 12 players | A one-shot officer: the compromise if nightly checks feel too strong at 6 | Medium | Cheap | Alternative to `officer` |
| Τρελός Επιστήμονας (Mad Scientist) | None | Each night experiments on one player; wins if alive when every living player has been experimented on | App-only | Needs three or more nights; six-seat games last two | Low (invisible) | Medium | No |
| Μάγος (Magician) | Evil | Once, by day but not Day 1: everyone falls asleep, straight to night, no vote that round | App-only | Killer++: a skipped vote at 6 is a free kill into parity (a) | High | Cheap | No |
| Γείτονας (Neighbour) | Good | A citizen told two names from the start: one is the shown killer, the other an ordinary citizen; does not know which | App-only | Town+ but soft: narrows five suspects to two and cross-checks the officer's steering; partial, so claims stay arguable | Medium-high: a citizen seat with something true and risky to say | Cheap (two names in the prompt) | **#5** |
| Προδότης (Traitor, PN) | Good, may turn | During any day may switch to the evil team and learns the killers; changes the count | App-only | Chaotic: at 6 a switch is 3v3 (b); AI agents would switch when losing | High | Medium | No |
| Πολίτης με σκύλο (Citizen with Dog) | Good | Linked to the Dog: if the owner dies the dog dies; the dog dying first changes nothing | App-only | One-way Lovers: two seats on one hit (c) | Medium | Medium | No |
| Σκύλος (Dog) | Good | As above | App-only | As above | | | No |

### 3.2 Other Greek roles (R3–R8, R10)

| Greek (English) | Team | Mechanics | Source, frequency | Balance at 6 | Drama | Cost | Fit |
|---|---|---|---|---|---|---|---|
| Τσιράκι (Henchman / accomplice; Ντάμα) | Evil | Opens eyes after the ρουφιάνος on night 1 and sees both killers; «βλέπει τους δολοφόνους στην πρώτη νύχτα, αλλά αυτοί δεν τον ξέρουν» (Newsbeast, R3); helps them while in the game (R4); cannot kill; wins with them. Same shape as ONUW's Minion, who sees the wolves while "the Werewolves don't learn who the Minion is" (R16), and Mafia's Traitor, which "Does not count toward mafia's majority win condition" (EpicMafia, R18) | R3, R4 (Τσιράκι); R6 Εταίρα; R8 Πουτάνα; R1 Ρουφιάνος/Δικηγόρος; R16 Minion; R11/R18 Traitor. Common | With two killers it is three evil voters of six: Day 1 is 3v3 and the killers force a tie whenever they want (b); even if the Τσιράκι does not count for parity (R18) the evil side controls Day 2 at 5 alive (3v2). Replacing the second killer (1 killer + Τσιράκι) is playable: 4 town votes v 2, one kill a night, the Τσιράκι's job is to counter-claim the officer; but then there is no shown killer for `police` | Very high: two liars with different knowledge; the killer may even kill the helper it does not know | Cheap (prompt; exclude from the kill vote; count as town for parity) | Not with two killers; `killer=1,accomplice` as an experiment |
| Εταίρα, good version | Good | Added at 8+ players; on night 1 sees both killers and the informer; steers the town like a second informer | R7 (one source) | Too much town information next to an officer | Medium | Cheap | No (and R7 says 8+) |
| Πουτάνα | Evil | Night 1: sees the hidden killer (the ρουφιάνος sees the shown one); by day protects the killers; town wins only when both killers **and** she are out | R8 (one source) | A Τσιράκι the town must also lynch: three lynches in a two-vote game | High | Cheap | No |
| Κυνηγός (Hunter) | Good | May kill one player, only by day and only when voted out; takes them along; hidden until then (R6). Werewolf's Hunter fires on any death (R15), or on a night death with talk stopped until he chooses (R14); EpicMafia's "When lynched, is awarded the ability to kill" (R18); Wikipedia's Woodcutter (R11) | R6 (one Greek source); common in Werewolf and Mafia | Town+ with teeth: a mislynched hunter who heard the officer steer shoots the shown killer, so a Day-1 miss stops being fatal (e); a wrong shot is two town seats in one day and the game, so the vote carries double stakes | Very high: last words, then a shot | Cheap (TARGET in the last-words prompt, `out()` twice) | **#2** |
| Νοσοκόμα (Nurse) | Good | Each night tells the previous victim whom she saves; never herself | R6 | = doctor without self-save (section 4) | | | Variant of doctor |
| Δήμαρχος, tie-only | Good | Hidden; vote counts double only in a tie; only the final result is announced | R6 | A silent tie-breaker: fixes (a) without the claim | Low | Cheap | Fallback for #1 |
| Μάντης (Seer), Άγγελος (Angel) | Good | Nightly check of a suspect; nightly protection before the killers act | R8 | = officer with checks, = doctor | | | In engine |
| Διεφθαρμένος Αστυνομικός (Corrupt Policeman) | Wins with killers | Reads as Citizen to the Ντετέκτιβ; known to the killers; knows the shown killer | R5, 12+ players | A Godfather-flavoured Τσιράκι; (b) and (d) | High | Cheap | No |
| Πουλημένος Δολοφόνος (Sold Killer) | Wins with town | Reads as Killer to the Ντετέκτιβ; knows the shown killer; unknown to all | R5, 12+ players | A Miller who knows a killer; the false guilty decides a six-seat game (d) | High | Cheap | No |
| Συγκάτοικοι (Cohabitants) | Good | Two players who look at each other on night 1 | R5, 15+ | = Φίλοι / Masons | | | See 3.1 |
| Ντετέκτιβ, nightly | Good | Points at one player a night; narrator nods yes or no | R5 (12+), R8 | = engine `officer` | | | In engine |
| Property cards («Φύλλα Ιδιότητας» R5, «Κάρτες Τύχης» R7) | Any holder | One-shots dealt beside the role: Έξτρα Ψήφος, Ακύρωση Ψήφου, Άμεση Καταγγελία (lynch without a vote), Ακύρωση Καταγγελίας, Εξαίρεση από ψηφοφορία, Ανάσταση, Αλεξίσφαιρο, Φωνή από το Υπερπέραν / Τυμβωρυχία (dead vote or reveal a night victim), Κρυστάλλινη Σφαίρα, Όνειρο (one yes/no question to the narrator), Μπλόφα/Τίποτα. R5 deals only the five vote cards at 7–11 and none at 4–6 | R5, R7 (two sources, the Criminalita lineage) | Each vote card is a hidden Mayor; Άμεση Καταγγελία decides the game outright; R5 itself leaves them out below 7 | High | Medium (a card system) | Not at 6; Όνειρο alone would be cheap and fun |

### 3.3 Mafia family (R11, R18, R19, R26, R28)

| Role | Team | Mechanics | Frequency | Balance at 6 | Drama | Cost | Fit |
|---|---|---|---|---|---|---|---|
| Godfather | Mafia | "Appears innocent on cop reports" (R18); leads the mafia (R11); R26: exclusive to mafia, Ninja variant hides from Tracker/Watcher instead; R19: too powerful for basic games, never with a Miller | Common | Killer++: the hidden killer reads innocent, so the officer ends up vouching for a killer (d); with `police` (no checks) it does nothing | High: the confident wrong vouch | Cheap | No |
| Lawyer | Mafia | "Visits one mafia member every night. That person will appear innocent" (R18); R11 also has a Lawyer who saves the top-voted player once | Common | Active Godfather; (d) | Medium | Medium | No |
| Framer | Mafia | Visits one player who "will appear guilty on cop reports that night" (R18; R28) | Common | Killer+++: one false guilty, one officer claim, one mislynch, game over (d) | Very high, once | Medium (frame before check) | No, except as a rare announced twist |
| Roleblocker / Hooker | Either | Blocks one player's night action; passives unaffected; blocked one-shots still count as used (R26); EpicMafia Hooker (R18) | Common | Killer++: the two killers neutralise both town night powers while still killing | Low (invisible) | Medium (resolution order) | No |
| Bodyguard | Town | Dies in place of the protected player, "sometimes killing the attacker" (R11); EpicMafia 50/50 (R18); UW: not the same player twice, never self (R14) | Common | A doctor that pays a seat per save: killer+ unless the attacker dies, then a vigilante with a trigger | Higher than doctor | Cheap (swap doctor) | Only the attacker-dies version |
| Vigilante | Town | Kills one player a night (R11); EpicMafia: dies if visiting the mafia's target (R18); one-shot variants (R11) | Common | Nightly: a wrong shot is fatal at 6; one-shot = Στρατιώτης | High | Cheap | One-shot at most |
| Tracker / Watcher | Town | Tracker learns whom a player visited; Watcher learns who visited a player (R11, R18); R19: for power-heavy games | Common | Town++: the only visitors at 6 are the killer, doctor and officer; a Watcher on the victim names the killer | Medium: talk is deductive, not revelatory | Medium (visit model) | Only instead of nightly checks |
| Masons | Town | Know each other and that both are innocent; no powers (R11, R14, R16); EpicMafia's recruiting version (R18) | Common | = Φίλοι | | | See 3.1 |
| Miller | Town | Innocent who reads guilty; "Appears as villager to self" (R18); R19: an anti-town role, dangerous with new players | Common | One false guilty decides a six-seat game (d). As a disclosed rule ("a citizen may read as a killer") it makes officer claims arguable instead of auto-trusted | High | Cheap | Only disclosed, and only if claims are too trusted |
| Jester / Fool / Tanner | None | Wins on being lynched; ToS version may kill one voter after (R11); EpicMafia play continues (R18); ONUW Tanner (R16) | Common | See Τρέλα | | | Change: continue the game |
| Survivor | None | Wins if alive at the end; hides with a non-visiting player (R18) | Common | A kingmaker vote that counts as town for parity; the killers must spend a night on it | Medium | Cheap | Meh |
| Serial Killer | Solo | Kills nightly; "Wins if alive alone or among the final two" (R18); R19: the one basic role with its own win | Common | A second killing seat: 6 to 3 in one cycle (c) | High | Medium | No |
| Cupid / Lovers | Varies | Cupid pairs two on night 1; one dies, both die; EpicMafia Cupid wins if both survive (R18); MH cross-team lovers win alone (R15) | Common | See Ερωτευμένοι (c) | | | No |
| Traitor | Mafia-aligned | Does not wake with the mafia, reads innocent, wins only if the mafia wins (R11); "Mafia does not know who Traitor is" and no parity count (R18) | Common | The cleanest Τσιράκι template | | | See 3.2 |
| Mayor | Town | Elected each morning in some variants; two votes (R11) | Common | See Δήμαρχος | | | **#1** |
| Hunter / Woodcutter | Town | Takes one player along on death (R11, R18) | Common | See Κυνηγός | | | **#2** |
| Bomb / Veteran | Town | Anyone who targets them at night dies (R11) | Less common | A killer dies on their first hit: town++ swing with no decision in it | High, once | Cheap | No (luck, not play) |
| Silencer / Prostitute | Mafia-aligned | The target cannot speak (and in one version cannot vote) next day (R11) | Less common | A skipped speaking turn for an AI seat; evil+ | Low-medium | Cheap | No |

### 3.4 Werewolf family (R12, R14–R17)

| Role | Team | Mechanics | Frequency | Balance at 6 | Drama | Cost | Fit |
|---|---|---|---|---|---|---|---|
| Seer | Village | Nightly thumbs up/down; may reveal at any time (R12) | Core | = `officer` | | | In engine |
| Cupid | Village | Pairs two lovers on night 1, may include self; lovers cannot vote each other; a wolf-villager pair wins by outliving everyone (R15, R12) | Core | (c) | High | Medium | No |
| Witch | Village | One healing potion, one poison, each once; is shown the victim and may heal; may poison at night; may target herself; a night can end with 0, 1 or 2 deaths (R15); UW: after using either, no longer learns the target (R14); Wikipedia: single-use revival (R11) | Core in MH/UW | As the doctor's replacement: one certain save (she sees the hit), one kill, plus the nightly name of the killers' target, which is a confirmed innocent; roughly doctor-equal in saves, plus a one-shot vigilante. WereBench found LLMs play the Witch best of all roles (R23) | High (poison!) | Medium (two one-shots, night order) | **#4** |
| Hunter | Village | On being killed or lynched, immediately eliminates one player (R15); UW: on a night death, nobody talks until he chooses (R14) | Core | See Κυνηγός | | | **#2** |
| Little Girl | Village | May peek during the wolves' turn; if caught, dies instead of the victim (R15) | Core in MH | A random peek; for agents a probability roll, not play | Medium | Cheap | No |
| Thief | Village | Swaps with one of two centre cards on night 1 (R15) | MH | No centre cards here | | | n/a |
| Sheriff / Captain | Any | Elected by the village; vote counts as two; names a successor on death (R15) | Core in MH | The elected Mayor: a Day-1 election with campaign talk the killers can win; electorate 4v2 so usually town+ | Very high | Medium (one extra vote round) | Alternative to #1 |
| Minion | Werewolf | Sees the wolves; they do not learn him; wins if no wolf dies, even if he dies (R16) | Core in ONUW | = Τσιράκι | | | See 3.2 |
| Tanner | None | Wins if lynched; "If the Tanner wins, all other teams lose" (UW, R14); ONUW: village also wins if a wolf dies with him (R16) | Core | = Τρέλα | | | See 3.1 |
| Masons | Village | See each other (R14, R16); UW: anyone who mentions them is eliminated | Core | = Φίλοι | | | See 3.1 |
| Sorceress | Werewolf | Hunts the Seer for the wolves, does not know the wolves (R14) | UW | An evil seat whose whole job is finding the officer: killer+ (b) | Medium | Cheap | No |
| Spellcaster | Village | Silences one player a day, never the same twice (R14) | UW | = Silencer | | | No |
| Bodyguard (UW) | Village | Protects; not the same player twice; not self (R14) | UW | See 3.3 | | | |
| Apprentice Seer | Village | Becomes the Seer when the Seer dies | *Snippet* | Defeats "kill the officer" at 6: town+ | Medium ("the officer is dead, long live…") | Cheap | Thin source; maybe |
| Prince | Village | Survives a lynching and reveals the role | *Snippet* | A one-time mislynch immunity (e): town+ | Medium (the vote fails) | Cheap | Thin source; maybe |
| Robber, Troublemaker, Insomniac, Drunk | Village | Card swapping in the single ONUW night (R16, R17) | ONUW | No multi-night equivalent | | | n/a |

## 4. Rule variants

| Variant | Mechanics and sources | Frequency | Balance at 6 | Drama | Cost | Fit |
|---|---|---|---|---|---|---|
| No-lynch option | The town may choose not to eliminate anyone; Wikipedia: typically favours the Mafia, except when the survivors are even in number (R11); BotC: execution optional (R20); UW: if the day's timer runs out, straight to night (R14); engine: a double tie is a no-lynch by the back door (R29) | Common in Mafia; absent in Greek sources | Every skipped vote is a free kill; two skipped days are a killer win (a) | Low (nothing happens) | Cheap | Don't add; also remove the "nobody out" fallback (see Ties) |
| Majority vs plurality | Greek: most votes is out (R2, R3, R5, R8; PR-S1/S8); Plotkin and UW: majority (R12, R14); BotC: at least half of the living (R20); Wikipedia: standard "over half", Davidoff plurality (R11); Werewolf Arena: majority (R22) | Both common | Majority at 6 is 4 of 6, 3 of 4: two killers plus one confused townie block every lynch (f). BotC's half-threshold still lets 2 killers execute at 4 alive while 2 townies only tie | Majority makes Day 1 a negotiation; plurality makes it a count | Cheap | Keep plurality |
| Day-start vs night-start | Plotkin: night first and an odd count, so the game ends on a lynch (R12, R11); Greek: identification night, first vote before the first murder (R3, R4, R5; PR-S1/S8); PN: starts with Day (R2); engine: quiet night 1 (R29) | Both common | With two killers a Night-1 kill leaves 5 alive (2K+3T) and one vote before parity, so the quiet night is mandatory. With one killer a Night-1 kill is survivable and moves the votes to odd counts (5, 3), tie-free | Day 1 with no information is the part people dislike (PR-S12, S23); a Night-1 death gives Day 1 a topic | Cheap (flag exists: `--kill-night1`) | Keep quiet night with 2 killers; try `--kill-night1` with 1 killer |
| Votes-only endgame at 4, final vote at 3 | With 2 killers, informer and one citizen left, nights stop and only votes remain; citizen or informer out = killers win; at 3 (1 killer, informer, citizen) the vote decides and voting out the citizen is «ισοπαλία» (R3, R4); R4's commenter Ορέστης: it is simply a 2v2 tie | Two Greek sources; disputed in R4's comments | Town+: the engine's two automatic parity losses (2K+2T, 1K+1T) become votes; 2v2 needs a tie-breaker (Mayor or lot) or the AIs deadlock | High: a last stand instead of a narrated loss | Cheap (skip `night()` when alive is 4 with 2 killers or 3 with 1; declare the draw) | **#3** |
| Killing the police ends the game | Classic: killers win the moment the ρουφιάνος is out (R3; PR-S6/S9; R4 default, which notes some groups drop it). Opposite in Palermo Nights: the good side wins if the policeman or soldier is left alone with one killer (R2) | Both common, contradictory | Classic at 6: the hidden killer gets a 1-in-4 instant win on Night 2, and the officer who steered Day 1 is guessable: killer++. PN's rule removes the killers' parity win while the police lives, so they must hunt the police through the doctor: town+ and one more decision per night | Classic: the officer's claim becomes a real gamble. PN: a manhunt | Cheap either way | PN rule as a flag at 6; classic only on bigger tables |
| Ties | Greek: revote among the tied until someone changes (R5; PR-S1/S8); R8: cancel and talk more; PN: discuss again (R2); MH: nobody out (R15); ONUW: all tied players die (R16); BotC: neither executed (R20); Wikipedia: by lot or a scapegoat role (R11); engine: two runoffs then nobody (R29) | All over the map | At 6 every vote is at an even count (section 2), so ties are structural; "nobody out" twice is a killer win (a). AI agents rarely flip in a runoff | A forced flip is the story of the day; a lot is not | Cheap | Break ties: Mayor first, then lot; never nobody |
| Night victim's role hidden | R2, R5, R7, R8; PR-S1/S10; engine per brief | Core in Greek | Already adopted | | | Check `game.py:112` text |
| No reveal at all (lynch either) | Voted-out player leaves without showing the card; may lie in last words (R8; also R5) | Two Greek sources | The town never learns if it hit a killer, parity stays hidden, killers cannot be counted; viewers know, players don't | Medium-high, but AI claims become unverifiable for everyone | Cheap | Risky; try once as a flag |
| Doctor limits | No self-save (R5 "other than themselves"; R6 Nurse); not the same target twice (R11; UW Bodyguard R14); the save is announced only as «χωρίς δολοφονία» (R3, R5) | Common | Self-save makes the doctor unkillable at night, so the killers must lynch them: fine for drama; no-self makes saves rarer and games shorter | Medium | Cheap (flag exists: `--no-self-save`) | Keep self-save at 6 |
| Odd player count | Plotkin: odd is best, even games end on a night murder and weaken the humans (R12) | Core in Werewolf | Six is even and the quiet night puts every vote at 6 then 4; the Mayor (#1) or a Night-1 kill with one killer restores odd votes | — | — | Handled by #1 |
| Sheriff election | Elected by vote at the start; double vote; names a successor (R15) | Core in MH | See 3.4 | | | Alternative to #1 |
| One-shot property cards | See 3.2 (R5, R7) | Two sources | Not below 7 even in R5 | | | No |
| First dead narrates | PN: the first player out runs the night (R2); folk: the previous victim is shown the kill (R4, R6) | App and folk | n/a (the GM is code) | — | — | n/a |
| Speaking order by bidding | Werewolf Arena: agents bid 0–4 for the next turn; ties random, weighted toward players just mentioned (R22) | AI-only | Not a balance lever; a pacing one | Medium: heated exchanges get the floor | Medium | Outside this brief |

## 5. Six-player setups found in sources

| Source | Setup at six | What it says about balance |
|---|---|---|
| R5 cardgamesgr, 4–6 players | Δολοφόνος Β (one, shown), Ρουφιάνος, 2–4 Πολίτες; no narrator, no property cards; "play as classic Palermo" | One killer only; the two-killer game starts at 7 with a doctor |
| R1/R2 Palermo Nights Classic, 5+ | 2 killers, 1 policeman (shown one killer, no checks), 3 citizens; no doctor | «Προτείνεται για αρχάριους» (R2) |
| R21 mafiarole.com | 1 Mafia, 1 Doctor, 1 Detective, 3 Villagers | "the smallest balanced setup with breathing room" (mafiarole.com) |
| R14 Ultimate Werewolf first game | 1 werewolf for 6–8 players, 1 Seer, rest Villagers | Two wolves only from 9 players |
| R12 Plotkin | At least seven, nine or eleven better; two wolves; odd count | Even counts favour the wolves |
| R13 Plotkin's simulation | Random lynching, seer ignored: 7 seats incl. moderator: 1 wolf 47%, 2 wolves 13% human wins; 6 seats: 25% and 0% | A floor for "completely stupid" humans; two wolves at six-ish seats is near hopeless without information |
| R24 Werewolf with a prophet | 4 villagers + prophet + 1 wolf (six seats): citizens 70% with the best reveal round; + 2 wolves (seven seats): 35% | A seer-type role is worth far more than a villager; two wolves halve the town's odds |
| R25 Braverman et al. | Even odds when mafia ∝ √n without a detective; parity of n matters | Asymptotic; not a six-seat statement |
| R11 Wikipedia | Minimum six players (ten for classic); Davidoff ~1/3 mafia; Plotkin exactly two | Six is the floor, not a recommendation |
| R20 Blood on the Clocktower | Five or more for Trouble Brewing; every seat has a character; run games with 5–10 players first; other scripts unfair at 5–6 | Small tables work only with the tamest script; the per-count table was not readable |
| R17 ONUW | 3–10 players, always two werewolves plus three centre cards, one night, one vote | A different game: one vote decides |
| R22 Werewolf Arena (LLM agents) | 8 players: 1 Seer, 1 Doctor, 2 Werewolves, 4 Villagers; majority vote; self-play 40–60% villager wins; villagers 1.2% with no talk, 100% with an always-believed Seer | The nearest published AI setup; two wolves need eight seats and a doctor to sit near 50% |
| R27 MafiaScum thread (*snippet*) | — | "balancing a genuine Mafia game with only 6 players is tricky" (forum poster) |
| R10 Artemis app | 5–20 players; roles switched on or off per count | No table published |
| R29 our saved games | 1 killer + officer + doctor + 3 citizens: town 9, killer 6, games 1–3 days; 2 killers + officer + doctor + 2 citizens: 1–1 finished, 7 stopped after Day 1 | Two-killer data is too thin to judge; single-killer sits near 60/40 town |

Pattern: every published six-seat setup has **one** evil seat, or two with a shown-only police and no doctor. Nobody publishes two killers plus a checking officer plus a doctor at six; the engine's default is denser in power than any source, which is what keeps a ~10% random baseline playable.

## 6. Top 5 for our game, ranked

1. **Δήμαρχος with reveal-to-activate (R1), replacing one citizen.** Every engine vote happens at an even count (6, then 4), so a 3v3 Day 1 and a 2v2 endgame are the normal case, and a tie resolved as "nobody out" is a killer win (section 2a). A code-certified double vote fixes exactly that, and the activation is a public claim no killer can fake. Five Greek sources have some mayor (R1, R3, R4, R6, R9); Millers Hollow's elected Sheriff (R15) is the louder alternative if an extra election round is affordable. Balance town+, drama high, cost cheap.
2. **Κυνηγός / Hunter, fires on being voted out (R6, R18; on any death in R15), replacing a citizen.** At six seats a Day-1 mislynch is the game; a lynched hunter who heard the officer steer gets one informed shot, so the town's one mistake stops being fatal, while a wrong shot is a two-seat disaster. That is the right kind of stakes for a two-day game. Cost is one TARGET in the existing last-words prompt. Prefer the vote-only trigger (Greek) to keep nights simple.
3. **Votes-only endgame at 4 and a final vote at 3 (R3, R4), with ties broken by the Mayor and then by lot.** Turns the two automatic parity losses into last-stand votes, adds one or two decisive days to a game that currently ends on a narration, and is Greek-native. Cheap: skip `night()` at the two counts and declare the draw case.
4. **Μάγισσα / Witch in place of the doctor (R15, R14).** One certain save (she sees the hit first), one poison, and the nightly name of the killers' target, which is a confirmed innocent she can quietly use. More decisions and less guaranteed stalling than a nightly doctor, a town-side kill the killers must fear, and the one role LLMs were measured to play best (R23). Medium cost: two one-shots and a night order (killers, then witch).
5. **Γείτονας / Neighbour (R1) as the citizen upgrade.** Two names, one the shown killer and one a citizen, unknown which. Gives a vanilla seat something true to say on Day 1, cross-checks the officer without duplicating him, and stays arguable because it is partial. One source only (the app), but it is Palermo-branded and costs two names in a prompt.

Two line-ups to try, both untested and my own composition: **A, Palermo**: killer ×2, `police` (shown only) or `officer`, mayor, hunter, neighbour, no vanilla citizen. **B, Mafia**: killer, accomplice (Τσιράκι counted as town for parity, killer does not know them), officer, witch, mayor, citizen.

Honourable mentions: Palermo Nights' "police alive with one killer means the good side wins" (R2) as the six-seat form of the officer-death rule; Αλεξίσφαιρος (R1, R7, R9) for one tie-free extra day; Φίλοι/Masons with a single killer; and changing the jester so its win does not end the game (R18).

## 7. Not for six seats, one line each

Τσιράκι beside two killers (3v3 Day 1, b); Lovers, Dog, Άρρωστος, Gambler (a seat lost outside the vote, c); Paid Killer, Serial Killer, Kamikaze, Magician (a second kill or a skipped vote into parity); Godfather, Lawyer, Framer, Miller, Corrupt Policeman, Sold Killer (the officer's result is the town's only edge, d); Roleblocker (both town night powers gone, invisibly); Tracker/Watcher beside an officer (too much information); Mother Teresa, Traitor-switch, Mad Scientist, Clown (odd incentives or too slow for a two-day game); no-lynch and majority voting (free nights for the killers, a, f); a Night-1 kill with two killers (one vote before parity).
