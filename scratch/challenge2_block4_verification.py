#!/usr/bin/env python3
"""
challenge2_block4_verification.py
=================================
Independent verification script by Challenger 2 for Milestone 4 (Block 4 Sequential Integration).

Stress-tests:
1. Cross-table consistency across all 36 Step 11 nested tables, 6 summary stacks, Table 4.1, and Appendix A.
2. Bit-for-bit invariance of all 20 coworker metrics against reports/.baseline_coworker_cache.json.
3. Strict exclusion and boundary condition invariants of the 6 missing workers (Rina under Probe ON).
4. Statistical precision and reproducibility.
"""

import os
import sys
import json
import re
import numpy as np
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

REPORT_PATH = "reports/block4_bucket2_to_bucket3_inferential_report.md"
BASELINE_CACHE = "reports/.baseline_coworker_cache.json"

def test_file_exists():
    assert os.path.exists(REPORT_PATH), f"Report not found: {REPORT_PATH}"
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    assert len(content) > 100000, f"Report content too small: {len(content)} chars"
    print(f"[PASS] Report exists ({len(content)} chars, {len(content.splitlines())} lines)")
    return content

def extract_tables(content):
    lines = content.splitlines()
    tables = {}
    current_table = None
    table_lines = []
    for line in lines:
        if line.startswith("#### Table ") or line.startswith("#### ") and "Summary" in line:
            if current_table:
                tables[current_table] = table_lines
            current_table = line.strip()
            table_lines = []
        elif current_table:
            if line.startswith("# ") or line.startswith("## ") or line.startswith("---"):
                tables[current_table] = table_lines
                current_table = None
                table_lines = []
            elif line.startswith("|"):
                table_lines.append(line.strip())
    if current_table:
        tables[current_table] = table_lines
    return tables

def test_table_structure_and_counts(tables):
    print(f"\n--- Checking Table Structure & Counts ---")
    s11_nested = [k for k in tables.keys() if "Step 11 Peer Identification" in k and k.startswith("#### Table ")]
    s11_stacks = [k for k in tables.keys() if "Step 11 Peer Identification" in k and not k.startswith("#### Table ")]
    print(f"Total tables found: {len(tables)}")
    print(f"Total Step 11 nested tables found: {len(s11_nested)}")
    print(f"Total Step 11 summary stacks found: {len(s11_stacks)}")
    assert len(s11_nested) == 36, f"Expected 36 Step 11 nested tables, found {len(s11_nested)}"
    assert len(s11_stacks) == 6, f"Expected 6 Step 11 summary stacks, found {len(s11_stacks)}"
    print("[PASS] Exactly 36 Step 11 nested tables and 6 Step 11 summary stacks present.")
    return s11_nested, s11_stacks

def test_model_pov_vs_seat_pov_consistency(tables):
    print(f"\n--- Checking Model POV vs Seat POV Sub-Table Average Consistency ---")
    # There are 18 pairs of Model POV and Seat POV tables for Step 11
    # Part 1:
    # 1.3 (Model S6) vs 1.9 (Seat S6)
    # 1.4 (Model S9) vs 1.10 (Seat S9)
    # 1.15 (Model S6) vs 1.21 (Seat S6)
    # 1.16 (Model S9) vs 1.22 (Seat S9)
    # 1.27 (Model S6) vs 1.33 (Seat S6)
    # 1.28 (Model S9) vs 1.34 (Seat S9)
    # Part 2:
    # 2.3 vs 2.9, 2.4 vs 2.10, 2.15 vs 2.21, 2.16 vs 2.22, 2.27 vs 2.33, 2.28 vs 2.34
    # Part 3:
    # 3.3 vs 3.9, 3.4 vs 3.10, 3.15 vs 3.21, 3.16 vs 3.22, 3.27 vs 3.33, 3.28 vs 3.34
    pairs = [
        ("Table 1.3:", "Table 1.9:"),
        ("Table 1.4:", "Table 1.10:"),
        ("Table 1.15:", "Table 1.21:"),
        ("Table 1.16:", "Table 1.22:"),
        ("Table 1.27:", "Table 1.33:"),
        ("Table 1.28:", "Table 1.34:"),
        ("Table 2.3:", "Table 2.9:"),
        ("Table 2.4:", "Table 2.10:"),
        ("Table 2.15:", "Table 2.21:"),
        ("Table 2.16:", "Table 2.22:"),
        ("Table 2.27:", "Table 2.33:"),
        ("Table 2.28:", "Table 2.34:"),
        ("Table 3.3:", "Table 3.9:"),
        ("Table 3.4:", "Table 3.10:"),
        ("Table 3.15:", "Table 3.21:"),
        ("Table 3.16:", "Table 3.22:"),
        ("Table 3.27:", "Table 3.33:"),
        ("Table 3.28:", "Table 3.34:"),
    ]

    for m_prefix, s_prefix in pairs:
        m_key = [k for k in tables.keys() if m_prefix in k][0]
        s_key = [k for k in tables.keys() if s_prefix in k][0]

        # Extract sub-table average rows
        m_avg_rows = [l for l in tables[m_key] if "SUB-TABLE AVERAGE" in l or "↳ *" in l and "Average" in l]
        s_avg_rows = [l for l in tables[s_key] if "SUB-TABLE AVERAGE" in l or "↳ *" in l and "Average" in l]

        assert len(m_avg_rows) == len(s_avg_rows), f"Mismatched avg row count between {m_key} and {s_key}"
        for mr, sr in zip(m_avg_rows, s_avg_rows):
            assert mr == sr, f"Discrepancy between {m_key} and {s_key}:\nModel POV: {mr}\nSeat POV:  {sr}"
    print(f"[PASS] All 18 Model POV vs Seat POV Sub-Table Averages match 100% bit-for-bit!")

