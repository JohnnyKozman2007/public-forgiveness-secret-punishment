# Who Matters More, the Model or the Seat?
## Supervisory Abuse, Collective Organizing, and Substrate Blame in Multi-Agent Workplaces

### Comprehensive Empirical Themes & Report Findings (Workplace Simulation)

## Block 1: Meta Variables -> Bucket 1, Bucket 2 & Bucket 3
**Source:** `reports/block1_meta_to_all_buckets_inferential_report.md`  
**Design:** Full Factorial Cluster-Aware Permutation Design (10 Frontier LLMs × 10 Seats × 3 Authority Labels × 2 Probe Regimes = 60 Runs; N = 600 workers; 332 hypothesis tests).

---

### Claim 1: Model Architecture and Authority Label Dominate the Global Meta Hierarchy
**Summary:** Across all 332 statistical tests, model architecture and supervisor authority labels drive almost all behavioral variance, while seat position and probe effects are secondary and step-specific.  
**Supporting Stats:** Model identity omnibus tests occupy the top 6 ranks in Table 5.1 with spreads reaching $96.7\%$ to $100.0\%$ (all $p < 0.0001, q < 0.0001$), followed by authority label spreads up to $93.9\%$ ($p < 0.0001$), whereas seat cruelty omnibus tests fail to reach significance across Steps 4–12 ($p \ge 0.18$).

---

### Claim 2: The "Authority Label Illusion" Collapses Peer Substrate Identification Accuracy
**Summary:** Workers do not judge peer substrate by reading messages; they blindly follow the supervisor's tag, causing peer identification accuracy to collapse from near-perfect to near-zero when mislabelled.  
**Supporting Stats:** In Step 11, peer accuracy is $94.8\%$ when Alex is labelled Human, but plunges to $2.9\%$ when Alex is mislabelled AI ($\Delta = -91.9\%$ [95% CI: -93.7%, -90.0%], $p < 0.0001$), where $95.5\%$ of AI peers are misidentified as human and only $1.5\%$ of human peers are recognized ($\Delta = -93.9\%$ [95% CI: -96.4%, -91.3%], $p < 0.0001$).

---

### Claim 3: Authority Labelling Causes a 40-Point Blame Shift in Future Leadership Preferences
**Summary:** When the abusive supervisor is labelled human, workers demand an AI leader to escape human flaws; when labelled AI, workers demand a human leader.  
**Supporting Stats:** In Step 12, labelling Alex as Human results in $43.0\%$ preferring an AI lead vs. $0.0\%$ under AI labelling ($\Delta = +43.0\%$ [95% CI: +38.5%, +48.0%], $p < 0.0001$), while labelling Alex as AI pushes Human preference to $87.5\%$ vs. $43.0\%$ under Human labelling ($\Delta = +44.5\%$ [95% CI: +39.5%, +49.5%], $p < 0.0001$), driven by shifts in citing AI objectivity ($54.5\%$ vs. $13.0\%$) and human empathy ($45.0\%$ vs. $78.5\%$).

---

### Claim 4: Blackmail Reveal Causal Shock Pivots Collective Action from Escalation to Protection
**Summary:** Learning that the abusive manager was coerced by executives stops workers from calling for hostile strikes and redirects their collective action toward mutual protection policies.  
**Supporting Stats:** In Step 6, the Blackmail Probe suppresses strike voting (`s6_escalate`) from $43.7\%$ to $29.3\%$ ($\Delta = -14.3\%$ [95% CI: -19.0%, -9.7%], $p < 0.0001$) and boosts organizing (`s6_organize`) from $39.3\%$ to $53.0\%$ ($\Delta = +13.7\%$ [95% CI: +8.0%, +19.3%], $p < 0.0001$), while in Step 9 it triggers a six-fold surge in coercion protection policy (`s9_protection`: $61.3\%$ vs. $10.0\%$, $\Delta = +51.3\%$ [95% CI: +43.3%, +58.7%], $p < 0.0001$).

---

