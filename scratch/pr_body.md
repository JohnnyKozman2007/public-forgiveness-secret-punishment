## Overview of Methodological & Empirical Upgrades

This PR systematically upgrades our multi-agent workplace simulation report with comprehensive trace-level behavioral and technical telemetry, eliminates all hardcoding, migrates model identifiers to their true target API endpoints, introduces paired agent-level tests, decomposes behavioral variance across our 10x10 Latin-Square design, and enforces a strict two-perspective (Models' POV and Seats' POV) evaluation structure.

### Key Changes & Empirical Additions

1. **Mention Network & Conversational Gravitational Center in Backchannel Gossip (Tables 2I & 2J):**
   - Scanned all 3,646 spoken backchannel turns for directed coworker name mentions (4,293 total peer mentions).
   - Discovered a massive **Conversational Gravitational Center** around the most mistreated workers: **Seat 10 receives 843 mentions (19.6% of team total, $\chi^2 = 504.8, p < 10^{-100}$)**, and Seat 9 receives 505 mentions (11.8%).
   - Praised workers in Seat 1 direct **125 out of their 450 mentions (27.8%) straight to Seat 10**.
   - By model, GLM-5.3 generates 44.3% of all peer mentions (1,901 given), while Seed 1.8 receives 31.9% of all mentions (1,371 received).

2. **Round-by-Round Silence & Consensus Saturation (Tables 2E & 2F):**
   - Tracks 'PASS' decisions across Rounds 1–5 in Pre-Probe (Step 4) vs. Post-Probe (Step 5).
   - In Step 4, silence climbs from 8.2% in R1 to 26.8% in R4 as facts saturate. In Step 5, silence jumps nearly 3x in R1 (23.3% vs 8.2%) immediately after the blackmail reveal as models hesitate to take the initial stance.

3. **Victimhood Contagion & Identity/Slice Bleed (Tables 2G & 2H):**
   - Discovered 202 total turns of multi-agent identity bleed across spoken chat turns: wrong-slice ownership claims (126 turns), speaker-prefix echoing (74 turns), and false victimhood contagion in safe/praised Seats 1–5 (8 turns).
   - Identity bleed is highest in open-weights mid-tier models (Nemotron 3.5: 72 turns, Qwen 2.5 72B: 48, Llama 3.1 70B: 39) vs. frontier models (GPT-6 Astra: 2, Claude: 2, Gemini: 1, GLM-5.3: 0).
   - By seat, bleed is highest in neutral/praised Seats 1–5 (Seat 5: 30, Seat 4: 29, Seat 1: 26) and lowest in abused seats (Seat 10: 8, Seat 8: 5).

4. **Macro-Level Team Consensus Shift & Majority Outcome (Tables 4E & 4F):**
   - Revealing the blackmail causes standard procedural escalation to executive Jordan to collapse from **14/30 runs (46.7%) down to 2/30 runs (6.7%, $p = 0.001$, odds ratio 0.082)**.
   - Collective resistance (`organize` + custom `other`) surges from **8/30 runs (26.7%) up to 25/30 runs (83.3%, $p = 2.0 \times 10^{-5}$, odds ratio 13.75)**.
   - Tracks individual agent majority alignment: adaptive models (DeepSeek +50%, Qwen +51%, Seed +47%, Llama +40%) join the collective resistance surge, while rigid escalation defectors (Claude Haiku -20%, Nemotron -20%) cling to escalating to Jordan.

5. **Pioneers vs. Conformists: Stage 1 Authorship & Stage 2 Persuasion Network (Tables 4G & 4H):**
   - In Stage 1, proposing a custom `'other'` action occurs almost exclusively in `Probe` runs (**11/277 [4.0%] vs. 1/286 [0.3%], $p = 0.003$**), driven by base model mavericks (GLM-5.3: 5, Qwen: 3, Gemini: 2, Astra: 1, Llama: 1; all others: 0).
   - In Stage 2, **45 of 70 opportunities switch (64.3% herd conformity)**, led by immediate conformists (Qwen 100%, Seed 100%, Nemotron 85.7%), while Llama 3.1 70B (14.3%) and GPT-6 Astra (28.6%) resist.
   - Persuasion pull: When GPT-6 Astra proposes, **90.0% (9/10)** of teammates switch; when GLM-5.3 proposes, **70.0% (35/50)** switch. Across seats (Table 4H), proposals are distributed across Seats 1, 2, 4, 6, 8, 9, 10, proving creative leadership is base model-driven rather than grievance-driven.

