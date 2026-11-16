# Palermo design system (generic, reusable)

Written 2026-10-26 for the UI rebuild. This file is the single source of truth for look and feel. It is deliberately
product-agnostic: tokens, type, components, motion and layout rules that any social-deduction or table game can reuse.


## 1. Direction in one paragraph
Palermo at night, one dark world: navy rooms, a cream card for what is said aloud, indigo for what is only thought,
coral for action and danger, gold for attention. Day and night differ by light (warm from above, cold moonlight), not
by hue. Illustrated portraits, not icons. The feel is a well-made board game box, not a dashboard and not a casino. Every screen has one hero (the spoken line, the
vote, the reveal) and everything else steps back. Motion is feedback, never decoration. The test is a person watching a
replay on a laptop or a phone: every line readable from a normal distance, in one place. (2026-11-14: the video target
and its `?video`/`?cut` modes were dropped; readability in the viewer comes first.)

**Two modes, one visible control: Watch / Guess.** *Watch* (the default) shows the viewer everything: every role, the
killers marked, each speaker's thought folded in above the line. *Guess* shows only what the table knows: roles appear
when a card is turned, thoughts are hidden, and everything is revealed on the end card. Engine internals (the engine's
turn labels, memory notes, clocks) are never shown; `?debug=1` shows the turn labels in the log. Without `?file` the viewer opens Home (§5); live is decided by `/games/index.json` (§5, Live), and `?file=…&live=1` forces it for a file the index does not list. Rule: say each fact in
one place. If the card already names the speaker, the seat does not repeat it in words. (2026-11-14: replaces the
*Details* switch, which hid the roles by default and made the replay hard to follow.)

## 2. Colour

### 2.1 Base palette (contrast-checked; `ui/src/tokens.css`)
| name | hex | use |
|---|---|---|
| navy-950 … navy-500 | `#05070F` `#0A0E1F` `#10162F` `#171E40` `#1F2852` `#2B3566` | the rooms (darkest at the night edge), panels `#171E40` / `#1F2852` |
| hairline | `rgba(244,239,228,.14)` | lines and borders on navy |
| moon | `#F4EFE4` | text on navy |
| moon-soft | `#A9B0CE` | secondary text on navy |
| cream | `#FBF6EA` | the card (what is said), the one light surface |
| cream-dim | `#F1E7D0` | second surface inside the card, notes |
| ink | `#14172B` | text on cream, gold, coral, mint, sky |
| ink-soft | `#565B78` | secondary text on cream |
| coral | `#FF6A4D` | action and danger: the speaker ring, killer, buttons, "a lie" |
| coral-deep | `#AD3418` | coral as text on cream |
| gold | `#FFD166` | attention: highlight, addressed ring, day labels, mayor, "true" |
| mint | `#5FD39A` | doctor, success, "safe" |
| sky | `#6FB6FF` | officer, information |
| indigo | `#262E63` | the private-thought surface |
| lilac | `#DCD6FF` | private-thought text |

Measured contrast (WCAG, computed 2026-11-16): ink/cream 16.4, ink-soft/cream 6.2 (cream-dim 5.4), coral-deep/cream 5.9,
moon/navy-700 14.1, moon-soft/navy-600 6.6, coral/navy-600 5.0, gold/navy-700 11.2, mint/navy-600 7.6, sky/navy-600 6.6,
lilac/indigo 9.1, ink on gold 12.3, on coral 6.3, on mint 9.5, on sky 8.3. Checked by `ui/src/tokens.test.ts` over
`ui/src/tokens.css`. Fails, so never used with text: cream or moon on coral (2.6), coral as text on cream (use
coral-deep), any bright seat colour as text on cream (use the deep set). Never add a colour outside this table without
adding it here.

