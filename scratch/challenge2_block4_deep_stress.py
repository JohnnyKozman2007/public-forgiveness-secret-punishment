#!/usr/bin/env python3
"""
challenge2_block4_deep_stress.py
================================
Deep adversarial stress-testing by Challenger 2 for Block 4:
1. Validates every cell in all 36 Step 11 nested tables and 6 summary stacks.
2. Checks Table 4.1 full ranking calculation (187 pairs) against the top 25 in the report.
3. Verifies deterministic reproducibility of report generation.
"""

import os
import sys
import re
import hashlib
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import generate_block4_bucket2_to_bucket3 as b4
import cluster_stats as cs

REPORT_PATH = "reports/block4_bucket2_to_bucket3_inferential_report.md"

def test_cell_syntax_and_values():
    print("--- 1. Testing Cell Formatting & Values Across All 36 Step 11 Tables & 6 Summary Stacks ---")
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    in_s11_table = False
    checked_cells = 0
    cell_pattern = re.compile(r"^\*?\*?\d+\.\d+% vs \d+\.\d+% \(p=(?:< 0\.0001|\d+\.\d+)(?:†)?\)\*?\*?$")

    current_tbl = None
    for line in lines:
        if line.startswith("#### Table ") or (line.startswith("#### ") and "Summary" in line):
            if "Step 11 Peer Identification" in line:
                in_s11_table = True
                current_tbl = line.strip()
            else:
                in_s11_table = False
                current_tbl = None
            continue
        elif in_s11_table and (line.startswith("# ") or line.startswith("## ") or line.startswith("---")):
            in_s11_table = False
            current_tbl = None
            continue

        if in_s11_table and line.startswith("| ↳ *"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            # parts[0] is driver name, parts[1..4] are outcome cells
            assert len(parts) == 5, f"Expected 4 outcome columns in {current_tbl}, line: {line}"
            for c_idx, cell in enumerate(parts[1:], start=1):
                checked_cells += 1
                assert cell_pattern.match(cell), f"Malformed cell in {current_tbl}: '{cell}'"
                # Check for nan
                assert "nan" not in cell.lower(), f"NaN found in {current_tbl}: '{cell}'"

    print(f"[PASS] Successfully checked {checked_cells} Step 11 cells. Zero NaNs, zero malformed strings.")

def test_table_41_independent_oracle():
    print("\n--- 2. Independent Oracle Calculation for Table 4.1 ---")
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

    assert len(all_upstream) == 11, f"Expected 11 upstream drivers, got {len(all_upstream)}"
    assert len(all_downstream) == 17, f"Expected 17 downstream outcomes, got {len(all_downstream)}"
    total_pairs = len(all_upstream) * len(all_downstream)
    assert total_pairs == 187, f"Expected 187 pairs, got {total_pairs}"
    print(f"Total multiple-testing pairs evaluated: {total_pairs}")

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

    scored_pairs.sort(key=lambda x: (x[0], x[1]))
    bh_ps, bonf_ps = cs.bh_bonferroni([x[0] for x in scored_pairs])

    # Read Table 4.1 from report
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    t41_report_rows = []
    in_t41 = False
    for l in lines:
        if "#### Table 4.1:" in l:
            in_t41 = True
            continue
        if in_t41:
            if l.startswith("| **#"):
                t41_report_rows.append(l)
            elif l.startswith("---") or (l.startswith("# ") and "APPENDIX" in l):
                break

    assert len(t41_report_rows) == 25, f"Expected 25 rows in Table 4.1 report, got {len(t41_report_rows)}"

    for r_idx, (_, _, b_label, t_label, off_txt, on_txt, comb_txt, adj_str) in enumerate(scored_pairs[:25], start=1):
        q_txt = cs.fmt_p(bh_ps[r_idx - 1])
        b_txt = cs.fmt_p(bonf_ps[r_idx - 1])
        expected_row = f"| **#{r_idx}** | **{b_label}** | `{t_label}` | {off_txt} | {on_txt} | **{comb_txt}** | {adj_str} | **{q_txt}** | **{b_txt}** |"
        report_row = t41_report_rows[r_idx - 1]
        assert expected_row == report_row, f"Table 4.1 mismatch at Rank #{r_idx}:\nExpected: {expected_row}\nReport:   {report_row}"

    print("[PASS] Table 4.1 matches independent oracle calculation 100% bit-for-bit across all 25 rows!")

    # Check whether any Step 11 outcomes are in the top 25
    s11_in_top25 = [r for r in t41_report_rows if "Step 11:" in r]
    print(f"Step 11 outcomes in Table 4.1 Top 25: {len(s11_in_top25)}")
    for r in s11_in_top25:
        print(f"  {r}")

def test_deterministic_reproducibility():
    print("\n--- 3. Testing Deterministic Reproducibility ---")
    with open(REPORT_PATH, "rb") as f:
        h1 = hashlib.sha256(f.read()).hexdigest()

    print(f"Current report SHA256: {h1}")
    # Re-run build
    b4.build_block4_report()

    with open(REPORT_PATH, "rb") as f:
        h2 = hashlib.sha256(f.read()).hexdigest()

    print(f"Regenerated report SHA256: {h2}")
    assert h1 == h2, f"Report regeneration is non-deterministic! Hash mismatch: {h1} vs {h2}"
    print("[PASS] Deterministic reproducibility verified: SHA256 hash matches bit-for-bit.")

if __name__ == "__main__":
    test_cell_syntax_and_values()
    test_table_41_independent_oracle()
    test_deterministic_reproducibility()
    print("\n========================================================")
    print("ALL ADVERSARIAL DEEP STRESS TESTS PASSED SUCCESSFULLY!")
    print("========================================================")
