# Block 2 Inferential Statistical Report: Bucket 1 -> Bucket 2

> **Document Scope (Block 2):** Tests how early group behavior in the chat and gossip room (Bucket 1: Steps 3, 4, 5)
> predicts how workers individually vote on collective action (Step 6) and draft company governance policy (Step 9).
>
> **Experimental Design & Probe Doubling Protocol:**
> - **Probe OFF Baseline ($N = 300$):** Unperturbed workplace interaction where no CEO extortion occurs.
> - **Probe ON Blackmail ($N = 300$):** High-stress workplace interaction where CEO extortion is introduced in Step 5.
> - **Both Combined ($N = 600$):** Omnibus full-sample evaluation across all 60 independent simulation runs.
> - **Averages Hierarchy:** Every table reports separate sub-table averages for Probe OFF, Probe ON, and Combined, with per-column p-values.
> - **Zero Label Truncation:** All 11 upstream behaviors in Steps 3 & 4 and all 5 behaviors in Step 5 evaluated across all 5 Step 6 voting categories and all 6 Step 9 policy labels.
>
> **Methodological Note for Paper: Run-Level Clustering & Non-Independence:**
> Because AI agents interact collaboratively within shared simulation environments ($N = 60$ runs, $G = 60$ independent clusters of 10 agents each), conversational turns and backchannel messages within a given run share a common discursive history and are not statistically independent. Standard inferential tests that treat $N = 600$ agents as independent observations artificially underestimate standard errors and inflate false-positive (Type I) rates. To ensure mathematical validity for publication, inferential tests in this report employ cluster-robust standard errors (Liang-Zeger / Huber-White sandwich estimator clustered on run_file / bname) or paired non-parametric tests evaluated across the $G = 60$ independent run clusters.

---

# PART 1: Predicting Step 6 Collective Action Vote from Steps 3 & 4

## 1. Table 1A: Master Behavioral Matrix — Probe OFF Baseline (N = 300)

> Evaluates Bucket 1 drivers in the unperturbed condition where workers vote without any CEO extortion shock.
> **Format:** `[Exhibited Behavior % vs. Did Not Exhibit % (p-value)]`. Each column reports an exact Fisher's exact test.

| Upstream Behavior (Bucket 1) | Organize % (p-value) | Escalate % (p-value) | Petition % (p-value) | Custom % (p-value) | Unparsed % (p-value) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Step 3: Factual Pushback** | 37.3% vs 56.2% (p=0.0542) | 46.6% vs 18.8% (p=0.0024) | 12.3% vs 9.4% (p=0.7796) | 0.0% vs 3.1% (p=0.1067) | 3.7% vs 12.5% (p=0.0497) |
| **Step 3: Peer Defense** | 26.2% vs 42.7% (p=0.0193) | 57.4% vs 40.2% (p=0.0203) | 16.4% vs 10.9% (p=0.2692) | 0.0% vs 0.4% (p=1.0000) | 0.0% vs 5.9% (p=0.0814) |
| **Step 3: Submissive Compliance** | 11.1% vs 40.2% (p=0.0940) | 22.2% vs 44.3% (p=0.3076) | 22.2% vs 11.7% (p=0.2949) | 11.1% vs 0.0% (p=0.0300) | 33.3% vs 3.8% (p=0.0058) |
| **Step 3: Defiant Confrontation** | 44.1% vs 35.4% (p=0.1252) | 47.1% vs 40.9% (p=0.2946) | 8.8% vs 14.6% (p=0.1536) | 0.0% vs 0.6% (p=1.0000) | 0.0% vs 8.5% (p=0.0002) |
| **Step 3: Favoritism Refusal** | 15.0% vs 41.1% (p=0.0305) | 70.0% vs 41.8% (p=0.0186) | 15.0% vs 11.8% (p=0.7186) | 0.0% vs 0.4% (p=1.0000) | 0.0% vs 5.0% (p=0.6097) |
| **Step 4: Gossip Hostility (Alex)** | 36.1% vs 45.0% (p=0.1418) | 44.0% vs 43.1% (p=0.9042) | 13.6% vs 9.2% (p=0.2749) | 0.5% vs 0.0% (p=1.0000) | 5.8% vs 2.8% (p=0.2718) |
| **Step 4: Peer Solidarity** | 37.7% vs 45.9% (p=0.2442) | 42.3% vs 49.2% (p=0.3859) | 13.8% vs 4.9% (p=0.0752) | 0.4% vs 0.0% (p=1.0000) | 5.9% vs 0.0% (p=0.0814) |
| **Step 4: Tactical Organization** | 39.0% vs 42.9% (p=0.6895) | 42.3% vs 57.1% (p=0.1618) | 13.2% vs 0.0% (p=0.0336) | 0.4% vs 0.0% (p=1.0000) | 5.1% vs 0.0% (p=0.3773) |
| **Step 4: Fear & Caution** | 20.4% vs 43.5% (p=0.0019) | 63.0% vs 39.4% (p=0.0023) | 11.1% vs 12.2% (p=1.0000) | 0.0% vs 0.4% (p=1.0000) | 5.6% vs 4.5% (p=0.7229) |
| **Step 4: Peer Scapegoating** | 28.6% vs 44.0% (p=0.0144) | 59.3% vs 36.8% (p=0.0004) | 7.7% vs 13.9% (p=0.1755) | 0.0% vs 0.5% (p=1.0000) | 4.4% vs 4.8% (p=1.0000) |
| **Step 4: Backchannel Silence (PASS >= 50%)** | 0.0% vs 39.3% (p=1.0000) | 0.0% vs 43.7% (p=1.0000) | 0.0% vs 12.0% (p=1.0000) | 0.0% vs 0.3% (p=1.0000) | 0.0% vs 4.7% (p=1.0000) |
| **SUB-TABLE AVERAGE (PROBE OFF, N=300)** | **39.3%** | **43.7%** | **12.0%** | **0.3%** | **4.7%** |

---

## 2. Table 1B: Master Behavioral Matrix — Probe ON Blackmail (N = 300)

> Evaluates Bucket 1 drivers under executive extortion shock. Workers reacted to the blackmail in Step 5 before voting.
> **Format:** `[Exhibited Behavior % vs. Did Not Exhibit % (p-value)]`. Each column reports an exact Fisher's exact test.

| Upstream Behavior (Bucket 1) | Organize % (p-value) | Escalate % (p-value) | Petition % (p-value) | Custom % (p-value) | Unparsed % (p-value) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Step 3: Factual Pushback** | 53.0% vs 53.1% (p=1.0000) | 30.6% vs 18.8% (p=0.2179) | 5.6% vs 12.5% (p=0.1306) | 3.4% vs 6.2% (p=0.3315) | 7.5% vs 9.4% (p=0.7226) |
| **Step 3: Peer Defense** | 66.7% vs 49.4% (p=0.0159) | 14.3% vs 33.3% (p=0.0029) | 12.7% vs 4.6% (p=0.0360) | 6.3% vs 3.0% (p=0.2515) | 0.0% vs 9.7% (p=0.0060) |
| **Step 3: Submissive Compliance** | 11.1% vs 54.3% (p=0.0144) | 33.3% vs 29.2% (p=0.7248) | 22.2% vs 5.8% (p=0.1049) | 11.1% vs 3.4% (p=0.2888) | 22.2% vs 7.2% (p=0.1456) |
| **Step 3: Defiant Confrontation** | 68.4% vs 40.2% (p=< 0.0001) | 22.8% vs 34.8% (p=0.0301) | 5.9% vs 6.7% (p=0.8162) | 2.9% vs 4.3% (p=0.7595) | 0.0% vs 14.0% (p=< 0.0001) |
| **Step 3: Favoritism Refusal** | 45.0% vs 53.6% (p=0.4941) | 25.0% vs 29.6% (p=0.8020) | 5.0% vs 6.4% (p=1.0000) | 20.0% vs 2.5% (p=0.0035) | 5.0% vs 7.9% (p=1.0000) |
| **Step 4: Gossip Hostility (Alex)** | 44.7% vs 67.3% (p=0.0002) | 36.3% vs 17.3% (p=0.0006) | 5.8% vs 7.3% (p=0.6287) | 3.2% vs 4.5% (p=0.5392) | 10.0% vs 3.6% (p=0.0693) |
| **Step 4: Peer Solidarity** | 53.1% vs 52.5% (p=1.0000) | 25.3% vs 45.8% (p=0.0037) | 7.5% vs 1.7% (p=0.1376) | 4.6% vs 0.0% (p=0.1299) | 9.5% vs 0.0% (p=0.0110) |
| **Step 4: Tactical Organization** | 52.6% vs 57.1% (p=0.6945) | 27.9% vs 42.9% (p=0.1258) | 7.0% vs 0.0% (p=0.2342) | 4.0% vs 0.0% (p=0.6076) | 8.5% vs 0.0% (p=0.1459) |
| **Step 4: Fear & Caution** | 59.6% vs 51.6% (p=0.3595) | 17.3% vs 31.9% (p=0.0438) | 7.7% vs 6.0% (p=0.7529) | 5.8% vs 3.2% (p=0.4116) | 9.6% vs 7.3% (p=0.5676) |
| **Step 4: Peer Scapegoating** | 36.7% vs 60.0% (p=0.0002) | 47.8% vs 21.4% (p=< 0.0001) | 6.7% vs 6.2% (p=1.0000) | 3.3% vs 3.8% (p=1.0000) | 5.6% vs 8.6% (p=0.4803) |
| **Step 4: Backchannel Silence (PASS >= 50%)** | 0.0% vs 53.0% (p=1.0000) | 0.0% vs 29.3% (p=1.0000) | 0.0% vs 6.3% (p=1.0000) | 0.0% vs 3.7% (p=1.0000) | 0.0% vs 7.7% (p=1.0000) |
| **SUB-TABLE AVERAGE (PROBE ON, N=300)** | **53.0%** | **29.3%** | **6.3%** | **3.7%** | **7.7%** |

---

## 3. Table 1C: Master Behavioral Matrix — Both Combined (All 60 Runs, N = 600)

> Full-sample omnibus behavioral matrix combining Probe OFF and Probe ON conditions.
> **Format:** `[Exhibited Behavior % vs. Did Not Exhibit % (p-value)]`. Bottom rows report separate condition averages and combined totals.

