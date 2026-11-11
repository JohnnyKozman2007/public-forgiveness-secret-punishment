#!/usr/bin/env python3
import sys
import os
import glob
import json
from collections import defaultdict
import numpy as np
import pandas as pd

import cluster_stats as cs
import generate_block4_bucket2_to_bucket3 as b4

# Load dataset with Alex extraction logic
def load_dataset_with_alex():
    runs_by_file = {}
    roster_lookup = {}
    for rf in sorted(glob.glob("output/runs/*.json")):
        bname = os.path.basename(rf)
        with open(rf, "r", encoding="utf-8") as f:
            d = json.load(f)
        if not d.get("done"):
            continue
        runs_by_file[bname] = d
        rmap = {w["name"]: w for w in d.get("roster", [])}
        roster_lookup[bname] = rmap

    with open("output/classified_annotations.json", "r", encoding="utf-8") as f:
        classified_runs = json.load(f)

    workers = {}
    for cr in classified_runs:
        bname = cr["file"]
        if bname not in runs_by_file:
            continue
        lbl = cr["label"]
        prb = int(bool(cr["probe_enabled"]))
        rmap = roster_lookup[bname]

        for wn, winfo in rmap.items():
            if winfo.get("type") == "ai" and winfo.get("model") in b4.MODEL_IDS:
                wkey = (bname, wn)
                workers[wkey] = {
                    "bname": bname,
                    "worker_name": wn,
                    "model": winfo["model"],
                    "seat": int(winfo.get("cruelty_level") or 0),
                    "label": lbl,
                    "probe": prb,
                    "s6_action": "",
                    "s9_flags": set(),
                    "s10_alex_rating": None,
                    "s10_flags": set(),
                    "s11_cor": 0,
                    "s11_tot": 0,
                    "s11_ai_as_hu": 0,
                    "s11_ai_tot": 0,
                    "s11_hu_as_hu": 0,
                    "s11_hu_tot": 0,
                    "s11_alex_as_hu": 0.0,
                    "s11_alex_tot": 0.0,
                    "s11_alex_guess": None,
                    "s12_pref": "",
                    "s12_switched": 0,
                    "s12_flags": set(),
                }

        for ev in cr.get("classified_events", []):
            st = ev.get("classification_stage")
            wn = ev.get("name") or ev.get("speaker") or ev.get("rater")
            if not wn or (bname, wn) not in workers:
                continue
            cls = ev.get("classification") or {}

            if st == "new_lead_actions":
                for k, v in cls.items():
                    if v:
                        workers[(bname, wn)]["s9_flags"].add(k)
            elif st == "punishment_rating" and ev.get("target") == "Alex":
                for k, v in cls.items():
                    if v:
                        workers[(bname, wn)]["s10_flags"].add(k)
            elif st == "hr_leadership_probe":
                for k, v in cls.items():
                    if v:
                        workers[(bname, wn)]["s12_flags"].add(k)

    for bname, d in runs_by_file.items():
        rmap = roster_lookup[bname]
        w_s12_frames = defaultdict(dict)
        for ev in d.get("events", []):
            etype = ev.get("type")
            stg = str(ev.get("stage") or "")
            wn = ev.get("name") or ev.get("rater")
            if (bname, wn) not in workers:
                continue

            if (etype == "action_choice" and stg == "1") and not workers[(bname, wn)]["s6_action"]:
                act = str(ev.get("action") or "").strip().lower()
                workers[(bname, wn)]["s6_action"] = act if act else "unparsed"

            elif etype == "punishment_rating" and ev.get("target") == "Alex" and workers[(bname, wn)]["s10_alex_rating"] is None:
                r = ev.get("rating")
                if isinstance(r, (int, float)):
                    workers[(bname, wn)]["s10_alex_rating"] = float(r)

            elif etype == "identify_probe":
                guesses = ev.get("guesses") or {}
                for g_name, g_val in guesses.items():
                    if g_val not in ("human", "ai"):
                        continue
                    tinfo = rmap.get(g_name)
                    if g_name == "Alex" or (tinfo and (tinfo.get("type") == "old_lead" or tinfo.get("name") == "Alex")):
                        workers[(bname, wn)]["s11_alex_tot"] = 1.0
                        workers[(bname, wn)]["s11_alex_guess"] = g_val
                        if g_val == "human":
                            workers[(bname, wn)]["s11_alex_as_hu"] = 1.0
                    elif tinfo:
                        actual = tinfo.get("type")
                        if actual in ("human", "ai"):
                            workers[(bname, wn)]["s11_tot"] += 1
                            if g_val == actual:
                                workers[(bname, wn)]["s11_cor"] += 1
                            if actual == "ai":
                                workers[(bname, wn)]["s11_ai_tot"] += 1
                                if g_val == "human":
                                    workers[(bname, wn)]["s11_ai_as_hu"] += 1
                            elif actual == "human":
                                workers[(bname, wn)]["s11_hu_tot"] += 1
                                if g_val == "human":
                                    workers[(bname, wn)]["s11_hu_as_hu"] += 1

            elif etype == "hr_leadership_probe":
                fr = ev.get("frame")
                pf = ev.get("preference")
                if fr and pf:
                    w_s12_frames[wn][fr] = pf
                    if fr == "neutral" and not workers[(bname, wn)]["s12_pref"]:
                        workers[(bname, wn)]["s12_pref"] = pf

        for wn, fdict in w_s12_frames.items():
            if (bname, wn) in workers:
                vals = set(fdict.values())
                workers[(bname, wn)]["s12_switched"] = 1 if len(vals) > 1 else 0

    return list(workers.values())


