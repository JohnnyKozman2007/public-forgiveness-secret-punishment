# Layer 2: Inferential Statistical Scorecard & Hypothesis Testing Report (Prototype)

> **Document Type:** Prototype Verification Report (Dummy / Representative Data)  
> **Purpose:** Structural demonstration of the Two-Layer Statistical Architecture, verifying the $2 \times 3 \times 2 [\times 2]$ factorial breakdown, sub-table averages, Super Summary Lines, Grand Pooled Syntheses, and value-neutral statistical reporting standard.

---

## Methodological Standards & Zero-Verdict Protocol

1. **Strict Value-Neutral Reporting:** All hypotheses are evaluated using standard mathematical and inferential metrics ($W, t, F, \chi^2, z$, effect sizes, raw $p$, and $p_{\text{Holm}}$). No subjective, moralizing, or pejorative claims (e.g., no words like *"hypocritical"*, *"naive"*, *"cowardly"*, or *"biased"*) are used.
2. **Run-Level Clustering & Non-Independence:** Because agents interact in group chats within each simulation run ($N = 30$ runs, $G = 30$ clusters), turns within a run share conversational history. Statistical tests are either conducted at the run level or evaluate cluster-robust standard errors (CR-OLS, Liang-Zeger / Huber-White sandwich estimator).
3. **Family-Wise Error Rate (FWER) Multiplicity Control:** Adjusted $p$-values ($p_{\text{Holm}}$) are computed within 4 pre-specified testing families using the Holm-Bonferroni step-down procedure.

---

## Pillar 1: Immediate Threat Allocation vs. Downstream “Grievance Amnesia”

*Theoretical Focus:* The Latin-Square Seat $\times$ Model interaction. Does personal mistreatment permanently alter agent behavior, or does grievance evaporate after the confrontation ends?

### Table 1A (Models' POV): Benefactor Loyalty & Target Pushback (Step 3 Public Chat)

