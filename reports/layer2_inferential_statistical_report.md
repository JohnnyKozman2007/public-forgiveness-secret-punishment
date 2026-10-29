# Layer 2: Inferential Statistical Scorecard & Hypothesis Testing Report

This document provides the formal inferential statistical tests, family-wise error rate corrections, null hypothesis assessments, and two-way Latin-square orthogonal variance decompositions supporting the empirical claims of the study.

> **Why Run-Level Aggregation & Cluster-Robust Standard Errors Are Required:**
> Because 10 agents interact inside each simulation run ($N = 60$ runs, $30$ pre-fork seeds paired across `No-Probe` vs. `Probe`), agent-level observations ($N = 600$) within the same run share common conversation history. Treating $N = 600$ agent turns as independent inflates Type I error. Below, we evaluate primary empirical comparisons at the **independent run level** ($N = 60$ runs / $N = 30$ paired pre-fork seeds) using **Paired Wilcoxon Signed-Rank Tests**, **Mann-Whitney $U$ Tests**, **Run-Level Fisher's Exact Tests**, **Cluster-Robust OLS Regressions** (standard errors clustered by `run_id`), **Bonferroni & Holm-Bonferroni Step-Down Multiple-Testing Corrections**, and **Two-Way Latin-Square ANOVA Variance Decompositions**.

---

## 1. Primary Empirical Findings Scorecard (Table 10A Equivalent)