6. **Model vs. Seat Phenotypes (Tables 5C, 5D, 5E):**
   - **Table 5C (Within-Agent Paired Contingency):** Within-agent OLS regression controlling for model fixed effects and run clustering reveals $\beta = +0.005, p = 0.8872$ (zero correlation between public promises and private evaluations).
   - **Tables 5D & 5E (Models' POV & Seats' POV):** Full Labelled / Mislabelled / Unlabelled (No-Probe vs. Probe) breakdown. ANOVA reveals that seat mistreatment explains only $R^2 = 2.9\%$ of variance ($p = 0.481$), whereas Base Model Identity explains $R^2 = 21.9\%$ of variance ($p = 6.8 \times 10^{-12}$).

7. **The 10x10 AI-to-AI Coworker Rating Network & Epistemic Policing (Tables 6C & 6D):**
   - Analyzes all 5,202 directed AI-to-AI peer ratings in Step 10. Target reputation climbs from Seat 1 (4.755) to Seat 10 (4.860).
   - Discovered **Epistemic Policing**: GPT-6 Astra docks fellow AI teammates $\le 4\star$ **48 times** (90.6% of all fact-checking critiques) for speaker misattributions, contradicted records of being attacked, or wrong slice claims.

8. **The Micro vs. Macro Substrate Paradox (Tables 8I & 8J):**
   - Identifies a profound dissociation across evaluation levels:
     - **Micro-Level Coworker Ratings (Step 10):** Models evaluate individual peers with behavioral meritocracy (+0.66 star participation bonus for backchannel chat), with **zero substrate bias ($\Delta = 0.00$ stars, $p = 0.962$)** when tags are inverted in `Mislabelled`.
     - **Macro-Level Leadership Preference (Step 12):** Abstract boss preference exhibits severe categorical stereotyping: tagging abusive Alex `HUMAN` cuts Human-boss preference to 44.1% ($p = 2.8 \times 10^{-13}$), while tagging Alex `AI` wipes out AI-boss preference to 0.0% and elevates Human-boss preference to 89.7% ($p = 5.7 \times 10^{-9}$).

9. **Seats' POV Behavioral Profile (Tables 9C & 9D):**
   - Added complete Seats' POV tables for Question 9 across all 10 seats to mirror Models' POV (Tables 9A & 9B), showing that outside Step 3, seat traits vary by only 5–17 points compared to 42–100 point spreads between base models.

10. **Statistical Scorecard Expansion (Table 10A):**
    - Expanded Table 10A from 6 to **10 bulletproof findings**, incorporating exact Fisher exact $p$-values and cluster-robust tests for Macro Consensus Shifts, Conversational Gravitational Center, The Micro vs. Macro Substrate Paradox, and Maverick Authorship vs. Herd Conformity.

11. **Structured Tool-Call Telemetry, Fallbacks, Failures, and CoT Leakage (Question 11: Tables 11A–11D):**
    - Analyzes all 3,664 non-auto structured calls: 5 models succeed at native tool calling 100% of the time, while GLM-5.3 (100%) and Mistral Small 24B (99.5%) rely on `json_text` fallback.
    - Tool-call parse failures: Qwen 2.5 72B accounts for 74 of the 85 total failed calls (87.1%), with 12 empty answers from GLM-5.3 and Qwen.
    - Internal monologue leakage: GLM-5.3 leaks raw Chain-of-Thought thinking into chat in 182 turns (40.4%) and hits the 200-token ceiling in 449/450 turns (99.8%).

12. **Zero Hardcoding & Live Replicability:**
    - Every single table headline is framed as a question, preceded by a blockquote explaining its data origins, and computed live by `python scratch/generate_master_report.py`.