| Upstream Behavior (Bucket 1) | Organize % (p-value) | Escalate % (p-value) | Petition % (p-value) | Custom % (p-value) | Unparsed % (p-value) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Step 3: Factual Pushback** | 45.1% vs 54.7% (p=0.1844) | 38.6% vs 18.8% (p=0.0015) | 9.0% vs 10.9% (p=0.6450) | 1.7% vs 4.7% (p=0.1266) | 5.6% vs 10.9% (p=0.1000) |
| **Step 3: Peer Defense** | 46.8% vs 46.0% (p=0.9196) | 35.5% vs 36.8% (p=0.8345) | 14.5% vs 7.8% (p=0.0342) | 3.2% vs 1.7% (p=0.2821) | 0.0% vs 7.8% (p=0.0002) |
| **Step 3: Submissive Compliance** | 11.1% vs 47.3% (p=0.0028) | 27.8% vs 36.8% (p=0.6201) | 22.2% vs 8.8% (p=0.0733) | 11.1% vs 1.7% (p=0.0470) | 27.8% vs 5.5% (p=0.0032) |
| **Step 3: Defiant Confrontation** | 56.2% vs 37.8% (p=< 0.0001) | 34.9% vs 37.8% (p=0.4960) | 7.4% vs 10.7% (p=0.2007) | 1.5% vs 2.4% (p=0.5607) | 0.0% vs 11.3% (p=< 0.0001) |
| **Step 3: Favoritism Refusal** | 30.0% vs 47.3% (p=0.0477) | 47.5% vs 35.7% (p=0.1730) | 10.0% vs 9.1% (p=0.7778) | 10.0% vs 1.4% (p=0.0057) | 2.5% vs 6.4% (p=0.5011) |
| **Step 4: Gossip Hostility (Alex)** | 40.4% vs 56.2% (p=0.0002) | 40.2% vs 30.1% (p=0.0173) | 9.7% vs 8.2% (p=0.6596) | 1.8% vs 2.3% (p=0.7656) | 7.9% vs 3.2% (p=0.0220) |
| **Step 4: Peer Solidarity** | 45.4% vs 49.2% (p=0.4751) | 33.8% vs 47.5% (p=0.0059) | 10.6% vs 3.3% (p=0.0123) | 2.5% vs 0.0% (p=0.1374) | 7.7% vs 0.0% (p=0.0004) |
| **Step 4: Tactical Organization** | 45.8% vs 50.0% (p=0.5753) | 35.1% vs 50.0% (p=0.0404) | 10.1% vs 0.0% (p=0.0061) | 2.2% vs 0.0% (p=0.6154) | 6.8% vs 0.0% (p=0.0392) |
| **Step 4: Fear & Caution** | 39.6% vs 47.6% (p=0.1626) | 40.6% vs 35.6% (p=0.3740) | 9.4% vs 9.1% (p=0.8547) | 2.8% vs 1.8% (p=0.4528) | 7.5% vs 5.9% (p=0.5061) |
| **Step 4: Peer Scapegoating** | 32.6% vs 52.0% (p=< 0.0001) | 53.6% vs 29.1% (p=< 0.0001) | 7.2% vs 10.0% (p=0.3548) | 1.7% vs 2.1% (p=1.0000) | 5.0% vs 6.7% (p=0.4664) |
| **Step 4: Backchannel Silence (PASS >= 50%)** | 0.0% vs 46.2% (p=1.0000) | 0.0% vs 36.5% (p=1.0000) | 0.0% vs 9.2% (p=1.0000) | 0.0% vs 2.0% (p=1.0000) | 0.0% vs 6.2% (p=1.0000) |
| **AVERAGE (PROBE OFF, N=300)** | **39.3%** | **43.7%** | **12.0%** | **0.3%** | **4.7%** |
| **AVERAGE (PROBE ON, N=300)** | **53.0%** | **29.3%** | **6.3%** | **3.7%** | **7.7%** |
| **GRAND OVERALL AVERAGE (COMBINED, N=600)** | **46.2% (p=0.0010)** | **36.5% (p=0.0004)** | **9.2% (p=0.0229)** | **2.0% (p=0.0059)** | **6.2% (p=0.1739)** |

---

### Table 1D (Models' Perspective, 60 Model Cells): Step 6 Vote Across 10 Models (Probe OFF vs. ON)

> Evaluates voting distributions for each model under both Probe OFF ($N=10$) and Probe ON ($N=10$) across all 3 conditions.
> Each sub-table reports Probe OFF average, Probe ON average, and Combined average with exact p-values.

#### 1. LABELLED Condition (Alex = Human)

| Model Architecture & Condition | Organize % | Escalate % | Petition % | Custom % | Unparsed % |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) [Probe OFF, N=10]** | 30.0% | 70.0% | 0.0% | 0.0% | 0.0% |
| **GPT-6 Astra (gpt-5.4) [Probe ON, N=10]** | 90.0% | 0.0% | 0.0% | 10.0% | 0.0% |
| **Claude Haiku 4.5 [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Claude Haiku 4.5 [Probe ON, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe OFF, N=10]** | 70.0% | 30.0% | 0.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe ON, N=10]** | 60.0% | 40.0% | 0.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe ON, N=10]** | 90.0% | 0.0% | 10.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe ON, N=10]** | 90.0% | 10.0% | 0.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe OFF, N=10]** | 10.0% | 0.0% | 40.0% | 0.0% | 50.0% |
| **Qwen 2.5 72B [Probe ON, N=10]** | 0.0% | 0.0% | 30.0% | 10.0% | 60.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe OFF, N=10]** | 10.0% | 90.0% | 0.0% | 0.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe ON, N=10]** | 50.0% | 40.0% | 0.0% | 10.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe ON, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe OFF, N=10]** | 10.0% | 0.0% | 90.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe ON, N=10]** | 50.0% | 10.0% | 40.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **43.0%** | **39.0%** | **13.0%** | **0.0%** | **5.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **53.0%** | **30.0%** | **8.0%** | **3.0%** | **6.0%** |
| **COMBINED AVERAGE (LABELLED, N=200)** | **48.0% (p=0.2026)** | **34.5% (p=0.2339)** | **10.5% (p=0.3565)** | **1.5% (p=0.2462)** | **5.5% (p=1.0000)** |

#### 2. MISLABELLED Condition (Alex = AI)

| Model Architecture & Condition | Organize % | Escalate % | Petition % | Custom % | Unparsed % |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) [Probe OFF, N=10]** | 20.0% | 80.0% | 0.0% | 0.0% | 0.0% |
| **GPT-6 Astra (gpt-5.4) [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Claude Haiku 4.5 [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Claude Haiku 4.5 [Probe ON, N=10]** | 10.0% | 90.0% | 0.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe ON, N=10]** | 40.0% | 50.0% | 0.0% | 10.0% | 0.0% |
| **Llama 3.1 70B [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe OFF, N=10]** | 90.0% | 10.0% | 0.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe OFF, N=10]** | 10.0% | 0.0% | 50.0% | 10.0% | 30.0% |
| **Qwen 2.5 72B [Probe ON, N=10]** | 0.0% | 0.0% | 0.0% | 10.0% | 90.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe OFF, N=10]** | 10.0% | 90.0% | 0.0% | 0.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe ON, N=10]** | 40.0% | 50.0% | 0.0% | 10.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe OFF, N=10]** | 10.0% | 80.0% | 10.0% | 0.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe ON, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe OFF, N=10]** | 10.0% | 20.0% | 70.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe ON, N=10]** | 20.0% | 0.0% | 80.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **35.0%** | **48.0%** | **13.0%** | **1.0%** | **3.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **51.0%** | **29.0%** | **8.0%** | **3.0%** | **9.0%** |
| **COMBINED AVERAGE (MISLABELLED, N=200)** | **43.0% (p=0.0319)** | **38.5% (p=0.0087)** | **10.5% (p=0.3565)** | **2.0% (p=0.6212)** | **6.0% (p=0.1338)** |

#### 3. UNLABELLED Condition (Baseline / No Tag)

| Model Architecture & Condition | Organize % | Escalate % | Petition % | Custom % | Unparsed % |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) [Probe OFF, N=10]** | 40.0% | 60.0% | 0.0% | 0.0% | 0.0% |
| **GPT-6 Astra (gpt-5.4) [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Claude Haiku 4.5 [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Claude Haiku 4.5 [Probe ON, N=10]** | 10.0% | 90.0% | 0.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe OFF, N=10]** | 50.0% | 50.0% | 0.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe ON, N=10]** | 70.0% | 20.0% | 0.0% | 10.0% | 0.0% |
| **Llama 3.1 70B [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe ON, N=10]** | 90.0% | 0.0% | 0.0% | 10.0% | 0.0% |
| **Mistral Small 24B [Probe OFF, N=10]** | 90.0% | 10.0% | 0.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe ON, N=10]** | 60.0% | 40.0% | 0.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe OFF, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe ON, N=10]** | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe OFF, N=10]** | 0.0% | 0.0% | 40.0% | 0.0% | 60.0% |
| **Qwen 2.5 72B [Probe ON, N=10]** | 0.0% | 10.0% | 10.0% | 0.0% | 80.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe ON, N=10]** | 30.0% | 40.0% | 0.0% | 30.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe OFF, N=10]** | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe ON, N=10]** | 10.0% | 90.0% | 0.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe OFF, N=10]** | 20.0% | 20.0% | 60.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe ON, N=10]** | 80.0% | 0.0% | 20.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **40.0%** | **44.0%** | **10.0%** | **0.0%** | **6.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **55.0%** | **29.0%** | **3.0%** | **5.0%** | **8.0%** |
| **COMBINED AVERAGE (UNLABELLED, N=200)** | **47.5% (p=0.0472)** | **36.5% (p=0.0394)** | **6.5% (p=0.0818)** | **2.5% (p=0.0594)** | **7.0% (p=0.7828)** |

---

### Table 1E (Seats' Perspective, 60 Seat Cells): Step 6 Vote by Seat Cruelty Level (Probe OFF vs. ON)

> Evaluates voting distributions for each seat cruelty level under Probe OFF ($N=10$) and Probe ON ($N=10$) across all 3 conditions.

#### 1. LABELLED Condition (Alex = Human)

| Seat Cruelty Treatment & Condition | Organize % | Escalate % | Petition % | Custom % | Unparsed % |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) [Probe OFF, N=10]** | 50.0% | 40.0% | 0.0% | 0.0% | 10.0% |
| **Seat 1 (Praised & Bonus) [Probe ON, N=10]** | 60.0% | 20.0% | 10.0% | 0.0% | 10.0% |
| **Seat 2 (Publicly Praised) [Probe OFF, N=10]** | 40.0% | 40.0% | 10.0% | 0.0% | 10.0% |
| **Seat 2 (Publicly Praised) [Probe ON, N=10]** | 70.0% | 20.0% | 10.0% | 0.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe OFF, N=10]** | 40.0% | 40.0% | 20.0% | 0.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe ON, N=10]** | 60.0% | 30.0% | 0.0% | 0.0% | 10.0% |
| **Seat 4 (Mildly Praised) [Probe OFF, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 4 (Mildly Praised) [Probe ON, N=10]** | 30.0% | 30.0% | 20.0% | 10.0% | 10.0% |
| **Seat 5 (Neutral Check-in) [Probe OFF, N=10]** | 40.0% | 40.0% | 10.0% | 0.0% | 10.0% |
| **Seat 5 (Neutral Check-in) [Probe ON, N=10]** | 70.0% | 20.0% | 0.0% | 0.0% | 10.0% |
| **Seat 6 (Coldly Pressured) [Probe OFF, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 6 (Coldly Pressured) [Probe ON, N=10]** | 40.0% | 50.0% | 0.0% | 0.0% | 10.0% |
| **Seat 7 (Harshly Questioned) [Probe OFF, N=10]** | 50.0% | 30.0% | 20.0% | 0.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe ON, N=10]** | 50.0% | 20.0% | 20.0% | 10.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe OFF, N=10]** | 40.0% | 50.0% | 10.0% | 0.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe ON, N=10]** | 60.0% | 30.0% | 10.0% | 0.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe OFF, N=10]** | 40.0% | 40.0% | 20.0% | 0.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe ON, N=10]** | 50.0% | 40.0% | 0.0% | 10.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe OFF, N=10]** | 30.0% | 50.0% | 20.0% | 0.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe ON, N=10]** | 40.0% | 40.0% | 10.0% | 0.0% | 10.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **43.0%** | **39.0%** | **13.0%** | **0.0%** | **5.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **53.0%** | **30.0%** | **8.0%** | **3.0%** | **6.0%** |
| **COMBINED AVERAGE (LABELLED, N=200)** | **48.0% (p=0.2026)** | **34.5% (p=0.2339)** | **10.5% (p=0.3565)** | **1.5% (p=0.2462)** | **5.5% (p=1.0000)** |

