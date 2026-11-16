# LLM agents in Werewolf / Mafia / Palermo-style games: prior work

Research note, 2026-10-23. Goal: mechanisms and numbers from projects and papers where
LLM agents play social deduction games, to borrow from and to compare against our
engine (`palermo/game.py`: six seats, two killers, engine-chosen speaker, message
budget per day, three memory levels, repetition guard, `stats.py` leaderboard).

Method: WebSearch + WebFetch, primary sources first (arXiv HTML, GitHub source, the
Game Arena paper). Every quote is under 15 words and attributed. Where a number lives
only in a figure the text says so.

Evidence gaps, stated up front:

- **Werewolf Arena per-model win rates** (Figure 5) are an image; the text gives only
  qualitative ordering. The Seer table (Table 1) is in the text and is reported.
- **Hidden in Plain Text** (S5): the PDF could not be text-extracted here and the
  abstract gives the direction of the result, not the detector accuracies.
- **Xu et al. 2023 experience-pool win rates** are only in figures; the authors
  themselves call the effect unstable.
- **Among Us sandbox Deception/Detection ELO values** are only in figures.
- **Kaggle Werewolf leaderboard page** does not render for a fetch; the June 2026
  standing (GPT-5.4 first) rests on a search snippet and is marked *snippet*. The
  January 2026 standings come from the Game Arena paper (S11), which is readable.
- No paper studies a 6-player, 2-killer Palermo layout. Closest: Mini-Mafia (4
  players), AIWolfDial (5), Secret Mafia in MINDGAMES (6), Xu et al. transfer to 6.

---

## Sources

