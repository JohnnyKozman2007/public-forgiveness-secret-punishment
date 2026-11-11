#!/usr/bin/env python3
"""
Empirical Challenge & Stress Harness for Milestone 4 (Block 4 Bucket 2 -> Bucket 3).
Author: Challenger 1 (critic, specialist)
"""

import os
import sys

sys.path.insert(0, os.path.abspath("."))

import json
import re
import numpy as np
import pandas as pd
from collections import Counter

import generate_block4_bucket2_to_bucket3 as b4
import cluster_stats as cs

def test_1_denominator_masking_and_imputation():
    print("=" * 70)
    print("TEST 1: Denominator Masking & Zero Artificial Imputation")
    print("=" * 70)

    raw_workers = b4.load_dataset()
    assert len(raw_workers) == 600, f"Expected 600 raw workers, got {len(raw_workers)}"

    df = pd.DataFrame([b4.extract_worker_metrics(w) for w in raw_workers])
    assert len(df) == 600, f"Expected 600 extracted worker rows, got {len(df)}"

    # 1. Total valid vs missing Alex guesses
    alex_tot_series = df["s11_alex_tot"]
    alex_hu_series = df["s11_alex_as_hu"]
    alex_has_guess = df["s11_alex_has_guess"]

    n_valid = int((alex_tot_series == 1.0).sum())
    n_missing = int((alex_tot_series == 0.0).sum())
    print(f"[Check 1.1] Total valid Alex guesses: {n_valid} (expected 594)")
    print(f"[Check 1.2] Total missing Alex guesses: {n_missing} (expected 6)")
    assert n_valid == 594, f"Expected exactly 594 valid Alex guesses, got {n_valid}"
    assert n_missing == 6, f"Expected exactly 6 missing Alex guesses, got {n_missing}"

    # Alias check
    assert (alex_tot_series == alex_has_guess).all(), "s11_alex_tot and s11_alex_has_guess must be identical"
    print("[Check 1.3] Alias identity: s11_alex_tot == s11_alex_has_guess for all 600 rows: PASS")

    # Missing rows inspection
    missing_df = df[alex_tot_series == 0.0]
    for idx, row in missing_df.iterrows():
        assert row["worker_name"] == "Rina", f"Unexpected missing worker: {row['worker_name']}"
        assert row["probe"] == 1, f"Missing worker was not Probe ON: {row['bname']}"
        assert row["model"] == "qwen-2-5-72b", f"Missing worker model was not Qwen: {row['model']}"
        assert row["s11_alex_as_hu"] == 0.0, f"Artificial imputation found in missing row! {row['s11_alex_as_hu']}"
        assert row["s11_alex_tot"] == 0.0, f"Denominator non-zero in missing row! {row['s11_alex_tot']}"
    print(f"[Check 1.4] Provenance and Zero Imputation across all 6 missing rows: PASS (All Rina, Qwen-2-5-72b, Probe ON, zero imputed)")

    # Coworker metrics isolation on missing rows
    for idx, row in missing_df.iterrows():
        assert row["s11_tot"] == 0, f"Expected s11_tot == 0 for missing worker {row['worker_name']} in run {row['bname']}"
        assert row["s11_accuracy"] == 0.0
        assert row["s11_ai_as_hu"] == 0.0
        assert row["s11_hu_as_hu"] == 0.0
    print(f"[Check 1.5] Coworker metrics on missing rows remain intact (s11_tot==0, zero-ratio): PASS")

    # Ratio Denominator Exclusion
    tot_sum = alex_tot_series.sum()
    hu_sum = (df["s11_alex_as_hu"] * df["s11_alex_tot"]).sum()
    hu_rate = (hu_sum / tot_sum) * 100.0
    print(f"[Check 1.6] Denominator sum = {tot_sum:.1f}, Numerator sum = {hu_sum:.1f}, Pooled Rate = {hu_rate:.4f}%")
    assert tot_sum == 594.0, f"Expected denominator sum 594.0, got {tot_sum}"
    assert hu_sum == 384.0, f"Expected numerator sum 384.0, got {hu_sum}"
    assert abs(hu_rate - 64.646464) < 1e-4

    print("TEST 1 PASSED: Denominator masking and zero imputation strictly verified.\n")
    return df

