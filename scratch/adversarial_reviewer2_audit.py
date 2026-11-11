#!/usr/bin/env python3
"""
Adversarial Reviewer 2 Audit Script for Milestone 4:
Block 4 Sequential Integration (`generate_block4_bucket2_to_bucket3.py`).
"""

import ast
import json
import os
import re
import sys
import os
sys.path.insert(0, os.path.abspath("."))
import numpy as np
import pandas as pd

import cluster_stats as cs
import generate_block4_bucket2_to_bucket3 as b4

def test_ast_integrity():
    print("=== 1. AST AND INTEGRITY AUDIT ===")
    src_file = "generate_block4_bucket2_to_bucket3.py"
    with open(src_file, "r", encoding="utf-8") as f:
        src = f.read()

    tree = ast.parse(src)
    # Check for suspicious hardcoded literals in return statements or functions
    suspicious = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ("bh_ps", "bonf_ps", "scored_pairs"):
                    if isinstance(node.value, (ast.List, ast.Tuple)) and len(node.value.elts) > 0:
                        suspicious.append(f"Hardcoded list/dict assignment to {target.id}")
                    elif isinstance(node.value, ast.Dict) and len(node.value.keys) > 0:
                        suspicious.append(f"Hardcoded dict assignment to {target.id}")
    
    assert len(suspicious) == 0, f"Found suspicious assignments: {suspicious}"
    print("[PASS] AST check: No hardcoded output tables, rankings, or FDR arrays found.")

def test_missing_data_and_denominators():
    print("\n=== 2. MISSING DATA & DENOMINATOR AUDIT ===")
    raw_workers = b4.load_dataset()
    assert len(raw_workers) == 600, f"Expected 600 raw workers, got {len(raw_workers)}"

    df = pd.DataFrame([b4.extract_worker_metrics(w) for w in raw_workers])
    assert len(df) == 600, f"Expected 600 df rows, got {len(df)}"

    # Check Alex metrics
    n_valid_alex = (df["s11_alex_tot"] == 1.0).sum()
    n_missing_alex = (df["s11_alex_tot"] == 0.0).sum()
    print(f"Alex valid count: {n_valid_alex}, missing count: {n_missing_alex}")
    assert n_valid_alex == 594, f"Expected 594 valid Alex, got {n_valid_alex}"
    assert n_missing_alex == 6, f"Expected 6 missing Alex, got {n_missing_alex}"

    # Verify missing records
    missing_df = df[df["s11_alex_tot"] == 0.0]
    assert (missing_df["s11_alex_as_hu"] == 0.0).all(), "Missing Alex records have non-zero s11_alex_as_hu"
    assert (missing_df["probe"] == 1).all(), "Missing Alex records are not all Probe ON"
    assert (missing_df["model"] == "qwen-2-5-72b").all(), "Missing Alex records are not all qwen-2-5-72b"
    print(f"Missing Alex records seats: {missing_df['seat'].tolist()}")

    # Verify coworker counts: 19 for valid Step 11 workers, 0 for the 6 missing Step 11 workers
    assert (df[df["s11_alex_tot"] == 1.0]["s11_tot"] == 19).all(), "Valid Step 11 workers do not all have s11_tot == 19"
    assert (df[df["s11_alex_tot"] == 0.0]["s11_tot"] == 0).all(), "Missing Step 11 workers do not have s11_tot == 0"
    assert (df[df["s11_alex_tot"] == 1.0]["s11_ai_tot"] == 9).all()
    assert (df[df["s11_alex_tot"] == 1.0]["s11_hu_tot"] == 10).all()

    # Verify pooled percentage of Alex
    k_alex = df["s11_alex_as_hu"].sum() # since each valid has s11_alex_tot == 1.0 and s11_alex_hu == 1.0
    # or using the count map:
    cor_c, tot_c = b4.S11_COUNT_MAP["s11_alex_as_hu"]
    k_alex_cnt = df[cor_c].sum()
    tot_alex_cnt = df[tot_c].sum()
    print(f"Alex Human guesses: {k_alex_cnt} / {tot_alex_cnt} = {k_alex_cnt / tot_alex_cnt * 100.0:.4f}%")
    assert tot_alex_cnt == 594.0
    assert k_alex_cnt == 384.0
    print("[PASS] Missing data uniformity: N=594 valid, N=6 missing (all Rina Probe ON), coworker metrics intact at N=600.")

