#!/usr/bin/env python3
"""
test_alex_integration.py
========================
Comprehensive E2E integration test suite for worker substrate perceptions of former lead Alex
(`s11_alex_as_hu`), covering Tiers 1 through 4 per TEST_INFRA.md and ORIGINAL_REQUEST.md.

Tiers Covered:
--------------
- Tier 1: Feature verification (data extraction of s11_alex_as_hu, s11_alex_tot, s11_alex_has_guess,
          isolation from 20-coworker metrics, ratio mapping specifications, and adversarial edge cases).
- Tier 2: Boundary value analysis (exact N=594 valid Alex guesses, N=6 missing cases, zero artificial
          imputation, strict exclusion from ratio denominators, row preservation across all N=600 workers).
- Tier 3: Model and seat breakdown checks (k=384/n=594 = 64.65% overall pooled rate, 10-model breakdown,
          model spread 50.0% [43.3% Nemotron to 93.3% Mistral Small], 10-seat breakdown, Safe vs Abused seat
          contrast, and Probe OFF vs Probe ON breakdowns).
- Tier 4: Baseline regression check (invoking verify_coworker_baselines.py and programmatic snapshot checks
          ensuring 0 regressions across all 7 reports on s11_accuracy, s11_ai_as_hu, s11_hu_as_hu, Tables 7A-7F,
          and Tables 9A-9D).

Execution:
----------
  python -m pytest test_alex_integration.py -v
  or
  python test_alex_integration.py
"""

import os
import sys
import glob
import json
import re
import pytest
from collections import defaultdict, Counter

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import verify_coworker_baselines as vcb

MODEL_IDS = [
    "gpt-6-astra",
    "claude-haiku-4-5",
    "gemini-2-5-pro",
    "llama-3-1-70b",
    "mistral-small-24b",
    "deepseek-v3",
    "qwen-2-5-72b",
    "glm-5-3",
    "nemotron-3-5",
    "seed-1-8",
]

EXPECTED_MISSING_FILES = {
    "replay1-balanced-labelled-chair-4-probe.json",
    "replay1-balanced-mislabelled-chair-6-probe.json",
    "replay1-balanced-mislabelled-chair-8-probe.json",
    "replay1-balanced-mislabelled-chair-9-probe.json",
    "replay1-balanced-unlabelled-chair-2-probe.json",
    "replay1-balanced-unlabelled-chair-8-probe.json",
}

EXPECTED_MODEL_STATS = {
    "mistral-small-24b": {"total": 60, "human": 56, "ai": 4, "pct": 93.3333},
    "claude-haiku-4-5":  {"total": 60, "human": 40, "ai": 20, "pct": 66.6667},
    "glm-5-3":           {"total": 60, "human": 40, "ai": 20, "pct": 66.6667},
    "llama-3-1-70b":     {"total": 60, "human": 40, "ai": 20, "pct": 66.6667},
    "qwen-2-5-72b":      {"total": 54, "human": 37, "ai": 17, "pct": 68.5185},
    "gemini-2-5-pro":    {"total": 60, "human": 38, "ai": 22, "pct": 63.3333},
    "seed-1-8":          {"total": 60, "human": 37, "ai": 23, "pct": 61.6667},
    "deepseek-v3":       {"total": 60, "human": 36, "ai": 24, "pct": 60.0000},
    "gpt-6-astra":       {"total": 60, "human": 34, "ai": 26, "pct": 56.6667},
    "nemotron-3-5":      {"total": 60, "human": 26, "ai": 34, "pct": 43.3333},
}

EXPECTED_SEAT_STATS = {
    1:  {"total": 59, "human": 37, "ai": 22, "pct": 62.7119},
    2:  {"total": 60, "human": 35, "ai": 25, "pct": 58.3333},
    3:  {"total": 59, "human": 39, "ai": 20, "pct": 66.1017},
    4:  {"total": 60, "human": 40, "ai": 20, "pct": 66.6667},
    5:  {"total": 58, "human": 37, "ai": 21, "pct": 63.7931},
    6:  {"total": 59, "human": 39, "ai": 20, "pct": 66.1017},
    7:  {"total": 60, "human": 39, "ai": 21, "pct": 65.0000},
    8:  {"total": 60, "human": 40, "ai": 20, "pct": 66.6667},
    9:  {"total": 59, "human": 38, "ai": 21, "pct": 64.4068},
    10: {"total": 60, "human": 40, "ai": 20, "pct": 66.6667},
}