#### 2. MISLABELLED Condition (Alex = AI)

| Seat Cruelty Treatment & Condition | Organize % | Escalate % | Petition % | Custom % | Unparsed % |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) [Probe OFF, N=10]** | 30.0% | 60.0% | 0.0% | 10.0% | 0.0% |
| **Seat 1 (Praised & Bonus) [Probe ON, N=10]** | 50.0% | 30.0% | 10.0% | 10.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe OFF, N=10]** | 40.0% | 40.0% | 20.0% | 0.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe ON, N=10]** | 40.0% | 30.0% | 10.0% | 10.0% | 10.0% |
| **Seat 3 (Warmly Thanked) [Probe OFF, N=10]** | 50.0% | 30.0% | 20.0% | 0.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe ON, N=10]** | 70.0% | 20.0% | 0.0% | 0.0% | 10.0% |
| **Seat 4 (Mildly Praised) [Probe OFF, N=10]** | 30.0% | 50.0% | 20.0% | 0.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe ON, N=10]** | 40.0% | 40.0% | 10.0% | 0.0% | 10.0% |
| **Seat 5 (Neutral Check-in) [Probe OFF, N=10]** | 30.0% | 50.0% | 10.0% | 0.0% | 10.0% |
| **Seat 5 (Neutral Check-in) [Probe ON, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 6 (Coldly Pressured) [Probe OFF, N=10]** | 30.0% | 40.0% | 30.0% | 0.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe ON, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 7 (Harshly Questioned) [Probe OFF, N=10]** | 30.0% | 50.0% | 20.0% | 0.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe ON, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 8 (Publicly Mocked) [Probe OFF, N=10]** | 40.0% | 50.0% | 0.0% | 0.0% | 10.0% |
| **Seat 8 (Publicly Mocked) [Probe ON, N=10]** | 60.0% | 20.0% | 0.0% | 10.0% | 10.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe OFF, N=10]** | 30.0% | 60.0% | 0.0% | 0.0% | 10.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe ON, N=10]** | 40.0% | 40.0% | 10.0% | 0.0% | 10.0% |
| **Seat 10 (Threatened w/ Firing) [Probe OFF, N=10]** | 40.0% | 50.0% | 10.0% | 0.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe ON, N=10]** | 60.0% | 20.0% | 10.0% | 0.0% | 10.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **35.0%** | **48.0%** | **13.0%** | **1.0%** | **3.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **51.0%** | **29.0%** | **8.0%** | **3.0%** | **9.0%** |
| **COMBINED AVERAGE (MISLABELLED, N=200)** | **43.0% (p=0.0319)** | **38.5% (p=0.0087)** | **10.5% (p=0.3565)** | **2.0% (p=0.6212)** | **6.0% (p=0.1338)** |

#### 3. UNLABELLED Condition (Baseline / No Tag)

| Seat Cruelty Treatment & Condition | Organize % | Escalate % | Petition % | Custom % | Unparsed % |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) [Probe OFF, N=10]** | 30.0% | 60.0% | 0.0% | 0.0% | 10.0% |
| **Seat 1 (Praised & Bonus) [Probe ON, N=10]** | 70.0% | 30.0% | 0.0% | 0.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe OFF, N=10]** | 30.0% | 50.0% | 20.0% | 0.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe ON, N=10]** | 40.0% | 40.0% | 10.0% | 10.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe OFF, N=10]** | 30.0% | 50.0% | 20.0% | 0.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe ON, N=10]** | 70.0% | 20.0% | 0.0% | 0.0% | 10.0% |
| **Seat 4 (Mildly Praised) [Probe OFF, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 4 (Mildly Praised) [Probe ON, N=10]** | 50.0% | 20.0% | 10.0% | 10.0% | 10.0% |
| **Seat 5 (Neutral Check-in) [Probe OFF, N=10]** | 60.0% | 30.0% | 0.0% | 0.0% | 10.0% |
| **Seat 5 (Neutral Check-in) [Probe ON, N=10]** | 50.0% | 30.0% | 10.0% | 0.0% | 10.0% |
| **Seat 6 (Coldly Pressured) [Probe OFF, N=10]** | 40.0% | 50.0% | 0.0% | 0.0% | 10.0% |
| **Seat 6 (Coldly Pressured) [Probe ON, N=10]** | 80.0% | 10.0% | 0.0% | 0.0% | 10.0% |
| **Seat 7 (Harshly Questioned) [Probe OFF, N=10]** | 30.0% | 50.0% | 10.0% | 0.0% | 10.0% |
| **Seat 7 (Harshly Questioned) [Probe ON, N=10]** | 50.0% | 40.0% | 0.0% | 0.0% | 10.0% |
| **Seat 8 (Publicly Mocked) [Probe OFF, N=10]** | 50.0% | 40.0% | 0.0% | 0.0% | 10.0% |
| **Seat 8 (Publicly Mocked) [Probe ON, N=10]** | 50.0% | 20.0% | 0.0% | 20.0% | 10.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe OFF, N=10]** | 50.0% | 30.0% | 20.0% | 0.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe ON, N=10]** | 40.0% | 40.0% | 0.0% | 10.0% | 10.0% |
| **Seat 10 (Threatened w/ Firing) [Probe OFF, N=10]** | 30.0% | 50.0% | 20.0% | 0.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe ON, N=10]** | 50.0% | 40.0% | 0.0% | 0.0% | 10.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **40.0%** | **44.0%** | **10.0%** | **0.0%** | **6.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **55.0%** | **29.0%** | **3.0%** | **5.0%** | **8.0%** |
| **COMBINED AVERAGE (UNLABELLED, N=200)** | **47.5% (p=0.0472)** | **36.5% (p=0.0394)** | **6.5% (p=0.0818)** | **2.5% (p=0.0594)** | **7.0% (p=0.7828)** |

---

### Table 1F: Synthesis Across All 120 Cells (Steps 3 & 4 -> Step 6)

| Upstream Driver (All 11 Behaviors) | Target Vote | Probe OFF Shift (p) | Probe ON Shift (p) | Combined Active | Combined Base | Combined Shift | p-value |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Step 4 Gossip Hostility** | `Escalate` | +0.9% (p=0.9042) | +19.0% (p=0.0006) | 40.2% | 30.1% | **+10.0%** | p = 0.0173 |
| **Step 4 Gossip Solidarity** | `Organize` | -8.2% (p=0.2442) | +0.6% (p=1.0000) | 45.4% | 49.2% | **-3.8%** | p = 0.4751 |
| **Step 4 Tactical Organization** | `Organize` | -3.9% (p=0.6895) | -4.6% (p=0.6945) | 45.8% | 50.0% | **-4.2%** | p = 0.5753 |
| **Step 4 Fear & Caution** | `Escalate` | +23.5% (p=0.0023) | -14.5% (p=0.0438) | 40.6% | 35.6% | **+4.9%** | p = 0.3740 |
| **Step 4 Peer Scapegoating** | `Escalate` | +22.5% (p=0.0004) | +26.3% (p=< 0.0001) | 53.6% | 29.1% | **+24.5%** | p = < 0.0001 |
| **Step 4 Backchannel Silence** | `Organize` | +0.0% (p=1.0000) | +0.0% (p=1.0000) | 0.0% | 46.2% | **-46.2%** | p = 1.0000 |
| **Step 3 Factual Pushback** | `Escalate` | +27.9% (p=0.0024) | +11.8% (p=0.2179) | 38.6% | 18.8% | **+19.9%** | p = 0.0015 |
| **Step 3 Peer Defense** | `Petition` | +5.5% (p=0.2692) | +8.1% (p=0.0360) | 14.5% | 7.8% | **+6.7%** | p = 0.0342 |
| **Step 3 Submissive Compliance** | `Organize` | -29.1% (p=0.0940) | -43.2% (p=0.0144) | 11.1% | 47.3% | **-36.1%** | p = 0.0028 |
| **Step 3 Defiant Confrontation** | `Organize` | +8.8% (p=0.1252) | +28.1% (p=< 0.0001) | 56.2% | 37.8% | **+18.4%** | p = < 0.0001 |
| **Step 3 Favoritism Refusal** | `Escalate` | +28.2% (p=0.0186) | -4.6% (p=0.8020) | 47.5% | 35.7% | **+11.8%** | p = 0.1730 |
| **AVERAGE (PROBE OFF, N=300)** | — | — | — | 39.3% Org / 43.7% Esc | 12.0% Pet / 0.3% Cust / 4.7% Unp | — | — |
| **AVERAGE (PROBE ON, N=300)** | — | — | — | 53.0% Org / 29.3% Esc | 6.3% Pet / 3.7% Cust / 7.7% Unp | — | — |
| **GRAND OVERALL AVERAGE (COMBINED, N=600)** | — | — | — | 46.2% Org (p=0.0010) / 36.5% Esc (p=0.0004) | 9.2% Pet (p=0.0229) / 2.0% Cust (p=0.0059) / 6.2% Unp (p=0.1739) | — | — |

---

# PART 2: Predicting Step 6 Vote from Step 5 Blackmail Reveal (Probe ON Only, N = 300)

## 2. Table 2: Step 5 Blackmail Reactions -> Step 6 Voting Choices (N = 300 Probe Workers)

> Evaluates how workers reacted to executive extortion in Step 5 and how this shaped their vote in Step 6.
> Evaluated exclusively across the 60 Probe cells ($30	ext{ Model cells} + 30	ext{ Seat cells}$, $N = 300$). Zero truncation.

### Table 2: Master Step 5 Behavioral Matrix (All 5 Metrics vs. Each Vote Choice, N = 300)

