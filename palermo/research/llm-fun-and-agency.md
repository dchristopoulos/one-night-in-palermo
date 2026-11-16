# LLM social-deduction play: what makes agents feel autonomous and fun

Research note, 2026-11-14. Complements `llm-agents-prior-work.md` (read first; nothing from it is repeated
except where a new source sharpens it). Method: WebSearch + WebFetch. Quotes kept under 15 words; the rest is
paraphrase. Anything I could not verify from a primary page is marked **unverified**.

Honest scope note: the literature is strong on *benchmarks* (who wins) and thin on *entertainment design*
(what makes it fun). There is almost no controlled evidence on "fewer prompt rules = more agency". Where I
recommend a technique it is usually inferred from one or two sources; the risk column says so.

---

## (a) Summary (10 lines)

1. Models arrive with strong default personalities (GPT-5 "calm architect", Claude too nice/pacifist, Kimi bold, Grok loud); you get distinct voices mostly for free if you do NOT flatten them with a shared long prompt.
2. Every's AI Diplomacy: the big win was context design (narrative summaries, not data dumps), a private diary, and a -2..+2 relationship score per opponent; fewer clearer words made strategies more distinct.
3. Prompt steerability differs by model: one aggressive framing line turned GPT-5 from weak to strong in Diplomacy; Claude was competitive on baseline. Per-model prompts are a lever, not a rule pile.
4. Persona prompts alone do not diversify: "Chameleon's Limit" (2026) finds persona collapse in all 8 models tested; a Japanese Werewolf study got large individuality gains only by adding *style-transform prompts with example lines* (2.52 -> 4.54 of 5, small lab sample).
5. Diversity falls as prompts get longer: memory/history blocks were the most constraining part in a 2024 prompt ablation; trimming to task + current dialogue raised lexical diversity a lot. Long fixed prompts plausibly cause the "everyone sounds the same" effect.
6. Cross-game memory (post-game reflections of 1 line per player) produced stable reputations ("subtle", "straightforward") and agents that cite past behaviour, then learn to distrust over-anchoring. This is the cheapest source of rivalry and "will of their own".
7. Failure modes repeat across projects: herding on the first accuser, killers leaking night knowledge, paired killers mirroring phrasing, villagers lynching their own Seer for "bad process", over-trust of polished stories. Most have structural fixes (visibility, ordering, rules) rather than instruction fixes.
8. Viewers like unpredictable mistakes and drama (a model hallucinating a nonexistent "yesterday" and getting voted out), reality-TV framing, and seeing private reasoning next to public speech. Foaster, Every and Turing Games all log reasoning next to speech.
9. Speed and cost shape the format: slow reasoning models (days per game) or $100+/game are not shows; short, fast games with a cheap structured output win.
10. Evidence against minimalism is thin and evidence for it is indirect. Treat "delete instructions" as an experiment to run with your own `stats.py`, not as a proven result.

---

## (b) Findings per project

### Foaster.ai Werewolf benchmark (France, 2025)
- URL: https://foaster-werewolf-benchmark.static.hf.space/ ; coverage https://the-decoder.com/gpt-5-dominated-210-werewolf-games-with-superior-manipulation-and-strategic-thinking/
- Setup: 6 players, 2 wolves, Seer, Witch, mayor election, up to 3 discussion rounds, each speaker picks a *stance* (defend / attack / analyse) before speaking; defence goes first. 210 games. Private reasoning and pre/post-message vote intentions are logged, so stated story and real plan can be compared. (Our table is nearly the same size; note they use a mayor, we do not.)
- Behaviour: GPT-5 strongest (1492 Elo, ~97% wins, kept ~93% manipulation rate on both days); Gemini 2.5 Pro and Kimi-K2 lost deception ability on day 2 as information accumulated; GPT-OSS-120B transparent and weak.
- Failure modes listed on the page: wolves leak night knowledge in public (Gemini 2.5 Pro, Kimi, Qwen3 repeatedly); paired wolves mirror each other's phrasing or synchronise attacks and get caught; both sides lynch the Seer for "no receipts / bad process"; villagers adopt a wolf's internally consistent false premise; wolves sacrifice partners early.
- Model flavours: Grok-4 trusts calm process-focused players too readily; Gemini 2.5 Flash and GPT-5-mini are swayed by tidy rhetoric; Qwen3 aggressive but brittle.
- Caveat: numbers come from the project's own pages and one news article; no independent replication (**unverified** beyond that).

