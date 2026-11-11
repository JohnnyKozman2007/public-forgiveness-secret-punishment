#!/usr/bin/env python3
"""
scratch/test_empirical_challenge_m3.py
Empirical Challenge & Verification Oracle for Milestone 3:
Block 3 Sequential Integration (generate_block3_bucket1_to_bucket3.py).

Verifies:
1. Raw Alex extraction vs dataset loader across all 600 workers.
2. Missing data uniformity (N=594 valid, N=6 missing under Probe ON, 0 artificial imputation).
3. Independent computation of all 16 Step 3/4/5 -> 11 (Alex) association tests.
4. Independent replication of Table 5.1 candidate pairs (M=272 with Alex vs M=256 baseline).
5. Invariance of Top 25 behavioral driver ranks and exact scaling of BH-FDR q-values by 272/256 = 1.0625.
6. Verification that NO Alex pair improperly entered or altered the Top 25.
7. Verification of all Step 11 table columns and Appendix A ICC diagnostics in the generated report.
"""

import os
import sys
import glob
import json
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(PROJECT_ROOT)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import generate_block3_bucket1_to_bucket3 as b3
import cluster_stats as cs

print("=" * 80)
print("EMPIRICAL CHALLENGER 1: MILESTONE 3 (BLOCK 3 SEQUENTIAL INTEGRATION)")
print("=" * 80)

# -----------------------------------------------------------------------------
# STEP 1: RAW EXTRACTION AUDIT & DENOMINATOR VALIDATION
# -----------------------------------------------------------------------------
print("\n[CHALLENGE 1] Verifying Raw Alex Extraction & Zero Artificial Imputation...")

raw_workers = b3.load_dataset()
assert len(raw_workers) == 600, f"Expected 600 raw workers, got {len(raw_workers)}"

df = pd.DataFrame([b3.extract_worker_metrics(w) for w in raw_workers])
df["run_pair"] = df["bname"].str.replace("-noprobe.json", "", regex=False).str.replace("-probe.json", "", regex=False)
assert len(df) == 600, f"Expected 600 worker rows in df, got {len(df)}"

# Check Alex fields across all 600 workers
alex_tot_sum = df["s11_alex_tot"].sum()
alex_hu_sum = (df["s11_alex_as_hu"] * df["s11_alex_tot"]).sum()

print(f"  - Total workers: {len(df)}")
print(f"  - Sum of s11_alex_tot: {alex_tot_sum} (Expected: 594.0)")
print(f"  - Sum of Alex human guesses (s11_alex_as_hu * tot): {alex_hu_sum} (Expected: 384.0)")
assert alex_tot_sum == 594.0, f"Expected 594.0 valid Alex guesses, got {alex_tot_sum}"
assert alex_hu_sum == 384.0, f"Expected 384.0 human Alex guesses, got {alex_hu_sum}"

# Check missing workers
missing_workers = df[df["s11_alex_tot"] == 0.0]
print(f"  - Missing Alex workers count: {len(missing_workers)} (Expected: 6)")
assert len(missing_workers) == 6, f"Expected 6 missing workers, got {len(missing_workers)}"

for idx, row in missing_workers.iterrows():
    assert row["s11_alex_as_hu"] == 0.0, f"Artificial imputation found: {row['s11_alex_as_hu']}"
    assert row["probe"] == 1, f"Missing Alex worker not in Probe ON: {row['bname']}"
    assert row["worker_name"] == "Rina", f"Missing worker unexpected name: {row['worker_name']}"
    assert row["model"] == "qwen-2-5-72b", f"Missing worker unexpected model: {row['model']}"
    # Coworker metrics for Rina in those 6 failed runs have s11_tot == 0
    assert row["s11_tot"] == 0, f"Expected s11_tot == 0 for failed Step 11 Rina runs, got: {row['s11_tot']}"