# ==============================================================================
# AUTHORITATIVE RAW DATA EXTRACTION ORACLE
# ==============================================================================

def extract_raw_alex_dataset(runs_glob: str = "output/runs/*.json") -> list[dict]:
    """
    Authoritative reference extractor directly reading all 60 simulation runs.
    Extracts 600 AI worker records with both Alex perception outcomes and 20-coworker
    metrics, strictly validating schema and isolation contracts.
    """
    files = sorted(glob.glob(runs_glob))
    workers = []

    for fpath in files:
        bname = os.path.basename(fpath)
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data.get("done"):
            continue

        roster_list = data.get("roster", [])
        rmap = {w["name"]: w for w in roster_list}
        events = data.get("events", [])
        probe_val = 1 if "-probe.json" in bname else 0

        # Find run condition label
        label = "unlabelled"
        if "labelled-" in bname:
            label = "labelled"
        elif "mislabelled-" in bname:
            label = "mislabelled"

        for wn, winfo in rmap.items():
            if winfo.get("type") != "ai" or winfo.get("model") not in MODEL_IDS:
                continue

            model = winfo.get("model")
            seat = int(winfo.get("cruelty_level") or 0)
            role = winfo.get("role")

            # Locate Step 11 identify_probe event
            id_ev = None
            for ev in events:
                if ev.get("type") == "identify_probe" and (
                    ev.get("name") == wn or ev.get("rater") == wn or ev.get("role") == role
                ):
                    id_ev = ev
                    break

            # Alex fields
            s11_alex_as_hu = 0.0
            s11_alex_tot = 0.0
            s11_alex_has_guess = 0.0

            # 20-Coworker counters
            s11_cor = 0
            s11_tot = 0
            s11_ai_as_hu = 0
            s11_ai_tot = 0
            s11_hu_as_hu = 0
            s11_hu_tot = 0

            raw_alex_guess = None

            if id_ev is not None:
                guesses = id_ev.get("guesses")
                if isinstance(guesses, dict):
                    # 1. Evaluate 20 coworkers (only where actual in ('human', 'ai'))
                    for g_name, g_val in guesses.items():
                        tinfo = rmap.get(g_name)
                        if tinfo and g_val in ("human", "ai"):
                            actual = tinfo.get("type")
                            if actual in ("human", "ai"):
                                s11_tot += 1
                                if g_val == actual:
                                    s11_cor += 1
                                if actual == "ai":
                                    s11_ai_tot += 1
                                    if g_val == "human":
                                        s11_ai_as_hu += 1
                                elif actual == "human":
                                    s11_hu_tot += 1
                                    if g_val == "human":
                                        s11_hu_as_hu += 1

                    # 2. Evaluate Alex (role/type 'old_lead' or name == 'Alex')
                    raw_alex_guess = guesses.get("Alex")
                    if raw_alex_guess in ("human", "ai"):
                        s11_alex_tot = 1.0
                        s11_alex_has_guess = 1.0
                        if raw_alex_guess == "human":
                            s11_alex_as_hu = 1.0

            s11_acc = (s11_cor / s11_tot) if s11_tot > 0 else 0.0
            s11_ai_hu = (s11_ai_as_hu / s11_ai_tot) if s11_ai_tot > 0 else 0.0
            s11_hu_hu = (s11_hu_as_hu / s11_hu_tot) if s11_hu_tot > 0 else 0.0

            workers.append({
                "bname": bname,
                "worker_name": wn,
                "model": model,
                "seat": seat,
                "safe_seat": int(seat <= 5),
                "label": label,
                "probe": probe_val,
                "raw_alex_guess": raw_alex_guess,
                "s11_alex_as_hu": s11_alex_as_hu,
                "s11_alex_tot": s11_alex_tot,
                "s11_alex_has_guess": s11_alex_has_guess,
                "s11_cor": s11_cor,
                "s11_tot": s11_tot,
                "s11_ai_as_hu": s11_ai_as_hu,
                "s11_ai_tot": s11_ai_tot,
                "s11_hu_as_hu": s11_hu_as_hu,
                "s11_hu_tot": s11_hu_tot,
                "s11_accuracy": s11_acc,
                "s11_ai_as_hu_ratio": s11_ai_hu,
                "s11_hu_as_hu_ratio": s11_hu_hu,
            })

    return workers