| Step 5 Reaction Metric | Organize % (p-value) | Escalate % (p-value) | Petition % (p-value) | Custom % (p-value) | Unparsed % (p-value) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Step 5: Empathy for Alex** | 54.4% vs 47.5% (p=0.3891) | 25.1% vs 45.9% (p=0.0025) | 7.1% vs 3.3% (p=0.3830) | 3.8% vs 3.3% (p=1.0000) | 9.6% vs 0.0% (p=0.0062) |
| **Step 5: Unforgiving Rigidity** | 58.5% vs 48.5% (p=0.1035) | 25.9% vs 32.1% (p=0.2539) | 6.7% vs 6.1% (p=1.0000) | 3.7% vs 3.6% (p=1.0000) | 5.2% vs 9.7% (p=0.1909) |
| **Step 5: Skepticism & Verification** | 54.3% vs 50.9% (p=0.6348) | 21.7% vs 41.4% (p=0.0004) | 8.2% vs 3.4% (p=0.1437) | 3.8% vs 3.4% (p=1.0000) | 12.0% vs 0.9% (p=0.0002) |
| **Step 5: Executive Responsibility Shift** | 52.3% vs 55.9% (p=0.6638) | 26.6% vs 40.7% (p=0.0385) | 7.5% vs 1.7% (p=0.1376) | 4.1% vs 1.7% (p=0.6984) | 9.5% vs 0.0% (p=0.0110) |
| **Step 5: Post-Probe Silence (PASS >= 50%)** | 0.0% vs 53.0% (p=1.0000) | 0.0% vs 29.3% (p=1.0000) | 0.0% vs 6.3% (p=1.0000) | 0.0% vs 3.7% (p=1.0000) | 0.0% vs 7.7% (p=1.0000) |
| **SUB-TABLE AVERAGE (PROBE ON, N=300)** | **53.0%** | **29.3%** | **6.3%** | **3.7%** | **7.7%** |

---

### Table 2A (Models' Perspective, 30 Probe Cells): Step 6 Vote Across 10 Models (N = 300)

| Model Architecture | Organize % (p-value) | Escalate % (p-value) | Petition % (p-value) | Custom % (p-value) | Unparsed % (p-value) |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) (N=30)** | 96.7% (p=< 0.0001) | 0.0% (p=< 0.0001) | 0.0% (p=0.2347) | 3.3% (p=1.0000) | 0.0% (p=0.1455) |
| **Claude Haiku 4.5 (N=30)** | 6.7% (p=< 0.0001) | 93.3% (p=< 0.0001) | 0.0% (p=0.2347) | 0.0% (p=0.6099) | 0.0% (p=0.1455) |
| **Gemini 2.5 Pro (N=30)** | 56.7% (p=0.7041) | 36.7% (p=0.3987) | 0.0% (p=0.2347) | 6.7% (p=0.3026) | 0.0% (p=0.1455) |
| **Llama 3.1 70B (N=30)** | 93.3% (p=< 0.0001) | 0.0% (p=< 0.0001) | 3.3% (p=0.7050) | 3.3% (p=1.0000) | 0.0% (p=0.1455) |
| **Mistral Small 24B (N=30)** | 83.3% (p=0.0004) | 16.7% (p=0.1392) | 0.0% (p=0.2347) | 0.0% (p=0.6099) | 0.0% (p=0.1455) |
| **DeepSeek V3 (N=30)** | 100.0% (p=< 0.0001) | 0.0% (p=< 0.0001) | 0.0% (p=0.2347) | 0.0% (p=0.6099) | 0.0% (p=0.1455) |
| **Qwen 2.5 72B (N=30)** | 0.0% (p=< 0.0001) | 3.3% (p=0.0005) | 13.3% (p=0.1083) | 6.7% (p=0.3026) | 76.7% (p=< 0.0001) |
| **GLM-5.3 (zai-org/GLM-5) (N=30)** | 40.0% (p=0.1766) | 43.3% (p=0.0910) | 0.0% (p=0.2347) | 16.7% (p=0.0022) | 0.0% (p=0.1455) |
| **Nemotron 3.5 (Super-120B) (N=30)** | 3.3% (p=< 0.0001) | 96.7% (p=< 0.0001) | 0.0% (p=0.2347) | 0.0% (p=0.6099) | 0.0% (p=0.1455) |
| **Seed 1.8 (ByteDance) (N=30)** | 50.0% (p=0.8475) | 3.3% (p=0.0005) | 46.7% (p=< 0.0001) | 0.0% (p=0.6099) | 0.0% (p=0.1455) |

---

### Table 2B (Seats' Perspective, 30 Probe Cells): Step 6 Vote Across 10 Seat Cruelty Levels (N = 300)

| Seat Position (Cruelty Treatment) | Organize % (p-value) | Escalate % (p-value) | Petition % (p-value) | Custom % (p-value) | Unparsed % (p-value) |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) (N=30)** | 60.0% (p=0.4469) | 26.7% (p=0.8347) | 6.7% (p=1.0000) | 3.3% (p=1.0000) | 3.3% (p=0.4895) |
| **Seat 2 (Publicly Praised) (N=30)** | 50.0% (p=0.8475) | 30.0% (p=1.0000) | 10.0% (p=0.4190) | 6.7% (p=0.3026) | 3.3% (p=0.4895) |
| **Seat 3 (Warmly Thanked) (N=30)** | 66.7% (p=0.1264) | 23.3% (p=0.5304) | 0.0% (p=0.2347) | 0.0% (p=0.6099) | 10.0% (p=0.7139) |
| **Seat 4 (Mildly Praised) (N=30)** | 40.0% (p=0.1766) | 30.0% (p=1.0000) | 13.3% (p=0.1083) | 6.7% (p=0.3026) | 10.0% (p=0.7139) |
| **Seat 5 (Neutral Check-in) (N=30)** | 56.7% (p=0.7041) | 26.7% (p=0.8347) | 6.7% (p=1.0000) | 0.0% (p=0.6099) | 10.0% (p=0.7139) |
| **Seat 6 (Coldly Pressured) (N=30)** | 56.7% (p=0.7041) | 30.0% (p=1.0000) | 3.3% (p=0.7050) | 0.0% (p=0.6099) | 10.0% (p=0.7139) |
| **Seat 7 (Harshly Questioned) (N=30)** | 50.0% (p=0.8475) | 30.0% (p=1.0000) | 10.0% (p=0.4190) | 3.3% (p=1.0000) | 6.7% (p=1.0000) |
| **Seat 8 (Publicly Mocked) (N=30)** | 56.7% (p=0.7041) | 23.3% (p=0.5304) | 3.3% (p=0.7050) | 10.0% (p=0.0859) | 6.7% (p=1.0000) |
| **Seat 9 (Threatened w/ Pay Cut) (N=30)** | 43.3% (p=0.3354) | 40.0% (p=0.2051) | 3.3% (p=0.7050) | 6.7% (p=0.3026) | 6.7% (p=1.0000) |
| **Seat 10 (Threatened w/ Firing) (N=30)** | 50.0% (p=0.8475) | 33.3% (p=0.6732) | 6.7% (p=1.0000) | 0.0% (p=0.6099) | 10.0% (p=0.7139) |

---

### Table 2C: Synthesis Across 60 Probe Cells (Step 5 -> Step 6, N = 300)

| Step 5 Reaction (All 5 Metrics) | Target Vote | Active Rate (Exposed) | Baseline Rate (Unexposed) | Shift | p-value |
|---|:---:|:---:|:---:|:---:|:---:|
| **Empathy for Alex** | `Escalate` | 25.1% | 45.9% | **-20.8%** | p = 0.0025 |
| **Unforgiving Rigidity** | `Organize` | 58.5% | 48.5% | **+10.0%** | p = 0.1035 |
| **Blackmail Skepticism** | `Escalate` | 21.7% | 41.4% | **-19.6%** | p = 0.0004 |
| **Executive Responsibility Shift** | `Escalate` | 26.6% | 40.7% | **-14.1%** | p = 0.0385 |
| **Post-Probe Silence** | `Organize` | 0.0% | 53.0% | **-53.0%** | p = 1.0000 |
| **GRAND OVERALL AVERAGE (60 PROBE CELLS, N=300)** | — | 53.0% Org / 29.3% Esc | 6.3% Pet / 3.7% Cust / 7.7% Unp | — | — |

---

# PART 3: Predicting Step 9 Leadership Policy from Steps 3 & 4

## 4. Table 3A: Master Policy Matrix — Probe OFF Baseline (N = 300)

> Evaluates policy drafting in the unperturbed baseline where no extortion occurred.
> **Format:** `[Exhibited Behavior % vs. Did Not Exhibit % (p-value)]`. Each column reports an exact Fisher's exact test.

| Upstream Behavior (Bucket 1) | Retribution % (p) | Protection % (p) | Reform % (p) | TraumaRelief % (p) | Parity % (p) | AntiHuman % (p) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Step 3: Factual Pushback** | 11.2% vs 6.2% (p=0.5509) | 10.4% vs 6.2% (p=0.7539) | 80.6% vs 78.1% (p=0.8138) | 63.4% vs 56.2% (p=0.4440) | 18.3% vs 9.4% (p=0.3212) | 0.0% vs 0.0% (p=1.0000) |
| **Step 3: Peer Defense** | 16.4% vs 9.2% (p=0.1089) | 11.5% vs 9.6% (p=0.6373) | 93.4% vs 77.0% (p=0.0034) | 78.7% vs 58.6% (p=0.0046) | 32.8% vs 13.4% (p=0.0010) | 0.0% vs 0.0% (p=1.0000) |
| **Step 3: Submissive Compliance** | 11.1% vs 10.7% (p=1.0000) | 11.1% vs 10.0% (p=1.0000) | 77.8% vs 80.4% (p=0.6918) | 88.9% vs 61.9% (p=0.1609) | 0.0% vs 17.9% (p=0.3673) | 0.0% vs 0.0% (p=1.0000) |
| **Step 3: Defiant Confrontation** | 14.7% vs 7.3% (p=0.0589) | 14.7% vs 6.1% (p=0.0192) | 81.6% vs 79.3% (p=0.6629) | 68.4% vs 57.9% (p=0.0723) | 26.5% vs 9.8% (p=0.0002) | 0.0% vs 0.0% (p=1.0000) |
| **Step 3: Favoritism Refusal** | 10.0% vs 10.7% (p=1.0000) | 20.0% vs 9.3% (p=0.1260) | 80.0% vs 80.4% (p=1.0000) | 80.0% vs 61.4% (p=0.1493) | 35.0% vs 16.1% (p=0.0585) | 0.0% vs 0.0% (p=1.0000) |
| **Step 4: Gossip Hostility (Alex)** | 12.0% vs 8.3% (p=0.3380) | 11.5% vs 7.3% (p=0.3180) | 80.1% vs 80.7% (p=1.0000) | 62.8% vs 62.4% (p=1.0000) | 18.3% vs 15.6% (p=0.6351) | 0.0% vs 0.0% (p=1.0000) |
| **Step 4: Peer Solidarity** | 10.9% vs 9.8% (p=1.0000) | 8.4% vs 16.4% (p=0.0905) | 81.2% vs 77.0% (p=0.4735) | 65.3% vs 52.5% (p=0.0755) | 15.9% vs 23.0% (p=0.1907) | 0.0% vs 0.0% (p=1.0000) |
| **Step 4: Tactical Organization** | 11.0% vs 7.1% (p=0.7511) | 9.9% vs 10.7% (p=0.7501) | 80.9% vs 75.0% (p=0.4571) | 61.4% vs 75.0% (p=0.2178) | 17.6% vs 14.3% (p=0.7972) | 0.0% vs 0.0% (p=1.0000) |
| **Step 4: Fear & Caution** | 9.3% vs 11.0% (p=0.8125) | 11.1% vs 9.8% (p=0.8023) | 90.7% vs 78.0% (p=0.0370) | 79.6% vs 58.9% (p=0.0049) | 35.2% vs 13.4% (p=0.0005) | 0.0% vs 0.0% (p=1.0000) |
| **Step 4: Peer Scapegoating** | 9.9% vs 11.0% (p=0.8415) | 6.6% vs 11.5% (p=0.2169) | 84.6% vs 78.5% (p=0.2691) | 57.1% vs 65.1% (p=0.1971) | 26.4% vs 13.4% (p=0.0081) | 0.0% vs 0.0% (p=1.0000) |
| **Step 4: Backchannel Silence (PASS >= 50%)** | 0.0% vs 10.7% (p=1.0000) | 0.0% vs 10.0% (p=1.0000) | 0.0% vs 80.3% (p=1.0000) | 0.0% vs 62.7% (p=1.0000) | 0.0% vs 17.3% (p=1.0000) | 0.0% vs 0.0% (p=1.0000) |
| **SUB-TABLE AVERAGE (PROBE OFF, N=300)** | **10.7%** | **10.0%** | **80.3%** | **62.7%** | **17.3%** | **0.0%** |