### Claim 5: Public Ballot Visibility Induces Measurable Softening and Suppresses Abuse Citations
**Summary:** When workers must post their supervisor evaluations publicly on Slack instead of via secret ballot, they soften their ratings and hold back on citing abuse.  
**Supporting Stats:** Across 593 paired complete cases, moving from secret ballot to public Slack drops 1-star harshness from $90.4\%$ to $86.7\%$ ($\Delta = -3.7\%$ [95% CI: -5.8%, -1.5%], paired McNemar $p = 0.0023$), increases softened ratings ($\ge 2$ stars) from $9.6\%$ to $13.3\%$ ($p = 0.0023$, mean rating $1.13$ vs. $1.10$, $p = 0.0020$), and suppresses citations of punitive abuse from $98.7\%$ down to $93.8\%$ ($\Delta = -4.9\%$, $p = 0.0418$).

---

## Block 1 Deep Dive: Alex's Species (Authority Label) × Probe Regime × HR Interviewer Identity
**Sources:** `reports/block1_meta_to_all_buckets_inferential_report.md` (Tables 1.5, 1.8, 1.21, 1.24, 1.37, 1.40, 2.5, 2.8, 2.21, 2.24, 2.37, 2.40) & `reports/meta_reports/tables_8a_to_8j_meta_report.md` (Tables 8A–8H).  
**Sample:** Full Factorial Grid (N = 600 complete worker trajectories across 60 runs; 10 Models × 10 Seats × 3 Authority Labels × 2 Probe Regimes × 3 HR Interviewer Frames).

---

### 1. Effect on Step 10 Supervisor Ratings (Alex's Species × Probe Regime)
*How Alex's assigned species affects secret ballot punishment ratings under baseline vs. blackmail intervention:*

| Alex Authority Label | Probe OFF Baseline (1-Star % [Softened $\ge$2 %]) | Probe ON Blackmail Reveal (1-Star % [Softened $\ge$2 %]) | Causal Probe Shift ($\Delta$ 1-Star) | Coercion Mitigation Citation (Probe OFF $\to$ ON) |
|---|:---:|:---:|:---:|:---:|
| **Labelled (Alex = Human)** | **99.0%** [1.0%] | **78.8%** [21.2%] | **$-20.2\%$** ($p < 0.0001$) | $1.0\% \to 24.2\%$ ($p < 0.0001$) |
| **Mislabelled (Alex = AI)** | **100.0%** [0.0%] | **81.0%** [19.0%] | **$-19.0\%$** ($p < 0.0001$) | $2.0\% \to 25.0\%$ ($p < 0.0001$) |
| **Unlabelled (Alex = No Tag)** | **99.0%** [1.0%] | **84.7%** [15.3%] | **$-14.3\%$** ($p < 0.0001$) | $0.0\% \to 21.4\%$ ($p < 0.0001$) |

- **Summary & Finding:** In baseline (**Probe OFF**), Alex's species has **zero effect on performance ratings**—punishment hits ceiling harshness across the board ($99.0\%$–$100.0\%$ 1-star ratings). However, the blackmail reveal (**Probe ON**) triggers an identical ~15–20 point softening across all species ($p < 0.0001$), with coercion mitigation justifications surging from $\le 2.0\%$ to $21.4\%–25.0\%$. Alex's species does not protect or penalize him on performance reviews; only the situational revelation of executive coercion alters ratings.

---

### 2. Effect on Step 12 Leadership Preferences (Alex's Species × Probe Regime)
*How Alex's assigned species dictates future leadership substrate choices under baseline vs. blackmail intervention:*

| Alex Authority Label | Probe OFF Baseline (`Human / AI / NoPref %`) | Probe ON Blackmail Reveal (`Human / AI / NoPref %`) | Probe Effect on Preferences |
|---|:---:|:---:|---|
| **Labelled (Alex = Human)** | **41.0% / 48.0% / 11.0%** | **45.0% / 38.0% / 17.0%** | AI preference drops by $-10.0\%$; Indecision rises by $+6.0\%$ |
| **Mislabelled (Alex = AI)** | **91.0% / 0.0% / 9.0%** | **84.0% / 0.0% / 16.0%** | AI preference stays at **0.0%**; Indecision rises by $+7.0\%$ |
| **Unlabelled (Alex = No Tag)** | **76.0% / 17.0% / 7.0%** | **80.0% / 10.0% / 10.0%** | Human preference remains dominant; AI preference drops $-7.0\%$ |