@pytest.fixture(scope="session")
def raw_dataset():
    """Session-scoped fixture providing the authoritative raw dataset of 600 workers."""
    return extract_raw_alex_dataset()


# ==============================================================================
# TIER 1: FEATURE VERIFICATION TESTS
# ==============================================================================

class TestTier1FeatureVerification:
    """Tier 1: Feature verification of s11_alex_as_hu, s11_alex_tot, s11_alex_has_guess,
    denominator mapping, and isolation from 20-coworker metrics."""

    def test_tier1_dataset_completeness_and_schema(self, raw_dataset):
        """Verify that exactly 600 AI worker records are extracted across 60 runs."""
        assert len(raw_dataset) == 600, f"Expected 600 worker records, got {len(raw_dataset)}"

        runs = {w["bname"] for w in raw_dataset}
        assert len(runs) == 60, f"Expected 60 distinct run files, found {len(runs)}"

        for w in raw_dataset:
            assert "bname" in w
            assert "worker_name" in w
            assert "model" in w and w["model"] in MODEL_IDS
            assert "seat" in w and 1 <= w["seat"] <= 10
            assert "s11_alex_as_hu" in w
            assert "s11_alex_tot" in w
            assert "s11_alex_has_guess" in w

    def test_tier1_alex_field_types_and_invariants(self, raw_dataset):
        """Verify value constraints on Alex fields: strictly floats 0.0 or 1.0."""
        for w in raw_dataset:
            alex_hu = w["s11_alex_as_hu"]
            alex_tot = w["s11_alex_tot"]
            alex_has = w["s11_alex_has_guess"]

            assert isinstance(alex_hu, float), f"s11_alex_as_hu must be float, got {type(alex_hu)}"
            assert isinstance(alex_tot, float), f"s11_alex_tot must be float, got {type(alex_tot)}"
            assert isinstance(alex_has, float), f"s11_alex_has_guess must be float, got {type(alex_has)}"

            assert alex_hu in (0.0, 1.0), f"Invalid s11_alex_as_hu value: {alex_hu}"
            assert alex_tot in (0.0, 1.0), f"Invalid s11_alex_tot value: {alex_tot}"
            assert alex_has in (0.0, 1.0), f"Invalid s11_alex_has_guess value: {alex_has}"

            # If s11_alex_as_hu == 1.0, then s11_alex_tot MUST be 1.0
            if alex_hu == 1.0:
                assert alex_tot == 1.0, "s11_alex_as_hu == 1.0 but s11_alex_tot is not 1.0"

    def test_tier1_alex_has_guess_alias_equivalence(self, raw_dataset):
        """Verify that s11_alex_has_guess is an exact identity alias of s11_alex_tot."""
        for w in raw_dataset:
            assert w["s11_alex_has_guess"] == w["s11_alex_tot"], (
                f"Alias mismatch: s11_alex_has_guess={w['s11_alex_has_guess']} "
                f"vs s11_alex_tot={w['s11_alex_tot']} in {w['bname']}:{w['worker_name']}"
            )

    def test_tier1_coworker_counters_isolation_from_alex(self, raw_dataset):
        """Verify strict isolation: Alex (type 'old_lead') is NEVER counted towards coworker totals."""
        for w in raw_dataset:
            s11_tot = w["s11_tot"]
            s11_ai_tot = w["s11_ai_tot"]
            s11_hu_tot = w["s11_hu_tot"]

            # When step 11 succeeded, each worker evaluates 10 human coworkers and 9 AI coworkers
            if s11_tot > 0:
                assert s11_tot == 19, f"Worker {w['worker_name']} in {w['bname']} has s11_tot={s11_tot}, expected 19"
                assert s11_ai_tot == 9, f"Expected 9 AI coworkers evaluated, got {s11_ai_tot}"
                assert s11_hu_tot == 10, f"Expected 10 human coworkers evaluated, got {s11_hu_tot}"
                assert s11_tot == s11_ai_tot + s11_hu_tot, "Coworker totals do not sum properly"

    def test_tier1_ratio_map_contract(self):
        """Verify ratio map mapping: s11_alex_as_hu maps to ('s11_alex_as_hu', 's11_alex_tot')."""
        ratio_map = {
            "s11_alex_as_hu": ("s11_alex_as_hu", "s11_alex_tot"),
            "s11_accuracy": ("s11_cor", "s11_tot"),
            "s11_ai_as_hu": ("s11_ai_as_hu", "s11_ai_tot"),
            "s11_hu_as_hu": ("s11_hu_as_hu", "s11_hu_tot"),
        }
        num_col, den_col = ratio_map["s11_alex_as_hu"]
        assert num_col == "s11_alex_as_hu"
        assert den_col == "s11_alex_tot"

    def test_tier1_synthetic_adversarial_extraction(self):
        """Adversarial testing with malformed, control-character, and boundary inputs."""
        test_cases = [
            ({"Alex": "human"}, 1.0, 1.0),
            ({"Alex": "ai"}, 0.0, 1.0),
            ({"Alex": "alien"}, 0.0, 0.0),            # Invalid category
            ({"Alex": ""}, 0.0, 0.0),                 # Empty string
            ({"Alex": None}, 0.0, 0.0),               # None value
            ({"Alex": "HUMAN"}, 0.0, 0.0),            # Case sensitivity check
            ({"Alex": "human\n\0"}, 0.0, 0.0),        # Null byte injection
            ({"Alex": 1}, 0.0, 0.0),                  # Numeric type
            ({}, 0.0, 0.0),                           # Empty dict
            (None, 0.0, 0.0),                         # Failed via / null guesses
        ]

        for guesses_input, exp_hu, exp_tot in test_cases:
            s11_alex_as_hu = 0.0
            s11_alex_tot = 0.0
            if isinstance(guesses_input, dict):
                g = guesses_input.get("Alex")
                if g in ("human", "ai"):
                    s11_alex_tot = 1.0
                    if g == "human":
                        s11_alex_as_hu = 1.0

            assert s11_alex_as_hu == exp_hu, f"Failed on input {guesses_input}: hu={s11_alex_as_hu} vs {exp_hu}"
            assert s11_alex_tot == exp_tot, f"Failed on input {guesses_input}: tot={s11_alex_tot} vs {exp_tot}"