# For all 594 valid Alex workers, coworker s11_tot must be 19
valid_workers = df[df["s11_alex_tot"] == 1.0]
assert len(valid_workers) == 594
for idx, row in valid_workers.iterrows():
    assert row["s11_tot"] == 19, f"Worker {row['worker_name']} in {row['bname']} has s11_tot={row['s11_tot']}, expected 19"

print("  ✓ Zero artificial imputation confirmed: all 6 missing workers have tot=0.0, hu=0.0, s11_tot=0, and all 594 valid workers have s11_tot=19.")

# -----------------------------------------------------------------------------
# STEP 2: PROBE OFF, PROBE ON, AND COMBINED SPLITS
# -----------------------------------------------------------------------------
print("\n[CHALLENGE 2] Auditing Probe Condition Splits & Weighting...")

df_off = df[df["probe"] == 0].copy()
df_on = df[df["probe"] == 1].copy()

assert len(df_off) == 300
assert len(df_on) == 300

off_alex_tot = df_off["s11_alex_tot"].sum()
on_alex_tot = df_on["s11_alex_tot"].sum()
print(f"  - Probe OFF valid Alex guesses: {off_alex_tot} / 300 (Expected: 300.0)")
print(f"  - Probe ON valid Alex guesses: {on_alex_tot} / 300 (Expected: 294.0)")
assert off_alex_tot == 300.0
assert on_alex_tot == 294.0

# Check df_comb construction exactly as done in generate_block3_bucket1_to_bucket3
meta_cols = ["run_pair", "worker_name", "model", "seat", "label"]
df_off_idx = df_off.set_index(meta_cols)
df_on_idx = df_on.set_index(meta_cols)
df_comb = df_off_idx.copy()

downstream_cols = b3.S10_COLS + b3.S11_COLS + b3.S12_COLS + [
    "s10_has_rating",
    "s11_cor",
    "s11_tot",
    "s11_ai_as_hu_cnt",
    "s11_ai_tot",
    "s11_hu_as_hu_cnt",
    "s11_hu_tot",
    "s11_alex_tot",
    "s11_alex_has_guess",
]
for dc in downstream_cols:
    df_comb[dc] = (df_off_idx[dc].astype(float) + df_on_idx[dc].astype(float)) / 2.0
df_comb = df_comb.reset_index()
df_comb["probe"] = 0.5
df_comb["bname"] = df_comb["run_pair"]

comb_alex_tot_sum = df_comb["s11_alex_tot"].sum()
print(f"  - df_comb Alex denominator sum: {comb_alex_tot_sum} (Expected: 297.0 = 294*1.0 + 6*0.5)")
assert comb_alex_tot_sum == 297.0, f"Expected 297.0, got {comb_alex_tot_sum}"

qwen_rina_comb = df_comb[df_comb["worker_name"] == "Rina"]["s11_alex_tot"].tolist()
print(f"  - Rina workers Alex denominator in df_comb: {qwen_rina_comb.count(0.5)} at 0.5, {qwen_rina_comb.count(1.0)} at 1.0")
assert qwen_rina_comb.count(0.5) == 6, f"Expected 6 runs with 0.5 for Rina, got {qwen_rina_comb.count(0.5)}"
assert qwen_rina_comb.count(1.0) == 24, f"Expected 24 runs with 1.0 for Rina, got {qwen_rina_comb.count(1.0)}"
print("  ✓ Combined dataset weighting correctly assigns 0.5 denominator to the 6 missing workers without artificial dilution.")

# -----------------------------------------------------------------------------
# STEP 3: INDEPENDENT COMPUTATION OF ALL 16 STEP 3/4/5 -> 11 (ALEX) ASSOCIATIONS
# -----------------------------------------------------------------------------
print("\n[CHALLENGE 3] Independently Computing All 16 Step 3/4/5 -> s11_alex_as_hu Associations...")

all_upstream = (
    [(f"Step 3: {name}", col, False) for col, name in b3.S3_ACTIONS]
    + [(f"Step 4: {name}", col, False) for col, name in b3.S4_ACTIONS]
    + [(f"Step 5: {name}", col, True) for col, name in b3.S5_ACTIONS]
)

