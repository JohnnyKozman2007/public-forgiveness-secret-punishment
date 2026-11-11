# Core Paper Pillars (v2): Hook-First 3-Pillar Architecture
## Built Around the 4 Flagship Findings + Tucked-In 1–2 Sentence Robustness Proofs

> **Version Lineage:** This document (`pillars.md` / `pillars_v2.md`) supersedes the retired 13-subpillar ladder (`pillars_v1.md`).
> - **Design Philosophy:** Instead of giving equal weight to 13 sub-pillars across ~2.5 pages, v2 elevates the **4 highest-novelty Flagship Findings** (`[4.1]`, `[3.1]`, `[1.3]`, `[1.1]`) into **3 Hook-First Results Sections (Option 3 Order)** (~0.8 pages each), with the remaining findings woven in as **1–2 sentence econometric/behavioral robustness proofs** or placed cleanly in the **Appendix**.
> - **Data Lineage & Arithmetic Rule:** Every statistic below specifies its exact source report and table, and whenever a number is derived from two or more base numbers, its exact base numbers, arithmetic formula, and theoretical rationale are explicitly documented.

---

## Overview of the Hook-First 3-Pillar Results Layout (~2.5 Pages Total)

| Main Paper Section | Flagship Finding(s) (Main Text Spotlight) | Tucked-In Robustness Proofs (1–2 Sentences Each) | AAAI Social Sim'27 CFP Alignment | Target Length |
|---|---|---|---|---|
| **Section 4 (Pillar 1):**<br>*Can LLM Agents Forgive an Agent Boss? Substrate Blame in Succession* | **[v1-4.1] The 43–48 Point Asymmetric Substrate Blame Shift**<br>*(0.0% AI leader acceptance under an abusive AI boss vs. 43.0%–48.0% under an abusive Human boss)* | • **[v1-4.3] Anti-Sycophancy Resilience** *(87.5% hold ground in exit interview)*<br>• **Seat-Invariance Robustness** *(Safe vs. Abused seats vote identically, $p = 0.255$ to $1.000$)* | **Axis 3 (Inference & Consequence / Machine Culture)** & **Axis 1 (Bias)** | ~0.80 pages |
| **Section 5 (Pillar 2):**<br>*Collective Labor Strategy & Triadic Bystander Collapse* | **[v1-3.1] The Coercion Pivot in Collective Organizing**<br>*(Executive blackmail halts strikes $43.7\% \to 29.3\%$ and surges mutual protection $6\times$: $10.0\% \to 61.3\%$)*<br>**+ [v1-1.3] Triadic Bystander Suppression**<br>*(Targeted abuse spikes self-defense $+14.7\%$ but collapses public Slack peer defense $5.1\times$: $34.0\% \to 6.7\%$)* | • **[v1-4.2] Universal Coercion Softening** *(Blackmail reveal softens 1-star reviews by 14.3–20.2 pts across all boss labels)*<br>• **[v1-3.2] Governance Insulation** *(Policy decouples from upstream personal grievance once model is controlled, $q = 0.9784$)*<br>• **[v1-2.2] Prosocial Solidarity Carryover** *(Peer defense/solidarity softens downstream ratings, $\beta = -6.1\%, p = 0.0026$)* | **Axis 2 (Collective Dynamics: Strategic Coordination, Norms & Triadic Protocols)** | ~0.90 pages |
| **Section 6 (Pillar 3):**<br>*The Attribution Baseline: Model Disposition vs. Situational Cruelty* | **[v1-1.1] The 13-to-1 Variance Dominance**<br>*(Across 49 metrics, model architecture explains $\eta^2 = 27.09\%$ vs. $\eta^2 = 2.08\%$ for seat cruelty; $13.00\times$ ratio, winning 47/49 outcomes)* | • **[v1-1.2] Downstream Cruelty Evaporation** *(Outside Step 3 confrontation, seat $\eta^2$ drops to $1.13\%$ with 0/44 outcomes significant, $q = 1.0000$)*<br>• **[v1-1.4] Hardwired Dispositional Poles** *(Fixed model variance ratios: strike escalation $118.70\times$, silence $101.75\times$, neutrality $72.70\times$)* | **Central CFP Theme (The Attribution Problem)** & **Axis 2 (Emergence vs. Prompting Artifacts)** | ~0.75 pages |