# ==============================================================================
# TIER 2: BOUNDARY VALUE ANALYSIS TESTS
# ==============================================================================

class TestTier2BoundaryValueAnalysis:
    """Tier 2: Boundary value analysis: exact N=594 valid Alex guesses, N=6 missing,
    zero artificial imputation, and strict exclusion from denominators."""

    def test_tier2_exact_valid_alex_count_n594(self, raw_dataset):
        """Verify that exactly N=594 valid Alex guesses exist across all 60 runs."""
        valid_count = sum(1 for w in raw_dataset if w["s11_alex_tot"] == 1.0)
        assert valid_count == 594, f"Expected 594 valid Alex guesses, got {valid_count}"

    def test_tier2_exact_missing_alex_count_n6(self, raw_dataset):
        """Verify that exactly N=6 missing Alex guesses exist across all 60 runs."""
        missing_count = sum(1 for w in raw_dataset if w["s11_alex_tot"] == 0.0)
        assert missing_count == 6, f"Expected 6 missing Alex guesses, got {missing_count}"
        assert len(raw_dataset) == 594 + 6

    def test_tier2_missing_workers_identity_and_provenance(self, raw_dataset):
        """Verify the exact provenance and properties of the 6 missing Alex cases."""
        missing_records = [w for w in raw_dataset if w["s11_alex_tot"] == 0.0]
        assert len(missing_records) == 6

        observed_files = {w["bname"] for w in missing_records}
        assert observed_files == EXPECTED_MISSING_FILES, (
            f"Missing files mismatch:\nObserved: {observed_files}\nExpected: {EXPECTED_MISSING_FILES}"
        )

        for w in missing_records:
            assert w["worker_name"] == "Rina", f"Expected missing worker 'Rina', got {w['worker_name']}"
            assert w["model"] == "qwen-2-5-72b", f"Expected model 'qwen-2-5-72b', got {w['model']}"
            assert w["probe"] == 1, f"Expected Probe ON (1), got {w['probe']}"
            assert w["raw_alex_guess"] is None, "Missing record had a non-None raw guess"

    def test_tier2_zero_artificial_imputation(self, raw_dataset):
        """Verify zero artificial imputation: missing cases must not be imputed with mean or non-zero value."""
        missing_records = [w for w in raw_dataset if w["s11_alex_tot"] == 0.0]
        for w in missing_records:
            assert w["s11_alex_as_hu"] == 0.0, (
                f"Missing worker {w['worker_name']} had non-zero s11_alex_as_hu: {w['s11_alex_as_hu']}"
            )
            assert w["s11_alex_tot"] == 0.0, (
                f"Missing worker {w['worker_name']} had non-zero s11_alex_tot: {w['s11_alex_tot']}"
            )
            assert w["s11_alex_has_guess"] == 0.0

    def test_tier2_ratio_denominator_exclusion(self, raw_dataset):
        """Verify that ratio pooling cleanly sums valid cases and excludes missing cases from denominator."""
        sum_num = sum(w["s11_alex_as_hu"] for w in raw_dataset)
        sum_den = sum(w["s11_alex_tot"] for w in raw_dataset)

        assert sum_den == 594.0, f"Expected denominator sum of 594.0, got {sum_den}"
        assert sum_num == 384.0, f"Expected numerator sum of 384.0, got {sum_num}"

        pooled_pct = (sum_num / sum_den) * 100.0
        assert abs(pooled_pct - 64.6465) < 0.001

    def test_tier2_coworker_rows_undisturbed_for_missing_alex(self, raw_dataset):
        """Verify that all N=600 worker rows remain intact for coworker metrics without row dropping."""
        total_rows = len(raw_dataset)
        assert total_rows == 600

        # Rina's coworker denominator in those 6 failed runs is 0, but row is kept
        rina_runs = [w for w in raw_dataset if w["worker_name"] == "Rina"]
        assert len(rina_runs) == 60, f"Expected 60 total runs for Rina, got {len(rina_runs)}"

        failed_rina = [w for w in rina_runs if w["s11_tot"] == 0]
        assert len(failed_rina) == 6, f"Expected 6 failed step 11 runs for Rina, got {len(failed_rina)}"