def test_zero_division_and_adversarial_slices():
    print("\n=== 3. ZERO-DIVISION & ADVERSARIAL SLICE AUDIT ===")
    raw_workers = b4.load_dataset()
    df = pd.DataFrame([b4.extract_worker_metrics(w) for w in raw_workers])

    # Case A: Empty dataframe
    empty_df = df.iloc[0:0].copy()
    r1, r0, p_val, flag, res = b4.calc_col_stats(empty_df, "s6_organize", "s11_alex_as_hu")
    assert r1 == 0.0 and r0 == 0.0 and p_val == 1.0, f"Empty df failed: {r1}, {r0}, {p_val}"

    # Case B: All workers have s11_alex_tot == 0 (e.g. only the 6 missing workers)
    missing_only_df = df[df["s11_alex_tot"] == 0.0].copy()
    r1, r0, p_val, flag, res = b4.calc_col_stats(missing_only_df, "s6_organize", "s11_alex_as_hu")
    assert r1 == 0.0 and r0 == 0.0, f"Missing-only slice failed: {r1}, {r0}"

    # Case C: Single-model slice where all workers voted the same (e.g., pos_df or neg_df is empty)
    single_model = df[df["model"] == "nemotron-3-5"]
    r1, r0, p_val, flag, res = b4.calc_col_stats(single_model, "s6_organize", "s11_alex_as_hu")
    assert not np.isnan(r1) and not np.isnan(r0) and not np.isnan(p_val)
    print(f"Nemotron s6_organize -> s11_alex_as_hu: {r1:.1f}% vs {r0:.1f}%, p={p_val}")

    # Case D: Synthetic dataframe with NaN, inf, or unexpected types
    syn_df = pd.DataFrame({
        "bname": ["run1", "run2"],
        "model": ["m1", "m2"],
        "seat": [1, 2],
        "label": ["labelled", "labelled"],
        "probe": [0, 0],
        "s6_organize": [1, 0],
        "s11_alex_as_hu": [0.0, 0.0],
        "s11_alex_tot": [0.0, 0.0],
    })
    r1, r0, p_val, flag, res = b4.calc_col_stats(syn_df, "s6_organize", "s11_alex_as_hu")
    assert r1 == 0.0 and r0 == 0.0 and p_val == 1.0

    print("[PASS] Zero-division handling: Handled safely in all degenerate/boundary slices.")

def test_part3_uncollapsed_architecture():
    print("\n=== 4. PART 3 UNCOLLAPSED ARCHITECTURE AUDIT ===")
    raw_workers = b4.load_dataset()
    df = pd.DataFrame([b4.extract_worker_metrics(w) for w in raw_workers])

    # Check Part 3 tables in the generated report
    with open("reports/block4_bucket2_to_bucket3_inferential_report.md", "r", encoding="utf-8") as f:
        report_text = f.read()

    # Part 3 heading
    assert "# PART 3: COMBINED BOTH AVERAGED (Full Dataset, N = 600 Workers Across 60 Runs)" in report_text
    
    # Check that Tables 3.1 to 3.36 all exist and specify N = 200 (since 200 per label across 60 runs)
    for t_idx in range(1, 37):
        assert f"#### Table 3.{t_idx}:" in report_text, f"Missing Table 3.{t_idx}"
        # Each condition table has N = 200 (labelled, mislabelled, unlabelled: 200 each, total 600)
        match = re.search(rf"#### Table 3\.{t_idx}:.*\(N = (\d+)\)", report_text)
        assert match is not None, f"Table 3.{t_idx} missing N count in title"
        n_count = int(match.group(1))
        assert n_count == 200, f"Table 3.{t_idx} has N = {n_count}, expected 200"

    # Check Triple-Average Summary Stacks
    assert "Triple-Average Summary Stack: Step 6 -> Step 11 Peer Identification" in report_text
    assert "Triple-Average Summary Stack: Step 9 -> Step 11 Peer Identification" in report_text
    assert "3. META GRAND AVERAGE (ALL COMBINED, N=600)" in report_text

    print("[PASS] Part 3 uncollapsed architecture: N=600 pooled across all 60 runs, 36 condition tables (N=200 each), complete triple-average summary stack.")