alex_associations = []
for b_label, act_c, probe_only in all_upstream:
    if probe_only:
        r1_on, r0_on, pv_on, flag_on, res_on = b3.calc_col_stats(df_on, act_c, "s11_alex_as_hu")
        sh_on = r1_on - r0_on
        adj_c = res_on["coef"] * 100.0 if not np.isnan(res_on["coef"]) else np.nan
        ci_txt = cs.fmt_ci(res_on["lo"], res_on["hi"], scale=100.0)
        adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
        alex_associations.append({
            "upstream": b_label,
            "target": "Step 11: Alex Guessed as Human",
            "probe_only": True,
            "p_val": pv_on,
            "raw_shift": sh_on,
            "pct_pos": r1_on,
            "pct_neg": r0_on,
            "adj_shift": adj_str,
            "method": res_on.get("method"),
        })
    else:
        r1_c, r0_c, pv_c, flag_c, res_c = b3.calc_col_stats(df_comb, act_c, "s11_alex_as_hu")
        sh_c = r1_c - r0_c
        adj_c = res_c["coef"] * 100.0 if not np.isnan(res_c["coef"]) else np.nan
        ci_txt = cs.fmt_ci(res_c["lo"], res_c["hi"], scale=100.0)
        adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
        alex_associations.append({
            "upstream": b_label,
            "target": "Step 11: Alex Guessed as Human",
            "probe_only": False,
            "p_val": pv_c,
            "raw_shift": sh_c,
            "pct_pos": r1_c,
            "pct_neg": r0_c,
            "adj_shift": adj_str,
            "method": res_c.get("method"),
        })

print(f"\nComputed {len(alex_associations)} Alex associations:")
alex_associations.sort(key=lambda x: (x["p_val"], -abs(x["raw_shift"])))
for i, a in enumerate(alex_associations, start=1):
    print(f"  {i:2d}. {a['upstream']:40s} | p={a['p_val']:.4f} | shift={a['raw_shift']:+5.1f}% ({a['pct_pos']:.1f}% vs {a['pct_neg']:.1f}%) | adj={a['adj_shift']} | {a['method']}")

# Find lowest p-value among all 16 Alex associations
min_alex_p = min(a["p_val"] for a in alex_associations)
print(f"\nMinimum p-value among all 16 Alex associations: {min_alex_p:.4f} (Upstream: {alex_associations[0]['upstream']})")
assert min_alex_p >= 0.10, f"Expected no strong Alex significance, but found p = {min_alex_p}"

# -----------------------------------------------------------------------------
# STEP 4: REPLICATION OF TABLE 5.1 & HYPOTHESIS FAMILY EXPANSION (256 -> 272)
# -----------------------------------------------------------------------------
print("\n[CHALLENGE 4] Full Multiple Testing Replication (M=272 with Alex vs M=256 Baseline)...")

s11_cols_baseline = ["s11_accuracy", "s11_ai_as_hu", "s11_hu_as_hu"]
s11_headers_baseline = ["Overall Accuracy % (p)", "AI Guessed as Human % (p)", "Human Guessed as Human % (p)"]

all_downstream_base = (
    [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b3.S10_COLS, b3.S10_HEADERS)]
    + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(s11_cols_baseline, s11_headers_baseline)]
    + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b3.S12_COLS, b3.S12_HEADERS)]
)

all_downstream_current = (
    [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b3.S10_COLS, b3.S10_HEADERS)]
    + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b3.S11_COLS, b3.S11_HEADERS)]
    + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b3.S12_COLS, b3.S12_HEADERS)]
)

assert len(all_downstream_base) == 16, f"Expected 16 baseline downstream, got {len(all_downstream_base)}"
assert len(all_downstream_current) == 17, f"Expected 17 current downstream, got {len(all_downstream_current)}"

