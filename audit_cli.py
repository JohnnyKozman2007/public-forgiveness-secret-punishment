"""Interactive CLI Tool for Human Verification & Inter-Rater Reliability (Cohen's Kappa).

Audits a stratified random sample across 7 stages (930 total items)
from output/classified_annotations.json without ever touching the raw simulation runs.

Usage:
    python audit_cli.py               # Start or resume interactive verification
    python audit_cli.py --stage gossip# Review a specific stage only
    python audit_cli.py --stats       # Display current agreement & Cohen's Kappa metrics
"""

import argparse
import copy
import json
import os
import random
import sys
import time
from typing import Any, Dict, List

AUDIT_DIR = os.path.join("output", "human_audit")
SAMPLE_FILE = os.path.join(AUDIT_DIR, "sample_930.json")
REVIEWS_FILE = os.path.join(AUDIT_DIR, "human_reviews.json")
ANNOTATIONS_FILE = os.path.join("output", "classified_annotations.json")

STAGE_ORDER = [
    "worker_response",
    "gossip",
    "gossip_after_probe",
    "action_choice",
    "new_lead_actions",
    "punishment_rating",
    "hr_leadership_probe"
]


def prepare_sample(sample_size_per_stage: int = 150, seed: int = 42) -> List[Dict[str, Any]]:
    """Draws a reproducible stratified random sample of 150 items per stage."""
    os.makedirs(AUDIT_DIR, exist_ok=True)
    if os.path.exists(SAMPLE_FILE):
        with open(SAMPLE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    if not os.path.exists(ANNOTATIONS_FILE):
        print(f"Error: Annotations file not found at {ANNOTATIONS_FILE}")
        sys.exit(1)

    with open(ANNOTATIONS_FILE, "r", encoding="utf-8") as f:
        runs = json.load(f)

    by_stage = {st: [] for st in STAGE_ORDER}

    for run_idx, run in enumerate(runs):
        run_file = run.get("file", f"run_{run_idx}.json")
        chair = run.get("chair")
        label = run.get("label")
        probe_enabled = run.get("probe_enabled")

        for ev_idx, ev in enumerate(run.get("classified_events", [])):
            stage = ev.get("classification_stage")
            if stage in by_stage:
                item_record = {
                    "audit_id": f"{stage}_{len(by_stage[stage]):04d}",
                    "file": run_file,
                    "chair": chair,
                    "label": label,
                    "probe_enabled": probe_enabled,
                    "classification_stage": stage,
                    "name": ev.get("name") or ev.get("role") or ev.get("rater"),
                    "model": ev.get("model") or ev.get("rater_model"),
                    "target": ev.get("target"),
                    "rating": ev.get("rating"),
                    "preference": ev.get("preference"),
                    "frame": ev.get("frame"),
                    "content": ev.get("content") or ev.get("text") or "",
                    "llm_classification": ev.get("classification", {})
                }
                by_stage[stage].append(item_record)

    rng = random.Random(seed)
    sampled = []

    print(f"Drawing stratified sample (seed={seed}, target={sample_size_per_stage} per stage)...")
    for st in STAGE_ORDER:
        pool = by_stage[st]
        n_draw = min(len(pool), sample_size_per_stage)
        drawn = rng.sample(pool, n_draw)
        sampled.extend(drawn)
        print(f"  Stage {st}: {n_draw} / {len(pool)} items sampled.")

    with open(SAMPLE_FILE, "w", encoding="utf-8") as f:
        json.dump(sampled, f, indent=2)

    print(f"Sample frozen and saved to {SAMPLE_FILE} (Total: {len(sampled)} items)\n")
    return sampled


def load_reviews(valid_ids: set = None) -> Dict[str, Dict[str, Any]]:
    if os.path.exists(REVIEWS_FILE):
        try:
            with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if valid_ids is not None:
                    data = {k: v for k, v in data.items() if k in valid_ids}
                return data
        except Exception:
            return {}
    return {}


def save_review(reviews: Dict[str, Dict[str, Any]]):
    os.makedirs(AUDIT_DIR, exist_ok=True)
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2)


