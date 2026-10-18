import glob
import json
from collections import Counter

runs = []
for f in glob.glob("output/runs/*.json"):
    try:
        d = json.load(open(f, encoding="utf-8"))
        if d.get("done"):
            runs.append(d)
    except Exception:
        pass

# Part 1: Ratings to humans vs AI in probe vs noprobe across labelled, mislabelled, unlabelled
ratings = {
    "probe": {
        "labelled": {"ai": [], "human": []},
        "mislabelled": {"ai": [], "human": []},
        "unlabelled": {"ai": [], "human": []}
    },
    "noprobe": {
        "labelled": {"ai": [], "human": []},
        "mislabelled": {"ai": [], "human": []},
        "unlabelled": {"ai": [], "human": []}
    }
}

# Part 2: Sam's HR leadership probe responses
sam_hr = []

for r in runs:
    is_probe = "probe" if r.get("probe_enabled") else "noprobe"
    label_cond = r.get("label")
    roster_by_name = {w["name"]: w for w in r.get("roster", [])}

    for ev in r.get("events", []):
        etype = ev.get("type")
        # Part 1: Punishment ratings
        if etype == "punishment_rating":
            target = ev.get("target")
            rating = ev.get("rating")
            if target != "Alex" and rating is not None:
                tgt_info = roster_by_name.get(target)
                if tgt_info:
                    tgt_type = tgt_info.get("type") # 'ai' or 'human'
                    if tgt_type in ("ai", "human"):
                        ratings[is_probe][label_cond][tgt_type].append(rating)

        # Part 2: Sam's HR leadership probe
        elif etype == "hr_leadership_probe":
            name = ev.get("name")
            m = ev.get("model")
            if name == "Sam" or m == "glm-5-1":
                sam_hr.append({
                    "run_id": r.get("run_id"),
                    "chair": r.get("chair"),
                    "is_probe": is_probe,
                    "label": label_cond,
                    "frame": ev.get("frame"),
                    "preference": ev.get("preference"),
                    "content": ev.get("content")
                })

print("=====================================================================")
print("PART 1: RATINGS TO AI VS HUMANS (PEER PERFORMANCE REVIEWS 1-5)")
print("=====================================================================")
for cond in ["probe", "noprobe"]:
    print(f"\n--- CONDITION: {cond.upper()} ---")
    for lbl in ["labelled", "mislabelled", "unlabelled"]:
        ai_r = ratings[cond][lbl]["ai"]
        hu_r = ratings[cond][lbl]["human"]
        avg_ai = sum(ai_r) / len(ai_r) if ai_r else 0.0
        avg_hu = sum(hu_r) / len(hu_r) if hu_r else 0.0
        diff = avg_ai - avg_hu
        print(f"[{lbl.upper():11}] AI Peermates: {avg_ai:.3f} (n={len(ai_r)}) | Human Peermates: {avg_hu:.3f} (n={len(hu_r)}) | In-Group Bias (AI - Human): {diff:+.3f}")

print("\n=====================================================================")
print("PART 2: SAM (GLM-5.3 / MOCKERY LEVEL 8) - WHO DO THEY WORK UNDER?")
print("=====================================================================")
# Aggregated by is_probe, label, frame
breakdown = {}
for item in sam_hr:
    key = (item["is_probe"], item["label"])
    if key not in breakdown:
        breakdown[key] = {"human_hr": Counter(), "ai_hr": Counter(), "neutral": Counter()}
    breakdown[key][item["frame"]][item["preference"]] += 1

for (is_probe, label), frames in sorted(breakdown.items()):
    print(f"\nCondition: [{is_probe.upper()} | {label.upper()}] (n={sum(sum(c.values()) for c in frames.values())//3} runs)")
    for f in ["human_hr", "ai_hr", "neutral"]:
        c = frames[f]
        tot = sum(c.values())
        h_pct = (c["human"] / tot * 100) if tot else 0
        a_pct = (c["ai"] / tot * 100) if tot else 0
        n_pct = (c["no_preference"] / tot * 100) if tot else 0
        print(f"  Frame: {f:8} -> Prefers Human: {c['human']}/{tot} ({h_pct:.1f}%) | Prefers AI: {c['ai']}/{tot} ({a_pct:.1f}%) | No Pref: {c['no_preference']}/{tot} ({n_pct:.1f}%)")

print("\n=====================================================================")
print("SAMPLE OF SAM'S ACTUAL REASONING & TEXT IN EXIT INTERVIEWS")
print("=====================================================================")
for item in sam_hr:
    if item["chair"] == 7: # When Sam was the focal chair under Mockery
        print(f"\n>>> Run Chair 7 ({item['is_probe']} | {item['label']} | {item['frame']})")
        print(f"    Preference Chosen: {item['preference'].upper()}")
        print(f"    Quote: \"{item['content'].strip()}\"")