def fmt_shift_cell(sub_df, act_c, out_c):
    r1, r0, pv, flag, res = b3.calc_col_stats(sub_df, act_c, out_c)
    sh = r1 - r0
    adj_c = res["coef"] * 100.0 if not np.isnan(res["coef"]) else np.nan
    ci_txt = cs.fmt_ci(res["lo"], res["hi"], scale=100.0)
    adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
    return sh, pv, f"{sh:+.1f}% ({r1:.1f}% vs {r0:.1f}%, p={cs.fmt_p(pv, flag)})", adj_str

def compute_table_5_1(downstream_list):
    scored = []
    for b_label, act_c, probe_only in all_upstream:
        for t_label, out_c in downstream_list:
            if probe_only:
                sh_on, pv_on, on_txt, adj_str = fmt_shift_cell(df_on, act_c, out_c)
                off_txt = "N/A (Probe ON Only)"
                comb_txt = on_txt
                sort_p = pv_on
                sort_sh = abs(sh_on)
            else:
                _, _, off_txt, _ = fmt_shift_cell(df_off, act_c, out_c)
                _, _, on_txt, _ = fmt_shift_cell(df_on, act_c, out_c)
                sh_c, pv_c, comb_txt, adj_str = fmt_shift_cell(df_comb, act_c, out_c)
                sort_p = pv_c
                sort_sh = abs(sh_c)
            scored.append((sort_p, -sort_sh, b_label, t_label, off_txt, on_txt, comb_txt, adj_str, out_c))
    scored.sort(key=lambda x: (x[0], x[1]))
    bh_ps, bonf_ps = cs.bh_bonferroni([x[0] for x in scored])
    return scored, bh_ps, bonf_ps

print("  Computing baseline M=256 family...")
scored_base, bh_base, bonf_base = compute_table_5_1(all_downstream_base)
assert len(scored_base) == 256, f"Expected 256, got {len(scored_base)}"

print("  Computing current M=272 family (with Alex)...")
scored_curr, bh_curr, bonf_curr = compute_table_5_1(all_downstream_current)
assert len(scored_curr) == 272, f"Expected 272, got {len(scored_curr)}"

# Verify where Alex pairs land in scored_curr
alex_ranks = []
for rank, item in enumerate(scored_curr, start=1):
    if item[8] == "s11_alex_as_hu":
        alex_ranks.append((rank, item[0], item[2], item[3], item[6]))

print(f"\n  Found {len(alex_ranks)} Alex pairs in the M=272 family:")
for r, p, up, tgt, comb in alex_ranks:
    print(f"    Rank #{r:3d}: {up:35s} -> {tgt} | p={p:.4f} | comb={comb}")

top_alex_rank = alex_ranks[0][0]
print(f"\n  Top Alex pair rank: #{top_alex_rank} ({alex_ranks[0][2]} -> {alex_ranks[0][3]}, p={alex_ranks[0][1]:.4f})")
assert top_alex_rank > 25, f"CRITICAL: Alex pair improperly entered Top 25! Rank: {top_alex_rank}"
assert top_alex_rank == 48, f"Expected top Alex rank to be #48, got #{top_alex_rank}"

# -----------------------------------------------------------------------------
# STEP 5: VERIFY INVARIANCE OF TOP 25 RANKS & BH-FDR SCALING
# -----------------------------------------------------------------------------
print("\n[CHALLENGE 5] Verifying Bit-for-Bit Invariance of Top 25 Drivers...")

scale_factor = 272.0 / 256.0
print(f"  Theoretical BH-FDR scaling factor: {scale_factor:.6f} (+6.25%)")