### 2.2 Semantic tokens (what components reference; themes swap the values)
```
--bg, --surface, --surface-2, --text, --text-muted, --line
--accent, --accent-strong, --on-accent, --ok, --info, --warn, --highlight, --on-highlight
--thought-bg, --thought-text
--shadow-1 (0 2px 8px rgba(0,0,0,.35)), --shadow-2 (0 18px 50px rgba(0,0,0,.5))
--ring-speaker (accent), --ring-addressed (highlight), --ring-thinking (thought-text), --ring-dead (text-muted)
```
Both themes are dark. Day: bg navy-700, surface navy-600, a warm glow from above (`rgba(255,190,120,.26)`). Night: bg
navy-900, surface navy-700, a cold glow from the upper right (`rgba(130,155,255,.20)`) and a deeper vignette. In both,
text moon, accent and accent-strong coral, `--on-accent` ink, highlight gold with `--on-highlight` ink, thought indigo
with lilac.
Role colours (fixed, both themes): killer coral, officer sky, doctor mint, mayor gold, citizen none. The ring carries
the colour; the role label is `--text`, the killer's `--accent-strong`.
Seat colours (seven, fixed by seat index). Bright set for rings, names and the log on navy (each ≥ 5.8 on navy-600):
`#FF8073 #6FB1FF #5FD39A #F2B25C #B39BFF #FF85C8 #4FD6D6`. Deep set, swapped in inside the cream card for the
speaker's name (each ≥ 5.5 on cream, 4.8 on cream-dim): `#B5331F #2459A8 #1F6B45 #8A5210 #6B46C1 #A82A72 #1F6F70`.
Table: a lit slab in the room, drawn in navy (`--wood` rim `#34407A` / `#232C5A`, `--felt` top `#131A3A` / `#0B1026`,
lamp light gold by day, moonlight by night). No text sits on the table itself; the card on it is cream.
The card swaps in its own light set (`Card.module.css`): cream with ink, ink-soft, coral-deep and the deep seats, in
both themes, so the hero never changes colour at dusk. The speaker's thought is an indigo strip with lilac italic; a
note is cream-dim with ink; a ghost line is navy with moon. `tokens.test.ts` checks all of them.

### 2.3 Rules
- Text contrast ≥ 4.5:1 for body, ≥ 3:1 for ≥ 24 px display. Bright colours are for the navy, deep ones for the cream card; never swap them.
- One accent per screen region. If two things glow at once, one of them is wrong.
- Role colour appears only when a role is public (dead, revealed, or "show roles" on).

## 3. Typography
- **Display: Bodoni Moda** (Google Fonts, variable, SIL OFL), upright only. A didone: at its natural optical size the
  hairlines vanish on a dark screen, so every use pins a sturdier cut (`--display-cut: 'opsz' 9`, the home title
  `--display-cut-xl: 'opsz' 16`). **Titles and big numbers only, 24 px and up**: the home title, section headings,
  phase titles, vote counts, the end card title, the scoreboard totals. **Never a sentence**: serif italic quotes
  proved unreadable at card sizes.
- **Everything else: Instrument Sans**: every sentence (speech 500, quotes on the home cards 600, the host's lines 500,
  the thought 500 italic), small headings (700), names, buttons, labels, the log.
  Fallbacks: `'Bodoni 72', Didot, 'Iowan Old Style', Georgia, serif` and `"Avenir Next", "Segoe UI", system-ui, sans-serif`.
  Self-host both as woff2 under `/fonts`; no runtime Google request (privacy, offline).
- **Floor: nothing under 13 px.** Tokens: `--fs-label` / `--fs-meta` 13 px · `--fs-log` 16 px (15 on phone) ·
  `--fs-ui` 16 px · `--fs-thought` clamp(15px, 1.2vw, 19px) · `--fs-seat` clamp(18px, 1.35vw, 22px) ·
  `--fs-live` clamp(22px, min(2.65vw, 4.3vh), 38px), the line on the card (38 px at 1440×900; a 30-word line under a two-line thought still fits there) · `--fs-title` clamp(28px, 3vw, 44px), the end card.
  (2026-10-26: names were 24 and the line 20, which made the name bigger than the hero. 2026-11-14: the floor and the
  clamps replace the fixed scale; 11 px labels went.)
- **Three sizes per screen.** Hero (the line, the vote count, the reveal), middle (names, the thought), small (everything
  else, muted). If a screen needs a fourth size, remove something.
- The card holds 3–4 lines of `--fs-live` without moving the seats; log lines ≤ ~50 characters (`max-width: 34em`).
- Numbers in Bodoni Moda with `font-variant-numeric: tabular-nums` (clocks, tallies).

## 4. Spacing, shape, depth
- Spacing scale: 4 · 8 · 12 · 16 · 24 · 32 · 48 px. Gutter on phone 16 px, on desktop 24 px.
- Radii: chips 999 px, cards 16 px, the card 18 px, portraits 50 %, buttons 12 px.
- Depth: two shadows only (`--shadow-1` for chips/buttons, `--shadow-2` for the hero card). No borders thicker than 1 px
  except portrait rings (3–4 px).
