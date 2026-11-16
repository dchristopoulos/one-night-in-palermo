# Palermo (Πέφτει η νύχτα στο Παλέρμο): how real groups play it

Research notes, 2026-10-23. Read-only survey of Greek-language sources first, then the English Mafia/Werewolf references, then a comparison with the engine in `palermo/game.py`. Every claim carries the URL it rests on. Where sources are thin or disagree it says so. No source below is invented; three pages that would have been useful could not be read (see the end of the Sources table).

Naming: the game is almost always called **«Πέφτει η νύχτα στο Παλέρμο»** (also «Η νύχτα πέφτει στο Παλέρμο»), shortened to **Παλέρμο**. Greek Wikipedia has only a one-line disambiguation entry and no article: «Ένα παιχνίδι που παίζεται συνήθως με τράπουλα και μοιάζει με το γνωστό παιχνίδι "Μαφία"» ([el.wikipedia.org](https://el.wikipedia.org/wiki/%CE%A0%CE%B1%CE%BB%CE%AD%CF%81%CE%BC%CE%BF_(%CE%B1%CF%80%CE%BF%CF%83%CE%B1%CF%86%CE%AE%CE%BD%CE%B9%CF%83%CE%B7))). English Wikipedia notes the game spread through Europe in the 1990s under the name *City of Palermo* ([en.wikipedia.org](https://en.wikipedia.org/wiki/Mafia_(party_game))).

---

## 1. Sources

| # | URL | Lang | What it is | Trust |
|---|-----|------|-----------|-------|
| S1 | https://cardgamesgr.blogspot.com/2014/03/blog-post_3402.html | el | «Πέφτει η νύχτα στο Παλέρμο», classic rules written as a rulebook by hobby blogger aeon_02, 23 Mar 2014; has reader Q&A in comments | **High** for the classic card-deck game: most complete, internally consistent, copied by later guides (S8) |
| S2 | https://cardgamesgr.blogspot.com/2015/03/palermo2.html | el | Same blogger, «Με περισσότερους Ρόλους» (4–24 players, role table by player count, full night script), 28 Mar 2015 | Medium: one author's elaborate variant, but the only Greek source with a per-player-count table |
| S3 | https://www.newsbeast.gr/entertainment/arthro/12273254/i-nychta-peftei-sto-palermo-kai-alla-paichnidia-choris-exoplismo-gia-na-paixete-oikogeneiaka-stis-giortes | el | Mainstream news site, family-games feature; full rules incl. night script, endgame, optional doctor/henchman/mayor | Medium-high: mainstream, agrees with S1 |
| S4 | https://www.all4fun.gr/portal/afierwmata/4411-peftei-i-nyxta-sto-palermo.html | el | 2015 feature by Κυριάκος Κουρουτσαβούρης: a real ~20-player session plus rules; reader comments argue about the endgame | Medium: session report, explicit that variants are «πάρα πολλές» |
| S5 | https://www.pillowfights.gr/oso-pataei-i-gata/i-nixta-peftei-sto-palermo/ | el | Lifestyle article by Άντρεα Λαζαρίδου, 9 Nov 2024: history, night script with «αστυνομικός», why it «έχει κλείσει σπίτια» | Medium: journalistic, light on mechanics |
| S6 | https://kidsproject.gr/articles/470/impostor-sto-palermo-hdh-eteron | el | Parenting site, Palermo vs Among Us; rules with «αστυνόμος» (the ace), win conditions | Medium |
| S7 | http://offtherecordnewsgr.blogspot.com/2015/07/blog-post_53.html | el | Blog post by Μαρκόπουλος Θωμάς, 31 Jul 2015: role list (2–3 killers, informer, courtesan, nurse, hunter, mayor) | Medium-low: role list only, no script |
| S8 | https://www.neotitafokid.gr/2021/01/blog-post_1.html | el | Youth office of the Metropolis of Fokida, 27 Jan 2021, filed under games for primary/high school; reproduces the S1 rules | Medium: shows what gets handed to kids' groups |
| S9 | https://sxeseis.forumgreek.com/t290-topic | el | Forum admin post «Παλέρμο (Οδηγίες / Κανόνες)», 3 Mar 2011: night script verbatim, history (Davidoff 1986) | Medium-low: single post, no replies |
| S10 | http://palermopaixnidi.blogspot.com/2013/11/blog-post_25.html (index: http://palermopaixnidi.blogspot.com/) | el | «Παλέρμο by Qbrain», Nov 2013: a fan print-and-play with Informer, Courtesan (8+), 14 «Κάρτες Τύχης» | Medium-low: one person's product, but reflects the commercial «Criminalita» family (S24) |
| S11 | http://palermogame.blogspot.com/2014/04/blog-post.html | el | «Palermo Game Team», 8 Apr 2014: rules with Ρουφιάνος + Πουτάνα, no reveal on death, 11+ players | Medium-low: one group's house rules, very explicit about day procedure |
| S12 | https://arkoudos.com/blog/?p=4988 | el | Personal blog; one-paragraph description (police «κάνει έρευνες», doctor «αν η παρέα είναι αρκετά μεγάλη»); author hated the game | Low-medium: useful as a critic's view |
| S13 | https://palermonights.gr/faqs/ | el | FAQ of the «Νύχτες στο Παλέρμο» app (Palermo Nights): phases, votes, ties, reveals, dead players, win conditions | High for the app's rules; medium as evidence of folk play |
| S14 | https://palermonights.gr/characters/ | el | Same app, all 25+ characters with Greek descriptions | Same |
| S15 | https://palermonights.gr/ | el | Same app, homepage («Δεν χρειάζεται αφηγητής») | Same |
| S16 | https://apps.apple.com/app/id1558515349 | en/el | App Store listing of Palermo Nights (Konstantinos Apostolakis): Classic = 2 killers, 1 police, rest citizens; 5+ players; first dead = Night Narrator | High for the app |
| S17 | https://mwm.ai/apps/palermo/949582134 | el | Mirror of the App Store page of «ΠΑΛΕΡΜΟ» by Icy Hippo G.P., first released 18 Dec 2014, 5–30 players; role names (Δήμαρχος, Ερωτευμένοι, Καμικάζι, Αλεξίσφαιρος, Ρουφιάνος, Τρέλα, Εκδικητής, Μητέρα Τερέζα) | Medium: store blurb, no rules |
| S18 | https://apps.apple.com/gr/app/%CE%BC%CE%AF%CE%B1-%CE%BD%CF%8D%CF%87%CF%84%CE%B1-%CF%83%CF%84%CE%BF-%CF%80%CE%B1%CE%BB%CE%AD%CF%81%CE%BC%CE%BF/id6759204428?l=el | el | «Μία Νύχτα στο Παλέρμο» (Artemis Codes), 5–20 players: Κρυφός/Φανερός Δολοφόνος, Ντετέκτιβ who knows the Φανερό, Γιατρός, Πληροφοριοδότης, Πολίτης, Ερωτευμένοι | Medium |
| S19 | https://apps.apple.com/us/app//id953539579 | el | «Μια Νύχτα στο Παλέρμο» (Kyriakos Leivadas), 5–75 players on one device, self-described port of Davidoff's game | Low: no rules in listing |
| S20 | https://www.efsyn.gr/nisides/207642_epese-i-nyhta-sto-palermo | el | Efsyn interview (17 Aug 2019) with novelist Σταυριανός Κιναλόπουλος about a book built on the game | Low for rules, good for flavour |
| S21 | https://www.youtube.com/watch?v=U1VaRu5EoOk | el | «ΜΟΥ ΤΗΝ ΠΕΦΤΕΙ ΝΥΧΤΑ ΣΤΟ ΠΑΛΕΡΜΟ #1», Kritikos Family, 14 Jan 2025, 426k views; 9 players; chapters show 3 days / 3 votes in a 34-min episode | Medium as evidence of pacing and popularity |
| S22 | https://www.youtube.com/watch?v=FeST2pFP_e8 | el | «Bar Games Andante edition», 16 May 2020, 30k views; 6 players, «4 γύροι με 4 ανατρεπτικές νύχτες» | Medium as evidence of pacing |
| S23 | https://medium.com/@timokliakousi/how-to-win-in-night-falls-in-palermo-mafia-game-c8959413bf76 | en | Strategy essay by Greek player Timoklia Kousi, 9 Apr 2018; «two assassins, one spy and citizens» as the popular setup; ~15-player session story | Medium: one experienced player's account |
| S24 | https://boardgamematcher.com/game/criminalita | en | Aggregator entry for *Criminalita* (2004, D. Chassapakis & Eric Parks, Typical Mutations LLC), 7–24 players, 30 min, «published only in Greek»; the commercial Palermo with power cards | Low-medium: third-party summary |
| S25 | https://en.wikipedia.org/wiki/Mafia_(party_game) | en | Reference article: history, standard roles, ratios, day/night, win conditions, optional roles | High |
| S26 | https://eblong.com/zarf/werewolf.html | en | Andrew Plotkin's original Werewolf rules (primary source) | High |
| S27 | https://rulespal.com/ultimate-werewolf/rulebook | en | Transcription of the Ultimate Werewolf rulebook (Bezier Games) | Medium-high |
| — | https://boardgamegeek.com/thread/404098/criminalita-peftei-i-nykhta-sto-palermo and https://boardgamegeek.com/thread/504580/palermo-to-paixnidi-teliose-pite-tis-entipwseis-sa | el | BGG threads about Criminalita / «ΠΑΛΕΡΜΟ – ΤΟ ΠΑΙΧΝΙΔΙ ΤΕΛΕΙΩΣΕ! Πείτε τις εντυπώσεις σας!» | **Not read**: BGG serves a Cloudflare bot check, which I did not bypass |
| — | https://www.ratpack.gr/buzz/story/32970/... and https://ipalermo.gr/ | el | A 2010s feature and the 2011 online version | **Dead**: ratpack redirects to a "we moved" notice; ipalermo.gr does not resolve |

Not found despite searching: an insomnia.gr thread on the game (the searches only surfaced generic forum sections), any Greek Wikipedia article, and any scout/camp PDF with rules.

---

## 2. Rules as played: consensus and variants

### 2.1 Standard roles

**Two killers, one «φανερός» (shown) and one «κρυφός» (hidden).** Present in essentially every Greek source: S1, S3, S4, S5, S6, S8, S9, S11, S13/S14, S18. The pair know each other from the first night (S1, S3, S8). Cards: the shown killer is usually the **red King** and the hidden the **black King** (S3, S4, S6); S1 and S9 use King = hidden and Queen = shown instead. S4 notes the hidden killer has a big advantage in surviving to the end (paraphrased).

**The informed good player.** In the older, card-deck sources this role is the **Ρουφιάνος** / **Καρφί** / **Πληροφοριοδότης** (the Ace): S1, S3, S4, S7, S8, S9, S10, S11. In newer and app sources the same role is called **Αστυνόμος / Αστυνομικός** (S5, S6, S12, S13, S14, S16) or **Ντετέκτιβ** (S18). Whatever the name, its power in the classic game is one thing: **on the first night it is shown the φανερός killer** (hand raised) and then must steer the town toward that killer without betraying that it knows (S1, S3, S8, S9; Palermo Nights S14: «Γνωρίζει από την αρχή τον φανερό δολοφόνο»). **It has no nightly investigation** in S1, S3, S4, S5, S6, S8, S9, S11, S13/S14 (Police), S18. Nightly checks exist only as a *separate* role or variant: S2's «Ντετέκτιβ» (used from 12 players; each night points at one player and is told killer or not), S14's «Ντετέκτιβ» (once per game, learns the team), and S12's one-line «ο αστυνόμος κάνει έρευνες». So the Greek policeman is Mafia's "witness", not Werewolf's seer.

**Γιατρός (doctor).** Optional in most sources: a variant for experienced groups (S3), an optional add-on (S5), «αν η παρέα είναι αρκετά μεγάλη» (S12), from 7 players in S2, present in S4, S7 (nurse or doctor), S18, and S14, but **not** in Palermo Nights' Classic mode (S13, S16). Each night picks one player; if the killers picked the same player, nobody dies and the town only learns «χωρίς δολοφονία» (S2, S4).

**Πολίτες (citizens).** Everyone else, dealt number cards (S1, S3, S6). Their weapons are numerical majority, observation and the informer's indirect help (S4, paraphrased).

**Αφηγητής (narrator).** A non-playing person in S1, S3 («έναν αφηγητή που δεν παίζει»), S8, S10. S11 lets the narrator play as a citizen by day. Palermo Nights removes the narrator («Δεν χρειάζεται αφηγητής», S15) and makes **the first player who dies the «βραδινός εκφωνητής»** who runs the night (S13, S16). S4 and S7 describe the same folk habit: the killers show their victim to «τον παίκτη που έχει αποχωρήσει», who signals the narrator that the choice is made (S4), and the nurse tells the previous victim whom she saves (S7).

### 2.2 Role counts by table size

Minimum size: 5 (apps S16, S17, S18), 6 (S8 «τουλάχιστον έξι παίχτες», S5 and S4 say more than 6), 7 (S3: at least 7 plus a narrator; S9 «εφτά ή και περισσότερα»; S10), 11+ (S11). Everyone agrees that more is better: «the bigger the group, the better» (S10, translated).

The only explicit Greek scaling rules:

- S1 (variant note): about one killer per four citizens, one hidden, the rest shown.
- S2 table: **4–6 players**: 1 shown killer, 1 informer, 2–4 citizens (only one killer). **7–11**: narrator, hidden killer, shown killer, informer, doctor, 2–6 citizens. **12–17**: three killers, corrupt policeman, informer, sold killer, detective, doctor, two cohabitants, 1–6 citizens. **18–24**: a fourth killer.
- S13/S16 (Palermo Nights Classic, 5+): 2 killers, 1 police, rest citizens, no doctor.
- S10 (Qbrain): 2 killers, 1 informer, add the Εταίρα at 8+.
- English references for comparison: Davidoff used about one third mafiosi; Plotkin recommends exactly two werewolves and an odd player count (S25, S26). Ultimate Werewolf's starter table: 1 werewolf at 6–8 players, 2 at 9–11, 3 at 12–15 (S27).

What this gives for the counts the engine cares about (derived from the rules above, not stated as tables in any Greek source except S2):

| Players | Greek classic (S1, S3, S8, S13) | S2's table | Werewolf starter (S27) |
|---|---|---|---|
| 6 | 2 killers, 1 informer/police, 3 citizens (no doctor) | 1 killer, 1 informer, 4 citizens | 1 wolf, 1 seer, 4 villagers |
| 7 | 2 killers, 1 police, 4 citizens (doctor optional) | 2 killers, informer, doctor, 2 citizens + narrator | 1 wolf, seer, 5 villagers |
| 8 | 2 killers, police, 5 citizens; S10 adds the Εταίρα here | 2 killers, informer, doctor, 3 citizens | 1 wolf, seer, 6 villagers |
| 10 | 2 killers, police, doctor, 6 citizens; S1's 1:4 rule would allow a third (shown) killer | 2 killers, informer, doctor, 5 citizens | 2 wolves, seer, 7 villagers |

Thin spot: no Greek source gives a 6-player setup with **both** a doctor and a police plus two killers; the engine's 6-seat default is denser in power roles than anything in the sources.

### 2.3 Day, votes, death (summary; detail in section 4)

- Open accusations, then one vote per living player; **most votes is out** (plurality) in S1, S3, S8, S10, S13. No Greek source requires a majority.
- **Ties: revote among the tied, repeat until someone changes their mind** (S1, S2, S8); S11 cancels the vote and resumes discussion if nobody budges; S13: «Οι παίκτες συζητούν ξανά».
- **Voted-out player shows their card** (S1, S3, S4, S6, S13); **night victim does not** (S1, S2, S10, S13). S11 and S2 never reveal anything.
- Dead players are silent and do not vote (S1, S2, S11, S13).

### 2.4 Win conditions

- Town wins when both killers are out (all sources).
- Killers win «σε περίπτωση που ξημερώσει και έχει μείνει ένας Δολοφόνος και ένας Πολίτης ή Ρουφιάνος» (S1; same in S2, S8), i.e. 1-vs-1 at dawn. Apps phrase it as parity: killers win when they «υπερτερούν αριθμητικά» or equal the citizens (S13, S16); S6 says equal numbers.
- **Killing the informer/police is an instant killer win** in S3, S6, S9 and the default of S4 (which adds that some groups drop this rule). Palermo Nights has the opposite rule: «Νικούν οι καλοί αν μείνει αστυνομικός ή στρατιώτης με έναν δολοφόνο» (S13). This is the biggest disagreement between sources.
- Endgame special case (S3, S4): **with 4 players left (2 killers, informer, 1 citizen) the nights stop and only votes remain**; with 3 left (1 killer, informer, citizen) the final vote decides, and voting out the citizen is «ισοπαλία». A commenter on S4 points out the 4-player rule can also just end in a draw.
- Compare Werewolf: humans win by killing both wolves, wolves win at parity (S26); Mafia wins at «numerical parity» (S25).

---

## 3. Night script

Assembled from the sources' own wording; the line-by-line structure is identical in S1, S3, S8, S9, S5 and S11, with the informer called αστυνομικός in S5/S6 and the apps.

### 3.1 First night (identification only, no murder)

> **Αφηγητής:** «Πέφτει η νύχτα στο Παλέρμο και όλοι κλείνουν τα μάτια τους.» (S1, S8; S3: «Η νύχτα πέφτει στο Παλέρμο και όλοι κλείνουν τα μάτια τους»; S10: «...κλείνουμε όλοι τα μάτια μας»; S11: «Όλοι οι παίκτες κλείνουν τα μάτια και κοιμούνται»)
> «Οι δύο δολοφόνοι ανοίγουν τα μάτια και κοιτάζονται.» (S4; S9: «Οι δυο δολοφόνοι να ανοίξουν τα ματιά κ να κοιταχτούν μεταξύ τους»)
> «Οι δυο δολοφονοι να κλεισουν τα ματια τους.» (S9, spelling as posted)
> The shown killer raises a hand, held so the neighbours cannot see it (S1, S8; S9: «Η ντάμα δολοφόνος να σηκώσει το χερι»)
> «Ο ρουφιανος να ανοίξει τα ματιά κ να δει το δολοφόνο.» (S9; S5 has the αστυνομικός here)
> «Ο δολοφόνος(ντάμα) να κατεβάσει το χέρι κ ο ρουφιανος να κλείσει τα ματιά» (S9)
> «Και μια νέα μέρα ξημερώνει στο Παλέρμο και όλοι ανοίγουν τα μάτια τους.» (S1, S2; S3: «Ξημερώνει μία νέα ημέρα στο Παλέρμο. Όλοι ανοίγουν τα μάτια τους.»)

Facts about this night:

- **The policeman is shown the killer on night 1, not at a separate setup step**, by the hand-raise (S1, S3, S5, S8, S9). The apps show it on the role screen instead (S13: «Τον γνωρίζει από την αρχή»).
- **There is no kill on the first night**: the S1, S3, S8 and S9 scripts go from the hand-raise straight to «ξημερώνει». Palermo Nights: «Κάθε παιχνίδι ξεκινάει με Φάση Ημέρας» (S13). So **the first vote happens before the first murder**.
- With extra roles the first night grows: the courtesan/henchman opens eyes after the informer and sees both killers (S10, S11, S3's Τσιράκι); cohabitants look at each other (S2).
- **No nod.** No Greek source has the narrator confirm anything to the policeman; the hand-raise is the whole answer. The thumbs-up/thumbs-down to a Seer is Werewolf (S26, S27).

### 3.2 Later nights

> «Πέφτει η νύχτα στο Παλέρμο και όλοι κλείνουν τα μάτια τους.» (S1)
> The killers open their eyes and show, by gestures, whom they want to kill; the hidden killer points the victim out to the narrator (S1, paraphrased). S4's narrator says the two killers now decide «ποιον παίκτη θα βγάλουν από το παιχνίδι».
> *(if a doctor is in play)* the doctor opens their eyes **after** the killers have pointed and picks one player to save, «εκτός από τον εαυτό του» (S2, S7; S4 says the doctor opens «αμέσως μόλις οι δολοφόνοι δείξουν»). S11's Angel is the exception that acts *before* the killers.
> *(if a detective is in play, S2 only)* the detective points at one player and is told killer / not killer.
> «Μία νέα μέρα ξημερώνει στο Παλέρμο χωρίς τον Τάδε.» (S1) or, after a save, «Μια νέα μέρα ξημερώνει στο Παλέρμο χωρίς Δολοφονία.» (S2)

Facts:

- **The killers point together.** Silent agreement by gestures, the hidden killer gives the final sign to the narrator (S1); the apps let each killer name a victim to the narrator (S14). Palermo Nights' Πληρωμένος Δολοφόνος can add a second victim (S14).
- **A dead killer keeps helping.** Asked whether a dead killer may join the night choice, the S1 author answered in the comments that killers coordinate every night, alive or dead (paraphrased). S23's story has the voted-out sister still choosing victims.
- **Doctor self-protection:** not allowed in S2 («other than himself») and S7 («εκτός από τον ίδιο»); allowed in Palermo Nights (S14: «ακόμα και τον εαυτό του»). Ultimate Werewolf's Bodyguard «may not choose themselves» (S27). Two of three Greek sources that address it say no.
- **The night victim does not show their card** (S1, S2, S10, S13).
- In the folk version the narrator's night helper is the last dead player (S4, S7, S13, S16).

---

## 4. Day and votes

**Discussion.** Free accusations, often from body language: «χαμογέλασε όταν πήρε την κάρτα» (S10, paraphrased); «Ο Γιώργος δεν λέει τίποτα, άρα κάτι κρύβει» (S5, example accusation). S11 adds procedure: the informer is expected to speak first; early accusations are weak; alliances form and break. Voters justify their choice as they vote (S9) — a one-line reason with the vote is normal.

**Vote mechanics.** One vote each, usually by hand. S11 goes around the circle, and each accused holds up fingers for the votes received. One forum post found via search describes secret votes and dead players re-entering, but that page (BGG thread 504580) could not be read, so treat secret voting as an unconfirmed variant. Palermo Nights limits to «one vote per alive player» (S18, release note) and has a «Συμβουλή» button (S13).

**Threshold.** Most votes wins (S1, S3, S8, S10, S13: «Ο παίκτης με τις περισσότερες ψήφους, βγαίνει από το παιχνίδι»). Werewolf needs a majority (S26, S27); Mafia rules differ but the Wikipedia default is more than half (S25).

**Ties.** Revote among the tied; if it ties again, repeat until someone changes their decision (S1, S8, S2). S11: if nobody changes, cancel the vote and talk more. S13: discuss again. S7: the mayor's double vote only counts in a tie. Nobody in the Greek sources says "nobody is out" after a second tie, except S11's cancel-and-talk.

**Defence speeches.** No Greek source has a formal defence before the vote. S11 allows a farewell speech *after* elimination, in which the player may claim innocent or guilty and need not tell the truth (paraphrased). Ultimate Werewolf: nominations need a second and the accused may defend before the vote (S27).

**Role reveal.** Voted out: shows the card (S1, S3, S4, S6; S13: «Ο χαρακτήρας του αποκαλύπτεται στους υπόλοιπους παίκτες»). Killed at night: card stays hidden (S1, S2, S13 «μένει μυστικός γιατί πέθανε στα κρυφά», S10 unless someone plays «Τυμβωρυχία»). Never revealed at all: S2, S11. All roles are shown at the end (S13).

**Dead players.** No talking, no gestures, no voting until the game ends (S1, S2, paraphrased), S11 the same, Palermo Nights «Όχι, δεν συμμετέχετε ενεργά» (S13). Exceptions: the first dead becomes the night narrator (S13, S16, S4 folk practice); S10's «Κρυστάλλινη Σφαίρα» and S2's Voice From Beyond card (name given in translation) let the dead cast one joint vote; a dead killer still whispers at night (S1 comments, S23). Plotkin: dead players «may not speak at all» (S26).

**Pacing on camera.** Kritikos Family's episode (9 players) runs three days and three votes in under 30 minutes of edited video, with a «Κανόνες» chapter of about 80 seconds (S21). The Andante bar game (6 players) advertises «4 γύροι με 4 ανατρεπτικές νύχτες» (S22). Criminalita lists 30 minutes (S24); Wikipedia gives 15–90 minutes (S25).

---

## 5. Extra roles

Counted by how many of the Greek sources above mention them (apps count once each).

| Role (Greek) | What it does | Sources | Count |
|---|---|---|---|
| **Γιατρός / Νοσοκόμα** | Saves one player per night; self not allowed in S2/S7, allowed in S14 | S2, S3, S4, S5, S7, S12, S14, S18, S23 | 9 |
| **Evil informed helper**: Τσιράκι (S3, S4), Εταίρα (S7, S10), Πουτάνα (S11), Ιερόδουλη (S5), Ρουφιάνος-as-evil and Δικηγόρος (S14) | Sees the killers on night 1 (one or both), killers do not know them, protects them by misdirection, wins with the killers | S3, S4, S5, S7, S10, S11, S14 | 7 |
| **Δήμαρχος** | Vote counts double; chosen openly before the deal (S3, S4), hidden and only in ties (S7), reveals to activate (S14), listed (S17) | S3, S4, S7, S14, S17 | 5 |
| **Ντετέκτιβ / Μάντης** (seer-like check) | Nightly killer check (S2, from 12 players), once per game (S14), nightly (S11) | S2, S11, S14, S12 | 4 |
| **Ερωτευμένοι** (lovers) | If one dies the other dies | S14, S17, S18 | 3 (apps only) |
| **Αλεξίσφαιρος** | Cannot die at night (card in S10, role in S14/S17) | S10, S14, S17 | 3 |
| **Τρέλα / Κλόουν** (jester-like) | Wins alone if voted out; the game ends | S14, S17 | 2 (apps only) |
| **Στρατιώτης / Κυνηγός** | One shot per game (S14) / kills a player when voted out (S7) | S7, S14 | 2 |
| **Καμικάζι** | Blows up with one good player during a day | S14, S17 | 2 |
| **Άγγελος** | Protects before the killers act | S11, S23 | 2 |
| **Μάγος** (skips a vote), **Μητέρα Τερέζα** (no more nights if voted out), **Προδότης**, **Γείτονας**, **Τζογαδόρος**, **Σκύλος**, **Άρρωστος**, **Τρελός Επιστήμονας**, **Βοηθός Αστυνομικού** | See S14 | S14 | 1 each |
| Corrupt Policeman, Sold Killer, Cohabitants (S2 names, in translation) | Double agents and a known-good pair, 12+ players | S2 | 1 |
| **«Κάρτες Τύχης» (S10) / «Ιδιότητες» (S2)**: Έχτρα Ψήφος, Ακύρωση Ψήφου, Άμεση Καταγγελία, Ακύρωση Καταγγελίας, Νεκρανάσταση, Αλεξίσφαιρο, Τυμβωρυχία, Κρυστάλλινη Σφαίρα, Όνειρο, Μπλόφα (S10 names); S2 adds Exemption and Voice From Beyond (in translation) | One-shot power cards dealt alongside roles | S2, S10 (and the Criminalita design, S24) | 2 |

Observations: the doctor and the **evil helper who is shown the killers** are the two most common additions; the mayor is a close third. Lovers and the jester-like Τρέλα are app inventions, not found in any blog or article. English references list Mayor/Doublevoter, Lovers, Jester-type and Bulletproof among common optional roles (S25), so the apps are importing from Werewolf.

---

## 6. What makes a night fun (quotes under 15 words)

- «η πονηριά και η ψευτιά έχουν τον πρώτο λόγο» — aeon_02, S1.
- «Βγάζει τον μαφιόζο από μέσα μας!» — Σταυριανός Κιναλόπουλος, S20.
- «για γερά νεύρα» and the idea that the group itself is the real winner — Άντρεα Λαζαρίδου, S5.
- «αφήστε τη φαντασία σας ελεύθερη» — Κυριάκος Κουρουτσαβούρης, S4.
- «4 γύροι με 4 ανατρεπτικές νύχτες στο Παλέρμο» — Bar Games Andante, S22.
- «the more people, the funnier it gets» — Timoklia Kousi, S23.
- «The night kills are the most trustworthy hints for the game.» — Kousi, S23.
- «Usually the first round is pure luck.» — Kousi, S23.
- «a game of accusations, lying, bluffing, second-guessing, assassination, and mob hysteria» — Andrew Plotkin, S26.
- The critic's view: citizens vote «χωρίς να έχουν κανένα στοιχείο» — arkoudos.com, S12. Worth keeping in mind: information-free days are the part people dislike.

Recurring themes: the hidden killer's double game (S4, S23), framing («kill the person in your team and automatically he/she will look guilty», S23), the informer's tightrope (S1, S3, S9), the celebration when a killer is unmasked (S23's «I knew it…»).

---

## 7. Differences from our engine

Engine facts from `palermo/game.py` (default `--roles killer=2,officer,doctor`, 6 seats; `run()` plays `night(n)` before `day(n)`; `check_pool` excludes self and the shown killer; `vote` → runoff → «Nobody is eliminated»).

| Topic | Greek sources | Engine | Gap |
|---|---|---|---|
| Officer's information | Shown the φανερός on night 1, **no nightly check** (S1, S3, S5, S8, S9, S13/S14) | Shown at setup **and** checks one player per night | Engine officer = Greek ρουφιάνος + Werewolf seer; stronger than any source. Only S2's 12+-player Ντετέκτιβ and S12 check nightly |
| First night | Identification only; **day 1 and its vote come before any murder** (S1, S3, S8, S13) | Night 1 kills immediately | Engine skips the Greek "zero-information day" |
| Killer coordination | Silent gestures; hidden killer gives the final sign (S1); dead killer still helps (S1 comments, S23) | Shown proposes, hidden has the last word; dead killers silent | Close; dead-killer whispering absent |
| Doctor | Optional, mostly for larger tables (S3, S5, S12); self not allowed in S2/S7, allowed in S14; acts after the killers point | Always on at 6; self allowed | Two of three Greek sources forbid self-save |
| Vote threshold | Plurality (S1, S3, S8, S13) | Plurality | Same |
| Vote reasons | Voters justify their choice (S9) | One-line reasons | Same |
| Ties | Revote among tied **until someone changes** (S1, S2, S8); S11 cancels and talks more | Runoff, then nobody out | Greek rules never let a tie fizzle silently |
| Role reveal, voted out | Card shown (S1, S3, S4, S6, S13) | Revealed | Same |
| Role reveal, night victim | **Not shown** (S1, S2, S10, S13) | Revealed | Different, strong consensus |
| Dead players | Silent, no vote (S1, S2, S11, S13); first dead may narrate nights (S13, S16) | Silent | Same |
| Killer win | 1-vs-1 at dawn (S1, S2, S8) / parity (S6, S13) | killers ≥ everyone else | Same in effect |
| Officer death | **Instant killer win** (S3, S6, S9, S4 default); opposite in S13 | No effect | Missing the classic stake; sources disagree |
| Endgame | At 4 alive nights stop, only votes (S3, S4) | Nights continue | Engine ends at 2K+2T by parity, Greek game keeps voting |
| Mayor | Double vote, 5 sources | None | Cheap to add |
| Evil helper (Τσιράκι/Εταίρα) | 7 sources, from 8 players | None | Needs a bigger table |
| Jester | Τρέλα in apps only (S14, S17) | `jester` flag | Same idea, app-only in sources |
| Table size | 6 is the floor; 7+ typical; no source puts 2 killers + police + doctor at 6 | 6 with four power roles | Engine's 6 is power-dense; S2 would use one killer at 6 |
| Narrator | Non-playing human; apps hand nights to the first dead | GM process | Fine |

---

## 8. Recommendations, ranked by fun for a watchable AI game

1. **Hide the night victim's role; keep the day-vote reveal.** Strong consensus (S1, S2, S10, S13). Lets the hidden killer claim a dead player's role, lets killers frame («kill the person in your team…», S23) and keeps the audience guessing about every night death. One-line change in the narration.
2. **Make the officer's death matter.** Classic rule: killers win the moment the ρουφιάνος dies (S3, S6, S9, S4). It turns the officer's claim into a real gamble and gives killers a target to hunt, which is the drama of the Greek game (S1, S9, S23: «If you know the spy kill him»). Because S4 says groups drop it and S13 has the opposite rule, ship it as a flag, default on for the Palermo role set.
3. **Classic officer: shown only, no nightly check** (S1, S3, S5, S8, S9, S14). At 6 seats the current officer finds the hidden killer in about two checks, and the doctor shields them; the folk officer has to win by persuasion, which is better television. If the check must stay, use Palermo Nights' compromise: one check per game (S14, Ντετέκτιβ).
4. **Keep voting when 4 are left** (S3, S4): no more nights, the last votes decide, voting out the last citizen at 3 is a draw. Gives the town a final showdown instead of a parity auto-win, and short 6-seat games get one more dramatic vote.
5. **Ties: revote until someone flips, no "nobody out"** (S1, S2, S8). The player who changes their vote becomes the story of the day. If the runoff must be capped, follow S11: cancel the vote and reopen discussion rather than sleeping on a tie.
6. **Add the Δήμαρχος** (S3, S4, S7, S14): a double vote. Palermo Nights' version, where the mayor reveals to activate it, is the most watchable (S14); S3/S4 choose the mayor openly before the deal.
7. **Start with an identification night and a vote before the first murder** (S1, S3, S8, S13). Authentic, and the officer's steering is the only signal on day 1; but S12 and S23 call information-free days the dull part («Usually the first round is pure luck»). Try it behind a flag and judge the transcripts.
8. **At 8+ seats add the evil helper (Τσιράκι/Εταίρα)** who knows the killers while they do not know them (S3, S4, S7, S10, S11, S14). It creates a second liar with a different information set. Not for 6 seats.
9. **Doctor tweaks:** no self-save (S2, S7), save announced as «χωρίς δολοφονία» (S2, S4), and consider dropping the doctor at 6 (S3, S5, S12 treat it as a larger-table role).
10. **Let a voted-out killer keep whispering at night** (S1 comments, S23). Flavour only, but it keeps an eliminated AI seat in the story.
11. **Seat count:** sources would play 6 as 2 killers + officer + 3 citizens (S1, S8) or 1 killer (S2); 7–8 as 2 killers + police + doctor (S2, S3). If the default stays at 6 with both power roles, the officer-only and hidden-victim changes above are what keep it balanced.

Thin or disputed ground, stated plainly: nobody publishes a per-player-count table except S2 and the apps; the instant-loss-on-officer-death rule is contradicted by Palermo Nights; doctor self-save has one source each way plus one against; "dead players may re-enter" and secret ballots come only from a BGG thread that could not be read; and no Greek source describes a defence speech before the vote.
