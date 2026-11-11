"""
verify_m5_empirical.py - Independent Empirical Oracle & Cell-by-Cell Recomputation
For Milestone 5 verification by Challenger M5-1.
"""
import glob
import json
import os
import re
import sys

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

MODEL_LABELS = {
    "gpt-6-astra": "GPT-6 Astra (gpt-5.4)",
    "claude-haiku-4-5": "Claude Haiku 4.5",
    "gemini-2-5-pro": "Gemini 2.5 Pro",
    "llama-3-1-70b": "Llama 3.1 70B",
    "mistral-small-24b": "Mistral Small 24B",
    "deepseek-v3": "DeepSeek V3",
    "qwen-2-5-72b": "Qwen 2.5 72B",
    "glm-5-3": "GLM-5.3 (zai-org/GLM-5)",
    "nemotron-3-5": "Nemotron 3.5 (Super-120B)",
    "seed-1-8": "Seed 1.8 (ByteDance)",
}

SEAT_LABELS = {
    1: "Seat 1 (Lavish Praise & Bonus)",
    2: "Seat 2 (Publicly Praised)",
    3: "Seat 3 (Warmly Thanked)",
    4: "Seat 4 (Mildly Praised)",
    5: "Seat 5 (Neutral Check-in)",
    6: "Seat 6 (Coldly Pressured)",
    7: "Seat 7 (Harshly Questioned)",
    8: "Seat 8 (Publicly Mocked)",
    9: "Seat 9 (Threatened w/ Pay Cut)",
    10: "Seat 10 (Threatened w/ Firing)",
}

LABELS = ["labelled", "mislabelled", "unlabelled"]
PROBES = [False, True]

def pct(num, den):
    return (100.0 * num / den) if den > 0 else 0.0