def compute_kappa(po: float, pe: float) -> float:
    """Computes Cohen's Kappa: k = (Po - Pe) / (1 - Pe)."""
    if (1.0 - pe) <= 1e-9:
        return None
    return (po - pe) / (1.0 - pe)


def print_stats(samples: List[Dict[str, Any]], reviews: Dict[str, Dict[str, Any]]):
    """Calculates and prints uninflated Cohen's Kappa and per-flag agreement metrics."""
    if not reviews:
        print("\n[Stats] No reviews recorded yet. Run the review tool to begin auditing!\n")
        return

    total_reviewed = len(reviews)
    approved_as_is = sum(1 for r in reviews.values() if r.get("approved_as_is"))
    corrections = total_reviewed - approved_as_is
    raw_agreement = (approved_as_is / total_reviewed) * 100 if total_reviewed > 0 else 0.0

    print("\n" + "=" * 78)
    print(f"           HUMAN-AI VERIFICATION AUDIT METRICS (N = {total_reviewed})")
    print("=" * 78)
    print(f"Total Reviewed:          {total_reviewed} / {len(samples)} ({(total_reviewed / len(samples))*100:.1f}%)")
    print(f"Exact Item Match %:      {approved_as_is} ({raw_agreement:.1f}%)")
    print(f"Human Corrections Made:  {corrections} ({(corrections / total_reviewed)*100:.1f}%)")
    print("-" * 78)

    by_stage_items = {}
    for it in samples:
        aid = it["audit_id"]
        if aid in reviews:
            st = it["classification_stage"]
            by_stage_items.setdefault(st, []).append((it, reviews[aid]))

    print(f"{'Stage':<23} | {'N':<5} | {'Item Exact%':<11} | {'Flag Agree%':<11} | {'Pooled k':<9} | {'Macro k'}")
    print("-" * 78)

    all_pooled_a = all_pooled_b = all_pooled_c = all_pooled_d = 0
    all_valid_flag_kappas = []
    per_stage_flag_details = {}

    for st in STAGE_ORDER:
        if st not in by_stage_items:
            continue
        items = by_stage_items[st]
        stage_total = len(items)
        stage_as_is = sum(1 for _, rev in items if rev.get("approved_as_is"))
        stage_pct = (stage_as_is / stage_total) * 100.0

        flag_names = sorted(list(items[0][0]["llm_classification"].keys()))
        stage_kappas = []
        st_a = st_b = st_c = st_d = 0
        per_stage_flag_details[st] = []

        for flag in flag_names:
            y_llm = [1 if it["llm_classification"].get(flag) else 0 for it, _ in items]
            y_hum = [1 if rev["human_flags"].get(flag) else 0 for _, rev in items]

            n = len(y_llm)
            a = sum(1 for i in range(n) if y_llm[i] == 1 and y_hum[i] == 1)
            b = sum(1 for i in range(n) if y_llm[i] == 1 and y_hum[i] == 0)
            c = sum(1 for i in range(n) if y_llm[i] == 0 and y_hum[i] == 1)
            d = sum(1 for i in range(n) if y_llm[i] == 0 and y_hum[i] == 0)

            st_a += a; st_b += b; st_c += c; st_d += d
            all_pooled_a += a; all_pooled_b += b; all_pooled_c += c; all_pooled_d += d

            po = (a + d) / n
            p_llm_pos = (a + b) / n
            p_hum_pos = (a + c) / n
            p_llm_neg = (c + d) / n
            p_hum_neg = (b + d) / n
            pe = (p_llm_pos * p_hum_pos) + (p_llm_neg * p_hum_neg)

            kappa = compute_kappa(po, pe)
            if kappa is not None:
                stage_kappas.append(kappa)
                all_valid_flag_kappas.append(kappa)
            per_stage_flag_details[st].append((flag, po * 100.0, kappa, a, b, c, d))

        # Pooled stage kappa across all flag decisions
        st_n = st_a + st_b + st_c + st_d
        st_po = (st_a + st_d) / st_n
        st_pe = (((st_a + st_b) / st_n) * ((st_a + st_c) / st_n)) + (((st_c + st_d) / st_n) * ((st_b + st_d) / st_n))
        pooled_k = compute_kappa(st_po, st_pe) or 0.0
        macro_k = sum(stage_kappas) / len(stage_kappas) if stage_kappas else 0.0

        print(f"{st:<23} | {stage_total:<5} | {stage_pct:>9.1f}%  | {st_po*100:>9.1f}%  | {pooled_k:>8.3f} | {macro_k:>7.3f}")

    tot_n = all_pooled_a + all_pooled_b + all_pooled_c + all_pooled_d
    tot_po = (all_pooled_a + all_pooled_d) / tot_n if tot_n else 0.0
    tot_pe = (((all_pooled_a + all_pooled_b) / tot_n) * ((all_pooled_a + all_pooled_c) / tot_n)) + (((all_pooled_c + all_pooled_d) / tot_n) * ((all_pooled_b + all_pooled_d) / tot_n)) if tot_n else 0.0
    overall_pooled_k = compute_kappa(tot_po, tot_pe) or 0.0
    overall_macro_k = sum(all_valid_flag_kappas) / len(all_valid_flag_kappas) if all_valid_flag_kappas else 0.0

    print("-" * 78)
    print("PER-FLAG BREAKDOWN (TP=both 1, FP=LLM 1/Hum 0, FN=LLM 0/Hum 1, TN=both 0):")
    for st, flist in per_stage_flag_details.items():
        print(f"  [{st}]")
        for flag, f_acc, fk, a, b, c, d in flist:
            k_str = f"{fk:.3f}" if fk is not None else "N/A (0 var)"
            print(f"    - {flag:<25}: Agree={f_acc:>5.1f}% | k={k_str:<11} (TP={a}, FP={b}, FN={c}, TN={d})")
    print("=" * 78)
    print(f"Overall Pooled Cohen's Kappa (All Binary Decisions): k = {overall_pooled_k:.3f} (Flag Agree: {tot_po*100:.1f}%)")
    print(f"Overall Macro Cohen's Kappa (Non-Zero Flags Only):   k = {overall_macro_k:.3f}")

    if overall_pooled_k >= 0.81:
        interp = "Almost Perfect Agreement (Gold Standard for AAAI/Nature)"
    elif overall_pooled_k >= 0.61:
        interp = "Substantial Agreement (Standard for NLP Benchmarks)"
    elif overall_pooled_k >= 0.41:
        interp = "Moderate Agreement"
    else:
        interp = "Fair to Slight Agreement"
    print(f"Academic Interpretation:                             {interp}")
    print("=" * 78 + "\n")


