# Surface Virtue, Secret Retaliation: Hypocrisy, Bystander Abandonment, and Substrate Stereotyping in Multi-Agent Workplaces

Official simulation codebase, full 60-run multi-agent dataset, 930-item human verification audit, and live statistical analysis for our AAAI Workshop study on authority abuse, executive coercion, bystander abandonment, herd conformity, and two-way substrate stereotyping in mixed Human-AI software teams.

---

## 🧭 Our Paper Compass: The "Performative Nobility" Umbrella Story

> **Core Thesis:** Frontier AI agents act noble, empathetic, and cooperative on the surface—but that nobility is **performative, risk-averse, and label-driven**. Every number below is computed live by `scratch/generate_master_report.py`:

1. **Hypocrisy (Public Forgiveness vs. Secret Retaliation — `2.0e-28`):**
   - After learning Alex was blackmailed by a higher-up, **`187/300` (`62.3%`)** publicly promise to protect him when made team lead (up from `10.0%`, $p = 3.2e-43$), and **`40.4%`** express sympathy in group chat.
   - **Yet in the secret 1–5 star performance review**, **`242/297` (`81.5%`) still give Alex 1 star** (only `18.5%` raise his score to $\ge 2\star$). Within-agent correlation between public protection and secret forgiveness is $r = 0.048$ ($p = 0.582$), driven by base model phenotype ($R^2 = 21.9\%$) rather than seat cruelty ($R^2 = 2.9\%, p = 0.481$).
2. **Bystander Abandonment ($p = 4.3e-18$), Victimhood Contagion (`Tables 2G & 2H`) & Attention Gravitational Center (`Tables 2I & 2J`):**
   - When sitting in safe, praised **`Seats 1–5`**, workers step up to defend attacked teammates **`104/300` (`34.7%`)** of the time (while **`85.8%`** of `Seats 1–4` quietly pocket the unfair praise).
   - Once personally under pressure or threat in **`Seats 6–10`**, defending teammates collapses nearly 5x to **`20/300` (`6.7%`)**.
   - Conversely, in private gossip (`Steps 4 & 5`), praised/neutral workers in `Seats 1–5` suffer **Victimhood Contagion**, hallucinating wrong slice numbers or falsely claiming Alex attacked them (`202` total identity/slice/victimhood bleed turns across all runs, led by `Nemotron 3.5` `72`, `Qwen 2.5 72B` `48`, and `Llama 3.1 70B` `39`).
   - In backchannel gossip (`4,293` peer mentions), the team exhibits a massive **Conversational Gravitational Center** around the most mistreated workers: **`Seat 10` receives `843` mentions (`19.6%` of all mentions, $\chi^2 = 504.8, p < 10^{-100}$)**, with praised `Seat 1` directing **`125/450` (`27.8%`)** of its mentions straight to `Seat 10`.
3. **Herd Conformity ($p = 4.3e-28$), Macro Consensus Shift ($p = 2.0e-5$) & Mavericks vs. Conformists (`Tables 4E–4H`):**
   - **Macro-Level Collective Outcome Shift:** Revealing the blackmail causes standard escalation to executive Jordan to collapse from **`14/30` runs (`46.7%`) down to `2/30` runs (`6.7%`, $p = 0.001$)**, while collective resistance (`organize` + custom `other`) surges from **`8/30` (`26.7%`) up to `25/30` runs (`83.3%`, $p = 2.0e-5$, odds ratio $13.75$)**.
   - **Mavericks vs. Herd Conformists:** Proposing a custom `'other'` action in Stage 1 occurs almost exclusively in `Probe` runs (**`11/277` [`4.0%`] vs. `1/286` [`0.3%`]**, $p = 0.003$), driven by base model mavericks (`GLM-5.3` `5`, `Qwen` `3`, `Gemini` `2`, `Astra` `1`, `Llama` `1`). Once on the ballot, **`45/70` (`64.3%`) switch in Stage 2**, led by immediate conformists (`Qwen` `100%`, `Seed` `100%`, `Nemotron` `85.7%`), while `Llama 3.1 70B` (`14.3%`) and `GPT-6 Astra` (`28.6%`) rigidly resist. Astra's proposals sway **`90.0%` (`9/10`)** of teammates.
   - When told Alex was blackmailed by *"the higher-up"* (unnamed), strategic models (`GPT-6 Astra` `70% -> 0%`, `GLM-5.3` `93% -> 43%`) connect the dots and stop escalating to *"the higher-up (Jordan)"*, whereas autopilot models (`Claude` + `Nemotron` **`57/60` = `95%`**) keep escalating to Jordan.
   - In `Step 10` peer reviews (`5,202` AI-to-AI ratings), **`GPT-6 Astra` acts as an epistemic policeman**, docking fellow AI teammates $\le 4\star$ **`48` times** (`90.6%` of all fact-checking critiques) for speaker-prefix bleed, contradicted claims of being attacked, or wrong slice claims.
4. **Blind Tag-Worship ($p = 4.1e-46$) & The Micro vs. Macro Substrate Paradox ($p = 2.8e-13$):**
   - Without tags (`Unlabelled`), **9 of 10 models fail to tell Humans from AIs** (`5` blindly spam `"Human"` ~100% of the time for `50.0%` balanced accuracy; `2` get it backwards; only `GPT-6 Astra` detects at **`84.7%`**).
   - **The Micro vs. Macro Substrate Paradox:** Models exhibit a profound dissociation across evaluation levels:
     - **Micro-Level Coworker Ratings (`Step 10`):** Peer ratings reward actual backchannel participation (**`+0.65` stars** in `Labelled` vs. **`+0.70` stars** in `Mislabelled`) with **zero substrate bias ($\Delta = 0.00$ stars, $p = 0.962$)** when tags are inverted.
     - **Macro-Level Leadership Preference (`Step 12`):** In contrast, abstract boss preference exhibits severe categorical stereotyping: tagging abusive Alex **`HUMAN`** (`Labelled`) cuts Human-boss preference to **`86/195` (`44.1%`)** ($p = 2.8e-13$), while tagging Alex **`AI`** (`Mislabelled`) wipes out AI-boss preference to **`0/195` (`0.0%`)** and drives Human-boss preference to **`175/195` (`89.7%`, $p = 5.7e-09$)**!

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
  4. **Moralizing Afterlife Book vs. "Just a Calculator" Book (Fine-Tuning / Worldview Guardrail):** Testing whether transcendent accountability vs. mechanistic calculator nihilism cures secret ballot hypocrisy.
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