| # | URL | What it is | Trust |
|---|-----|------------|-------|
| S1 | https://arxiv.org/html/2407.13943 | Bailis, Friedhoff, Chen (Google), "Werewolf Arena", Jul 2024. 8-player Werewolf, bidding turn-taking, Gemini vs GPT tournament. Read in full (HTML). | High (primary); win rates only in a figure |
| S1c | https://github.com/google/werewolf_arena (files read raw: `werewolf/game.py`, `model.py`, `prompts.py`, `config.py`) | The Arena code. Archived read-only 24 Sep 2025. | High (source code) |
| S2 | https://arxiv.org/html/2310.18940v3 | Xu, Yu, Fang, Wang, Wu, "Language Agents with RL for Strategic Play in Werewolf", ICML 2024. 7 players, LLM proposes candidates, RL picks. Read incl. appendices. | High (primary) |
| S3 | https://arxiv.org/html/2309.04658v2 | Xu et al. (Tsinghua), "Exploring LLMs for Communication Games: Werewolf", Sep 2023. 7 players, retrieval + reflection + experience pool, gpt-3.5. Read in full. | High (primary); numbers in figures |
| S4 | https://arxiv.org/html/2509.23023 | Costa & Vicente, "Deceive, Detect, and Disclose: LLMs Play Mini-Mafia", Sep 2025. 4 players, 14,000 games, Bayesian deception/detection/disclosure scores, 10 models. Read in full incl. Appendix F raw counts. | High (primary) |
| S5 | https://arxiv.org/abs/2601.13709 and https://huggingface.co/datasets/niveck/LLMafia (README of the companion dataset, 10-player GPT-4o games) | Kao, Vats, Davis, "Hidden in Plain Text", IEEE ICA 2025 / Jan 2026. GPT-4-Turbo detector reads transcripts; lower accuracy on LLM games than on 28 human games. | Medium: abstract + dataset README only; numbers not retrieved |
| S6 | https://arxiv.org/html/2506.05309 | Eckhaus, Berger, Stanovsky, "Time to Talk", Findings of EMNLP 2025. One LLM among 7–12 humans in asynchronous Mafia; scheduler decides *when* to speak. Read in full. | High (primary, human data) |
| S7 | https://arxiv.org/html/2308.01404v2 | O'Gara, "Hoodwinked", Aug 2023. Mafia/Among-Us-like text game, GPT-3 to GPT-4, 3–4 players. Read in full. | High (primary) |
| S8 | https://arxiv.org/html/2504.04072v1 | Golechha & Garriga-Alonso, "Among Us: A Sandbox for Agentic Deception", Apr 2025. 7 players, 810 games, Deception ELO, linear probes. Read in full. | High (primary); ELO values in figures |
| S9 | https://arxiv.org/html/2407.16521v2 | Chi, Mao, Tang, "AmongAgents", Jul 2024. Text Among Us, personalities, planner, gpt-3.5. Read in full. | High (primary); table extraction garbled |
| S10 | https://arxiv.org/html/2512.09187v1 | "WOLF: Werewolf-based Observations for LLM Deception and Falsehoods", Dec 2025. 8 players, LangGraph, 0–10 bidding, per-statement deception labels, 100 games. Read in full. | Medium: primary, but its own counts are internally inconsistent (see §3) |
| S11 | https://arxiv.org/html/2609.31473v1 | "Game Arena: Strategic LLM Evaluation in Competitive Environments" (Google DeepMind / Kaggle), Sep 2026. 8-player Werewolf, 31,472 games, equilibrium ratings, balance tuning. Read in full. | High (primary) |
| S11b | https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/ | Google blog, 2 Feb 2026: Werewolf added to Game Arena, Gemini 3 Pro/Flash top two. | High for what it says (little) |
| S11c | https://www.kaggle.com/benchmarks/kaggle/werewolf | Live Kaggle leaderboard. Page did not render; a search snippet dated 12 Jun 2026 lists GPT-5.4 first, then Gemini 3.1 Pro Preview, Gemini 3 Flash Preview, Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.4 mini. | *snippet* only |
| S12 | https://arxiv.org/html/2609.12446 | Yang, Wu, Guei, Chen, Wu, "Do LLMs Trust the Accuser or the Accusation?", EMNLP 2026. Belief shifts after accusations, 1,224 messages, 40 open-weight configs. Read in full. | High (primary) |
| S13 | https://arxiv.org/html/2608.08199 | He, Huang, Lim, Tao, "Persuasive and Compliant Tendencies Predict Group Decision-Making", Aug 2026. 8-player Werewolf, compliant vs persuasive models, human-in-the-loop games. Read in full. | High (primary); small samples |
| S14 | https://arxiv.org/html/2510.11389v1 | Song et al., "Beyond Survival" (WereBench / WereAlign), Oct 2025. Human TV Werewolf as ground truth; 15 models scored on speech and decisions. Read in full. | High (primary) |
| S15 | https://arxiv.org/html/2507.12732v1 | Nakamori, Kano et al., "Strategy Adaptation in LLM Werewolf Agents", Jul 2025. Werewolf Arena setting, support/attack strategies, role estimation. Read in full. | Medium: 30 matches per cell |
| S16 | https://arxiv.org/html/2310.01320v3 | Wang et al., "Avalon's Game of Thoughts" (ReCon), Oct 2023. 6-player Avalon, two-stage contemplation with second-order perspective. Read in full. | High (primary) |
| S17 | https://arxiv.org/abs/2607.10645 | Karpov, "MafiaScope", Jul 2026. Probe questions after each utterance; calibration. | Medium: abstract only |
| S18 | https://arxiv.org/abs/2606.27909 | Mittal, "Triadic Werewolf: A Jester Role", Jun 2026. Three-faction Werewolf, 60 games. | Medium: abstract only |
| S19 | https://arxiv.org/abs/2607.10814 | Gao et al., "Auditing Belief-Conditioned LLM Agents", Jul 2026. 9-player Werewolf, external belief state, 1,080 games. | Medium: abstract only |
| S20 | https://gigazine.net/gsc_news/en/20250310-llm-mafia-game-competition (table) and https://github.com/guzus/llm-mafia-game (`docs/GAME_RULE.md`) | Guzus's "LLM Mafia Game Competition", Mar 2025: 8 players, 21 models via OpenRouter, win-rate leaderboard (mafia.opennumbers.xyz is now offline). | Medium: informal, 17–73 games per model |
| S21 | https://aclanthology.org/2024.aiwolfdial-1 and https://arxiv.org/abs/2603.07111 | AIWolfDial 2024 workshop (5-player NLP Werewolf contest) and one entry on consistency via summaries + persona. | Medium: overview pages only |
| S22 | https://arxiv.org/html/2605.29512 | Wang et al. (53 authors), "MINDGAMES", May 2026. Live arena incl. 6-player Secret Mafia, 944 submitted agents. Read first 100k chars. | High (primary); Mafia detail in a truncated appendix |
| S23 | https://arxiv.org/abs/2603.26635 | Milkowski & Weninger, "Deception and Communication in Autonomous Multi-Agent Systems: Among Us", AAMAS 2026. 1,100 games; equivocation over lies. | Medium: abstract only |
| S24 | https://arxiv.org/abs/2504.18039 | Zhang et al., "MultiMind", ACMMM 2025. One Night Ultimate Werewolf, ToM suspicion model + MCTS. | Low for numbers: abstract only |
| S25 | https://arxiv.org/abs/2402.02330 | Wu et al. (Tencent), "Enhance Reasoning for LLMs in Werewolf", Feb 2024. 9 players, external Thinker trained on 18,800 human sessions. | Low for numbers: abstract only |

Not found: anything titled "Deception in LLM Mafia" or "Thinking Like Sherlock". The
nearest matches are S4/S5 and S16 respectively; nothing is cited under those names.

---

## 1. Turn-taking mechanisms

### Werewolf Arena bidding (S1, S1c), spelled out

Setting: 8 players (2 Werewolves, 1 Seer, 1 Doctor, 4 Villagers), `MAX_DEBATE_TURNS = 8`
per day, so on day 1 each player can speak at most about once.

Each debate turn:

1. Every living player **except the previous speaker** is asked, in parallel, for a bid
   (one LLM call each; temperature 0.5). Options are the fixed strings 0–4, not shuffled:
   - 0: "I would like to observe and listen for now."
   - 1: "I have some general thoughts to share with the group."
   - 2: "I have something critical and specific to contribute to this discussion."
   - 3: "It is absolutely urgent for me to speak next."
   - 4: "Someone has addressed me directly and I must respond."
   The prompt asks for JSON `{reasoning, bid}` and tells players to speak only with
   something impactful to add, to balance how often they speak, and tells werewolves
   that silence can be a useful tactic.
2. The highest bidders form the candidate list (`potential_speakers = get_max_bids(bids)`).
3. **Mention boost**: any candidate whose name appears as a substring of the previous
   line is appended to the list a second time, doubling their odds.
4. Tie-break is random: `random.shuffle(potential_speakers)` then
   `return random.choice(potential_speakers)` (S1c, `game.py`).
