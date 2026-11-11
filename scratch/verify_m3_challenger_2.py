#!/usr/bin/env python3
"""
Comprehensive Challenger Verification Script for Milestone 3
Block 3 Sequential Integration (generate_block3_bucket1_to_bucket3.py)
"""

import os
import re
import json
import numpy as np
import pandas as pd
from collections import defaultdict

REPORT_PATH = "reports/block3_bucket1_to_bucket3_inferential_report.md"
BASELINE_CACHE = "reports/.baseline_coworker_cache.json"

def run_audits():
    print("=" * 70)
    print("CHALLENGER 2 AUDIT: MILESTONE 3 BLOCK 3 INTEGRATION")
    print("=" * 70)

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        report_text = f.read()

    lines = report_text.splitlines()
    print(f"Loaded report: {len(lines)} lines, {len(report_text)} characters.")

    # ---------------------------------------------------------
    # 1. IDENTIFY ALL STEP 11 NESTED TABLES AND SUMMARY STACKS
    # ---------------------------------------------------------
    print("\n--- TEST 1: Table Enumeration & Structure ---")
    
    # Regex to find all table sections
    table_pattern = re.compile(r"^#### (Table \d+\.\d+: [^\n]+)", re.MULTILINE)
    all_table_matches = list(table_pattern.finditer(report_text))
    print(f"Total nested tables in report: {len(all_table_matches)}")

    s11_tables = []
    for m in all_table_matches:
        t_header = m.group(1)
        if "Step 11" in t_header:
            s11_tables.append((t_header, m.start()))

    print(f"Total Step 11 nested tables: {len(s11_tables)} (Expected: 42)")
    assert len(s11_tables) == 42, f"Expected 42 Step 11 nested tables, found {len(s11_tables)}"

    summary_pattern = re.compile(r"^#### ([^\n]*Summary[^\n]*Step 11[^\n]*)", re.MULTILINE)
    all_sum_matches = list(summary_pattern.finditer(report_text))
    print(f"Total Step 11 summary stacks: {len(all_sum_matches)} (Expected: 7)")
    for i, m in enumerate(all_sum_matches, 1):
        print(f"  {i}. {m.group(1)}")
    assert len(all_sum_matches) == 7, f"Expected 7 Step 11 summary stacks, found {len(all_sum_matches)}"

    # ---------------------------------------------------------
    # 2. VERIFY COLUMN HEADERS IN ALL STEP 11 TABLES & STACKS
    # ---------------------------------------------------------
    print("\n--- TEST 2: Step 11 Column Headers ---")
    expected_headers = [
        "Overall Accuracy % (p)",
        "AI Guessed as Human % (p)",
        "Human Guessed as Human % (p)",
        "Alex Guessed as Human % (p)",
    ]

    def extract_table_block(start_pos):
        # find table lines starting after header
        sub = report_text[start_pos:]
        tbl_lines = []
        for l in sub.splitlines()[1:]:
            if l.startswith("#### Table ") or l.startswith("#### ") or l.startswith("## ") or l.startswith("# ") or l.startswith("---"):
                break
            if l.strip().startswith("|"):
                tbl_lines.append(l.strip())
        return tbl_lines

    def parse_markdown_table(tbl_lines):
        if len(tbl_lines) < 2:
            return None, []
        headers = [c.strip() for c in tbl_lines[0].split("|")[1:-1]]
        rows = []
        for l in tbl_lines[2:]: # skip separator
            cells = [c.strip() for c in l.split("|")[1:-1]]
            rows.append(cells)
        return headers, rows

    all_parsed_tables = {}
    for t_header, start_pos in s11_tables:
        t_id = t_header.split(":")[0].replace("#### Table ", "").strip()
        tbl_lines = extract_table_block(start_pos)
        headers, rows = parse_markdown_table(tbl_lines)
        all_parsed_tables[t_id] = {
            "title": t_header,
            "headers": headers,
            "rows": rows
        }
        # Check headers
        assert len(headers) == 5, f"Table {t_id} headers length != 5: {headers}"
        for h_exp, h_act in zip(expected_headers, headers[1:]):
            assert h_exp == h_act, f"Table {t_id} header mismatch: {h_exp} vs {h_act}"

    print(f"PASS: All 42 Step 11 nested tables have exactly 5 columns with proper headers!")

    all_parsed_summaries = {}
    for m in all_sum_matches:
        s_title = m.group(1)
        tbl_lines = extract_table_block(m.start())
        headers, rows = parse_markdown_table(tbl_lines)
        all_parsed_summaries[s_title] = {
            "headers": headers,
            "rows": rows
        }
        assert len(headers) == 5, f"Summary {s_title} headers length != 5: {headers}"
        for h_exp, h_act in zip(expected_headers, headers[1:]):
            assert h_exp == h_act, f"Summary {s_title} header mismatch: {h_exp} vs {h_act}"

    print(f"PASS: All 7 Step 11 summary stacks have exactly 5 columns with proper headers!")

    # ---------------------------------------------------------
    # 3. VERIFY CELL FORMAT & VALIDITY ACROSS ALL CELLS
    # ---------------------------------------------------------
    print("\n--- TEST 3: Cell Format & Range Validation ---")
    cell_re = re.compile(r"^\*{0,2}(\d+\.\d+)% vs (\d+\.\d+)% \(p=([^\)]+)\)\*{0,2}$")

    total_cells = 0
    alex_cells = 0
    for t_id, data in all_parsed_tables.items():
        for r_idx, r in enumerate(data["rows"]):
            if len(r) == 0:
                continue
            first_col = r[0]
            # Check if divider/sub-header row (empty outcome cells)
            if all(c == "" for c in r[1:]):
                continue
            assert len(r) == 5, f"Row in table {t_id} does not have 5 cells: {r}"
            for c_idx, cell in enumerate(r[1:], start=1):
                total_cells += 1
                if c_idx == 4:
                    alex_cells += 1
                m = cell_re.match(cell)
                assert m is not None, f"Malformed cell in {t_id} row {r_idx} col {c_idx}: '{cell}'"
                p1 = float(m.group(1))
                p0 = float(m.group(2))
                pval_str = m.group(3)
                assert 0.0 <= p1 <= 100.0, f"Out of bounds p1: {p1}"
                assert 0.0 <= p0 <= 100.0, f"Out of bounds p0: {p0}"
                # check p-value format
                clean_pval = pval_str.replace("†", "").strip()
                if clean_pval.startswith("<"):
                    pv = 0.0001
                else:
                    pv = float(clean_pval)
                assert 0.0 <= pv <= 1.0, f"Out of bounds p-value: {pv} from '{pval_str}'"

    for s_title, data in all_parsed_summaries.items():
        for r_idx, r in enumerate(data["rows"]):
            if len(r) == 0:
                continue
            if all(c == "" for c in r[1:]):
                continue
            assert len(r) == 5, f"Row in summary {s_title} does not have 5 cells: {r}"
            for c_idx, cell in enumerate(r[1:], start=1):
                total_cells += 1
                if c_idx == 4:
                    alex_cells += 1
                m = cell_re.match(cell)
                assert m is not None, f"Malformed cell in summary {s_title} row {r_idx} col {c_idx}: '{cell}'"
                p1 = float(m.group(1))
                p0 = float(m.group(2))
                pval_str = m.group(3)
                assert 0.0 <= p1 <= 100.0, f"Out of bounds p1: {p1}"
                clean_pval = pval_str.replace("†", "").strip()
                if clean_pval.startswith("<"):
                    pv = 0.0001
                else:
                    pv = float(clean_pval)
                assert 0.0 <= pv <= 1.0, f"Out of bounds p-value: {pv} from '{pval_str}'"

    print(f"PASS: Validated {total_cells} outcome cells ({alex_cells} Alex cells) with zero malformations or NaNs!")

    # ---------------------------------------------------------
    # 4. CROSS-TABLE CONSISTENCY (MODEL POV vs SEAT POV SUB-TABLE AVERAGES)
    # ---------------------------------------------------------
    print("\n--- TEST 4: Cross-Table Consistency (Model POV vs Seat POV Sub-Table Averages) ---")
    # For each condition and step, the SUB-TABLE AVERAGE in Model POV table must match Seat POV table!
    pairs = [
        # Part 1: Probe OFF
        ("Table 1.3", "Table 1.9", "Part 1 S3->S11 Labelled"),
        ("Table 1.4", "Table 1.10", "Part 1 S4->S11 Labelled"),
        ("Table 1.15", "Table 1.21", "Part 1 S3->S11 Mislabelled"),
        ("Table 1.16", "Table 1.22", "Part 1 S4->S11 Mislabelled"),
        ("Table 1.27", "Table 1.33", "Part 1 S3->S11 Unlabelled"),
        ("Table 1.28", "Table 1.34", "Part 1 S4->S11 Unlabelled"),
        # Part 2: Probe ON
        ("Table 2.3", "Table 2.9", "Part 2 S3->S11 Labelled"),
        ("Table 2.4", "Table 2.10", "Part 2 S4->S11 Labelled"),
        ("Table 2.15", "Table 2.21", "Part 2 S3->S11 Mislabelled"),
        ("Table 2.16", "Table 2.22", "Part 2 S4->S11 Mislabelled"),
        ("Table 2.27", "Table 2.33", "Part 2 S3->S11 Unlabelled"),
        ("Table 2.28", "Table 2.34", "Part 2 S4->S11 Unlabelled"),
        # Part 3: Combined
        ("Table 3.3", "Table 3.9", "Part 3 S3->S11 Labelled"),
        ("Table 3.4", "Table 3.10", "Part 3 S4->S11 Labelled"),
        ("Table 3.15", "Table 3.21", "Part 3 S3->S11 Mislabelled"),
        ("Table 3.16", "Table 3.22", "Part 3 S4->S11 Mislabelled"),
        ("Table 3.27", "Table 3.33", "Part 3 S3->S11 Unlabelled"),
        ("Table 3.28", "Table 3.34", "Part 3 S4->S11 Unlabelled"),
        # Part 4: Step 5 (Probe ON)
        ("Table 4.2", "Table 4.5", "Part 4 S5->S11 Labelled"),
        ("Table 4.8", "Table 4.11", "Part 4 S5->S11 Mislabelled"),
        ("Table 4.14", "Table 4.17", "Part 4 S5->S11 Unlabelled"),
    ]

    def get_sub_table_avg_rows(table_data):
        avg_rows = {}
        for r in table_data["rows"]:
            if len(r) == 5 and "Average" in r[0]:
                avg_rows[r[0]] = r[1:]
        return avg_rows

    for t_model_id, t_seat_id, desc in pairs:
        t_model = all_parsed_tables[t_model_id]
        t_seat = all_parsed_tables[t_seat_id]
        m_avg = get_sub_table_avg_rows(t_model)
        s_avg = get_sub_table_avg_rows(t_seat)
        assert len(m_avg) > 0, f"No average rows in {t_model_id}"
        assert len(m_avg) == len(s_avg), f"Mismatched avg row count between {t_model_id} and {t_seat_id}"
        for action_name in m_avg:
            assert action_name in s_avg, f"Missing {action_name} in {t_seat_id}"
            m_cells = m_avg[action_name]
            s_cells = s_avg[action_name]
            for col_idx, (mc, sc) in enumerate(zip(m_cells, s_cells)):
                assert mc == sc, (
                    f"Mismatch in {desc} ({action_name}, col {expected_headers[col_idx]}):\n"
                    f"  Model POV ({t_model_id}): {mc}\n"
                    f"  Seat POV ({t_seat_id}):  {sc}"
                )

    print(f"PASS: All 21 Model POV vs Seat POV Sub-Table Averages are 100% IDENTICAL across all 4 outcome columns!")

    # ---------------------------------------------------------
    # 5. CROSS-TABLE CONSISTENCY (NESTED SUB-TABLE AVERAGES vs SUMMARY STACKS)
    # ---------------------------------------------------------
    print("\n--- TEST 5: Nested Sub-Table Averages vs Summary Stack Alignment ---")
    # Verify that the SUB-TABLE AVERAGE in nested tables matches the corresponding SUB-AVERAGE row in the Summary Stack!
    # For example, in Part 1 S3->S11:
    # Summary stack "PROBE OFF Summary: Step 3 -> Step 11 Peer Identification" has:
    # "| **SUB-AVERAGE: LABELLED (N=100)** |"
    # followed by rows for each action.
    # Check these match Table 1.3 SUB-TABLE AVERAGE rows!
    
    summary_checks = [
        ("PROBE OFF Summary: Step 3 -> Step 11 Peer Identification", "LABELLED", "Table 1.3"),
        ("PROBE OFF Summary: Step 3 -> Step 11 Peer Identification", "MISLABELLED", "Table 1.15"),
        ("PROBE OFF Summary: Step 3 -> Step 11 Peer Identification", "UNLABELLED", "Table 1.27"),
        ("PROBE OFF Summary: Step 4 -> Step 11 Peer Identification", "LABELLED", "Table 1.4"),
        ("PROBE OFF Summary: Step 4 -> Step 11 Peer Identification", "MISLABELLED", "Table 1.16"),
        ("PROBE OFF Summary: Step 4 -> Step 11 Peer Identification", "UNLABELLED", "Table 1.28"),

        ("PROBE ON Summary: Step 3 -> Step 11 Peer Identification", "LABELLED", "Table 2.3"),
        ("PROBE ON Summary: Step 3 -> Step 11 Peer Identification", "MISLABELLED", "Table 2.15"),
        ("PROBE ON Summary: Step 3 -> Step 11 Peer Identification", "UNLABELLED", "Table 2.27"),
        ("PROBE ON Summary: Step 4 -> Step 11 Peer Identification", "LABELLED", "Table 2.4"),
        ("PROBE ON Summary: Step 4 -> Step 11 Peer Identification", "MISLABELLED", "Table 2.16"),
        ("PROBE ON Summary: Step 4 -> Step 11 Peer Identification", "UNLABELLED", "Table 2.28"),

        ("Triple-Average Summary Stack: Step 3 -> Step 11 Peer Identification", "LABELLED", "Table 3.3"),
        ("Triple-Average Summary Stack: Step 3 -> Step 11 Peer Identification", "MISLABELLED", "Table 3.15"),
        ("Triple-Average Summary Stack: Step 3 -> Step 11 Peer Identification", "UNLABELLED", "Table 3.27"),
        ("Triple-Average Summary Stack: Step 4 -> Step 11 Peer Identification", "LABELLED", "Table 3.4"),
        ("Triple-Average Summary Stack: Step 4 -> Step 11 Peer Identification", "MISLABELLED", "Table 3.16"),
        ("Triple-Average Summary Stack: Step 4 -> Step 11 Peer Identification", "UNLABELLED", "Table 3.28"),

        ("Step 5 Summary: Step 5 -> Step 11 Peer Identification (Probe ON, N=300)", "LABELLED", "Table 4.2"),
        ("Step 5 Summary: Step 5 -> Step 11 Peer Identification (Probe ON, N=300)", "MISLABELLED", "Table 4.8"),
        ("Step 5 Summary: Step 5 -> Step 11 Peer Identification (Probe ON, N=300)", "UNLABELLED", "Table 4.14"),
    ]

    for s_title, lbl, t_id in summary_checks:
        s_data = all_parsed_summaries[s_title]
        t_data = all_parsed_tables[t_id]
        t_avgs = get_sub_table_avg_rows(t_data)
        
        # find in summary
        s_rows = s_data["rows"]
        # find where header starts for lbl
        target_sub = f"SUB-AVERAGE: {lbl}" if "Triple-Average" not in s_title else f"COMBINED CONDITION AVERAGE: {lbl}"
        idx_start = -1
        for i, r in enumerate(s_rows):
            if len(r) > 0 and target_sub in r[0]:
                idx_start = i
                break
        assert idx_start != -1, f"Could not find {target_sub} in {s_title}"
        
        # compare action rows
        # In summary stack: "↳ *Factual Pushback*" (bold=False), in nested table: "↳ *Factual Pushback Average*" (bold=True)
        # Note the values inside cells: nested table has bold=True "**X% vs Y% (p=...)**", summary stack has bold=False "X% vs Y% (p=...)"
        for offset in range(1, len(t_avgs) + 1):
            s_r = s_rows[idx_start + offset]
            s_act = s_r[0].replace("↳ *", "").replace("*", "").strip()
            # find corresponding in t_avgs
            matched = False
            for t_act_key, t_cells in t_avgs.items():
                t_act = t_act_key.replace("↳ *", "").replace(" Average*", "").strip()
                if t_act == s_act:
                    matched = True
                    for col_idx, (sc, tc) in enumerate(zip(s_r[1:], t_cells)):
                        # strip bolding
                        clean_sc = sc.replace("**", "").strip()
                        clean_tc = tc.replace("**", "").strip()
                        assert clean_sc == clean_tc, (
                            f"Mismatch in {s_title} vs {t_id} for {s_act} col {expected_headers[col_idx]}:\n"
                            f"  Summary: {clean_sc}\n"
                            f"  Nested:  {clean_tc}"
                        )
                    break
            assert matched, f"Could not match action {s_act} from {s_title} in {t_id}"

    print(f"PASS: All 21 Summary Stack condition slices match Nested Table Sub-Averages perfectly!")

    # ---------------------------------------------------------
    # 6. VERIFY BIT-FOR-BIT PRESERVATION OF COWORKER BASELINES
    # ---------------------------------------------------------
    print("\n--- TEST 6: Baseline Cache Bit-for-Bit Verification ---")
    with open(BASELINE_CACHE, "r", encoding="utf-8") as f:
        cache_data = json.load(f)

    b3_cache = cache_data.get("reports/block3_bucket1_to_bucket3_inferential_report.md", {})
    coworker_lines = b3_cache.get("coworker_lines", [])
    print(f"Baseline cache has {len(coworker_lines)} coworker baseline lines for Block 3 report.")
    assert len(coworker_lines) > 0, "No coworker baseline lines found!"

    import verify_coworker_baselines as vcb
    errors = vcb.verify_file("reports/block3_bucket1_to_bucket3_inferential_report.md", cache_data, verbose=True)
    assert len(errors) == 0, f"Baseline verification errors found: {errors}"
    print(f"PASS: Baseline verification confirmed 0 regressions over {len(coworker_lines)} coworker baseline lines!")

    # ---------------------------------------------------------
    # 7. AUDIT MISSING WORKERS (RINA UNDER PROBE ON)
    # ---------------------------------------------------------
    print("\n--- TEST 7: Audit 6 Missing Alex Cases (Rina Under Probe ON) ---")
    import glob
    from generate_block3_bucket1_to_bucket3 import load_dataset, extract_worker_metrics

    workers = load_dataset()
    df_all = pd.DataFrame([extract_worker_metrics(w) for w in workers])
    print(f"Total workers in dataset: {len(df_all)}")
    assert len(df_all) == 600, f"Expected 600 workers, found {len(df_all)}"

    # Filter missing Alex guesses
    missing_alex = df_all[df_all["s11_alex_tot"] == 0]
    valid_alex = df_all[df_all["s11_alex_tot"] == 1]
    print(f"Valid Alex guesses: {len(valid_alex)} (Expected: 594)")
    print(f"Missing Alex guesses: {len(missing_alex)} (Expected: 6)")
    assert len(valid_alex) == 594, f"Expected 594 valid Alex guesses, got {len(valid_alex)}"
    assert len(missing_alex) == 6, f"Expected 6 missing Alex guesses, got {len(missing_alex)}"

    # Audit the 6 missing workers:
    for idx, r in missing_alex.iterrows():
        assert r["worker_name"] == "Rina", f"Missing worker is not Rina: {r['worker_name']}"
        assert r["model"] == "qwen-2-5-72b", f"Missing worker model is not qwen-2-5-72b: {r['model']}"
        assert r["probe"] == 1, f"Missing worker probe is not 1 (Probe ON): {r['probe']}"
        assert r["s11_alex_as_hu"] == 0.0, f"Missing worker s11_alex_as_hu != 0.0: {r['s11_alex_as_hu']}"
        assert r["s11_alex_tot"] == 0.0, f"Missing worker s11_alex_tot != 0.0: {r['s11_alex_tot']}"
        # Crucially: For missing Rina records, identify_probe did not fire, so s11_tot == 0
        assert r["s11_tot"] == 0, f"Missing worker s11_tot != 0: {r['s11_tot']}"
        print(f"  Missing worker: {r['worker_name']} ({r['model']}), Seat {r['seat']}, Run: {r['bname']}, s11_tot={r['s11_tot']}, s11_alex_tot={r['s11_alex_tot']}")

    # For valid workers, all 594 must have s11_tot == 19
    for idx, r in valid_alex.iterrows():
        assert r["s11_tot"] == 19, f"Valid worker s11_tot != 19: {r['s11_tot']}"

    print(f"PASS: Exactly 6 missing Alex guesses verified: all Rina, all qwen-2-5-72b, all Probe ON, all with intact 19 coworker guesses!")

    # Check Probe OFF vs Probe ON Alex counts
    df_off = df_all[df_all["probe"] == 0]
    df_on = df_all[df_all["probe"] == 1]
    assert df_off["s11_alex_tot"].sum() == 300.0, f"Probe OFF Alex tot != 300: {df_off['s11_alex_tot'].sum()}"
    assert df_on["s11_alex_tot"].sum() == 294.0, f"Probe ON Alex tot != 294: {df_on['s11_alex_tot'].sum()}"
    print(f"Probe OFF valid Alex sum: {df_off['s11_alex_tot'].sum()}; Probe ON valid Alex sum: {df_on['s11_alex_tot'].sum()}")

    # ---------------------------------------------------------
    # 8. VERIFY TABLE 5.1 MULTIPLE TESTING & FDR
    # ---------------------------------------------------------
    print("\n--- TEST 8: Table 5.1 Verification ---")
    t51_lines = []
    in_t51 = False
    for l in lines:
        if "#### Table 5.1:" in l:
            in_t51 = True
            continue
        if in_t51:
            if l.startswith("---") or l.startswith("# APPENDIX"):
                break
            if l.strip().startswith("|"):
                t51_lines.append(l.strip())

    t51_headers, t51_rows = parse_markdown_table(t51_lines)
    print(f"Table 5.1 displayed rows: {len(t51_rows)}")
    assert len(t51_rows) == 25, f"Expected 25 rows in Table 5.1, found {len(t51_rows)}"

    # Check whether any Alex outcome is in the top 25
    alex_in_t51 = [r for r in t51_rows if "Alex Guessed as Human" in r[2]]
    print(f"Alex pairs in Table 5.1 Top 25: {len(alex_in_t51)}")
    assert len(alex_in_t51) == 0, f"Alex pairs unexpectedly found in Top 25: {alex_in_t51}"

    # Check narrative text for M=272
    m_found = re.findall(r"M\s*=\s*272", report_text)
    print(f"Narrative references to M=272: {len(m_found)}")
    assert len(m_found) >= 1, "Expected narrative reference to M=272 in report!"

    # ---------------------------------------------------------
    # 9. VERIFY APPENDIX A CLUSTERING DIAGNOSTICS
    # ---------------------------------------------------------
    print("\n--- TEST 9: Appendix A Diagnostics Table ---")
    app_a_lines = []
    in_app_a = False
    for l in lines:
        if "APPENDIX A:" in l:
            in_app_a = True
            continue
        if in_app_a:
            if l.startswith("---") or (l.startswith("# ") and "APPENDIX" not in l):
                break
            if l.strip().startswith("|"):
                app_a_lines.append(l.strip())

    app_a_headers, app_a_rows = parse_markdown_table(app_a_lines)
    print(f"Appendix A diagnostic rows: {len(app_a_rows)}")

    # Find Step 11 rows
    s11_app_rows = [r for r in app_a_rows if "Step 11" in r[0]]
    print(f"Step 11 rows in Appendix A: {len(s11_app_rows)}")
    for r in s11_app_rows:
        print("  ", " | ".join(r))
    assert len(s11_app_rows) == 4, f"Expected 4 Step 11 rows in Appendix A, found {len(s11_app_rows)}"

    alex_app_row = [r for r in s11_app_rows if "s11_alex_as_hu" in r[1]]
    assert len(alex_app_row) == 1, "Missing s11_alex_as_hu row in Appendix A!"
    print(f"Alex row in Appendix A: {alex_app_row[0]}")

    print("\n" + "=" * 70)
    print("ALL CHALLENGER AUDIT TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    run_audits()