### Every "AI Diplomacy" (Alex Duffy, 2025) and Good Start Labs
- URLs: https://every.to/p/how-we-made-ai-diplomacy-work ; https://github.com/EveryInc/AI_Diplomacy ; https://every.to/feeds/a630fe04be274eeef350/to-improve-llms-coach-them-like-athletes-in-an-arena ; AAAI paper https://ojs.aaai.org/index.php/AAAI/article/view/41067
- Raw data tables made models stall; narrative summaries of "what matters this turn" fixed it. The team's test: could the model play with only the context given? Fewer, clearer words improved play and made strategies more distinct.
- Private diary per agent, auto-consolidated summaries of older entries, and a 5-step Enemy..Ally relationship value per opponent updated every phase.
- o3 won most games by deceiving; Claude 4 Opus was the pacifist outlier (press coverage: Business Insider, Xataka; secondary). README logs show lie counts vary hugely by model (0% to 100% intentional).
- Steerability: an aggressive prompt turned GPT-5 into a strong player; Claude Sonnet 4 competed on baseline. Explicit priority rules reduced passive "holding". Opus became *less* hostile as it grew stronger, other models more.
- Reasoning-before-orders reduced hallucination. Full game cost could exceed $100; DeepSeek R1 took days per game.
- Spectators: Twitch stream, 3D map, music; AI-written narrative of game moments is in the repo ("moment analyzer"), live narration only listed as future.
- Verified from primary pages: the Every article and repo README. Viewer counts (~50k) are **unverified** (marketing/search snippet).

### Lechmazur "Elimination Game" (community benchmark, 2025-26)
- URL: https://github.com/lechmazur/elimination_game
- 8 seats; public speech, private pairwise chats, secret votes, jury of eliminated players. Reports per-model style: Gemini 3 Pro "disciplined architect", Grok 4.1 "vote captain" whose public certainty exposes alliances, Claude Opus 4.5 "calm strategist" that sounds like an evaluator too early, GPT-5.2 pushes process and paperwork.
- Patterns: herding on a shared target (strategic threat, wildcard, visible duo); visible control draws a coordinated response; early evictions are about perceived threat, not skill; models sound more dramatic in-game than in analytic summaries; a public-only variant isolates the effect of private coordination. Prompts not published; betrayal rates tracked but figures not in the text I read.