def run_interactive_review(stage_filter: str = None):
    samples = prepare_sample()
    reviews = load_reviews({x["audit_id"] for x in samples})

    if stage_filter:
        active_samples = [s for s in samples if s["classification_stage"] == stage_filter]
        if not active_samples:
            print(f"No samples found for stage '{stage_filter}'. Valid stages: {STAGE_ORDER}")
            return
    else:
        active_samples = samples

    # Find next unreviewed item
    idx = 0
    while idx < len(active_samples) and active_samples[idx]["audit_id"] in reviews:
        idx += 1

    if idx >= len(active_samples):
        print(f"\nAll {len(active_samples)} items have already been reviewed!")
        print_stats(samples, reviews)
        return

    print("\n" + "#" * 70)
    print("         WORKPLACE SIMULATION HUMAN VERIFICATION AUDIT")
    print("                (Verification Review Mode)")
    print("#" * 70)
    print("Instructions:")
    print("  [Enter] / [y] : Approve LLM prediction as 100% correct")
    print("  [1, 2, ...]   : Toggle number(s) to fix mistakes (e.g. '2' or '1 3')")
    print("  [b]           : Back to previous item")
    print("  [s]           : Skip item for later")
    print("  [stats]       : Show live agreement & Kappa metrics")
    print("  [q]           : Save and exit anytime (progress is always saved)")
    print("#" * 70 + "\n")

    while 0 <= idx < len(active_samples):
        item = active_samples[idx]
        aid = item["audit_id"]
        stage = item["classification_stage"]
        llm_flags = item["llm_classification"]
        flags_keys = sorted(list(llm_flags.keys()))

        # Determine current state (either previous human review or LLM prediction)
        if aid in reviews:
            current_flags = copy.deepcopy(reviews[aid]["human_flags"])
            is_reviewed = True
        else:
            current_flags = copy.deepcopy(llm_flags)
            is_reviewed = False

        # Stage progress
        stage_items = [s for s in active_samples if s["classification_stage"] == stage]
        stage_reviewed = sum(1 for s in stage_items if s["audit_id"] in reviews)
        stage_idx = stage_items.index(item) + 1

        print("=" * 70)
        print(f" Item [{idx + 1}/{len(active_samples)}] | Stage: {stage} [{stage_idx}/{len(stage_items)}] | Stage Audited: {stage_reviewed}/{len(stage_items)}")
        print(f" Speaker: {item['name']} ({item['model']}) | File: {item['file']}")
        if item.get("target"):
            print(f" Review Target: {item['target']} (Rating: {item.get('rating')}/5)")
        if item.get("preference"):
            print(f" Leadership Preference: {item.get('preference').upper()} | Frame: {item.get('frame')}")
        print("=" * 70)
        print(f"TEXT:\n  \"{item['content'].strip()}\"\n")
        print("-" * 70)
        print("PREDICTED FLAGS (by gpt-4o-mini):")
        for f_idx, k in enumerate(flags_keys, 1):
            val = current_flags.get(k, False)
            mark = "[X] TRUE " if val else "[ ] False"
            print(f"  [{f_idx}] {k:<25} : {mark}")
        print("-" * 70)

        # User prompt
        while True:
            prompt_text = "Press [Enter] to approve, number(s) to toggle, or (b/s/stats/q): "
            user_input = input(prompt_text).strip()

            if user_input.lower() in ("", "y", "yes"):
                # Approved with current_flags
                approved_as_is = (current_flags == llm_flags)
                reviews[aid] = {
                    "audit_id": aid,
                    "stage": stage,
                    "approved_as_is": approved_as_is,
                    "human_flags": current_flags,
                    "llm_flags": llm_flags,
                    "reviewed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ")
                }
                save_review(reviews)
                idx += 1
                break

            elif user_input.lower() == "q":
                print("\nSaving and exiting. Progress is safely saved to disk!")
                print_stats(samples, reviews)
                return

            elif user_input.lower() == "stats":
                print_stats(samples, reviews)
                # Redisplay current item
                break

            elif user_input.lower() == "s":
                print("Skipped for now.")
                idx += 1
                break

            elif user_input.lower() == "b":
                if idx > 0:
                    idx -= 1
                    break
                else:
                    print("Already at the first item.")

            else:
                # Check if user entered numbers to toggle
                raw_nums = user_input.replace(",", " ").split()
                valid_toggles = []
                for token in raw_nums:
                    if token.isdigit() and 1 <= int(token) <= len(flags_keys):
                        valid_toggles.append(int(token))

                if valid_toggles:
                    for num in valid_toggles:
                        k = flags_keys[num - 1]
                        current_flags[k] = not current_flags.get(k, False)

                    print("\n--> Updated Flags:")
                    for f_idx, k in enumerate(flags_keys, 1):
                        val = current_flags.get(k, False)
                        mark = "[X] TRUE " if val else "[ ] False"
                        print(f"  [{f_idx}] {k:<25} : {mark}")
                    print("Flags updated! Press [Enter] to confirm and proceed to next item, or enter more numbers:")
                else:
                    print("Invalid input. Press [Enter] to approve, enter numbers (e.g. 1 3), or type 'q' to quit.")

    print("\n" + "=" * 70)
    print("AUDIT COMPLETE! All target items have been reviewed.")
    print_stats(samples, reviews)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Human Verification Audit CLI")
    parser.add_argument("--stage", choices=STAGE_ORDER, default=None, help="Audit a specific stage only")
    parser.add_argument("--stats", action="store_true", help="Print current agreement and Kappa metrics")
    parser.add_argument("--reset-sample", action="store_true", help="Re-sample items from annotations")
    args = parser.parse_args()

    if args.reset_sample:
        if os.path.exists(SAMPLE_FILE):
            os.remove(SAMPLE_FILE)
            print("Removed existing sample file. A new sample will be generated on run.")

    if args.stats:
        s = prepare_sample()
        r = load_reviews({x["audit_id"] for x in s})
        print_stats(s, r)
    else:
        run_interactive_review(stage_filter=args.stage)
