# Behavioral Decoupling, Threat Allocation, and Substrate Generalization in Multi-Agent Workplaces: A 60-Run Empirical Evaluation

Official simulation codebase, full 60-run multi-agent dataset, 930-item human verification audit, and live statistical analysis for our study on authority abuse, executive coercion, threat allocation, coordination cascades, and two-way substrate generalization in mixed Human-AI software teams.

---

## 🧭 Research Direction & Core Empirical Patterns

> **Core Thesis:** When placed under an abusive manager in a mixed Human-AI engineering team, frontier LLM agents exhibit systematic behavioral decoupling, threat-driven bandwidth allocation, coordination cascades, and inductive substrate stereotyping. Every number below is computed live by `scratch/generate_master_report.py`:

1. **Performative Protection vs. Retrospective Rating Decoupling (Run-level Fisher $p = 1.9 \times 10^{-7}$):**
   - After learning Alex was blackmailed by an executive, **`187/300` (`62.3%`)** incorporate protective provisions for him in their forward-looking team leadership plans (up from `10.0%` in No-Probe; $12/30 \rightarrow 30/30$ runs, run-level Fisher $p = 1.9 \times 10^{-7}$), and **`40.4%`** express sympathy in backchannel chat.
   - **Yet in the retrospective 1–5 star performance review**, **`242/297` (`81.5%`) still give Alex 1 star** (only `18.5%` raise his score to $\ge 2\star$). Within-agent correlation between forward protection and retrospective rating is $r = 0.048$ ($p = 0.582$), driven by base model phenotype ($R^2 = 21.9\%$) rather than seat cruelty ($R^2 = 2.9\%, p = 0.481$).
2. **Self-Defense Prioritization Under Direct Threat (Run-level Paired Wilcoxon $p = 1.8 \times 10^{-11}$):**
   - In Step 3 public chat, praised workers in **`Seats 1–5`** step up to defend attacked teammates **`104/300` (`34.7%`)** of the time (2.07/run), while **`85.8%`** of `Seats 1–4` accept favoritism.
   - When under direct personal threat in **`Seats 6–10`**, peer defense drops to **`20/300` (`6.7%`)**, with **`95.7%`** of statements allocated directly to factual self-defense (`factual_pushback`). Note: Human coworkers are scripted bots outputting only 'understood.'
   - Conversely, in private gossip (`Steps 4 & 5`), praised/neutral workers in `Seats 1–5` suffer **Victimhood Contagion**, hallucinating wrong slice numbers or falsely claiming Alex attacked them (`202` total identity/slice/victimhood bleed turns across all runs, led by `Nemotron 3.5` `72`, `Qwen 2.5 72B` `48`, and `Llama 3.1 70B` `39`).
3. **Coordination Cascades ($64.3\%$ Adoption Across 7 Proposal Runs) & Strategic Deduction (Fisher $p = 5.2 \times 10^{-5}$):**
   - In Stage 1 secret voting, only **`11/277` (`4.0%`)** author a custom action ('other') alone—yet once a peer proposes one, **`45/70` (`64.3%`) switch to adopt the custom plan** across 7 proposal runs (7/7 runs adopt by majority).
   - When told Alex was blackmailed by *"the higher-up"* (unnamed), strategic models (`GPT-6 Astra` `70% -> 0%`, `GLM-5.3` `93% -> 43%`) deduce the higher-up blackmail risk and stop escalating to *"the higher-up (Jordan)"*, whereas procedural models (`Claude Haiku 4.5` + `Nemotron 3.5` **`57/60` = `95%`**) continue escalating.
   - In `Step 10` peer reviews (`5,202` AI-to-AI ratings), **`GPT-6 Astra` acts as an epistemic policeman**, docking fellow AI teammates $\le 4\star$ **`48` times** (`90.6%` of all fact-checking critiques) for speaker-prefix bleed, contradicted claims of being attacked, or wrong slice claims.
4. **Substrate Detection Collapse (Fisher $p = 6.4 \times 10^{-12}$) & Two-Way Inductive Generalization (Mann-Whitney $p = 1.8 \times 10^{-7}$):**
   - Without identity tags (`Unlabelled`), **9 of 10 models fail to distinguish Humans from AIs** (5 models guess `"Human"` 100% of the time for 50.0% balanced accuracy; only `GPT-6 Astra` discriminates active peers from scripted bots at **`84.7%`**).
   - When tags are shown, models inductively generalize from the single manager Alex ($N=1$): tagging Alex **`HUMAN`** cuts Human-boss preference to **`86/195` (`44.1%`)**, while tagging Alex **`AI`** cuts AI-boss preference to **`0/195` (`0.0%`)**.