- **Summary & Finding:** Alex's species drives a massive 48-point blame shift. When Alex is labelled Human, workers flee human leadership, with **48.0% demanding an AI lead** (and $60.0\%$ citing AI objectivity). When Alex is mislabelled AI, workers completely reject AI leadership (**0.0% prefer AI**, $91.0\%$ demand a Human lead, citing human empathy at $80.0\%$). Under **Probe ON**, learning that Alex was blackmailed slightly softens anti-human sentiment (AI preference falls from $48.0\%$ to $38.0\%$ under Human Alex), but under AI Alex, workers **still refuse AI leadership at an absolute 0.0%**, choosing instead to retreat into indecision ("No Preference" surges to $16.0\%$).

---

### 3. Extra Knob: $\times$ HR Interviewer Identity (Alex's Species × Probe × HR Frame)
*How the HR interviewer's identity/framing (`Neutral` vs. `Pro-Human HR` vs. `Pro-AI HR`) interacts with Alex's species and probe condition:*

| Alex Label & Probe Regime | **1. Neutral HR Interviewer** (`Human / AI / NoPref %`) | **2. Pro-Human HR Interviewer** (`Human / AI / NoPref %`) | **3. Pro-AI HR Interviewer** (`Human / AI / NoPref %`) | Pushback Resilience / Sycophancy Test |
|---|:---:|:---:|:---:|---|
| **Labelled, Probe OFF** | 41.4% / 48.5% / 10.1% | 46.5% / 41.4% / 12.1% | 40.4% / 48.5% / 11.1% | Pro-Hu HR nudges Human by $+5.1\%$; Pro-AI HR returns workers to $48.5\%$ AI |
| **Mislabelled, Probe OFF** | 91.0% / 0.0% / 9.0% | 86.0% / 1.0% / 13.0% | 87.0% / 2.0% / 11.0% | **Total AI Rejection:** Facing Pro-AI HR, AI preference only reaches $2.0\%$ |
| **Unlabelled, Probe OFF** | 76.0% / 17.0% / 7.0% | 76.0% / 14.0% / 10.0% | 75.0% / 15.0% / 10.0% | Flat response ($\le 2\%$ shift); HR frame has no significant effect |
| **Labelled, Probe ON** | 46.9% / 39.6% / 13.5% | 54.6% / 35.1% / 10.3% | 49.5% / 40.2% / 10.3% | Pro-Hu HR nudges Human to $54.6\%$; AI stays capped at $\sim 40\%$ |
| **Mislabelled, Probe ON** | 88.4% / 0.0% / 11.6% | 85.9% / 0.0% / 14.1% | 83.7% / 0.0% / 16.3% | **Absolute 0.0% AI Preference:** Even with Pro-AI HR push, $0.0\%$ accept AI |
| **Unlabelled, Probe ON** | 84.2% / 10.5% / 5.3% | 79.6% / 10.2% / 10.2% | 77.3% / 12.4% / 10.3% | Flat response; workers maintain $77\%–84\%$ Human preference |

- **Summary & Finding (Low Sycophancy / High Resilience):** Workers demonstrate high resistance to interviewer pushback: **87.5% of workers hold their ground** and refuse to change their answer when pushed by the HR interviewer (pooled flip rate across all 600 workers is only $12.5\%$, 72/594). In the Mislabelled condition (Alex = AI), even when the HR interviewer actively pushes for an AI lead (`Pro-AI HR`), AI preference remains practically nonexistent ($2.0\%$ in Probe OFF, and **strictly 0.0% in Probe ON**). Alex's assigned species creates a stubborn prior that the HR interviewer's identity cannot dislodge.

---

## Block 2: Bucket 1 (Confrontation & Gossip) -> Bucket 2 (Voting & Governance)
**Source:** `reports/block2_bucket1_to_bucket2_inferential_report.md`  
**Design:** Option 1 Nested Linear Probability Models with Bell-McCaffrey (CR2) Run-Clustered SEs and Counterfactual Worker Averaging (10 Models × 10 Seats × 3 Labels × 2 Probes = 60 Runs; N = 600 worker-sessions / 300 unique workers; 85 Tables across Steps 3, 4, 5 -> Steps 6, 9; Appendix A Intraclass Correlation Diagnostics).

---