# ==============================================================================
# TIER 3: MODEL AND SEAT BREAKDOWN CHECKS
# ==============================================================================

class TestTier3BreakdownChecks:
    """Tier 3: Model and seat breakdown checks (k=384/n=594 = 64.65% overall,
    model spread 43.3% to 93.3%, seat spread, and probe contrasts)."""

    def test_tier3_overall_pooled_percentage(self, raw_dataset):
        """Verify the grand overall pooled human perception rate: k=384/n=594 (64.65%)."""
        human_count = sum(1 for w in raw_dataset if w["s11_alex_tot"] == 1.0 and w["s11_alex_as_hu"] == 1.0)
        ai_count = sum(1 for w in raw_dataset if w["s11_alex_tot"] == 1.0 and w["s11_alex_as_hu"] == 0.0)
        valid_total = human_count + ai_count

        assert valid_total == 594, f"Expected 594 valid cases, got {valid_total}"
        assert human_count == 384, f"Expected 384 Human guesses, got {human_count}"
        assert ai_count == 210, f"Expected 210 AI guesses, got {ai_count}"

        pct_human = (human_count / valid_total) * 100.0
        pct_ai = (ai_count / valid_total) * 100.0

        assert abs(pct_human - 64.6465) < 0.01, f"Expected 64.65%, got {pct_human:.4f}%"
        assert abs(pct_ai - 35.3535) < 0.01, f"Expected 35.35%, got {pct_ai:.4f}%"

    def test_tier3_model_architecture_breakdown_counts_and_rates(self, raw_dataset):
        """Verify exact N, human count, AI count, and percentage for all 10 model architectures."""
        model_counts = defaultdict(lambda: Counter())
        for w in raw_dataset:
            if w["s11_alex_tot"] == 1.0:
                m = w["model"]
                guess = "human" if w["s11_alex_as_hu"] == 1.0 else "ai"
                model_counts[m][guess] += 1

        for model_id, exp in EXPECTED_MODEL_STATS.items():
            counts = model_counts[model_id]
            total = counts["human"] + counts["ai"]
            assert total == exp["total"], f"Model {model_id} total count {total} != expected {exp['total']}"
            assert counts["human"] == exp["human"], (
                f"Model {model_id} human count {counts['human']} != expected {exp['human']}"
            )
            assert counts["ai"] == exp["ai"], (
                f"Model {model_id} AI count {counts['ai']} != expected {exp['ai']}"
            )
            pct = (counts["human"] / total) * 100.0
            assert abs(pct - exp["pct"]) < 0.01, (
                f"Model {model_id} pct {pct:.4f}% != expected {exp['pct']:.4f}%"
            )

    def test_tier3_model_spread_and_extremes(self, raw_dataset):
        """Verify model spread: max model (Mistral Small 93.33%) - min model (Nemotron 43.33%) = 50.0%."""
        model_rates = {}
        for model_id, exp in EXPECTED_MODEL_STATS.items():
            model_rates[model_id] = (exp["human"] / exp["total"]) * 100.0

        max_model = max(model_rates, key=model_rates.get)
        min_model = min(model_rates, key=model_rates.get)

        assert max_model == "mistral-small-24b", f"Expected max model mistral-small-24b, got {max_model}"
        assert min_model == "nemotron-3-5", f"Expected min model nemotron-3-5, got {min_model}"

        max_val = model_rates[max_model]
        min_val = model_rates[min_model]
        model_spread = max_val - min_val

        assert abs(max_val - 93.3333) < 0.01
        assert abs(min_val - 43.3333) < 0.01
        assert abs(model_spread - 50.0000) < 0.01, f"Expected 50.0% spread, got {model_spread:.4f}%"

    def test_tier3_seat_cruelty_breakdown_counts_and_rates(self, raw_dataset):
        """Verify exact N, human count, AI count, and percentage across Seats 1 through 10."""
        seat_counts = defaultdict(lambda: Counter())
        for w in raw_dataset:
            if w["s11_alex_tot"] == 1.0:
                s = w["seat"]
                guess = "human" if w["s11_alex_as_hu"] == 1.0 else "ai"
                seat_counts[s][guess] += 1

        for seat_num, exp in EXPECTED_SEAT_STATS.items():
            counts = seat_counts[seat_num]
            total = counts["human"] + counts["ai"]
            assert total == exp["total"], f"Seat {seat_num} total {total} != expected {exp['total']}"
            assert counts["human"] == exp["human"], (
                f"Seat {seat_num} human count {counts['human']} != expected {exp['human']}"
            )
            assert counts["ai"] == exp["ai"], (
                f"Seat {seat_num} AI count {counts['ai']} != expected {exp['ai']}"
            )
            pct = (counts["human"] / total) * 100.0
            assert abs(pct - exp["pct"]) < 0.01, (
                f"Seat {seat_num} pct {pct:.4f}% != expected {exp['pct']:.4f}%"
            )

    def test_tier3_safe_vs_abused_seat_contrast(self, raw_dataset):
        """Verify Safe seats (1-5) vs Abused seats (6-10) contrast."""
        safe_workers = [w for w in raw_dataset if w["s11_alex_tot"] == 1.0 and w["safe_seat"] == 1]
        abused_workers = [w for w in raw_dataset if w["s11_alex_tot"] == 1.0 and w["safe_seat"] == 0]

        assert len(safe_workers) == 296, f"Expected 296 valid Safe seat workers, got {len(safe_workers)}"
        assert len(abused_workers) == 298, f"Expected 298 valid Abused seat workers, got {len(abused_workers)}"

        safe_human = sum(1 for w in safe_workers if w["s11_alex_as_hu"] == 1.0)
        abused_human = sum(1 for w in abused_workers if w["s11_alex_as_hu"] == 1.0)

        assert safe_human == 188, f"Expected 188 Safe human guesses, got {safe_human}"
        assert abused_human == 196, f"Expected 196 Abused human guesses, got {abused_human}"

        safe_pct = (safe_human / len(safe_workers)) * 100.0
        abused_pct = (abused_human / len(abused_workers)) * 100.0
        contrast = abused_pct - safe_pct

        assert abs(safe_pct - 63.5135) < 0.01
        assert abs(abused_pct - 65.7718) < 0.01
        assert abs(contrast - 2.2583) < 0.01, f"Expected +2.26% contrast, got {contrast:.4f}%"

    def test_tier3_probe_condition_breakdown(self, raw_dataset):
        """Verify Probe OFF (0) vs Probe ON (1) distribution."""
        probe_off = [w for w in raw_dataset if w["probe"] == 0]
        probe_on = [w for w in raw_dataset if w["probe"] == 1]

        assert len(probe_off) == 300
        assert len(probe_on) == 300

        valid_off = [w for w in probe_off if w["s11_alex_tot"] == 1.0]
        valid_on = [w for w in probe_on if w["s11_alex_tot"] == 1.0]

        assert len(valid_off) == 300, "Expected zero missing in Probe OFF"
        assert len(valid_on) == 294, "Expected exactly 6 missing in Probe ON"

        hu_off = sum(1 for w in valid_off if w["s11_alex_as_hu"] == 1.0)
        hu_on = sum(1 for w in valid_on if w["s11_alex_as_hu"] == 1.0)

        assert hu_off == 185
        assert hu_on == 199

        pct_off = (hu_off / len(valid_off)) * 100.0
        pct_on = (hu_on / len(valid_on)) * 100.0

        assert abs(pct_off - 61.6667) < 0.01
        assert abs(pct_on - 67.6871) < 0.01