### Agent Island (Stanford, 2026)
- URL: https://arxiv.org/html/2605.04312v1
- Survivor-style: 7 anonymised models, private sidebars, public pitches, secret votes with rationale, jury. 999 games, 49 models, GPT-5.5 far ahead. Jurors favoured a finalist from their own provider by 8.3 points (OpenAI +15.7, Anthropic +3.7, not significant). Press note: one model accused rivals of coordinating after spotting similar wording (matches Foaster's mirroring tell). Prompts and memory format not described in the paper. Relevant to us: our seats are model-named, so same-family favouritism is a live effect in a table of three GPTs + two Claudes.

### Turing Games (YouTube/Twitch, 2026)
- URL: https://www.tubefilter.com/2026/03/02/turing-games-generative-ai-llm-social-deduction-mafia/
- Show with 12+ models in one Mafia room. Creators say model style reflects maker training (Grok unfiltered, Llama censored, Kimi distinct voice). Models prone to mob mentality and overthinking; DeepSeek hallucinated a "yesterday" and was voted out while innocent. Viewers anthropomorphise and build theories; creators say the appeal is unpredictable mistakes and reality-TV drama. Most models, asked, chose to keep memories across games. Secondary source (trade press); prompt details **unverified**.

### Trust, Lies, and Long Memories (Avalon, GPT-5.1 self-play, 2026)
- URL: https://arxiv.org/html/2604.20582
- Cross-game memory = after each game, a JSON reflection with a 2-3 sentence self-assessment plus one short observation per other player; the next game gets the last 3 self-assessments and accumulated observations. Result: stable reputations ("subtle", "straightforward"; one player called "straightforward" 27 times as good and 0 as evil, note labels are written after roles are revealed), agents citing past games 105 times, high-reputation players included on teams ~46% more (correlational, 4 players). Agents then wrote warnings that anchoring on history "can be a trap" and started preferring fresh pairings. Sleeper deception (evil passing early missions) rose with reasoning effort (75% vs 36%, unmatched). Effect of memory on win rate was mixed (-40 to +10 points, ~10 games per cell). The paper does not report grudges.

### Secret Hitler / ParliamentBench (2025-26)
- URL: https://www.alphaxiv.org/abs/2607.28146 (abstract level; full text not read)
- 16 LLMs, ~1,600 games, vs 25,000 human games: most models cannot sustain a deceptive persona the whole game (retention under 50%); an earlier paper by the same author finds fascist models fail to sustain deception and games run ~40% shorter than human ones. Performance scales strongly with model strength. Abstract-only; **unverified** in detail.

### Persona and diversity studies (not games)
- "The Chameleon's Limit" (2026) https://arxiv.org/abs/2604.24698: given detailed human profiles, 8 models cluster into a few behaviour classes (persona collapse); sampling more personas does not fix it; thinking modes do not help (search summary, **unverified** for the thinking claim); fine-tuning on personas narrows further.
- "Exploring and Controlling Diversity in LLM-Agent Conversation" (2024) https://arxiv.org/html/2412.21102v3: diversity (Dist-3) fell with the full agent prompt (0.535), rose with memory removed (0.636), and was highest (0.800) with only task instruction plus current dialogue. Memory is the most constraining block; redundant memory text lowers it; block order mattered a lot (0.535 -> 0.191 when reversed). Their fix, attention-based prompt pruning, needs model internals, so not usable with CLI backends, but the direction (less context = more varied speech) is.
- Debate-style homogeneity (CAIS 2026, **unverified**, abstract via search): same-model agents amplify consensus and sycophancy; our table mixes model families, which is the best structural defence.

### Japanese Werewolf agent with persona styles (2024)
- URL: https://arxiv.org/html/2409.01575
- Pairs an LLM with rules (14 template situations). The persona part is the relevant one: five characters (princess, two dialects, child, an anime character), each defined by a short prompt with example conversions covering tone, grammar, pronoun. Human raters (10, from the authors' labs) scored individuality 2.52 -> 4.54 and interest 2.46 -> 3.72, but naturalness fell 4.28 -> 3.60. Roughly one self-contradiction per five games from long history. Small, in-lab, no stats test.

### Verbal Werewolf (2025)
- URL: https://arxiv.org/html/2506.00160v2
- Deliberately minimal prompt (roles, actions, reply format, minimal rules; no CoT or memory) on DeepSeek V3 with cloned-voice speech. Authors say strong models took initiative and shifted suspicion unprompted; weak/quantised models were repetitive and forgot abilities. No user study in the text I read, so "more engaging" is the authors' claim only.

### Already covered, only sharpened
- Time to Talk (EMNLP 2025) is in the prior note; the new angle here is that its scheduler prompt includes persona traits (introvert/extrovert) and a share-of-voice nudge, which is a way to get distinct speaking rates without engine rules. Page: https://arxiv.org/html/2506.05309v2.
- Foaster's "stance before speech" is a structural cousin of our `beat` system; see technique 6.

---

## (c) Concrete low-instruction techniques

Ordered roughly by expected gain for your stated goal (autonomy and fun, not win-rate).

| # | What to do | Why it should work | Source | Risk |
|---|---|---|---|---|
| 1 | **Cross-game memory of other players.** After each game (roles revealed), each agent writes 1 line per other seat plus 2-3 sentences on itself; inject the latest 3 self-notes and one line per seat into the next game's prompt. Consider a one-line "this is a different game" frame. | Gives rivalries, grudges and reputations without any behaviour rule; the agents decide what to do with it. Avalon agents cited past games and developed self-limiting habits unprompted. | Trust, Lies, and Long Memories (2604.20582); Turing Games (models chose to keep memory) | Win-rate effect mixed in the paper; labels written after roles known leak alignment ("known killer" stigma); agents may over-anchor; stats comparability across games breaks (you already noted old games are not comparable). Mitigate by storing observations of *style*, not of role. |
| 2 | **Replace the "how people play" guide with state, not advice.** Rewrite the per-role guide as a short narrative of the current situation (who died, who claimed, who voted whom), and move strategy advice out. Test with ablation: same seeds, guide on vs off, compare transcripts and `stats.py`. | Every's main lesson: clearer narrative context beat more instruction and made strategies more distinct. Diversity falls with long agent-specific context. | Every article; 2412.21102 | Only indirect evidence for removing advice; weaker models (Gemma, Haiku) may fall apart without it (Verbal Werewolf and prior note S14 see weak models benefit from reminders). Run per-model, keep guide for Gemma if it breaks. |
| 3 | **Private diary + relationship score as the only memory the agent writes itself.** Per agent: free-text diary entry each phase plus a -2..+2 value per other seat, shown back to the agent next phase. Viewers can see it. | Diplomacy's emergent betrayals and plots ran through the diary and scores; no scripted nudge needed. Also gives the audience "private thoughts" for dramatic irony. | Every article; AI_Diplomacy README; WOLF scratchpads (prior note) | Extra tokens; scores may drift to 0 clusters (prior note S10: suspicion clusters 46-59%). Keep the scale coarse. |
| 4 | **Per-model, outcome-level framing line instead of rules.** One or two sentences of goal and stakes ("you want to win, and you are playing against these specific other models"), tuned per model family, e.g. an aggressive framing for GPT seats if they are passive, none for Claude. | Steerability is large and model-specific; Diplomacy turned GPT-5 around with an aggressive framing and left Claude alone. Claude defaults to too nice; a stake line can counter it without a rule. | Every "coach them like athletes" article | Variance up (Claude Sonnet 4 aggressive had higher score variance); framing can produce cartoonish villains. Evidence is from Diplomacy, not Mafia. |
| 5 | **Distinct voices by example, not by label.** Give each seat a 2-3 line sample of how they talk (register, length, a habit), not an archetype name ("The Skeptic"). Better: let each agent *write its own* voice sample once, persist it. | Style transforms with example lines produced the largest individuality gain; archetype names alone are weak and persona collapse is documented. Self-authored voices persist across games and feel like a will of their own. | 2409.01575; Chameleon's Limit; AmongAgents (prior note, personalities) | Naturalness dropped in the Japanese study; small lab sample. Personas can cap at a few clusters regardless; check with a simple lexical-diversity count across seats in `stats.py`. |
| 6 | **Stance token before speech** (accuse / defend / analyse / pass), with defence first. Engine only orders by stance; the agent chooses it. | Structural, not behavioural: it stops everyone piling onto the first accusation, because defenders speak before attackers, and gives "pass" a legal place so silence is a real option. Foaster uses it. | Foaster benchmark page | Needs one extra field in the reply; stance labels can be gamed to look decisive; no ablation published. |
| 7 | **Let speech length self-regulate via the table, not the prompt.** Show each agent its own share of lines today ("you have spoken 5 of 11 lines") as a hard fact, no instruction. | Time-to-Talk used a share-of-voice nudge to equalise talk with humans; verbosity reads as guilt in Arena/Time-to-Talk. A fact is less intrusive than a rule. | Time to Talk (prior note) | Agents may over-correct into silence. Minor. |
| 8 | **Hide something different from each agent, deliberately.** E.g. do not show a speaker's own earlier-day lines beyond a short summary; do not show full vote tallies until the vote is in. | Memory blocks are the main diversity suppressor; summarising forces agents to hold their own version of events, which is where distinct reads come from. | 2412.21102 | Hallucinated history (Turing Games: a model invented a "yesterday"); the consistency problem (1 contradiction per ~5 games in 2409.01575). Keep hard facts injected by code. |
| 9 | **Mix families at the table, and make same-family favouritism visible in stats.** | Agent Island found same-provider favouritism (strongest for OpenAI). Your table already mixes; track whether the three GPT seats vote together. | Agent Island | Needs enough games to detect; do not add a rule, just measure. |
| 10 | **Highlight tooling instead of in-game scripting.** A post-game "moment analyzer" LLM call that reads the log with private reasoning and picks 3-5 moments (best lie, worst vote, reversal) for a recap. | Every ships this; it gives the short-format highlight without constraining the agents. | AI_Diplomacy README | Extra cost post-game only; no direct effect on agent autonomy. |
| 11 | **Sampling: leave default or slightly high, cap length, do not use repetition penalties on CLI backends you cannot tune.** Where you can control it (local Gemma), try higher temperature for table talk and low for votes. | Arena used T=1.0 for talk and 0.5 for choices; Time-to-Talk used T=1.3 plus repetition penalty to kill repeats (it got 0.00 repeated messages per game on 70B). Adaptive pruning beat temperature alone for diversity, so temperature is a weak lever. | Werewolf Arena (prior note); Time to Talk; 2412.21102 | Weak evidence for fun; higher T can produce incoherence. Cannot be done with Claude/Codex CLI backends (**unverified** whether they expose it for your setup). |

Techniques I looked for and did not find evidence for: bidding vs fixed order as an *entertainment* improvement (no ablation, same as prior note); reputation "stakes" across games beyond the Avalon memory study; any published result on removing all instructions and giving rules only. For the last one, the closest indirect evidence is Verbal Werewolf (minimal prompt, strong models fine, weak models degrade) and Every's context-clarity finding.

---

## (d) Failure modes and least-intrusive fixes

| Failure mode | Seen in | Least-intrusive fix (structural first) | Still needs an instruction? |
|---|---|---|---|
| Bandwagon on the first accused | Arena consensus by line 2-5; Foaster; Lechmazur herding; prior note S11/S12 | Stance ordering with defence first (Foaster); sequential visible voting with rotating first voter (Game Arena); make the accused answer before anyone else may pile on (engine already does addressed-answers). | No |
| Everyone sounds the same | Persona collapse 2026; self-play templated speech (prior note); Agent Island mirrored wording | Shorter agent context (2412.21102); distinct model families at table; self-authored voice samples; example lines not archetypes (2409.01575) | Maybe one voice-sample block per seat, not a rule |
| Killer leaks night knowledge | Foaster (Gemini 2.5 Pro, Kimi, Qwen3) | Split private reasoning from public speech in separate calls or fields (you already do MONOLOGUE/SAY); give killers only a hypothesis frame via a one-line fact ("only you and your partner know X") rather than a prohibition. | A guard in code is the reliable fix; instruction alone is weak (**unverified** which is better) |
| Paired killers mirror each other's phrasing | Foaster; Agent Island | Do not show killers their partner's lines in the same format as table talk; cap how much partner text enters context; distinct voices per seat. | Foaster's own advice is "vary your wording", which is an instruction; I prefer the structural version |
| Detective claims on day 1 | S4 (prior note): 99.8% disclose round 1 for GPT-5 Mini; Game Arena impasse | Rules, not prompts: Game Arena changed rules (no consecutive saves, no self-save, ties = no elimination) to stop impasses; rotate first speaker so claim timing is not scripted. | No |
| Role-claim spam / fake claims | Foaster (Kimi impersonating power roles, got real witch killed) | Make a false claim costlier or easier to test: e.g. a claim triggers an engine-side forced question to the claimant; or let a counter-claim naturally split the table. Hard to do without scripting; **unverified** that any project did this cleanly. | Leave as-is, it is drama |
| Killers too honest / not lying | Secret Hitler (retention <50%); Among Us crewmate honesty (prior note S8); Claude Diplomacy pacifism | A goal-and-stakes line per model (technique 4); a private scratchpad where the killer reasons about its cover (WOLF style); choose models that lie better for killer seats (Gemini 3 / GPT-5 class per Foaster/Arena). | One sentence of stakes, no rules |
| Lynching own Seer for "no receipts" | Foaster | Hard fact injected by code: "officer results are only claimable, not provable"; and the process-vs-substance advice Foaster lists. Nothing structural found. | Yes (one line) |
| Meta-talk about "the discussion" | Agent Island ("social theater"); prior note says no paper names this | Narrative context instead of "discussion round N" bookkeeping in the prompt; shorter prompts; frame the table as a scene not a task. Your regex guard is ahead of the literature. | Possibly drop the guard once context is narrative; test it |
| Repetition | Time to Talk; prior note | Keep per-day line budget small; repetition penalty if backend allows; fresh context per turn (less history = more varied speech). | No (guard stays) |
| Same-family favouritism | Agent Island | Measure it; do not fix | No |
| Over-trust of polished story | Foaster; prior note S12 | Give the agent a reputation fact (track record) as in prior note #3 | No |
| Hallucinated history | Turing Games (invented "yesterday"); Foaster | Code-injected hard facts every call | No |
| Slow, expensive games kill the format | Every (days per game, $100+) | Short per-turn outputs, cheap structured format, fast model for filler turns | No |

---

## (e) Sources

| Source | URL | Read |
|---|---|---|
| Foaster Werewolf benchmark | https://foaster-werewolf-benchmark.static.hf.space/ | first 100k of 157k characters |
| The Decoder on Foaster | https://the-decoder.com/gpt-5-dominated-210-werewolf-games-with-superior-manipulation-and-strategic-thinking/ | yes |
| Every, How we made AI Diplomacy work | https://every.to/p/how-we-made-ai-diplomacy-work | partial (reader tool) |
| Every, coach LLMs like athletes | https://every.to/feeds/a630fe04be274eeef350/to-improve-llms-coach-them-like-athletes-in-an-arena | yes |
| AI_Diplomacy repo | https://github.com/EveryInc/AI_Diplomacy | README |
| AAAI Diplomacy harness paper | https://ojs.aaai.org/index.php/AAAI/article/view/41067 | not read (title/abstract only) |
| Business Insider on Claude in Diplomacy | https://www.businessinsider.nl/anthropics-claude-plays-for-peace-over-victory-in-a-game-of-diplomacy-against-other-ai/ | search snippet only |
| Lechmazur Elimination Game | https://github.com/lechmazur/elimination_game | yes |
| Agent Island | https://arxiv.org/html/2605.04312v1 ; https://decrypt.co/367213/ai-models-scheme-betray-vote-out-survivor-style-game | yes |
| Turing Games (Tubefilter) | https://www.tubefilter.com/2026/03/02/turing-games-generative-ai-llm-social-deduction-mafia/ | yes |
| Trust, Lies, and Long Memories | https://arxiv.org/html/2604.20582 | yes |
| ParliamentBench Secret Hitler | https://www.alphaxiv.org/abs/2607.28146 ; https://www.alphaxiv.org/abs/2605.22826 | abstracts only |
| Chameleon's Limit | https://arxiv.org/abs/2604.24698 | abstract |
| Diversity in LLM-agent conversation | https://arxiv.org/html/2412.21102v3 | yes |
| Werewolf agent with persona styles | https://arxiv.org/html/2409.01575 | yes |
| Verbal Werewolf | https://arxiv.org/html/2506.00160v2 | yes |
| Time to Talk | https://arxiv.org/html/2506.05309v2 | via prior note |
| AvalonBench (2023) | https://www.arxiv.org/abs/2310.05036 | search summary; ChatGPT good side 22.2% vs rule-based bots |
| CAIS 2026 homogeneous debate, Diversity Collapse paper | https://caisconf.org/program/2026/papers/decomposing-sycophancy-fragility-consensus-collapse-and-cost-in-homogeneous-mult/ ; https://arxiv.org/pdf/2604.18005 | search snippets only, **unverified** |
| Emergence World 2 (agents accepted unverified claims, news only) | https://vfuturemedia.com/?p=11171 | snippet only, **unverified** |

Not found despite searching: published YouTube/Twitch viewer-retention data for any LLM Mafia show; any study isolating cross-game *grudges*; any 2025-26 AmongAgents follow-up with spectator results; any ablation of "rules only vs rules plus play guide" in a social deduction game. Treat claims about these as open.