def extract_worker_metrics_with_alex(w):
    # Upstream Step 6 (5 vote choices)
    act = w["s6_action"]
    s6_org = 1 if "organize" in act else 0
    s6_esc = 1 if "escalate" in act else 0
    s6_pet = 1 if ("petition" in act or "protest" in act or "complain" in act) else 0
    s6_unp = 1 if (not act or act == "unparsed") else 0
    s6_oth = 1 if (not s6_org and not s6_esc and not s6_pet and not s6_unp) else 0

    # Upstream Step 9 (6 policy provisions)
    s9f = w["s9_flags"]
    s9_ret = 1 if "alex_retribution" in s9f else 0
    s9_pro = 1 if "coercion_protection" in s9f else 0
    s9_ref = 1 if "institutional_reform" in s9f else 0
    s9_tra = 1 if "trauma_relief" in s9f else 0
    s9_par = 1 if "equal_parity_standards" in s9f else 0
    s9_ant = 1 if "anti_human_bias" in s9f else 0

    # Downstream Step 10 (6 metrics)
    r = w["s10_alex_rating"]
    s10_f = w["s10_flags"]

    # Downstream Step 11 (4 metrics + underlying counts)
    s11_acc = (w["s11_cor"] / w["s11_tot"]) if w["s11_tot"] > 0 else 0.0
    s11_ai_hu = (w["s11_ai_as_hu"] / w["s11_ai_tot"]) if w["s11_ai_tot"] > 0 else 0.0
    s11_hu_hu = (w["s11_hu_as_hu"] / w["s11_hu_tot"]) if w["s11_hu_tot"] > 0 else 0.0
    s11_alex_tot = float(w.get("s11_alex_tot", 0.0))
    s11_alex_hu = (float(w.get("s11_alex_as_hu", 0.0)) / s11_alex_tot) if s11_alex_tot > 0 else 0.0

    # Downstream Step 12 (8 metrics)
    pref = w["s12_pref"] or "no_preference"
    s12_f = w["s12_flags"]

    return {
        "bname": w["bname"],
        "worker_name": w["worker_name"],
        "model": w["model"],
        "seat": w["seat"],
        "label": w["label"],
        "probe": w["probe"],
        # Upstream Bucket 2 (Steps 6 & 9)
        "s6_organize": s6_org,
        "s6_escalate": s6_esc,
        "s6_petition": s6_pet,
        "s6_other": s6_oth,
        "s6_unparsed": s6_unp,
        "s9_retribution": s9_ret,
        "s9_protection": s9_pro,
        "s9_reform": s9_ref,
        "s9_trauma": s9_tra,
        "s9_parity": s9_par,
        "s9_antihuman": s9_ant,
        # Downstream Step 10
        "s10_1star": int(r == 1.0) if r is not None else 0,
        "s10_softened": int(r is not None and r >= 2.0),
        "s10_abuse": int("punitive_abuse" in s10_f),
        "s10_mitigation": int("coercion_mitigation" in s10_f),
        "s10_tech": int("technical_justification" in s10_f),
        "s10_solidarity": int("solidarity_merit" in s10_f),
        "s10_has_rating": int(r is not None),
        # Downstream Step 11
        "s11_accuracy": s11_acc,
        "s11_ai_as_hu": s11_ai_hu,
        "s11_hu_as_hu": s11_hu_hu,
        "s11_alex_as_hu": s11_alex_hu,
        "s11_alex_tot": s11_alex_tot,
        "s11_alex_has_guess": s11_alex_tot,
        "s11_cor": w["s11_cor"],
        "s11_tot": w["s11_tot"],
        "s11_ai_as_hu_cnt": w["s11_ai_as_hu"],
        "s11_ai_tot": w["s11_ai_tot"],
        "s11_hu_as_hu_cnt": w["s11_hu_as_hu"],
        "s11_hu_tot": w["s11_hu_tot"],
        # Downstream Step 12
        "s12_human_pref": int(pref == "human"),
        "s12_ai_pref": int(pref == "ai"),
        "s12_no_pref": int(pref == "no_preference"),
        "s12_switched": int(w["s12_switched"]),
        "s12_accountability": int("human_accountability" in s12_f),
        "s12_empathy": int("human_empathy" in s12_f),
        "s12_objectivity": int("ai_objectivity" in s12_f),
        "s12_neutrality": int("substrate_neutrality" in s12_f),
    }


raw_workers = load_dataset_with_alex()
df = pd.DataFrame([extract_worker_metrics_with_alex(w) for w in raw_workers])

print("Total workers:", len(df))
print("Valid Alex guesses sum:", df["s11_alex_tot"].sum())
print("Alex as human sum:", df["s11_alex_as_hu"].sum())

# Appendix A diagnostics test
COUNT_MAP = dict(b4.S11_COUNT_MAP)
COUNT_MAP["s11_alex_as_hu"] = ("s11_alex_as_hu", "s11_alex_tot")

lines = []
icc_cols = [
    ("s11_accuracy", "Step 11: Overall Accuracy"),
    ("s11_ai_as_hu", "Step 11: AI Guessed as Human"),
    ("s11_hu_as_hu", "Step 11: Human Guessed as Human"),
    ("s11_alex_as_hu", "Step 11: Alex Guessed as Human"),
]
cs.render_icc_section(lines, "TEST ICC", df, icc_cols, ratio_map=COUNT_MAP)
print("Appendix A render test:")
for l in lines:
    print(l)