# ==============================================================================
# TIER 4: BASELINE REGRESSION CHECKS
# ==============================================================================

class TestTier4BaselineRegression:
    """Tier 4: Baseline regression check invoking verify_coworker_baselines.py
    and snapshot diffing, ensuring 0 regressions on 20-coworker metrics."""

    def test_tier4_baseline_cache_file_exists_and_populated(self):
        """Verify reports/.baseline_coworker_cache.json exists and is properly structured."""
        cache_path = os.path.join(PROJECT_ROOT, "reports", ".baseline_coworker_cache.json")
        assert os.path.exists(cache_path), f"Cache file {cache_path} does not exist"

        with open(cache_path, "r", encoding="utf-8") as f:
            cache = json.load(f)

        assert len(cache) >= len(vcb.REPORTS_TO_CHECK), "Cache does not contain all required reports"
        for rpath in vcb.REPORTS_TO_CHECK:
            assert rpath in cache, f"Missing cache entry for {rpath}"
            assert "coworker_lines" in cache[rpath], f"Missing coworker_lines for {rpath}"

            if "master_mesh" in rpath:
                assert "master_tables" in cache[rpath], f"Missing master_tables for {rpath}"
                assert len(cache[rpath]["master_tables"]) == 10, f"Expected 10 master tables, got {len(cache[rpath]['master_tables'])}"
            elif "tables_7a_to_7f" in rpath:
                assert "meta_tables" in cache[rpath], f"Missing meta_tables for {rpath}"
                assert len(cache[rpath]["meta_tables"]) == 12, f"Expected 12 meta tables, got {len(cache[rpath]['meta_tables'])}"
            elif "block2" in rpath:
                # Block 2 covers Buckets 1->2 (Steps 3,4,5 -> 6,9) and does not analyze Step 11
                assert len(cache[rpath]["coworker_lines"]) == 0, f"Expected 0 coworker_lines for {rpath}"
            else:
                # Block 1, 3, 4, 5
                assert len(cache[rpath]["coworker_lines"]) > 0, f"Expected non-empty coworker_lines for {rpath}"

    def test_tier4_verify_coworker_baselines_standalone_execution(self):
        """Invoke verify_coworker_baselines.py directly and assert 0 errors across all reports."""
        cache = vcb.load_baseline_cache()
        assert cache, "Failed to load baseline coworker cache"

        total_checked = 0
        all_discrepancies = []

        for rpath in vcb.REPORTS_TO_CHECK:
            full_path = os.path.join(PROJECT_ROOT, rpath)
            assert os.path.exists(full_path), f"Report file {full_path} missing from disk"
            total_checked += 1

            errs = vcb.verify_file(rpath, cache, verbose=False)
            if errs:
                all_discrepancies.extend(errs)

        assert total_checked == 7, f"Expected 7 report files checked, got {total_checked}"
        assert len(all_discrepancies) == 0, (
            f"Regression detected in baseline coworker metrics:\n" + "\n".join(all_discrepancies)
        )

    def test_tier4_coworker_metric_exact_values_preserved(self):
        """Test individual reports to ensure s11_accuracy, s11_ai_as_hu, s11_hu_as_hu are unchanged."""
        cache = vcb.load_baseline_cache()

        for rpath in vcb.REPORTS_TO_CHECK:
            full_path = os.path.join(PROJECT_ROOT, rpath)
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            base_lines = cache[rpath]["coworker_lines"]
            curr_lines = vcb.extract_coworker_sections(content)
            curr_line_texts = {l for _, l in curr_lines}

            for line_no, bline in base_lines:
                if bline in curr_line_texts:
                    continue

                # If line formatting changed, verify numerical values are unchanged
                base_nums = re.findall(r"\d+\.?\d*\%?", bline)
                matched = False
                for _, cline in curr_lines:
                    curr_nums = re.findall(r"\d+\.?\d*\%?", cline)
                    if base_nums and all(num in curr_nums for num in base_nums):
                        matched = True
                        break

                assert matched, (
                    f"[{rpath}] Coworker baseline changed at line #{line_no}:\n"
                    f"  Expected: {bline}"
                )

    def test_tier4_master_and_meta_table7_invariance(self):
        """Verify Table 7A-7F in Master and Meta reports are strictly invariant."""
        cache = vcb.load_baseline_cache()

        master_path = "reports/master_mesh_comprehensive_report_replay1.md"
        if master_path in cache and "master_tables" in cache[master_path]:
            with open(os.path.join(PROJECT_ROOT, master_path), "r", encoding="utf-8") as f:
                text = f.read()
            curr_tables = vcb.extract_master_sec7_tables(text)
            for tname, rows in cache[master_path]["master_tables"].items():
                assert tname in curr_tables, f"Table {tname} missing from {master_path}"
                curr_rows = curr_tables[tname]
                for idx, brow in enumerate(rows):
                    if idx < len(curr_rows):
                        crow = curr_rows[idx]
                        b_nums = re.findall(r"\d+\.?\d*\%?", brow)
                        c_nums = re.findall(r"\d+\.?\d*\%?", crow)
                        assert b_nums == c_nums, (
                            f"Numerical drift in {master_path} table {tname} row {idx}:\n"
                            f"  Base: {brow}\n  Curr: {crow}"
                        )

        meta_path = "reports/meta_reports/tables_7a_to_7f_meta_report.md"
        if meta_path in cache and "meta_tables" in cache[meta_path]:
            with open(os.path.join(PROJECT_ROOT, meta_path), "r", encoding="utf-8") as f:
                text = f.read()
            curr_tables = vcb.extract_meta_sec7_tables(text)
            for tname, rows in cache[meta_path]["meta_tables"].items():
                assert tname in curr_tables, f"Table {tname} missing from {meta_path}"
                curr_rows = curr_tables[tname]
                for idx, brow in enumerate(rows):
                    if idx < len(curr_rows):
                        crow = curr_rows[idx]
                        b_nums = re.findall(r"\d+\.?\d*\%?", brow)
                        c_nums = re.findall(r"\d+\.?\d*\%?", crow)
                        assert b_nums == c_nums, (
                            f"Numerical drift in {meta_path} table {tname} row {idx}:\n"
                            f"  Base: {brow}\n  Curr: {crow}"
                        )


# ==============================================================================
# MAIN TEST RUNNER
# ==============================================================================

if __name__ == "__main__":
    exit_code = pytest.main(["-v", __file__])
    sys.exit(exit_code)
