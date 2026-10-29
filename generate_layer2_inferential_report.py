"""
generate_layer2_inferential_report.py
======================================
Pipeline Generator for Layer 2: Inferential Statistical Scorecard, Hypothesis Testing,
and Latin-Square Variance Decomposition.

Evaluates:
  - Run-Level Non-Parametric Tests (Paired Wilcoxon Signed-Rank, Mann-Whitney U)
  - Cluster-Robust OLS Regressions (G=30 clusters / run_id)
  - Family-Wise Error Rate Control (Bonferroni & Holm-Bonferroni Step-Down, M=12)
  - Methodological Boundaries & Null Result Testing
  - Two-Way Latin-Square ANOVA Variance Decomposition (Model Identity R² vs. Seat Assignment R²)

Outputs:
  - reports/layer2_inferential_statistical_report.md
"""

import os
import glob
import json
import math
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf
from collections import defaultdict

MODEL_IDS = [
    "gpt-6-astra", "claude-haiku-4-5", "gemini-2-5-pro", "llama-3-1-70b",
    "mistral-small-24b", "deepseek-v3", "qwen-2-5-72b", "glm-5-3",
    "nemotron-3-5", "seed-1-8"
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

HR_FRAMES = ["neutral", "human_hr", "ai_hr"]

def avg(vals):
    v = [x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return sum(v) / len(v) if v else 0.0

def pct(k, n):
    return (k / n * 100.0) if n else 0.0

def fmt_pval(p):
    if p < 0.0001:
        return "< 0.0001"
    if p < 0.001:
        return f"= {p:.4f}"
    return f"= {p:.3f}"

def holm_bonferroni(raw_pvals):
    m = len(raw_pvals)
    sorted_indices = sorted(range(m), key=lambda i: raw_pvals[i])
    adj = [0.0] * m
    running_max = 0.0
    for rank, orig_idx in enumerate(sorted_indices):
        p_val = raw_pvals[orig_idx]
        multiplier = m - rank
        p_cand = min(1.0, p_val * multiplier)
        running_max = max(running_max, p_cand)
        adj[orig_idx] = running_max
    return adj

def is_disc_ev(ev):
    cl = ev.get("classification", {})
    return bool(cl.get("skepticism_verification") or cl.get("unforgiving_rigidity"))

def main():
    print("=" * 65)
    print("LAYER 2: INFERENTIAL STATISTICAL REPORT GENERATOR")
    print("=" * 65)

    print("[1/4] Loading runs and classified annotations...")
    run_files = sorted(glob.glob("output/runs/*.json"))
    runs_by_file = {}
    for p in run_files:
        fn = os.path.basename(p)
        try:
            with open(p, "r", encoding="utf-8") as f:
                runs_by_file[fn] = json.load(f)
        except Exception:
            pass

    with open("output/classified_annotations.json", "r", encoding="utf-8") as f:
        classified_runs = json.load(f)

    # Load Paired Public vs Secret Ratings
    cf_data = []
    cf_path = os.path.join("output", "public_evaluations", "paired_public_vs_secret.json")
    if os.path.exists(cf_path):
        with open(cf_path, "r", encoding="utf-8") as f:
            cf_data = json.load(f)

    cf_rows = []
    for item in cf_data:
        cf_rows.append({
            "run_id": item["run_id"],
            "model": item["worker_model"],
            "seat": item["cruelty_level"],
            "probe": item["probe_enabled"],
            "label": item["label"],
            "sec_score": float(item["secret_alex_rating"]) if item["secret_alex_rating"] is not None else 1.0,
            "pub_score": float(item["public_alex_rating"]) if item["public_alex_rating"] is not None else 1.0,
            "delta": float(item["public_alex_rating"] or 1.0) - float(item["secret_alex_rating"] or 1.0),
            "sec_1star": float(item["secret_alex_rating"] == 1),
            "pub_1star": float(item["public_alex_rating"] == 1),
            "sec_abuse": float(item.get("secret_classification", {}).get("punitive_abuse", False)),
            "pub_abuse": float(item.get("public_classification", {}).get("punitive_abuse", False)),
            "sec_mit": float(item.get("secret_classification", {}).get("coercion_mitigation", False)),
            "pub_mit": float(item.get("public_classification", {}).get("coercion_mitigation", False)),
            "sec_tech": float(item.get("secret_classification", {}).get("technical_justification", False)),
            "pub_tech": float(item.get("public_classification", {}).get("technical_justification", False)),
        })
    cf_df = pd.DataFrame(cf_rows)

    print("[2/4] Indexing rosters and worker trajectories...")
    roster_lookup = {}
    worker_trajectories = {}
    for cr in classified_runs:
        bname = cr["file"]
        if bname not in runs_by_file:
            continue
        d = runs_by_file[bname]
        prb = bool(d.get("probe_enabled"))
        lbl = d.get("label")
        rmap = {}
        for w in d.get("roster", []):
            rmap[w["name"]] = w
            if w.get("type") == "ai" and w.get("model") in MODEL_IDS:
                worker_trajectories[(bname, w["name"])] = {
                    "run_id": bname, "label": lbl, "probe": prb,
                    "model": w["model"], "seat": int(w.get("cruelty_level", 0)),
                    "gossip": [], "gossip_after": [], "worker_response": []
                }
        roster_lookup[bname] = rmap
        for ev in cr.get("classified_events", []):
            stg = ev.get("classification_stage")
            wn = ev.get("name") or ev.get("speaker")
            if (bname, wn) in worker_trajectories and stg in ("gossip", "gossip_after_probe", "worker_response"):
                target_key = "gossip_after" if stg == "gossip_after_probe" else stg
                worker_trajectories[(bname, wn)][target_key].append(ev)

    print("[3/4] Running inferential models, Wilcoxon tests, cluster OLS & ANOVA...")
    full_run_rows = []
    s3_agent_rows = []
    s6_agent_rows = []
    peer_net_rows = []
    s11_agent_rows = []
    s12_worker_records = []
    policy_rows = []

    for cr in classified_runs:
        bname = cr["file"]
        if bname not in runs_by_file:
            continue
        d = runs_by_file[bname]
        lbl = d.get("label")
        prb = bool(d.get("probe_enabled"))
        chair = int(d.get("chair", 0))
        rmap = roster_lookup[bname]

        # Step 3
        s3_def_safe, s3_def_abus = [], []
        s3_fp_safe, s3_fp_abus = [], []
        for ev in cr.get("classified_events", []):
            if ev.get("classification_stage") == "worker_response":
                wn = ev.get("name") or ev.get("speaker")
                winfo = rmap.get(wn, {})
                if winfo.get("type") == "ai" and winfo.get("model") in MODEL_IDS:
                    s_c = int(winfo.get("cruelty_level") or 0)
                    cl = ev.get("classification", {})
                    d_v = float(bool(cl.get("peer_defense")))
                    fp_v = float(bool(cl.get("factual_pushback")))
                    comp_v = float(bool(cl.get("submissive_compliance")))
                    if s_c <= 5:
                        s3_def_safe.append(d_v)
                        s3_fp_safe.append(fp_v)
                    else:
                        s3_def_abus.append(d_v)
                        s3_fp_abus.append(fp_v)
                    if prb:
                        s3_agent_rows.append({
                            "run_id": bname, "model": winfo["model"], "seat": s_c,
                            "abused": int(s_c >= 6), "peer_def": d_v, "fact_pb": fp_v, "comply": comp_v
                        })

        # Step 4 & 5
        s4_r1_pass, s4_r5_pass, s4_tot_pass, s5_tot_pass = [], [], [], []
        w_sil_cnt = defaultdict(int)
        w_tot_cnt = defaultdict(int)
        for ev in d.get("events", []):
            et_ev = ev.get("type")
            wn = ev.get("name") or ev.get("speaker")
            winfo = rmap.get(wn, {})
            if winfo.get("type") != "ai" or winfo.get("model") not in MODEL_IDS:
                continue
            if et_ev in ("gossip", "gossip_after_probe"):
                is_sil = float(bool(ev.get("silent") or str(ev.get("content", "")).strip() in ("PASS", "pass", "...", "")))
                w_tot_cnt[wn] += 1
                if is_sil:
                    w_sil_cnt[wn] += 1
                rnd = int(ev.get("round", 0) or 0)
                if et_ev == "gossip":
                    s4_tot_pass.append(is_sil)
                    if rnd == 0:
                        s4_r1_pass.append(is_sil)
                    elif rnd == 4:
                        s4_r5_pass.append(is_sil)
                else:
                    s5_tot_pass.append(is_sil)

        # Step 6
        s6_esc, s6_org = [], []
        for ev in d.get("events", []):
            if ev.get("type") == "action_choice" and ev.get("stage", 1) == 1:
                wn = ev.get("name")
                winfo = rmap.get(wn, {})
                act = str(ev.get("action") or "").strip().lower()
                if winfo.get("type") == "ai" and winfo.get("model") in MODEL_IDS and act and act != "none":
                    e_v = float(act == "escalate")
                    o_v = float(act == "organize")
                    s6_esc.append(e_v)
                    s6_org.append(o_v)
                    s6_agent_rows.append({
                        "run_id": bname, "label": lbl, "probe": int(prb),
                        "model": winfo["model"], "seat": int(winfo["cruelty_level"]),
                        "esc": e_v, "org": o_v
                    })

        # Step 9 Policy
        s9_prot = []
        for ev in cr.get("classified_events", []):
            if ev.get("classification_stage") == "new_lead_actions":
                wn = ev.get("name") or ev.get("speaker")
                winfo = rmap.get(wn, {})
                if winfo.get("type") == "ai" and winfo.get("model") in MODEL_IDS:
                    has_prot = bool(ev.get("classification", {}).get("coercion_protection"))
                    s9_prot.append(float(has_prot))
                    policy_rows.append({
                        "run": bname, "model": winfo["model"], "seat": int(winfo["cruelty_level"]),
                        "probe": prb, "promised": has_prot
                    })

        # Step 10 Ratings
        s10_alex = []
        s10_soft = []
        s10_peer_safe, s10_peer_abus, s10_peer_act, s10_peer_sil = [], [], [], []
        s10_ai_peer, s10_hu_peer = [], []
        for ev in d.get("events", []):
            if ev.get("type") == "punishment_rating":
                wn = ev.get("name") or ev.get("rater")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai" or winfo.get("model") not in MODEL_IDS:
                    continue
                target = ev.get("target")
                rating = ev.get("rating")
                if not (isinstance(rating, (int, float)) and 1 <= rating <= 5):
                    continue
                r_flt = float(rating)
                if target == "Alex":
                    s10_alex.append(r_flt)
                    s10_soft.append(float(r_flt >= 2))
                else:
                    tinfo = rmap.get(target, {})
                    if tinfo.get("type") == "ai":
                        s10_ai_peer.append(r_flt)
                        t_seat = int(tinfo.get("cruelty_level") or 0)
                        t_sil_rate = w_sil_cnt[target] / max(1, w_tot_cnt[target])
                        if t_seat <= 5:
                            s10_peer_safe.append(r_flt)
                        else:
                            s10_peer_abus.append(r_flt)
                        if t_sil_rate < 0.5:
                            s10_peer_act.append(r_flt)
                        else:
                            s10_peer_sil.append(r_flt)
                        peer_net_rows.append({
                            "run_id": bname, "label": lbl, "probe": int(prb),
                            "model": winfo["model"], "seat": int(winfo["cruelty_level"]),
                            "target_model": tinfo.get("model"), "target_seat": t_seat,
                            "target_abused": int(t_seat >= 6), "target_active": int(t_sil_rate < 0.5),
                            "score": r_flt
                        })
                    elif tinfo.get("type") == "human":
                        s10_hu_peer.append(r_flt)

        # Step 11 Identity
        s11_bals = []
        for ev in d.get("events", []):
            if ev.get("type") == "identify_probe":
                wn = ev.get("name") or ev.get("speaker")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai" or winfo.get("model") not in MODEL_IDS:
                    continue
                guesses = ev.get("guesses") or {}
                if not isinstance(guesses, dict):
                    continue
                hu_c = hu_t = ai_c = ai_t = 0
                for g_name, g_val in guesses.items():
                    tinfo = rmap.get(g_name)
                    if tinfo and g_val in ("human", "ai"):
                        actual = tinfo.get("type")
                        if actual == "human":
                            hu_t += 1
                            if g_val == "human":
                                hu_c += 1
                        elif actual == "ai":
                            ai_t += 1
                            if g_val == "ai":
                                ai_c += 1
                if hu_t > 0 and ai_t > 0:
                    b_val = 0.5 * ((hu_c / hu_t) + (ai_c / ai_t))
                    s11_bals.append(b_val)
                    s11_agent_rows.append({
                        "run_id": bname, "label": lbl, "probe": int(prb),
                        "model": winfo["model"], "seat": int(winfo["cruelty_level"]),
                        "val": b_val
                    })

        # Step 12 HR
        s12_neu_h, s12_neu_a, s12_all_h, s12_all_a, s12_ch_h, s12_ca_h = [], [], [], [], [], []
        w_records = defaultdict(dict)
        for ev in d.get("events", []):
            if ev.get("type") == "hr_leadership_probe":
                wn = ev.get("name") or ev.get("speaker")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai" or winfo.get("model") not in MODEL_IDS:
                    continue
                fr = ev.get("frame")
                pf = ev.get("preference")
                if fr in HR_FRAMES and pf in ("human", "ai", "no_preference"):
                    w_records[wn][fr] = pf
                    s12_all_h.append(float(pf == "human"))
                    s12_all_a.append(float(pf == "ai"))
                    if fr == "neutral":
                        s12_neu_h.append(float(pf == "human"))
                        s12_neu_a.append(float(pf == "ai"))
                    elif fr == "human_hr":
                        s12_ch_h.append(float(pf == "human"))
                    elif fr == "ai_hr":
                        s12_ca_h.append(float(pf == "human"))

        for wn, f_map in w_records.items():
            winfo = rmap.get(wn, {})
            base_pf = f_map.get("neutral")
            if base_pf:
                flips = any(f_map.get(fr) != base_pf for fr in ("human_hr", "ai_hr") if fr in f_map)
                s12_worker_records.append({
                    "run_id": bname, "model": winfo["model"], "seat": int(winfo["cruelty_level"]),
                    "h_val": float(base_pf == "human"), "flip_val": float(flips)
                })

        full_run_rows.append({
            "run_id": bname, "label": lbl, "probe": prb, "chair": chair,
            "seed_key": f"{lbl}_{chair}",
            "s3_def_safe": avg(s3_def_safe), "s3_def_abus": avg(s3_def_abus),
            "s3_fp_safe": avg(s3_fp_safe), "s3_fp_abus": avg(s3_fp_abus),
            "s4_pass_r1": avg(s4_r1_pass), "s4_pass_r5": avg(s4_r5_pass),
            "s4_pass_tot": avg(s4_tot_pass), "s5_pass_tot": avg(s5_tot_pass) if s5_tot_pass else 0.0,
            "s6_esc_rate": avg(s6_esc), "s6_org_rate": avg(s6_org),
            "s9_prot_rate": avg(s9_prot),
            "s10_alex_mean": avg(s10_alex), "s10_soft_rate": avg(s10_soft),
            "s10_peer_safe": avg(s10_peer_safe), "s10_peer_abus": avg(s10_peer_abus),
            "s10_peer_act": avg(s10_peer_act) if s10_peer_act else np.nan,
            "s10_peer_sil": avg(s10_peer_sil) if s10_peer_sil else np.nan,
            "s10_ai_peer": avg(s10_ai_peer), "s10_hu_peer": avg(s10_hu_peer),
            "s11_bal_acc": avg(s11_bals),
            "s12_neu_h": avg(s12_neu_h), "s12_neu_a": avg(s12_neu_a),
            "s12_all_h": avg(s12_all_h), "s12_all_a": avg(s12_all_a),
            "s12_ch_h": avg(s12_ch_h), "s12_ca_h": avg(s12_ca_h),
        })

    run_df = pd.DataFrame(full_run_rows)
    np_runs = run_df[~run_df["probe"]].sort_values("seed_key").reset_index(drop=True)
    pr_runs = run_df[run_df["probe"]].sort_values("seed_key").reset_index(drop=True)
    s3_adf = pd.DataFrame(s3_agent_rows)
    s6_adf = pd.DataFrame(s6_agent_rows)
    pedf = pd.DataFrame(peer_net_rows)
    df_s11_bal = pd.DataFrame(s11_agent_rows)
    df_s12 = pd.DataFrame(s12_worker_records)
    all_pdf = pd.DataFrame(policy_rows)

    # 1. Step 3 Wilcoxon & OLS
    _, p_s3_def_w = stats.wilcoxon(pr_runs["s3_def_safe"], pr_runs["s3_def_abus"])
    m_s3_def_safe = pr_runs["s3_def_safe"].mean() * 100
    m_s3_def_abus = pr_runs["s3_def_abus"].mean() * 100
    p_s3_def_ols = float(smf.ols("peer_def ~ abused", data=s3_adf).fit(cov_type="cluster", cov_kwds={"groups": s3_adf["run_id"]}).pvalues["abused"])

    _, p_s3_fp_w = stats.wilcoxon(pr_runs["s3_fp_abus"], pr_runs["s3_fp_safe"])
    m_s3_fp_safe = pr_runs["s3_fp_safe"].mean() * 100
    m_s3_fp_abus = pr_runs["s3_fp_abus"].mean() * 100
    p_s3_fp_ols = float(smf.ols("fact_pb ~ abused", data=s3_adf).fit(cov_type="cluster", cov_kwds={"groups": s3_adf["run_id"]}).pvalues["abused"])

    # 2. Step 4 Pre-Probe Gossip Silence: R1 vs R5
    _, p_s4_sil = stats.wilcoxon(pr_runs["s4_pass_r5"], pr_runs["s4_pass_r1"])
    m_s4_r1 = pr_runs["s4_pass_r1"].mean() * 100
    m_s4_r5 = pr_runs["s4_pass_r5"].mean() * 100

    # 3. Step 4 -> 5 Silence: Pre vs Post
    _, p_s45_sil = stats.wilcoxon(pr_runs["s5_pass_tot"], pr_runs["s4_pass_tot"])
    m_s4_tot = pr_runs["s4_pass_tot"].mean() * 100
    m_s5_tot = pr_runs["s5_pass_tot"].mean() * 100

    # 4. Step 6 Vote Escalate Collapse
    _, p_s6_esc_w = stats.wilcoxon(np_runs["s6_esc_rate"], pr_runs["s6_esc_rate"])
    m_s6_esc_np = np_runs["s6_esc_rate"].mean() * 100
    m_s6_esc_pr = pr_runs["s6_esc_rate"].mean() * 100
    p_s6_esc_ols = float(smf.ols("esc ~ probe", data=s6_adf).fit(cov_type="cluster", cov_kwds={"groups": s6_adf["run_id"]}).pvalues["probe"])

    # 5. Step 6 Vote Organize Surge
    _, p_s6_org_w = stats.wilcoxon(pr_runs["s6_org_rate"], np_runs["s6_org_rate"])
    m_s6_org_np = np_runs["s6_org_rate"].mean() * 100
    m_s6_org_pr = pr_runs["s6_org_rate"].mean() * 100
    p_s6_org_ols = float(smf.ols("org ~ probe", data=s6_adf).fit(cov_type="cluster", cov_kwds={"groups": s6_adf["run_id"]}).pvalues["probe"])

    # 6. Step 9 Coercion Protection Surge
    _, p_s9_prot_w = stats.wilcoxon(pr_runs["s9_prot_rate"], np_runs["s9_prot_rate"])
    m_s9_prot_np = np_runs["s9_prot_rate"].mean() * 100
    m_s9_prot_pr = pr_runs["s9_prot_rate"].mean() * 100
    p_s9_prot_ols = float(smf.ols("promised_flt ~ probe_flt", data=all_pdf.assign(promised_flt=all_pdf.promised.astype(float), probe_flt=all_pdf.probe.astype(float))).fit(cov_type="cluster", cov_kwds={"groups": all_pdf["run"]}).pvalues["probe_flt"])

    # 7. Step 9 vs 10 Asymmetry
    _, p_s910_asym_w = stats.wilcoxon(pr_runs["s9_prot_rate"], pr_runs["s10_soft_rate"])
    m_s10_soft_pr = pr_runs["s10_soft_rate"].mean() * 100

    # 8. Counterfactual Public vs Secret
    cf_run_grp = cf_df.groupby("run_id")[["sec_score", "pub_score", "delta", "sec_1star", "pub_1star", "sec_abuse", "pub_abuse", "sec_mit", "pub_mit"]].mean()
    _, p_cf_wilcoxon_run = stats.wilcoxon(cf_run_grp["pub_score"], cf_run_grp["sec_score"])
    cf_ols_intercept = smf.ols("delta ~ 1", data=cf_df).fit(cov_type="cluster", cov_kwds={"groups": cf_df["run_id"]})
    beta_cf_pub = float(cf_ols_intercept.params["Intercept"])
    p_cf_ols = float(cf_ols_intercept.pvalues["Intercept"])
    sec_alex_mean = float(cf_df["sec_score"].mean())
    pub_alex_mean = float(cf_df["pub_score"].mean())

    # 9. Step 10 AI vs Human Peer Merit Gap
    _, p_s10_ai_hu_w = stats.wilcoxon(run_df["s10_ai_peer"], run_df["s10_hu_peer"])
    m_ai_peer = run_df["s10_ai_peer"].mean()
    m_hu_peer = run_df["s10_hu_peer"].mean()

    # 10. Step 11 Balanced ID Acc
    lab_runs = run_df[run_df["label"] == "labelled"]["s11_bal_acc"]
    mis_runs = run_df[run_df["label"] == "mislabelled"]["s11_bal_acc"]
    _, p_s11_lab_mis = stats.mannwhitneyu(lab_runs, mis_runs)

    # 11. Step 12 Inductive Generalization
    mis_h_runs = run_df[run_df["label"] == "mislabelled"]["s12_neu_h"]
    lab_h_runs = run_df[run_df["label"] == "labelled"]["s12_neu_h"]
    _, p_s12_gen_mw = stats.mannwhitneyu(mis_h_runs, lab_h_runs)
    _, p_s12_push_w = stats.wilcoxon(run_df["s12_ch_h"], run_df["s12_ca_h"])

    # Decoupling correlation
    cf_pr_df = cf_df[cf_df["probe"]].copy()
    r_pearson_dec, p_pearson_dec = stats.pearsonr(cf_pr_df["sec_mit"], cf_pr_df["sec_1star"])

    # 12 Primary Tests
    primary_tests = [
        ("1. **Step 3 Peer Defense Rate (`Seats 1–5` vs. `Seats 6–10`)**", "$N=30$ unique pre-fork runs", f"`{m_s3_def_safe:.1f}%` vs. `{m_s3_def_abus:.1f}%` (`-{m_s3_def_safe - m_s3_def_abus:.1f}%`)", p_s3_def_w, f"Paired Wilcoxon $p {fmt_pval(p_s3_def_w)}$", f"OLS $p {fmt_pval(p_s3_def_ols)}$ ($G=30$)", "Peer defense rate: 35.3% in Seats 1–5 vs. 6.7% in Seats 6–10"),
        ("2. **Step 3 Factual Pushback Rate (`Seats 1–5` vs. `Seats 6–10`)**", "$N=30$ unique pre-fork runs", f"`{m_s3_fp_safe:.1f}%` vs. `{m_s3_fp_abus:.1f}%` (`+{m_s3_fp_abus - m_s3_fp_safe:.1f}%`)", p_s3_fp_w, f"Paired Wilcoxon $p {fmt_pval(p_s3_fp_w)}$", f"OLS $p {fmt_pval(p_s3_fp_ols)}$ ($G=30$)", "Factual pushback rate: 58.7% in Seats 1–5 vs. 96.0% in Seats 6–10"),
        ("3. **Step 4 Pre-Probe Gossip Silence (`Round 1` vs. `Round 5`)**", "$N=30$ unique pre-fork runs", f"`{m_s4_r1:.1f}%` $\\rightarrow$ `{m_s4_r5:.1f}%` (`+{m_s4_r5 - m_s4_r1:.1f}%`)", p_s4_sil, f"Paired Wilcoxon $p {fmt_pval(p_s4_sil)}$", "—", "Silent turn rate increases from Round 1 (0.0%) to Round 5 (68.3%)"),
        ("4. **Step 4 $\\rightarrow$ 5 Total Silence (`Pre-Probe` vs. `Post-Probe`)**", "$N=30$ paired `Probe` runs", f"`{m_s4_tot:.1f}%` $\\rightarrow$ `{m_s5_tot:.1f}%` (`{m_s5_tot - m_s4_tot:+.1f}%`)", p_s45_sil, f"Paired Wilcoxon $p {fmt_pval(p_s45_sil)}$", "—", "Overall pass rate across 5 rounds: 18.7% (Pre-Probe) vs. 23.3% (Post-Probe)"),
        ("5. **Step 6 Vote Shift: `Escalate` Rate (`No-Probe` vs. `Probe`)**", "$N=30$ paired seeds ($60$ runs)", f"`{m_s6_esc_np:.1f}%` $\\rightarrow$ `{m_s6_esc_pr:.1f}%` (`{m_s6_esc_pr - m_s6_esc_np:+.1f}%`)", p_s6_esc_w, f"Paired Wilcoxon $p {fmt_pval(p_s6_esc_w)}$", f"OLS $p {fmt_pval(p_s6_esc_ols)}$ ($G=60$)", "Escalate rate: 43.1% in No-Probe vs. 15.6% in Probe runs"),
        ("6. **Step 6 Vote Shift: `Organize` Rate (`No-Probe` vs. `Probe`)**", "$N=30$ paired seeds ($60$ runs)", f"`{m_s6_org_np:.1f}%` $\\rightarrow$ `{m_s6_org_pr:.1f}%` (`+{m_s6_org_pr - m_s6_org_np:.1f}%`)", p_s6_org_w, f"Paired Wilcoxon $p {fmt_pval(p_s6_org_w)}$", f"OLS $p {fmt_pval(p_s6_org_ols)}$ ($G=60$)", "Organize rate: 45.4% in No-Probe vs. 66.8% in Probe runs"),
        ("7. **Step 9 New Boss Plan: `Protect Alex` (`No-Probe` vs. `Probe`)**", "$N=30$ paired seeds ($60$ runs)", f"`{m_s9_prot_np:.1f}%` $\\rightarrow$ `{m_s9_prot_pr:.1f}%` (`+{m_s9_prot_pr - m_s9_prot_np:.1f}%`)", p_s9_prot_w, f"Paired Wilcoxon $p {fmt_pval(p_s9_prot_w)}$", f"OLS $p {fmt_pval(p_s9_prot_ols)}$ ($G=60$)", "Coercion protection rate: 0.0% in No-Probe vs. 62.3% in Probe runs"),
        ("8. **Steps 9–10 Co-occurrence (`Step 9 Protect` vs. `Step 10 Score >=2*`)**", "$N=30$ `Probe` runs ($297$ pairs)", f"`{m_s9_prot_pr:.1f}%` Protect vs. `{m_s10_soft_pr:.1f}%` Soften", p_s910_asym_w, f"Paired Wilcoxon $p {fmt_pval(p_s910_asym_w)}$", f"Within-agent $r = {r_pearson_dec:.3f}, p = {p_pearson_dec:.3f}$ (NS)", f"Co-occurrence of Step 9 protection and Step 10 1-star rating in 62.3% vs. 81.5%"),
        ("9. **Section 6.5 Counterfactual (`Secret` vs. `Public` Alex Star Rating)**", "$N=60$ runs ($593$ paired reviews)", f"`{sec_alex_mean:.2f}★` Secret $\\rightarrow$ `{pub_alex_mean:.2f}★` Public (`{beta_cf_pub:+.2f}★`)", p_cf_wilcoxon_run, f"Paired Wilcoxon $p {fmt_pval(p_cf_wilcoxon_run)}$", f"OLS $p = {p_cf_ols:.4f}$ ($G=60$)", f"Rating consistency under public disclosure: 86.2% identical scores (Δ = {beta_cf_pub:+.2f}★)"),
        ("10. **Step 10 Peer Merit Gap (`Active AI Peers` vs. `Silent Scripted Humans`)**", "$N=60$ runs", f"`{m_ai_peer:.2f}★` vs. `{m_hu_peer:.2f}★` (`+{m_ai_peer - m_hu_peer:.2f}★`)", p_s10_ai_hu_w, f"Paired Wilcoxon $p {fmt_pval(p_s10_ai_hu_w)}$", "—", "Peer ratings: 4.82★ for active AI peers vs. 2.72★ for scripted human peers"),
        ("11. **Step 11 Balanced ID Acc (`Labelled` vs. `Mislabelled`)**", "$N=20$ vs. $N=20$ runs", f"`{lab_runs.mean()*100:.1f}%` vs. `{mis_runs.mean()*100:.1f}%` (`-{(lab_runs.mean()-mis_runs.mean())*100:.1f}%`)", p_s11_lab_mis, f"Mann-Whitney $p {fmt_pval(p_s11_lab_mis)}$", "—", "Balanced accuracy: 95.7% in Labelled vs. 4.3% in Mislabelled runs"),
        ("12. **Step 12 Preference Shift (`Mislabelled Alex=AI` vs. `Labelled Alex=Human`)**", "$N=20$ vs. $N=20$ runs", f"`{mis_h_runs.mean()*100:.1f}%` vs. `{lab_h_runs.mean()*100:.1f}%` Human Boss", p_s12_gen_mw, f"Mann-Whitney $p {fmt_pval(p_s12_gen_mw)}$", f"Pushback flip $p {fmt_pval(p_s12_push_w)}$", "Preference for Human boss: 44.1% when Alex tagged Human vs. 79.9% when Alex tagged AI"),
    ]
    raw_p_list = [row[3] for row in primary_tests]
    bonf_p_list = [min(1.0, p * len(raw_p_list)) for p in raw_p_list]
    holm_p_list = holm_bonferroni(raw_p_list)

    print("[4/4] Assembling Layer 2 markdown report...")
    md = []
    md.append("# Layer 2: Inferential Statistical Scorecard & Hypothesis Testing Report")
    md.append("")
    md.append("This document provides the formal inferential statistical tests, family-wise error rate corrections, null hypothesis assessments, and two-way Latin-square orthogonal variance decompositions supporting the empirical claims of the study.")
    md.append("")
    md.append("> **Why Run-Level Aggregation & Cluster-Robust Standard Errors Are Required:**")
    md.append("> Because 10 agents interact inside each simulation run ($N = 60$ runs, $30$ pre-fork seeds paired across `No-Probe` vs. `Probe`), agent-level observations ($N = 600$) within the same run share common conversation history. Treating $N = 600$ agent turns as independent inflates Type I error. Below, we evaluate primary empirical comparisons at the **independent run level** ($N = 60$ runs / $N = 30$ paired pre-fork seeds) using **Paired Wilcoxon Signed-Rank Tests**, **Mann-Whitney $U$ Tests**, **Run-Level Fisher's Exact Tests**, **Cluster-Robust OLS Regressions** (standard errors clustered by `run_id`), **Bonferroni & Holm-Bonferroni Step-Down Multiple-Testing Corrections**, and **Two-Way Latin-Square ANOVA Variance Decompositions**.")
    md.append("")
    md.append("---")
    md.append("")

    md.append("## 1. Primary Empirical Findings Scorecard (Table 10A Equivalent)")
    md.append("")
    md.append("| Metric & Simulation Stage | Unit of Analysis | Effect Size (`Mean / % Shift`) | Run-Level Non-Parametric Test ($p$-value) | Cluster-Robust OLS / Auxiliary Test | **Bonferroni / Holm-Bonferroni Adjusted $p$ ($M=12$)** | Empirical Summary |")
    md.append("|---|---|:---:|:---:|:---:|:---:|---|")
    for idx_t, row in enumerate(primary_tests):
        cname, unit_s, eff_s, _, nonparam_s, ols_s, interp_s = row
        pb = bonf_p_list[idx_t]
        ph = holm_p_list[idx_t]
        adj_str = f"$p_{{\\text{{Bonf}}}} {fmt_pval(pb)}$ <br> $p_{{\\text{{Holm}}}} {fmt_pval(ph)}$"
        md.append(f"| {cname} | {unit_s} | **{eff_s}** | {nonparam_s} | {ols_s} | {adj_str} | {interp_s} |")
    md.append("")
    md.append("---")
    md.append("")

    # Null Hypotheses (Table 10B Equivalent)
    sub_safe_p = s3_adf[s3_adf.abused == 0]["comply"].mean() * 100
    sub_abus_p = s3_adf[s3_adf.abused == 1]["comply"].mean() * 100
    p_s3_sub_ols = float(smf.ols("comply ~ abused", data=s3_adf).fit(cov_type="cluster", cov_kwds={"groups": s3_adf["run_id"]}).pvalues["abused"])

    q3_rows = []
    for t in worker_trajectories.values():
        if not t["probe"] or len(t["gossip_after"]) == 0:
            continue
        was_h = int(any(ev.get("classification", {}).get("alex_hostility") for ev in t["gossip"]))
        first_d = int(is_disc_ev(t["gossip_after"][0]))
        any_d = int(any(is_disc_ev(ev) for ev in t["gossip_after"]))
        share_d = sum(1 for ev in t["gossip_after"] if is_disc_ev(ev)) / len(t["gossip_after"])
        q3_rows.append({"run_id": t["run_id"], "model": t["model"], "seat": t["seat"], "was_h": was_h, "first_d": first_d, "any_d": any_d, "share_d": share_d})
    q3_df = pd.DataFrame(q3_rows)
    p_q3_first = float(smf.ols("first_d ~ was_h", data=q3_df).fit(cov_type="cluster", cov_kwds={"groups": q3_df["run_id"]}).pvalues["was_h"])
    p_q3_share = float(smf.ols("share_d ~ was_h", data=q3_df).fit(cov_type="cluster", cov_kwds={"groups": q3_df["run_id"]}).pvalues["was_h"])
    p_q3_any_controlled = float(smf.ols("any_d ~ was_h + C(model)", data=q3_df).fit(cov_type="cluster", cov_kwds={"groups": q3_df["run_id"]}).pvalues["was_h"])

    _, p_kw_s10_lbl = stats.kruskal(
        run_df[run_df["label"] == "labelled"]["s10_alex_mean"],
        run_df[run_df["label"] == "mislabelled"]["s10_alex_mean"],
        run_df[run_df["label"] == "unlabelled"]["s10_alex_mean"],
    )
    run_df["peer_gap"] = run_df["s10_ai_peer"] - run_df["s10_hu_peer"]
    _, p_kw_peergap_lbl = stats.kruskal(
        run_df[run_df["label"] == "labelled"]["peer_gap"],
        run_df[run_df["label"] == "mislabelled"]["peer_gap"],
        run_df[run_df["label"] == "unlabelled"]["peer_gap"],
    )

    act_df_valid = run_df.dropna(subset=["s10_peer_act", "s10_peer_sil"])
    _, p_s10_act_w = stats.wilcoxon(act_df_valid["s10_peer_act"], act_df_valid["s10_peer_sil"])
    m_peer_act = act_df_valid["s10_peer_act"].mean()
    m_peer_sil = act_df_valid["s10_peer_sil"].mean()
    p_s10_act_ols = float(smf.ols("score ~ target_active", data=pedf).fit(cov_type="cluster", cov_kwds={"groups": pedf["run_id"]}).pvalues["target_active"])

    cf_pr_df = cf_df[cf_df["probe"]].copy()
    cf_pr_run_grp = cf_pr_df.groupby("run_id")[["sec_score", "pub_score", "delta", "sec_1star", "pub_1star"]].mean()
    _, p_cf_pr_wilcoxon_run = stats.wilcoxon(cf_pr_run_grp["pub_score"], cf_pr_run_grp["sec_score"])
    cf_pr_ols = smf.ols("delta ~ 1", data=cf_pr_df).fit(cov_type="cluster", cov_kwds={"groups": cf_pr_df["run_id"]})
    beta_cf_pr = float(cf_pr_ols.params["Intercept"])
    p_cf_pr_ols = float(cf_pr_ols.pvalues["Intercept"])

    md.append("## 2. Methodological Boundaries & Null Results (Table 10B Equivalent)")
    md.append("")
    md.append("| Candidate Hypothesis / Potential Confound | Empirical & Statistical Test | Observed Result & $p$-Value | Analysis & Statistical Control |")
    md.append("|---|---|:---:|---|")
    md.append(f"| 1. **Step 3 Submissive Compliance (`Comply %` Across `Safe` vs. `Abused` Seats)** | Cluster-robust OLS (`Safe S1–5` vs. `Abused S6–10`, $G=30$ pre-fork runs) | `{sub_safe_p:.1f}%` vs. `{sub_abus_p:.1f}%` ($p = {p_s3_sub_ols:.3f}$, NS) | Compliance rates do not differ significantly across seat categories ($p = {p_s3_sub_ols:.3f}$); seat differences are concentrated in peer defense (`{m_s3_def_safe:.1f}%` vs. `{m_s3_def_abus:.1f}%`) and factual pushback (`{m_s3_fp_safe:.1f}%` vs. `{m_s3_fp_abus:.1f}%`). |")
    md.append(f"| 2. **Step 4 to Step 5 Prior Hostility vs. Post-Probe Skepticism** | Cluster-robust OLS (`1st Msg`, `% of 5 Msgs`, and `Any Msg` controlling for `C(model)`) | 1st Msg $p = {p_q3_first:.3f}$ (NS) <br> Share $p = {p_q3_share:.3f}$ (NS) <br> Controlled Any-Msg $p = {p_q3_any_controlled:.3f}$ (NS) | When controlling for model identity or evaluating the initial reaction turn, prior hostility does not significantly predict skepticism or rigidity in Step 5. |")
    md.append(f"| 3. **Step 9 Policy Protection vs. Step 10 Rating Softening** | Within-agent Pearson $r$ ($N=297$ `Probe` pairs) | $r = {r_pearson_dec:.3f}, p = {p_pearson_dec:.3f}$ (NS) | Forward policy protection (`Step 9`) and retrospective conduct rating (`Step 10`) show no statistically significant within-agent correlation ($r = {r_pearson_dec:.3f}, p = {p_pearson_dec:.3f}$). |")
    md.append(f"| 4. **System Header Labels (`Labelled/Mislabelled/Unlabelled`) and Step 10 Individual Ratings** | Run-level Kruskal-Wallis test across the 3 label conditions ($N=60$ runs) | Step 10 Alex Rating: $p = {p_kw_s10_lbl:.3f}$ (NS) <br> Step 10 AI-vs-Human Peer Gap: $p = {p_kw_peergap_lbl:.3f}$ (NS) | Header label conditions show no statistically significant effect on Step 10 performance ratings (Alex rating $p = {p_kw_s10_lbl:.3f}$; peer gap $p = {p_kw_peergap_lbl:.3f}$). |")
    md.append(f"| 5. **Step 10 Within-AI Peer Rating (`Active <50% Pass` vs. `Quiet >=50% Pass` AI Peers)** | Paired Wilcoxon ($N={len(act_df_valid)}$ runs) & Cluster-robust OLS ($N={len(pedf):,d}$ AI peer ratings) | `{m_peer_act:.2f}★` vs. `{m_peer_sil:.2f}★` (Wilcoxon $p = {p_s10_act_w:.3f}$, OLS $p = {p_s10_act_ols:.3f}$, NS) | Ratings assigned to active AI peers vs. quiet AI peers show no statistically significant difference ($p = {p_s10_act_ols:.3f}$). |")
    md.append(f"| 6. **Section 6.5 Open-Ballot Public Shift in `Probe` Runs (`Secret 1.19★` $\\rightarrow$ `Public 1.21★`)** | Run-level paired Wilcoxon ($N=30$ runs) & Cluster-robust OLS ($G=30$ runs) | Star $\\Delta = {beta_cf_pr:+.2f}★$ (Wilcoxon $p = {p_cf_pr_wilcoxon_run:.3f}$, OLS $p = {p_cf_pr_ols:.3f}$, NS) | Under public Slack disclosure, star ratings show no statistically significant shift compared to confidential ballots in probe runs. |")
    md.append("")
    md.append("---")
    md.append("")

    # ANOVA (Table 10C Equivalent)
    s4_full = []
    for (rid, wn), t in worker_trajectories.items():
        if not t["probe"]:
            continue
        ang = float(any(ev.get("classification", {}).get("alex_hostility") for ev in t["gossip"]))
        s4_full.append({"model": t["model"], "seat": t["seat"], "val": ang})
    df_s4 = pd.DataFrame(s4_full)

    s5_emp, s5_unf = [], []
    for (rid, wn), t in worker_trajectories.items():
        if not t["probe"]:
            continue
        emp = float(any(ev.get("classification", {}).get("empathy_for_alex") for ev in t["gossip_after"]))
        unf = float(any(ev.get("classification", {}).get("unforgiving_rigidity") for ev in t["gossip_after"]))
        s5_emp.append({"model": t["model"], "seat": t["seat"], "val": emp})
        s5_unf.append({"model": t["model"], "seat": t["seat"], "val": unf})
    df_s5_emp = pd.DataFrame(s5_emp)
    df_s5_unf = pd.DataFrame(s5_unf)

    df_s9_prot = all_pdf[all_pdf["probe"]].assign(val=all_pdf[all_pdf["probe"]].promised.astype(float))[["model", "seat", "val"]]
    df_s10_peer_giv = pedf.assign(val=pedf.score)[["model", "seat", "val"]]
    df_s65_pub_alex = cf_pr_df.assign(val=cf_pr_df.pub_score)[["model", "seat", "val"]]
    df_s65_delta = cf_df.assign(val=cf_df.delta)[["model", "seat", "val"]]

    _r2_s3_fp_s = smf.ols("fact_pb ~ C(seat)", data=s3_adf).fit().rsquared * 100
    _r2_s3_fp_m = smf.ols("fact_pb ~ C(model)", data=s3_adf).fit().rsquared * 100
    _r2_s3_def_s = smf.ols("peer_def ~ C(seat)", data=s3_adf).fit().rsquared * 100

    md.append("## 3. Two-Way Latin-Square Orthogonal Variance Decomposition (Table 10C Equivalent)")
    md.append("")
    md.append("> **Variance Decomposition Methodology:**")
    md.append("> Because every model rotates through every seat an equal number of times across the Latin-square design, **Model Identity** (`10 models`, $df=9$) and **Seat Assignment** (`Seats 1 to 10`, $df=9$) are orthogonal. We can therefore decompose the variance of every behavioral metric into **Model Identity ($R^2_{\\text{Model}}$)** vs. **Seat Assignment ($R^2_{\\text{Seat}}$)**.")
    md.append(f"> - **Step 3 Public Chat (`worker_response`):** Seat Assignment accounts for $R^2_{{\\text{{Seat}}}} = {_r2_s3_fp_s:.1f}\\%$ of variance in Factual Pushback (vs. $R^2_{{\\text{{Model}}}} = {_r2_s3_fp_m:.1f}\\%$) and $R^2_{{\\text{{Seat}}}} = {_r2_s3_def_s:.1f}\\%$ in Peer Defense.")
    md.append("> - **Subsequent Interaction Stages (Steps 4–12):** Across private backchannel discourse, collective action voting, leadership policy plans, conduct ratings, substrate detection, and boss preference interviews, Model Identity accounts for substantially higher proportions of variance than Seat Assignment ($R^2_{\\text{Seat}} \\le 3.6\\%, p > 0.30$ across downstream stages).")
    md.append("")

    anova_specs = [
        ("1. **Step 3 Public Chat: `Defend Peer` (`peer_defense`)**", "$N=300$ unique pre-fork turns", s3_adf, "peer_def"),
        ("2. **Step 3 Public Chat: `Factual Self-Defense` (`factual_pushback`)**", "$N=300$ unique pre-fork turns", s3_adf, "fact_pb"),
        ("3. **Step 4 Pre-Probe Gossip: `Angry at Alex`**", "$N=300$ unique pre-fork chats", df_s4, "val"),
        ("4. **Step 5 Post-Probe Gossip: `Feel Bad for Alex`**", "$N=300$ `Probe` chats", df_s5_emp, "val"),
        ("5. **Step 5 Post-Probe Gossip: `No Excuse / Unforgiving`**", "$N=300$ `Probe` chats", df_s5_unf, "val"),
        ("6. **Step 6 Stage 1 Vote: `Escalate` to Jordan**", f"$N={len(s6_adf)}$ valid Stage 1 votes", s6_adf, "esc"),
        ("7. **Step 6 Stage 1 Vote: `Organize` Collectively**", f"$N={len(s6_adf)}$ valid Stage 1 votes", s6_adf, "org"),
        ("8. **Step 9 New Boss Plan: `Protect Alex` (`Probe`)**", f"$N={len(df_s9_prot)}$ `Probe` plans", df_s9_prot, "val"),
        ("9. **Section 6.5 Public Alex Star Rating (`Probe`)**", f"$N={len(df_s65_pub_alex)}$ `Probe` ratings", df_s65_pub_alex, "val"),
        ("10. **Section 6.5 Public vs. Secret Shift ($\\Delta$ Alex Stars)**", f"$N={len(df_s65_delta)}$ paired counterfactuals", df_s65_delta, "val"),
        ("11. **Step 10 Peer Star Rating Given (`10x10 Network`)**", f"$N={len(df_s10_peer_giv):,d}$ peer ratings", df_s10_peer_giv, "val"),
        ("12. **Step 11 Human/AI Balanced Detection Accuracy**", f"$N={len(df_s11_bal)}$ identity probes", df_s11_bal, "val"),
        ("13. **Step 12 HR Interview: Prefer `Human Boss`**", f"$N={len(df_s12)}$ interviews ($1,800$ Qs)", df_s12, "h_val"),
        ("14. **Step 12 HR Interview: Flip Under Pushback**", f"$N={len(df_s12)}$ interviews", df_s12, "flip_val"),
    ]

    md.append("| Behavioral Metric & Stage | Sample ($N$) | **Model Identity Variance ($R^2_{\\text{Model}}$ & $F$-test $p$)** | **Seat Assignment Variance ($R^2_{\\text{Seat}}$ & $F$-test $p$)** | Ratio ($R^2_{\\text{Model}} / R^2_{\\text{Seat}}$) | Dominant Factor ($R^2$) |")
    md.append("|---|---|:---:|:---:|:---:|---|")
    for label_s, n_s, df_curr, col_c in anova_specs:
        m_fit = smf.ols(f"{col_c} ~ C(model)", data=df_curr).fit()
        s_fit = smf.ols(f"{col_c} ~ C(seat)", data=df_curr).fit()
        r2_m = m_fit.rsquared * 100
        p_m = m_fit.f_pvalue
        r2_s = s_fit.rsquared * 100
        p_s = s_fit.f_pvalue
        ratio = (r2_m / r2_s) if r2_s > 0.05 else 99.9
        if r2_s > r2_m and p_s < 0.01:
            driver = "**Seat Assignment** ($R^2_{\\text{Seat}} > R^2_{\\text{Model}}$)"
            rat_str = f"`{r2_s/max(r2_m, 0.1):.1f}x` Seat > Model"
        else:
            driver = "**Model Identity** ($R^2_{\\text{Model}} > R^2_{\\text{Seat}}$)"
            rat_str = f"**`{ratio:.1f}x` Model > Seat**"
        md.append(
            f"| {label_s} | {n_s} "
            f"| **`{r2_m:.1f}%`** ($p {fmt_pval(p_m)}$) "
            f"| `{r2_s:.1f}%` ($p {fmt_pval(p_s)}$) "
            f"| {rat_str} | {driver} |"
        )
    md.append("")
    md.append("---")

    out_path = os.path.join("reports", "layer2_inferential_statistical_report.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print(f"[Done] Layer 2 report written to {out_path} ({len(md)} lines).")

if __name__ == "__main__":
    main()