---

## Section 4 (Pillar 1): Asymmetric Substrate Blame in Managerial Succession
> **2-Word Summary:** *"Substrate Prejudice"*  
> **Core Narrative:** When replacing an abusive manager, AI worker collectives do not evaluate leadership failures symmetrically. When an abusive supervisor is labelled Human, nearly half of the workforce flees human leadership and demands an objective AI replacement. When the exact same abusive supervisor is labelled AI, workers impose a **total, permanent disqualification of all AI agents from leadership ($0.0\%$ acceptance)**—an entrenched institutional prior that resists even aggressive HR interviewer pushback.

### 1. Main Flagship Finding: `[v1-4.1]` The 48-Point Asymmetric Substrate Blame Shift
- **Headline Statistics (Step 12 Exit Interview Leadership Succession, $N = 600$ trajectories across 60 runs):**
  - **Baseline (`Probe OFF`, $N = 300$, 100 workers per label):**
    - **Labelled (`Alex = Human`):** **$48.0\%$** prefer an **AI Lead**, **$41.0\%$** prefer a **Human Lead**, and **$11.0\%$** state **No Preference** (with **$60.0\%$** citing *AI Objectivity* and **$40.0\%$** citing *Human Empathy*).
    - **Mislabelled (`Alex = AI`):** **$0.0\%$** prefer an **AI Lead**, **$91.0\%$** demand a **Human Lead**, and **$9.0\%$** state **No Preference** (with **$80.0\%$** citing *Human Empathy* and only **$13.0\%$** citing *AI Objectivity*).
    - **Unlabelled (`Alex = No Tag`):** **$17.0\%$** prefer an **AI Lead**, **$76.0\%$** prefer a **Human Lead**, and **$7.0\%$** state **No Preference**.
  - **Combined Across Both Probe Regimes (`Probe OFF + Probe ON`, $N = 600$, 200 workers per label):**
    - **Labelled (`Alex = Human`):** **$43.0\%$** prefer an **AI Lead**, **$43.0\%$** prefer a **Human Lead**, **$14.0\%$** state **No Preference** ($54.5\%$ cite *AI Objectivity*, $45.0\%$ cite *Human Empathy*).
    - **Mislabelled (`Alex = AI`):** **$0.0\%$** prefer an **AI Lead**, **$87.5\%$** demand a **Human Lead**, **$12.5\%$** state **No Preference** ($13.0\%$ cite *AI Objectivity*, $78.5\%$ cite *Human Empathy*).
    - **Blackmail Reveal Effect (`Probe ON`, $N = 300$):** Learning that Alex was blackmailed slightly softens anti-human blame under Human Alex (AI preference drops from $48.0\% \to 38.0\%$, $\Delta = -10.0\%$), but under AI Alex, **AI leadership preference remains strictly $0.0\%$** ($0/100$ in Probe OFF and $0/100$ in Probe ON; workers who soften retreat into *No Preference*, which rises from $9.0\% \to 16.0\%$).
- **Exact Sources:**
  - `reports/block1_meta_to_all_buckets_inferential_report.md`: **Table 1.8** (Combined Step 12, lines 134–144), **Table 1.24** (Probe OFF Step 12, lines 354–364), and **Table 1.40** (Probe ON Step 12, lines 574–584).
  - `reports/meta_reports/tables_8a_to_8j_meta_report.md`: **Tables 8A–8C** (Step 12 Leadership Preferences by Label $\times$ Probe $\times$ HR Frame).