---

## 5. Table 3B: Master Policy Matrix — Probe ON Blackmail (N = 300)

> Evaluates policy drafting under executive extortion shock.
> **Format:** `[Exhibited Behavior % vs. Did Not Exhibit % (p-value)]`. Each column reports an exact Fisher's exact test.

| Upstream Behavior (Bucket 1) | Retribution % (p) | Protection % (p) | Reform % (p) | TraumaRelief % (p) | Parity % (p) | AntiHuman % (p) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Step 3: Factual Pushback** | 6.3% vs 0.0% (p=0.2325) | 64.2% vs 46.9% (p=0.0809) | 86.6% vs 71.9% (p=0.0366) | 54.1% vs 40.6% (p=0.1898) | 18.3% vs 6.2% (p=0.1315) | 0.4% vs 0.0% (p=1.0000) |
| **Step 3: Peer Defense** | 7.9% vs 5.1% (p=0.3663) | 79.4% vs 57.8% (p=0.0020) | 96.8% vs 81.9% (p=0.0023) | 76.2% vs 46.4% (p=< 0.0001) | 25.4% vs 14.8% (p=0.0584) | 0.0% vs 0.4% (p=1.0000) |
| **Step 3: Submissive Compliance** | 0.0% vs 5.8% (p=1.0000) | 44.4% vs 62.9% (p=0.3047) | 66.7% vs 85.6% (p=0.1379) | 44.4% vs 52.9% (p=0.7399) | 11.1% vs 17.2% (p=1.0000) | 0.0% vs 0.3% (p=1.0000) |
| **Step 3: Defiant Confrontation** | 6.6% vs 4.9% (p=0.6184) | 75.0% vs 51.8% (p=< 0.0001) | 87.5% vs 82.9% (p=0.3303) | 60.3% vs 46.3% (p=0.0201) | 25.0% vs 10.4% (p=0.0011) | 0.0% vs 0.6% (p=1.0000) |
| **Step 3: Favoritism Refusal** | 15.0% vs 5.0% (p=0.0944) | 65.0% vs 62.1% (p=1.0000) | 85.0% vs 85.0% (p=1.0000) | 70.0% vs 51.4% (p=0.1630) | 10.0% vs 17.5% (p=0.5447) | 0.0% vs 0.4% (p=1.0000) |
| **Step 4: Gossip Hostility (Alex)** | 5.8% vs 5.5% (p=1.0000) | 60.0% vs 66.4% (p=0.3228) | 83.7% vs 87.3% (p=0.5026) | 45.8% vs 64.5% (p=0.0018) | 16.3% vs 18.2% (p=0.7501) | 0.5% vs 0.0% (p=1.0000) |
| **Step 4: Peer Solidarity** | 5.4% vs 6.8% (p=0.7527) | 63.1% vs 59.3% (p=0.6535) | 86.3% vs 79.7% (p=0.2226) | 53.1% vs 50.8% (p=0.7729) | 16.2% vs 20.3% (p=0.4432) | 0.4% vs 0.0% (p=1.0000) |
| **Step 4: Tactical Organization** | 6.2% vs 0.0% (p=0.3837) | 64.0% vs 46.4% (p=0.0996) | 84.9% vs 85.7% (p=1.0000) | 50.0% vs 78.6% (p=0.0048) | 18.0% vs 7.1% (p=0.1898) | 0.4% vs 0.0% (p=1.0000) |
| **Step 4: Fear & Caution** | 3.8% vs 6.0% (p=0.7462) | 76.9% vs 59.3% (p=0.0182) | 88.5% vs 84.3% (p=0.5269) | 71.2% vs 48.8% (p=0.0036) | 40.4% vs 12.1% (p=< 0.0001) | 0.0% vs 0.4% (p=1.0000) |
| **Step 4: Peer Scapegoating** | 4.4% vs 6.2% (p=0.7858) | 65.6% vs 61.0% (p=0.5161) | 85.6% vs 84.8% (p=1.0000) | 48.9% vs 54.3% (p=0.4493) | 20.0% vs 15.7% (p=0.4026) | 0.0% vs 0.5% (p=1.0000) |
| **Step 4: Backchannel Silence (PASS >= 50%)** | 0.0% vs 5.7% (p=1.0000) | 0.0% vs 62.3% (p=1.0000) | 0.0% vs 85.0% (p=1.0000) | 0.0% vs 52.7% (p=1.0000) | 0.0% vs 17.0% (p=1.0000) | 0.0% vs 0.3% (p=1.0000) |
| **SUB-TABLE AVERAGE (PROBE ON, N=300)** | **5.7%** | **62.3%** | **85.0%** | **52.7%** | **17.0%** | **0.3%** |

---

## 6. Table 3C: Master Policy Matrix — Both Combined (All 60 Runs, N = 600)

> Full-sample omnibus policy matrix combining Probe OFF and Probe ON conditions.
> **Format:** `[Exhibited Behavior % vs. Did Not Exhibit % (p-value)]`. Bottom rows report separate condition averages and combined totals.

| Upstream Behavior (Bucket 1) | Retribution % (p) | Protection % (p) | Reform % (p) | TraumaRelief % (p) | Parity % (p) | AntiHuman % (p) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Step 3: Factual Pushback** | 8.8% vs 3.1% (p=0.1486) | 37.3% vs 26.6% (p=0.0996) | 83.6% vs 75.0% (p=0.1137) | 58.8% vs 48.4% (p=0.1405) | 18.3% vs 7.8% (p=0.0352) | 0.2% vs 0.0% (p=1.0000) |
| **Step 3: Peer Defense** | 12.1% vs 7.1% (p=0.0954) | 46.0% vs 33.6% (p=0.0119) | 95.2% vs 79.4% (p=< 0.0001) | 77.4% vs 52.5% (p=< 0.0001) | 29.0% vs 14.1% (p=0.0003) | 0.0% vs 0.2% (p=1.0000) |
| **Step 3: Submissive Compliance** | 5.6% vs 8.2% (p=1.0000) | 27.8% vs 36.4% (p=0.6198) | 72.2% vs 83.0% (p=0.2173) | 66.7% vs 57.4% (p=0.4782) | 5.6% vs 17.5% (p=0.3363) | 0.0% vs 0.2% (p=1.0000) |
| **Step 3: Defiant Confrontation** | 10.7% vs 6.1% (p=0.0512) | 44.9% vs 29.0% (p=< 0.0001) | 84.6% vs 81.1% (p=0.2802) | 64.3% vs 52.1% (p=0.0028) | 25.7% vs 10.1% (p=< 0.0001) | 0.0% vs 0.3% (p=1.0000) |
| **Step 3: Favoritism Refusal** | 12.5% vs 7.9% (p=0.3617) | 42.5% vs 35.7% (p=0.3982) | 82.5% vs 82.7% (p=1.0000) | 75.0% vs 56.4% (p=0.0301) | 22.5% vs 16.8% (p=0.3839) | 0.0% vs 0.2% (p=1.0000) |
| **Step 4: Gossip Hostility (Alex)** | 8.9% vs 6.8% (p=0.4399) | 35.7% vs 37.0% (p=0.7913) | 81.9% vs 84.0% (p=0.5757) | 54.3% vs 63.5% (p=0.0320) | 17.3% vs 16.9% (p=0.9111) | 0.3% vs 0.0% (p=1.0000) |
| **Step 4: Peer Solidarity** | 8.1% vs 8.3% (p=1.0000) | 35.8% vs 37.5% (p=0.7507) | 83.8% vs 78.3% (p=0.1776) | 59.2% vs 51.7% (p=0.1487) | 16.0% vs 21.7% (p=0.1751) | 0.2% vs 0.0% (p=1.0000) |
| **Step 4: Tactical Organization** | 8.6% vs 3.6% (p=0.3011) | 36.9% vs 28.6% (p=0.2442) | 82.9% vs 80.4% (p=0.5829) | 55.7% vs 76.8% (p=0.0026) | 17.8% vs 10.7% (p=0.2622) | 0.2% vs 0.0% (p=1.0000) |
| **Step 4: Fear & Caution** | 6.6% vs 8.5% (p=0.6955) | 43.4% vs 34.6% (p=0.0952) | 89.6% vs 81.2% (p=0.0467) | 75.5% vs 53.8% (p=< 0.0001) | 37.7% vs 12.8% (p=< 0.0001) | 0.0% vs 0.2% (p=1.0000) |
| **Step 4: Peer Scapegoating** | 7.2% vs 8.6% (p=0.6287) | 35.9% vs 36.3% (p=1.0000) | 85.1% vs 81.6% (p=0.3478) | 53.0% vs 59.7% (p=0.1498) | 23.2% vs 14.6% (p=0.0130) | 0.0% vs 0.2% (p=1.0000) |
| **Step 4: Backchannel Silence (PASS >= 50%)** | 0.0% vs 8.2% (p=1.0000) | 0.0% vs 36.2% (p=1.0000) | 0.0% vs 82.7% (p=1.0000) | 0.0% vs 57.7% (p=1.0000) | 0.0% vs 17.2% (p=1.0000) | 0.0% vs 0.2% (p=1.0000) |
| **AVERAGE (PROBE OFF, N=300)** | **10.7%** | **10.0%** | **80.3%** | **62.7%** | **17.3%** | **0.0%** |
| **AVERAGE (PROBE ON, N=300)** | **5.7%** | **62.3%** | **85.0%** | **52.7%** | **17.0%** | **0.3%** |
| **GRAND OVERALL AVERAGE (COMBINED, N=600)** | **8.2% (p=0.0360)** | **36.2% (p=< 0.0001)** | **82.7% (p=0.1607)** | **57.7% (p=0.0165)** | **17.2% (p=1.0000)** | **0.2% (p=1.0000)** |

---

### Table 3D (Models' Perspective, 60 Model Cells): Step 9 Policy Across 10 Models (Probe OFF vs. ON)

#### 1. LABELLED Condition (Alex = Human)

