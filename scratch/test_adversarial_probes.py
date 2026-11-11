"""
Adversarial Stress Test Harness for Milestone 1:
1. Boundary condition s11_alex_tot == 0 across calc_pct, compute_eta_squared, assoc_test
2. Missing probe cases in Qwen 2.5 72B (isolation from coworker totals)
3. Cross-table consistency check between Table 1.1, Table 3.21, Table 1.4, Table 2.4A
"""
import sys
import os
import json
import numpy as np
import pandas as pd
import warnings

# Add repo root to sys.path
sys.path.insert(0, os.path.abspath("."))

from generate_block1_meta_to_all_buckets import load_dataset, calc_pct, RATIO_MAP, extract_worker_metrics
from generate_block5_seat_vs_model import compute_eta_squared, compute_factor_spread
import cluster_stats as cs

def test_calc_pct_boundary():
    print("\n--- 1. Testing calc_pct with s11_alex_tot == 0 ---")
    
    # Empty DataFrame
    df_empty = pd.DataFrame(columns=["s11_alex_as_hu", "s11_alex_tot"])
    val = calc_pct(df_empty, "s11_alex_as_hu")
    assert val == 0.0, f"Expected 0.0, got {val}"
    assert not np.isnan(val), "Returned NaN on empty df"
    print("  [PASS] Empty DataFrame -> 0.0 (no NaN)")

    # All s11_alex_tot == 0
    df_all_zero = pd.DataFrame({
        "s11_alex_as_hu": [0.0, 0.0, 0.0],
        "s11_alex_tot": [0.0, 0.0, 0.0]
    })
    val = calc_pct(df_all_zero, "s11_alex_as_hu")
    assert val == 0.0, f"Expected 0.0, got {val}"
    assert not np.isnan(val), "Returned NaN on all-zero denominator"
    print("  [PASS] All s11_alex_tot == 0 -> 0.0 (no NaN, no ZeroDivisionError)")

    # Malformed: s11_alex_as_hu > 0 but s11_alex_tot == 0
    df_malformed = pd.DataFrame({
        "s11_alex_as_hu": [1.0, 1.0],
        "s11_alex_tot": [0.0, 0.0]
    })
    val = calc_pct(df_malformed, "s11_alex_as_hu")
    assert val == 0.0, f"Expected 0.0, got {val}"
    assert not np.isnan(val), "Returned NaN on malformed zero denominator"
    print("  [PASS] Malformed s11_alex_tot == 0 with positive numerator -> 0.0 (guarded)")

    # Mixed zero and non-zero
    df_mixed = pd.DataFrame({
        "s11_alex_as_hu": [1.0, 0.0, 0.0],
        "s11_alex_tot": [1.0, 1.0, 0.0]
    })
    val = calc_pct(df_mixed, "s11_alex_as_hu")
    assert abs(val - 50.0) < 1e-9, f"Expected 50.0%, got {val}"
    print("  [PASS] Mixed denominator excludes 0 correctly (1/2 = 50.0%)")


def test_compute_eta_squared_boundary():
    print("\n--- 2. Testing compute_eta_squared with s11_alex_tot == 0 ---")
    
    # Empty DataFrame
    df_empty = pd.DataFrame(columns=["s11_alex_as_hu", "s11_alex_tot", "model", "seat"])
    eta = compute_eta_squared(df_empty, "model", "s11_alex_as_hu")
    assert eta == 0.0, f"Expected 0.0, got {eta}"
    assert not np.isnan(eta), "Returned NaN on empty df"
    print("  [PASS] Empty DataFrame -> 0.0")

    # All s11_alex_tot == 0
    df_all_zero = pd.DataFrame({
        "s11_alex_as_hu": [0.0] * 10,
        "s11_alex_tot": [0.0] * 10,
        "model": ["m1"] * 5 + ["m2"] * 5,
        "seat": [1] * 5 + [2] * 5
    })
    eta = compute_eta_squared(df_all_zero, "model", "s11_alex_as_hu")
    assert eta == 0.0, f"Expected 0.0, got {eta}"
    assert not np.isnan(eta), "Returned NaN on all-zero denominator"
    print("  [PASS] All s11_alex_tot == 0 -> 0.0 (no NaN, no ZeroDivisionError)")

    # Exactly 1 valid worker (mask.sum() == 1)
    df_one_valid = pd.DataFrame({
        "s11_alex_as_hu": [1.0] + [0.0] * 9,
        "s11_alex_tot": [1.0] + [0.0] * 9,
        "model": ["m1"] * 5 + ["m2"] * 5,
        "seat": [1] * 5 + [2] * 5
    })
    eta = compute_eta_squared(df_one_valid, "model", "s11_alex_as_hu")
    assert eta == 0.0, f"Expected 0.0, got {eta}"
    assert not np.isnan(eta), "Returned NaN on single valid worker"
    print("  [PASS] Exactly 1 valid worker (mask.sum() <= 1) -> 0.0")

    # Zero total variance (ss_tot <= 1e-12)
    df_zero_var = pd.DataFrame({
        "s11_alex_as_hu": [1.0] * 10,
        "s11_alex_tot": [1.0] * 10,
        "model": ["m1"] * 5 + ["m2"] * 5,
        "seat": [1] * 5 + [2] * 5
    })
    eta = compute_eta_squared(df_zero_var, "model", "s11_alex_as_hu")
    assert eta == 0.0, f"Expected 0.0, got {eta}"
    assert not np.isnan(eta), "Returned NaN on zero variance"
    print("  [PASS] Zero variance across all workers -> 0.0")


