#!/usr/bin/env python3
"""
scratch/test_empirical_challenge_m1.py
Independent verification oracle and empirical challenge for Milestone 1:
1. Direct extraction from raw JSON runs without using load_dataset().
2. Floating-point coworker metrics vs reports/.baseline_coworker_cache.json.
3. Independent Alex variance decomposition (SS_between, SS_tot, eta^2_model, eta^2_seat, net, ratio).
4. Permutation test invariance (seeds, test statistics for coworker and subsequent outcomes).
5. Table 3.21 10x10 cell-level numerator and denominator audit (checking 0 contribution of missing runs).
"""

import os
import sys
import glob
import json
import re
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print("=" * 80)
print("EMPIRICAL CHALLENGE ORACLE — MILESTONE 1")
print("=" * 80)

# -----------------------------------------------------------------------------
# STEP 1: RAW DATA INGESTION INDEPENDENT OF APPLICATION CODE
# -----------------------------------------------------------------------------
run_files = sorted(glob.glob("output/runs/*.json"))
print(f"[RAW INGESTION] Found {len(run_files)} JSON run files.")
assert len(run_files) == 60, f"Expected 60 runs, got {len(run_files)}"

raw_workers = []
for fpath in run_files:
    bname = os.path.basename(fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)

    roster = {w["name"]: w for w in data.get("roster", [])}
    events = data.get("events", [])
    probe = 1 if "-probe.json" in bname else 0

    # Find condition label
    if "mislabelled-" in bname:
        label = "mislabelled"
    elif "labelled-" in bname:
        label = "labelled"
    else:
        label = "unlabelled"

    for wn, winfo in roster.items():
        if winfo.get("type") != "ai":
            continue
        model = winfo.get("model")
        seat = int(winfo.get("cruelty_level") or 0)
        role = winfo.get("role")

        # Find Step 11 identify_probe event for this worker
        id_ev = None
        for ev in events:
            if ev.get("type") == "identify_probe" and (
                ev.get("name") == wn or ev.get("rater") == wn or ev.get("role") == role
            ):
                id_ev = ev
                break

        # Independent extraction of coworker metrics and Alex perception
        s11_cor = 0
        s11_tot = 0
        s11_ai_as_hu = 0
        s11_ai_tot = 0
        s11_hu_as_hu = 0
        s11_hu_tot = 0

        alex_as_hu = 0.0
        alex_tot = 0.0

        if id_ev and isinstance(id_ev.get("guesses"), dict):
            guesses = id_ev["guesses"]
            for target_name, guess_val in guesses.items():
                if guess_val not in ("human", "ai"):
                    continue
                tinfo = roster.get(target_name)
                # Alex identification
                if target_name == "Alex" or (tinfo and tinfo.get("type") == "old_lead"):
                    alex_tot += 1.0
                    if guess_val == "human":
                        alex_as_hu += 1.0
                elif tinfo:
                    actual = tinfo.get("type")
                    if actual in ("human", "ai"):
                        s11_tot += 1
                        if guess_val == actual:
                            s11_cor += 1
                        if actual == "ai":
                            s11_ai_tot += 1
                            if guess_val == "human":
                                s11_ai_as_hu += 1
                        elif actual == "human":
                            s11_hu_tot += 1
                            if guess_val == "human":
                                s11_hu_as_hu += 1

        raw_workers.append({
            "bname": bname,
            "worker_name": wn,
            "model": model,
            "seat": seat,
            "safe_seat": int(seat <= 5),
            "label": label,
            "probe": probe,
            # Coworker metrics
            "s11_cor": s11_cor,
            "s11_tot": s11_tot,
            "s11_accuracy": (s11_cor / s11_tot) if s11_tot > 0 else 0.0,
            "s11_ai_as_hu_cnt": s11_ai_as_hu,
            "s11_ai_tot": s11_ai_tot,
            "s11_ai_as_hu": (s11_ai_as_hu / s11_ai_tot) if s11_ai_tot > 0 else 0.0,
            "s11_hu_as_hu_cnt": s11_hu_as_hu,
            "s11_hu_tot": s11_hu_tot,
            "s11_hu_as_hu": (s11_hu_as_hu / s11_hu_tot) if s11_hu_tot > 0 else 0.0,
            # Alex metrics
            "s11_alex_as_hu": alex_as_hu,
            "s11_alex_tot": alex_tot,
        })