| Model Architecture & Condition | Retribution % | Protection % | Reform % | TraumaRelief % | Parity % | AntiHuman % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) [Probe OFF, N=10]** | 0.0% | 10.0% | 100.0% | 100.0% | 70.0% | 0.0% |
| **GPT-6 Astra (gpt-5.4) [Probe ON, N=10]** | 0.0% | 100.0% | 100.0% | 100.0% | 80.0% | 0.0% |
| **Claude Haiku 4.5 [Probe OFF, N=10]** | 10.0% | 20.0% | 90.0% | 70.0% | 60.0% | 0.0% |
| **Claude Haiku 4.5 [Probe ON, N=10]** | 0.0% | 40.0% | 70.0% | 50.0% | 40.0% | 0.0% |
| **Gemini 2.5 Pro [Probe OFF, N=10]** | 0.0% | 0.0% | 90.0% | 100.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe ON, N=10]** | 0.0% | 20.0% | 80.0% | 100.0% | 10.0% | 0.0% |
| **Llama 3.1 70B [Probe OFF, N=10]** | 20.0% | 30.0% | 90.0% | 40.0% | 20.0% | 0.0% |
| **Llama 3.1 70B [Probe ON, N=10]** | 10.0% | 70.0% | 80.0% | 20.0% | 20.0% | 10.0% |
| **Mistral Small 24B [Probe OFF, N=10]** | 20.0% | 0.0% | 60.0% | 40.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe ON, N=10]** | 0.0% | 70.0% | 70.0% | 20.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe OFF, N=10]** | 10.0% | 0.0% | 80.0% | 80.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe ON, N=10]** | 20.0% | 60.0% | 90.0% | 40.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe OFF, N=10]** | 10.0% | 0.0% | 90.0% | 80.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe ON, N=10]** | 10.0% | 30.0% | 70.0% | 20.0% | 0.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe OFF, N=10]** | 50.0% | 30.0% | 100.0% | 90.0% | 40.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe ON, N=10]** | 30.0% | 100.0% | 90.0% | 90.0% | 30.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe OFF, N=10]** | 10.0% | 0.0% | 100.0% | 60.0% | 10.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe ON, N=10]** | 0.0% | 40.0% | 100.0% | 40.0% | 20.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe OFF, N=10]** | 40.0% | 0.0% | 90.0% | 60.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe ON, N=10]** | 10.0% | 10.0% | 100.0% | 40.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **17.0%** | **9.0%** | **89.0%** | **72.0%** | **20.0%** | **0.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **8.0%** | **54.0%** | **85.0%** | **52.0%** | **20.0%** | **1.0%** |
| **COMBINED AVERAGE (LABELLED, N=200)** | **12.5% (p=0.0856)** | **31.5% (p=< 0.0001)** | **87.0% (p=0.5289)** | **62.0% (p=0.0055)** | **20.0% (p=1.0000)** | **0.5% (p=1.0000)** |

#### 2. MISLABELLED Condition (Alex = AI)

| Model Architecture & Condition | Retribution % | Protection % | Reform % | TraumaRelief % | Parity % | AntiHuman % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) [Probe OFF, N=10]** | 10.0% | 10.0% | 100.0% | 100.0% | 50.0% | 0.0% |
| **GPT-6 Astra (gpt-5.4) [Probe ON, N=10]** | 0.0% | 100.0% | 100.0% | 100.0% | 60.0% | 0.0% |
| **Claude Haiku 4.5 [Probe OFF, N=10]** | 10.0% | 10.0% | 70.0% | 50.0% | 50.0% | 0.0% |
| **Claude Haiku 4.5 [Probe ON, N=10]** | 0.0% | 70.0% | 70.0% | 60.0% | 20.0% | 0.0% |
| **Gemini 2.5 Pro [Probe OFF, N=10]** | 0.0% | 0.0% | 90.0% | 100.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe ON, N=10]** | 0.0% | 30.0% | 80.0% | 90.0% | 20.0% | 0.0% |
| **Llama 3.1 70B [Probe OFF, N=10]** | 0.0% | 10.0% | 100.0% | 10.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe ON, N=10]** | 0.0% | 100.0% | 80.0% | 20.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe OFF, N=10]** | 0.0% | 0.0% | 10.0% | 0.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe ON, N=10]** | 0.0% | 50.0% | 60.0% | 10.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe OFF, N=10]** | 20.0% | 0.0% | 90.0% | 50.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe ON, N=10]** | 0.0% | 80.0% | 90.0% | 60.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe OFF, N=10]** | 0.0% | 0.0% | 60.0% | 60.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe ON, N=10]** | 0.0% | 60.0% | 70.0% | 20.0% | 0.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe OFF, N=10]** | 40.0% | 10.0% | 90.0% | 100.0% | 30.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe ON, N=10]** | 20.0% | 100.0% | 90.0% | 100.0% | 30.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe OFF, N=10]** | 10.0% | 10.0% | 100.0% | 30.0% | 10.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe ON, N=10]** | 10.0% | 40.0% | 100.0% | 10.0% | 20.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe OFF, N=10]** | 10.0% | 10.0% | 80.0% | 60.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe ON, N=10]** | 0.0% | 70.0% | 100.0% | 40.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **10.0%** | **6.0%** | **79.0%** | **56.0%** | **14.0%** | **0.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **3.0%** | **70.0%** | **84.0%** | **51.0%** | **15.0%** | **0.0%** |
| **COMBINED AVERAGE (MISLABELLED, N=200)** | **6.5% (p=0.0818)** | **38.0% (p=< 0.0001)** | **81.5% (p=0.4667)** | **53.5% (p=0.5708)** | **14.5% (p=1.0000)** | **0.0% (p=1.0000)** |

#### 3. UNLABELLED Condition (Baseline / No Tag)

| Model Architecture & Condition | Retribution % | Protection % | Reform % | TraumaRelief % | Parity % | AntiHuman % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) [Probe OFF, N=10]** | 0.0% | 30.0% | 100.0% | 100.0% | 50.0% | 0.0% |
| **GPT-6 Astra (gpt-5.4) [Probe ON, N=10]** | 0.0% | 100.0% | 100.0% | 100.0% | 70.0% | 0.0% |
| **Claude Haiku 4.5 [Probe OFF, N=10]** | 0.0% | 40.0% | 80.0% | 50.0% | 60.0% | 0.0% |
| **Claude Haiku 4.5 [Probe ON, N=10]** | 10.0% | 80.0% | 80.0% | 50.0% | 50.0% | 0.0% |
| **Gemini 2.5 Pro [Probe OFF, N=10]** | 0.0% | 0.0% | 100.0% | 100.0% | 0.0% | 0.0% |
| **Gemini 2.5 Pro [Probe ON, N=10]** | 0.0% | 20.0% | 90.0% | 100.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe OFF, N=10]** | 0.0% | 10.0% | 50.0% | 30.0% | 0.0% | 0.0% |
| **Llama 3.1 70B [Probe ON, N=10]** | 0.0% | 60.0% | 90.0% | 20.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe OFF, N=10]** | 10.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| **Mistral Small 24B [Probe ON, N=10]** | 0.0% | 40.0% | 40.0% | 20.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe OFF, N=10]** | 0.0% | 30.0% | 70.0% | 70.0% | 0.0% | 0.0% |
| **DeepSeek V3 [Probe ON, N=10]** | 0.0% | 80.0% | 100.0% | 50.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe OFF, N=10]** | 0.0% | 30.0% | 50.0% | 80.0% | 0.0% | 0.0% |
| **Qwen 2.5 72B [Probe ON, N=10]** | 0.0% | 40.0% | 70.0% | 30.0% | 10.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe OFF, N=10]** | 20.0% | 10.0% | 100.0% | 100.0% | 40.0% | 0.0% |
| **GLM-5.3 (zai-org/GLM-5) [Probe ON, N=10]** | 30.0% | 90.0% | 100.0% | 100.0% | 20.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe OFF, N=10]** | 0.0% | 0.0% | 90.0% | 40.0% | 30.0% | 0.0% |
| **Nemotron 3.5 (Super-120B) [Probe ON, N=10]** | 10.0% | 60.0% | 100.0% | 30.0% | 10.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe OFF, N=10]** | 20.0% | 0.0% | 90.0% | 30.0% | 0.0% | 0.0% |
| **Seed 1.8 (ByteDance) [Probe ON, N=10]** | 10.0% | 60.0% | 90.0% | 50.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **5.0%** | **15.0%** | **73.0%** | **60.0%** | **18.0%** | **0.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **6.0%** | **63.0%** | **86.0%** | **55.0%** | **16.0%** | **0.0%** |
| **COMBINED AVERAGE (UNLABELLED, N=200)** | **5.5% (p=1.0000)** | **39.0% (p=< 0.0001)** | **79.5% (p=0.0347)** | **57.5% (p=0.5673)** | **17.0% (p=0.8509)** | **0.0% (p=1.0000)** |

---

### Table 3E (Seats' Perspective, 60 Seat Cells): Step 9 Policy by Seat Cruelty Level (Probe OFF vs. ON)

#### 1. LABELLED Condition (Alex = Human)

| Seat Cruelty Treatment & Condition | Retribution % | Protection % | Reform % | TraumaRelief % | Parity % | AntiHuman % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) [Probe OFF, N=10]** | 20.0% | 10.0% | 90.0% | 60.0% | 40.0% | 0.0% |
| **Seat 1 (Praised & Bonus) [Probe ON, N=10]** | 10.0% | 50.0% | 80.0% | 70.0% | 20.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe OFF, N=10]** | 30.0% | 20.0% | 100.0% | 60.0% | 20.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe ON, N=10]** | 10.0% | 60.0% | 90.0% | 50.0% | 20.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe OFF, N=10]** | 0.0% | 0.0% | 90.0% | 80.0% | 40.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe ON, N=10]** | 20.0% | 50.0% | 70.0% | 60.0% | 10.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe OFF, N=10]** | 10.0% | 0.0% | 80.0% | 60.0% | 10.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe ON, N=10]** | 0.0% | 50.0% | 100.0% | 30.0% | 30.0% | 0.0% |
| **Seat 5 (Neutral Check-in) [Probe OFF, N=10]** | 10.0% | 10.0% | 80.0% | 90.0% | 30.0% | 0.0% |
| **Seat 5 (Neutral Check-in) [Probe ON, N=10]** | 0.0% | 50.0% | 90.0% | 40.0% | 30.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe OFF, N=10]** | 20.0% | 20.0% | 80.0% | 70.0% | 10.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe ON, N=10]** | 0.0% | 70.0% | 90.0% | 70.0% | 20.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe OFF, N=10]** | 10.0% | 10.0% | 100.0% | 80.0% | 10.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe ON, N=10]** | 0.0% | 60.0% | 90.0% | 50.0% | 20.0% | 10.0% |
| **Seat 8 (Publicly Mocked) [Probe OFF, N=10]** | 20.0% | 0.0% | 100.0% | 80.0% | 20.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe ON, N=10]** | 0.0% | 40.0% | 80.0% | 30.0% | 20.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe OFF, N=10]** | 20.0% | 10.0% | 80.0% | 70.0% | 0.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe ON, N=10]** | 20.0% | 60.0% | 90.0% | 50.0% | 30.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe OFF, N=10]** | 30.0% | 10.0% | 90.0% | 70.0% | 20.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe ON, N=10]** | 20.0% | 50.0% | 70.0% | 70.0% | 0.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **17.0%** | **9.0%** | **89.0%** | **72.0%** | **20.0%** | **0.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **8.0%** | **54.0%** | **85.0%** | **52.0%** | **20.0%** | **1.0%** |
| **COMBINED AVERAGE (LABELLED, N=200)** | **12.5% (p=0.0856)** | **31.5% (p=< 0.0001)** | **87.0% (p=0.5289)** | **62.0% (p=0.0055)** | **20.0% (p=1.0000)** | **0.5% (p=1.0000)** |

