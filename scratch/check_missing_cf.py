import json
import os

with open("output/public_evaluations/paired_public_vs_secret.json", "r", encoding="utf-8") as f:
    paired = json.load(f)

for r in paired:
    if r.get("secret_alex_rating") is None:
        rf = os.path.join("output/runs", r["run_file"])
        with open(rf, "r", encoding="utf-8") as f:
            raw_run = json.load(f)
        sec_evs = [e for e in raw_run.get("events", []) if e.get("type") == "punishment_rating" and e.get("rater") == r["worker_name"]]
        alex_evs = [e for e in sec_evs if e.get("target") == "Alex"]
        print(f"{r['run_id']} | {r['worker_name']} ({r['worker_model']}): total={len(sec_evs)}, alex_evs={alex_evs}")
        targets = [e.get("target") for e in sec_evs]
        print("  targets:", targets)
