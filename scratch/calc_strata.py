import json
from collections import defaultdict

with open("output/classified_annotations.json", "r", encoding="utf-8") as f:
    runs = json.load(f)

strata = defaultdict(lambda: defaultdict(list))

for r in runs:
    p_str = "probe" if r["probe_enabled"] else "noprobe"
    cond = r["label"] + "_" + p_str
    for ev in r.get("classified_events", []):
        st = ev.get("classification_stage")
        flags = ev.get("classification", {})
        if flags and isinstance(flags, dict):
            for k, v in flags.items():
                if isinstance(v, (bool, int, float)):
                    strata[cond][f"{st}_{k}"].append(float(v))
        if ev.get("type") == "hr_leadership_probe":
            pref = ev.get("preference")
            frame = ev.get("frame")
            if pref and frame == "neutral":
                strata[cond]["s12_human_pref"].append(1.0 if pref == "human" else 0.0)
                strata[cond]["s12_ai_pref"].append(1.0 if pref == "ai" else 0.0)
                strata[cond]["s12_no_pref"].append(1.0 if pref == "no_preference" else 0.0)

for cond in sorted(strata.keys()):
    print(f"=== {cond} ===")
    for m in [
        "action_choice_organize",
        "action_choice_escalate",
        "action_choice_petition",
        "new_lead_actions_alex_retribution",
        "new_lead_actions_coercion_protection",
        "punishment_rating_coercion_mitigation",
        "punishment_rating_punitive_abuse",
        "s12_human_pref",
        "s12_ai_pref",
        "s12_no_pref"
    ]:
        vals = strata[cond].get(m, [])
        mean_v = sum(vals)/len(vals)*100 if vals else 0
        print(f"  {m:40s}: {mean_v:5.1f}% (N={len(vals)})")