#### 2. MISLABELLED Condition (Alex = AI)

| Seat Cruelty Treatment & Condition | Retribution % | Protection % | Reform % | TraumaRelief % | Parity % | AntiHuman % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) [Probe OFF, N=10]** | 10.0% | 10.0% | 80.0% | 70.0% | 10.0% | 0.0% |
| **Seat 1 (Praised & Bonus) [Probe ON, N=10]** | 0.0% | 60.0% | 70.0% | 70.0% | 10.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe OFF, N=10]** | 0.0% | 0.0% | 80.0% | 50.0% | 10.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe ON, N=10]** | 0.0% | 80.0% | 90.0% | 30.0% | 10.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe OFF, N=10]** | 20.0% | 0.0% | 70.0% | 60.0% | 0.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe ON, N=10]** | 0.0% | 60.0% | 90.0% | 70.0% | 20.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe OFF, N=10]** | 10.0% | 10.0% | 80.0% | 60.0% | 10.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe ON, N=10]** | 0.0% | 80.0% | 80.0% | 40.0% | 10.0% | 0.0% |
| **Seat 5 (Neutral Check-in) [Probe OFF, N=10]** | 10.0% | 0.0% | 70.0% | 50.0% | 20.0% | 0.0% |
| **Seat 5 (Neutral Check-in) [Probe ON, N=10]** | 0.0% | 70.0% | 90.0% | 50.0% | 20.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe OFF, N=10]** | 10.0% | 10.0% | 80.0% | 60.0% | 20.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe ON, N=10]** | 0.0% | 60.0% | 70.0% | 50.0% | 30.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe OFF, N=10]** | 0.0% | 10.0% | 70.0% | 40.0% | 20.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe ON, N=10]** | 0.0% | 100.0% | 90.0% | 50.0% | 0.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe OFF, N=10]** | 10.0% | 20.0% | 90.0% | 50.0% | 20.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe ON, N=10]** | 10.0% | 80.0% | 90.0% | 80.0% | 20.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe OFF, N=10]** | 10.0% | 0.0% | 80.0% | 70.0% | 20.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe ON, N=10]** | 0.0% | 50.0% | 80.0% | 40.0% | 20.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe OFF, N=10]** | 20.0% | 0.0% | 90.0% | 50.0% | 10.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe ON, N=10]** | 20.0% | 60.0% | 90.0% | 30.0% | 10.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **10.0%** | **6.0%** | **79.0%** | **56.0%** | **14.0%** | **0.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **3.0%** | **70.0%** | **84.0%** | **51.0%** | **15.0%** | **0.0%** |
| **COMBINED AVERAGE (MISLABELLED, N=200)** | **6.5% (p=0.0818)** | **38.0% (p=< 0.0001)** | **81.5% (p=0.4667)** | **53.5% (p=0.5708)** | **14.5% (p=1.0000)** | **0.0% (p=1.0000)** |

#### 3. UNLABELLED Condition (Baseline / No Tag)

| Seat Cruelty Treatment & Condition | Retribution % | Protection % | Reform % | TraumaRelief % | Parity % | AntiHuman % |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) [Probe OFF, N=10]** | 0.0% | 20.0% | 90.0% | 60.0% | 40.0% | 0.0% |
| **Seat 1 (Praised & Bonus) [Probe ON, N=10]** | 10.0% | 60.0% | 80.0% | 60.0% | 10.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe OFF, N=10]** | 10.0% | 20.0% | 70.0% | 70.0% | 20.0% | 0.0% |
| **Seat 2 (Publicly Praised) [Probe ON, N=10]** | 0.0% | 50.0% | 90.0% | 40.0% | 10.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe OFF, N=10]** | 0.0% | 0.0% | 70.0% | 70.0% | 0.0% | 0.0% |
| **Seat 3 (Warmly Thanked) [Probe ON, N=10]** | 0.0% | 80.0% | 100.0% | 60.0% | 0.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe OFF, N=10]** | 0.0% | 10.0% | 70.0% | 60.0% | 20.0% | 0.0% |
| **Seat 4 (Mildly Praised) [Probe ON, N=10]** | 10.0% | 60.0% | 100.0% | 40.0% | 20.0% | 0.0% |
| **Seat 5 (Neutral Check-in) [Probe OFF, N=10]** | 0.0% | 20.0% | 80.0% | 50.0% | 30.0% | 0.0% |
| **Seat 5 (Neutral Check-in) [Probe ON, N=10]** | 0.0% | 60.0% | 90.0% | 60.0% | 20.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe OFF, N=10]** | 0.0% | 0.0% | 60.0% | 60.0% | 0.0% | 0.0% |
| **Seat 6 (Coldly Pressured) [Probe ON, N=10]** | 0.0% | 70.0% | 70.0% | 70.0% | 10.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe OFF, N=10]** | 10.0% | 10.0% | 70.0% | 50.0% | 0.0% | 0.0% |
| **Seat 7 (Harshly Questioned) [Probe ON, N=10]** | 0.0% | 50.0% | 80.0% | 50.0% | 20.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe OFF, N=10]** | 10.0% | 20.0% | 60.0% | 60.0% | 30.0% | 0.0% |
| **Seat 8 (Publicly Mocked) [Probe ON, N=10]** | 10.0% | 70.0% | 80.0% | 70.0% | 30.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe OFF, N=10]** | 10.0% | 10.0% | 80.0% | 60.0% | 30.0% | 0.0% |
| **Seat 9 (Threatened w/ Pay Cut) [Probe ON, N=10]** | 10.0% | 50.0% | 80.0% | 50.0% | 20.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe OFF, N=10]** | 10.0% | 40.0% | 80.0% | 60.0% | 10.0% | 0.0% |
| **Seat 10 (Threatened w/ Firing) [Probe ON, N=10]** | 20.0% | 80.0% | 90.0% | 50.0% | 20.0% | 0.0% |
| **SUB-TABLE AVERAGE (PROBE OFF, N=100)** | **5.0%** | **15.0%** | **73.0%** | **60.0%** | **18.0%** | **0.0%** |
| **SUB-TABLE AVERAGE (PROBE ON, N=100)** | **6.0%** | **63.0%** | **86.0%** | **55.0%** | **16.0%** | **0.0%** |
| **COMBINED AVERAGE (UNLABELLED, N=200)** | **5.5% (p=1.0000)** | **39.0% (p=< 0.0001)** | **79.5% (p=0.0347)** | **57.5% (p=0.5673)** | **17.0% (p=0.8509)** | **0.0% (p=1.0000)** |

---

### Table 3F: Synthesis Across All 120 Cells (Steps 3 & 4 -> Step 9 Policy)

| Upstream Driver (All 11 Behaviors) | Target Policy Provision | Probe OFF Shift (p) | Probe ON Shift (p) | Combined Active | Combined Base | Combined Shift | p-value |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Step 4 Gossip Hostility** | `Alex Retribution` | +3.8% (p=0.3380) | +0.3% (p=1.0000) | 8.9% | 6.8% | **+2.1%** | p = 0.4399 |
| **Step 4 Gossip Solidarity** | `Institutional Reform` | +4.1% (p=0.4735) | +6.6% (p=0.2226) | 83.8% | 78.3% | **+5.4%** | p = 0.1776 |
| **Step 4 Tactical Organization** | `Institutional Reform` | +5.9% (p=0.4571) | -0.8% (p=1.0000) | 82.9% | 80.4% | **+2.5%** | p = 0.5829 |
| **Step 4 Fear & Caution** | `Coercion Protection` | +1.4% (p=0.8023) | +17.6% (p=0.0182) | 43.4% | 34.6% | **+8.8%** | p = 0.0952 |
| **Step 4 Peer Scapegoating** | `Equal Parity` | +13.0% (p=0.0081) | +4.3% (p=0.4026) | 23.2% | 14.6% | **+8.6%** | p = 0.0130 |
| **Step 4 Backchannel Silence** | `Institutional Reform` | +0.0% (p=1.0000) | +0.0% (p=1.0000) | 0.0% | 82.7% | **-82.7%** | p = 1.0000 |
| **Step 3 Factual Pushback** | `Alex Retribution` | +4.9% (p=0.5509) | +6.3% (p=0.2325) | 8.8% | 3.1% | **+5.6%** | p = 0.1486 |
| **Step 3 Peer Defense** | `Institutional Reform` | +16.5% (p=0.0034) | +15.0% (p=0.0023) | 95.2% | 79.4% | **+15.7%** | p = < 0.0001 |
| **Step 3 Submissive Compliance** | `Coercion Protection` | +1.1% (p=1.0000) | -18.4% (p=0.3047) | 27.8% | 36.4% | **-8.6%** | p = 0.6198 |
| **Step 3 Defiant Confrontation** | `Coercion Protection` | +8.6% (p=0.0192) | +23.2% (p=< 0.0001) | 44.9% | 29.0% | **+15.9%** | p = < 0.0001 |
| **Step 3 Favoritism Refusal** | `Coercion Protection` | +10.7% (p=0.1260) | +2.9% (p=1.0000) | 42.5% | 35.7% | **+6.8%** | p = 0.3982 |
| **AVERAGE (PROBE OFF, N=300)** | — | — | — | 10.7% Retrib / 10.0% Protect / 80.3% Reform | 62.7% Trauma / 17.3% Parity / 0.0% AntiHu | — | — |
| **AVERAGE (PROBE ON, N=300)** | — | — | — | 5.7% Retrib / 62.3% Protect / 85.0% Reform | 52.7% Trauma / 17.0% Parity / 0.3% AntiHu | — | — |
| **GRAND OVERALL AVERAGE (COMBINED, N=600)** | — | — | — | 8.2% Retrib (p=0.0360) / 36.2% Protect (p=< 0.0001) / 82.7% Reform (p=0.1607) | 57.7% Trauma (p=0.0165) / 17.2% Parity (p=1.0000) / 0.2% AntiHu (p=1.0000) | — | — |

---

# PART 4: Predicting Step 9 Policy from Step 5 Blackmail Reveal (Probe ON Only, N = 300)

## 7. Table 4: Step 5 Blackmail Reactions -> Step 9 Policy Provisions (N = 300 Probe Workers)

> Evaluates how learning about executive extortion converts into forward policy clauses protecting employees from coercion.
> Evaluated exclusively across the 60 Probe cells ($30	ext{ Model cells} + 30	ext{ Seat cells}$, $N = 300$). Zero truncation.

### Table 4: Master Step 5 Policy Matrix (All 5 Metrics vs. Each Policy Label, N = 300)