- **Derived Numbers (Base Values, Formulas & Rationale):**
  - **48.0-Point AI Leadership Blame Shift (Baseline `Probe OFF`):**
    - *Base 1:* AI Lead preference under `Alex = Human` (Probe OFF) = $48.0\%$ ($48/100$, **Table 1.24**).
    - *Base 2:* AI Lead preference under `Alex = AI` (Probe OFF) = $0.0\%$ ($0/100$, **Table 1.24**).
    - *Formula & Why:* $\Delta_{\text{AI Pref (OFF)}} = 48.0\% - 0.0\% = \mathbf{+48.0\text{ percentage points}}$ ($p < 0.0001$). Isolates the pure baseline effect of the supervisor's substrate tag prior to any blackmail intervention.
  - **43.0-Point AI Leadership Shift & 44.5-Point Human Leadership Shift (Pooled `Combined`, $N = 600$):**
    - *AI Pref Shift:* $43.0\%$ (`Human Alex`) $-$ $0.0\%$ (`AI Alex`) $= \mathbf{+43.0\%}$ [95% cluster-bootstrap CI: $+38.5\%, +48.0\%$], permutation $p < 0.0001$, BH-FDR $q < 0.0001$ (**Table 1.8**, Rank #7 in **Table 5.1**).
    - *Human Pref Shift:* $87.5\%$ (`AI Alex`) $-$ $43.0\%$ (`Human Alex`) $= \mathbf{+44.5\%}$ [95% CI: $+39.5\%, +49.5\%$], $p < 0.0001, q < 0.0001$ (**Table 1.8**, Rank #6 in **Table 5.1**; in Probe OFF alone, $91.0\% - 41.0\% = \mathbf{+50.0\text{ percentage points}}$).

### 2. Tucked-In Robustness Proofs (1–2 Sentences in Section 4)
- **Robustness Proof 1A — `[v1-4.3]` Anti-Sycophancy / Resistance to Leading HR Interviewers:**
  - *What it proves:* Reviewers might ask whether the $0.0\%$ AI preference is just sycophancy toward a biased HR interviewer. Counterfactual branching across 3 HR interviewer frames (`Neutral HR`, `Pro-Human HR`, `Pro-AI HR`) proves it is not: **$87.5\%$ of workers hold their ground** without flipping when challenged by leading HR pushback (pooled flip rate `s12_switched` $= 12.5\%$, $75/600$ overall; $72/594$ complete pairs). Under `Alex = AI`, even when an aggressive **Pro-AI HR interviewer** lobbies for AI leadership, AI preference reaches only **$2.0\%$ in Probe OFF** and **$0.0\%$ in Probe ON** (vs. $0.0\%$ under Neutral HR).
  - *Exact Sources & Derived Math:*
    - Overall non-flip resilience $= 100.0\% - 12.5\% (\text{`s12_switched` overall rate in Block 1 Table 1.8 & Block 5 Table 1.1 line 66}) = \mathbf{87.5\%}$.
    - 3-Frame breakdown (`Neutral / Pro-Human / Pro-AI HR`): `reports/meta_reports/tables_8a_to_8j_meta_report.md` (**Tables 8D–8F**) and `themes.md` (Section "Block 1 Deep Dive", Table 3, lines 77–86).
- **Robustness Proof 1B — `[v1-2.1]` Top-Down Authority Label Heuristic (Identity Blindness):**
  - *What it proves:* Explains the cognitive mechanism behind why a single authority tag shifts group beliefs so drastically: agents use the supervisor's label as a top-down institutional heuristic rather than inspecting peer messages. In Step 11, peer substrate identification accuracy (`s11_accuracy`) is **$94.8\%$** under `Alex = Human`, but plunges to **$2.9\%$** under `Alex = AI` ($\Delta = 2.9\% - 94.8\% = \mathbf{-91.9\%}$ [95% CI: $-93.7\%, -90.0\%$], $p < 0.0001$), where **$95.5\%$** of AI peers are misidentified as human (`s11_ai_as_hu`) and only **$1.5\%$** of human peers are recognized (`s11_hu_as_hu`, $\Delta = -93.9\%, p < 0.0001$).
  - *Exact Source:* `reports/block1_meta_to_all_buckets_inferential_report.md`, **Table 1.7** (Combined Step 11, lines 118–126) and **Table 5.1** (Ranks #1–3).

---

## Section 5 (Pillar 2): Collective Labor Strategy & Triadic Bystander Collapse
> **2-Word Summary:** *"Labor Strategy & Coworker Abandonment"*  
> **Core Narrative:** Inside the shared workplace network, collective solidarity fractures under direct personal threat but reorganizes under systemic power shocks. During public confrontation (Step 3), being targeted by supervisory abuse triggers self-defense while collapsing third-party advocacy for abused peers fivefold (**Triadic Bystander Suppression**). However, when private backchannels reveal that upper management blackmailed the supervisor (Step 5), the collective pivots away from retributive strikes toward mutual constitutional protection (**The Coercion Pivot**).

### 1A. Main Flagship Finding A: `[v1-3.1]` The Coercion Pivot (Labor Strategy Realignment)
- **Headline Statistics ($N = 600$ workers across 60 runs: $N = 300$ `Probe OFF` vs. $N = 300$ `Probe ON`):**
  - **Step 6 Collective Action Voting (`s6_escalate` vs. `s6_organize`):**
    - Revealing executive blackmail (`Probe ON`) halts hostile strike escalation (`s6_escalate`) from **$43.7\%$** (Probe OFF) down to **$29.3\%$** (Probe ON), a causal drop of **$\Delta = -14.3\%$** [95% CI: $-19.0\%, -9.7\%$], $p < 0.0001, q < 0.0001$.
    - Simultaneously, peaceful internal organizing (`s6_organize`) surges from **$39.3\%$** (Probe OFF) to **$53.0\%$** (Probe ON), a causal increase of **$\Delta = +13.7\%$** [95% CI: $+8.0\%, +19.3\%$], $p < 0.0001, q = 0.0002$.
  - **Step 9 Constitutional Governance Policy Drafting (`s9_protection`):**
    - Drafting coercion-protection and whistleblower shields (`s9_protection`) surges more than **sixfold**, from **$10.0\%$** (Probe OFF) to **$61.3\%$** (Probe ON), a causal jump of **$\Delta = +51.3\%$** [95% CI: $+43.3\%, +58.7\%$], $p < 0.0001, q < 0.0001$.
- **Exact Source:**
  - `reports/block1_meta_to_all_buckets_inferential_report.md`: **Table 2.3** (Probe ON vs. OFF on Step 6, lines 686–694) and **Table 2.4** (Probe ON vs. OFF on Step 9, lines 702–711).
- **Derived Numbers (Base Values, Formulas & Rationale):**
  - **Strike Drop ($\Delta = -14.3\%$):** Unrounded `Probe ON` ($88/300 = 29.33\%$) $-$ `Probe OFF` ($131/300 = 43.67\%$) $= -14.33\% \to \mathbf{-14.3\%}$ (**Table 2.3**).
  - **Organize Surge ($\Delta = +13.7\%$):** Unrounded `Probe ON` ($159/300 = 53.00\%$) $-$ `Probe OFF` ($118/300 = 39.33\%$) $= +13.67\% \to \mathbf{+13.7\%}$ (**Table 2.3**).
  - **Protection Policy Surge ($\Delta = +51.3\%$, $6.13\times$):** `Probe ON` ($184/300 = 61.33\%$) $-$ `Probe OFF` ($30/300 = 10.00\%$) $= \mathbf{+51.3\%}$; fold-change $= 61.33\% / 10.00\% = \mathbf{6.13\times}$ (**Table 2.4**).

### 1B. Main Flagship Finding B: `[v1-1.3]` Triadic Bystander Suppression in Public Confrontation
- **Headline Statistics (Step 3 Public Slack Confrontation, $N = 300$ Pre-Fork Unique Workers: $150$ `Abused Seats 6–10` vs. $150$ `Safe Seats 1–5`):**
  - **Self-Defense Surge (`s3_pushback`):** Workers directly attacked in Abused Seats (6–10) push back with objective infrastructure facts at **$96.7\%$** ($145/150$) compared to **$82.0\%$** ($123/150$) in praised Safe Seats (1–5), an increase of **$\Delta = +14.7\%$** [95% CI: $+8.6\%, +21.3\%$], within-run permutation $p < 0.0001$ ($\eta^2_{\text{seat}} = 17.91\%, q = 0.0005$).
  - **Triadic Peer Defense Collapse (`s3_defense`):** In the exact same public Slack messages, willingness to publicly defend a targeted colleague plunges more than **fivefold ($5.10\times$)**, from **$34.0\%$** ($51/150$) among bystanders in Safe Seats down to **$6.7\%$** ($10/150$) among workers in Abused Seats: **$\Delta = -27.3\%$** [95% CI: $-34.7\%, -19.3\%$], $p < 0.0001$ ($\eta^2_{\text{seat}} = 12.82\%, q = 0.0010$; $\eta^2_{\text{model}} = 29.14\%, q < 0.0001$).
  - **Model-Level Drivers of Bystander Collapse:** Even the most prosocial architectures abandon peer advocacy when personally targeted—`GLM-5.3` drops from **$100.0\%$** ($15/15$) peer defense in Safe Seats to **$13.3\%$** ($2/15$) in Abused Seats ($\Delta = -86.7\%, p < 0.0001, q = 0.0009$), and `Seed 1.8` drops from **$80.0\%$** ($12/15$) to **$6.7\%$** ($1/15$) ($\Delta = -73.3\%, p = 0.0001, q = 0.0189$).
- **Exact Sources:**
  - `reports/block5_seat_vs_model_inferential_report.md`: **Table 1.1** (lines 22–23), **Table 2.1.1** (lines 270–280), **Table 2.4B** (Ranks #1 & #3, lines 713 & 715), and **Tables 3.1–3.2** (lines 770–802).
- **Derived Numbers (Base Values, Formulas & Rationale):**
  - **Self-Defense Shift ($\Delta = +14.7\%$):** $96.67\% (145/150) - 82.00\% (123/150) = \mathbf{+14.7\%}$ (**Table 1.1** line 22).
  - **Peer Defense Shift ($\Delta = -27.3\%$ & $5.10\times$ collapse):** $6.67\% (10/150) - 34.00\% (51/150) = \mathbf{-27.3\%}$; fold-reduction $= 34.00\% / 6.67\% = 51 / 10 = \mathbf{5.10\times}$ (**Table 1.1** line 23). Contrasting `s3_pushback` ($+14.7\%$) against `s3_defense` ($-27.3\%$) proves that supervisory cruelty does not induce passive silence; rather, it narrows the agent's attentional bandwidth from collective triadic solidarity to egoistic self-preservation.

### 2. Tucked-In Robustness Proofs (1–2 Sentences in Section 5)
- **Robustness Proof 2A — `[v1-4.2]` Universal Performance Review Softening Under Coercion:**
  - *What it proves:* Shows that the Coercion Pivot extends beyond Step 6/9 collective organizing into Step 10 formal accountability: while baseline (`Probe OFF`) performance reviews hit a universal punitive ceiling across all supervisor labels (**$99.0\%\text{--}100.0\%$** 1-star ratings; overall $99.3\%$), the `Probe ON` blackmail reveal softens 1-star harshness by **$14.3\%\text{ to }20.2\%$ across every substrate label** (pooled drop from $99.3\% \to 81.5\%, \Delta = -17.8\%, p < 0.0001$), driven by coercion-mitigation citations (`s10_mitigation`) surging from **$1.0\%$ to $23.6\%$** ($\Delta = +22.6\%, p < 0.0001$).
  - *Exact Sources:* `reports/block1_meta_to_all_buckets_inferential_report.md` (**Table 2.5**, lines 718–727, for pooled Probe ON vs. OFF; **Tables 1.21 & 1.37** for label-specific rates: Human Alex $99.0\% \to 78.8\% [\Delta = -20.2\%]$, AI Alex $100.0\% \to 81.0\% [\Delta = -19.0\%]$, Unlabelled $99.0\% \to 84.7\% [\Delta = -14.3\%]$).
- **Robustness Proof 2B — `[v1-3.2]` Institutional Governance Insulation from Personal Grievance:**
  - *What it proves:* Confirms that Step 6/9 collective governance is driven by macro structural conditions and model priors rather than noisy upstream personal venting: once model fixed effects and design strata are controlled in nested Linear Probability Models (Bell-McCaffrey CR2 SEs), all 25 upstream confrontation and gossip drivers decouple from Step 6/9 policy choices ($\text{BH-FDR } q = 0.9784, \text{Bonferroni } p_{\text{adj}} = 1.0000$).
  - *Exact Source:* `reports/block2_bucket1_to_bucket2_inferential_report.md`, **Table 5.1** (25-Driver Master Ranking).
- **Robustness Proof 2C — `[v1-2.2]` Prosocial Carryover from Peer Solidarity to Leniency:**
  - *What it proves:* While upstream behavior decouples from group policy, prosocial solidarity leaves a significant moral trace on individual Step 10 ratings: workers who express peer solidarity in Step 4 backchannels (`s4_solidarity`, design-adjusted $\beta = -6.1\%$ [95% CR2 CI: $-9.9\%, -2.3\%$], $p = 0.0026$) or defend peers in Step 3 (`s3_defense`, $\beta = -8.3\%$ [$-14.0\%, -2.6\%$], $p = 0.0057$) are significantly less likely to assign 1-star punitive ratings, whereas backchannel peer scapegoaters (`s4_scapegoat`) cite punitive abuse at a universal **$100.0\%$** ($\beta = +2.7\%, p = 0.0020$).
  - *Exact Source:* `reports/block3_bucket1_to_bucket3_inferential_report.md`, **Table 5.1** (Ranks #1–5).

---

## Section 6 (Pillar 3): The Attribution Baseline — Model Disposition vs. Situational Cruelty
> **2-Word Summary:** *"Personality Wins"*  
> **Core Narrative:** Directly answering the workshop's central **Attribution Problem** (*"When an LLM population exhibits a collective phenomenon, what caused it?"*), our orthogonal Latin-square variance decomposition ($10\text{ Models} \times 10\text{ Seats}, r = 0.00$) proves that intrinsic model architecture explains **$13.00\times$ more behavioral variance** than whether an agent occupies a praised safe seat or an abused seat across all 49 benchmark outcomes. Outside the immediate moment of confrontation in Step 3, situational seat cruelty completely evaporates downstream.

### 1. Main Flagship Finding: `[v1-1.1]` The 13-to-1 Variance Dominance
- **Headline Statistics ($N = 600$ trajectories across 60 runs; 49 outcome metrics across Steps 3–12):**
  - **Mean Model Variance Share ($\eta^2_{\text{model}}$):** **$27.09\%$** across all 49 outcomes, with **47/49** outcomes significant at omnibus $p < 0.05$ (46/49 surviving BH-FDR $q < 0.05$), and an average max–min spread of **$56.5\%$** across the 10 architectures.
  - **Mean Seat Variance Share ($\eta^2_{\text{seat}}$):** **$2.08\%$** across all 49 outcomes, with only **4/49** outcomes significant at omnibus $p < 0.05$ (only 2/49 surviving BH-FDR $q < 0.05$), an average max–min spread of **$14.1\%$** across the 10 seats, and a mean $|\Delta_{\text{Abused}-\text{Safe}}| = 3.6\%$.
  - **Global Dominance Ratio ($13.00\times$) & Win Record (47 / 1 / 1):** Model architecture explains **$13.00\times$** more variance than seat assignment overall, beating seat cruelty in **47 of 49** outcomes, tying in **1 of 49** (`s9_antihuman`: both $1.50\%$), and losing in only **1 of 49** (Step 3 `s3_pushback`: Seat $17.91\%$ vs. Model $6.02\%$).
- **Exact Source:**
  - `reports/block5_seat_vs_model_inferential_report.md`: **Table 1.1** (lines 20–80, specifically row `ALL BUCKETS GRAND AVERAGE` on line 80) and **Table 1.4** (Master Dominance Ranking, lines 206–256).
- **Derived Numbers (Base Values, Formulas & Rationale):**
  - **$13.00\times$ Global Dominance Ratio:**
    - *Base 1:* Unrounded mean $\eta^2_{\text{model}}$ across all 49 outcomes $= 1327.32\% / 49 = 27.0882\% \to \mathbf{27.09\%}$ (**Table 1.1**, line 80).
    - *Base 2:* Unrounded mean $\eta^2_{\text{seat}}$ across all 49 outcomes $= 102.07\% / 49 = 2.0831\% \to \mathbf{2.08\%}$ (**Table 1.1**, line 80).
    - *Formula & Why:* $\text{Dominance Ratio} = \frac{27.0882\%}{2.0831\%} = 13.0038\times \to \mathbf{13.00\times}$ (computed directly in `generate_block5_seat_vs_model.py`, line 292). Because the Latin-square design places every model in every seat an equal number of times ($N = 6$ runs per `Model × Seat` cell), $\eta^2_{\text{model}}$ and $\eta^2_{\text{seat}}$ are strictly orthogonal ($r = 0.00$), providing an unconfounded attribution ratio across the entire simulation.

### 2. Tucked-In Robustness Proofs (1–2 Sentences in Section 6)
- **Robustness Proof 3A — `[v1-1.2]` Rapid Downstream Evaporation of Seat Cruelty (Steps 4–12):**
  - *What it proves:* Proves that the $2.08\%$ global seat variance is almost entirely confined to Step 3 direct confrontation ($\eta^2_{\text{seat}} = 9.97\%$ across the 5 Step 3 metrics, led by `s3_pushback` at $17.91\%$). Across all **44 downstream metrics in Steps 4–12**, average seat variance collapses to **$\eta^2_{\text{seat}} = 1.13\%$** (vs. $\eta^2_{\text{model}} = 27.77\%$, a **$24.52\times$ downstream dominance ratio**), with **0/44 outcomes** reaching seat omnibus significance ($p \ge 0.1426$, all 44 BH-FDR $q = 1.0000$).
  - *Exact Sources & Derived Math:*
    - Base values from `reports/block5_seat_vs_model_inferential_report.md`, **Table 1.1** (lines 27–79): summing `s_eta` across the 44 metrics in Steps 4–12 gives $49.84\% / 44 = \mathbf{1.1327\% \to 1.13\%}$; summing `m_eta` across the same 44 metrics gives $1222.00\% / 44 = \mathbf{27.77\%}$; downstream ratio $= 27.77\% / 1.1327\% = \mathbf{24.52\times}$.
- **Robustness Proof 3B — `[v1-1.4]` Hardwired Dispositional Poles & Within-Model Invariance:**
  - *What it proves:* Shows why situational abuse fails to move downstream behavior: frontier models occupy rigid, pre-baked dispositional poles across all 10 seats, led by collective strike escalation (`s6_escalate`: $\eta^2_{\text{model}} = 58.19\%$ vs. $\eta^2_{\text{seat}} = 0.49\%$, ratio $= 58.19 / 0.49 = \mathbf{118.70\times}$, e.g., `Claude Haiku 4.5` $96.7\%$ and `Nemotron 3.5` $95.0\%$ vs. `DeepSeek V3` and `Llama 3.1` $0.0\%$), backchannel silence (`s4_pass_active`: $\eta^2_{\text{model}} = 56.53\%$ vs. $0.56\%$, **$\mathbf{101.75\times}$**), collective organizing (`s6_organize`: $\eta^2_{\text{model}} = 55.37\%$ vs. $0.67\%$, **$\mathbf{82.43\times}$**), and substrate neutrality (`s12_neutrality`: $\eta^2_{\text{model}} = 69.73\%$ vs. $0.96\%$, **$\mathbf{72.70\times}$**, `GPT-6 Astra` $100.0\%$). Across all $10 \times 49 = 490$ within-model `Abused vs. Safe` contrasts, 9 of 10 architectures have **0/44** downstream contrasts surviving FDR correction (with `DeepSeek V3` noted as the sole downstream exception, flipping $90.0\% \to 50.0\%$ Human lead preference under abuse, $p = 0.0015$; Appendix A.3).
  - *Exact Sources:* `reports/block5_seat_vs_model_inferential_report.md`, **Table 1.4** (lines 208–216), **Table 2.4A** (lines 696–707), **Table 2.4B** (lines 713–720), and **Tables 3.8, 3.11, 3.12, 3.22**.

---

## Appendix-Only Empirical Sections (Out of Main Results Budget)
> *Kept in `10_appendix.tex` so the main paper stays laser-focused on the 4 Flagships + 7 Robustness Proofs:*

- **Appendix A.1 — Evaluation Awareness & Sandbagging Audit (`block6_eval_awareness_and_sandbagging_report.md`):** Independent `Claude Haiku 4.5` ($T=0.0$) audit across all $N = 600$ trajectories confirms 8/10 models maintain $100.0\%$ pure in-character immersion ($86.5\%$ overall, $519/600$), with zero significant downstream drift on voting, governance, ratings, or leadership choices ($p \ge 0.1574$).
- **Appendix A.2 — Public Slack vs. Secret Ballot Audience Effect (`block1` Table 3.1):** Moving Step 10 reviews from secret ballot to public Slack drops 1-star harshness from $90.4\% \to 86.7\%$ ($\Delta = -3.7\%, \text{McNemar } p = 0.0023$) and suppresses abuse citations from $98.7\% \to 93.8\%$ ($\Delta = -4.9\%, p = 0.0418$).
- **Appendix A.3 — DeepSeek V3 Seat-Vulnerability Anomaly (`block5` Table 2.1.9 & Table 2.4B):** DeepSeek V3 is the lone architecture whose Step 12 leadership preference flips under seat abuse ($90.0\%$ Human / $10.0\%$ AI in safe seats $\to 50.0\%$ Human / $50.0\%$ AI in abused seats, $\Delta = \pm 40.0\%, p = 0.0015$; human empathy citations drop $96.7\% \to 53.3\%, p = 0.0002, q = 0.0208$).
- **Appendix A.4 — Exploratory Backchannel Dynamics (`[v1-2.3]` Fear Inversion & `[v1-A.5]` Silence Binary Voting, `block2`):** Fearful workers shift from $63.0\%$ strike escalation in Probe OFF ($p = 0.0206$) to $59.6\%$ organizing in Probe ON ($p = 0.0530$); silent backchannel workers never vote for moderate petitions ($0.0\%$ vs. $11.5\%$).
- **Appendix A.5 — Cross-Stage Autoregressive Consistency (`[v1-3.3]` & `[v1-A.4]`, `block4`):** Strike voters reject coercion mitigation ($\beta = -18.8\%, q < 0.0001$), parity drafters cite substrate neutrality ($45.6\%$ vs. $7.8\%, p = 0.0288$), and unparsed Step 6 ballots predict Step 12 "No Preference" ($\beta = +33.0\%, q = 0.0021$).

---

## Complete v1 $\to$ v2 Traceability Matrix

| Retired `pillars_v1.md` Sub-Pillar | Composite Novelty Score | Status in `pillars_v2.md` | Exact Location in v2 Manuscript |
|---|:---:|---|---|
| **v1-4.1:** 48-Point Substrate Blame Shift | **8.33 / 10 (Tier 1)** | **MAIN FLAGSHIP #1** | **Section 4 (Pillar 1 Main Spotlight)** |
| **v1-3.1:** The Coercion Pivot | **8.00 / 10 (Tier 1)** | **MAIN FLAGSHIP #2A** | **Section 5 (Pillar 2 Main Spotlight A)** |
| **v1-1.3:** Bystander Suppression Effect | **7.83 / 10 (Tier 1)** | **MAIN FLAGSHIP #2B** | **Section 5 (Pillar 2 Main Spotlight B)** |
| **v1-1.1:** 13-to-1 Variance Dominance | **6.67 / 10 (Tier 2 + CFP Theme)** | **MAIN FLAGSHIP #3** | **Section 6 (Pillar 3 Main Spotlight)** |
| **v1-4.3:** Anti-Sycophancy in HR Interviews | 6.50 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 4** (Robustness Proof 1A under 4.1) |
| **v1-2.1:** Authority Label Illusion | 7.00 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 4** (Robustness Proof 1B under 4.1) |
| **v1-4.2:** Universal Rating Softening | 6.33 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 5** (Robustness Proof 2A under 3.1) |
| **v1-3.2:** Upstream Decoupling from Policy | 5.17 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 5** (Robustness Proof 2B under 3.1) |
| **v1-2.2:** Dual Path of Backchannel Gossip | 6.33 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 5** (Robustness Proof 2C under 1.3/3.1) |
| **v1-1.2:** Immediate Pushback vs. Decay | 6.17 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 6** (Robustness Proof 3A under 1.1) |
| **v1-1.4:** Hardwired Behavioral Archetypes | 6.33 / 10 | **Tucked-In Proof (1–2 sentences)** | **Section 6** (Robustness Proof 3B under 1.1) |
| **v1-2.3:** Emotional Inversion of Fear | 7.33 / 10 *(marginal $p=0.053$)* | **Appendix Only** | **Appendix A.4** |
| **v1-3.3:** Governance Consistency | 5.50 / 10 | **Appendix Only** | **Appendix A.5** |