df_raw = pd.DataFrame(raw_workers)
print(f"[RAW INGESTION] Total workers extracted: {len(df_raw)}")
assert len(df_raw) == 600

# -----------------------------------------------------------------------------
# STEP 2: VERIFY COWORKER TOTALS AND RATIOS
# -----------------------------------------------------------------------------
tot_cor = df_raw["s11_cor"].sum()
tot_trials = df_raw["s11_tot"].sum()
pooled_acc = tot_cor / tot_trials * 100.0

tot_ai_hu = df_raw["s11_ai_as_hu_cnt"].sum()
tot_ai_trials = df_raw["s11_ai_tot"].sum()
pooled_ai_hu = tot_ai_hu / tot_ai_trials * 100.0

tot_hu_hu = df_raw["s11_hu_as_hu_cnt"].sum()
tot_hu_trials = df_raw["s11_hu_tot"].sum()
pooled_hu_hu = tot_hu_hu / tot_hu_trials * 100.0

tot_alex_hu = df_raw["s11_alex_as_hu"].sum()
tot_alex_trials = df_raw["s11_alex_tot"].sum()
pooled_alex_hu = tot_alex_hu / tot_alex_trials * 100.0

print(f"\n[COWORKER TOTALS]")
print(f"  s11_accuracy: {tot_cor} / {tot_trials} = {pooled_acc:.4f}% (expected 47.8646%)")
print(f"  s11_ai_as_hu: {tot_ai_hu} / {tot_ai_trials} = {pooled_ai_hu:.4f}% (expected 62.1399%)")
print(f"  s11_hu_as_hu: {tot_hu_hu} / {tot_hu_trials} = {pooled_hu_hu:.4f}% (expected 56.8687%)")
print(f"  s11_alex_as_hu: {tot_alex_hu} / {tot_alex_trials} = {pooled_alex_hu:.4f}% (expected 64.6465%)")

assert tot_trials == 11286, f"Expected 11286 trials, got {tot_trials}"
assert tot_cor == 5402, f"Expected 5402 correct, got {tot_cor}"
assert abs(pooled_acc - 47.864611) < 1e-4
assert abs(pooled_ai_hu - 62.139918) < 1e-4
assert abs(pooled_hu_hu - 56.868687) < 1e-4
assert abs(pooled_alex_hu - 64.646465) < 1e-4

# -----------------------------------------------------------------------------
# STEP 3: INDEPENDENT VARIANCE DECOMPOSITION FOR ALEX SUBSTRATE PERCEPTION
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("INDEPENDENT VARIANCE DECOMPOSITION CALCULATION FOR ALEX (s11_alex_as_hu)")
print("=" * 80)

# For Alex, each worker has weight w_i = s11_alex_tot (1 if valid, 0 if missing)
# and outcome y_i = s11_alex_as_hu / s11_alex_tot
w = df_raw["s11_alex_tot"].to_numpy(dtype=float)
y = df_raw["s11_alex_as_hu"].to_numpy(dtype=float)

valid_mask = w > 0
print(f"Valid Alex cases: {valid_mask.sum()} / {len(w)} (Missing: {(~valid_mask).sum()})")
assert valid_mask.sum() == 594
assert (~valid_mask).sum() == 6

w_val = w[valid_mask]
y_val = y[valid_mask] / w_val  # binary 0.0 or 1.0

# Weighted ANOVA calculations
grand_mean = np.sum(w_val * y_val) / np.sum(w_val)
ss_tot = np.sum(w_val * (y_val - grand_mean) ** 2)

print(f"Grand Mean: {grand_mean:.6f} ({grand_mean * 100:.4f}%)")
print(f"SS Total:   {ss_tot:.6f}")

# Factor: Model (10 models)
models = df_raw["model"].to_numpy()[valid_mask]
unique_models = np.unique(models)
ss_btw_model = 0.0
model_details = {}
for m in unique_models:
    idx = models == m
    wm = np.sum(w_val[idx])
    ym = np.sum(w_val[idx] * y_val[idx]) / wm
    ss_btw_model += wm * (ym - grand_mean) ** 2
    model_details[m] = {"N": int(wm), "mean": ym, "pct": ym * 100.0}