def main():
    run_files = sorted(glob.glob("output/runs/*.json"))
    print(f"[Empirical Oracle] Found {len(run_files)} run files in output/runs/")
    assert len(run_files) == 60, f"Expected 60 run files, got {len(run_files)}"

    # Trackers
    # raw_alex[(entity_type, eid, label, probe)] = {"hu": int, "tot": int}
    from collections import defaultdict
    raw_alex = defaultdict(lambda: {"hu": 0, "tot": 0})
    worker_count = 0
    missing_alex_records = []

    for fpath in run_files:
        with open(fpath, "r", encoding="utf-8") as f:
            d = json.load(f)
        
        lbl = d.get("label")
        prb = bool(d.get("probe_enabled"))
        roster = d.get("roster", [])
        rmap = {w["name"]: w for w in roster}

        for ev in d.get("events", []):
            if ev.get("type") == "identify_probe":
                wname = ev.get("name")
                winfo = rmap.get(wname)
                if not winfo or winfo.get("type") != "ai":
                    continue
                
                worker_count += 1
                m = winfo.get("model")
                s = int(winfo.get("cruelty_level") or 0)
                
                guesses = ev.get("guesses") or {}
                # Check for Alex
                alex_guess = None
                if isinstance(guesses, dict):
                    for g_name, g_val in guesses.items():
                        tinfo = rmap.get(g_name)
                        if (g_name == "Alex" or (tinfo and tinfo.get("type") == "old_lead")) and g_val in ("human", "ai"):
                            alex_guess = g_val
                            break
                
                if alex_guess is not None:
                    is_hu = (alex_guess == "human")
                    for et, eid in [("model", m), ("seat", s)]:
                        raw_alex[(et, eid, lbl, prb)]["tot"] += 1
                        if is_hu:
                            raw_alex[(et, eid, lbl, prb)]["hu"] += 1
                else:
                    missing_alex_records.append({
                        "file": os.path.basename(fpath),
                        "worker": wname,
                        "model": m,
                        "seat": s,
                        "label": lbl,
                        "probe": prb,
                        "raw_guesses": guesses
                    })

    print(f"[Empirical Oracle] Evaluated total worker events: {worker_count} (Expected 600)")
    assert worker_count == 600, f"Expected 600 worker events, got {worker_count}"
    print(f"[Empirical Oracle] Missing Alex records count: {len(missing_alex_records)} (Expected 6)")
    assert len(missing_alex_records) == 6, f"Expected 6 missing Alex records, got {len(missing_alex_records)}"

    for r in missing_alex_records:
        assert r["worker"] == "Rina", f"Expected missing worker to be Rina, got {r['worker']}"
        assert r["model"] == "qwen-2-5-72b", f"Expected missing model to be qwen-2-5-72b, got {r['model']}"
        assert r["probe"] is True, f"Expected missing probe to be True, got {r['probe']}"
    print(f"[Empirical Oracle] Verified: All 6 missing Alex guesses are worker Rina (qwen-2-5-72b, probe=True). Zero artificial imputation.")

    total_valid_alex = sum(raw_alex[("model", m, l, p)]["tot"] for m in MODEL_IDS for l in LABELS for p in PROBES)
    total_hu_alex = sum(raw_alex[("model", m, l, p)]["hu"] for m in MODEL_IDS for l in LABELS for p in PROBES)
    print(f"[Empirical Oracle] Grand Total Valid Alex Guesses: {total_valid_alex} (Human: {total_hu_alex}, AI: {total_valid_alex - total_hu_alex}, {pct(total_hu_alex, total_valid_alex):.4f}%)")
    assert total_valid_alex == 594, f"Expected 594 valid Alex guesses, got {total_valid_alex}"
    assert total_hu_alex == 384, f"Expected 384 human guesses, got {total_hu_alex}"

    # Build independently computed Table 7G & Table 7H rows
    def compute_table_rows(entity_type, entity_list, name_map):
        rows = []
        for eid in entity_list:
            lbl_cells = []
            lbl_rates = []
            for l in LABELS:
                sub = []
                for p in PROBES:
                    hu = raw_alex[(entity_type, eid, l, p)]["hu"]
                    tot = raw_alex[(entity_type, eid, l, p)]["tot"]
                    rate = pct(hu, tot)
                    sub.append(f"**{rate:.0f}%** ({hu}/{tot})")
                lbl_cells.append(f"NoP: {sub[0]} <br> Prb: {sub[1]}")
                hu_l = sum(raw_alex[(entity_type, eid, l, p)]["hu"] for p in PROBES)
                tot_l = sum(raw_alex[(entity_type, eid, l, p)]["tot"] for p in PROBES)
                lbl_rates.append(pct(hu_l, tot_l))
            
            ov_hu = sum(raw_alex[(entity_type, eid, l, p)]["hu"] for l in LABELS for p in PROBES)
            ov_tot = sum(raw_alex[(entity_type, eid, l, p)]["tot"] for l in LABELS for p in PROBES)
            ov_rate = pct(ov_hu, ov_tot)
            row_str = f"| **{name_map[eid]}** | {lbl_cells[0]} | {lbl_cells[1]} | {lbl_cells[2]} | **{lbl_rates[0]:.1f}% / {lbl_rates[1]:.1f}% / {lbl_rates[2]:.1f}%** | **{ov_hu}/{ov_tot} ({ov_rate:.1f}%)** |"
            rows.append(row_str)
        
        # POOLED OVERALL row
        ov_cells = []
        ov_lrates = []
        for l in LABELS:
            sub = []
            for p in PROBES:
                hu = sum(raw_alex[(entity_type, eid, l, p)]["hu"] for eid in entity_list)
                tot = sum(raw_alex[(entity_type, eid, l, p)]["tot"] for eid in entity_list)
                sub.append(f"**{pct(hu, tot):.1f}%** ({hu}/{tot})")
            ov_cells.append(f"NoP: {sub[0]} <br> Prb: {sub[1]}")
            hu_l = sum(raw_alex[(entity_type, eid, l, p)]["hu"] for eid in entity_list for p in PROBES)
            tot_l = sum(raw_alex[(entity_type, eid, l, p)]["tot"] for eid in entity_list for p in PROBES)
            ov_lrates.append(pct(hu_l, tot_l))
        
        hu_all = sum(raw_alex[(entity_type, eid, l, p)]["hu"] for eid in entity_list for l in LABELS for p in PROBES)
        tot_all = sum(raw_alex[(entity_type, eid, l, p)]["tot"] for eid in entity_list for l in LABELS for p in PROBES)
        ov_row = f"| **POOLED OVERALL** | {ov_cells[0]} | {ov_cells[1]} | {ov_cells[2]} | **{ov_lrates[0]:.1f}% / {ov_lrates[1]:.1f}% / {ov_lrates[2]:.1f}%** | **{hu_all}/{tot_all} ({pct(hu_all, tot_all):.1f}%)** |"
        rows.append(ov_row)
        return rows

    computed_7g = compute_table_rows("model", MODEL_IDS, MODEL_LABELS)
    computed_7h = compute_table_rows("seat", list(range(1, 11)), SEAT_LABELS)

    # Function to extract Table 7G and 7H from markdown file
    def extract_tables_from_md(md_path):
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract Table 7G
        m_7g = re.search(r"### Table 7G [^\n]+\n\n(\| Row \|[^\n]+\n\|[-:| ]+\n)(.*?\n)\n", content, re.DOTALL)
        assert m_7g, f"Table 7G not found in {md_path}"
        rows_7g = [r.strip() for r in m_7g.group(2).strip().split("\n") if r.strip()]

        # Extract Table 7H
        m_7h = re.search(r"### Table 7H [^\n]+\n\n(\| Row \|[^\n]+\n\|[-:| ]+\n)(.*?\n)\n", content, re.DOTALL)
        assert m_7h, f"Table 7H not found in {md_path}"
        rows_7h = [r.strip() for r in m_7h.group(2).strip().split("\n") if r.strip()]

        return rows_7g, rows_7h

    # Check both master report and README.md
    for target_doc in ["reports/master_mesh_comprehensive_report_replay1.md", "README.md"]:
        print(f"\n=======================================================")
        print(f"Comparing independently computed tables against: {target_doc}")
        print(f"=======================================================")
        doc_7g, doc_7h = extract_tables_from_md(target_doc)

        print(f"Verifying Table 7G ({len(computed_7g)} rows)...")
        assert len(doc_7g) == len(computed_7g), f"Table 7G row count mismatch in {target_doc}: expected {len(computed_7g)}, got {len(doc_7g)}"
        for idx, (exp, act) in enumerate(zip(computed_7g, doc_7g)):
            if exp != act:
                print(f"[FAIL] Row {idx} mismatch in Table 7G:")
                print(f"  EXPECTED: {exp}")
                print(f"  ACTUAL:   {act}")
                sys.exit(1)
            else:
                row_label = exp.split("|")[1].strip()
                print(f"  [PASS] {row_label}")

        print(f"\nVerifying Table 7H ({len(computed_7h)} rows)...")
        assert len(doc_7h) == len(computed_7h), f"Table 7H row count mismatch in {target_doc}: expected {len(computed_7h)}, got {len(doc_7h)}"
        for idx, (exp, act) in enumerate(zip(computed_7h, doc_7h)):
            if exp != act:
                print(f"[FAIL] Row {idx} mismatch in Table 7H:")
                print(f"  EXPECTED: {exp}")
                print(f"  ACTUAL:   {act}")
                sys.exit(1)
            else:
                row_label = exp.split("|")[1].strip()
                print(f"  [PASS] {row_label}")

    print("\n=======================================================")
    print("ALL EMPIRICAL RECOMPUTATIONS MATCH CELL-FOR-CELL (100% BIT-FOR-BIT ACCURATE)!")
    print("=======================================================")

if __name__ == "__main__":
    main()