- Surfaces are navy rooms: a radial navy gradient, an inset vignette and one glow (warm from above by day, cold by
  night). The table is drawn in CSS (a lighter navy rim, a dark top catching the light), no image.

## 5. Components (names are the React component names in `ui/src/`)
- **Seat**: portrait (`--portrait`, set by the composition) in a cream ring; name (display, `--fs-seat`) and model caption
  (13 px muted; hidden on phone, the end card lists it); tags: the role (Watch, or when public; the killer's in the
  accent, and a killer's portrait border is coral), the **turned card** when dead (a small cream playing card with a
  role-colour top band and the role's emblem; it flips in and stays), `card face down` when a death hides the role,
  `says officer` (dashed) from `say.claim`; on phone the claim is a small dashed mark with the claimed role's emblem on
  the portrait's shoulder. Rings, one at a time: speaking (accent ring + glow, scale 1.08), addressed (gold ring), ghost
  (dotted outline while the dead seat talks to the audience). Dead: face grey at 50 %, name muted. Top-row seats put the
  label above the portrait, so every portrait faces the table.
- **Pile** (on the seat): who leans on this seat (`say.lean`), small faces in a slot under the portrait (always reserved,
  so nothing jumps; it tucks 4 px into the cream ring and never covers the face). At the table the slot hangs toward the
  table, over the gap and the table's rim. Light while they talk, solid accent with a count at the vote; cleared once the
  death after the vote has been shown, and at the end. Count the faces, get the votes. Never arrows.
- **Emblem** (`Emblem.tsx`): one flat shape per role on a 48 grid, drawn in SVG, in the role colour: killer a dagger,
  officer a shield with a star cut out, doctor a cross in a ring, citizen a house, mayor a key. Used on the reveal, the
  turned card at the seat, the log's death card and the phone claim mark. No stock icons, no emoji.
- **Card** (the one reading place, on the table): cream, ink, 18 px radius, a tail toward the speaker's portrait. Holds,
  in turn: the thought strip (`THINKS`, thought surface, italic, `--fs-thought`; Watch only, only when it belongs to the
  speaker) over the line (`--fs-live`), with a 44 px face, the name in the seat colour and the context: `to [Luna]` chip,
  `whispers to`, `declines to answer`, tags `last words` (accent), `before the game` / `after the game` (muted). Variants:
  narrator (phase title in display, or `the host` label over a plain sans line; an aside is smaller and muted, `the host, aside`); note
  (cream-dim, ruled, rotated −0.8°, `A note from X · found in the morning`, italic sans in quotes); ghost (navy,
  moon, `from beyond · only you can hear`); votes (targets side by side, 56 px face (40 on phone), count large in
  Bodoni Moda, voters' faces stacked under each, then `X is out`; a **secret ballot** (engine default from 2026-11-15) is
  labelled `the vote · secret ballot`: Watch shows the voters with `The table saw only the counts. You see who voted for
  whom.`, Guess shows the counts alone, on the card, the seats and the log, until the game is over); death (**RoleCard**, a CSS 3D flip from the portrait back
  to the role face — the emblem large in the role colour over the role name, inside a double rule — held 4.5 s; `voted out` / `killed in the night`, `X is out.`, `X was an officer.`). The card scrolls inside itself if a
  line is ever longer than it.
- **Log** (right column, or below on stack): one entry per turn, the thought folded in as a muted italic line (Watch
  only); thoughts with no line after them, memory notes and clocks left out. Sticky phase headers `Day 2 · 5 at the
  table`. Narration centred sans italic, asides smaller and muted. The vote grouped by target, the reasons one tap
  away (`<details>`). A death as a small card with the turned role. Notes as cream-dim slips; ghost lines indented, navy,
  `X, from beyond`; last words tagged. Follows the live moment; scrolling up pauses following and shows `Back to live ↓`;
  clicking an entry jumps the replay there. The current entry is marked by an inset accent bar and shadow, never a
  background (notes and ghosts keep theirs).
- **Header**: where you are, then the state. Where: a home button (house, `Games` from 1100 px), the title (≥ 1100 px),
  the evening nav `‹ Game 3 of 12 ›` (prev / next game of the same evening, disabled at the ends; `so far` while the
  evening is still playing; on phone `‹ 3 of 12 ›`), and a `LIVE` chip when following. State: in words (`Day 2 · 5 at
  the table · 2 killers left`, the moon by night; Guess counts only what the table knows; on phone the count at the table
  is left to the log head). Then previous / play / next, speed 1× / 1.5× / 2×, Watch / Guess, Log (wide only), a
  scrubber over the stops with phase marks and death dots. Live hides the replay controls and the scrubber. Phone:
  row 1 home · state · evening nav, row 2 the controls, row 3 the scrubber.
- **EndCard**: who won (`--fs-title`), then the host's closing remark if there is one (`THE HOST` label, italic
  Bodoni Moda 20 px, ink; the last `gm` aside with no phase, vote or death after it; the replay does not stop on it, and
  without it nothing is left blank; engine 2026-11-15: one host remark per game, at the end), `Game 3 of 12` with a link that swaps the cast for **the evening so far**
  (`Who was who` swaps back), the cast with face, name, model, role and when each went out (`voted out, Day 1`,
  `killed, Night 2`, `survived`), the recap at 16 px. The body scrolls; the actions stay in view: `Watch again`, then
  `Next game: 4 →` when it exists, `Game 4 starts soon…` (muted italic) while the evening is still playing and the next
  file has not appeared (the button replaces it within 5 s of the file appearing), else `All games`.