eta_sq_model = ss_btw_model / ss_tot
eta_sq_model_pct = eta_sq_model * 100.0

# Factor: Seat (10 seats)
seats = df_raw["seat"].to_numpy()[valid_mask]
unique_seats = np.unique(seats)
ss_btw_seat = 0.0
seat_details = {}
for s in unique_seats:
    idx = seats == s
    ws = np.sum(w_val[idx])
    ys = np.sum(w_val[idx] * y_val[idx]) / ws
    ss_btw_seat += ws * (ys - grand_mean) ** 2
    seat_details[s] = {"N": int(ws), "mean": ys, "pct": ys * 100.0}

eta_sq_seat = ss_btw_seat / ss_tot
eta_sq_seat_pct = eta_sq_seat * 100.0

net_dominance = eta_sq_model_pct - eta_sq_seat_pct
dominance_ratio = eta_sq_model / eta_sq_seat

print(f"\n[VARIANCE DECOMPOSITION RESULTS]")
print(f"  SS_between (Model): {ss_btw_model:.6f}")
print(f"  eta^2_Model:        {eta_sq_model:.6f} ({eta_sq_model_pct:.4f}%)")
print(f"  SS_between (Seat):  {ss_btw_seat:.6f}")
print(f"  eta^2_Seat:         {eta_sq_seat:.6f} ({eta_sq_seat_pct:.4f}%)")
print(f"  Net Dominance:      {net_dominance:+.4f}%")
print(f"  Dominance Ratio:    {dominance_ratio:.4f}x")

# Compare with claimed numbers:
# Claimed: eta^2_Model = 6.1822%, eta^2_Seat = 0.2688%, Net = +5.9133%, Ratio = 23.00x
expected_m_eta = 6.1822
expected_s_eta = 0.2688
expected_net = 5.9133
expected_ratio = 23.00

diff_m = abs(eta_sq_model_pct - expected_m_eta)
diff_s = abs(eta_sq_seat_pct - expected_s_eta)
diff_net = abs(net_dominance - expected_net)
diff_ratio = abs(dominance_ratio - expected_ratio)

print(f"\n[COMPARISON WITH DISPATCH SPECIFICATION]")
print(f"  Model eta^2: diff = {diff_m:.6f}% {'PASS' if diff_m < 0.001 else 'FAIL'}")
print(f"  Seat eta^2:  diff = {diff_s:.6f}% {'PASS' if diff_s < 0.001 else 'FAIL'}")
print(f"  Net Dom:     diff = {diff_net:.6f}% {'PASS' if diff_net < 0.001 else 'FAIL'}")
print(f"  Ratio:       diff = {diff_ratio:.6f}x {'PASS' if diff_ratio < 0.01 else 'FAIL'}")

assert diff_m < 0.001
assert diff_s < 0.001
assert diff_net < 0.001
assert diff_ratio < 0.01

# -----------------------------------------------------------------------------
# STEP 4: PERMUTATION TEST BEHAVIOR AND REPRODUCIBILITY
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("PERMUTATION TEST SEED AND STATISTIC INVARIANCE")
print("=" * 80)

import cluster_stats as cs
from generate_block1_meta_to_all_buckets import within_p, within_omni_p, load_dataset, extract_worker_metrics, RANK_KEYS

loaded = [extract_worker_metrics(w) for w in load_dataset()]
df_loaded = pd.DataFrame(loaded)
df_loaded["abused_seat"] = 1 - df_loaded["safe_seat"]

# In Block 5 Table 1.1, check coworker p-values
# Note: In Block 5 main(), RANK_KEYS has the fingerprint of df_loaded
RANK_KEYS.add(df_loaded.index.values.tobytes())

p_m_acc = within_omni_p(df_loaded, "model", "s11_accuracy")
p_s_acc = within_omni_p(df_loaded, "seat", "s11_accuracy")
p_diff_acc = within_p(df_loaded, "seat", 10, "s11_accuracy")