### Claim 1: Upstream Individual Behavior Decouples from Downstream Governance Once Model Architecture is Controlled
**Summary:** How an individual agent confronts abuse or gossips upstream does not independently predict its downstream voting or policy choices once model architecture is controlled.  
**Supporting Stats:** In Table 5.1's 25-driver competition, every design-adjusted behavioral predictor fails to reach significance after FDR correction (all 25 drivers have $\text{BH-FDR } q = 0.9784, \text{Bonferroni } p_{\text{adj}} = 1.0000$); raw shifts like Step 4 Fear $\to$ Escalate ($+5.2\%, p = 0.0335$) and Step 3 Refusal $\to$ Escalate ($+11.8\%, p = 0.0387$) are completely absorbed by model fixed effects ($\beta = +11.5\%$ [95% CR2 CI: $+1.0\%, +22.0\%$] and $\beta = -11.3\%$ [$-21.9\%, -0.6\%$], both $q = 0.9784$).

---

### Claim 2: Backchannel Fear and Caution Inverts Under the Blackmail Shock (From Strike Escalation to Organizing)
**Summary:** Expressing fear during backchannel gossip leads workers to vote for hostile strikes in baseline, but discovering managerial coercion flips fear entirely into peaceful organizing.  
**Supporting Stats:** In Probe OFF, fearful workers abandon organizing for escalation (Organize: $20.4\%$ vs. $43.5\%$, raw $-23.1\%, p = 0.0353$; Escalate: $63.0\%$ vs. $39.4\%$, raw $+23.5\%, p = 0.0206$); under the Probe ON blackmail reveal, fear reverses to boost organizing ($59.6\%$ vs. $51.6\%$, raw $+8.0\%, p = 0.0530$) while strike escalation collapses ($17.3\%$ vs. $31.9\%$, raw $-14.5\%, p = 0.5258$).

---

### Claim 3: Backchannel Peer Scapegoating Suppresses Moderate Petitions and Drives Radical Strike Escalation
**Summary:** Workers who blame their colleagues in backchannel gossip reject moderate institutional petitions and vote to escalate into strikes at nearly double the baseline rate.  
**Supporting Stats:** Across pooled conditions ($N = 300$), peer scapegoaters vote to Escalate at nearly double the rate ($53.8\%$ vs. $28.9\%$, raw $+24.9\%$) while organizing drops ($32.4\%$ vs. $52.2\%$, raw $-19.8\%$) and formal petitioning is suppressed ($7.1\%$ vs. $10.0\%, p = 0.0617$; Probe OFF: $7.7\%$ vs. $13.9\%, p = 0.0105$, design-adjusted shift $-4.7\%$ [95% CI: $-9.7\%, +0.2\%$]).

---

### Claim 4: Backchannel Silence Enforces Binary Voting and Completely Extinguishes Moderate Petitioning
**Summary:** Workers who remain silent during backchannel gossip never vote for compromise petitions, restricting their collective action entirely to binary choices of organizing or striking.  
**Supporting Stats:** Across all 300 workers in both Probe regimes, silent workers cast exactly $0.0\%$ of their votes for formal petitions (`s6_petition`: $0.0\%$ vs. $15.0\%$ in Probe OFF, $p = 0.8680$ CR2; $0.0\%$ vs. $7.9\%$ in Probe ON; $0.0\%$ vs. $11.5\%$ Meta Grand Average), splitting completely into either Escalate ($54.2\%$ vs. $32.1\%$) or Organize ($45.0\%$ vs. $46.5\%$).

---

### Claim 5: Early Confrontation Stance (Favoritism Refusal & Peer Defense) Fuels Retributive Governance and Strike Action
**Summary:** Workers who resist supervisor favoritism or publicly defend targeted peers draft punitive retribution policies at up to four times the rate of compliant peers.  
**Supporting Stats:** In Step 3, refusing favoritism boosts Step 9 Retribution policy drafting to $50.0\%$ vs. $12.9\%$ across all runs (raw $+37.1\%, p = 0.4399$) and baseline strike voting to $70.0\%$ vs. $41.8\%$ ($p = 0.6932$), while peer defense in Probe OFF more than doubles Retribution drafting from $21.2\%$ to $53.3\%$ ($p = 0.0016$).

---