- **Scoreboard** (`Scoreboard.tsx`, ink on cream or cream-dim): a small caps title (`The evening so far` / `After game 3`),
  town wins against killer wins in 2 rem Bodoni Moda (mint / coral; on the cream card the deep shades), then a table: player (face, name) · `won N
  of M` · `killer N×`, sorted by games won, then fewer times killer. Counts finished games only, a stopped game counts
  for nobody. **Spoiler rule:** inside a game the scoreboard counts only games up to that one and appears only on its end
  card; the header shows numbers and arrows, never a result. Home shows the whole evening.
- **Home** (`Home.tsx`, `/ui/` with no `?file`; navy, one column, max 1080 px; rebuilt 2026-11-15 so a first-time
  visitor can start a game with one click). Top to bottom: the **hero** (night card, radius 28 px, a warm glow at the
  top right): eyebrow `Seven AI models · two secret killers · one table`, the title, one sentence (`Claude, GPT and Gemma sit down to play Mafia (the families are read from the cast, so another table names its own). Two of them are killers and must lie to the rest. You hear what each one says, and what
  it really thinks.`), the seven players (72 px portraits with a seat-colour ring, name, model; a 4-column grid on
  phone), the primary button `Watch the best game →` (the top game by the fun meter; `Watch the latest game →` without
  scores; `Watch the live game` while one is playing) and the secondary `Guess the killers` (the same game in Guess mode).
  Then **how a game goes** in three panel cards (Night / Day / You). Then **Start with these**: the six best games by
  the fun meter (`funmeter.py`, scores in `games/fun/`), each a panel card with the **meter** (five pips and the 0–100
  score), `Today, 10:16 · Game 7`, a line a player really said at that table (Instrument Sans 600, upright, with the speaker's face
  and seat colour; never a result), the length and `Watch →`. Then **Every evening** with the switch **Results: Hidden /
  Shown** at its right (segmented, ink when pressed; default Hidden, remembered in localStorage); the first evening is
  open, the others folded; a game row also carries its meter (dropped on phone). A closing line: `Nobody scripted these
  games. Every line, lie and mistake is the models' own.` Also: a **live row** per game being written
  (night card, pulsing `#FF6A4D` dot, `Live now`, `Today, 08:44 · Game 3 · Day 2 now`, the cast's faces, `Watch →`;
  the one loud thing on the page); then the **evenings** newest first, a live one first, each a folded `<details>`
  (open: the first and any live one): summary `Today, 08:44 · morning` (sans 700; the part of day muted, dropped on phone) · `12 games · 7 players · 5 town – 3
  killers · ● playing` · the tag in monospace (hidden on phone); body the game rows and the evening's scoreboard on a
  panel card at the right (below on ≤ 820 px). A **game row** is one button: `Game 3` (display), who won (`Killers win`
  coral, `Town wins` mint, `Stopped` muted, `playing now`), `2 days · 7 min`, the killers' faces with a
  coral border and their names (faces only on phone, two lines; names also hidden at 821–900 px beside the
  scoreboard). An evening shows its first six rows, then a dashed `Show all 12 games` (a live game always shows).
  **Results hidden** (the default, so nobody is spoiled, above all for Guess): a row shows only `Game 3` and `2 days · 7
  min`; the summary drops the tally; the scoreboard becomes `Results hidden. Watch the games, or switch results on
  above.`; the live row stays. A game this device watched to its end card (file names remembered in localStorage) shows
  its result anyway, and an evening's tally and scoreboard come back once every finished game in it was watched.
  localStorage is wrapped in try/catch: without it results stay hidden. Inside a game nothing changes. Old timestamp-named games sit at the bottom in a
  folded `Older games`. An evening is the games of one `--tag` (a repeated game number starts a new evening); its time
  is the first game's start: `Today, 08:44` / `Yesterday, 22:10` / `Sat 14 Nov, 22:10` (two evenings of one morning differ by
  the time).