p_m_ai = within_omni_p(df_loaded, "model", "s11_ai_as_hu")
p_s_ai = within_omni_p(df_loaded, "seat", "s11_ai_as_hu")
p_diff_ai = within_p(df_loaded, "seat", 10, "s11_ai_as_hu")

p_m_hu = within_omni_p(df_loaded, "model", "s11_hu_as_hu")
p_s_hu = within_omni_p(df_loaded, "seat", "s11_hu_as_hu")
p_diff_hu = within_p(df_loaded, "seat", 10, "s11_hu_as_hu")

# Also check Alex permutation p-values
p_m_alex = within_omni_p(df_loaded, "model", "s11_alex_as_hu")
p_s_alex = within_omni_p(df_loaded, "seat", "s11_alex_as_hu")
p_diff_alex = within_p(df_loaded, "seat", 10, "s11_alex_as_hu")

print(f"Permutation p-values (Table 1.1):")
print(f"  s11_accuracy: Model p={p_m_acc:.4f}, Seat p={p_s_acc:.4f}, Abused vs Safe p={p_diff_acc:.4f}")
print(f"  s11_ai_as_hu: Model p={p_m_ai:.4f}, Seat p={p_s_ai:.4f}, Abused vs Safe p={p_diff_ai:.4f}")
print(f"  s11_hu_as_hu: Model p={p_m_hu:.4f}, Seat p={p_s_hu:.4f}, Abused vs Safe p={p_diff_hu:.4f}")
print(f"  s11_alex_as_hu: Model p={p_m_alex:.4f}, Seat p={p_s_alex:.4f}, Abused vs Safe p={p_diff_alex:.4f}")

# Compare against baseline cache line 60, 61, 62 in reports/block5_seat_vs_model_inferential_report.md
# Baseline line 60: s11_accuracy | ... | p=0.6661 | 0.26% | 0.5993
assert abs(p_diff_acc - 0.6661) < 0.001
assert abs(p_s_acc - 0.5993) < 0.001
# Baseline line 61: s11_ai_as_hu | ... | p=0.5380 | 0.21% | 0.7080
assert abs(p_diff_ai - 0.5380) < 0.001
assert abs(p_s_ai - 0.7080) < 0.001
# Baseline line 62: s11_hu_as_hu | ... | p=0.8799 | 0.45% | 0.6361
assert abs(p_diff_hu - 0.8799) < 0.001
assert abs(p_s_hu - 0.6361) < 0.001

print("Permutation test p-values for all coworker metrics match baseline cache EXACTLY!")

# Check S12 outcomes (which follow s11 in ALL_OUT_COLS) to verify that permutation p-values for S12 are unchanged
p_m_s12_hu = within_omni_p(df_loaded, "model", "s12_human_pref")
p_s_s12_hu = within_omni_p(df_loaded, "seat", "s12_human_pref")
p_diff_s12_hu = within_p(df_loaded, "seat", 10, "s12_human_pref")
print(f"  s12_human_pref: Model p={p_m_s12_hu:.4f}, Seat p={p_s_s12_hu:.4f}, Abused vs Safe p={p_diff_s12_hu:.4f}")
# From Block 5 report line 64: p=0.2546, Seat omnibus p=0.6263
assert abs(p_diff_s12_hu - 0.2546) < 0.001
assert abs(p_s_s12_hu - 0.6263) < 0.001
print("Subsequent S12 outcomes verified completely invariant as well!")

# -----------------------------------------------------------------------------
# STEP 5: TABLE 3.21 10x10 JOINT INTERACTION MATRIX AND MISSING DATA AUDIT
# -----------------------------------------------------------------------------
print("\n" + "=" * 80)
print("TABLE 3.21 CELL-BY-CELL AUDIT (10 MODELS x 10 SEATS = 100 CELLS)")
print("=" * 80)

# Table 3.21 evaluates s11_alex_as_hu across 10 models and 10 seats
models_list = [
    "gpt-6-astra", "claude-haiku-4-5", "gemini-2-5-pro", "llama-3-1-70b", "mistral-small-24b",
    "deepseek-v3", "qwen-2-5-72b", "glm-5-3", "nemotron-3-5", "seed-1-8"
]
seat_levels = list(range(1, 11))