def test_2_table41_multiple_testing_and_alex_ranks(df):
    print("=" * 70)
    print("TEST 2: Table 4.1 Multiple Testing Ranks & Alex Driver Pairs")
    print("=" * 70)

    df_off = df[df["probe"] == 0]
    df_on = df[df["probe"] == 1]

    all_upstream = (
        [(f"Step 6: {name}", col) for col, name in b4.S6_ACTIONS]
        + [(f"Step 9: {name}", col) for col, name in b4.S9_ACTIONS]
    )
    all_downstream = (
        [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S10_COLS, b4.S10_HEADERS)]
        + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S11_COLS, b4.S11_HEADERS)]
        + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S12_COLS, b4.S12_HEADERS)]
    )

    n_upstream = len(all_upstream)
    n_downstream = len(all_downstream)
    m_total = n_upstream * n_downstream
    print(f"[Check 2.1] Upstream actions: {n_upstream}, Downstream outcomes: {n_downstream}, Total hypotheses M = {m_total}")
    assert n_upstream == 11, f"Expected 11 upstream, got {n_upstream}"
    assert n_downstream == 17, f"Expected 17 downstream, got {n_downstream}"
    assert m_total == 187, f"Expected M = 187, got {m_total}"

    def fmt_shift_cell(sub_df, act_c, out_c):
        r1, r0, pv, flag, res = b4.calc_col_stats(sub_df, act_c, out_c)
        sh = r1 - r0
        adj_c = res["coef"] * 100.0 if not np.isnan(res["coef"]) else np.nan
        ci_txt = cs.fmt_ci(res["lo"], res["hi"], scale=100.0)
        adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
        return sh, pv, f"{sh:+.1f}% ({r1:.1f}% vs {r0:.1f}%, p={cs.fmt_p(pv, flag)})", adj_str

    print("Computing all 187 hypothesis tests...")
    scored_pairs = []
    for b_label, act_c in all_upstream:
        for t_label, out_c in all_downstream:
            _, _, off_txt, _ = fmt_shift_cell(df_off, act_c, out_c)
            _, _, on_txt, _ = fmt_shift_cell(df_on, act_c, out_c)
            sh_c, pv_c, comb_txt, adj_str = fmt_shift_cell(df, act_c, out_c)
            scored_pairs.append({
                "pv_c": pv_c,
                "neg_abs_sh": -abs(sh_c),
                "sh_c": sh_c,
                "b_label": b_label,
                "act_c": act_c,
                "t_label": t_label,
                "out_c": out_c,
                "off_txt": off_txt,
                "on_txt": on_txt,
                "comb_txt": comb_txt,
                "adj_str": adj_str,
            })

    # Sort according to Table 4.1 logic
    scored_pairs.sort(key=lambda x: (x["pv_c"], x["neg_abs_sh"]))
    raw_pvals = [x["pv_c"] for x in scored_pairs]
    bh_ps, bonf_ps = cs.bh_bonferroni(raw_pvals)

    for i, pair in enumerate(scored_pairs):
        pair["rank"] = i + 1
        pair["bh_q"] = bh_ps[i]
        pair["bonf_p"] = bonf_ps[i]

    # Inspect all Alex pairs
    alex_pairs = [p for p in scored_pairs if p["out_c"] == "s11_alex_as_hu"]
    print(f"\n[Check 2.2] Total pairs involving s11_alex_as_hu: {len(alex_pairs)} (expected 11)")
    assert len(alex_pairs) == 11, f"Expected 11 Alex pairs, got {len(alex_pairs)}"

    print("\n--- Detailed Summary of all 11 Step 6/9 -> Step 11 Alex Pairs ---")
    for ap in alex_pairs:
        print(f"Rank #{ap['rank']:3d} | {ap['b_label']:35s} -> {ap['t_label']:30s} | Comb Raw: {ap['comb_txt']} | Adj: {ap['adj_str']} | BH q={cs.fmt_p(ap['bh_q'])} | Bonf={cs.fmt_p(ap['bonf_p'])}")

    top_alex_pair = alex_pairs[0]
    print(f"\nHighest-ranked Alex pair: Rank #{top_alex_pair['rank']} ({top_alex_pair['b_label']} -> {top_alex_pair['t_label']})")
    print(f"Raw p-value: {top_alex_pair['pv_c']:.4f}, Raw Shift: {top_alex_pair['sh_c']:+.1f}%")

    # Verify no Alex pair is in the top 25
    alex_in_top_25 = [p for p in alex_pairs if p["rank"] <= 25]
    print(f"[Check 2.3] Alex pairs in Top 25: {len(alex_in_top_25)} (expected 0)")
    assert len(alex_in_top_25) == 0, f"Alex pairs unexpectedly entered Top 25: {alex_in_top_25}"

    # Also compute Table 4.1 WITHOUT Alex (M = 176) to verify stability of Top 25
    legacy_pairs = [p for p in scored_pairs if p["out_c"] != "s11_alex_as_hu"]
    legacy_pairs.sort(key=lambda x: (x["pv_c"], x["neg_abs_sh"]))
    legacy_bh, legacy_bonf = cs.bh_bonferroni([x["pv_c"] for x in legacy_pairs])
    for i, lp in enumerate(legacy_pairs):
        lp["legacy_rank"] = i + 1
        lp["legacy_bh"] = legacy_bh[i]
        lp["legacy_bonf"] = legacy_bonf[i]

    print("\n[Check 2.4] Verifying Top 25 Ranks Invariance (M=176 vs M=187):")
    for r in range(25):
        new_p = scored_pairs[r]
        leg_p = legacy_pairs[r]
        assert new_p["b_label"] == leg_p["b_label"], f"Rank {r+1} driver mismatch: {new_p['b_label']} vs {leg_p['b_label']}"
        assert new_p["t_label"] == leg_p["t_label"], f"Rank {r+1} target mismatch: {new_p['t_label']} vs {leg_p['t_label']}"
        assert new_p["pv_c"] == leg_p["pv_c"], f"Rank {r+1} p-value mismatch"
        print(f"Rank #{r+1:2d}: {new_p['b_label']} -> {new_p['t_label']} [PASS: identical pair, p={new_p['pv_c']:.4f}]")

    # Compare with report markdown verbatim
    report_path = "reports/block4_bucket2_to_bucket3_inferential_report.md"
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    print("\n[Check 2.5] Verifying Report Table 4.1 Top 25 rows against independent recomputation:")
    table41_lines = [l for l in report_text.splitlines() if l.startswith("| **#")]
    assert len(table41_lines) == 25, f"Expected 25 rendered rows in Table 4.1, found {len(table41_lines)}"

    for r_idx, line in enumerate(table41_lines, start=1):
        p = scored_pairs[r_idx - 1]
        q_txt = cs.fmt_p(p["bh_q"])
        b_txt = cs.fmt_p(p["bonf_p"])
        expected_line = f"| **#{r_idx}** | **{p['b_label']}** | `{p['t_label']}` | {p['off_txt']} | {p['on_txt']} | **{p['comb_txt']}** | {p['adj_str']} | **{q_txt}** | **{b_txt}** |"
        assert line == expected_line, f"Table 4.1 row #{r_idx} discrepancy:\nREPORT:   {line}\nEXPECTED: {expected_line}"

    print("All 25 rows in Report Table 4.1 match independent recomputation character-for-character! PASS.")
    print("TEST 2 PASSED: Multiple testing ranks and Alex pairs strictly verified.\n")
    return scored_pairs