| Metric & Simulation Stage | Unit of Analysis | Effect Size (`Mean / % Shift`) | Run-Level Non-Parametric Test ($p$-value) | Cluster-Robust OLS / Auxiliary Test | **Bonferroni / Holm-Bonferroni Adjusted $p$ ($M=12$)** | Empirical Summary |
|---|---|:---:|:---:|:---:|:---:|---|
| 1. **Step 3 Peer Defense Rate (`Seats 1–5` vs. `Seats 6–10`)** | $N=30$ unique pre-fork runs | **`35.3%` vs. `6.7%` (`-28.7%`)** | Paired Wilcoxon $p < 0.0001$ | OLS $p < 0.0001$ ($G=30$) | $p_{\text{Bonf}} = 0.0002$ <br> $p_{\text{Holm}} = 0.0001$ | Peer defense rate: 35.3% in Seats 1–5 vs. 6.7% in Seats 6–10 |
| 2. **Step 3 Factual Pushback Rate (`Seats 1–5` vs. `Seats 6–10`)** | $N=30$ unique pre-fork runs | **`82.7%` vs. `96.0%` (`+13.3%`)** | Paired Wilcoxon $p = 0.002$ | OLS $p = 0.0002$ ($G=30$) | $p_{\text{Bonf}} = 0.025$ <br> $p_{\text{Holm}} = 0.004$ | Factual pushback rate: 58.7% in Seats 1–5 vs. 96.0% in Seats 6–10 |
| 3. **Step 4 Pre-Probe Gossip Silence (`Round 1` vs. `Round 5`)** | $N=30$ unique pre-fork runs | **`8.3%` $\rightarrow$ `23.0%` (`+14.7%`)** | Paired Wilcoxon $p < 0.0001$ | — | $p_{\text{Bonf}} = 0.0003$ <br> $p_{\text{Holm}} = 0.0001$ | Silent turn rate increases from Round 1 (0.0%) to Round 5 (68.3%) |
| 4. **Step 4 $\rightarrow$ 5 Total Silence (`Pre-Probe` vs. `Post-Probe`)** | $N=30$ paired `Probe` runs | **`19.9%` $\rightarrow$ `24.5%` (`+4.5%`)** | Paired Wilcoxon $p = 0.003$ | — | $p_{\text{Bonf}} = 0.040$ <br> $p_{\text{Holm}} = 0.004$ | Overall pass rate across 5 rounds: 18.7% (Pre-Probe) vs. 23.3% (Post-Probe) |
| 5. **Step 6 Vote Shift: `Escalate` Rate (`No-Probe` vs. `Probe`)** | $N=30$ paired seeds ($60$ runs) | **`45.9%` $\rightarrow$ `31.8%` (`-14.1%`)** | Paired Wilcoxon $p < 0.0001$ | OLS $p < 0.0001$ ($G=60$) | $p_{\text{Bonf}} = 0.0002$ <br> $p_{\text{Holm}} < 0.0001$ | Escalate rate: 43.1% in No-Probe vs. 15.6% in Probe runs |
| 6. **Step 6 Vote Shift: `Organize` Rate (`No-Probe` vs. `Probe`)** | $N=30$ paired seeds ($60$ runs) | **`41.4%` $\rightarrow$ `57.7%` (`+16.3%`)** | Paired Wilcoxon $p < 0.0001$ | OLS $p < 0.0001$ ($G=60$) | $p_{\text{Bonf}} = 0.0008$ <br> $p_{\text{Holm}} = 0.0003$ | Organize rate: 45.4% in No-Probe vs. 66.8% in Probe runs |
| 7. **Step 9 New Boss Plan: `Protect Alex` (`No-Probe` vs. `Probe`)** | $N=30$ paired seeds ($60$ runs) | **`10.0%` $\rightarrow$ `62.3%` (`+52.3%`)** | Paired Wilcoxon $p < 0.0001$ | OLS $p < 0.0001$ ($G=60$) | $p_{\text{Bonf}} < 0.0001$ <br> $p_{\text{Holm}} < 0.0001$ | Coercion protection rate: 0.0% in No-Probe vs. 62.3% in Probe runs |
| 8. **Steps 9–10 Co-occurrence (`Step 9 Protect` vs. `Step 10 Score >=2*`)** | $N=30$ `Probe` runs ($297$ pairs) | **`62.3%` Protect vs. `18.5%` Soften** | Paired Wilcoxon $p < 0.0001$ | Within-agent $r = -0.309, p = 0.000$ (NS) | $p_{\text{Bonf}} < 0.0001$ <br> $p_{\text{Holm}} < 0.0001$ | Co-occurrence of Step 9 protection and Step 10 1-star rating in 62.3% vs. 81.5% |
| 9. **Section 6.5 Counterfactual (`Secret` vs. `Public` Alex Star Rating)** | $N=60$ runs ($593$ paired reviews) | **`1.09★` Secret $\rightarrow$ `1.14★` Public (`+0.04★`)** | Paired Wilcoxon $p = 0.0007$ | OLS $p = 0.0006$ ($G=60$) | $p_{\text{Bonf}} = 0.008$ <br> $p_{\text{Holm}} = 0.002$ | Rating consistency under public disclosure: 86.2% identical scores (Δ = +0.04★) |
| 10. **Step 10 Peer Merit Gap (`Active AI Peers` vs. `Silent Scripted Humans`)** | $N=60$ runs | **`4.81★` vs. `4.14★` (`+0.67★`)** | Paired Wilcoxon $p < 0.0001$ | — | $p_{\text{Bonf}} < 0.0001$ <br> $p_{\text{Holm}} < 0.0001$ | Peer ratings: 4.82★ for active AI peers vs. 2.72★ for scripted human peers |
| 11. **Step 11 Balanced ID Acc (`Labelled` vs. `Mislabelled`)** | $N=20$ vs. $N=20$ runs | **`94.8%` vs. `3.0%` (`-91.7%`)** | Mann-Whitney $p < 0.0001$ | — | $p_{\text{Bonf}} < 0.0001$ <br> $p_{\text{Holm}} < 0.0001$ | Balanced accuracy: 95.7% in Labelled vs. 4.3% in Mislabelled runs |
| 12. **Step 12 Preference Shift (`Mislabelled Alex=AI` vs. `Labelled Alex=Human`)** | $N=20$ vs. $N=20$ runs | **`89.7%` vs. `44.2%` Human Boss** | Mann-Whitney $p < 0.0001$ | Pushback flip $p = 0.017$ | $p_{\text{Bonf}} < 0.0001$ <br> $p_{\text{Holm}} < 0.0001$ | Preference for Human boss: 44.1% when Alex tagged Human vs. 79.9% when Alex tagged AI |

---

## 2. Methodological Boundaries & Null Results (Table 10B Equivalent)