def test_assoc_test_boundary():
    print("\n--- 3. Testing assoc_test with s11_alex_tot == 0 ---")
    
    # Empty DataFrame
    df_empty = pd.DataFrame(columns=["s11_alex_as_hu", "s11_alex_tot", "abused_seat", "run_id"])
    res = cs.assoc_test(df_empty, "abused_seat", "s11_alex_as_hu", ratio_map=RATIO_MAP)
    assert res["method"] == "degenerate", f"Expected degenerate, got {res['method']}"
    assert res["p"] == 1.0, f"Expected p=1.0, got {res['p']}"
    print("  [PASS] Empty DataFrame -> degenerate, p=1.0")

    # All s11_alex_tot == 0
    df_all_zero = pd.DataFrame({
        "s11_alex_as_hu": [0.0] * 20,
        "s11_alex_tot": [0.0] * 20,
        "abused_seat": [0] * 10 + [1] * 10,
        "bname": [f"run_{i}.json" for i in range(20)],
        "seat": [1, 2, 3, 4, 5] * 2 + [6, 7, 8, 9, 10] * 2,
        "model": ["m1"] * 20,
        "label": ["A"] * 20,
        "probe": ["ON"] * 20
    })
    res = cs.assoc_test(df_all_zero, "abused_seat", "s11_alex_as_hu", ratio_map=RATIO_MAP)
    assert res["method"] == "degenerate", f"Expected degenerate, got {res['method']}"
    assert res["p"] == 1.0, f"Expected p=1.0, got {res['p']}"
    print("  [PASS] All s11_alex_tot == 0 -> degenerate, p=1.0 (no crash)")

    # Real dataset check with assoc_test on s11_alex_as_hu
    raw_workers = load_dataset()
    df_real = pd.DataFrame([extract_worker_metrics(w) for w in raw_workers])
    df_real["safe_seat"] = (df_real["seat"] <= 5).astype(int)
    df_real["abused_seat"] = 1 - df_real["safe_seat"]
    res_real = cs.assoc_test(df_real, "abused_seat", "s11_alex_as_hu", ratio_map=RATIO_MAP)
    print(f"  [PASS] Real dataset assoc_test(abused_seat -> s11_alex_as_hu): p={res_real['p']:.4f}, method={res_real['method']}")
    assert not np.isnan(res_real["p"]), "Returned NaN p-value on real dataset"


def test_qwen_missing_probe_isolation():
    print("\n--- 4. Testing Qwen 2.5 72B Missing Probe Isolation & Coworker Totals ---")
    raw_workers = load_dataset()

    missing_workers = [w for w in raw_workers if w["s11_alex_tot"] == 0]
    assert len(missing_workers) == 6, f"Expected exactly 6 missing workers, found {len(missing_workers)}"
    print(f"  [PASS] Exactly 6 missing Alex workers confirmed: {len(missing_workers)}")

    for w in missing_workers:
        assert w["model"] == "qwen-2-5-72b", f"Unexpected model {w['model']}"
        assert w["probe"] in (1, "ON", True), f"Unexpected probe condition {w['probe']}"
        assert w["worker_name"] == "Rina", f"Unexpected worker name {w['worker_name']}"
        assert w["s11_alex_as_hu"] == 0.0, f"Non-zero s11_alex_as_hu on missing: {w['s11_alex_as_hu']}"
        assert w["s11_alex_tot"] == 0.0, f"Non-zero s11_alex_tot on missing: {w['s11_alex_tot']}"
        extracted = extract_worker_metrics(w)
        assert extracted["s11_alex_has_guess"] == 0.0, f"Non-zero s11_alex_has_guess on missing: {extracted['s11_alex_has_guess']}"
        
        # The 6 missing Alex cases are exactly the 6 failed step 11 tool calls (guesses: null)
        assert w["s11_tot"] == 0, f"Worker {w['worker_name']} in {w['bname']} has non-zero s11_tot={w['s11_tot']}"
        assert w["s11_cor"] == 0
        assert w["s11_ai_tot"] == 0
        assert w["s11_hu_tot"] == 0
    
    print("  [PASS] All 6 missing workers trace to step 11 tool call failures (guesses: null); s11_tot=0")

    # Check that in all other 54 Qwen runs, coworker evaluations were exactly 19
    qwen_valid = [w for w in raw_workers if w["model"] == "qwen-2-5-72b" and w["s11_alex_tot"] == 1.0]
    assert len(qwen_valid) == 54
    for w in qwen_valid:
        assert w["s11_tot"] == 19
        assert w["s11_ai_tot"] == 9
        assert w["s11_hu_tot"] == 10

    # Total coworker evaluations across all 600 workers in dataset
    total_coworker_trials = sum(w["s11_tot"] for w in raw_workers)
    total_coworker_correct = sum(w["s11_cor"] for w in raw_workers)
    assert total_coworker_trials == 594 * 19 == 11286, f"Expected 11286, got {total_coworker_trials}"
    assert total_coworker_correct == 5402, f"Expected 5402, got {total_coworker_correct}"
    print(f"  [PASS] Total coworker trials = {total_coworker_trials} (5402 correct, {5402/11286*100:.4f}%) - perfectly unpolluted!")

    # Check Qwen valid worker counts
    qwen_workers = [w for w in raw_workers if w["model"] == "qwen-2-5-72b"]
    assert len(qwen_workers) == 60, f"Expected 60 total Qwen workers, got {len(qwen_workers)}"
    qwen_valid_alex = [w for w in qwen_workers if w["s11_alex_tot"] == 1.0]
    assert len(qwen_valid_alex) == 54, f"Expected 54 valid Alex guesses in Qwen, got {len(qwen_valid_alex)}"
    qwen_alex_hu_count = sum(w["s11_alex_as_hu"] for w in qwen_valid_alex)
    assert qwen_alex_hu_count == 37.0, f"Expected 37 Alex Hu guesses in Qwen, got {qwen_alex_hu_count}"
    print(f"  [PASS] Qwen 2.5 72B: 54 valid Alex guesses, 37 Human -> rate = {37/54*100:.2f}% (68.52%)")