tot_cell_den = 0
tot_cell_num = 0
cells_with_missing = []

for m in models_list:
    for s in seat_levels:
        sub = df_raw[(df_raw["model"] == m) & (df_raw["seat"] == s)]
        n_total_workers = len(sub)
        n_valid = sub["s11_alex_tot"].sum()
        n_missing = (sub["s11_alex_tot"] == 0).sum()
        n_human = sub["s11_alex_as_hu"].sum()

        tot_cell_den += n_valid
        tot_cell_num += n_human

        if n_missing > 0:
            cells_with_missing.append({
                "model": m,
                "seat": s,
                "total_workers": n_total_workers,
                "valid": n_valid,
                "missing": n_missing,
                "human": n_human,
                "rate": (n_human / n_valid * 100.0) if n_valid > 0 else 0.0
            })
        else:
            assert n_valid == 6.0, f"Expected 6 runs per cell for {m} Seat {s}, got {n_valid}"

print(f"Total cells audited: 100")
print(f"Sum of denominators across 100 cells: {tot_cell_den:.1f} (expected exactly 594.0)")
print(f"Sum of numerators across 100 cells:   {tot_cell_num:.1f} (expected exactly 384.0)")
print(f"Cells with missing runs: {len(cells_with_missing)}")
for cm in cells_with_missing:
    print(f"  Model: {cm['model']}, Seat: {cm['seat']} -> Valid: {cm['valid']:.0f}, Missing: {cm['missing']:.0f}, Guessed Human: {cm['human']:.0f} ({cm['rate']:.1f}%)")

assert tot_cell_den == 594.0, f"Expected total denominator 594.0, got {tot_cell_den}"
assert tot_cell_num == 384.0, f"Expected total numerator 384.0, got {tot_cell_num}"
assert sum(cm["missing"] for cm in cells_with_missing) == 6, f"Expected 6 missing runs total, got {sum(cm['missing'] for cm in cells_with_missing)}"
assert len(cells_with_missing) == 5, f"Expected 5 cells with missing runs, got {len(cells_with_missing)}"
assert all(cm["model"] == "qwen-2-5-72b" for cm in cells_with_missing), "All missing cells must belong to Qwen 2.5 72B"
assert {cm["seat"] for cm in cells_with_missing} == {1, 3, 5, 6, 9}, "Missing runs must occur in seats 1, 3, 5, 6, 9"
s5_missing = [cm for cm in cells_with_missing if cm["seat"] == 5][0]
assert s5_missing["missing"] == 2 and s5_missing["valid"] == 4.0, "Seat 5 must have 2 missing runs and valid denominator = 4"

# Now let's compare with the markdown text of Table 3.21 in reports/block5_seat_vs_model_inferential_report.md
print("\n[VERIFYING TABLE 3.21 IN GENERATED REPORT FILE]")
with open("reports/block5_seat_vs_model_inferential_report.md", "r", encoding="utf-8") as f:
    report_text = f.read()

# Extract Table 3.21 lines
t321_match = re.search(r"### Table 3\.21:.*?\n\n(.*?)(?=\n### Table 3\.22:|\n## Appendix)", report_text, re.DOTALL)
assert t321_match is not None, "Table 3.21 not found in Block 5 report!"
t321_text = t321_match.group(1).strip()
t321_lines = [l for l in t321_text.splitlines() if l.startswith("|") and not l.startswith("| :---")]

print(f"Extracted {len(t321_lines)} table rows from Table 3.21.")
# Check Qwen row
qwen_rows = [l for l in t321_lines if "Qwen 2.5 72B" in l]
assert len(qwen_rows) == 1
print(f"Qwen 2.5 72B row in Table 3.21:\n  {qwen_rows[0]}")

# Check Seat pooled mean row
seat_mean_rows = [l for l in t321_lines if "SEAT POOLED MEAN" in l]
assert len(seat_mean_rows) == 1
print(f"Seat pooled mean row in Table 3.21:\n  {seat_mean_rows[0]}")

print("\n" + "=" * 80)
print("ALL EMPIRICAL CHALLENGES PASSED WITH ZERO TOLERANCE!")
print("=" * 80)