def test_3_step11_tables_and_subtable_averages(df):
    print("=" * 70)
    print("TEST 3: Step 11 Tables, Sub-Table Averages & Edge Cases")
    print("=" * 70)

    # Check Qwen 2.5 72B under Probe ON (Part 2)
    df_on = df[df["probe"] == 1]
    qwen_on = df_on[df_on["model"] == "qwen-2-5-72b"]
    assert len(qwen_on) == 30, f"Expected 30 Qwen workers in Probe ON, got {len(qwen_on)}"
    qwen_alex_tot = qwen_on["s11_alex_tot"].sum()
    print(f"[Check 3.1] Qwen-2-5-72b Probe ON: total workers = {len(qwen_on)}, valid Alex denominator = {qwen_alex_tot}")
    assert qwen_alex_tot == 24.0, f"Expected 24.0 valid Alex guesses for Qwen Probe ON, got {qwen_alex_tot}"

    # Check Table 2.3 and 2.4 calculations for Qwen on s11_alex_as_hu
    for act_col, act_name in b4.S6_ACTIONS:
        r1, r0, pv, flag, res = b4.calc_col_stats(qwen_on, act_col, "s11_alex_as_hu")
        assert not np.isnan(r1), f"NaN rate for {act_name} in Qwen ON"
        assert not np.isnan(r0), f"NaN rate for {act_name} in Qwen ON"
        assert not np.isnan(pv), f"NaN p-value for {act_name} in Qwen ON"
    print("[Check 3.2] Qwen-2-5-72b Probe ON Step 6 -> 11 calculations: PASS (No NaNs, correctly excludes 6 missing)")

    for act_col, act_name in b4.S9_ACTIONS:
        r1, r0, pv, flag, res = b4.calc_col_stats(qwen_on, act_col, "s11_alex_as_hu")
        assert not np.isnan(r1), f"NaN rate for {act_name} in Qwen ON"
        assert not np.isnan(r0), f"NaN rate for {act_name} in Qwen ON"
        assert not np.isnan(pv), f"NaN p-value for {act_name} in Qwen ON"
    print("[Check 3.3] Qwen-2-5-72b Probe ON Step 9 -> 11 calculations: PASS (No NaNs, correctly excludes 6 missing)")

    # Read the report and verify Step 11 table structures
    report_path = "reports/block4_bucket2_to_bucket3_inferential_report.md"
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    # Step 11 table headers
    step11_tables = re.findall(r"(#### Table \d+\.\d+: .*?-> Step 11 Peer Identification.*?)\n\n(\|.*?\|)\n(\|.*?\|)", report_text)
    print(f"[Check 3.4] Found {len(step11_tables)} Step 11 tables in report (expected 36)")
    assert len(step11_tables) == 36, f"Expected 36 Step 11 tables, found {len(step11_tables)}"

    expected_s11_header = "| Overall Accuracy % (p) | AI Guessed as Human % (p) | Human Guessed as Human % (p) | Alex Guessed as Human % (p) |"
    for title, hline, aline in step11_tables:
        assert hline.endswith(expected_s11_header), f"Table header missing Alex column:\n{title}\n{hline}"
    print("[Check 3.5] All 36 Step 11 tables contain all 4 Step 11 columns with Alex Guessed as Human % (p): PASS")

    # Verify Summary Stacks
    summary_stacks = re.findall(r"(#### .*?(?:Summary|Summary Stack).*?Step [69] -> Step 11 Peer Identification.*?)\n\n(\|.*?\|)\n(\|.*?\|)", report_text)
    print(f"[Check 3.6] Found {len(summary_stacks)} Step 11 Summary Stacks (expected 6)")
    assert len(summary_stacks) == 6, f"Expected 6 Step 11 summary stacks, found {len(summary_stacks)}"
    for title, hline, aline in summary_stacks:
        assert hline.endswith(expected_s11_header), f"Summary stack missing Alex column:\n{title}\n{hline}"
    print("[Check 3.7] All 6 Step 11 Summary Stacks contain all 4 Step 11 columns: PASS")

    print("TEST 3 PASSED: Step 11 tables, subtable averages, and edge cases strictly verified.\n")