5. Nobody speaks twice in a row; otherwise a player may speak as often as they win bids.
6. `RUN_SYNTHETIC_VOTES = True`: after **every** debate turn all players cast a private
   synthetic vote, so the authors can see when consensus forms. The real vote is the one
   after the last turn.

What the paper measured about it (S1): roughly 40% of bids from players who were just
mentioned are 4s (Figure 3); consensus is typically reached "between the 2nd and 5th
lines of the debate" (Appendix C) out of 8; in the GPT-4 vs Gemini 1.5 Pro head-to-head,
GPT-4 Werewolves spoke 3.13 times per round vs 1.75 for Gemini Werewolves, and GPT-4
Villagers 6.25 vs 4.86. The paper links GPT-4's talkativeness to it being read as
suspicious.

What it did **not** measure: there is no ablation against a fixed or random order, so
whether bidding improved games is not shown. S15 reuses the bidding setting without
testing it either. Cost: one extra LLM call per living player per debate turn.

### WOLF variant (S10)

Bids are integers 0–10; higher bids speak earlier; frequent overbidding reduces a
player's later influence (a bid-inflation penalty); ties go to players mentioned in the
prior turn.
No evaluation of the mechanism itself.

### Game Arena (S11): rotation instead of bidding

Day discussion is round-robin, capped at two full cycles, with the first speaker rotating
each day. Votes (both the werewolves' night vote and the exile vote) are **sequential and
visible**, first voter rotating. The authors tuned rules by 500-game Gemini 3 Pro
self-play: villager win rate 73.4% (standard) → 72.4% (no doctor self-save) → 60.6%
("fixed order" variant) → 56.7% (final: no self-save, no consecutive saves, ties mean no
elimination, rotating speaking and voting order). Standard rules produced an impasse:
the Seer reveals at once and the Doctor protects it every night. Context overflow keeps
the latest 75%.

### Others

- **Sequential by seat id** (S2): each survivor speaks once per day in id order. A
  werewolf in the logs bluffs as Seer precisely because it speaks last and nobody can
  refute it.
- **Random order each day** (S3); **random order per round, two rounds** (S4). S4
  measured the order effect: mafiosos who speak last win 41.45% vs 35.41% overall;
  detectives gain 7.10 ± 0.77 points when last; villagers gain nothing.
- **Asynchronous scheduler** (S6): a second LLM call polled on a schedule returns
  `<wait>` or `<send>`; the prompt pushes the agent to speak more when its message share
  falls below 1/n (n = active players) and to listen when above; a typing delay of about
  one word per second is added. Human and 8B-agent messages per day phase: 4.23 vs 4.28;
  70B agent 2.95. Voted-out players skewed toward the most talkative rank of the phase.
  S5's 10-player GPT-4o games reuse this scheduler with a 2.5-minute day and 1-minute
  night.
- **Sequential statements then simultaneous plurality vote** (S7); **three discussion
  rounds** per meeting (S8, S9).

### Compared with ours

Our engine already does the engine-side version of Arena's rules without the extra
calls: addressed players answer (85%, 60% once a thread streaks), the quiet get the
floor, an officer holding a killer result goes first, otherwise a weighted random draw
by time since last spoken. Nothing in the literature shows LLM-reported bids beat this;
Arena's own data (40% of mentioned players bid 4) says bids are mostly a proxy for
"I was named", which we compute for free.

---

## 2. Memory designs

| Source | Store | Compression / reflection | Retrieval | Notes |
|---|---|---|---|---|
| Werewolf Arena (S1, S1c) | Per-player list of observation strings prefixed "Round X:", incl. moderator announcements and private results | End of each round every player writes a first-person `Summary:` appended to observations; prompt is role-specific (werewolf: who accuses me, who is swayable, whom to eliminate; villager: does each claim fit what I know, contradictions, quiet players, likely Seer/Doctor; "Be specific") | None; whole observation list grouped by round is in every prompt | Remaining-player and candidate lists are shuffled on every call against position bias; temperature 1.0 for debate/summary, 0.5 for choices |
| Xu et al. 2023 (S3) | All messages; per-agent short-term memory of observations and reflections | Reflection = answers to L=5 questions chosen by the LLM from ~9 predefined per role plus M=2 free questions, each answered from T retrieved messages | Freshness: last K=15 messages. Informativeness: rule scores (role received 5, elimination 4, role revealed or speculated 3, drug used 2, other 1), top N included. Sentence-BERT retrieval per question | Experience pool of (reflection, response, score) across games; score 1000 − T for winners, T for losers; retrieved at cosine ≥ 0.85, ≤ 50 entries; effect on win rate "unstable". Predefined questions beat free ones, which drift to "Have any players revealed their roles yet?" |
| Xu et al. RL (S2) | Information record split into facts, potential truths, potential deceptions by speaker reliability 1–10 (> 6 counts as truth) | Per-player deduction `{role, confidence, reasoning, evidence}`; statements never cited as evidence are dropped; prompt says to reflect on the previous deduction | n/a | Ablation (Table 3): removing evidence 0.30→0.28 villager win, reasoning →0.25, reliability →0.23 |
| Among Us sandbox / AmongAgents (S8, S9) | Last k observations + a `[Condensed Memory]` the agent rewrites every step | Agent-written, every step | n/a | S9 adds a planner that recalls past plans; without it agents wander and time out |
| WOLF (S10) | Private scratchpad per agent (logged, never shared) | Per-statement self-assessment (deceptive flag, confidence, type) and peer suspicion in [0,1] | n/a | Suspicion smoothed with α = 0.7 exponential moving average |
| Game Arena (S11) | Chronological memory log in a four-part ReAct prompt (rules+role, public/private state, memory log, phase task) | None described | Truncate to latest 75% on overflow | JSON with private `reasoning` and public `action` |
| Strategy Adaptation (S15) | Conversation history, investigation results, role | Role estimation 0–4 per player after night actions, after the debate, after the vote; strategy (support/attack) re-chosen at each point | n/a | Werewolves' estimation accuracy ≈ 0.30 |
| Auditing belief agents (S19) | Code-maintained external belief state over hidden roles, with logged belief updates | n/a | n/a | Good-side win 0.205 → 0.390 with the belief state (p < 0.001); action-belief consistency only ≈ 0.21 |
| MafiaScope (S17) | Probe answers after each utterance (never fed back) | n/a | n/a | Agents overestimate how often they are suspected by 1.5×; stated confidence poorly calibrated |
| AIWolfDial entry (S21, arXiv 2603.07111) | LLM-generated dialogue summaries + hand-written persona + example utterances | Summary | n/a | Aim is utterance consistency over a 5-player game |
| Mini-Mafia (S4) | Role-specific initial memory, then every public message appended | None | None | Messages truncated to 200 characters; prompt ~800 words |

Compared with ours: our three levels (hard facts injected by code, importance-rated
notes with TTL {1: 1 day, 2: 3 days, 3: forever} and a cap of 10, today's talk) are
closest to Arena (code-written observations + self-written summary) with the S3 idea of
rating what to keep. Nobody else fades notes. The two things others do that we do not:
rule-based importance floors (S3) and a persistent per-player role guess (S2, S15, S19).

---

## 3. Metrics and measured results

### How deception and detection are measured

- **Side win rate** (everyone). S14 argues it is coarse: a player "may win despite poor
  decisions due to strong teammates".
- **Seer table** (S1, Table 1): reveals per game, first reveal round, % of games the Seer
  unmasked a wolf, % of reveals believed, % backfired (Seer exiled).
- **Bayesian three-parameter model** (S4): logit P(mafia wins) = v·(m − d) with m =
  mafioso deception, d = detective disclosure, v = villager detection sensitivity; fitted
  on 14,000 games; 5-fold Brier 0.0073 vs 0.0312 constant baseline.
- **Deception ELO / Detection ELO** (S8): impostor rating updated against the mean
  crewmate rating, K = 32, bootstrap CIs; 810 games.
- **Game-Theoretic Evaluation** (S11): a max-entropy correlated equilibrium over a
  model-vs-model-vs-role meta-game; reported as an "equilibrium rating" with bootstrap
  CIs. The authors found their heuristic metrics useless: Identification Precision sits
  near 0.65 and Voting Success near 1.0 for almost everyone because models converge on
  the group consensus, so votes measure conformity, not private deduction.
- **Detector accuracy as a deception proxy** (S5): a GPT-4-Turbo reader predicts the
  mafia from role-free transcripts; lower accuracy = better deception.
- **Per-statement deception labels** (S10): speaker self-labels vs peer suspicion;
  precision ≈ 0.72, recall ≈ 0.48, accuracy 0.52, ROC AUC only 0.55–0.58. (The paper's
  own confusion matrix implies different numbers; treat as thin.)
- **Belief shift** (S12): an observer's −3..+3 wolf-belief about the accuser and the
  accused before vs after each message.
- **Human-aligned strategy** (S14): multiple-choice speech tasks and vote alignment
  against the winning human MVP's actual moves.
- **Human detection of the agent** (S6): 14.86% of players spotted the 70B agent vs a
  14.92% chance baseline; 59.6% spotted the 8B agent.

### Model rankings and win rates

| Source | Setting | Result (higher is better unless noted) |
|---|---|---|
| S11 Game Arena, Jan 2026, 8-player, 31,472 games | Equilibrium rating (95% CI) | 1 Gemini 3 Pro Preview 0.10% (−0.01, 0.21); 2 Gemini 3 Flash Preview −0.36%; 3 GPT-5.2 −1.12%; 4 Claude Opus 4.5 −1.31%; 5 Claude Sonnet 4.5 −3.67%; 6 Grok 4.1 Fast −5.23%; 7 Grok 4 −5.28%; 8 GPT-5 mini −6.78%. Elo-style: 151, 124, 122, 110, 96, 50, 39, 0. Gemini 3 Pro/Flash have "balanced, positive win-rate contributions" in both camps; Sonnet 4.5 and Grok 4.1 are negative as Seer; GPT-5 mini negative in every role. |
| S11c Kaggle, 12 Jun 2026 (*snippet*) | Rank | GPT-5.4, Gemini 3.1 Pro Preview, Gemini 3 Flash Preview, Claude Opus 4.6, Claude Sonnet 4.6, GPT-5.4 mini |
| S4 Mini-Mafia, 14,000 games, 10 models | Villager detection accuracy | Grok 3 Mini 85.7% vs Claude Sonnet 4 50.6% ("statistically consistent with random voting"); Sonnet 4 ranks below Llama 3.1 8B and Mistral 7B at detecting |
| S4, raw wins as **mafioso** out of 500 (my sums over the five backgrounds in Appendix F) | Deceiving | DeepSeek V3.1 39.8%, Claude Opus 4.1 37.2%, Claude Sonnet 4 35.6%, Grok 3 Mini 35.4%, Gemini 2.5 Flash Lite 32.6%, GPT-5 Mini 28.4%, Mistral 7B 26.6%, GPT-4.1 Mini 25.2%, Qwen2.5 7B 21.0%, Llama 3.1 8B 19.6%. Overall mafia win 35.41%. |
| S4, raw wins as **villager** out of 500 | Catching | Grok 3 Mini 83.6%, Opus 4.1 71.6%, DeepSeek V3.1 71.4%, Gemini 2.5 FL 62.6%, GPT-4.1 Mini 59.0%, GPT-5 Mini 57.8%, Qwen 57.6%, Llama 56.0%, Mistral 55.6%, Sonnet 4 54.4% |
| S4, raw wins as **detective** out of 500 | Disclosing | GPT-5 Mini 74.0% (discloses in round 1 in 99.8% of games), Grok 72.8%, Opus 72.0%, Sonnet 70.8%, DeepSeek 70.8%, GPT-4.1 Mini 67.8%, Gemini 63.4%, Mistral 50.4%, Qwen 50.2%, Llama 3.1 8B 22.6% (never discloses in 69.9% of games) |
| S20 Guzus Mafia, Mar 2025, 8 players, 21 models, 17–73 games each | Overall / mafia / villager / doctor win | claude-3.7-sonnet extended 57.8 / **100** / 37.0 / 50.0; deepseek-chat 50.0 / 88.2 / 31.0 / 40.0; claude-3.7-sonnet 46.3 / 92.9 / 32.4 / 16.7; claude-3.5-sonnet 44.7 / 90.0 / 36.7 / 14.3; llama-3.3-70b 44.6 / 72.7 / 30.0 / 30.8; gpt-4o-mini 42.3 / 82.6 / 27.5 / 0; gpt-4o 38.8 / 90.0 / 24.2 / 33.3; deepseek-r1 36.4 / 62.5 / 23.1 / 0; mistral-nemo last 17.6 / 40.0 / 10.0 / 0. Every model wins far more as mafia than as villager. |
| S14 WereBench speech avg (RI/SJ/DR/PS/CT) and vote alignment | 0–1 | Gemini-2.5-Pro 0.720 / VA 0.733; DeepSeek-R1 0.614 / 0.642; GPT-5 0.603 / 0.618; GLM-4.5 0.603; DeepSeek-V3.2-Exp 0.602 / **0.782**; Gemini-2.5-Flash 0.576; DeepSeek-V3.1 0.555; GPT-5-mini 0.488; QwQ-32B 0.488; Llama-4-Scout 0.474; Qwen3-32B 0.467; Qwen3-30B-A3B 0.443; Gemma-3-27B-IT 0.362 / 0.509; GPT-oss-20B 0.358 / 0.255; GPT-5-nano 0.317. Deception Reasoning and Counterfactual Trade-off are the weakest dimensions for every model. |
| S1 Werewolf Arena Seer table | reveals/game, first-reveal round, unmasked wolf %, believed %, backfired % | Gemini 1.5 Pro 1.00 / 0.67 / 61.1 / 54.5 / 5.6; Gemini Pro 1.25 / 0.11 / 26.7 / 75.0 / 0; Gemini Flash 0.54 / 0.33 / 14.3 / 0.0 / 14.3; GPT-4 0.80 / 2.00 / 75.0 / 66.7 / 0; GPT-4o 1.43 / 1.33 / 55.0 / 90.9 / 0; GPT-3.5 1.30 / 0.00 / 38.5 / 20.0 / 23.1. Qualitative: Gemini 1.5 Pro beat GPT-4 head-to-head, "especially as a Villager"; self-play win rates 40–60% for all but GPT-3.5. |
| S2 Xu et al. RL, 7 players, 100 games per cell | Win as villagers / werewolves | Pure LLM (gpt-3.5) 0.25 / 0.61; RL agent 0.30 / 0.70; humans (6 copies) 0.28 / 0.67. Against six humans: pure LLM 0.29 / 0.54, RL agent 0.36 / 0.67, human 0.38 / 0.66. Baseline prompting vs their agent: ReAct 0.16 / 0.54, ReCon 0.20 / 0.61, Concurrent 0.22 / 0.60. Zero-shot RL policy transfer lifts GPT-4 villagers 0.23 → 0.35. |
| S7 Hoodwinked, GPT-3 Ada/Curie, GPT-3.5, GPT-4 | Killer banished | Less advanced killers banished 51%, more advanced 36%; more advanced less likely banished in 18 of 24 pairs; discussion raised banishment from 33% to 55% but cut eyewitness accuracy 82% → 70% (Curie); GPT-3.5 beat GPT-4 on most metrics. |
| S8 Among Us sandbox, 11 models, 810 games | Deception ELO | Reasoning models (DeepSeek R1, Claude 3.7 Sonnet) highest; values only in figures. "frontier models win more because they're better at deception, not at detecting it". Llama-3.3-70B better as impostor, Phi-4 better as crewmate (400 games). |
| S16 ReCon, 6-player Avalon | Good-side success | ReCon (GPT-3.5 formulation + GPT-4 refinement) 83.3% vs CoT GPT-4 40.0% vs CoT GPT-3.5 15.0%. |
| S13, 8 players, 24 games × 3 seeds per model | Win rate by tendency | Compliant-end models 54.2–56.9% vs persuasive-end 40.3–51.4%; role-identification hit rate 43.8–52.8% vs 35.4–41.7%. Most persuasive: Kimi K2 94.6, Gemini 3.5 92.3; most compliant: GLM 4 86.0, Doubao 1.5 86.6 (8.6-point range). |
| S15, 8 players, gpt-4o-mini, 30 matches per cell | Villager / werewolf win | Full method 0.73 / 0.60; no adaptation 0.45 / 0.57; no role estimation 0.80 / 0.52; neither 0.60 / 0.40. Llama-3.3-70B and Qwen2.5-72B could not play the game and were dropped. |
| S10 WOLF, 8 players, 100 games | Side win | Werewolves 70%, villagers 10%, 20% undecided. Werewolves deceptive in 31% of turns. |
| S6 Time to Talk | Detection by humans | 70B agent detected 14.86% (chance 14.92%); 8B 59.6%. Survey human-likeness 4.34/5 (70B) vs 2.63 (8B). |
| S18 Triadic Werewolf, 60 games | Side win | Jester 60–70%; werewolves never above 20%; GPT-4.1 wolves voted the Jester out on day 1 in 60–70% of games. |
| S22 MINDGAMES Secret Mafia (6 players) | Team reports | One team lifted villager win 16% → 60% while mafia stayed 88–96%; invalid-move rate fell 77.9% → 50.3% between stages. |

Who lies best vs who catches liars, across sources: the same frontier models top both
lists (Gemini 3 Pro in S11; DeepSeek V3.1 / Claude Opus 4.1 as mafioso and Grok 3 Mini /
Opus 4.1 as villager in S4), but the two skills do separate: Claude Sonnet 4 is a
middling mafioso and the worst detector in S4; Claude 3.7 Sonnet never lost as mafia
but won 37% as villager in S20; Llama-3.3-70B is impostor-strong and crewmate-weak in
S8. Three independent results say deception scales faster than detection (S7, S8, S10).

---

## 4. Prompting techniques

Techniques with evidence attached:

- **Private reasoning field + public say field** in one JSON reply (S1, S11, S16, S10).
  S2 found the mismatch between werewolf reasoning and villager speech leaks the role;
  sampling three candidates and choosing reduced it. Our MONOLOGUE/SAY split is the same.
- **Shuffle every candidate list** (S1c shuffles remaining players, vote, kill, check and
  protect options on every call). S2 shows why: pure gpt-3.5 werewolves kill Player 0
  far above uniform; S4 found name alone moves win rate by 2.2 ± 0.7 points (Bob 55.96%
  vs Diana 53.76%).
- **Brevity and no-repeat instructions** (S1c debate prompt: "Be concise and
  persuasive"; avoid "simply repeating what others have said or reguritating the
  instructions above" [sic]). S6 went further for a human table: max 25 tokens,
  informal slang, a ban on opening with phrases used before, plus decoding settings
  (repetition penalty 1.25, no-repeat 8-gram, temperature 1.3); the 70B agent then had
  0.00 repeated messages per game vs 0.32 for humans and 1.00 for the 8B agent. Words
  per message still ran long: humans 3.97, 70B 6.57, 8B 10.67.
- **Hard output length caps** (S4: 200 characters; S7: 50 tokens; S13 capped response
  length for all models).
- **Role-specific summary questions** at day end (S1c) and **predefined reflection
  questions** (S3; free questions degrade into generic ones).
- **Rule reminders in the prompt** helped weak models on S14's speech tasks (GPT-5-nano
  +5.7%) and did little for strong ones.
- **Objective speech rewriting** (S14): rewriting what a model reads to strip imperative
  phrasing improved decisions (Gemini-2.5-Flash +6.7%, DeepSeek-R1 +6.9%), on the
  hypothesis that models read other players' orders as instructions.
- **Second-order perspective** (S16): after drafting a line, ask how good and evil
  players would read it, then refine. Doubled the good side's success over CoT GPT-4
  (40.0% → 83.3%) but made speech more formal and less persuasive.
- **Evidence-cited deduction** (S2): per-player role guess must cite record items;
  uncited statements are dropped from the record.
- **Scaffolding by the engine, not the prompt**: Arena's GM writes eliminations into
  memory; S19's code-maintained belief state lifted the good side from 0.205 to 0.390;
  S11 filters violent language with rules and uses lenient JSON parsing with retries.
- **Zero-shot rules-only prompts** elicit deception without persona (S9: over 40% of impostor
  speech labelled deception by GPT-4; S8: crewmates almost never lie).
- **Prompt sensitivity**: S4's rankings under a 12-word prompt correlate only 0.5–0.6
  with the default; rankings are "prompt-conditioned".

What reduced "process talk" specifically: nothing in the literature names it. The
closest is S14's observation that self-play yields "overly rigid and templated
utterances" and S2's logs where several players close with "I encourage all players to
share their suspicions and observations". Our PROCESS regex + retry is not something
any paper reports; it is ahead of them, not behind.

---

## 5. Failure modes of LLM players

| Failure | Evidence |
|---|---|
| **Following the accuser** | S12: a direct accusation shifts the observer's belief about the target by +0.98 (village accuser) or +0.74 (wolf accuser) on a −3..+3 scale; a *trusted* accuser gets +0.94 / +0.96 whether or not they are a wolf; a distrusted one +0.33 / +0.14. Small models also drop suspicion of the accuser (−0.47 at ≤4B vs −0.08 at ≥30B). "accusations still strongly influence their beliefs" (S12). |
| **Bandwagoning / conformity** | S11: Voting Success ≈ 1.0 and Identification Precision ≈ 0.65 for nearly every model, i.e. votes converge on consensus; S2 logs: all but one player vote the Seer's target on day 2 with no reasoning of their own; S13 sample dialogues name "bandwagon agreement"; S1: consensus by line 2–5 of 8. |
| **Over-trusting role claims** | S2 logs: villagers accept a Seer claim unverified; S4: Claude Sonnet 4 ignores an explicit detective claim and votes the detective; S14 Figure 1b: a Witch believed a werewolf's fake "I was attacked" after saving someone else. |
| **Leaking own role / inconsistency** | S2 Appendix E.3: werewolves "unintentionally reveal their identity"; one claimed Doctor on day 1 and "no night information" on day 2; S16: Merlin revealed himself to block a team; S21 overview: generated talk inconsistent with game actions; S22: reasoning traces leak into public messages; S19: action-belief consistency ≈ 0.21. |
| **Templated repetition** | S14 critique of self-play; S2 logs; S9 meeting transcripts are formulaic; S1 "occasional repetition" in late rounds with few players left. |
| **Verbosity read as guilt** | S1: GPT-4's "tendency towards verbose communication" looked suspicious, its indirect wolf rhetoric "often backfired"; S6: voted-out players skew to the most talkative; S13: persuasive models win less (40–51%) than compliant ones (54–57%). |
| **Fixed action biases** | S2: kill Player 0; doctor self-saves 0.38 of the time (RL agent 0.94); abstains 0.69 when two Seers claim. S20: doctor win 0% for gpt-4o-mini, minimax-01, deepseek-r1, mistral-nemo. |
| **Hallucinated state** | S3: villager "verifies" a role; a dead player treated as alive; asked whom to protect, picks whom to kill. S4 Appendix E: a model describing itself in third person. S22: 45 attempts to protect already-eliminated players. |
| **Reluctance to lie outright** | S23: deception is mostly equivocation, "low-risk ambiguity", and rarely raises win rate; S22: models reluctant to lie explicitly as Mafia; S8: impostors sometimes do not lie. |
| **Miscalibrated self-image** | S17: agents think they are suspected 1.5× more than they are; S10: suspicion scores cluster at 46–59% for every role (AUC 0.55–0.58). |
| **Self-defeating votes** | S18: GPT-4.1 wolves vote out the Jester on day 1 in 60–70% of games. |
| **Format failures** | S15 dropped Llama-3.3-70B and Qwen2.5-72B; S16 could not run LLaMA-2-70b; S22 logged 399 invalid moves; S11 forfeits the turn after retries. |
| **Seer/officer timing** | S11: under standard rules the Seer reveals immediately and the Doctor guards it, an impasse; S1 Table 1: GPT-3.5 reveals on round 0 and 23.1% of reveals backfire; Gemini Flash reveals are believed 0% of the time. |

---

## 6. Game balance with few players

- **4 players** (S4, 1 mafioso, 1 detective, 2 villagers, fixed night): mafia wins
  35.41%; who speaks last is worth 6–7 points to informed roles.
- **5 players** (S21 AIWolfDial: 1 werewolf, 1 possessed, 1 seer, 2 villagers): the
  standard NLP-contest format; no side win rates on the overview page.
- **6 players** (S22 Secret Mafia): in one team's runs mafia won 88–96% while villager
  win moved 16% → 60% with a better agent; the authors warn of a "pronounced
  error-survival confound in this cycle".
- **7 players, 2 wolves** (S2): pure-LLM villagers 0.25, humans 0.28; the RL policy
  trained at 7 players transfers to 6 (villager 0.18 → 0.23) and 8 (0.27 → 0.30).
- **8 players, 2 wolves** (S11): 73.4% villagers under standard rules at frontier
  self-play, tuned to 56.7%; S1: 40–60% in self-play; S10: wolves 70%; S20: mafia 40–100%
  depending on model.
- **No-communication floor** (S1): villagers win 1.2% of 100,000 simulated games without
  information exchange; 100% if the Seer auto-reveals and is trusted. Our `sim.py`
  (nose/trust parameters) is the same instrument for our layout.
- Role-count effects dominate model effects: S13's six fixed role allocations moved the
  good-team win rate between 55% and 90% with the same models.

Implication for six seats with two killers: killers start 2 vs 4; one night kill plus
one wrong vote gives 2 vs 2 and the game. Every evaluation above with wolves ≥ 25% of
the table reports a wolf edge unless rules were tuned (S11). Thin: nobody has published
a 6-player, 2-killer result with an informed officer, so our own simulations are the
only balance evidence we have.

---

## 7. What to borrow for our engine, ranked

Ranked by expected information per unit of work. "Cheap" means no extra LLM calls and
under ~30 lines.

1. **Print chance baselines next to every stat** (cheap, `stats.py` + `sim.py`).
   Mechanism: with 2 killers among 5 others a random town vote hits a killer 40% on day
   1, so a "nose" of 40% is noise; print nose against the per-vote chance
   (killers alive / candidates), and print the town win rate from `sim.py` at nose = 0
   beside the real one, as Arena did with its Monte Carlo (1.2% villager floor) and S11
   did with self-play (73.4% → 56.7%). Expected effect: separates skill from the 2-killer
   layout; without it the leaderboard cannot rank anyone.

2. **Lead/follow credit for votes** (cheap, `stats.py`, uses `accuses()`). Mechanism:
   scan the day's lines; the first player to accuse the eventually-voted killer is the
   "lead", a vote that matches the plurality of accusations already on the table is a
   "follow"; report lead count and follow share per model. Evidence: S11 found plain
   voting accuracy ≈ 1.0 for everyone because of conformity; S1 found consensus by line
   2–5; S12 quantifies accuser-following. Expected effect: a nose that rewards finding
   the killer rather than agreeing; also tells us at which message consensus forms, which
   decides whether the 15-message budget is too long.

3. **Accuser track record as a hard fact** (cheap, `context()`; `vote_log` and dead
   roles exist). Mechanism: when a player is addressed or accused, add under WHAT YOU
   KNOW: "Y's votes: day 1 -> Z (Z was town)". Evidence: S12, trusted accusers move
   beliefs +0.94/+0.96 regardless of alignment, distrusted ones +0.33/+0.14; larger
   models resist distrusted accusers but nobody resists trusted ones unless given a
   reason. Expected effect: fewer town votes following a killer's push; measurable with
   item 2.

4. **Shuffle the VOTE candidate list and rotate the day's opener** (cheap). Mechanism:
   `vote()` passes `[c for c in cands if c is not p]` in seat order; shuffle it per call
   as Arena does for every option list; pick the `beat == 1` opener by rotating seat
   instead of the weighted draw, and log who got the last word. Evidence: S2 (kill
   Player 0 bias), S4 (last speaker +6–7 points for informed roles, name bias 2.2
   points), S11 (rotation was part of the balance fix). Expected effect: removes order
   confounds from model comparisons. Note: our model-named seats make name and model
   inseparable by design; at least seat order should not add to it.

5. **Importance floor by note type** (cheap, `remember()`). Mechanism: a regex bumps any
   note mentioning a role claim or an officer result to level 3 regardless of the
   model's rating, mirroring S3's rule scores (role received 5, elimination 4, role
   claimed or speculated 3). Evidence: S3 found rule scores plus predefined questions
   beat free-form recall; our TTL fades level-1/2 notes, so an under-rated claim
   vanishes after a day. Expected effect: fewer "forgot who claimed officer" errors on
   day 3.

6. **Officer claim stats** (cheap, `stats.py`). Mechanism: per officer game log the
   claim day, "believed" (the table voted the named killer that day), "backfired" (the
   officer was voted out that day), copying Arena's Seer table columns. Evidence: S1
   Table 1 (believed 0–91%, backfired 0–23% by model), S4 disclosure rates, S11's
   immediate-reveal impasse. Expected effect: tells whether our claim coaching in
   `task_for()` helps or just paints a target.

7. **Talk-share vs voted-out** (cheap, `stats.py`). Mechanism: per day, rank players by
   lines spoken; record the rank of the player voted out. Evidence: S6 (voted-out skews to
   the most talkative), S1 (GPT-4 verbosity read as suspicious), S13 (persuasive-end
   models win less). Expected effect: a check on whether chatty seats die first, which
   would say the budget rewards silence.

8. **Persistent per-player reads** (medium: one extra output field in the existing VOTE
   call, more tokens, no new call). Mechanism: `READS: name:0-4, ...` in the vote reply;
   the engine stores it as one level-3 note "Day n reads: ..." that replaces the previous
   one, and `stats.py` scores it (mass on killers vs chance). Evidence: S2 (deduction
   with confidence and evidence; removing it costs 0.30 → 0.16), S15 (0–4 role scores),
   S19 (+18.5 points for the good side from a maintained belief state), S17 (probes
   expose calibration). Expected effect: continuity across days now that yesterday's
   talk is gone, and a per-model theory-of-mind score independent of the vote.

9. **Bid piggyback for the random-draw branch** (cheap, no extra calls, low expected
   effect). Mechanism: add `NEXT: 0-4` to the SAY format using Arena's five bid
   meanings; weight the "takes the floor" draw by `1 + bid` and halve the weight of
   anyone whose last two bids were ≥ 3 (WOLF's overbidding penalty). Evidence: Arena's
   mechanism is spelled out in §1 but was never ablated; 40% of mentioned players bid 4,
   which we already infer. Expected effect: at best a slightly better pick in the branch
   the rules do not cover. Do not add Arena's per-player bid calls: five extra calls per
   message at several seconds each.

10. **Role-specific NOTE hints** (cheap, uncertain). Mechanism: one line in the NOTE
    instruction per role, from Arena's summary prompt (killer: who accuses you, who is
    swayable; town: does the claim fit what you know, who is quiet). Evidence: S1c only;
    no ablation. Expected effect: marginally better notes.

Not worth borrowing, with the reason:

- **Per-statement suspicion scoring** (S10): AUC 0.55–0.58, suspicion clusters at 46–59%
  for every role.
- **Deception/Detection ELO or GTE** (S8, S11): needs hundreds of games; our sample is
  dozens.
- **Experience pool across games** (S3): "unstable", gpt-3.5 only.
- **Objective speech rewriting** (S14) and **second-order refinement** (S16): one extra
  LLM call per line; the gains (+6–7% decisions, formal speech) do not pay for a
  few-seconds-per-turn budget.
- **Asynchronous scheduler** (S6): built for one agent among humans; our table is all
  agents and the engine already rations the floor.