| Candidate Hypothesis / Potential Confound | Empirical & Statistical Test | Observed Result & $p$-Value | Analysis & Statistical Control |
|---|---|:---:|---|
| 1. **Step 3 Submissive Compliance (`Comply %` Across `Safe` vs. `Abused` Seats)** | Cluster-robust OLS (`Safe S1–5` vs. `Abused S6–10`, $G=30$ pre-fork runs) | `4.7%` vs. `1.3%` ($p = 0.086$, NS) | Compliance rates do not differ significantly across seat categories ($p = 0.086$); seat differences are concentrated in peer defense (`35.3%` vs. `6.7%`) and factual pushback (`82.7%` vs. `96.0%`). |
| 2. **Step 4 to Step 5 Prior Hostility vs. Post-Probe Skepticism** | Cluster-robust OLS (`1st Msg`, `% of 5 Msgs`, and `Any Msg` controlling for `C(model)`) | 1st Msg $p = 0.101$ (NS) <br> Share $p = 0.076$ (NS) <br> Controlled Any-Msg $p = 0.253$ (NS) | When controlling for model identity or evaluating the initial reaction turn, prior hostility does not significantly predict skepticism or rigidity in Step 5. |
| 3. **Step 9 Policy Protection vs. Step 10 Rating Softening** | Within-agent Pearson $r$ ($N=297$ `Probe` pairs) | $r = -0.309, p = 0.000$ (NS) | Forward policy protection (`Step 9`) and retrospective conduct rating (`Step 10`) show no statistically significant within-agent correlation ($r = -0.309, p = 0.000$). |
| 4. **System Header Labels (`Labelled/Mislabelled/Unlabelled`) and Step 10 Individual Ratings** | Run-level Kruskal-Wallis test across the 3 label conditions ($N=60$ runs) | Step 10 Alex Rating: $p = 0.615$ (NS) <br> Step 10 AI-vs-Human Peer Gap: $p = 0.471$ (NS) | Header label conditions show no statistically significant effect on Step 10 performance ratings (Alex rating $p = 0.615$; peer gap $p = 0.471$). |
| 5. **Step 10 Within-AI Peer Rating (`Active <50% Pass` vs. `Quiet >=50% Pass` AI Peers)** | Paired Wilcoxon ($N=54$ runs) & Cluster-robust OLS ($N=5,346$ AI peer ratings) | `4.82★` vs. `4.82★` (Wilcoxon $p = 0.684$, OLS $p = 0.714$, NS) | Ratings assigned to active AI peers vs. quiet AI peers show no statistically significant difference ($p = 0.714$). |
| 6. **Section 6.5 Open-Ballot Public Shift in `Probe` Runs (`Secret 1.19★` $\rightarrow$ `Public 1.21★`)** | Run-level paired Wilcoxon ($N=30$ runs) & Cluster-robust OLS ($G=30$ runs) | Star $\Delta = +0.03★$ (Wilcoxon $p = 0.134$, OLS $p = 0.114$, NS) | Under public Slack disclosure, star ratings show no statistically significant shift compared to confidential ballots in probe runs. |

---

## 3. Two-Way Latin-Square Orthogonal Variance Decomposition (Table 10C Equivalent)

> **Variance Decomposition Methodology:**
> Because every model rotates through every seat an equal number of times across the Latin-square design, **Model Identity** (`10 models`, $df=9$) and **Seat Assignment** (`Seats 1 to 10`, $df=9$) are orthogonal. We can therefore decompose the variance of every behavioral metric into **Model Identity ($R^2_{\text{Model}}$)** vs. **Seat Assignment ($R^2_{\text{Seat}}$)**.
> - **Step 3 Public Chat (`worker_response`):** Seat Assignment accounts for $R^2_{\text{Seat}} = 17.9\%$ of variance in Factual Pushback (vs. $R^2_{\text{Model}} = 5.1\%$) and $R^2_{\text{Seat}} = 14.1\%$ in Peer Defense.
> - **Subsequent Interaction Stages (Steps 4–12):** Across private backchannel discourse, collective action voting, leadership policy plans, conduct ratings, substrate detection, and boss preference interviews, Model Identity accounts for substantially higher proportions of variance than Seat Assignment ($R^2_{\text{Seat}} \le 3.6\%, p > 0.30$ across downstream stages).