def test_4_appendix_a_diagnostics(df):
    print("=" * 70)
    print("TEST 4: Appendix A Clustering Diagnostics (ICC & Design Effect)")
    print("=" * 70)

    icc_cols = (
        [(col, f"Step 6: {name}") for col, name in b4.S6_ACTIONS]
        + [(col, f"Step 9: {name}") for col, name in b4.S9_ACTIONS]
        + [(col, f"Step 10: {hdr.replace(' % (p)', '')}") for col, hdr in zip(b4.S10_COLS, b4.S10_HEADERS)]
        + [(col, f"Step 11: {hdr.replace(' % (p)', '')}") for col, hdr in zip(b4.S11_COLS, b4.S11_HEADERS)]
        + [(col, f"Step 12: {hdr.replace(' % (p)', '')}") for col, hdr in zip(b4.S12_COLS, b4.S12_HEADERS)]
    )

    lines = []
    cs.render_icc_section(
        lines,
        "APPENDIX A: CLUSTERING DIAGNOSTICS (ICC & Design Effect per Variable, Cluster = Run)",
        df,
        icc_cols,
        ratio_map=b4.S11_COUNT_MAP,
    )
    rendered_icc = "\n".join(lines)

    # Check Alex row
    expected_alex_row = "| Step 11: Alex Guessed as Human | `s11_alex_as_hu` | 60 | 9.9 | -0.059 | 1.00 | 600 |"
    assert expected_alex_row in rendered_icc, f"Expected Alex row not found in rendered Appendix A:\n{rendered_icc}"
    print(f"[Check 4.1] Alex ICC row verified: {expected_alex_row}")

    # Check coworker rows
    expected_acc_row = "| Step 11: Overall Accuracy | `s11_accuracy` | 60 | 9.9 | -0.071 | 1.00 | 600 |"
    expected_ai_row = "| Step 11: AI Guessed as Human | `s11_ai_as_hu` | 60 | 9.9 | -0.084 | 1.00 | 600 |"
    expected_hu_row = "| Step 11: Human Guessed as Human | `s11_hu_as_hu` | 60 | 9.9 | -0.067 | 1.00 | 600 |"

    assert expected_acc_row in rendered_icc, f"Accuracy ICC mismatch"
    assert expected_ai_row in rendered_icc, f"AI ICC mismatch"
    assert expected_hu_row in rendered_icc, f"Human ICC mismatch"
    print("[Check 4.2] Coworker ICC rows match baseline values (-0.071, -0.084, -0.067): PASS")

    # Check report content matches rendered
    report_path = "reports/block4_bucket2_to_bucket3_inferential_report.md"
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    assert expected_alex_row in report_text, f"Alex ICC row missing from report file!"
    assert expected_acc_row in report_text, f"Accuracy ICC row missing from report file!"
    assert expected_ai_row in report_text, f"AI ICC row missing from report file!"
    assert expected_hu_row in report_text, f"Human ICC row missing from report file!"
    print("[Check 4.3] Report file contains exact Appendix A diagnostics: PASS")

    print("TEST 4 PASSED: Appendix A clustering diagnostics strictly verified.\n")

if __name__ == "__main__":
    df = test_1_denominator_masking_and_imputation()
    scored_pairs = test_2_table41_multiple_testing_and_alex_ranks(df)
    test_3_step11_tables_and_subtable_averages(df)
    test_4_appendix_a_diagnostics(df)
    print("=" * 70)
    print("ALL EMPIRICAL CHALLENGE TESTS PASSED (0 FAILURES, 0 REGRESSIONS)")
    print("=" * 70)