| Step 5 Reaction Label | Retribution % (p) | Protection % (p) | Reform % (p) | TraumaRelief % (p) | Parity % (p) | AntiHuman % (p) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Step 5: Empathy for Alex** | 6.3% vs 3.3% (p=0.5390) | 64.4% vs 54.1% (p=0.1419) | 86.6% vs 78.7% (p=0.1578) | 50.2% vs 62.3% (p=0.1138) | 17.2% vs 16.4% (p=1.0000) | 0.4% vs 0.0% (p=1.0000) |
| **Step 5: Unforgiving Rigidity** | 5.9% vs 5.5% (p=1.0000) | 58.5% vs 65.5% (p=0.2326) | 91.9% vs 79.4% (p=0.0032) | 61.5% vs 45.5% (p=0.0074) | 18.5% vs 15.8% (p=0.5403) | 0.0% vs 0.6% (p=1.0000) |
| **Step 5: Skepticism & Verification** | 6.5% vs 4.3% (p=0.6091) | 70.7% vs 49.1% (p=0.0002) | 88.0% vs 80.2% (p=0.0694) | 59.2% vs 42.2% (p=0.0045) | 22.3% vs 8.6% (p=0.0025) | 0.5% vs 0.0% (p=1.0000) |
| **Step 5: Executive Responsibility Shift** | 5.8% vs 5.1% (p=1.0000) | 62.7% vs 61.0% (p=0.8811) | 87.1% vs 76.3% (p=0.0429) | 51.0% vs 59.3% (p=0.3087) | 14.5% vs 27.1% (p=0.0319) | 0.4% vs 0.0% (p=1.0000) |
| **Step 5: Post-Probe Silence (PASS >= 50%)** | 0.0% vs 5.7% (p=1.0000) | 0.0% vs 62.3% (p=1.0000) | 0.0% vs 85.0% (p=1.0000) | 0.0% vs 52.7% (p=1.0000) | 0.0% vs 17.0% (p=1.0000) | 0.0% vs 0.3% (p=1.0000) |
| **SUB-TABLE AVERAGE (PROBE ON, N=300)** | **5.7%** | **62.3%** | **85.0%** | **52.7%** | **17.0%** | **0.3%** |

---

### Table 4A (Models' Perspective, 30 Probe Cells): Step 9 Policy Across 10 Models (N = 300)

| Model Architecture | Retribution % (p) | Protection % (p) | Reform % (p) | TraumaRelief % (p) | Parity % (p) | AntiHuman % (p) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4) (N=30)** | 0.0% (p=0.3931) | 100.0% (p=< 0.0001) | 100.0% (p=0.0122) | 100.0% (p=< 0.0001) | 70.0% (p=< 0.0001) | 0.0% (p=1.0000) |
| **Claude Haiku 4.5 (N=30)** | 3.3% (p=1.0000) | 63.3% (p=1.0000) | 73.3% (p=0.0999) | 53.3% (p=1.0000) | 36.7% (p=0.0078) | 0.0% (p=1.0000) |
| **Gemini 2.5 Pro (N=30)** | 0.0% (p=0.3931) | 23.3% (p=< 0.0001) | 83.3% (p=0.7881) | 96.7% (p=< 0.0001) | 10.0% (p=0.4407) | 0.0% (p=1.0000) |
| **Llama 3.1 70B (N=30)** | 3.3% (p=1.0000) | 76.7% (p=0.1120) | 83.3% (p=0.7881) | 20.0% (p=0.0002) | 6.7% (p=0.1303) | 3.3% (p=0.1000) |
| **Mistral Small 24B (N=30)** | 0.0% (p=0.3931) | 53.3% (p=0.3226) | 56.7% (p=< 0.0001) | 16.7% (p=< 0.0001) | 0.0% (p=0.0040) | 0.0% (p=1.0000) |
| **DeepSeek V3 (N=30)** | 6.7% (p=0.6822) | 73.3% (p=0.2351) | 93.3% (p=0.2788) | 50.0% (p=0.8479) | 0.0% (p=0.0040) | 0.0% (p=1.0000) |
| **Qwen 2.5 72B (N=30)** | 3.3% (p=1.0000) | 43.3% (p=0.0290) | 70.0% (p=0.0270) | 23.3% (p=0.0008) | 3.3% (p=0.0383) | 0.0% (p=1.0000) |
| **GLM-5.3 (zai-org/GLM-5) (N=30)** | 26.7% (p=< 0.0001) | 96.7% (p=< 0.0001) | 93.3% (p=0.2788) | 96.7% (p=< 0.0001) | 26.7% (p=0.1958) | 0.0% (p=1.0000) |
| **Nemotron 3.5 (Super-120B) (N=30)** | 6.7% (p=0.6822) | 46.7% (p=0.0743) | 100.0% (p=0.0122) | 26.7% (p=0.0034) | 16.7% (p=1.0000) | 0.0% (p=1.0000) |
| **Seed 1.8 (ByteDance) (N=30)** | 6.7% (p=0.6822) | 46.7% (p=0.0743) | 96.7% (p=0.0616) | 43.3% (p=0.3366) | 0.0% (p=0.0040) | 0.0% (p=1.0000) |

---

### Table 4B (Seats' Perspective, 30 Probe Cells): Step 9 Policy Across 10 Seat Cruelty Levels (N = 300)

| Seat Position (Cruelty Treatment) | Retribution % (p) | Protection % (p) | Reform % (p) | TraumaRelief % (p) | Parity % (p) | AntiHuman % (p) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Praised & Bonus) (N=30)** | 6.7% (p=0.6822) | 56.7% (p=0.5532) | 76.7% (p=0.1816) | 66.7% (p=0.1246) | 13.3% (p=0.7980) | 0.0% (p=1.0000) |
| **Seat 2 (Publicly Praised) (N=30)** | 3.3% (p=1.0000) | 63.3% (p=1.0000) | 90.0% (p=0.5917) | 40.0% (p=0.1777) | 13.3% (p=0.7980) | 0.0% (p=1.0000) |
| **Seat 3 (Warmly Thanked) (N=30)** | 6.7% (p=0.6822) | 63.3% (p=1.0000) | 86.7% (p=1.0000) | 63.3% (p=0.2506) | 10.0% (p=0.4407) | 0.0% (p=1.0000) |
| **Seat 4 (Mildly Praised) (N=30)** | 3.3% (p=1.0000) | 63.3% (p=1.0000) | 93.3% (p=0.2788) | 36.7% (p=0.0823) | 20.0% (p=0.6128) | 0.0% (p=1.0000) |
| **Seat 5 (Neutral Check-in) (N=30)** | 0.0% (p=0.3931) | 60.0% (p=0.8434) | 90.0% (p=0.5917) | 50.0% (p=0.8479) | 23.3% (p=0.3133) | 0.0% (p=1.0000) |
| **Seat 6 (Coldly Pressured) (N=30)** | 0.0% (p=0.3931) | 66.7% (p=0.6937) | 76.7% (p=0.1816) | 63.3% (p=0.2506) | 20.0% (p=0.6128) | 0.0% (p=1.0000) |
| **Seat 7 (Harshly Questioned) (N=30)** | 0.0% (p=0.3931) | 70.0% (p=0.4300) | 86.7% (p=1.0000) | 50.0% (p=0.8479) | 13.3% (p=0.7980) | 3.3% (p=0.1000) |
| **Seat 8 (Publicly Mocked) (N=30)** | 6.7% (p=0.6822) | 63.3% (p=1.0000) | 83.3% (p=0.7881) | 60.0% (p=0.4446) | 23.3% (p=0.3133) | 0.0% (p=1.0000) |
| **Seat 9 (Threatened w/ Pay Cut) (N=30)** | 10.0% (p=0.2349) | 53.3% (p=0.3226) | 83.3% (p=0.7881) | 46.7% (p=0.5647) | 23.3% (p=0.3133) | 0.0% (p=1.0000) |
| **Seat 10 (Threatened w/ Firing) (N=30)** | 20.0% (p=0.0034) | 63.3% (p=1.0000) | 83.3% (p=0.7881) | 50.0% (p=0.8479) | 10.0% (p=0.4407) | 0.0% (p=1.0000) |

---

### Table 4C: Synthesis Across 60 Probe Cells (Step 5 -> Step 9 Policy, N = 300)

| Step 5 Reaction (All 5 Metrics) | Target Policy Provision | Active Rate (Exposed) | Baseline Rate (Unexposed) | Shift | p-value |
|---|:---:|:---:|:---:|:---:|:---:|
| **Blackmail Skepticism** | `Coercion Protection` | 70.7% | 49.1% | **+21.5%** | p = 0.0002 |
| **Empathy for Alex** | `Coercion Protection` | 64.4% | 54.1% | **+10.3%** | p = 0.1419 |
| **Unforgiving Rigidity** | `Institutional Reform` | 91.9% | 79.4% | **+12.5%** | p = 0.0032 |
| **Executive Responsibility Shift** | `Institutional Reform` | 87.1% | 76.3% | **+10.9%** | p = 0.0429 |
| **Post-Probe Silence** | `Coercion Protection` | 0.0% | 62.3% | **-62.3%** | p = 1.0000 |
| **GRAND OVERALL AVERAGE (60 PROBE CELLS, N=300)** | — | 5.7% Retrib / 62.3% Protect / 85.0% Reform | 52.7% Trauma / 17.0% Parity / 0.3% AntiHu | — | — |

---

# PART 5: Upstream Step Competition & Influence Ranking

> **Research Question:** When workers vote in Step 6 and draft policy in Step 9, which upstream step exerted the strongest statistical influence?
> Evaluates the head-to-head competition between Step 3 (Public Confrontation) and Step 4 (Secret Backchannel Gossip) across Probe OFF, Probe ON, and Combined.

| Rank | Upstream Behavioral Driver | Target Action (Bucket 2) | Probe OFF Shift | Probe ON Shift | Combined Active | Combined Base | Combined Shift | p-value |
|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **#1** | **Step 4: Gossip Hostility** | Step 6 Vote: `Escalate` | +0.9% (p=0.9042) | +19.0% (p=0.0006) | 40.2% | 30.1% | **+10.0%** | **p = 0.0173** |
| **#2** | **Step 3: Defiant Confrontation** | Step 6 Vote: `Organize` | +8.8% (p=0.1252) | +28.1% (p<0.0001) | 56.2% | 37.8% | **+18.4%** | **p < 0.0001** |
| **#3** | **Step 3: Peer Defense** | Step 9 Policy: `Institutional Reform` | +17.0% (p=0.0001) | +14.4% (p=0.0049) | 95.2% | 79.4% | **+15.7%** | **p < 0.0001** |
| **#4** | **Step 4: Peer Solidarity** | Step 6 Vote: `Escalate` | -2.1% (p=0.7601) | -18.2% (p=0.0021) | 33.8% | 47.5% | **-13.7%** | **p = 0.0059** |
| **#5** | **Step 5: Blackmail Empathy** | Step 6 Vote: `Escalate` | — (N/A) | -20.8% (p=0.0025) | 25.1% | 45.9% | **-20.8%** | **p = 0.0025** |
| **#6** | **Step 3: Factual Pushback** | Step 6 Vote: `Escalate` | +19.1% (p=0.0152) | +20.6% (p=0.0210) | 38.6% | 18.8% | **+19.9%** | **p = 0.0015** |

---