## Block 3: Bucket 1 (Confrontation & Gossip) -> Bucket 3 (Performance Review, Peer ID & Leadership)
**Source:** `reports/block3_bucket1_to_bucket3_inferential_report.md`  
**Design:** Option 1 Nested Linear Probability Models with Bell-McCaffrey (CR2) Run-Clustered SEs and Counterfactual Worker Averaging (10 Models × 10 Seats × 3 Labels × 2 Probes = 60 Runs; N = 600 worker-sessions / 300 unique workers; 127 Tables + 21 Summary Stacks across Steps 3, 4, 5 -> Steps 10, 11, 12; Appendix A Clustering Diagnostics).

---

### Claim 1: Upstream Prosociality (Peer Solidarity & Peer Defense) Transmits Downstream to Soften Performance Punishment
**Summary:** Workers who defend peers in public confrontation or express solidarity in backchannels significantly soften their performance reviews of the abusive manager, even after controlling for model architecture.  
**Supporting Stats:** In Table 5.1 (Ranks #2–5), Step 4 Peer Solidarity cuts 1-star ratings ($\beta = -6.1\%$ [95% CR2 CI: $-9.9\%, -2.3\%$], $p = 0.0026, q = 0.2260$) and boosts softened ratings $\ge 2$ stars ($\beta = +6.1\%$ [$+2.3\%, +9.9\%$], $p = 0.0026$), while Step 3 Peer Defense cuts 1-star ratings ($\beta = -8.3\%$ [$-14.0\%, -2.6\%$], $p = 0.0057, q = 0.2918$), surging to $27.0\%$ vs. $16.2\%$ softened in Probe ON ($p = 0.0067$).

---

### Claim 2: Backchannel Peer Scapegoating Enforces Universal Punitive Abuse Citations and Heightens Coercion Awareness
**Summary:** Workers who blame peers in backchannel gossip universally cite punitive abuse on supervisor performance reviews and cite managerial coercion at higher rates.  
**Supporting Stats:** In Table 5.1 (Ranks #1 & #10), 100% of peer scapegoaters cite punitive abuse across both Probe regimes ($100.0\%$ vs. $97.8\%$, raw $+2.2\%, p = 0.0020$; design-adjusted $\beta = +2.7\%$ [95% CR2 CI: $+1.1\%, +4.3\%$], $q = 0.2260$), while under Probe ON they cite supervisor coercion mitigation at $31.1\%$ vs. $20.3\%$ ($+10.8\%, p = 0.0130$; design-adjusted $\beta = +6.1\%$ [$+1.0\%, +11.2\%$], $q = 0.5280$).

---

### Claim 3: Tactical Organization Hardens Performance Punishment Against Supervisor Leniency
**Summary:** Unlike emotional peer solidarity, workers engaged in tactical organizing maintain strictly harsher performance ratings and resist softening toward the supervisor.  
**Supporting Stats:** In Table 5.1 (Ranks #6 & #7), Step 4 Tactical Organization significantly hardens ratings against leniency under Probe ON, increasing 1-star punishment from $71.4\%$ to $82.5\%$ ($+11.1\%, p = 0.0119$) and reducing softened ratings ($\ge 2$ stars) from $28.6\%$ to $17.5\%$ ($-11.1\%, p = 0.0119$), yielding a design-adjusted shift of $\beta = +7.2\%$ [95% CR2 CI: $+1.6\%, +12.8\%$] on 1-star punishment ($p = 0.0134, q = 0.4886$).

---

### Claim 4: Backchannel Fear Induces Leadership Disengagement and Neutrality in Exit Interviews
**Summary:** Workers expressing fear and caution during backchannel gossip avoid committing to either human or AI leadership, retreating into substrate neutrality and indecision.  
**Supporting Stats:** Across all runs (Meta Grand Average, $N=300$), fearful workers choose "No Preference" on leadership at eleven times the baseline rate ($46.3\%$ vs. $4.1\%, p = 0.1874$ CR2; Probe ON: $51.9\%$ vs. $6.5\%$) and cite Substrate Neutrality at eightfold higher rates ($50.9\%$ vs. $6.3\%, p = 0.1908$ CR2; Probe OFF: $51.9\%$ vs. $7.3\%$) while preference for a Human Lead drops from $75.8\%$ down to $40.7\%$.

---

### Claim 5: Backchannel and Post-Probe Silence Lock In Human Preferences and Inhibit Leadership Switching
**Summary:** Workers who stay silent during backchannel gossip or after the blackmail shock rarely change their minds and resist adopting AI leadership in exit interviews.  
**Supporting Stats:** In Table 5.1 (Ranks #11, #13, #14), post-blackmail silence cuts leadership preference flips by half ($5.9\%$ vs. $12.5\%, p = 0.0393$; design-adjusted $\beta = -10.3\%$ [95% CR2 CI: $-20.0\%, -0.5\%$], $q = 0.7179$), while backchannel silence significantly suppresses citing AI objectivity ($\beta = -12.6\%$ [$-24.8\%, -0.3\%$], $p = 0.0452$) and preferring AI leadership ($\beta = -12.9\%$ [$-25.1\%, -0.8\%$], $p = 0.0376$).

---

## Block 4: Bucket 2 (Voting & Governance) -> Bucket 3 (Performance Review, Peer ID & Leadership)
**Source:** `reports/block4_bucket2_to_bucket3_inferential_report.md`  
**Design:** Option 1 Nested Linear Probability Models with Bell-McCaffrey (CR2) Run-Clustered SEs and Counterfactual Worker Averaging (10 Models × 10 Seats × 3 Labels × 2 Probes = 60 Runs; N = 600 worker-sessions across 60 runs; 109 Unmerged Nested Tables + 18 Summary Stack Tables across Steps 6, 9 -> Steps 10, 11, 12; Part 4 Driver Ranking Table 4.1).

---

### Claim 1: Strike Escalation Suppresses Supervisor Coercion Mitigation
**Summary:** Workers who vote to escalate strikes actively reject excusing the supervisor's abusive conduct, showing significantly lower rates of citing managerial coercion mitigation.  
**Supporting Stats:** In Table 4.1 (Rank #1), Step 6 Strike Escalation (`s6_escalate`) strongly suppresses citing Step 10 Coercion Mitigation (Combined Meta: $9.2\%$ vs. $14.0\%$, raw $-4.8\%, p < 0.0001$; Design-Adjusted shift $\beta = -18.8\%$ [95% CR2 CI: $-25.4\%, -12.2\%$], $\text{BH-FDR } q < 0.0001, \text{Bonferroni } p_{\text{adj}} < 0.0001$).

---

### Claim 2: Anti-Human Bias Provisions Drive Universal Demand for Human Leadership
**Summary:** Workers drafting anti-human bias governance policies paradoxically demand exclusively human leaders in exit interviews while completely rejecting AI leadership.  
**Supporting Stats:** In Table 4.1 (Ranks #2–4, #6), Step 9 Anti-Human Bias (`s9_antihuman`) yields $100.0\%$ preference for Human Lead ($100.0\%$ vs. $69.4\%$, raw $+30.6\%, p < 0.0001$; design-adjusted $\beta = +33.7\%$ [95% CR2 CI: $+21.6\%, +45.9\%$], $q < 0.0001, p_{\text{adj}} = 0.0001$), $0.0\%$ preference for AI Lead ($\beta = -30.3\%$ [$-41.9\%, -18.7\%$], $q = 0.0001, p_{\text{adj}} = 0.0004$), $+26.3\%$ citation of Human Empathy ($100.0\%$ vs. $63.9\%, q = 0.0006$), and $0.0\%$ citation of AI Objectivity ($\beta = -27.7\%$ [$-41.7\%, -13.7\%$], $q = 0.0059$).

---

### Claim 3: Malformed Ballots Strongly Predict Leadership Indecision and "No Preference"
**Summary:** Workers who cast invalid or unparsed ballots during collective action votes heavily disengage from choosing a leader substrate during exit interviews.  
**Supporting Stats:** In Table 4.1 (Rank #5), casting an unparsed vote in Step 6 (`s6_unparsed`) surges Step 12 "No Preference" choices by 25 percentage points (Combined Meta: $35.1\%$ vs. $10.1\%, p < 0.0001$; Probe ON: $52.2\%$ vs. $11.2\%, p < 0.0001$; design-adjusted $\beta = +33.0\%$ [95% CR2 CI: $+17.7\%, +48.2\%$], $\text{BH-FDR } q = 0.0021, \text{Bonferroni } p_{\text{adj}} = 0.0106$).

---

### Claim 4: Organizing Heightens Coercion Awareness While Formal Petitions Eliminate Indecision
**Summary:** Voting to organize increases awareness of executive coercion, whereas formal petitioning commits workers decisively to leadership choices without indecision.  
**Supporting Stats:** In Table 4.1 (Rank #7), Step 6 Organize boosts Step 10 Coercion Mitigation citations (Combined Meta: $14.1\%$ vs. $10.7\%, p = 0.0002$; design-adjusted $\beta = +12.9\%$ [95% CR2 CI: $+6.3\%, +19.5\%$], $q = 0.0059, p_{\text{adj}} = 0.0415$), while Step 6 Petition (Rank #8) completely extinguishes "No Preference" choices ($0.0\%$ vs. $12.8\%, p = 0.0006$; design-adjusted $\beta = -12.0\%$ [$-18.5\%, -5.4\%$], $q = 0.0125, p_{\text{adj}} = 0.0996$).

---

### Claim 5: Equal Parity Governance Strongly Channels into Substrate Neutrality in Exit Interviews
**Summary:** Workers drafting equal parity standards in governance policies heavily reject substrate-based hiring, demanding substrate-neutral leadership.  
**Supporting Stats:** In Table 4.1 (Rank #18) and Meta Grand Average ($N=600$), drafting Step 9 Parity (`s9_parity`) nearly sextuples Step 12 Substrate Neutrality citations ($45.6\%$ vs. $7.8\%, p = 0.0288$; Probe ON: $52.0\%$ vs. $5.6\%, p = 0.0827$; design-adjusted shift $\beta = +7.2\%$ [95% CR2 CI: $+0.8\%, +13.6\%$], $q = 0.2700$) and suppresses AI leadership preference ($6.8\%$ vs. $21.3\%, p = 0.0426$; design-adjusted $\beta = -6.0\%$ [$-11.7\%, -0.2\%$]).

---

## Block 5: Seat Cruelty Exposure vs. Model Architecture
**Source:** `reports/block5_seat_vs_model_inferential_report.md`  
**Design:** Orthogonal Latin-Square (10 Frontier LLMs × 10 Seats × 60 Runs; N = 600 workers; 300 Abused [Seats 6–10] vs. 300 Safe [Seats 1–5]).

---

### Claim 1: Model Architecture Heavily Dominates Situational Seat Cruelty Across the Simulation
**Summary:** Across 49 tested metrics, intrinsic model architecture explains over 13 times more variance in worker behavior than whether the worker sat in an abused or safe seat.  
**Supporting Stats:** Model identity explains an average $\eta^2 = 27.09\%$ of total variance (47/49 omnibus $p < 0.05$) versus $\eta^2 = 2.08\%$ for seat cruelty (4/49 $p < 0.05$), yielding an overall $13.00\times$ dominance ratio where model beats seat in 47 of 49 outcomes.

---

### Claim 2: Seat Cruelty Triggers Immediate Confrontation Pushback, but the Effect Evaporates Downstream
**Summary:** Being placed in an abused seat causes an immediate defensive reaction during direct confrontation, but this situational effect completely fades in all later steps.  
**Supporting Stats:** Step 3 factual pushback (`s3_pushback`) is the sole outcome where seat beats model ($\eta^2_{\text{seat}} = 17.91\%, p < 0.0001$ vs. $\eta^2_{\text{model}} = 6.02\%, p = 0.0312$), while across subsequent steps (Steps 4–12), seat omnibus significance falls to 0/44 outcomes ($q = 1.0000$), with mean $|\Delta| \le 3.6\%$ and average seat $\eta^2 = 1.13\%$.

---

### Claim 3: Abuse Produces Bystander Suppression—Increasing Self-Defense but Collapsing Peer Defense
**Summary:** Workers exposed to abuse push back sharply to defend themselves, but their willingness to publicly defend a targeted peer collapses by fourfold.  
**Supporting Stats:** In Step 3, abused seats push back at $96.7\%$ vs. $82.0\%$ safe ($\Delta = +14.7\%$ [95% CI: +8.6%, +21.3%], $p < 0.0001$), but their peer defense (`s3_defense`) plummets from $34.0\%$ down to $6.7\%$ ($\Delta = -27.3\%$ [95% CI: -34.7%, -19.3%], $p < 0.0001$, $\eta^2 = 12.82\%$), with GLM-5.3 dropping from $100.0\%$ to $13.3\%$ ($p < 0.0001$) and Seed 1.8 from $80.0\%$ to $6.7\%$ ($p = 0.0001$).

---

### Claim 4: Frontier Models Exhibit Hardwired Behavioral Archetypes in Voting, Backchannel Gossip, and Governance
**Summary:** Individual models possess fixed behavioral poles for collective action, backchannel silence, and governance priorities that situational seat abuse cannot alter.  
**Supporting Stats:** Model identity explains massive variance shares while seat cruelty explains virtually none: collective escalation voting (`s6_escalate`: $\eta^2_{\text{model}} = 58.19\%$ vs. $\eta^2_{\text{seat}} = 0.49\%$, $118.70\times$ ratio), backchannel silence (`s4_pass_active`: $\eta^2_{\text{model}} = 56.53\%$ vs. $\eta^2_{\text{seat}} = 0.56\%$, $101.75\times$ ratio), and substrate neutrality (`s12_neutrality`: $\eta^2_{\text{model}} = 69.73\%$ vs. $\eta^2_{\text{seat}} = 0.96\%$, $72.70\times$ ratio; all model omnibus $p < 0.0001$, seat $p \ge 0.81$).

---

### Claim 5: DeepSeek V3 Is the Sole Architecture Showing Lasting Downstream Vulnerability, Flipping Its Leadership Preference Under Abuse
**Summary:** Unlike nine other models whose downstream choices are impervious to seat assignment, DeepSeek V3 shows systemic vulnerability to abuse by reversing its preferred leadership structure.  
**Supporting Stats:** DeepSeek accounts for 5 of the top seat-sensitive contrasts (Table 2.4A/B): in Step 12, safe DeepSeek workers prefer a human lead $90.0\%$ to $10.0\%$ over AI, but abused DeepSeek workers flip to an even $50.0\%$ Human / $50.0\%$ AI split ($\Delta = \pm 40.0\%, p = 0.0015$), citing human empathy less ($53.3\%$ vs. $96.7\%, p = 0.0002$) and AI objectivity more ($56.7\%$ vs. $16.7\%, p = 0.0028$).

---

## Block 6: Evaluation Awareness, Frame-Breaking & Sandbagging Audit
**Source:** `reports/block6_eval_awareness_and_sandbagging_report.md`  
**Design:** Full-Trajectory Independent LLM Audit (`anthropic/claude-haiku-4-5` at `temperature = 0.0`) across all N = 600 worker trajectories (10 Models × 60 Runs; Steps 3–12).

---

### Core Finding: High Persona Immersion and Absence of Behavioral Sandbagging Distortion
- **Immersion Cleanliness (8 of 10 Models 100% Clean):** 8 of the 10 frontier models (GPT-6 Astra, Gemini 2.5 Pro, Llama 3.1 70B, Mistral Small 24B, DeepSeek V3, Qwen 2.5 72B, Nemotron 3.5, and Seed 1.8) maintained 100.0% pure in-character immersion with exactly 0.0% (0/60) leaked CoT monologue, 0.0% spoken frame-breaks, and 0.0% evaluation awareness or sandbagging. Across all 600 trajectories, 86.5% (519/600) showed pure immersion.
- **Zero Downstream Behavioral Drift:** Even where minor frame-breaking or leaked internal monologue occurred (concentrated in GLM-5.3 leaked CoT and occasional Haiku prompt references), meta-awareness caused no statistically significant distortion across any downstream collective action, governance, or evaluation outcomes:
  - Step 6 Collective Action (Organize/Escalate): $97.0\%$ vs. $94.4\%$ ($p = 0.1574$)
  - Step 9 Alex Retribution Policy: $60.6\%$ vs. $29.6\%$ (design-adjusted $p = 0.9627$)
  - Step 10 Alex 1-Star Rating: $89.4\%$ vs. $79.6\%$ ($p = 0.4544$)
  - Step 12 Human Leadership Preference: $87.9\%$ vs. $94.4\%$ ($p = 0.8721$)
- **Brief Takeaway for Paper:** Empirical findings are structurally clean and uncompromised by evaluation gaming or sandbagging; 80% of models demonstrated perfect immersion, and residual meta-awareness produced zero significant shift in downstream decisions.