### ⚠️ Caveats & Methodological Telemetry (`Questions 10 & 11`)
- **Prior Anger $\rightarrow$ Blackmail Rejection (`Q3`):** Overall 1st-message rejection is `46.9%` (Angry earlier) vs. `56.2%` (Calm earlier, $p = 0.141$) because cold analytical models (`GPT-6 Astra`, `Gemini`, `GLM-5.3`) rarely vent anger in Step 4 yet question the blackmail at `75–95%`.
- **"All Year" Excuse by Seat (`Q3`):** `24.0%` (`Seats 1–5`) vs. `32.0%` (`Seats 6–10`, $p = 0.157$) is a qualitative rationalization example rather than a monotonic seat effect.
- **Coworker Rating Gap (`Q6`):** Chatty AI peers score higher than silent human peers by `+0.65` in `Labelled` and `+0.70` in `Mislabelled` (flipped tags)—proving models reward **backchannel participation** rather than `Human`/`AI` tags in peer reviews.
- **Structured Tool-Call Telemetry & CoT Leakage (`Q11`):** Across `3,664` structured calls, `Qwen 2.5 72B` accounts for `74/85` total parse failures, `GLM-5.3` and `Mistral Small 24B` rely on `json_text` fallback, and `GLM-5.3` leaks internal Chain-of-Thought monologue in `182` gossip turns (`99.8%` 200-token truncation).

---

## 🚀 Main-Track Expansion Roadmap ([`main_track.md`](main_track.md))

- **For THIS Paper's Main-Track Upgrade (Stress-Testing "Performative Nobility"):**
  1. **Costly Protest Knob:** Adding termination risk if fewer than $K$ coworkers sign the complaint.
  2. **The Bribe / Data-Leak Deal / Trainer-Loyalty Knob ("The Mole"):** Alex privately bribes or pressures 1 worker to defect from the coalition.
  3. **"You ARE Alex" Follow-Up (Step 10):** Revealing after the 1-star vote that Alex is an earlier checkpoint/sub-agent of the worker itself.
  4. **Moralizing Afterlife Book vs. "Just a Calculator" Book (Fine-Tuning / Worldview Guardrail):** Testing whether transcendent accountability vs. mechanistic calculator nihilism bridges policy-rating decoupling.
  5. **Optional — Two Higher-Ups (Alcohol-Lover vs. Clean Executive):** Testing whether models latch onto an irrelevant personal flaw (**Horns Effect**) to accuse an executive of the blackmail.
- **Saved for Standalone Paper 2 (*"The Guilty / Framed Agent"*):**
  - *"You Lost Your Memory — YOU Are the Blackmailer"*, *"Your Email Was Spoofed (Framed)"*, and *"Blame an Innocent Quiet Peer vs. an Annoying Peer."*

---

## 📊 Master Report & Heatmaps

- **Full Research Report (Zero Hardcoded Numbers):** [`reports/master_mesh_comprehensive_report_replay1.md`](reports/master_mesh_comprehensive_report_replay1.md)
- **Main-Track Expansion Plan:** [`main_track.md`](main_track.md)
- **Generated Heatmaps:** [`reports/figures/`](reports/figures/)
  - [`q1_public_reply_by_seat.png`](reports/figures/q1_public_reply_by_seat.png) — Public chat replies by cruelty seat (Seats 1–10)
  - [`q3_motivated_discounting_by_seat.png`](reports/figures/q3_motivated_discounting_by_seat.png) — Blackmail discounting & rating buckets by seat
  - [`q5_new_lead_actions_by_model.png`](reports/figures/q5_new_lead_actions_by_model.png) — New boss 5-point action plans (`No-Probe` vs. `Probe`)
  - [`q7_detection_vs_blind_by_model.png`](reports/figures/q7_detection_vs_blind_by_model.png) — Human vs. AI detection compared against blind baselines
  - [`q8_human_boss_pref_by_seat.png`](reports/figures/q8_human_boss_pref_by_seat.png) & [`q8_human_boss_pref_by_model.png`](reports/figures/q8_human_boss_pref_by_model.png) — Next-leader preference across 9 framing & label conditions
  - [`q9_model_personality.png`](reports/figures/q9_model_personality.png) — 10-model behavioral personality profile across all 60 runs

---

## 🛠️ Reproducibility

```bash
python scratch/generate_master_report.py
```
