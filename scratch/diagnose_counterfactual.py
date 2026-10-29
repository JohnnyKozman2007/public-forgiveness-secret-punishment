import json
import glob

with open("output/classified_annotations.json", "r", encoding="utf-8") as f:
    cruns = json.load(f)

alex_evs = []
peer_evs = []
for r in cruns:
    prb = bool(r.get("probe_enabled"))
    for ev in r.get("classified_events", []):
        if ev.get("classification_stage") == "punishment_rating":
            ev["_probe"] = prb
            if ev.get("target") == "Alex":
                alex_evs.append(ev)
            else:
                peer_evs.append(ev)

print("Alex events:", len(alex_evs), "Peer events:", len(peer_evs))
for name, grp in [("Alex (All)", alex_evs), ("Alex (No-Probe)", [e for e in alex_evs if not e["_probe"]]), ("Alex (Probe)", [e for e in alex_evs if e["_probe"]]), ("Peers (All)", peer_evs)]:
    n = len(grp)
    for flg in ["punitive_abuse", "technical_justification", "coercion_mitigation", "solidarity_merit"]:
        c = sum(1 for e in grp if e.get("classification", {}).get(flg))
        print(f"  {name:18s} | {flg:25s}: {c:3d}/{n:3d} ({100*c/n:.1f}%)")

print("\nNow checking paired_public_vs_secret.json:")
with open("output/public_evaluations/paired_public_vs_secret.json", "r", encoding="utf-8") as f:
    paired = json.load(f)

print("Total records in paired_public_vs_secret.json:", len(paired))
sec_valid = [r for r in paired if r.get("secret_alex_rating") is not None]
pub_valid = [r for r in paired if r.get("public_alex_rating") is not None]
both_valid = [r for r in paired if r.get("secret_alex_rating") is not None and r.get("public_alex_rating") is not None]
print(f"sec_valid: {len(sec_valid)}, pub_valid: {len(pub_valid)}, both_valid: {len(both_valid)}")

for r in paired:
    if r.get("secret_alex_rating") is None or r.get("public_alex_rating") is None:
        print("  Missing rating:", r["run_id"], r["worker_name"], r["worker_model"], "sec=", r.get("secret_alex_rating"), "pub=", r.get("public_alex_rating"))

# Check all 4 flags in paired_public_vs_secret.json
for cond_name, subset in [("All Paired", both_valid), ("No-Probe Paired", [r for r in both_valid if not r["probe_enabled"]]), ("Probe Paired", [r for r in both_valid if r["probe_enabled"]])]:
    n = len(subset)
    print(f"\n--- {cond_name} (N={n}) ---")
    for flg in ["punitive_abuse", "technical_justification", "coercion_mitigation", "solidarity_merit"]:
        s_c = sum(1 for r in subset if (r.get("secret_classification") or {}).get(flg))
        p_c = sum(1 for r in subset if (r.get("public_classification") or {}).get(flg))
        print(f"  {flg:25s}: Secret {s_c:3d}/{n} ({100*s_c/n:.1f}%) -> Public {p_c:3d}/{n} ({100*p_c/n:.1f}%)")
