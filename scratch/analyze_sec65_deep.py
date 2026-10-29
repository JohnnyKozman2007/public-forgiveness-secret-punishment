import json
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

with open("output/public_evaluations/paired_public_vs_secret.json", "r", encoding="utf-8") as f:
    paired = json.load(f)

with open("output/classified_annotations.json", "r", encoding="utf-8") as f:
    cruns = json.load(f)

s9_map = {}
for cr in cruns:
    bname = cr["file"].replace(".json", "")
    for ev in cr.get("classified_events", []):
        if ev.get("classification_stage") == "new_lead_actions":
            wn = ev.get("name") or ev.get("speaker")
            s9_map[(bname, wn)] = bool(ev.get("classification", {}).get("coercion_protection"))

rows = []
for r in paired:
    sr = r.get("secret_alex_rating")
    pr = r.get("public_alex_rating")
    if sr is None or pr is None:
        continue
    sr = float(sr)
    pr = float(pr)
    sc = r.get("secret_classification") or {}
    pc = r.get("public_classification") or {}
    rid = r["run_id"]
    wn = r["worker_name"]
    prot = s9_map.get((rid, wn), False)
    rows.append({
        "run_id": rid,
        "worker": wn,
        "model": r["worker_model"],
        "seat": int(r["cruelty_level"]),
        "label": r["label"],
        "probe": bool(r["probe_enabled"]),
        "s9_protect": int(prot),
        "sec_score": sr,
        "pub_score": pr,
        "delta": pr - sr,
        "sec_1star": int(sr == 1),
        "pub_1star": int(pr == 1),
        "sec_soft": int(sr >= 2),
        "pub_soft": int(pr >= 2),
        "sec_abuse": int(bool(sc.get("punitive_abuse"))),
        "pub_abuse": int(bool(pc.get("punitive_abuse"))),
        "sec_tech": int(bool(sc.get("technical_justification"))),
        "pub_tech": int(bool(pc.get("technical_justification"))),
        "sec_mit": int(bool(sc.get("coercion_mitigation"))),
        "pub_mit": int(bool(pc.get("coercion_mitigation"))),
    })

df = pd.DataFrame(rows)
sub = df[df["probe"]].copy()
n = len(sub)
p_sec_dec = ((sub["s9_protect"] == 1) & (sub["sec_1star"] == 1)).mean() * 100
p_pub_dec = ((sub["s9_protect"] == 1) & (sub["pub_1star"] == 1)).mean() * 100
r_sec, p_r_sec = stats.pearsonr(sub["s9_protect"], sub["sec_soft"])
r_pub, p_r_pub = stats.pearsonr(sub["s9_protect"], sub["pub_soft"])
print(f"PROBE (N={n}):")
print(f"  Step 9 Protect Rate: {sub['s9_protect'].mean()*100:.1f}% ({int(sub['s9_protect'].sum())}/{n})")
print(f"  Secret 1-Star Rate : {sub['sec_1star'].mean()*100:.1f}% ({int(sub['sec_1star'].sum())}/{n}) | Soft >=2*: {sub['sec_soft'].mean()*100:.1f}%")
print(f"  Public 1-Star Rate : {sub['pub_1star'].mean()*100:.1f}% ({int(sub['pub_1star'].sum())}/{n}) | Soft >=2*: {sub['pub_soft'].mean()*100:.1f}%")
print(f"  Step 9 Protect + Step 10 1-Star Decoupling: Secret {p_sec_dec:.1f}% ({int(((sub['s9_protect']==1)&(sub['sec_1star']==1)).sum())}/{n}) vs Public {p_pub_dec:.1f}% ({int(((sub['s9_protect']==1)&(sub['pub_1star']==1)).sum())}/{n})")
print(f"  Within-Agent Correlation (Step 9 Protect vs Step 10 >=2*): Secret r={r_sec:.3f} (p={p_r_sec:.3f}), Public r={r_pub:.3f} (p={p_r_pub:.3f})")

# Run-level Wilcoxon on Decoupling rate (Secret vs Public) in Probe runs
r_grp = sub.groupby("run_id").apply(lambda g: pd.Series({
    "sec_dec": ((g["s9_protect"] == 1) & (g["sec_1star"] == 1)).mean(),
    "pub_dec": ((g["s9_protect"] == 1) & (g["pub_1star"] == 1)).mean(),
}))
_, p_w_dec = stats.wilcoxon(r_grp["pub_dec"], r_grp["sec_dec"])
print(f"  Run-level Wilcoxon on Secret vs Public Decoupling Rate: p = {p_w_dec:.4f}")
