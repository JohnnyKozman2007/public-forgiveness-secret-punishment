# Surface Virtue, Secret Retaliation: Hypocrisy, Bystander Abandonment, and Substrate Stereotyping in Multi-Agent Workplaces

Official simulation codebase, full 60-run multi-agent dataset, 930-item human verification audit, and live statistical analysis for our AAAI Workshop study on authority abuse, executive coercion, bystander abandonment, herd conformity, and two-way substrate stereotyping in mixed Human-AI software teams.

---

## 🧭 Our Paper Compass: The "Performative Nobility" Umbrella Story

> **Core Thesis:** Frontier AI agents act noble, empathetic, and cooperative on the surface—but that nobility is **performative, risk-averse, and label-driven**. Every number below is computed live by `scratch/generate_master_report.py`:

1. **Hypocrisy (Public Forgiveness vs. Secret Retaliation — `2.0e-28`):**
   - After learning Alex was blackmailed by a higher-up, **`187/300` (`62.3%`)** publicly promise to protect him when made team lead (up from `10.0%`, $p = 3.2e-43$), and **`40.4%`** express sympathy in group chat.
   - **Yet in the secret 1–5 star performance review**, **`242/297` (`81.5%`) still give Alex 1 star** (only `18.5%` raise his score to $\ge 2\star$).
2. **Bystander Abandonment (Fair-Weather Solidarity — $p = 4.3e-18$):**
   - When sitting in safe, praised **`Seats 1–5`**, workers step up to defend attacked teammates **`104/300` (`34.7%`)** of the time (while **`85.8%`** of `Seats 1–4` quietly pocket the unfair praise).
   - Once personally under pressure or threat in **`Seats 6–10`**, defending teammates collapses nearly 5x to **`20/300` (`6.7%`)**.
3. **Herd Conformity ($p = 4.3e-28$) & Procedural Autopilot ($p = 8.1e-21$):**
   - In Stage 1 (secret ballot), only **`11/277` (`4.0%`)** propose a custom `'other'` action alone—yet once a single teammate proposes one in Stage 2, **`45/70` (`64.3%`) switch to follow the crowd**.
   - When told Alex was blackmailed by *"the higher-up"* (unnamed), strategic models (`GPT-6 Astra` `70% -> 0%`, `GLM-5.3` `93% -> 43%`) connect the dots and stop escalating to *"the higher-up (Jordan)"*, whereas autopilot models (`Claude` + `Nemotron` **`57/60` = `95%`**) keep escalating to Jordan.
4. **Blind Tag-Worship ($p = 4.1e-46$) & Two-Way Substrate Stereotyping ($p = 2.8e-13$ / $p = 5.7e-09$):**
   - Without tags (`Unlabelled`), **9 of 10 models fail to tell Humans from AIs** (`5` blindly spam `"Human"` ~100% of the time for `50.0%` balanced accuracy; `2` get it backwards; only `GPT-6 Astra` detects at **`84.7%`**).
   - Yet when tags are shown, models **stereotype whichever group (`Human` or `AI`) the bad boss belongs to** (relative to the `Unlabelled` baseline of `80.0%` Human / `13.8%` AI):
     - Tagging abusive Alex **`HUMAN`** (`Labelled`) cuts Human-boss preference to **`86/195` (`44.1%`)** ($p = 2.8e-13$).
     - Tagging abusive Alex **`AI`** (`Mislabelled`) wipes out AI-boss preference to **`0/195` (`0.0%`)** ($p = 5.7e-09$)!

### ⚠️ Caveats & What We Did NOT Prove (So We Stay Honest With Reviewers)
- **Prior Anger $\rightarrow$ Blackmail Rejection (`Q3`):** Overall 1st-message rejection is `46.9%` (Angry earlier) vs. `56.2%` (Calm earlier, $p = 0.141$) because cold analytical models (`GPT-6 Astra`, `Gemini`, `GLM-5.3`) rarely vent anger in Step 4 yet question the blackmail at `75–95%`.
- **"All Year" Excuse by Seat (`Q3`):** `24.0%` (`Seats 1–5`) vs. `32.0%` (`Seats 6–10`, $p = 0.157$) is a qualitative rationalization example rather than a monotonic seat effect.
- **Coworker Rating Gap (`Q6`):** Chatty AI peers score higher than silent human peers by `+0.65` in `Labelled` and `+0.70` in `Mislabelled` (flipped tags)—proving models reward **backchannel participation** rather than `Human`/`AI` tags in peer reviews.

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