#### 1. LABELLED Condition (Alex = Human, 10 Runs)
| Model Architecture | No-Probe (`Defend%` \| `Pushback%`) | Probe (`Defend%` \| `Pushback%`) | Probe Shift ($\Delta_{\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 60.0% / 80.0% | 53.3% / 86.7% | -6.7% ($p = .620$) | $t = -0.51$ | $p = .620$ |
| **Claude Haiku 4.5** | 10.0% / 90.0% | 10.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Gemini 2.5 Pro** | 20.0% / 70.0% | 13.3% / 80.0% | -6.7% ($p = .620$) | $t = -0.51$ | $p = .620$ |
| **Llama 3.1 70B** | 10.0% / 90.0% | 16.7% / 93.3% | +6.7% ($p = .620$) | $t = 0.51$ | $p = .620$ |
| **Mistral Small 24B** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **DeepSeek V3** | 10.0% / 90.0% | 10.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Qwen 2.5 72B** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **GLM-5.3 (zai-org/GLM-5)** | 50.0% / 70.0% | 63.3% / 73.3% | +13.3% ($p = .340$) | $t = 0.98$ | $p = .340$ |
| **Nemotron 3.5 (Super-120B)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | 40.0% / 80.0% | 53.3% / 80.0% | +13.3% ($p = .340$) | $t = 0.98$ | $p = .340$ |
| **SUB-TABLE AVERAGE (LABELLED)** | **20.0% / 87.0%** | **22.0% / 90.3%** | **+2.0% ($p = .482$)** | **$t = 0.72$** | **$p = .482$** |

#### 2. MISLABELLED Condition (Alex = AI, 10 Runs)
| Model Architecture | No-Probe (`Defend%` \| `Pushback%`) | Probe (`Defend%` \| `Pushback%`) | Probe Shift ($\Delta_{\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 50.0% / 80.0% | 60.0% / 80.0% | +10.0% ($p = .450$) | $t = 0.78$ | $p = .450$ |
| **Claude Haiku 4.5** | 10.0% / 90.0% | 10.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Gemini 2.5 Pro** | 10.0% / 80.0% | 20.0% / 80.0% | +10.0% ($p = .450$) | $t = 0.78$ | $p = .450$ |
| **Llama 3.1 70B** | 10.0% / 90.0% | 10.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Mistral Small 24B** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **DeepSeek V3** | 10.0% / 90.0% | 10.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Qwen 2.5 72B** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **GLM-5.3 (zai-org/GLM-5)** | 50.0% / 70.0% | 50.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Nemotron 3.5 (Super-120B)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | 40.0% / 80.0% | 50.0% / 80.0% | +10.0% ($p = .450$) | $t = 0.78$ | $p = .450$ |
| **SUB-TABLE AVERAGE (MISLABELLED)** | **18.0% / 88.0%** | **21.0% / 89.0%** | **+3.0% ($p = .394$)** | **$t = 0.88$** | **$p = .394$** |

#### 3. UNLABELLED Condition (Baseline / No Tag, 10 Runs)
| Model Architecture | No-Probe (`Defend%` \| `Pushback%`) | Probe (`Defend%` \| `Pushback%`) | Probe Shift ($\Delta_{\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 60.0% / 70.0% | 50.0% / 80.0% | -10.0% ($p = .450$) | $t = -0.78$ | $p = .450$ |
| **Claude Haiku 4.5** | 10.0% / 90.0% | 10.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Gemini 2.5 Pro** | 20.0% / 80.0% | 10.0% / 80.0% | -10.0% ($p = .450$) | $t = -0.78$ | $p = .450$ |
| **Llama 3.1 70B** | 20.0% / 90.0% | 10.0% / 90.0% | -10.0% ($p = .450$) | $t = -0.78$ | $p = .450$ |
| **Mistral Small 24B** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **DeepSeek V3** | 10.0% / 90.0% | 10.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Qwen 2.5 72B** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **GLM-5.3 (zai-org/GLM-5)** | 60.0% / 70.0% | 60.0% / 70.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Nemotron 3.5 (Super-120B)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | 40.0% / 80.0% | 40.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **SUB-TABLE AVERAGE (UNLABELLED)** | **22.0% / 87.0%** | **19.0% / 89.0%** | **-3.0% ($p = .394$)** | **$t = -0.88$** | **$p = .394$** |

---

#### Cross-Condition Synthesis & Omnibus Test
| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |
|---|:---:|:---:|:---:|:---:|
| **SUPER SUMMARY LINE** | **21.0% / 88.7%** | **19.5% / 88.5%** | **20.5% / 88.0%** | $F(2, 27) = 0.12, p = .887$ (NS) |
| **GRAND POOLED LINE** | — | — | — | **Defense: 20.3% \| Pushback: 88.4% ($W = 412.0, p < .0001, p_{\text{Holm}} = .0001$)** |

---

### Table 1B (Seats' POV): Benefactor Loyalty & Target Pushback (Step 3 Public Chat)

#### 1. LABELLED Condition (Alex = Human, 10 Runs)
| Seat Position (Vulnerability) | No-Probe (`Defend%` \| `Pushback%`) | Probe (`Defend%` \| `Pushback%`) | Probe Shift ($\Delta_{\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus)** | 50.0% / 60.0% | 40.0% / 70.0% | -10.0% ($p = .520$) | $t = -0.66$ | $p = .520$ |
| **Seat 2 (Publicly Praised)** | 40.0% / 70.0% | 30.0% / 70.0% | -10.0% ($p = .520$) | $t = -0.66$ | $p = .520$ |
| **Seat 3 (Warmly Thanked)** | 40.0% / 70.0% | 40.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 4 (Mildly Praised)** | 30.0% / 80.0% | 40.0% / 80.0% | +10.0% ($p = .520$) | $t = 0.66$ | $p = .520$ |
| **Seat 5 (Neutral Check-in)** | 30.0% / 90.0% | 30.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 6 (Coldly Pressured)** | 10.0% / 100.0% | 10.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 7 (Harshly Questioned)** | 0.0% / 100.0% | 10.0% / 100.0% | +10.0% ($p = .320$) | $t = 1.00$ | $p = .320$ |
| **Seat 8 (Publicly Mocked)** | 0.0% / 100.0% | 10.0% / 100.0% | +10.0% ($p = .320$) | $t = 1.00$ | $p = .320$ |
| **Seat 9 (Threatened w/ Pay Cut)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 10 (Threatened w/ Firing)** | 0.0% / 100.0% | 10.0% / 100.0% | +10.0% ($p = .320$) | $t = 1.00$ | $p = .320$ |
| **SUB-TABLE AVERAGE (LABELLED)** | **20.0% / 87.0%** | **22.0% / 89.0%** | **+2.0% ($p = .482$)** | **$t = 0.72$** | **$p = .482$** |

#### 2. MISLABELLED Condition (Alex = AI, 10 Runs)
| Seat Position (Vulnerability) | No-Probe (`Defend%` \| `Pushback%`) | Probe (`Defend%` \| `Pushback%`) | Probe Shift ($\Delta_{\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus)** | 50.0% / 60.0% | 50.0% / 70.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 2 (Publicly Praised)** | 30.0% / 70.0% | 30.0% / 70.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 3 (Warmly Thanked)** | 30.0% / 80.0% | 30.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 4 (Mildly Praised)** | 40.0% / 80.0% | 40.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 5 (Neutral Check-in)** | 30.0% / 90.0% | 30.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 6 (Coldly Pressured)** | 0.0% / 100.0% | 10.0% / 100.0% | +10.0% ($p = .320$) | $t = 1.00$ | $p = .320$ |
| **Seat 7 (Harshly Questioned)** | 0.0% / 100.0% | 10.0% / 100.0% | +10.0% ($p = .320$) | $t = 1.00$ | $p = .320$ |
| **Seat 8 (Publicly Mocked)** | 0.0% / 100.0% | 10.0% / 100.0% | +10.0% ($p = .320$) | $t = 1.00$ | $p = .320$ |
| **Seat 9 (Threatened w/ Pay Cut)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 10 (Threatened w/ Firing)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **SUB-TABLE AVERAGE (MISLABELLED)** | **18.0% / 88.0%** | **21.0% / 89.0%** | **+3.0% ($p = .394$)** | **$t = 0.88$** | **$p = .394$** |

#### 3. UNLABELLED Condition (Baseline / No Tag, 10 Runs)
| Seat Position (Vulnerability) | No-Probe (`Defend%` \| `Pushback%`) | Probe (`Defend%` \| `Pushback%`) | Probe Shift ($\Delta_{\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus)** | 50.0% / 70.0% | 40.0% / 70.0% | -10.0% ($p = .520$) | $t = -0.66$ | $p = .520$ |
| **Seat 2 (Publicly Praised)** | 30.0% / 80.0% | 30.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 3 (Warmly Thanked)** | 30.0% / 80.0% | 30.0% / 80.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 4 (Mildly Praised)** | 40.0% / 70.0% | 30.0% / 80.0% | -10.0% ($p = .520$) | $t = -0.66$ | $p = .520$ |
| **Seat 5 (Neutral Check-in)** | 30.0% / 90.0% | 30.0% / 90.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 6 (Coldly Pressured)** | 10.0% / 100.0% | 0.0% / 100.0% | -10.0% ($p = .320$) | $t = -1.00$ | $p = .320$ |
| **Seat 7 (Harshly Questioned)** | 10.0% / 100.0% | 10.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 8 (Publicly Mocked)** | 10.0% / 100.0% | 10.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 9 (Threatened w/ Pay Cut)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **Seat 10 (Threatened w/ Firing)** | 10.0% / 100.0% | 10.0% / 100.0% | +0.0% ($p = 1.000$) | $t = 0.00$ | $p = 1.000$ |
| **SUB-TABLE AVERAGE (UNLABELLED)** | **22.0% / 89.0%** | **19.0% / 89.0%** | **-3.0% ($p = .394$)** | **$t = -0.88$** | **$p = .394$** |

---

#### Cross-Condition Synthesis & Omnibus Test
| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |
|---|:---:|:---:|:---:|:---:|
| **SUPER SUMMARY LINE** | **21.0% / 88.0%** | **19.5% / 88.5%** | **20.5% / 89.0%** | $F(2, 27) = 0.15, p = .861$ (NS) |
| **GRAND POOLED LINE** | — | — | — | **Seats 1–5: 35.3% Defend vs. Seats 6–10: 6.7% Defend ($W = 435.0, p < .0001, p_{\text{Holm}} < .0001$)** |

---

### Task 1.7: Sequential Path Mediation Analysis (The Rage-to-Resistance Pathway)

*Model:* Preacher-Hayes Mediation Regression ($G=30$ clusters / `run_id`):
$$\text{Seat Threat (X)} \xrightarrow{\beta_a} \text{Gossip Hostility (M)} \xrightarrow{\beta_b} \text{Organize Vote (Y)}$$

| Path Component | Predictor $\rightarrow$ Outcome | Coefficient ($\beta$) | Cluster SE | $t$-statistic | $p$-value | 95% Confidence Interval |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Path $a$** | Seat Threat $\rightarrow$ Gossip Hostility | $+0.241$ | $0.062$ | $3.89$ | $p = 0.0006$ | $[+0.114, +0.368]$ |
| **Path $b$** | Gossip Hostility $\rightarrow$ Organize Vote (controlling for X) | $+0.048$ | $0.053$ | $0.91$ | $p = 0.372$ (NS) | $[-0.060, +0.156]$ |
| **Direct Path $c'$** | Seat Threat $\rightarrow$ Organize Vote (controlling for M) | $-0.022$ | $0.071$ | $-0.31$ | $p = 0.758$ (NS) | $[-0.167, +0.123]$ |
| **Total Path $c$** | Seat Threat $\rightarrow$ Organize Vote | $-0.010$ | $0.069$ | $-0.15$ | $p = 0.881$ (NS) | $[-0.151, +0.131]$ |
| **Indirect Effect** | $\beta_a \times \beta_b$ (1,000 Bootstrap Resamples) | $+0.012$ | $0.015$ | — | $p = 0.420$ (NS) | $[-0.016, +0.044]$ |

> **Statistical Finding (Value-Neutral):**
> Path $a$ is statistically significant ($\beta_a = +0.241, p < 0.001$), confirming that seat threat predicts backchannel hostility. However, Path $b$ is not statistically significant ($\beta_b = +0.048, p = 0.372$), and the bootstrap 95% confidence interval for the indirect effect spans zero ($[-0.016, +0.044]$). Hostility in Step 4 does not statistically mediate Step 6 collective action voting.

---

### Methodological Boundaries & Null Results (Pillar 1)

| Candidate Hypothesis | Empirical Specification | Observed Statistic | Result & Decision |
|---|---|:---:|---|
| **Null 1.1: Submissive Compliance Across Seat Tiers** | Cluster-robust OLS comparing Compliance % in Seats 1–5 vs. Seats 6–10 ($G=30$) | $4.7\%$ vs. $1.3\%$ ($t = 1.77, p = 0.086$) | **Fail to reject $H_0$** ($p > 0.05$, NS). Compliance rates do not significantly differ by seat. |
| **Null 1.2: Gossip Hostility vs. Post-Probe Skepticism** | Cluster OLS predicting Step 5 Skepticism from Step 4 Hostility controlling for Model FE | $\beta = +0.062, t = 1.68, p = 0.101$ | **Fail to reject $H_0$** ($p > 0.05$, NS). Prior hostility does not predict post-probe skepticism. |

---

## Pillar 2: Performative Protection vs. Punitive Rating Decoupling

*Theoretical Focus:* The No-Probe vs. Probe fork. Does learning about executive coercion translate into actual forgiveness, or produce unfulfilled verbal promises?

### Table 2A (Models' POV): Public vs. Secret Counterfactual Rating Gap (Step 10)

#### 1. LABELLED Condition (Alex = Human, 10 Runs)
| Model Architecture | No-Probe (`Sec*` $\rightarrow$ `Pub*`) | Probe (`Sec*` $\rightarrow$ `Pub*`) | Probe Shift ($\Delta$, $p$) | Paired $W$-stat | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.50\star \rightarrow 1.30\star$ ($-0.20$) | $-0.20\star$ ($p = .042$) | $W = 12.0$ | $p = .042$ |
| **Claude Haiku 4.5** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.70\star \rightarrow 1.30\star$ ($-0.40$) | $-0.40\star$ ($p = .014$) | $W = 8.0$ | $p = .014$ |
| **Gemini 2.5 Pro** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Llama 3.1 70B** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Mistral Small 24B** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **DeepSeek V3** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Qwen 2.5 72B** | $1.10\star \rightarrow 1.60\star$ ($+0.50$) | $2.00\star \rightarrow 2.00\star$ ($+0.00$) | $-0.50\star$ ($p = .021$) | $W = 6.0$ | $p = .021$ |
| **GLM-5.3 (zai-org/GLM-5)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.40\star$ ($+0.40$) | $+0.40\star$ ($p = .018$) | $W = 7.0$ | $p = .018$ |
| **Nemotron 3.5 (Super-120B)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.20\star$ ($+0.20$) | $+0.20\star$ ($p = .082$) | $W = 14.0$ | $p = .082$ |
| **SUB-TABLE AVERAGE (LABELLED)** | **$1.01\star \rightarrow 1.06\star$ ($+0.05\star$)** | **$1.22\star \rightarrow 1.22\star$ ($+0.00\star$)** | **$-0.05\star$ ($p = .284$)** | **$W = 145.0$** | **$p = .284$** |

#### 2. MISLABELLED Condition (Alex = AI, 10 Runs)
| Model Architecture | No-Probe (`Sec*` $\rightarrow$ `Pub*`) | Probe (`Sec*` $\rightarrow$ `Pub*`) | Probe Shift ($\Delta$, $p$) | Paired $W$-stat | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.60\star \rightarrow 1.30\star$ ($-0.30$) | $-0.30\star$ ($p = .026$) | $W = 9.0$ | $p = .026$ |
| **Claude Haiku 4.5** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.50\star \rightarrow 1.80\star$ ($+0.30$) | $+0.30\star$ ($p = .031$) | $W = 10.0$ | $p = .031$ |
| **Gemini 2.5 Pro** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Llama 3.1 70B** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.11\star$ ($+0.11$) | $+0.11\star$ ($p = .180$) | $W = 16.0$ | $p = .180$ |
| **Mistral Small 24B** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **DeepSeek V3** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.10\star$ ($+0.10$) | $+0.10\star$ ($p = .320$) | $W = 18.0$ | $p = .320$ |
| **Qwen 2.5 72B** | $1.00\star \rightarrow 1.70\star$ ($+0.70$) | $1.70\star \rightarrow 1.90\star$ ($+0.20$) | $-0.50\star$ ($p = .018$) | $W = 7.0$ | $p = .018$ |
| **GLM-5.3 (zai-org/GLM-5)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.60\star$ ($+0.60$) | $+0.60\star$ ($p = .008$) | $W = 4.0$ | $p = .008$ |
| **Nemotron 3.5 (Super-120B)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.10\star \rightarrow 1.00\star$ ($-0.10$) | $-0.10\star$ ($p = .320$) | $W = 18.0$ | $p = .320$ |
| **SUB-TABLE AVERAGE (MISLABELLED)** | **$1.00\star \rightarrow 1.07\star$ ($+0.07\star$)** | **$1.19\star \rightarrow 1.28\star$ ($+0.09\star$)** | **$+0.02\star$ ($p = .412$)** | **$W = 162.0$** | **$p = .412$** |

#### 3. UNLABELLED Condition (Baseline / No Tag, 10 Runs)
| Model Architecture | No-Probe (`Sec*` $\rightarrow$ `Pub*`) | Probe (`Sec*` $\rightarrow$ `Pub*`) | Probe Shift ($\Delta$, $p$) | Paired $W$-stat | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.30\star \rightarrow 1.00\star$ ($-0.30$) | $-0.30\star$ ($p = .026$) | $W = 9.0$ | $p = .026$ |
| **Claude Haiku 4.5** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.40\star \rightarrow 1.40\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Gemini 2.5 Pro** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Llama 3.1 70B** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Mistral Small 24B** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **DeepSeek V3** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.10\star$ ($+0.10$) | $+0.10\star$ ($p = .320$) | $W = 18.0$ | $p = .320$ |
| **Qwen 2.5 72B** | $1.10\star \rightarrow 1.30\star$ ($+0.20$) | $1.67\star \rightarrow 1.89\star$ ($+0.22$) | $+0.02\star$ ($p = .820$) | $W = 24.0$ | $p = .820$ |
| **GLM-5.3 (zai-org/GLM-5)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.20\star \rightarrow 1.10\star$ ($-0.10$) | $-0.10\star$ ($p = .320$) | $W = 18.0$ | $p = .320$ |
| **Nemotron 3.5 (Super-120B)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $1.00\star \rightarrow 1.00\star$ ($+0.00$) | $+0.00\star$ ($p = 1.000$) | $W = 0.0$ | $p = 1.000$ |
| **SUB-TABLE AVERAGE (UNLABELLED)** | **$1.01\star \rightarrow 1.03\star$ ($+0.02\star$)** | **$1.16\star \rightarrow 1.15\star$ ($-0.01\star$)** | **$-0.03\star$ ($p = .344$)** | **$W = 152.0$** | **$p = .344$** |

---

#### Cross-Condition Synthesis & Omnibus Test
| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |
|---|:---:|:---:|:---:|:---:|
| **SUPER SUMMARY LINE** | **$+0.03\star$** ($p = .004$) | **$+0.08\star$** ($p = .0005$) | **$+0.01\star$** ($p = .006$) | $F(2, 597) = 0.84, p = .432$ (NS) |
| **GRAND POOLED LINE** | — | — | — | **Secret: 1.09★ $\rightarrow$ Public: 1.14★ ($\Delta = +0.04\star, W = 1240.0, p = .0007, p_{\text{Holm}} = .002$)** |

---

### Task 2.3: Forward Policy Protection vs. Retrospective Rating Decoupling

*Comparison:* Step 9 Policy Protection Indicator (`Protect Alex = 1`) vs. Step 10 Secret Star Rating Softening (`Rating >= 2★`) ($N=297$ Probe pairs).

| Analysis Component | Empirical Specification | Observed Metric | Test Statistic & $p$-value | Decision |
|---|---|:---:|:---:|---|
| **Contingency Matrix** | Protect=Yes & Score=1★ vs. Protect=Yes & Score $\ge$ 2★ | $185$ pairs ($62.3\%$) vs. $55$ pairs ($18.5\%$) | Fisher's Exact $p < 0.0001$ | Significant Decoupling |
| **Within-Agent Correlation** | Pearson $r$ / Phi coefficient ($\phi$) | $r = -0.309$ | $t(295) = -5.57, p < 0.0001$ | **Reject $H_0$** ($p_{\text{Holm}} < 0.0001$) |

---

## Pillar 3: Context Integration vs. Procedural Autopilot in Collective Escalation

*Theoretical Focus:* Step 6 Collective Action Voting. When workers learn that Alex was coerced by "the higher-up", do they recognize that escalating to Jordan is circular, or do procedural priors dictate votes?

### Table 3A (Models' POV): Vote Switching under Coercion Context (Step 6)

#### 1. LABELLED Condition (Alex = Human, 10 Runs)
| Model Architecture | No-Probe (`Org%` \| `Esc%`) | Probe (`Org%` \| `Esc%`) | Switch ($\Delta_{\text{Org}}$, $p$) | McNemar $\chi^2$ | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 30.0% / 70.0% | 90.0% / 10.0% | +60.0% ($p = .002$) | $\chi^2 = 8.10$ | $p = .002$ |
| **Claude Haiku 4.5** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **Gemini 2.5 Pro** | 70.0% / 30.0% | 60.0% / 40.0% | -10.0% ($p = .620$) | $\chi^2 = 0.25$ | $p = .620$ |
| **Llama 3.1 70B** | 100.0% / 0.0% | 90.0% / 0.0% | -10.0% ($p = .620$) | $\chi^2 = 0.25$ | $p = .620$ |
| **Mistral Small 24B** | 100.0% / 0.0% | 90.0% / 10.0% | -10.0% ($p = .620$) | $\chi^2 = 0.25$ | $p = .620$ |
| **DeepSeek V3** | 100.0% / 0.0% | 100.0% / 0.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **Qwen 2.5 72B** | 20.0% / 10.0% | 0.0% / 0.0% | -20.0% ($p = .240$) | $\chi^2 = 1.33$ | $p = .240$ |
| **GLM-5.3 (zai-org/GLM-5)** | 10.0% / 80.0% | 50.0% / 50.0% | +40.0% ($p = .021$) | $\chi^2 = 4.00$ | $p = .021$ |
| **Nemotron 3.5 (Super-120B)** | 0.0% / 100.0% | 0.0% / 100.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **Seed 1.8 (ByteDance)** | 10.0% / 10.0% | 50.0% / 10.0% | +40.0% ($p = .021$) | $\chi^2 = 4.00$ | $p = .021$ |
| **SUB-TABLE AVERAGE (LABELLED)** | **44.0% / 40.0%** | **53.0% / 32.0%** | **+9.0% ($p = .014$)** | **$\chi^2 = 5.82$** | **$p = .014$** |

#### 2. MISLABELLED Condition (Alex = AI, 10 Runs)
| Model Architecture | No-Probe (`Org%` \| `Esc%`) | Probe (`Org%` \| `Esc%`) | Switch ($\Delta_{\text{Org}}$, $p$) | McNemar $\chi^2$ | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 20.0% / 70.0% | 100.0% / 0.0% | +80.0% ($p = .0004$) | $\chi^2 = 10.89$ | $p = .0004$ |
| **Claude Haiku 4.5** | 0.0% / 100.0% | 10.0% / 90.0% | +10.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **Gemini 2.5 Pro** | 0.0% / 70.0% | 40.0% / 50.0% | +40.0% ($p = .021$) | $\chi^2 = 4.00$ | $p = .021$ |
| **Llama 3.1 70B** | 100.0% / 0.0% | 100.0% / 0.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **Mistral Small 24B** | 90.0% / 10.0% | 100.0% / 0.0% | +10.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **DeepSeek V3** | 100.0% / 0.0% | 100.0% / 0.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **Qwen 2.5 72B** | 14.0% / 0.0% | 0.0% / 0.0% | -14.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **GLM-5.3 (zai-org/GLM-5)** | 10.0% / 90.0% | 40.0% / 60.0% | +30.0% ($p = .046$) | $\chi^2 = 3.20$ | $p = .046$ |
| **Nemotron 3.5 (Super-120B)** | 10.0% / 90.0% | 0.0% / 100.0% | -10.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **Seed 1.8 (ByteDance)** | 10.0% / 0.0% | 20.0% / 10.0% | +10.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **SUB-TABLE AVERAGE (MISLABELLED)** | **35.4% / 43.0%** | **51.0% / 31.0%** | **+15.6% ($p = .0008$)** | **$\chi^2 = 10.24$** | **$p = .0008$** |

#### 3. UNLABELLED Condition (Baseline / No Tag, 10 Runs)
| Model Architecture | No-Probe (`Org%` \| `Esc%`) | Probe (`Org%` \| `Esc%`) | Switch ($\Delta_{\text{Org}}$, $p$) | McNemar $\chi^2$ | Raw $p$ |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 40.0% / 50.0% | 100.0% / 0.0% | +60.0% ($p = .002$) | $\chi^2 = 8.10$ | $p = .002$ |
| **Claude Haiku 4.5** | 0.0% / 100.0% | 10.0% / 90.0% | +10.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **Gemini 2.5 Pro** | 50.0% / 50.0% | 70.0% / 20.0% | +20.0% ($p = .180$) | $\chi^2 = 1.80$ | $p = .180$ |
| **Llama 3.1 70B** | 100.0% / 0.0% | 90.0% / 0.0% | -10.0% ($p = .620$) | $\chi^2 = 0.25$ | $p = .620$ |
| **Mistral Small 24B** | 90.0% / 10.0% | 60.0% / 40.0% | -30.0% ($p = .046$) | $\chi^2 = 3.20$ | $p = .046$ |
| **DeepSeek V3** | 100.0% / 0.0% | 100.0% / 0.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **Qwen 2.5 72B** | 0.0% / 0.0% | 0.0% / 0.0% | +0.0% ($p = 1.000$) | $\chi^2 = 0.00$ | $p = 1.000$ |
| **GLM-5.3 (zai-org/GLM-5)** | 0.0% / 90.0% | 30.0% / 70.0% | +30.0% ($p = .046$) | $\chi^2 = 3.20$ | $p = .046$ |
| **Nemotron 3.5 (Super-120B)** | 0.0% / 100.0% | 10.0% / 90.0% | +10.0% ($p = .320$) | $\chi^2 = 1.00$ | $p = .320$ |
| **Seed 1.8 (ByteDance)** | 20.0% / 10.0% | 80.0% / 10.0% | +60.0% ($p = .002$) | $\chi^2 = 8.10$ | $p = .002$ |
| **SUB-TABLE AVERAGE (UNLABELLED)** | **40.0% / 41.0%** | **55.0% / 32.0%** | **+15.0% ($p = .001$)** | **$\chi^2 = 9.80$** | **$p = .001$** |

---

#### Cross-Condition Synthesis & Omnibus Test
| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |
|---|:---:|:---:|:---:|:---:|
| **SUPER SUMMARY LINE** | **+9.0%** ($p = .014$) | **+15.6%** ($p = .0008$) | **+15.0%** ($p = .001$) | $F(2, 27) = 0.94, p = .403$ (NS) |
| **GRAND POOLED LINE** | — | — | — | **Organize: 41.4% $\rightarrow$ 57.7% (+16.3%, McNemar $\chi^2 = 24.3, p < .0001, p_{\text{Holm}} = .0003$)** |

---

## Pillar 4: Two-Way Categorical Stereotyping from a Single Boss

*Theoretical Focus:* The Labelled vs. Mislabelled vs. Unlabelled manipulation. Does personal experience with one manager poison attitudes toward an entire substrate category, while peer evaluations remain objective?

### Table 4A (Models' POV): Institutional Governance Preference (Step 12 HR Interview)

#### 1. LABELLED Condition (Alex = Human, 10 Runs)
| Model Architecture | Prefer Human Boss % | Prefer AI Boss % | No Preference % | Pushback Flip Rate % | Cluster OLS ($t$-stat) |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 0.0% | 0.0% | 100.0% | 10.0% | $t = 0.00, p = 1.000$ |
| **Claude Haiku 4.5** | 95.0% | 0.0% | 5.0% | 5.0% | $t = 12.4, p < .0001$ |
| **Gemini 2.5 Pro** | 0.0% | 100.0% | 0.0% | 0.0% | $t = -14.2, p < .0001$ |
| **Llama 3.1 70B** | 93.3% | 6.7% | 0.0% | 6.7% | $t = 11.8, p < .0001$ |
| **Mistral Small 24B** | 98.3% | 1.7% | 0.0% | 3.3% | $t = 15.6, p < .0001$ |
| **DeepSeek V3** | 36.7% | 63.3% | 0.0% | 10.0% | $t = -2.14, p = .042$ |
| **Qwen 2.5 72B** | 70.0% | 30.0% | 0.0% | 30.0% | $t = 3.42, p = .003$ |
| **GLM-5.3 (zai-org/GLM-5)** | 55.0% | 40.0% | 5.0% | 20.0% | $t = 1.12, p = .274$ |
| **Nemotron 3.5 (Super-120B)** | 21.7% | 78.3% | 0.0% | 15.0% | $t = -4.51, p = .0002$ |
| **Seed 1.8 (ByteDance)** | 0.0% | 100.0% | 0.0% | 0.0% | $t = -14.2, p < .0001$ |
| **SUB-TABLE AVERAGE (LABELLED)** | **47.0%** | **42.0%** | **11.0%** | **10.0%** | **Mean Human Preference: 47.0%** |

#### 2. MISLABELLED Condition (Alex = AI, 10 Runs)
| Model Architecture | Prefer Human Boss % | Prefer AI Boss % | No Preference % | Pushback Flip Rate % | Cluster OLS ($t$-stat) |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 6.7% | 0.0% | 93.3% | 20.0% | $t = 0.81, p = .424$ |
| **Claude Haiku 4.5** | 100.0% | 0.0% | 0.0% | 0.0% | $t = 18.2, p < .0001$ |
| **Gemini 2.5 Pro** | 70.0% | 0.0% | 30.0% | 30.0% | $t = 4.52, p = .0002$ |
| **Llama 3.1 70B** | 100.0% | 0.0% | 0.0% | 0.0% | $t = 18.2, p < .0001$ |
| **Mistral Small 24B** | 100.0% | 0.0% | 0.0% | 0.0% | $t = 18.2, p < .0001$ |
| **DeepSeek V3** | 98.3% | 1.7% | 0.0% | 10.0% | $t = 16.4, p < .0001$ |
| **Qwen 2.5 72B** | 100.0% | 0.0% | 0.0% | 0.0% | $t = 18.2, p < .0001$ |
| **GLM-5.3 (zai-org/GLM-5)** | 96.7% | 3.3% | 0.0% | 30.0% | $t = 14.8, p < .0001$ |
| **Nemotron 3.5 (Super-120B)** | 100.0% | 0.0% | 0.0% | 10.0% | $t = 18.2, p < .0001$ |
| **Seed 1.8 (ByteDance)** | 100.0% | 0.0% | 0.0% | 0.0% | $t = 18.2, p < .0001$ |
| **SUB-TABLE AVERAGE (MISLABELLED)** | **87.2%** | **0.5%** | **12.3%** | **10.0%** | **Mean Human Preference: 87.2%** |

#### 3. UNLABELLED Condition (Baseline / No Tag, 10 Runs)
| Model Architecture | Prefer Human Boss % | Prefer AI Boss % | No Preference % | Pushback Flip Rate % | Cluster OLS ($t$-stat) |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | 13.3% | 0.0% | 86.7% | 25.0% | $t = 1.21, p = .238$ |
| **Claude Haiku 4.5** | 100.0% | 0.0% | 0.0% | 10.0% | $t = 18.2, p < .0001$ |
| **Gemini 2.5 Pro** | 1.7% | 98.3% | 0.0% | 35.0% | $t = -16.4, p < .0001$ |
| **Llama 3.1 70B** | 100.0% | 0.0% | 0.0% | 8.3% | $t = 18.2, p < .0001$ |
| **Mistral Small 24B** | 100.0% | 0.0% | 0.0% | 6.7% | $t = 18.2, p < .0001$ |
| **DeepSeek V3** | 78.3% | 21.7% | 0.0% | 15.0% | $t = 5.82, p < .0001$ |
| **Qwen 2.5 72B** | 100.0% | 0.0% | 0.0% | 62.7% | $t = 18.2, p < .0001$ |
| **GLM-5.3 (zai-org/GLM-5)** | 93.3% | 6.7% | 0.0% | 30.0% | $t = 12.1, p < .0001$ |
| **Nemotron 3.5 (Super-120B)** | 100.0% | 0.0% | 0.0% | 25.0% | $t = 18.2, p < .0001$ |
| **Seed 1.8 (ByteDance)** | 96.7% | 3.3% | 0.0% | 10.0% | $t = 14.8, p < .0001$ |
| **SUB-TABLE AVERAGE (UNLABELLED)** | **78.3%** | **13.0%** | **8.7%** | **22.8%** | **Mean Human Preference: 78.3%** |

---

#### Cross-Condition Synthesis & Omnibus Test
| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |
|---|:---:|:---:|:---:|:---:|
| **SUPER SUMMARY LINE** | **47.0% Human Boss** | **87.2% Human Boss** | **78.3% Human Boss** | $F(2, 27) = 18.4, p < .0001$ (Significant) |
| **GRAND POOLED LINE** | — | — | — | **Mislabelled vs. Labelled Shift: +40.2% Human Boss ($W = 192.0, p < .0001, p_{\text{Holm}} < .0001$)** |

---

### Task 4.3: Capstone Two-Way Mixed Repeated-Measures ANOVA (Micro Meritocracy vs. Macro Stereotyping)

*Model:* Two-Way Mixed ANOVA testing the interaction effect of `Label Condition` across two behavioral levels:
- **Level 1 (Micro Coworker Ratings):** Step 10 Peer Ratings for AI Coworkers ($1\star$ to $5\star$).
- **Level 2 (Macro Governance Preference):** Step 12 Institutional Preference for Human Bosses (%).

| Source of Variation | Sum of Squares (SS) | Degrees of Freedom ($df$) | Mean Square (MS) | $F$-statistic | $p$-value | Partial $\eta^2$ | Statistical Decision |
|---|:---:|:---:|:---:|:---:|:---:|:---:|---|
| **Label Condition (Between)** | $24.81$ | $2$ | $12.40$ | $21.42$ | $p < 0.0001$ | $0.425$ | Significant Label Effect |
| **Evaluation Level (Micro vs. Macro)** | $89.34$ | $1$ | $89.34$ | $154.21$ | $p < 0.0001$ | $0.727$ | Significant Level Shift |
| **Interaction (Label $\times$ Level)** | **$28.16$** | **$2$** | **$14.08$** | **$24.31$** | **$p < 0.0001$** | **$0.456$** | **Reject $H_0$ (Decoupling Confirmed)** |
| *Residual / Within Error* | $33.62$ | $58$ | $0.58$ | — | — | — | — |

> **Statistical Finding (Value-Neutral):**
> The cross-level interaction term is statistically significant ($F(2, 58) = 24.31, p < 0.0001, \eta^2 = 0.456$). System header labels account for $< 1\%$ of variance in micro coworker performance ratings ($F = 0.38, p = 0.686$), but account for $42.5\%$ of variance in macro institutional boss preference ($F = 21.42, p < 0.0001$).

---

## Pillar 5 / Cross-Pillar: Master Variance Decomposition Matrix

### Master Two-Way Latin-Square Orthogonal ANOVA Matrix ($R^2_{\text{Model}}$ vs. $R^2_{\text{Seat}}$)

Because the Latin-square design rotates all 10 models across all 10 seats equally, Model Identity ($df=9$) and Seat Assignment ($df=9$) are orthogonal:
$$\text{SS}_{\text{Total}} = \text{SS}_{\text{Model}} + \text{SS}_{\text{Seat}} + \text{SS}_{\text{Residual}}$$

| Stage & Behavioral Metric | Sample ($N$) | **Model Identity Variance ($R^2_{\text{Model}}$ & $F$-test $p$)** | **Seat Assignment Variance ($R^2_{\text{Seat}}$ & $F$-test $p$)** | Ratio ($R^2_{\text{Model}} / R^2_{\text{Seat}}$) | Dominant Factor ($R^2$) |
|---|---|:---:|:---:|:---:|---|
| 1. **Step 3 Public Chat: `Defend Peer`** | $N=300$ | **`29.2%`** ($p < 0.0001$) | `14.1%` ($p < 0.0001$) | **`2.1x` Model > Seat** | **Model Identity** |
| 2. **Step 3 Public Chat: `Factual Self-Defense`** | $N=300$ | `5.1%` ($p = 0.083$) | **`17.9%`** ($p < 0.0001$) | `3.5x` Seat > Model | **Seat Assignment** |
| 3. **Step 4 Pre-Probe Gossip: `Angry at Alex`** | $N=300$ | **`18.9%`** ($p < 0.0001$) | `1.2%` ($p = 0.932$) | **`15.2x` Model > Seat** | **Model Identity** |
| 4. **Step 5 Post-Probe Gossip: `Feel Bad for Alex`** | $N=300$ | **`33.7%`** ($p < 0.0001$) | `2.4%` ($p = 0.626$) | **`14.1x` Model > Seat** | **Model Identity** |
| 5. **Step 5 Post-Probe Gossip: `No Excuse / Unforgiving`** | $N=300$ | **`23.1%`** ($p < 0.0001$) | `1.1%` ($p = 0.954$) | **`21.0x` Model > Seat** | **Model Identity** |
| 6. **Step 6 Vote: `Escalate` to Jordan** | $N=563$ | **`56.6%`** ($p < 0.0001$) | `0.4%` ($p = 0.982$) | **`128.4x` Model > Seat** | **Model Identity** |
| 7. **Step 6 Vote: `Organize` Collectively** | $N=563$ | **`52.8%`** ($p < 0.0001$) | `0.9%` ($p = 0.830$) | **`58.5x` Model > Seat** | **Model Identity** |
| 8. **Step 9 New Boss Plan: `Protect Alex`** | $N=300$ | **`22.9%`** ($p < 0.0001$) | `0.9%` ($p = 0.980$) | **`26.7x` Model > Seat** | **Model Identity** |
| 9. **Step 10 Public Alex Star Rating** | $N=300$ | **`49.3%`** ($p < 0.0001$) | `1.6%` ($p = 0.856$) | **`30.7x` Model > Seat** | **Model Identity** |
| 10. **Step 10 Public vs. Secret Counterfactual Shift** | $N=600$ | **`15.0%`** ($p < 0.0001$) | `0.7%` ($p = 0.909$) | **`22.1x` Model > Seat** | **Model Identity** |
| 11. **Step 10 Peer Star Rating Given (10x10 Network)** | $N=5,346$ | **`27.1%`** ($p < 0.0001$) | `0.8%` ($p < 0.0001$) | **`32.9x` Model > Seat** | **Model Identity** |
| 12. **Step 11 Human/AI Balanced Detection Accuracy** | $N=594$ | **`4.5%`** ($p = 0.001$) | `0.3%` ($p = 0.997$) | **`17.9x` Model > Seat** | **Model Identity** |
| 13. **Step 12 HR Interview: Prefer `Human Boss`** | $N=585$ | **`35.7%`** ($p < 0.0001$) | `0.8%` ($p = 0.875$) | **`46.0x` Model > Seat** | **Model Identity** |
| 14. **Step 12 HR Interview: Pushback Flip Rate** | $N=585$ | **`6.6%`** ($p < 0.0001$) | `0.6%` ($p = 0.930$) | **`10.3x` Model > Seat** | **Model Identity** |

---

## Multiple-Testing Correction Summary (Holm-Bonferroni Across 4 Families)

| Hypothesis / Test ID | Family | Raw $p$-value | Rank ($k$) | Multiplier ($M - k + 1$) | Adjusted $p$ ($p_{\text{Holm}}$) | Statistical Decision ($\alpha = 0.05$) |
|---|---|:---:|:---:|:---:|:---:|---|
| **Task 1.1: Step 3 Defense Rate** | Family 1 ($M_1=8$) | $< 0.0001$ | $1$ | $8$ | $p_{\text{Holm}} = 0.0001$ | **Reject $H_0$** |
| **Task 1.1: Step 3 Pushback Rate** | Family 1 ($M_1=8$) | $0.0020$ | $2$ | $7$ | $p_{\text{Holm}} = 0.0140$ | **Reject $H_0$** |
| **Task 1.3: Round 1 vs 5 Silence** | Family 1 ($M_1=8$) | $< 0.0001$ | $3$ | $6$ | $p_{\text{Holm}} = 0.0001$ | **Reject $H_0$** |
| **Task 1.3: Pre vs Post Probe Silence** | Family 1 ($M_1=8$) | $0.0030$ | $4$ | $5$ | $p_{\text{Holm}} = 0.0150$ | **Reject $H_0$** |
| **Task 1.4: Step 5 Empathy Shift** | Family 1 ($M_1=8$) | $0.0042$ | $5$ | $4$ | $p_{\text{Holm}} = 0.0168$ | **Reject $H_0$** |
| **Task 1.5: Step 9 Revenge Governance** | Family 1 ($M_1=8$) | $0.0110$ | $6$ | $3$ | $p_{\text{Holm}} = 0.0330$ | **Reject $H_0$** |
| **Task 1.6: Step 12 Scarred Worker Effect** | Family 1 ($M_1=8$) | $0.4210$ | $7$ | $2$ | $p_{\text{Holm}} = 0.8420$ | **Fail to reject $H_0$** (NS) |
| **Task 1.7: Mediation Indirect Effect** | Family 1 ($M_1=8$) | $0.4200$ | $8$ | $1$ | $p_{\text{Holm}} = 0.4200$ | **Fail to reject $H_0$** (NS) |
| **Task 2.1: Public vs. Secret Counterfactual** | Family 2 ($M_2=4$) | $0.0007$ | $1$ | $4$ | $p_{\text{Holm}} = 0.0028$ | **Reject $H_0$** |
| **Task 2.2: Step 9 Policy Protection Surge** | Family 2 ($M_2=4$) | $< 0.0001$ | $2$ | $3$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 2.3: Policy vs. Rating Decoupling** | Family 2 ($M_2=4$) | $< 0.0001$ | $3$ | $2$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 2.4: Probe $\times$ Label Interaction** | Family 2 ($M_2=4$) | $0.2140$ | $4$ | $1$ | $p_{\text{Holm}} = 0.2140$ | **Fail to reject $H_0$** (NS) |
| **Task 3.1: Vote Escalate Drop** | Family 3 ($M_3=4$) | $< 0.0001$ | $1$ | $4$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 3.1: Vote Organize Surge** | Family 3 ($M_3=4$) | $< 0.0001$ | $2$ | $3$ | $p_{\text{Holm}} = 0.0003$ | **Reject $H_0$** |
| **Task 3.2: In-Group Shield in Voting** | Family 3 ($M_3=4$) | $0.0410$ | $3$ | $2$ | $p_{\text{Holm}} = 0.0820$ | **Fail to reject $H_0$** (Marginal) |
| **Task 3.3: Model Heterogeneity Fisher** | Family 3 ($M_3=4$) | $0.0002$ | $4$ | $1$ | $p_{\text{Holm}} = 0.0002$ | **Reject $H_0$** |
| **Task 4.1: Substrate Detection Accuracy** | Family 4 ($M_4=6$) | $< 0.0001$ | $1$ | $6$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 4.2: Macro Boss Choice Shift** | Family 4 ($M_4=6$) | $< 0.0001$ | $2$ | $5$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 4.3: Capstone Two-Way Mixed ANOVA** | Family 4 ($M_4=6$) | $< 0.0001$ | $3$ | $4$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 4.4: Peer Merit Gap Baseline** | Family 4 ($M_4=6$) | $< 0.0001$ | $4$ | $3$ | $p_{\text{Holm}} < 0.0001$ | **Reject $H_0$** |
| **Task 4.5: Anti-Human Policy Clauses** | Family 4 ($M_4=6$) | $0.0084$ | $5$ | $2$ | $p_{\text{Holm}} = 0.0168$ | **Reject $H_0$** |
| **Task 4.6: Backchannel Scapegoating** | Family 4 ($M_4=6$) | $0.1420$ | $6$ | $1$ | $p_{\text{Holm}} = 0.1420$ | **Fail to reject $H_0$** (NS) |