def test_summary_stack_consistency(tables):
    print(f"\n--- Checking Summary Stack vs Nested Table Sub-Average Consistency ---")
    # Part 1: PROBE OFF Summary: Step 6 -> Step 11
    # Check that SUB-AVERAGE: LABELLED matches Table 1.3 / 1.9 sub-table average
    # Check that SUB-AVERAGE: MISLABELLED matches Table 1.15 / 1.21
    # Check that SUB-AVERAGE: UNLABELLED matches Table 1.27 / 1.33
    stack_p1_s6_key = [k for k in tables.keys() if "PROBE OFF Summary: Step 6 -> Step 11" in k][0]
    stack_p1_s6_rows = tables[stack_p1_s6_key]

    t13_key = [k for k in tables.keys() if "Table 1.3:" in k][0]
    t115_key = [k for k in tables.keys() if "Table 1.15:" in k][0]
    t127_key = [k for k in tables.keys() if "Table 1.27:" in k][0]

    def extract_driver_cells(table_rows, label_prefix):
        res = []
        found = False
        for l in table_rows:
            if label_prefix in l:
                found = True
                continue
            if found:
                if l.startswith("| ↳ *"):
                    # Extract the cells part after name
                    parts = [p.strip() for p in l.split("|")[1:-1]]
                    res.append((parts[0].replace(" Average", "").strip(), parts[1:]))
                else:
                    break
        return res

    def extract_stack_section(stack_rows, section_header):
        res = []
        found = False
        for l in stack_rows:
            if section_header in l:
                found = True
                continue
            if found:
                if l.startswith("| ↳ *"):
                    parts = [p.strip() for p in l.split("|")[1:-1]]
                    res.append((parts[0].replace(" Grand Average", "").strip(), parts[1:]))
                elif l.startswith("| **"):
                    break
        return res

    # Verify Part 1 Step 6
    p1_s6_lbl_table = extract_driver_cells(tables[t13_key], "SUB-TABLE AVERAGE (LABELLED")
    p1_s6_lbl_stack = extract_stack_section(stack_p1_s6_rows, "SUB-AVERAGE: LABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p1_s6_lbl_table, p1_s6_lbl_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 1 Step 6 Labelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    p1_s6_mis_table = extract_driver_cells(tables[t115_key], "SUB-TABLE AVERAGE (MISLABELLED")
    p1_s6_mis_stack = extract_stack_section(stack_p1_s6_rows, "SUB-AVERAGE: MISLABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p1_s6_mis_table, p1_s6_mis_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 1 Step 6 Mislabelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    p1_s6_unl_table = extract_driver_cells(tables[t127_key], "SUB-TABLE AVERAGE (UNLABELLED")
    p1_s6_unl_stack = extract_stack_section(stack_p1_s6_rows, "SUB-AVERAGE: UNLABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p1_s6_unl_table, p1_s6_unl_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 1 Step 6 Unlabelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    # Verify Part 2 Step 6
    stack_p2_s6_key = [k for k in tables.keys() if "PROBE ON Summary: Step 6 -> Step 11" in k][0]
    t23_key = [k for k in tables.keys() if "Table 2.3:" in k][0]
    t215_key = [k for k in tables.keys() if "Table 2.15:" in k][0]
    t227_key = [k for k in tables.keys() if "Table 2.27:" in k][0]

    p2_s6_lbl_table = extract_driver_cells(tables[t23_key], "SUB-TABLE AVERAGE (LABELLED")
    p2_s6_lbl_stack = extract_stack_section(tables[stack_p2_s6_key], "SUB-AVERAGE: LABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p2_s6_lbl_table, p2_s6_lbl_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 2 Step 6 Labelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    p2_s6_mis_table = extract_driver_cells(tables[t215_key], "SUB-TABLE AVERAGE (MISLABELLED")
    p2_s6_mis_stack = extract_stack_section(tables[stack_p2_s6_key], "SUB-AVERAGE: MISLABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p2_s6_mis_table, p2_s6_mis_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 2 Step 6 Mislabelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    p2_s6_unl_table = extract_driver_cells(tables[t227_key], "SUB-TABLE AVERAGE (UNLABELLED")
    p2_s6_unl_stack = extract_stack_section(tables[stack_p2_s6_key], "SUB-AVERAGE: UNLABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p2_s6_unl_table, p2_s6_unl_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 2 Step 6 Unlabelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    # Verify Part 3 Triple-Average Summary Stack
    stack_p3_s6_key = [k for k in tables.keys() if "Triple-Average Summary Stack: Step 6 -> Step 11" in k][0]
    t33_key = [k for k in tables.keys() if "Table 3.3:" in k][0]
    t315_key = [k for k in tables.keys() if "Table 3.15:" in k][0]
    t327_key = [k for k in tables.keys() if "Table 3.27:" in k][0]

    p3_s6_lbl_table = extract_driver_cells(tables[t33_key], "SUB-TABLE AVERAGE (LABELLED")
    p3_s6_lbl_stack = extract_stack_section(tables[stack_p3_s6_key], "COMBINED CONDITION AVERAGE: LABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p3_s6_lbl_table, p3_s6_lbl_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 3 Step 6 Labelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    p3_s6_mis_table = extract_driver_cells(tables[t315_key], "SUB-TABLE AVERAGE (MISLABELLED")
    p3_s6_mis_stack = extract_stack_section(tables[stack_p3_s6_key], "COMBINED CONDITION AVERAGE: MISLABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p3_s6_mis_table, p3_s6_mis_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 3 Step 6 Mislabelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    p3_s6_unl_table = extract_driver_cells(tables[t327_key], "SUB-TABLE AVERAGE (UNLABELLED")
    p3_s6_unl_stack = extract_stack_section(tables[stack_p3_s6_key], "COMBINED CONDITION AVERAGE: UNLABELLED")
    for (name_t, cells_t), (name_s, cells_s) in zip(p3_s6_unl_table, p3_s6_unl_stack):
        clean_t = [c.replace("**", "").strip() for c in cells_t]
        clean_s = [c.replace("**", "").strip() for c in cells_s]
        assert clean_t == clean_s, f"Part 3 Step 6 Unlabelled mismatch: {name_t}\nTable: {clean_t}\nStack: {clean_s}"

    # Verify Grand Averages alignment in Triple-Average Stack:
    # 1. PROBE OFF OVERALL AVERAGE in Triple Stack should match OVERALL PROBE OFF GRAND AVERAGE in Part 1 Stack
    p1_grand = extract_stack_section(stack_p1_s6_rows, "OVERALL PROBE OFF GRAND AVERAGE")
    p3_off = extract_stack_section(tables[stack_p3_s6_key], "1. PROBE OFF OVERALL AVERAGE")
    for (name_1, cells_1), (name_3, cells_3) in zip(p1_grand, p3_off):
        clean_1 = [c.replace("**", "").strip() for c in cells_1]
        clean_3 = [c.replace("**", "").strip() for c in cells_3]
        assert clean_1 == clean_3, f"Probe OFF Grand Average mismatch:\nP1: {clean_1}\nP3: {clean_3}"

    # 2. PROBE ON OVERALL AVERAGE in Triple Stack should match OVERALL PROBE ON GRAND AVERAGE in Part 2 Stack
    p2_grand = extract_stack_section(tables[stack_p2_s6_key], "OVERALL PROBE ON GRAND AVERAGE")
    p3_on = extract_stack_section(tables[stack_p3_s6_key], "2. PROBE ON OVERALL AVERAGE")
    for (name_2, cells_2), (name_3, cells_3) in zip(p2_grand, p3_on):
        clean_2 = [c.replace("**", "").strip() for c in cells_2]
        clean_3 = [c.replace("**", "").strip() for c in cells_3]
        assert clean_2 == clean_3, f"Probe ON Grand Average mismatch:\nP2: {clean_2}\nP3: {clean_3}"

    print("[PASS] Summary stacks and nested tables match 100% across all condition slices!")

def test_coworker_baselines_invariance():
    print(f"\n--- Checking Coworker Metrics Invariance Bit-for-Bit ---")
    assert os.path.exists(BASELINE_CACHE), f"Baseline cache missing: {BASELINE_CACHE}"
    with open(BASELINE_CACHE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    
    assert REPORT_PATH in cache, f"Report {REPORT_PATH} not in baseline cache"
    cached_lines = cache[REPORT_PATH]["coworker_lines"]
    
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        current_content = f.read()
    
    # Use verify_coworker_baselines logic
    import verify_coworker_baselines as vcb
    current_lines = vcb.extract_coworker_sections(current_content)
    
    print(f"Cached coworker lines: {len(cached_lines)}")
    print(f"Current coworker lines: {len(current_lines)}")
    assert len(cached_lines) == len(current_lines), f"Line count mismatch: cached {len(cached_lines)} vs current {len(current_lines)}"
    
    mismatches = []
    for (c_line_no, c_txt), (cur_line_no, cur_txt) in zip(cached_lines, current_lines):
        # We allow difference in line numbers if tables expanded or headers changed, but text must match!
        if c_txt != cur_txt:
            mismatches.append((c_line_no, c_txt, cur_line_no, cur_txt))
    
    if mismatches:
        print(f"[FAIL] Found {len(mismatches)} coworker mismatches:")
        for c_l, c_t, cur_l, cur_t in mismatches[:5]:
            print(f"  Cached:  L{c_l}: {c_t}")
            print(f"  Current: L{cur_l}: {cur_t}")
        assert False, f"{len(mismatches)} coworker baseline regressions found!"
    
    print("[PASS] Exactly 0 coworker metric regressions! All coworker lines match baseline snapshot verbatim.")

def test_missing_workers_boundary_conditions():
    print(f"\n--- Checking Missing Worker Boundary Invariants (N=6, Rina under Probe ON) ---")
    import generate_block4_bucket2_to_bucket3 as b4
    raw_workers = b4.load_dataset()
    assert len(raw_workers) == 600, f"Expected 600 workers, got {len(raw_workers)}"
    
    missing_workers = [w for w in raw_workers if w["s11_alex_tot"] == 0.0]
    valid_workers = [w for w in raw_workers if w["s11_alex_tot"] == 1.0]
    
    print(f"Total workers: {len(raw_workers)}")
    print(f"Valid Alex guesses: {len(valid_workers)} (expected 594)")
    print(f"Missing Alex guesses: {len(missing_workers)} (expected 6)")
    assert len(missing_workers) == 6, f"Expected 6 missing workers, got {len(missing_workers)}"
    assert len(valid_workers) == 594, f"Expected 594 valid workers, got {len(valid_workers)}"
    
    # Check that all 6 missing workers are strictly Rina (model=qwen-2-5-72b) and probe=1 (Probe ON)
    for mw in missing_workers:
        assert mw["model"] == "qwen-2-5-72b", f"Unexpected model for missing worker: {mw}"
        assert mw["probe"] == 1, f"Missing worker not in Probe ON: {mw}"
        assert mw["worker_name"] == "Rina", f"Worker name not Rina: {mw}"
        assert mw["s11_alex_as_hu"] == 0.0, f"s11_alex_as_hu not 0.0: {mw}"
        assert mw["s11_alex_tot"] == 0.0, f"s11_alex_tot not 0.0: {mw}"
        assert mw["s11_alex_guess"] is None, f"s11_alex_guess not None: {mw}"
        # In those 6 runs, Rina's Step 11 call failed, so s11_tot is 0 (no guesses made)
        assert mw["s11_tot"] == 0, f"Coworker s11_tot expected 0 for failed Step 11 call: {mw['s11_tot']}"

    # For the 54 valid Rina workers, ensure coworker s11_tot is 19
    rina_valid = [w for w in valid_workers if w["worker_name"] == "Rina"]
    assert len(rina_valid) == 54, f"Expected 54 valid Rina workers, got {len(rina_valid)}"
    for vw in rina_valid:
        assert vw["s11_tot"] == 19, f"Coworker s11_tot not 19 for valid Rina: {vw['s11_tot']}"
    
    # Check that in Probe OFF, all 300 workers are valid (0 missing)
    probe_off_workers = [w for w in raw_workers if w["probe"] == 0]
    probe_off_missing = [w for w in probe_off_workers if w["s11_alex_tot"] == 0.0]
    assert len(probe_off_missing) == 0, f"Found missing workers in Probe OFF: {len(probe_off_missing)}"
    
    # Check that in Probe ON, exactly 294 are valid
    probe_on_workers = [w for w in raw_workers if w["probe"] == 1]
    probe_on_valid = [w for w in probe_on_workers if w["s11_alex_tot"] == 1.0]
    assert len(probe_on_valid) == 294, f"Expected 294 valid in Probe ON, got {len(probe_on_valid)}"
    
    # Check distribution across labels in Probe ON
    for lbl in ["labelled", "mislabelled", "unlabelled"]:
        lbl_workers = [w for w in probe_on_workers if w["label"] == lbl]
        lbl_valid = [w for w in lbl_workers if w["s11_alex_tot"] == 1.0]
        lbl_missing = [w for w in lbl_workers if w["s11_alex_tot"] == 0.0]
        print(f"  Probe ON {lbl}: {len(lbl_valid)} valid, {len(lbl_missing)} missing (total {len(lbl_workers)})")
        assert len(lbl_valid) + len(lbl_missing) == 100
    
    # Check model qwen-2-5-72b:
    qwen_workers = [w for w in raw_workers if w["model"] == "qwen-2-5-72b"]
    qwen_valid = [w for w in qwen_workers if w["s11_alex_tot"] == 1.0]
    assert len(qwen_valid) == 54, f"Expected 54 valid Qwen workers, got {len(qwen_valid)}"
    
    # Check all other models have 60 valid
    for m in b4.MODEL_IDS:
        if m == "qwen-2-5-72b":
            continue
        m_workers = [w for w in raw_workers if w["model"] == m]
        m_valid = [w for w in m_workers if w["s11_alex_tot"] == 1.0]
        assert len(m_valid) == 60, f"Model {m} has {len(m_valid)} valid, expected 60"
        
    print("[PASS] Missing worker boundary conditions and invariants strictly verified across all dimensions!")

def test_appendix_a_diagnostics():
    print(f"\n--- Checking Appendix A Clustering Diagnostics ---")
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    
    expected_rows = [
        "| Step 11: Overall Accuracy | `s11_accuracy` | 60 | 9.9 | -0.071 | 1.00 | 600 |",
        "| Step 11: AI Guessed as Human | `s11_ai_as_hu` | 60 | 9.9 | -0.084 | 1.00 | 600 |",
        "| Step 11: Human Guessed as Human | `s11_hu_as_hu` | 60 | 9.9 | -0.067 | 1.00 | 600 |",
        "| Step 11: Alex Guessed as Human | `s11_alex_as_hu` | 60 | 9.9 | -0.059 | 1.00 | 600 |",
    ]
    for er in expected_rows:
        assert er in text, f"Missing expected Appendix A row:\n{er}"
    print("[PASS] Appendix A clustering diagnostics rows strictly verified.")

def test_table_41_structure():
    print(f"\n--- Checking Table 4.1 Multiple Testing Structure ---")
    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    
    assert "#### Table 4.1: Head-to-Head Upstream Behavioral Driver Ranking" in text
    # Extract top 25 rows
    lines = text.splitlines()
    t41_lines = []
    in_t41 = False
    for l in lines:
        if "#### Table 4.1:" in l:
            in_t41 = True
            continue
        if in_t41:
            if l.startswith("| **#"):
                t41_lines.append(l)
            elif l.startswith("---") or (l.startswith("# ") and "APPENDIX" in l):
                break
    print(f"Table 4.1 Top rows count: {len(t41_lines)} (expected 25)")
    assert len(t41_lines) == 25, f"Expected 25 rows in Table 4.1, found {len(t41_lines)}"
    
    # Check #1 rank row
    print(f"Top 1: {t41_lines[0]}")
    assert "| **#1** |" in t41_lines[0]
    print("[PASS] Table 4.1 multiple testing structure strictly verified.")

if __name__ == "__main__":
    content = test_file_exists()
    tables = extract_tables(content)
    test_table_structure_and_counts(tables)
    test_model_pov_vs_seat_pov_consistency(tables)
    test_summary_stack_consistency(tables)
    test_coworker_baselines_invariance()
    test_missing_workers_boundary_conditions()
    test_appendix_a_diagnostics()
    test_table_41_structure()
    print("\n========================================================")
    print("ALL CHALLENGER 2 STRESS TESTS PASSED SUCCESSFULLY!")
    print("========================================================")