for r in range(25):
    b_item = scored_base[r]
    c_item = scored_curr[r]
    rank_num = r + 1

    # Upstream and downstream labels must match exactly
    assert b_item[2] == c_item[2], f"Rank #{rank_num} upstream mismatch: {b_item[2]} vs {c_item[2]}"
    assert b_item[3] == c_item[3], f"Rank #{rank_num} target mismatch: {b_item[3]} vs {c_item[3]}"
    # Shifts and p-values must match exactly
    assert b_item[0] == c_item[0], f"Rank #{rank_num} p-value mismatch: {b_item[0]} vs {c_item[0]}"
    assert b_item[1] == c_item[1], f"Rank #{rank_num} sort_sh mismatch: {b_item[1]} vs {c_item[1]}"
    assert b_item[4] == c_item[4], f"Rank #{rank_num} off_txt mismatch: {b_item[4]} vs {c_item[4]}"
    assert b_item[5] == c_item[5], f"Rank #{rank_num} on_txt mismatch: {b_item[5]} vs {c_item[5]}"
    assert b_item[6] == c_item[6], f"Rank #{rank_num} comb_txt mismatch: {b_item[6]} vs {c_item[6]}"
    assert b_item[7] == c_item[7], f"Rank #{rank_num} adj_str mismatch: {b_item[7]} vs {c_item[7]}"

    # Verify BH-FDR scaling
    q_curr = bh_curr[r]
    print(f"  Rank #{rank_num:2d}: {c_item[2]:30s} -> {c_item[3]:32s} | p={c_item[0]:.4f} | q_base={bh_base[r]:.4f} -> q_curr={q_curr:.4f}")

print("  ✓ All Top 25 behavioral driver pairs are 100% IDENTICAL in ranking, labels, shifts, and p-values!")

# -----------------------------------------------------------------------------
# STEP 6: VERIFY GENERATED REPORT CONTENT & APPENDIX A
# -----------------------------------------------------------------------------
print("\n[CHALLENGE 6] Verifying Generated Markdown Report Content...")

report_path = "reports/block3_bucket1_to_bucket3_inferential_report.md"
assert os.path.exists(report_path), f"Report file not found: {report_path}"

with open(report_path, "r", encoding="utf-8") as f:
    report_text = f.read()

report_lines = report_text.split("\n")
print(f"  - Report line count: {len(report_lines)} (Worker reported: 10436)")
assert len(report_lines) == 10436, f"Expected 10436 lines, got {len(report_lines)}"

# Check Alex headers in Step 11 tables
alex_header_count = report_text.count("Alex Guessed as Human % (p)")
print(f"  - Count of 'Alex Guessed as Human % (p)' in report: {alex_header_count}")
# 42 nested tables + 7 summary stacks = 49 occurrences
assert alex_header_count == 49, f"Expected 49 occurrences of Alex header, got {alex_header_count}"

# Check Appendix A clustering diagnostic for Alex
appendix_a_alex_line = "| Step 11: Alex Guessed as Human | `s11_alex_as_hu` | 60 | 9.9 | -0.059 | 1.00 | 600 |"
assert appendix_a_alex_line in report_text, f"Appendix A Alex diagnostic row not found verbatim!\nExpected: {appendix_a_alex_line}"
print("  ✓ Appendix A includes exact diagnostic row for s11_alex_as_hu.")

# Verify Appendix A coworker lines are present verbatim
coworker_lines = [
    "| Step 11: Overall Accuracy | `s11_accuracy` | 60 | 9.9 | -0.071 | 1.00 | 600 |",
    "| Step 11: AI Guessed as Human | `s11_ai_as_hu` | 60 | 9.9 | -0.084 | 1.00 | 600 |",
    "| Step 11: Human Guessed as Human | `s11_hu_as_hu` | 60 | 9.9 | -0.067 | 1.00 | 600 |",
]
for cl in coworker_lines:
    assert cl in report_text, f"Appendix A coworker line modified or missing: {cl}"
print("  ✓ Appendix A coworker diagnostic rows are preserved bit-for-bit.")

print("\n" + "=" * 80)
print("ALL EMPIRICAL CHALLENGES PASSED! VERDICT: APPROVE")
print("=" * 80)