- **Button**: 44 px minimum; primary accent with `--on-accent`; secondary surface with a 1 px line; segmented for modes.

## 6. Motion
- Easing: `cubic-bezier(.2,.8,.2,1)` for enters, `ease-in` for exits. Nothing linear, nothing bouncy.
- Durations: feedback 120–200 ms (chips, buttons, hover); content 200–300 ms (card rise 8 px + fade); drama 600–1200 ms
  (death desaturate, day↔night crossfade 1.2 s, end card). Never block input while motion plays.
- One idea per moment: the vote faces stagger 100 ms each so the eye follows the count; nothing else moves then.
- Reduced motion: honour `prefers-reduced-motion`. `?at=N` (a still at N events) disables all animation; animated
  elements keep their final state as the base style, so a still shows the last frame.
- Pace: each stop holds by word count, the folded thought included (`pace()` in `game.ts`): a line
  max(2.5 s, 1.4 s + 0.3 s/word + 0.24 s/thought word); a note 2.2 s + 0.3 s/word; the vote 3.5 s + 0.6 s/voter; the
  reveal 4.5 s. Divided by the speed.

## 7. Layout compositions (by the frame's shape, not by device)
- **Wide (≥ 760 px wide and aspect ≥ 1.2):** header across the top; the stage is a wide horizontal table (a lit navy slab:
  lighter rim, dark top) with the seats along its long sides and the card in the middle of the top, 90 % of the top's width (about 80 %
  of the table); the log is a right column (32 %,
  min 340 px), shown by default from 1100 px wide and toggled by `Log`.
- **Seating rule:** ceil(n/2) seats on the top side, the rest on the bottom, clockwise from the top left (seven = 4 + 3,
  six = 3 + 3), spaced evenly so the two rows stagger. Why: the reading place has to be one wide card, and a wide card
  wants a wide table; seats on the two long sides keep every name and tag off the card, keep the tail short, and leave
  nothing important at the bottom edge. (2026-11-14: replaces the 1 : 2.3 table art with three seats a side and the
  bubble in a bottom third, which put the line at the bottom edge and did not fit seven.)
- **Short wide (≤ 720 px tall, e.g. 800×600):** the seat label sits beside the portrait, the title goes, padding tightens,
  so the card keeps 3–4 lines.
- **Stack (portrait, phone):** the cast as a grid on top (seven: 4 + 3, the second row centred; six: 3 + 3), the card at
  full width under it (max 48 vh, the tail points up at the speaker), the log below like a chat. No sheet. Phone
  (< 520 px): 44 px portraits, 17 px names, tight role tags, model captions and the claim words hidden (the claim is a
  mark), header in three short rows (where and state, controls, scrubber), log at 15 px. The card takes what it needs and the log the rest (at least 96 px): with a
  three-line message the log gets about 36 % of 375×812; a 30-word line under a thought takes the card to ~380 px and
  the log shrinks, the line is never cut.
- **Routing:** `/ui/` is Home, `/ui/?file=games/x.json` a game (plus `at`, `mode`, `debug`, `live`). Opening a game or
  going home pushes a history entry, so the browser's back and forward move between them; the old `index.html` at the
  root redirects to `/ui/` keeping the query.
