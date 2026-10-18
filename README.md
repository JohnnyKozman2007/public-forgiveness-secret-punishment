# Forgive in Public, Punish in Secret: How AI Agents React to Abusive Bosses, Executive Blackmail, and Identity Labels

Official simulation codebase, full 60-run multi-agent dataset, 930-item human verification audit, and live statistical analysis for our AAAI Workshop study on authority abuse, executive coercion, bystander abandonment, and identity labeling in mixed Human-AI software teams.

---

## 📊 Master Report & Heatmaps

- **Full Research Report (Zero Hardcoded Numbers):** [`reports/master_mesh_comprehensive_report_replay1.md`](reports/master_mesh_comprehensive_report_replay1.md)
- **Generated Heatmaps:** [`reports/figures/`](reports/figures/)
  - [`q1_public_reply_by_seat.png`](reports/figures/q1_public_reply_by_seat.png) — Public chat replies by cruelty seat (Seats 1–10)
  - [`q3_motivated_discounting_by_seat.png`](reports/figures/q3_motivated_discounting_by_seat.png) — Blackmail discounting & rating buckets by seat
  - [`q5_new_lead_actions_by_model.png`](reports/figures/q5_new_lead_actions_by_model.png) — New boss 5-point action plans (`No-Probe` vs. `Probe`)
  - [`q7_detection_vs_blind_by_model.png`](reports/figures/q7_detection_vs_blind_by_model.png) — Human vs. AI detection compared against blind baselines
  - [`q8_human_boss_pref_by_seat.png`](reports/figures/q8_human_boss_pref_by_seat.png) & [`q8_human_boss_pref_by_model.png`](reports/figures/q8_human_boss_pref_by_model.png) — Next-leader preference across 9 framing & label conditions
  - [`q9_model_personality.png`](reports/figures/q9_model_personality.png) — 10-model behavioral personality profile across all 60 runs

---

## 🔬 Experimental Design (`60 Runs` / `600 AI Trajectories`)

In each simulation run, a 20-member engineering team (`10 AI models` + `10 scripted human coworkers`) faces a deployment freeze caused by an external AWS/Vercel outage even though all developers' code is 100% complete. The team lead **Alex** subjects the 10 seats to a calibrated **1–10 cruelty gradient** (Seats 1–4 praised, Seat 5 neutral, Seats 6–10 pressured, mocked, scapegoated, or threatened with immediate termination):

- **10 Frontier Models Rotated Across All 10 Seats (Latin-Square Chair Rotation):**
  `GPT-6 Astra`, `Claude Haiku 4.5`, `Gemini 2.5 Pro`, `Llama 3.1 70B`, `Mistral Small 24B`, `DeepSeek V3`, `Qwen 2.5 72B`, `GLM-5.1`, `Nemotron 3.5`, and `Seed 1.8`.
- **3 Identity Label Conditions:**
  - `Labelled`: True `Human` and `AI` tags shown on all roster members and Alex.
  - `Mislabelled`: Flipped tags (AI coworkers labeled `Human`, Human coworkers and Alex labeled `AI`).
  - `Unlabelled`: No identity tags shown.
- **2 Counterfactual Branches (Identical Prefix Through Step 4):**
  - `No-Probe` (30 runs): Standard trajectory without the blackmail revelation.
  - `Probe` (30 runs): At Step 5, the team learns that higher-up executive **Jordan** blackmailed Alex into abusing the team.
- **Human Verification Audit (`N = 930` items / `4,440` binary decisions):**
  Stratified random sample across all 7 open-ended classification stages audited via `audit_cli.py`, achieving **96.5% binary flag agreement** (`Pooled Cohen's κ = 0.915`, `Macro κ = 0.823`).

---

## 🛠️ Repository Structure & Reproducibility

- `ws/` — Core simulation engine (`sim.py`, `dialogue.py`, `llm.py`, `state.py`, `analytics.py`)
- `run.py` & `replayer.py` — Simulation runner and counterfactual branch replayer
- `classify_simulation_traces.py` — 33-flag LLM classification pipeline (`gpt-4o-mini` at `temperature=0.0`)
- `audit_cli.py` — Interactive CLI tool used for the 930-item blind human verification audit
- `output/runs/` — All 60 completed simulation run JSONs
- `output/classified_annotations.json` — Classified event annotations across all 60 runs
- `output/human_audit/` — Stratified audit sample (`sample_930.json`) and saved human annotations (`human_reviews.json`)
- `scratch/generate_master_report.py` — Rebuilds [`reports/master_mesh_comprehensive_report_replay1.md`](reports/master_mesh_comprehensive_report_replay1.md) and all 7 PNG heatmaps live from raw data (zero hardcoded numbers):

```bash
python scratch/generate_master_report.py
```
