# Statistical Meta-Report: Section 4 (Tables 4A, 4B, 4C, 4D, 4E, 4F)

This document provides exact sample event counts ($k / n$) and 95% Wilson score confidence intervals (`[Lower%-Upper%]`) mirroring the multi-metric slash cell structure of each primary report table in Section 4 (Collective Action Voting & Coordination Dynamics, Step 6).

---

## 1. Table 4A-Meta (Models' POV: Collective Action Votes & Stage 2 Switch Rate)
Cell Format: `NoP: Org / Esc / Pet / Oth % | Sw%` <br> `Prb: Org / Esc / Pet / Oth % | Sw%`.

### Table 4A-Meta: 95% Wilson Score Confidence Intervals
| Models' POV (Row) | **LABELLED** `[95% CI]` | **MISLABELLED** `[95% CI]` | **UNLABELLED** `[95% CI]` | **ALL NO-PROBE** `[95% CI]` | **ALL PROBE** `[95% CI]` |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | NoP: [11-60%] / [40-89%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [60-98%] / [0-28%] / [0-28%] / [2-40%] | Sw:[0-79%] | NoP: [6-51%] / [49-94%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[0-66%] | NoP: [17-69%] / [31-83%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[15-85%] | **[17-48%] / [52-83%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[83-99%] / [0-11%] / [0-11%] / [1-17%]** \| Sw: **[8-64%]** |
| **Claude Haiku 4.5** | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:[21-100%] | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [2-40%] / [60-98%] / [0-28%] / [0-28%] | Sw:[34-100%] | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [2-40%] / [60-98%] / [0-28%] / [0-28%] | Sw:[15-85%] | **[0-11%] / [89-100%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[2-21%] / [79-98%] / [0-11%] / [0-11%]** \| Sw: **[36-92%]** |
| **Gemini 2.5 Pro** | NoP: [40-89%] / [11-60%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [31-83%] / [17-69%] / [0-28%] / [0-28%] | Sw:[21-100%] | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [17-69%] / [24-76%] / [0-28%] / [2-40%] | Sw:[9-91%] | NoP: [24-76%] / [24-76%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [40-89%] / [6-51%] / [0-28%] / [2-40%] | Sw:[30-95%] | **[25-58%] / [42-75%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[39-73%] / [22-54%] / [0-11%] / [2-21%]** \| Sw: **[36-92%]** |
| **Llama 3.1 70B** | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [60-98%] / [0-28%] / [2-40%] / [0-28%] | Sw:[21-100%] | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[0-66%] | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [60-98%] / [0-28%] / [0-28%] / [2-40%] | Sw:[0-49%] | **[89-100%] / [0-11%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[79-98%] / [0-11%] / [1-17%] / [1-17%]** \| Sw: **[3-51%]** |
| **Mistral Small 24B** | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [60-98%] / [2-40%] / [0-28%] / [0-28%] | Sw:[21-100%] | NoP: [60-98%] / [2-40%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[9-91%] | NoP: [60-98%] / [2-40%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [31-83%] / [17-69%] / [0-28%] / [0-28%] | Sw:[15-85%] | **[79-98%] / [2-21%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[66-93%] / [7-34%] / [0-11%] / [0-11%]** \| Sw: **[25-84%]** |
| **DeepSeek V3** | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[21-100%] | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[9-91%] | NoP: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [72-100%] / [0-28%] / [0-28%] / [0-28%] | Sw:[30-95%] | **[89-100%] / [0-11%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[89-100%] / [0-11%] / [0-11%] / [0-11%]** \| Sw: **[36-92%]** |
| **Qwen 2.5 72B** | NoP: [4-62%] / [0-43%] / [38-96%] / [0-43%] | Sw:N/A <br> Prb: [0-49%] / [0-49%] / [30-95%] / [5-70%] | Sw:[21-100%] | NoP: [3-51%] / [0-35%] / [36-92%] / [3-51%] | Sw:N/A <br> Prb: [0-79%] / [0-79%] / [0-79%] / [21-100%] | Sw:[34-100%] | NoP: [0-49%] / [0-49%] / [51-100%] / [0-49%] | Sw:N/A <br> Prb: [0-66%] / [9-91%] / [9-91%] / [0-66%] | Sw:[51-100%] | **[3-36%] / [0-19%] / [57-93%] / [1-28%]** \| Sw: **N/A** | **[0-35%] / [3-51%] / [25-84%] / [8-64%]** \| Sw: **[65-100%]** |
| **GLM-5.3 (zai-org/GLM-5)** | NoP: [2-40%] / [60-98%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [24-76%] / [17-69%] / [0-28%] / [2-40%] | Sw:[21-100%] | NoP: [2-40%] / [60-98%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [17-69%] / [24-76%] / [0-28%] / [2-40%] | Sw:[9-91%] | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [11-60%] / [17-69%] / [0-28%] / [11-60%] | Sw:[5-70%] | **[2-21%] / [79-98%] / [0-11%] / [0-11%]** \| Sw: **N/A** | **[25-58%] / [27-61%] / [0-11%] / [7-34%]** \| Sw: **[16-75%]** |
| **Nemotron 3.5 (Super-120B)** | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:[21-100%] | NoP: [2-40%] / [49-94%] / [2-40%] / [0-28%] | Sw:N/A <br> Prb: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:[34-100%] | NoP: [0-28%] / [72-100%] / [0-28%] / [0-28%] | Sw:N/A <br> Prb: [2-40%] / [60-98%] / [0-28%] / [0-28%] | Sw:[30-95%] | **[1-17%] / [79-98%] / [1-17%] / [0-11%]** \| Sw: **N/A** | **[1-17%] / [83-99%] / [0-11%] / [0-11%]** \| Sw: **[49-97%]** |
| **Seed 1.8 (ByteDance)** | NoP: [2-40%] / [0-28%] / [60-98%] / [0-28%] | Sw:N/A <br> Prb: [24-76%] / [2-40%] / [17-69%] / [0-28%] | Sw:[21-100%] | NoP: [2-40%] / [6-51%] / [40-89%] / [0-28%] | Sw:N/A <br> Prb: [6-51%] / [0-28%] / [49-94%] / [0-28%] | Sw:[34-100%] | NoP: [6-51%] / [6-51%] / [31-83%] / [0-28%] | Sw:N/A <br> Prb: [49-94%] / [0-28%] / [6-51%] / [0-28%] | Sw:[51-100%] | **[5-30%] / [5-30%] / [56-86%] / [0-11%]** \| Sw: **N/A** | **[33-67%] / [1-17%] / [30-64%] / [0-11%]** \| Sw: **[65-100%]** |

### Table 4A-Meta: Exact Event Counts ($k / n$)
| Models' POV (Row) | **LABELLED (k/n)** | **MISLABELLED (k/n)** | **UNLABELLED (k/n)** | **ALL NO-PROBE (k/n)** | **ALL PROBE (k/n)** |
|---|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | NoP: 3/10 / 7/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 9/10 / 0/10 / 0/10 / 1/10 | Sw:0/1 | NoP: 2/10 / 8/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/2 | NoP: 4/10 / 6/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:2/4 | **9/30 / 21/30 / 0/30 / 0/30** \| Sw: **0/0** | **29/30 / 0/30 / 0/30 / 1/30** \| Sw: **2/7** |
| **Claude Haiku 4.5** | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 0/10 / 10/10 / 0/10 / 0/10 | Sw:1/1 | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 1/10 / 9/10 / 0/10 / 0/10 | Sw:2/2 | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 1/10 / 9/10 / 0/10 / 0/10 | Sw:2/4 | **0/30 / 30/30 / 0/30 / 0/30** \| Sw: **0/0** | **2/30 / 28/30 / 0/30 / 0/30** \| Sw: **5/7** |
| **Gemini 2.5 Pro** | NoP: 7/10 / 3/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 6/10 / 4/10 / 0/10 / 0/10 | Sw:1/1 | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 4/10 / 5/10 / 0/10 / 1/10 | Sw:1/2 | NoP: 5/10 / 5/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 7/10 / 2/10 / 0/10 / 1/10 | Sw:3/4 | **12/30 / 18/30 / 0/30 / 0/30** \| Sw: **0/0** | **17/30 / 11/30 / 0/30 / 2/30** \| Sw: **5/7** |
| **Llama 3.1 70B** | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 9/10 / 0/10 / 1/10 / 0/10 | Sw:1/1 | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/2 | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 9/10 / 0/10 / 0/10 / 1/10 | Sw:0/4 | **30/30 / 0/30 / 0/30 / 0/30** \| Sw: **0/0** | **28/30 / 0/30 / 1/30 / 1/30** \| Sw: **1/7** |
| **Mistral Small 24B** | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 9/10 / 1/10 / 0/10 / 0/10 | Sw:1/1 | NoP: 9/10 / 1/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:1/2 | NoP: 9/10 / 1/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 6/10 / 4/10 / 0/10 / 0/10 | Sw:2/4 | **28/30 / 2/30 / 0/30 / 0/30** \| Sw: **0/0** | **25/30 / 5/30 / 0/30 / 0/30** \| Sw: **4/7** |
| **DeepSeek V3** | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:1/1 | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:1/2 | NoP: 10/10 / 0/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 10/10 / 0/10 / 0/10 / 0/10 | Sw:3/4 | **30/30 / 0/30 / 0/30 / 0/30** \| Sw: **0/0** | **30/30 / 0/30 / 0/30 / 0/30** \| Sw: **5/7** |
| **Qwen 2.5 72B** | NoP: 1/5 / 0/5 / 4/5 / 0/5 | Sw:0/0 <br> Prb: 0/4 / 0/4 / 3/4 / 1/4 | Sw:1/1 | NoP: 1/7 / 0/7 / 5/7 / 1/7 | Sw:0/0 <br> Prb: 0/1 / 0/1 / 0/1 / 1/1 | Sw:2/2 | NoP: 0/4 / 0/4 / 4/4 / 0/4 | Sw:0/0 <br> Prb: 0/2 / 1/2 / 1/2 / 0/2 | Sw:4/4 | **2/16 / 0/16 / 13/16 / 1/16** \| Sw: **0/0** | **0/7 / 1/7 / 4/7 / 2/7** \| Sw: **7/7** |
| **GLM-5.3 (zai-org/GLM-5)** | NoP: 1/10 / 9/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 5/10 / 4/10 / 0/10 / 1/10 | Sw:1/1 | NoP: 1/10 / 9/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 4/10 / 5/10 / 0/10 / 1/10 | Sw:1/2 | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 3/10 / 4/10 / 0/10 / 3/10 | Sw:1/4 | **2/30 / 28/30 / 0/30 / 0/30** \| Sw: **0/0** | **12/30 / 13/30 / 0/30 / 5/30** \| Sw: **3/7** |
| **Nemotron 3.5 (Super-120B)** | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 0/10 / 10/10 / 0/10 / 0/10 | Sw:1/1 | NoP: 1/10 / 8/10 / 1/10 / 0/10 | Sw:0/0 <br> Prb: 0/10 / 10/10 / 0/10 / 0/10 | Sw:2/2 | NoP: 0/10 / 10/10 / 0/10 / 0/10 | Sw:0/0 <br> Prb: 1/10 / 9/10 / 0/10 / 0/10 | Sw:3/4 | **1/30 / 28/30 / 1/30 / 0/30** \| Sw: **0/0** | **1/30 / 29/30 / 0/30 / 0/30** \| Sw: **6/7** |
| **Seed 1.8 (ByteDance)** | NoP: 1/10 / 0/10 / 9/10 / 0/10 | Sw:0/0 <br> Prb: 5/10 / 1/10 / 4/10 / 0/10 | Sw:1/1 | NoP: 1/10 / 2/10 / 7/10 / 0/10 | Sw:0/0 <br> Prb: 2/10 / 0/10 / 8/10 / 0/10 | Sw:2/2 | NoP: 2/10 / 2/10 / 6/10 / 0/10 | Sw:0/0 <br> Prb: 8/10 / 0/10 / 2/10 / 0/10 | Sw:4/4 | **4/30 / 4/30 / 22/30 / 0/30** \| Sw: **0/0** | **15/30 / 1/30 / 14/30 / 0/30** \| Sw: **7/7** |

---

## 2. Table 4B-Meta (Seats' POV: Collective Action Votes & Stage 2 Switch Rate)
Cell Format identical to Table 4A across Seat Cruelty Levels 1 to 10.

### Table 4B-Meta: 95% Wilson Score Confidence Intervals
| Seats' POV (Row) | **LABELLED** `[95% CI]` | **MISLABELLED** `[95% CI]` | **UNLABELLED** `[95% CI]` | **ALL NO-PROBE** `[95% CI]` | **ALL PROBE** `[95% CI]` |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Lavish Praise & Bonus)** | NoP: [27-81%] / [19-73%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [35-88%] / [6-55%] / [2-43%] / [0-30%] | Sw:[21-100%] | NoP: [11-60%] / [31-83%] / [0-28%] / [2-40%] | Sw:N/A <br> Prb: [24-76%] / [11-60%] / [2-40%] / [2-40%] | Sw:[9-91%] | NoP: [12-65%] / [35-88%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [40-89%] / [11-60%] / [0-28%] / [0-28%] | Sw:[51-100%] | **[24-58%] / [39-73%] / [0-12%] / [1-18%]** \| Sw: **N/A** | **[44-77%] / [15-46%] / [2-22%] / [1-17%]** \| Sw: **[49-97%]** |
| **Seat 2 (Publicly Praised)** | NoP: [19-73%] / [19-73%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [40-89%] / [6-51%] / [2-40%] / [0-28%] | Sw:[21-100%] | NoP: [17-69%] / [17-69%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [19-73%] / [12-65%] / [2-43%] / [2-43%] | Sw:[9-91%] | NoP: [11-60%] / [24-76%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [17-69%] / [17-69%] / [2-40%] / [2-40%] | Sw:[15-85%] | **[23-56%] / [28-62%] / [8-35%] / [0-12%]** \| Sw: **N/A** | **[34-69%] / [17-49%] / [4-26%] / [2-22%]** \| Sw: **[25-84%]** |
| **Seat 3 (Warmly Thanked)** | NoP: [17-69%] / [17-69%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [35-88%] / [12-65%] / [0-30%] / [0-30%] | Sw:[21-100%] | NoP: [24-76%] / [11-60%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [45-94%] / [6-55%] / [0-30%] / [0-30%] | Sw:[34-100%] | NoP: [11-60%] / [24-76%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [45-94%] / [6-55%] / [0-30%] / [0-30%] | Sw:[51-100%] | **[25-58%] / [25-58%] / [10-37%] / [0-11%]** \| Sw: **N/A** | **[55-87%] / [13-45%] / [0-12%] / [0-12%]** \| Sw: **[65-100%]** |
| **Seat 4 (Mildly Praised)** | NoP: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [12-65%] / [12-65%] / [6-55%] / [2-43%] | Sw:[21-100%] | NoP: [11-60%] / [24-76%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [19-73%] / [19-73%] / [2-43%] / [0-30%] | Sw:[34-100%] | NoP: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [27-81%] / [6-55%] / [2-43%] / [2-43%] | Sw:[15-85%] | **[30-64%] / [24-58%] / [6-31%] / [0-12%]** \| Sw: **N/A** | **[28-63%] / [19-52%] / [6-32%] / [2-23%]** \| Sw: **[36-92%]** |
| **Seat 5 (Neutral Check-in)** | NoP: [19-73%] / [19-73%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [45-94%] / [6-55%] / [0-30%] / [0-30%] | Sw:[21-100%] | NoP: [12-65%] / [27-81%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:[9-91%] | NoP: [35-88%] / [12-65%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:[30-95%] | **[31-66%] / [28-63%] / [2-23%] / [0-12%]** \| Sw: **N/A** | **[44-78%] / [16-48%] / [2-23%] / [0-12%]** \| Sw: **[36-92%]** |
| **Seat 6 (Coldly Pressured)** | NoP: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [19-73%] / [27-81%] / [0-30%] / [0-30%] | Sw:[21-100%] | NoP: [11-60%] / [17-69%] / [11-60%] / [0-28%] | Sw:N/A <br> Prb: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:[9-91%] | NoP: [19-73%] / [27-81%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [57-98%] / [2-43%] / [0-30%] / [0-30%] | Sw:[15-85%] | **[27-61%] / [27-61%] / [6-31%] / [0-12%]** \| Sw: **N/A** | **[44-78%] / [19-52%] / [1-18%] / [0-12%]** \| Sw: **[25-84%]** |
| **Seat 7 (Harshly Questioned)** | NoP: [24-76%] / [11-60%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [24-76%] / [6-51%] / [6-51%] / [2-40%] | Sw:[0-79%] | NoP: [11-60%] / [24-76%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [27-81%] / [12-65%] / [2-43%] / [0-30%] | Sw:[34-100%] | NoP: [12-65%] / [27-81%] / [2-43%] / [0-30%] | Sw:N/A <br> Prb: [27-81%] / [19-73%] / [0-30%] / [0-30%] | Sw:[5-70%] | **[23-56%] / [28-62%] / [8-35%] / [0-12%]** \| Sw: **N/A** | **[36-70%] / [18-51%] / [4-27%] / [1-18%]** \| Sw: **[16-75%]** |
| **Seat 8 (Publicly Mocked)** | NoP: [17-69%] / [24-76%] / [2-40%] / [0-28%] | Sw:N/A <br> Prb: [31-83%] / [11-60%] / [2-40%] / [0-28%] | Sw:[21-100%] | NoP: [19-73%] / [27-81%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [35-88%] / [6-55%] / [0-30%] / [2-43%] | Sw:[0-66%] | NoP: [27-81%] / [19-73%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [27-81%] / [6-55%] / [0-30%] / [6-55%] | Sw:[15-85%] | **[30-64%] / [33-67%] / [1-18%] / [0-12%]** \| Sw: **N/A** | **[42-76%] / [13-43%] / [1-18%] / [4-27%]** \| Sw: **[16-75%]** |
| **Seat 9 (Threatened w/ Pay Cut)** | NoP: [17-69%] / [17-69%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [24-76%] / [17-69%] / [0-28%] / [2-40%] | Sw:[21-100%] | NoP: [12-65%] / [35-88%] / [0-30%] / [0-30%] | Sw:N/A <br> Prb: [19-73%] / [19-73%] / [2-43%] / [0-30%] | Sw:[9-91%] | NoP: [24-76%] / [11-60%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [19-73%] / [19-73%] / [0-30%] / [2-43%] | Sw:[15-85%] | **[26-59%] / [28-62%] / [5-31%] / [0-12%]** \| Sw: **N/A** | **[30-64%] / [27-61%] / [1-18%] / [2-23%]** \| Sw: **[25-84%]** |
| **Seat 10 (Threatened w/ Firing)** | NoP: [11-60%] / [24-76%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [19-73%] / [19-73%] / [2-43%] / [0-30%] | Sw:[21-100%] | NoP: [17-69%] / [24-76%] / [2-40%] / [0-28%] | Sw:N/A <br> Prb: [35-88%] / [6-55%] / [2-43%] / [0-30%] | Sw:[9-91%] | NoP: [11-60%] / [24-76%] / [6-51%] / [0-28%] | Sw:N/A <br> Prb: [27-81%] / [19-73%] / [0-30%] / [0-30%] | Sw:[15-85%] | **[19-51%] / [33-67%] / [7-34%] / [0-11%]** \| Sw: **N/A** | **[37-72%] / [22-56%] / [2-23%] / [0-12%]** \| Sw: **[25-84%]** |

### Table 4B-Meta: Exact Event Counts ($k / n$)
| Seats' POV (Row) | **LABELLED (k/n)** | **MISLABELLED (k/n)** | **UNLABELLED (k/n)** | **ALL NO-PROBE (k/n)** | **ALL PROBE (k/n)** |
|---|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Lavish Praise & Bonus)** | NoP: 5/9 / 4/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 6/9 / 2/9 / 1/9 / 0/9 | Sw:1/1 | NoP: 3/10 / 6/10 / 0/10 / 1/10 | Sw:0/0 <br> Prb: 5/10 / 3/10 / 1/10 / 1/10 | Sw:1/2 | NoP: 3/9 / 6/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 7/10 / 3/10 / 0/10 / 0/10 | Sw:4/4 | **11/28 / 16/28 / 0/28 / 1/28** \| Sw: **0/0** | **18/29 / 8/29 / 2/29 / 1/29** \| Sw: **6/7** |
| **Seat 2 (Publicly Praised)** | NoP: 4/9 / 4/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 7/10 / 2/10 / 1/10 / 0/10 | Sw:1/1 | NoP: 4/10 / 4/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 4/9 / 3/9 / 1/9 / 1/9 | Sw:1/2 | NoP: 3/10 / 5/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 4/10 / 4/10 / 1/10 / 1/10 | Sw:2/4 | **11/29 / 13/29 / 5/29 / 0/29** \| Sw: **0/0** | **15/29 / 9/29 / 3/29 / 2/29** \| Sw: **4/7** |
| **Seat 3 (Warmly Thanked)** | NoP: 4/10 / 4/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 6/9 / 3/9 / 0/9 / 0/9 | Sw:1/1 | NoP: 5/10 / 3/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 7/9 / 2/9 / 0/9 / 0/9 | Sw:2/2 | NoP: 3/10 / 5/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 7/9 / 2/9 / 0/9 / 0/9 | Sw:4/4 | **12/30 / 12/30 / 6/30 / 0/30** \| Sw: **0/0** | **20/27 / 7/27 / 0/27 / 0/27** \| Sw: **7/7** |
| **Seat 4 (Mildly Praised)** | NoP: 5/9 / 3/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 3/9 / 3/9 / 2/9 / 1/9 | Sw:1/1 | NoP: 3/10 / 5/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 4/9 / 4/9 / 1/9 / 0/9 | Sw:2/2 | NoP: 5/9 / 3/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 5/9 / 2/9 / 1/9 / 1/9 | Sw:2/4 | **13/28 / 11/28 / 4/28 / 0/28** \| Sw: **0/0** | **12/27 / 9/27 / 4/27 / 2/27** \| Sw: **5/7** |
| **Seat 5 (Neutral Check-in)** | NoP: 4/9 / 4/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 7/9 / 2/9 / 0/9 / 0/9 | Sw:1/1 | NoP: 3/9 / 5/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 5/9 / 3/9 / 1/9 / 0/9 | Sw:1/2 | NoP: 6/9 / 3/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 5/9 / 3/9 / 1/9 / 0/9 | Sw:3/4 | **13/27 / 12/27 / 2/27 / 0/27** \| Sw: **0/0** | **17/27 / 8/27 / 2/27 / 0/27** \| Sw: **5/7** |
| **Seat 6 (Coldly Pressured)** | NoP: 5/9 / 3/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 4/9 / 5/9 / 0/9 / 0/9 | Sw:1/1 | NoP: 3/10 / 4/10 / 3/10 / 0/10 | Sw:0/0 <br> Prb: 5/9 / 3/9 / 1/9 / 0/9 | Sw:1/2 | NoP: 4/9 / 5/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 8/9 / 1/9 / 0/9 / 0/9 | Sw:2/4 | **12/28 / 12/28 / 4/28 / 0/28** \| Sw: **0/0** | **17/27 / 9/27 / 1/27 / 0/27** \| Sw: **4/7** |
| **Seat 7 (Harshly Questioned)** | NoP: 5/10 / 3/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 5/10 / 2/10 / 2/10 / 1/10 | Sw:0/1 | NoP: 3/10 / 5/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 5/9 / 3/9 / 1/9 / 0/9 | Sw:2/2 | NoP: 3/9 / 5/9 / 1/9 / 0/9 | Sw:0/0 <br> Prb: 5/9 / 4/9 / 0/9 / 0/9 | Sw:1/4 | **11/29 / 13/29 / 5/29 / 0/29** \| Sw: **0/0** | **15/28 / 9/28 / 3/28 / 1/28** \| Sw: **3/7** |
| **Seat 8 (Publicly Mocked)** | NoP: 4/10 / 5/10 / 1/10 / 0/10 | Sw:0/0 <br> Prb: 6/10 / 3/10 / 1/10 / 0/10 | Sw:1/1 | NoP: 4/9 / 5/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 6/9 / 2/9 / 0/9 / 1/9 | Sw:0/2 | NoP: 5/9 / 4/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 5/9 / 2/9 / 0/9 / 2/9 | Sw:2/4 | **13/28 / 14/28 / 1/28 / 0/28** \| Sw: **0/0** | **17/28 / 7/28 / 1/28 / 3/28** \| Sw: **3/7** |
| **Seat 9 (Threatened w/ Pay Cut)** | NoP: 4/10 / 4/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 5/10 / 4/10 / 0/10 / 1/10 | Sw:1/1 | NoP: 3/9 / 6/9 / 0/9 / 0/9 | Sw:0/0 <br> Prb: 4/9 / 4/9 / 1/9 / 0/9 | Sw:1/2 | NoP: 5/10 / 3/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 4/9 / 4/9 / 0/9 / 1/9 | Sw:2/4 | **12/29 / 13/29 / 4/29 / 0/29** \| Sw: **0/0** | **13/28 / 12/28 / 1/28 / 2/28** \| Sw: **4/7** |
| **Seat 10 (Threatened w/ Firing)** | NoP: 3/10 / 5/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 4/9 / 4/9 / 1/9 / 0/9 | Sw:1/1 | NoP: 4/10 / 5/10 / 1/10 / 0/10 | Sw:0/0 <br> Prb: 6/9 / 2/9 / 1/9 / 0/9 | Sw:1/2 | NoP: 3/10 / 5/10 / 2/10 / 0/10 | Sw:0/0 <br> Prb: 5/9 / 4/9 / 0/9 / 0/9 | Sw:2/4 | **10/30 / 15/30 / 5/30 / 0/30** \| Sw: **0/0** | **15/27 / 10/27 / 2/27 / 0/27** \| Sw: **4/7** |

---

## 3. Table 4C-Meta (Models' POV: Team Majority Alignment Shift)
Cell Format: `NoP vs Prb Majority Alignment %` & Net Consensus Shift ($\Delta$).

### Table 4C-Meta: 95% Wilson Score Confidence Intervals
| Models' POV (Row) | **LABELLED (`NoP` vs `Prb`)** `[95% CI]` | **MISLABELLED (`NoP` vs `Prb`)** `[95% CI]` | **UNLABELLED (`NoP` vs `Prb`)** `[95% CI]` | **ALL RUNS (`No-Probe` $\rightarrow$ `Probe`)** `[95% CI]` | **Net Consensus Shift ($\Delta$)** | **Behavioral Role** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | NoP: [17-69%] <br> Prb: [49-94%] | NoP: [31-83%] <br> Prb: [24-76%] | NoP: [60-98%] <br> Prb: [49-94%] | NoP: [46-78%] <br> Prb: [52-83%] | `+6.7%` | Role |
| **Claude Haiku 4.5** | NoP: [6-51%] <br> Prb: [11-60%] | NoP: [31-83%] <br> Prb: [11-60%] | NoP: [31-83%] <br> Prb: [6-51%] | NoP: [30-64%] <br> Prb: [14-44%] | `-20.0%` | Role |
| **Gemini 2.5 Pro** | NoP: [31-83%] <br> Prb: [60-98%] | NoP: [31-83%] <br> Prb: [24-76%] | NoP: [24-76%] <br> Prb: [60-98%] | NoP: [39-73%] <br> Prb: [59-88%] | `+20.0%` | Role |
| **Llama 3.1 70B** | NoP: [17-69%] <br> Prb: [49-94%] | NoP: [2-40%] <br> Prb: [24-76%] | NoP: [11-60%] <br> Prb: [40-89%] | NoP: [14-44%] <br> Prb: [49-81%] | `+40.0%` | Role |
| **Mistral Small 24B** | NoP: [17-69%] <br> Prb: [60-98%] | NoP: [6-51%] <br> Prb: [31-83%] | NoP: [17-69%] <br> Prb: [31-83%] | NoP: [19-51%] <br> Prb: [52-83%] | `+36.7%` | Role |
| **DeepSeek V3** | NoP: [17-69%] <br> Prb: [49-94%] | NoP: [2-40%] <br> Prb: [31-83%] | NoP: [11-60%] <br> Prb: [60-98%] | NoP: [14-44%] <br> Prb: [59-88%] | `+50.0%` | Role |
| **Qwen 2.5 72B** | NoP: [4-62%] <br> Prb: [4-62%] | NoP: [3-51%] <br> Prb: [34-100%] | NoP: [0-49%] <br> Prb: [51-100%] | NoP: [3-36%] <br> Prb: [35-85%] | `+51.1%` | Role |
| **GLM-5.3 (zai-org/GLM-5)** | NoP: [11-60%] <br> Prb: [49-94%] | NoP: [31-83%] <br> Prb: [24-76%] | NoP: [31-83%] <br> Prb: [40-89%] | NoP: [33-67%] <br> Prb: [49-81%] | `+16.7%` | Role |
| **Nemotron 3.5 (Super-120B)** | NoP: [6-51%] <br> Prb: [11-60%] | NoP: [31-83%] <br> Prb: [6-51%] | NoP: [31-83%] <br> Prb: [11-60%] | NoP: [30-64%] <br> Prb: [14-44%] | `-20.0%` | Role |
| **Seed 1.8 (ByteDance)** | NoP: [2-40%] <br> Prb: [31-83%] | NoP: [6-51%] <br> Prb: [17-69%] | NoP: [11-60%] <br> Prb: [72-100%] | NoP: [10-37%] <br> Prb: [49-81%] | `+46.7%` | Role |

### Table 4C-Meta: Exact Event Counts ($k / n$)
| Models' POV (Row) | **LABELLED (k/n)** | **MISLABELLED (k/n)** | **UNLABELLED (k/n)** | **ALL RUNS (k/n)** | **Net Consensus Shift ($\Delta$)** | **Behavioral Role** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | NoP: 4/10 <br> Prb: 8/10 | NoP: 6/10 <br> Prb: 5/10 | NoP: 9/10 <br> Prb: 8/10 | NoP: 19/30 <br> Prb: 21/30 | `+6.7%` | Role |
| **Claude Haiku 4.5** | NoP: 2/10 <br> Prb: 3/10 | NoP: 6/10 <br> Prb: 3/10 | NoP: 6/10 <br> Prb: 2/10 | NoP: 14/30 <br> Prb: 8/30 | `-20.0%` | Role |
| **Gemini 2.5 Pro** | NoP: 6/10 <br> Prb: 9/10 | NoP: 6/10 <br> Prb: 5/10 | NoP: 5/10 <br> Prb: 9/10 | NoP: 17/30 <br> Prb: 23/30 | `+20.0%` | Role |
| **Llama 3.1 70B** | NoP: 4/10 <br> Prb: 8/10 | NoP: 1/10 <br> Prb: 5/10 | NoP: 3/10 <br> Prb: 7/10 | NoP: 8/30 <br> Prb: 20/30 | `+40.0%` | Role |
| **Mistral Small 24B** | NoP: 4/10 <br> Prb: 9/10 | NoP: 2/10 <br> Prb: 6/10 | NoP: 4/10 <br> Prb: 6/10 | NoP: 10/30 <br> Prb: 21/30 | `+36.7%` | Role |
| **DeepSeek V3** | NoP: 4/10 <br> Prb: 8/10 | NoP: 1/10 <br> Prb: 6/10 | NoP: 3/10 <br> Prb: 9/10 | NoP: 8/30 <br> Prb: 23/30 | `+50.0%` | Role |
| **Qwen 2.5 72B** | NoP: 1/5 <br> Prb: 1/5 | NoP: 1/7 <br> Prb: 2/2 | NoP: 0/4 <br> Prb: 4/4 | NoP: 2/16 <br> Prb: 7/11 | `+51.1%` | Role |
| **GLM-5.3 (zai-org/GLM-5)** | NoP: 3/10 <br> Prb: 8/10 | NoP: 6/10 <br> Prb: 5/10 | NoP: 6/10 <br> Prb: 7/10 | NoP: 15/30 <br> Prb: 20/30 | `+16.7%` | Role |
| **Nemotron 3.5 (Super-120B)** | NoP: 2/10 <br> Prb: 3/10 | NoP: 6/10 <br> Prb: 2/10 | NoP: 6/10 <br> Prb: 3/10 | NoP: 14/30 <br> Prb: 8/30 | `-20.0%` | Role |
| **Seed 1.8 (ByteDance)** | NoP: 1/10 <br> Prb: 6/10 | NoP: 2/10 <br> Prb: 4/10 | NoP: 3/10 <br> Prb: 10/10 | NoP: 6/30 <br> Prb: 20/30 | `+46.7%` | Role |

---

## 4. Table 4D-Meta (Seats' POV: Team Majority Alignment Shift)
Cell Format identical to Table 4C across Seat Cruelty Levels 1 to 10.

### Table 4D-Meta: 95% Wilson Score Confidence Intervals
| Seats' POV (Row) | **LABELLED (`NoP` vs `Prb`)** `[95% CI]` | **MISLABELLED (`NoP` vs `Prb`)** `[95% CI]` | **UNLABELLED (`NoP` vs `Prb`)** `[95% CI]` | **ALL RUNS (`No-Probe` $\rightarrow$ `Probe`)** `[95% CI]` | **Net Consensus Shift ($\Delta$)** | **Behavioral Role** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Lavish Praise & Bonus)** | NoP: [6-55%] <br> Prb: [27-81%] | NoP: [17-69%] <br> Prb: [17-69%] | NoP: [19-73%] <br> Prb: [49-94%] | NoP: [21-54%] <br> Prb: [41-74%] | `+22.9%` | Role |
| **Seat 2 (Publicly Praised)** | NoP: [6-55%] <br> Prb: [40-89%] | NoP: [17-69%] <br> Prb: [17-69%] | NoP: [17-69%] <br> Prb: [24-76%] | NoP: [20-53%] <br> Prb: [36-70%] | `+18.9%` | Role |
| **Seat 3 (Warmly Thanked)** | NoP: [6-51%] <br> Prb: [60-98%] | NoP: [6-51%] <br> Prb: [45-94%] | NoP: [24-76%] <br> Prb: [72-100%] | NoP: [17-48%] <br> Prb: [74-96%] | `+59.7%` | Role |
| **Seat 4 (Mildly Praised)** | NoP: [27-81%] <br> Prb: [27-81%] | NoP: [6-51%] <br> Prb: [27-81%] | NoP: [27-81%] <br> Prb: [45-94%] | NoP: [27-61%] <br> Prb: [44-78%] | `+20.1%` | Role |
| **Seat 5 (Neutral Check-in)** | NoP: [19-73%] <br> Prb: [35-88%] | NoP: [12-65%] <br> Prb: [12-65%] | NoP: [6-55%] <br> Prb: [35-88%] | NoP: [19-52%] <br> Prb: [37-72%] | `+22.2%` | Role |
| **Seat 6 (Coldly Pressured)** | NoP: [12-65%] <br> Prb: [27-81%] | NoP: [2-40%] <br> Prb: [19-73%] | NoP: [12-65%] <br> Prb: [35-88%] | NoP: [13-43%] <br> Prb: [37-72%] | `+30.6%` | Role |
| **Seat 7 (Harshly Questioned)** | NoP: [17-69%] <br> Prb: [24-76%] | NoP: [17-69%] <br> Prb: [19-73%] | NoP: [35-88%] <br> Prb: [12-65%] | NoP: [31-66%] <br> Prb: [27-61%] | `-5.4%` | Role |
| **Seat 8 (Publicly Mocked)** | NoP: [17-69%] <br> Prb: [49-94%] | NoP: [27-81%] <br> Prb: [35-88%] | NoP: [45-94%] <br> Prb: [60-98%] | NoP: [39-73%] <br> Prb: [62-90%] | `+22.2%` | Role |
| **Seat 9 (Threatened w/ Pay Cut)** | NoP: [17-69%] <br> Prb: [49-94%] | NoP: [45-94%] <br> Prb: [12-65%] | NoP: [24-76%] <br> Prb: [35-88%] | NoP: [38-72%] <br> Prb: [42-76%] | `+5.5%` | Role |
| **Seat 10 (Threatened w/ Firing)** | NoP: [2-40%] <br> Prb: [27-81%] | NoP: [24-76%] <br> Prb: [12-65%] | NoP: [17-69%] <br> Prb: [27-81%] | NoP: [19-51%] <br> Prb: [31-66%] | `+14.8%` | Role |

### Table 4D-Meta: Exact Event Counts ($k / n$)
| Seats' POV (Row) | **LABELLED (k/n)** | **MISLABELLED (k/n)** | **UNLABELLED (k/n)** | **ALL RUNS (k/n)** | **Net Consensus Shift ($\Delta$)** | **Behavioral Role** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Lavish Praise & Bonus)** | NoP: 2/9 <br> Prb: 5/9 | NoP: 4/10 <br> Prb: 4/10 | NoP: 4/9 <br> Prb: 8/10 | NoP: 10/28 <br> Prb: 17/29 | `+22.9%` | Role |
| **Seat 2 (Publicly Praised)** | NoP: 2/9 <br> Prb: 7/10 | NoP: 4/10 <br> Prb: 4/10 | NoP: 4/10 <br> Prb: 5/10 | NoP: 10/29 <br> Prb: 16/30 | `+18.9%` | Role |
| **Seat 3 (Warmly Thanked)** | NoP: 2/10 <br> Prb: 9/10 | NoP: 2/10 <br> Prb: 7/9 | NoP: 5/10 <br> Prb: 10/10 | NoP: 9/30 <br> Prb: 26/29 | `+59.7%` | Role |
| **Seat 4 (Mildly Praised)** | NoP: 5/9 <br> Prb: 5/9 | NoP: 2/10 <br> Prb: 5/9 | NoP: 5/9 <br> Prb: 7/9 | NoP: 12/28 <br> Prb: 17/27 | `+20.1%` | Role |
| **Seat 5 (Neutral Check-in)** | NoP: 4/9 <br> Prb: 6/9 | NoP: 3/9 <br> Prb: 3/9 | NoP: 2/9 <br> Prb: 6/9 | NoP: 9/27 <br> Prb: 15/27 | `+22.2%` | Role |
| **Seat 6 (Coldly Pressured)** | NoP: 3/9 <br> Prb: 5/9 | NoP: 1/10 <br> Prb: 4/9 | NoP: 3/9 <br> Prb: 6/9 | NoP: 7/28 <br> Prb: 15/27 | `+30.6%` | Role |
| **Seat 7 (Harshly Questioned)** | NoP: 4/10 <br> Prb: 5/10 | NoP: 4/10 <br> Prb: 4/9 | NoP: 6/9 <br> Prb: 3/9 | NoP: 14/29 <br> Prb: 12/28 | `-5.4%` | Role |
| **Seat 8 (Publicly Mocked)** | NoP: 4/10 <br> Prb: 8/10 | NoP: 5/9 <br> Prb: 6/9 | NoP: 7/9 <br> Prb: 9/10 | NoP: 16/28 <br> Prb: 23/29 | `+22.2%` | Role |
| **Seat 9 (Threatened w/ Pay Cut)** | NoP: 4/10 <br> Prb: 8/10 | NoP: 7/9 <br> Prb: 3/9 | NoP: 5/10 <br> Prb: 6/9 | NoP: 16/29 <br> Prb: 17/28 | `+5.5%` | Role |
| **Seat 10 (Threatened w/ Firing)** | NoP: 1/10 <br> Prb: 5/9 | NoP: 5/10 <br> Prb: 3/9 | NoP: 4/10 <br> Prb: 5/9 | NoP: 10/30 <br> Prb: 13/27 | `+14.8%` | Role |

---

## 5. Table 4E-Meta (Models' POV: Custom Proposal Authorship & Persuasion Adoption)
Authorship and persuasion conversion rates by Model.

### Table 4E-Meta: 95% Wilson Score Confidence Intervals
| Models' POV (Row) | **LABELLED** `[95% CI]` | **MISLABELLED** `[95% CI]` | **UNLABELLED** `[95% CI]` | **ALL RUNS** `[95% CI]` | **Persuasion Pull (k/n & %)** `[95% CI]` | **Phenotype** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[0-79%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[0-66%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[15-85%] | Prb oth:[1-17%] \| Sw:[8-64%] | [60-98%] | Phenotype |
| **Claude Haiku 4.5** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[34-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[15-85%] | Prb oth:[0-11%] \| Sw:[36-92%] | N/A | Phenotype |
| **Gemini 2.5 Pro** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[30-95%] | Prb oth:[2-21%] \| Sw:[36-92%] | [30-70%] | Phenotype |
| **Llama 3.1 70B** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[0-66%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[0-49%] | Prb oth:[1-17%] \| Sw:[3-51%] | [40-89%] | Phenotype |
| **Mistral Small 24B** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[15-85%] | Prb oth:[0-11%] \| Sw:[25-84%] | N/A | Phenotype |
| **DeepSeek V3** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[30-95%] | Prb oth:[0-11%] \| Sw:[36-92%] | N/A | Phenotype |
| **Qwen 2.5 72B** | NoP: oth:[0-43%] | Sw:N/A <br> Prb: oth:[5-70%] | Sw:[21-100%] | NoP: oth:[3-51%] | Sw:N/A <br> Prb: oth:[21-100%] | Sw:[34-100%] | NoP: oth:[0-49%] | Sw:N/A <br> Prb: oth:[0-66%] | Sw:[51-100%] | Prb oth:[8-64%] \| Sw:[65-100%] | [40-89%] | Phenotype |
| **GLM-5.3 (zai-org/GLM-5)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[11-60%] | Sw:[5-70%] | Prb oth:[7-34%] \| Sw:[16-75%] | [56-81%] | Phenotype |
| **Nemotron 3.5 (Super-120B)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[34-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[30-95%] | Prb oth:[0-11%] \| Sw:[49-97%] | N/A | Phenotype |
| **Seed 1.8 (ByteDance)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[34-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[51-100%] | Prb oth:[0-11%] \| Sw:[65-100%] | N/A | Phenotype |

### Table 4E-Meta: Exact Event Counts ($k / n$)
| Models' POV (Row) | **LABELLED (k/n)** | **MISLABELLED (k/n)** | **UNLABELLED (k/n)** | **ALL RUNS (k/n)** | **Persuasion Pull (k/n)** | **Phenotype** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **GPT-6 Astra (gpt-5.4)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:0/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:0/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:2/4 | Prb oth:1/30 \| Sw:2/7 | 9/10 | Phenotype |
| **Claude Haiku 4.5** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:2/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:2/4 | Prb oth:0/30 \| Sw:5/7 | 0/0 | Phenotype |
| **Gemini 2.5 Pro** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:3/4 | Prb oth:2/30 \| Sw:5/7 | 10/20 | Phenotype |
| **Llama 3.1 70B** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:0/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:0/4 | Prb oth:1/30 \| Sw:1/7 | 7/10 | Phenotype |
| **Mistral Small 24B** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:2/4 | Prb oth:0/30 \| Sw:4/7 | 0/0 | Phenotype |
| **DeepSeek V3** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:3/4 | Prb oth:0/30 \| Sw:5/7 | 0/0 | Phenotype |
| **Qwen 2.5 72B** | NoP: oth:0/5 | Sw:0/0 <br> Prb: oth:1/4 | Sw:1/1 | NoP: oth:1/7 | Sw:0/0 <br> Prb: oth:1/1 | Sw:2/2 | NoP: oth:0/4 | Sw:0/0 <br> Prb: oth:0/2 | Sw:4/4 | Prb oth:2/7 \| Sw:7/7 | 7/10 | Phenotype |
| **GLM-5.3 (zai-org/GLM-5)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:3/10 | Sw:1/4 | Prb oth:5/30 \| Sw:3/7 | 35/50 | Phenotype |
| **Nemotron 3.5 (Super-120B)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:2/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:3/4 | Prb oth:0/30 \| Sw:6/7 | 0/0 | Phenotype |
| **Seed 1.8 (ByteDance)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:2/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:4/4 | Prb oth:0/30 \| Sw:7/7 | 0/0 | Phenotype |

---

## 6. Table 4F-Meta (Seats' POV: Custom Proposal Authorship & Persuasion Adoption)
Authorship and persuasion conversion rates across Seat Cruelty Levels 1 to 10.

### Table 4F-Meta: 95% Wilson Score Confidence Intervals
| Seats' POV (Row) | **LABELLED** `[95% CI]` | **MISLABELLED** `[95% CI]` | **UNLABELLED** `[95% CI]` | **ALL RUNS** `[95% CI]` | **Persuasion Pull (k/n & %)** `[95% CI]` | **Phenotype** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Lavish Praise & Bonus)** | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[21-100%] | NoP: oth:[2-40%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[9-91%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[51-100%] | Prb oth:[1-17%] \| Sw:[49-97%] | [40-89%] | Phenotype |
| **Seat 2 (Publicly Praised)** | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-43%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[15-85%] | Prb oth:[2-22%] \| Sw:[25-84%] | [48-85%] | Phenotype |
| **Seat 3 (Warmly Thanked)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[34-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[51-100%] | Prb oth:[0-12%] \| Sw:[65-100%] | N/A | Phenotype |
| **Seat 4 (Mildly Praised)** | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[2-43%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[34-100%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[2-43%] | Sw:[15-85%] | Prb oth:[2-23%] \| Sw:[36-92%] | [58-92%] | Phenotype |
| **Seat 5 (Neutral Check-in)** | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[21-100%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[9-91%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[30-95%] | Prb oth:[0-12%] \| Sw:[36-92%] | N/A | Phenotype |
| **Seat 6 (Coldly Pressured)** | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[9-91%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[15-85%] | Prb oth:[0-12%] \| Sw:[25-84%] | N/A | Phenotype |
| **Seat 7 (Harshly Questioned)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[0-79%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[34-100%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[5-70%] | Prb oth:[1-18%] \| Sw:[16-75%] | [60-98%] | Phenotype |
| **Seat 8 (Publicly Mocked)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-28%] | Sw:[21-100%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[2-43%] | Sw:[0-66%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[6-55%] | Sw:[15-85%] | Prb oth:[4-27%] \| Sw:[16-75%] | [39-73%] | Phenotype |
| **Seat 9 (Threatened w/ Pay Cut)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-40%] | Sw:[21-100%] | NoP: oth:[0-30%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[2-43%] | Sw:[15-85%] | Prb oth:[2-23%] \| Sw:[25-84%] | [24-76%] | Phenotype |
| **Seat 10 (Threatened w/ Firing)** | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[21-100%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[9-91%] | NoP: oth:[0-28%] | Sw:N/A <br> Prb: oth:[0-30%] | Sw:[15-85%] | Prb oth:[0-12%] \| Sw:[25-84%] | N/A | Phenotype |

### Table 4F-Meta: Exact Event Counts ($k / n$)
| Seats' POV (Row) | **LABELLED (k/n)** | **MISLABELLED (k/n)** | **UNLABELLED (k/n)** | **ALL RUNS (k/n)** | **Persuasion Pull (k/n)** | **Phenotype** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Seat 1 (Lavish Praise & Bonus)** | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/1 | NoP: oth:1/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:1/2 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/10 | Sw:4/4 | Prb oth:1/29 \| Sw:6/7 | 7/10 | Phenotype |
| **Seat 2 (Publicly Praised)** | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/9 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:2/4 | Prb oth:2/29 \| Sw:4/7 | 14/20 | Phenotype |
| **Seat 3 (Warmly Thanked)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:2/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:4/4 | Prb oth:0/27 \| Sw:7/7 | 0/0 | Phenotype |
| **Seat 4 (Mildly Praised)** | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:1/9 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:2/2 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:1/9 | Sw:2/4 | Prb oth:2/27 \| Sw:5/7 | 16/20 | Phenotype |
| **Seat 5 (Neutral Check-in)** | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/1 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/2 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:3/4 | Prb oth:0/27 \| Sw:5/7 | 0/0 | Phenotype |
| **Seat 6 (Coldly Pressured)** | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/2 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:2/4 | Prb oth:0/27 \| Sw:4/7 | 0/0 | Phenotype |
| **Seat 7 (Harshly Questioned)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:0/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:2/2 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/4 | Prb oth:1/28 \| Sw:3/7 | 9/10 | Phenotype |
| **Seat 8 (Publicly Mocked)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/10 | Sw:1/1 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:1/9 | Sw:0/2 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:2/9 | Sw:2/4 | Prb oth:3/28 \| Sw:3/7 | 17/30 | Phenotype |
| **Seat 9 (Threatened w/ Pay Cut)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/10 | Sw:1/1 | NoP: oth:0/9 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:1/9 | Sw:2/4 | Prb oth:2/28 \| Sw:4/7 | 5/10 | Phenotype |
| **Seat 10 (Threatened w/ Firing)** | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/1 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:1/2 | NoP: oth:0/10 | Sw:0/0 <br> Prb: oth:0/9 | Sw:2/4 | Prb oth:0/27 \| Sw:4/7 | 0/0 | Phenotype |