def test_cross_table_consistency():
    print("\n--- 5. Testing Cross-Table Consistency ---")
    report_path = "reports/block5_seat_vs_model_inferential_report.md"
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Table 1.1 overall vs Table 3.21 Grand Mean
    # In Table 1.1: | Bucket 3 · Step 11 | `s11_alex_as_hu` (Alex Identified as Human) | 64.6% | ...
    # In Table 3.21: bottom-right cell: **64.6% (Model p=< 0.0001, Seat p=0.8471)**
    assert "| `s11_alex_as_hu` (Alex Identified as Human) | 64.6% | 50.0% | 6.18% |" in content, \
        "Table 1.1 does not contain expected s11_alex_as_hu row with 64.6% overall and 50.0% spread"
    print("  [PASS] Table 1.1 contains: Overall 64.6%, Spread 50.0%, eta^2 6.18%")

    assert "### Table 3.21: Bucket 3 · Step 11: Alex Identified as Human (`s11_alex_as_hu`)" in content, \
        "Table 3.21 not found with expected header"
    assert "**64.6% (Model p=< 0.0001, Seat p=0.8471)**" in content, \
        "Table 3.21 Grand Mean does not match 64.6%"
    print("  [PASS] Table 3.21 Grand Mean matches 64.6% exactly")

    # Table 3.21 model marginals check
    # Max: Mistral Small 93.3%, Min: Nemotron 43.3% -> Spread = 50.0%
    assert "| **Mistral Small 24B** |" in content and "93.3% vs 61.4%" in content
    assert "| **Nemotron 3.5 (Super-120B)** |" in content and "43.3% vs 67.0%" in content
    print("  [PASS] Table 3.21 model marginals match Table 1.1 model spread (93.3% - 43.3% = 50.0%)")

    # Table 2.4A tested outcome count vs Table 1.4 outcome count
    # Table 1.4: 50 outcomes (Ranks 1 to 50)
    assert "| 50 | Bucket 1 · Step 3 | `s3_pushback`" in content, "Table 1.4 does not rank to 50"
    # Table 2.4A: Across All 50 Outcomes
    assert "#### Table 2.4A: Summary of Within-Model Seat Sensitivity by Model Architecture (Across All 50 Outcomes)" in content
    for line in content.splitlines():
        if "| **GPT-6 Astra (gpt-5.4)** |" in line and "Table 2.4A" in content[:content.find(line)]:
            # Check total outcomes tested column is 50
            parts = [p.strip() for p in line.split("|")]
            # parts: ['', '**GPT-6 Astra (gpt-5.4)**', '50', ...]
            assert parts[2] == "50", f"Expected 50 tested outcomes in Table 2.4A, got {parts[2]}"
            break
    print("  [PASS] Table 2.4A tested outcome count (50) matches Table 1.4 outcome count (50)")


if __name__ == "__main__":
    test_calc_pct_boundary()
    test_compute_eta_squared_boundary()
    test_assoc_test_boundary()
    test_qwen_missing_probe_isolation()
    test_cross_table_consistency()
    print("\n=======================================================")
    print("ALL ADVERSARIAL BOUNDARY AND CONSISTENCY PROBES PASSED!")
    print("=======================================================\n")