def test_table41_multiple_testing_and_fdr():
    print("\n=== 5. TABLE 4.1 MULTIPLE TESTING & FDR AUDIT ===")
    raw_workers = b4.load_dataset()
    df = pd.DataFrame([b4.extract_worker_metrics(w) for w in raw_workers])
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

    assert len(all_upstream) == 11, f"Expected 11 upstream actions, got {len(all_upstream)}"
    assert len(all_downstream) == 17, f"Expected 17 downstream outcomes, got {len(all_downstream)}"
    m_family = len(all_upstream) * len(all_downstream)
    print(f"Total hypothesis testing family size M = {len(all_upstream)} x {len(all_downstream)} = {m_family}")
    assert m_family == 187, f"Expected M=187, got {m_family}"

    def fmt_shift_cell(sub_df, act_c, out_c):
        r1, r0, pv, flag, res = b4.calc_col_stats(sub_df, act_c, out_c)
        sh = r1 - r0
        adj_c = res["coef"] * 100.0 if not np.isnan(res["coef"]) else np.nan
        ci_txt = cs.fmt_ci(res["lo"], res["hi"], scale=100.0)
        adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
        return sh, pv, f"{sh:+.1f}% ({r1:.1f}% vs {r0:.1f}%, p={cs.fmt_p(pv, flag)})", adj_str

    scored_pairs = []
    for b_label, act_c in all_upstream:
        for t_label, out_c in all_downstream:
            _, _, off_txt, _ = fmt_shift_cell(df_off, act_c, out_c)
            _, _, on_txt, _ = fmt_shift_cell(df_on, act_c, out_c)
            sh_c, pv_c, comb_txt, adj_str = fmt_shift_cell(df, act_c, out_c)
            scored_pairs.append((pv_c, -abs(sh_c), b_label, t_label, off_txt, on_txt, comb_txt, adj_str))

    assert len(scored_pairs) == 187

    scored_pairs.sort(key=lambda x: (x[0], x[1]))
    bh_ps, bonf_ps = cs.bh_bonferroni([x[0] for x in scored_pairs])
    assert len(bh_ps) == 187
    assert len(bonf_ps) == 187

    # Check monotonicity of FDR
    assert np.all(np.diff(bh_ps) >= -1e-12), "BH-FDR q-values are not monotonically non-decreasing!"

    # Locate all Alex pairs and inspect their ranks
    alex_ranks = []
    for r_idx, x in enumerate(scored_pairs, start=1):
        if "Alex Guessed as Human" in x[3]:
            alex_ranks.append((r_idx, x[2], x[3], x[0], bh_ps[r_idx - 1]))

    print(f"Number of Alex pairs in Table 4.1: {len(alex_ranks)}")
    assert len(alex_ranks) == 11, f"Expected 11 Alex pairs, got {len(alex_ranks)}"
    print("Alex pair ranks and p-values:")
    for r_idx, u_act, d_out, p_val, q_val in alex_ranks:
        print(f"  Rank #{r_idx}: {u_act} -> {d_out} (p={p_val:.4f}, q={q_val:.4f})")

    min_alex_rank = min(r[0] for r in alex_ranks)
    print(f"Highest ranking Alex pair is at Rank #{min_alex_rank}")
    assert min_alex_rank > 25, f"Alex pair entered top 25 at rank {min_alex_rank}!"

    # Verify that the Top 25 rows in report match scored_pairs[:25]
    with open("reports/block4_bucket2_to_bucket3_inferential_report.md", "r", encoding="utf-8") as f:
        lines = f.readlines()

    t41_lines = []
    capture = False
    for line in lines:
        if "#### Table 4.1:" in line:
            capture = True
            continue
        if capture:
            if line.startswith("| **#"):
                t41_lines.append(line.strip())
            elif line.startswith("---") or (line.startswith("#") and "APPENDIX" in line):
                break

    assert len(t41_lines) == 25, f"Expected 25 rows in Table 4.1, found {len(t41_lines)}"
    for idx, (row_str, sp) in enumerate(zip(t41_lines, scored_pairs[:25]), start=1):
        assert f"| **#{idx}** |" in row_str
        assert sp[2] in row_str
        assert sp[3] in row_str
        # Check q-value
        q_exp = cs.fmt_p(bh_ps[idx - 1])
        assert q_exp in row_str

    print("[PASS] Table 4.1 Multiple Testing & FDR: M=187 family size, BH-FDR monotonic, top 25 invariant (highest Alex rank is > 25).")

def test_report_structure_and_column_counts():
    print("\n=== 6. REPORT STRUCTURE & COLUMN COUNT AUDIT ===")
    with open("reports/block4_bucket2_to_bucket3_inferential_report.md", "r", encoding="utf-8") as f:
        report_lines = f.readlines()

    print(f"Total lines in report: {len(report_lines)}")
    assert len(report_lines) in (9044, 9045), f"Expected 9044/9045 lines, got {len(report_lines)}"

    # Audit all Markdown tables in the report for column consistency
    table_count = 0
    in_table = False
    expected_cols = 0
    table_header = ""

    for line_num, line in enumerate(report_lines, start=1):
        sline = line.strip()
        if sline.startswith("|") and sline.endswith("|"):
            parts = [p.strip() for p in sline.split("|")[1:-1]]
            if not in_table:
                # Table Header
                in_table = True
                expected_cols = len(parts)
                table_count += 1
                table_header = sline
            elif set(sline) <= set("|-: "):
                # Table Separator
                assert len(parts) == expected_cols, f"Separator mismatch at line {line_num}: header has {expected_cols}, separator has {len(parts)}"
            else:
                # Table Data Row
                assert len(parts) == expected_cols, f"Row mismatch at line {line_num} in table '{table_header}': expected {expected_cols}, got {len(parts)}: {sline}"
        else:
            in_table = False

    print(f"Audited {table_count} tables across {len(report_lines)} lines. Zero column count mismatches.")
    assert table_count >= 120, f"Expected at least 120 tables, found {table_count}"
    print("[PASS] Markdown table formatting and column counts are 100% consistent.")

if __name__ == "__main__":
    test_ast_integrity()
    test_missing_data_and_denominators()
    test_zero_division_and_adversarial_slices()
    test_part3_uncollapsed_architecture()
    test_table41_multiple_testing_and_fdr()
    test_report_structure_and_column_counts()
    print("\nALL ADVERSARIAL REVIEW CHECKS PASSED SUCCESSFULLY!")