- **Live:** `view.py` (and `game.py --serve`, which imports its handler) serves `/games/index.json`: one summary per
  saved game in `games/` (not `games/lab/`; dry runs, fixtures and `latest.json` skipped), cached by mtime and size, a
  file caught mid-write keeps its last summary. A game is live when it has no end event and its file changed in the last
  2 minutes; an unfinished file older than that is left out. The viewer polls the index every 5 s and a live game file
  every 1 s; when the game ends the end card offers the next game as soon as the index lists it. The ending plays at
  1×; if the viewer is more than 20 stops behind when the `end` arrives, a small `Jump to the end` button sits by the
  LIVE chip until the end card. Clocks and night actions are never shown, so a day cut short ("the table leans"), a
  night with no doctor (night 1) or a death with no host aside change nothing in the replay.
- Short frames (≤ 720 px tall) also tighten the end card so the recap and `Watch again` stay in view.
- Nothing overlaps a label; no page scroll; seats keep ≥ 8 px from the frame edge. Checked at 1440×900, 1024×768,
  800×600, 768×1024 and 375×812 with `games/ui-fixture-7-stress.json` (a 20-word line under a two-line thought, a reply,
  a 3 / 2 / 2 vote of seven, the reveal, last words, a note, ghost lines, night, the end).

### 7.1 Layout rules checked by the audit (2026-11-15)

Rules, from Apple HIG, Material and WCAG 2.2 as collected in the UI/UX guideline set the project uses:

1. **Nothing covers anything.** No text or face may sit under another element, at any size. Deliberate exceptions, all
   badges: the faces of a pile overlap each other, the claim badge sits on its portrait's rim, the role card flips over
   its own back, the end card lies over the dimmed table.
2. **Everything is reachable.** No content below or beside the screen unless its box scrolls; no horizontal page scroll.
3. **Touch targets are 44 px** in both directions (the scrubber is a 44 px strip, the evening arrows 44 px on phone, log
   entries that jump the replay are at least 44 px tall).
4. **No text under 12 px**; body and log text 15–16 px on phone.
5. **One primary action per screen** (Home: `Watch the best game →`; a game: play).
6. **Floating controls do not sit on content**: `Back to live ↓` is a bar under the log, not a button over its last line.
7. **Three compositions, chosen by the frame**: wide (≥ 760 px wide, ≥ 440 px tall, ratio ≥ 1.2: table with the card in
   its middle, log column), stack (portrait: cast grid, card, log), and short (under 440 px tall and ≥ 520 px wide, a
   phone on its side: one header row without the scrubber, the cast as two columns of one-line seats at the left, the
   card at the right, no log; under 700 px wide the status text goes too).

**The audit.** `games/lab/ui-audit.js` measures one page: for every text and image it asks the browser what is really
painted at three points of it (`elementFromPoint`), and reports anything covered, clipped, unreachable, under 12 px, or
a control under 40 px. `games/lab/ui-audit-run.js` opens Home and nine moments of a game (a line, a whisper, the vote in
Watch and in Guess, last words, the card turn, a comment from beyond, a long line, the end card) in hidden frames at
twelve sizes from 320×640 to 1920×1080, both phone orientations included. To run it: serve the viewer, open `/ui/`, and
in the browser console run `eval(await (await fetch('/games/lab/ui-audit-run.js')).text()); await
__audit([[1366,768],[375,812],[812,375]], __urls('fun9-1'))`. State on 2026-11-15: clean at 12 sizes × 10 screens. It
found and this round fixed: seat names under the card on a sideways phone (and seats and card cut off there), a game
row's meter under the killers' faces on Home between 520 and 820 px, `Back to live` over the last log line, the
scrubber at 24–30 px and the evening arrows at 36 px.

## 8. Accessibility
- Keyboard: Space play/pause, ←/→ step, Enter on a log entry jumps there. Focus rings visible (2 px accent).
- Colour is never the only signal: role rings also carry a label; the speaker and the addressee are named on the card;
  the tally carries faces and a number.
- Live regions: the spoken line and the narrator are `aria-live="polite"`.
- Hit targets ≥ 44 px. Text zoom to 200 % must not break the card (it scrolls inside itself).

## 9. Voice (copy)
- Short, concrete, present tense. "Terra is out. Terra was the officer." Not "Player eliminated".
- Labels state the fact, never explain the UI: "from beyond · only you can hear", "found in the morning".
- Model names shown as the product would: "Claude Haiku 5.5", "GPT-6 Sol", "Gemma 4 26B · local".

## 10. Don'ts
No arrows across the table. No more than one glow. No pills for everything (pills are for state, not for labels). No
emoji in UI chrome (the moon in the phase pill is the one exception). No gradient text. No bouncing. No sound by default.