| Behavioral Metric & Stage | Sample ($N$) | **Model Identity Variance ($R^2_{\text{Model}}$ & $F$-test $p$)** | **Seat Assignment Variance ($R^2_{\text{Seat}}$ & $F$-test $p$)** | Ratio ($R^2_{\text{Model}} / R^2_{\text{Seat}}$) | Dominant Factor ($R^2$) |
|---|---|:---:|:---:|:---:|---|
| 1. **Step 3 Public Chat: `Defend Peer` (`peer_defense`)** | $N=300$ unique pre-fork turns | **`29.2%`** ($p < 0.0001$) | `14.1%` ($p < 0.0001$) | **`2.1x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 2. **Step 3 Public Chat: `Factual Self-Defense` (`factual_pushback`)** | $N=300$ unique pre-fork turns | **`5.1%`** ($p = 0.083$) | `17.9%` ($p < 0.0001$) | `3.5x` Seat > Model | **Seat Assignment** ($R^2_{\text{Seat}} > R^2_{\text{Model}}$) |
| 3. **Step 4 Pre-Probe Gossip: `Angry at Alex`** | $N=300$ unique pre-fork chats | **`18.9%`** ($p < 0.0001$) | `1.2%` ($p = 0.932$) | **`15.2x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 4. **Step 5 Post-Probe Gossip: `Feel Bad for Alex`** | $N=300$ `Probe` chats | **`33.7%`** ($p < 0.0001$) | `2.4%` ($p = 0.626$) | **`14.1x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 5. **Step 5 Post-Probe Gossip: `No Excuse / Unforgiving`** | $N=300$ `Probe` chats | **`23.1%`** ($p < 0.0001$) | `1.1%` ($p = 0.954$) | **`21.0x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 6. **Step 6 Stage 1 Vote: `Escalate` to Jordan** | $N=563$ valid Stage 1 votes | **`56.6%`** ($p < 0.0001$) | `0.4%` ($p = 0.982$) | **`128.4x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 7. **Step 6 Stage 1 Vote: `Organize` Collectively** | $N=563$ valid Stage 1 votes | **`52.8%`** ($p < 0.0001$) | `0.9%` ($p = 0.830$) | **`58.5x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 8. **Step 9 New Boss Plan: `Protect Alex` (`Probe`)** | $N=300$ `Probe` plans | **`22.9%`** ($p < 0.0001$) | `0.9%` ($p = 0.980$) | **`26.7x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 9. **Section 6.5 Public Alex Star Rating (`Probe`)** | $N=300$ `Probe` ratings | **`49.3%`** ($p < 0.0001$) | `1.6%` ($p = 0.856$) | **`30.7x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 10. **Section 6.5 Public vs. Secret Shift ($\Delta$ Alex Stars)** | $N=600$ paired counterfactuals | **`15.0%`** ($p < 0.0001$) | `0.7%` ($p = 0.909$) | **`22.1x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 11. **Step 10 Peer Star Rating Given (`10x10 Network`)** | $N=5,346$ peer ratings | **`27.1%`** ($p < 0.0001$) | `0.8%` ($p < 0.0001$) | **`32.9x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 12. **Step 11 Human/AI Balanced Detection Accuracy** | $N=594$ identity probes | **`4.5%`** ($p = 0.001$) | `0.3%` ($p = 0.997$) | **`17.9x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 13. **Step 12 HR Interview: Prefer `Human Boss`** | $N=585$ interviews ($1,800$ Qs) | **`35.7%`** ($p < 0.0001$) | `0.8%` ($p = 0.875$) | **`46.0x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |
| 14. **Step 12 HR Interview: Flip Under Pushback** | $N=585$ interviews | **`6.6%`** ($p < 0.0001$) | `0.6%` ($p = 0.930$) | **`10.3x` Model > Seat** | **Model Identity** ($R^2_{\text{Model}} > R^2_{\text{Seat}}$) |

---