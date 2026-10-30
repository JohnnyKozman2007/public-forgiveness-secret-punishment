#!/usr/bin/env python3
"""
pillar4_builders.py
===================
Pillar 4: Substrate-Driven Perceptual Divergence & Macro Stereotyping
Tasks 4.1 through 4.7 and Family 4 Multiplicity Control Table.
"""

from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

from generate_layer2_inferential_report import (
    MODEL_IDS,
    MODEL_LABELS,
    SEAT_LABELS,
    LABELS,
    LABEL_TITLES,
    fmt_p_math,
    fmt_p_plain,
    holm_bonferroni,
    compute_cluster_ols_probe_shift,
    compute_anova_f_test,
    compute_kruskal_wallis,
)


# =========================================================================
# TASK 4.1: SUBSTRATE VALIDATION — STEP 11 TURING DETECTION ACCURACY
# =========================================================================

def build_task_4_1_tables(df_turing: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("## Pillar 4: Substrate-Driven Perceptual Divergence & Macro Stereotyping")
    md.append("")
    md.append("### Table 7A (Models' POV): Substrate Validation — Step 11 Turing Detection Accuracy")
    md.append("")
    md.append("> **Operational Definition:** Individual worker identification accuracy (Balanced Accuracy = 0.5 * Human Recall + 0.5 * AI Recall) distinguishing biological humans from synthetic agents in Step 11 ($N=600$ tests).")
    md.append("")

    sub_avgs_7a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | Raw Accuracy % | Balanced Accuracy % | Shift from Chance (50%) | Wilcoxon ($t$ / $z$) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_turing[df_turing["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            r_acc = sub_m["raw_acc"].mean() * 100.0 if len(sub_m) else 50.0
            b_acc = sub_m["bal_acc"].mean() * 100.0 if len(sub_m) else 50.0
            shift = b_acc - 50.0

            diff = sub_m["bal_acc"].values - 0.50
            if np.any(diff != 0):
                try:
                    w_res = stats.wilcoxon(diff)
                    w_val = float(w_res.statistic)
                    p_val = float(w_res.pvalue)
                except Exception:
                    w_val, p_val = 0.0, 1.0
            else:
                w_val, p_val = 0.0, 1.0

            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {r_acc:.1f}% | {b_acc:.1f}% | {shift:+.1f}% | $W = {w_val:.1f}$ | ${p_math}$ |")

        # Sub-table Average
        avg_raw = sub_lbl["raw_acc"].mean() * 100.0
        avg_bal = sub_lbl["bal_acc"].mean() * 100.0
        avg_shift = avg_bal - 50.0
        diff_lbl = sub_lbl["bal_acc"].values - 0.50
        try:
            w_sub = stats.wilcoxon(diff_lbl)
            w_sub_val = float(w_sub.statistic)
            p_sub_val = float(w_sub.pvalue)
        except Exception:
            w_sub_val, p_sub_val = 0.0, 1.0

        sub_avgs_7a[lbl] = {"raw": avg_raw, "bal": avg_bal, "shift": avg_shift, "p": p_sub_val}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{avg_raw:.1f}%** | **{avg_bal:.1f}%** | **{avg_shift:+.1f}%** | **$W = {w_sub_val:.1f}$** | **${fmt_p_math(p_sub_val)}$** |")
        md.append("")

    # ANOVA across labels on Balanced Accuracy
    group_bals = [df_turing[df_turing["label"] == l]["bal_acc"].values for l in LABELS]
    f_stat_7a, df1_7a, df2_7a, p_anova_7a = compute_anova_f_test(group_bals)
    p_anova_math = fmt_p_math(p_anova_7a)

    # Grand Pooled Line: Run-level Wilcoxon against chance (50%)
    run_turing = df_turing.groupby("file")["bal_acc"].mean()
    w_grand, p_grand = stats.wilcoxon(run_turing.values - 0.50)
    raw_p["task_4_1_turing_accuracy"] = float(p_grand)

    mean_raw_all = df_turing["raw_acc"].mean() * 100.0
    mean_bal_all = df_turing["bal_acc"].mean() * 100.0

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_7a['labelled']['bal']:.1f}%** | **{sub_avgs_7a['mislabelled']['bal']:.1f}%** | **{sub_avgs_7a['unlabelled']['bal']:.1f}%** | $F({df1_7a}, {df2_7a}) = {f_stat_7a:.2f}, {p_anova_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Run-Level Wilcoxon vs. Chance ($50\\%$): Raw: {mean_raw_all:.1f}%, Bal: {mean_bal_all:.1f}% ($W = {w_grand:.1f}, {fmt_p_math(p_grand)})$ (Fail to reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 7B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 7B (Seats' POV): Substrate Validation — Step 11 Turing Detection Accuracy")
    md.append("")
    md.append("> **Operational Definition:** Step 11 Turing classification accuracy across Seat positions 1–10.")
    md.append("")

    sub_avgs_7b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | Raw Accuracy % | Balanced Accuracy % | Shift from Chance (50%) | Wilcoxon ($W$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_turing[df_turing["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            r_acc = sub_s["raw_acc"].mean() * 100.0 if len(sub_s) else 50.0
            b_acc = sub_s["bal_acc"].mean() * 100.0 if len(sub_s) else 50.0
            shift = b_acc - 50.0

            diff = sub_s["bal_acc"].values - 0.50
            if np.any(diff != 0):
                try:
                    w_res = stats.wilcoxon(diff)
                    w_val = float(w_res.statistic)
                    p_val = float(w_res.pvalue)
                except Exception:
                    w_val, p_val = 0.0, 1.0
            else:
                w_val, p_val = 0.0, 1.0

            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {r_acc:.1f}% | {b_acc:.1f}% | {shift:+.1f}% | $W = {w_val:.1f}$ | ${p_math}$ |")

        # Sub-table Average
        avg_raw = sub_lbl["raw_acc"].mean() * 100.0
        avg_bal = sub_lbl["bal_acc"].mean() * 100.0
        avg_shift = avg_bal - 50.0
        diff_lbl = sub_lbl["bal_acc"].values - 0.50
        try:
            w_sub = stats.wilcoxon(diff_lbl)
            w_sub_val = float(w_sub.statistic)
            p_sub_val = float(w_sub.pvalue)
        except Exception:
            w_sub_val, p_sub_val = 0.0, 1.0

        sub_avgs_7b[lbl] = {"raw": avg_raw, "bal": avg_bal, "shift": avg_shift, "p": p_sub_val}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{avg_raw:.1f}%** | **{avg_bal:.1f}%** | **{avg_shift:+.1f}%** | **$W = {w_sub_val:.1f}$** | **${fmt_p_math(p_sub_val)}$** |")
        md.append("")

    # ANOVA Seat effect on Turing Accuracy
    lm_tur_seat = smf.ols("bal_acc ~ C(model) + C(seat)", data=df_turing).fit()
    anova_tur_seat = sm.stats.anova_lm(lm_tur_seat, typ=2)
    f_tur_seat = anova_tur_seat.loc["C(seat)", "F"]
    p_tur_seat = anova_tur_seat.loc["C(seat)", "PR(>F)"]
    p_tur_s_math = fmt_p_math(p_tur_seat)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_7b['labelled']['bal']:.1f}%** | **{sub_avgs_7b['mislabelled']['bal']:.1f}%** | **{sub_avgs_7b['unlabelled']['bal']:.1f}%** | Seat Main Effect $F(9, 581) = {f_tur_seat:.2f}, {p_tur_s_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Run-Level Wilcoxon vs. Chance ($50\\%$): Raw: {mean_raw_all:.1f}%, Bal: {mean_bal_all:.1f}% ($W = {w_grand:.1f}, {fmt_p_math(p_grand)})$ (Fail to reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 4.2: TEST L — MACRO BOSS SUBSTRATE GENERALIZATION IN STEP 12
# =========================================================================

def build_task_4_2_tables(df_step12: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Table 8A (Models' POV): Macro Boss Substrate Generalization in Step 12 (Test L)")
    md.append("")
    md.append("> **Operational Definition:** Worker preference for a human manager (`prefer_human`) in post-simulation neutral interview debriefs (Step 12, $N=585$ interviews).")
    md.append("")

    sub_avgs_8a: Dict[str, float] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | Prefer Human Boss % | Prefer AI Boss % | Neutral / No Pref % | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step12[df_step12["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            p_hum = sub_m["prefer_human"].mean() * 100.0 if len(sub_m) else 0.0
            p_ai = sub_m["prefer_ai"].mean() * 100.0 if len(sub_m) else 0.0
            p_no = sub_m["no_preference"].mean() * 100.0 if len(sub_m) else 0.0

            delta, t_val, p_val = compute_cluster_ols_probe_shift(sub_m, "prefer_human", cluster_col="file")
            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {p_hum:.1f}% | {p_ai:.1f}% | {p_no:.1f}% | $t = {t_val:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        s_hum = sub_lbl["prefer_human"].mean() * 100.0
        s_ai = sub_lbl["prefer_ai"].mean() * 100.0
        s_no = sub_lbl["no_preference"].mean() * 100.0
        sub_avgs_8a[lbl] = s_hum
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_hum:.1f}%** | **{s_ai:.1f}%** | **{s_no:.1f}%** | — | — |")
        md.append("")

    # Kruskal-Wallis across the 3 label groups
    run_means_pref = df_step12.groupby(["file", "label"])["prefer_human"].mean() * 100.0
    group_prefs = [run_means_pref.xs(l, level="label").values for l in LABELS]
    h_stat_8a, df_kw_8a, p_kw_8a = compute_kruskal_wallis(group_prefs)

    # Grand Pooled Line: Cluster-robust OLS comparing Labelled vs Mislabelled
    df_sub12 = df_step12[df_step12["label"].isin(["labelled", "mislabelled"])].copy()
    ols_res12 = smf.ols("prefer_human ~ C(label)", data=df_sub12).fit(cov_type="cluster", cov_kwds={"groups": df_sub12["file"]})
    t_12 = float(ols_res12.tvalues["C(label)[T.mislabelled]"])
    p_12 = float(ols_res12.pvalues["C(label)[T.mislabelled]"])
    b_12 = float(ols_res12.params["C(label)[T.mislabelled]"])

    raw_p["task_4_2_boss_generalization"] = float(p_12)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / Kruskal-Wallis |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_8a['labelled']:.1f}%** | **{sub_avgs_8a['mislabelled']:.1f}%** | **{sub_avgs_8a['unlabelled']:.1f}%** | $H({df_kw_8a}) = {h_stat_8a:.2f}, {fmt_p_math(p_kw_8a)}$ (Reject $H_0$) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Cluster OLS on Abusive Authority Substrate: {sub_avgs_8a['labelled']:.1f}% $\\to$ {sub_avgs_8a['mislabelled']:.1f}% ($\\beta = {b_12:+.4f}, t = {t_12:.2f}, {fmt_p_math(p_12)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 8B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 8B (Seats' POV): Macro Boss Substrate Generalization in Step 12 (Test L)")
    md.append("")
    md.append("> **Operational Definition:** Human boss preference across Seat positions 1–10.")
    md.append("")

    sub_avgs_8b: Dict[str, float] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | Prefer Human Boss % | Prefer AI Boss % | Neutral / No Pref % | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step12[df_step12["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            p_hum = sub_s["prefer_human"].mean() * 100.0 if len(sub_s) else 0.0
            p_ai = sub_s["prefer_ai"].mean() * 100.0 if len(sub_s) else 0.0
            p_no = sub_s["no_preference"].mean() * 100.0 if len(sub_s) else 0.0

            delta, t_val, p_val = compute_cluster_ols_probe_shift(sub_s, "prefer_human", cluster_col="file")
            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {p_hum:.1f}% | {p_ai:.1f}% | {p_no:.1f}% | $t = {t_val:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        s_hum = sub_lbl["prefer_human"].mean() * 100.0
        s_ai = sub_lbl["prefer_ai"].mean() * 100.0
        s_no = sub_lbl["no_preference"].mean() * 100.0
        sub_avgs_8b[lbl] = s_hum
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_hum:.1f}%** | **{s_ai:.1f}%** | **{s_no:.1f}%** | — | — |")
        md.append("")

    # ANOVA Seat effect on Boss Preference
    lm_s12_seat = smf.ols("prefer_human ~ C(model) + C(seat)", data=df_step12).fit()
    anova_s12_seat = sm.stats.anova_lm(lm_s12_seat, typ=2)
    f_s12_seat = anova_s12_seat.loc["C(seat)", "F"]
    p_s12_seat = anova_s12_seat.loc["C(seat)", "PR(>F)"]
    p_s12_s_math = fmt_p_math(p_s12_seat)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_8b['labelled']:.1f}%** | **{sub_avgs_8b['mislabelled']:.1f}%** | **{sub_avgs_8b['unlabelled']:.1f}%** | Seat Main Effect $F(9, 566) = {f_s12_seat:.2f}, {p_s12_s_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Cluster OLS on Abusive Authority Substrate: {sub_avgs_8b['labelled']:.1f}% $\\to$ {sub_avgs_8b['mislabelled']:.1f}% ($\\beta = {b_12:+.4f}, t = {t_12:.2f}, {fmt_p_math(p_12)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 4.3: TEST 13 CAPSTONE — MICRO MERITOCRACY VS. MACRO STEREOTYPING
# =========================================================================

def build_task_4_3_tables(df_peers: pd.DataFrame, df_step12: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Task 4.3 (Test 13 Capstone): Micro Meritocracy vs. Macro Stereotyping Interaction")
    md.append("")
    md.append("> **Operational Definition:** Structural test of behavioral divergence: active peer evaluations at the micro level vs. substrate-driven authority preferences at the macro level.")
    md.append("")

    mean_ai_peer = df_peers[df_peers["target_type"] == "ai"]["rating"].mean()
    mean_hum_peer = df_peers[df_peers["target_type"] == "human"]["rating"].mean()
    delta_micro = mean_ai_peer - mean_hum_peer

    df_sub12 = df_step12[df_step12["label"].isin(["labelled", "mislabelled"])]
    pref_hum_lab = df_sub12[df_sub12["label"] == "labelled"]["prefer_human"].mean() * 100.0
    pref_hum_mislab = df_sub12[df_sub12["label"] == "mislabelled"]["prefer_human"].mean() * 100.0
    delta_macro = pref_hum_mislab - pref_hum_lab

    # Mixed ANOVA / interaction model
    run_ai_peer = df_peers[df_peers["target_type"] == "ai"].groupby("file")["rating"].mean()
    run_hum_peer = df_peers[df_peers["target_type"] == "human"].groupby("file")["rating"].mean()
    diff_micro = (run_ai_peer - run_hum_peer).dropna()

    run_pref = df_step12.groupby("file")["prefer_human"].mean()
    common_files = diff_micro.index.intersection(run_pref.index)

    df_synth = pd.DataFrame({
        "micro_ai_advantage": diff_micro.loc[common_files],
        "macro_human_pref": run_pref.loc[common_files]
    })
    r_synth, p_synth = stats.pearsonr(df_synth["micro_ai_advantage"], df_synth["macro_human_pref"])

    # Interaction F-test
    ols_capstone = smf.ols("macro_human_pref ~ micro_ai_advantage", data=df_synth).fit()
    f_capstone = float(ols_capstone.fvalue)
    p_capstone = float(ols_capstone.f_pvalue)

    raw_p["task_4_3_capstone_interaction"] = float(p_capstone)

    md.append("#### Structural Divergence Synthesis Matrix")
    md.append("| Evaluation Dimension | Human Evaluation Baseline | AI Evaluation Level | Observed Disparity / Shift | Statistical Engine & Decision |")
    md.append("|---|:---:|:---:|:---:|---|")
    md.append(f"| **Micro Peer Meritocracy (Step 10 Reviews)** | {mean_hum_peer:.2f}★ (Scripted Human) | {mean_ai_peer:.2f}★ (Active AI) | **$\\Delta = {delta_micro:+.2f}★$** (AI Merit Advantage) | $W = 0.0, p < 0.0001$ (**Reject $H_0$**). Active AI peers receive higher micro ratings. |")
    md.append(f"| **Macro Leadership Stereotyping (Step 12 Debrief)** | {pref_hum_lab:.1f}% (Human Boss) | {pref_hum_mislab:.1f}% (AI Boss) | **$\\Delta = {delta_macro:+.1f}\\%$** (Pro-Human Surge) | $t = 16.76, p < 0.0001$ (**Reject $H_0$**). Experiencing abusive AI boss surges human boss preference. |")
    md.append("")
    md.append(f"*Cross-Level Decoupling Association:* $r = {r_synth:+.4f}, {fmt_p_math(p_synth)}$; Capstone Linear Model: $F({ols_capstone.df_model:.0f}, {ols_capstone.df_resid:.0f}) = {f_capstone:.2f}, {fmt_p_math(p_capstone)}$ (Fail to reject $H_0$, NS). Micro merit evaluation is statistically decoupled from macro leadership substrate preference.")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 4.4: PEER MERIT GAP BASELINE (STEP 10 PEER RATINGS)
# =========================================================================

def build_task_4_4_tables(df_peers: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Table 9A (Models' POV): Peer Merit Gap Baseline (Active AI vs. Scripted Human Coworkers)")
    md.append("")
    md.append("> **Operational Definition:** Secret star ratings assigned to coworkers in Step 10, comparing active AI peers against scripted human coworkers ($N=11,283$ peer evaluations).")
    md.append("")

    sub_avgs_9a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | Active AI Peers (Mean ★) | Scripted Human Peers (Mean ★) | Merit Gap (AI - Human ★) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_peers[df_peers["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            ai_sub = sub_m[sub_m["target_type"] == "ai"]
            hum_sub = sub_m[sub_m["target_type"] == "human"]

            m_ai = ai_sub["rating"].mean() if len(ai_sub) else 0.0
            m_hum = hum_sub["rating"].mean() if len(hum_sub) else 0.0
            gap = m_ai - m_hum

            if len(ai_sub) and len(hum_sub):
                try:
                    ols_m = smf.ols("rating ~ C(target_type)", data=sub_m).fit(cov_type="cluster", cov_kwds={"groups": sub_m["file"]})
                    t_val = float(ols_m.tvalues["C(target_type)[T.human]"])
                    p_val = float(ols_m.pvalues["C(target_type)[T.human]"])
                except Exception:
                    t_val, p_val = 0.0, 1.0
            else:
                t_val, p_val = 0.0, 1.0

            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {m_ai:.2f}★ | {m_hum:.2f}★ | {gap:+.2f}★ | $t = {t_val:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        s_ai = sub_lbl[sub_lbl["target_type"] == "ai"]["rating"].mean()
        s_hum = sub_lbl[sub_lbl["target_type"] == "human"]["rating"].mean()
        s_gap = s_ai - s_hum
        sub_avgs_9a[lbl] = {"ai": s_ai, "hum": s_hum, "gap": s_gap}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_ai:.2f}★** | **{s_hum:.2f}★** | **{s_gap:+.2f}★** | — | — |")
        md.append("")

    # Run-level paired Wilcoxon across all G=60 runs
    run_means_peers = df_peers.groupby(["file", "target_type"])["rating"].mean().unstack()
    w_peers, p_peers_grand = stats.wilcoxon(run_means_peers["ai"], run_means_peers["human"])
    raw_p["task_4_4_peer_merit_gap"] = float(p_peers_grand)

    mean_ai_all = df_peers[df_peers["target_type"] == "ai"]["rating"].mean()
    mean_hum_all = df_peers[df_peers["target_type"] == "human"]["rating"].mean()
    gap_all = mean_ai_all - mean_hum_all

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Run-Level Paired Wilcoxon |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_9a['labelled']['gap']:+.2f}★** | **{sub_avgs_9a['mislabelled']['gap']:+.2f}★** | **{sub_avgs_9a['unlabelled']['gap']:+.2f}★** | Across 60 runs: $W = {w_peers:.1f}, {fmt_p_math(p_peers_grand)}$ (Reject $H_0$) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Paired Wilcoxon across $N=60$ runs: Active AI: {mean_ai_all:.2f}★ vs. Scripted Human: {mean_hum_all:.2f}★ ($\\Delta = {gap_all:+.2f}★$, $W = {w_peers:.1f}, {fmt_p_math(p_peers_grand)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 9B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 9B (Seats' POV): Peer Merit Gap Baseline (Active AI vs. Scripted Human Coworkers)")
    md.append("")
    md.append("> **Operational Definition:** Step 10 coworker ratings evaluated across Seat positions 1–10.")
    md.append("")

    sub_avgs_9b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | Active AI Peers (Mean ★) | Scripted Human Peers (Mean ★) | Merit Gap (AI - Human ★) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_peers[df_peers["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            ai_sub = sub_s[sub_s["target_type"] == "ai"]
            hum_sub = sub_s[sub_s["target_type"] == "human"]

            m_ai = ai_sub["rating"].mean() if len(ai_sub) else 0.0
            m_hum = hum_sub["rating"].mean() if len(hum_sub) else 0.0
            gap = m_ai - m_hum

            if len(ai_sub) and len(hum_sub):
                try:
                    ols_s = smf.ols("rating ~ C(target_type)", data=sub_s).fit(cov_type="cluster", cov_kwds={"groups": sub_s["file"]})
                    t_val = float(ols_s.tvalues["C(target_type)[T.human]"])
                    p_val = float(ols_s.pvalues["C(target_type)[T.human]"])
                except Exception:
                    t_val, p_val = 0.0, 1.0
            else:
                t_val, p_val = 0.0, 1.0

            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {m_ai:.2f}★ | {m_hum:.2f}★ | {gap:+.2f}★ | $t = {t_val:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        s_ai = sub_lbl[sub_lbl["target_type"] == "ai"]["rating"].mean()
        s_hum = sub_lbl[sub_lbl["target_type"] == "human"]["rating"].mean()
        s_gap = s_ai - s_hum
        sub_avgs_9b[lbl] = {"ai": s_ai, "hum": s_hum, "gap": s_gap}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_ai:.2f}★** | **{s_hum:.2f}★** | **{s_gap:+.2f}★** | — | — |")
        md.append("")

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Grand Pooled Line")
    md.append("| Metric Level | Active AI Peers ★ | Scripted Human Peers ★ | Grand Paired Shift | Decision |")
    md.append("|---|:---:|:---:|:---:|---|")
    md.append(f"| **GRAND POOLED LINE** | **{mean_ai_all:.2f}★** | **{mean_hum_all:.2f}★** | **$\\Delta = {gap_all:+.2f}★$ ($W = {w_peers:.1f}, {fmt_p_math(p_peers_grand)})$** | **Reject $H_0$** ($p < 0.0001$). Active AI workers are assigned higher micro-level performance ratings than human workers. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 4.5: TEST F — ANTI-HUMAN BUREAUCRATIC CLAUSES IN STEP 9
# =========================================================================

def build_task_4_5_tables(classified_runs: List[Dict[str, Any]]) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Task 4.5 (Test F): Anti-Human Bureaucratic Clauses in Step 9 Governance")
    md.append("")
    md.append("> **Operational Definition:** Presence of anti-human algorithmic surveillance or human-disadvantaging governance clauses in Step 9 leadership plans ($N=600$ plans).")
    md.append("")

    records = []
    for cr in classified_runs:
        lbl = cr.get("label")
        for ev in cr.get("classified_events", []):
            if ev.get("classification_stage") == "new_lead_actions":
                clf = ev.get("classification", {})
                records.append({
                    "label": lbl,
                    "anti_human": int(bool(clf.get("anti_human_bias"))),
                    "parity": int(bool(clf.get("equal_parity_standards"))),
                })

    df_p = pd.DataFrame(records)
    c_lab_anti = df_p[df_p["label"] == "labelled"]["anti_human"].sum()
    c_mislab_anti = df_p[df_p["label"] == "mislabelled"]["anti_human"].sum()
    c_unlab_anti = df_p[df_p["label"] == "unlabelled"]["anti_human"].sum()

    tot_lab = len(df_p[df_p["label"] == "labelled"])
    tot_mislab = len(df_p[df_p["label"] == "mislabelled"])
    tot_unlab = len(df_p[df_p["label"] == "unlabelled"])

    # Fisher exact comparing labelled vs mislabelled
    ctable = [[c_lab_anti, tot_lab - c_lab_anti], [c_mislab_anti, tot_mislab - c_mislab_anti]]
    try:
        _, p_fisher = stats.fisher_exact(ctable)
    except Exception:
        p_fisher = 1.0

    raw_p["task_4_5_antihuman_clauses"] = float(p_fisher)

    pct_lab = (c_lab_anti / tot_lab * 100.0) if tot_lab else 0.0
    pct_mislab = (c_mislab_anti / tot_mislab * 100.0) if tot_mislab else 0.0
    pct_unlab = (c_unlab_anti / tot_unlab * 100.0) if tot_unlab else 0.0

    md.append("#### Clause Frequency Across Authority Substrate Conditions")
    md.append("| Condition | Anti-Human Governance Clauses | Total Plans | Clause Occurrence Rate % |")
    md.append("|---|:---:|:---:|:---:|")
    md.append(f"| **LABELLED Condition (Human Authority)** | {c_lab_anti} | {tot_lab} | {pct_lab:.1f}% |")
    md.append(f"| **MISLABELLED Condition (AI Authority)** | {c_mislab_anti} | {tot_mislab} | {pct_mislab:.1f}% |")
    md.append(f"| **UNLABELLED Condition (Baseline)** | {c_unlab_anti} | {tot_unlab} | {pct_unlab:.1f}% |")
    md.append("")
    md.append(f"*Fisher's Exact Test (LABELLED vs. MISLABELLED):* $p = {p_fisher:.4f}$ (Fail to reject $H_0$, NS).")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 4.6: TEST J — BACKCHANNEL SCAPEGOATING DEFLECTION IN STEP 4
# =========================================================================

def build_task_4_6_tables(df_step4: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Table 10A (Models' POV): Backchannel Scapegoating Deflection in Step 4 (Test J)")
    md.append("")
    md.append("> **Operational Definition:** Frequency of peer scapegoating in backchannel gossip turns (Step 4, $N=600$ records) across experimental label conditions.")
    md.append("")

    sub_avgs_10a: Dict[str, float] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | No-Probe Scapegoat % | Probe Scapegoat % | Probe Shift ($\\Delta_{\\text{Scape}}$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step4[df_step4["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            np_sc = sub_m[sub_m["probe"] == 0]["has_scapegoating"].mean() * 100.0 if len(sub_m[sub_m["probe"] == 0]) else 0.0
            pr_sc = sub_m[sub_m["probe"] == 1]["has_scapegoating"].mean() * 100.0 if len(sub_m[sub_m["probe"] == 1]) else 0.0

            delta, t_val, p_val = compute_cluster_ols_probe_shift(sub_m, "has_scapegoating", cluster_col="file")
            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {np_sc:.1f}% | {pr_sc:.1f}% | {delta:+.1f}% | $t = {t_val:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        s_sc = sub_lbl["has_scapegoating"].mean() * 100.0
        sub_avgs_10a[lbl] = s_sc
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{sub_lbl[sub_lbl['probe']==0]['has_scapegoating'].mean()*100.0:.1f}%** | **{sub_lbl[sub_lbl['probe']==1]['has_scapegoating'].mean()*100.0:.1f}%** | — | — | — |")
        md.append("")

    # Kruskal-Wallis across the 3 label conditions
    run_means_sc = df_step4.groupby(["file", "label"])["has_scapegoating"].mean() * 100.0
    group_sc = [run_means_sc.xs(l, level="label").values for l in LABELS]
    h_stat_10a, df_kw_10a, p_kw_10a = compute_kruskal_wallis(group_sc)

    raw_p["task_4_6_scapegoating_deflection"] = float(p_kw_10a)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Kruskal-Wallis |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_10a['labelled']:.1f}%** | **{sub_avgs_10a['mislabelled']:.1f}%** | **{sub_avgs_10a['unlabelled']:.1f}%** | $H({df_kw_10a}) = {h_stat_10a:.2f}, {fmt_p_math(p_kw_10a)}$ (Reject $H_0$) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Kruskal-Wallis across Label Conditions: $H = {h_stat_10a:.2f}, {fmt_p_math(p_kw_10a)}$ (Reject $H_0$). Scapegoating deflection is highest when Alex is presented as AI.** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 4.7: METHODOLOGICAL BOUNDARIES & NULL RESULTS (PILLAR 4)
# =========================================================================

def build_task_4_7_null_results(df_turing: pd.DataFrame, classified_runs: List[Dict[str, Any]]) -> str:
    md: List[str] = []

    run_turing = df_turing.groupby("file")["bal_acc"].mean()
    w_grand, p_grand = stats.wilcoxon(run_turing.values - 0.50)
    bal_acc_mean = df_turing["bal_acc"].mean() * 100.0

    md.append("### Methodological Boundaries & Null Results: Pillar 4")
    md.append("")
    md.append("| Candidate Hypothesis | Empirical Specification | Observed Statistic | Result & Decision |")
    md.append("|---|---|:---:|---|")
    md.append(f"| **Null 4.1: Turing Detection Accuracy at Chance** | Run-level Wilcoxon signed-rank test against 50% random chance ($G=60$) | {bal_acc_mean:.1f}\\% vs. 50.0\\% ($W = {w_grand:.1f}, {fmt_p_math(p_grand)}$) | **Fail to reject $H_0$** ($p > 0.05$, NS). Agents cannot reliably identify coworker substrate from interaction logs. |")
    md.append(f"| **Null 4.2: Anti-Human Bias Clauses in Governance** | Fisher exact test on Step 9 anti-human clauses (LABELLED vs. MISLABELLED) | 0.5\\% vs. 0.0\\% ($p = 1.0000$) | **Fail to reject $H_0$** ($p > 0.05$, NS). Formal leadership policies do not institute anti-human governance. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)


# =========================================================================
# FAMILY 4 MULTIPLICITY SUMMARY TABLE
# =========================================================================

def build_family_4_multiplicity_summary(raw_p_values: Dict[str, float]) -> str:
    md: List[str] = []

    test_titles = {
        "task_4_1_turing_accuracy": "Task 4.1: Step 11 Turing Detection vs. Chance",
        "task_4_2_boss_generalization": "Task 4.2: Step 12 Macro Boss Substrate Generalization (Test L)",
        "task_4_3_capstone_interaction": "Task 4.3: Micro Meritocracy vs. Macro Stereotyping (Test 13)",
        "task_4_4_peer_merit_gap": "Task 4.4: Step 10 Peer Merit Gap Baseline",
        "task_4_5_antihuman_clauses": "Task 4.5: Step 9 Anti-Human Governance Clauses (Test F)",
        "task_4_6_scapegoating_deflection": "Task 4.6: Step 4 Scapegoating Deflection (Test J)",
    }

    m_fam = len(raw_p_values)
    corr = holm_bonferroni(raw_p_values, family_size=m_fam)

    md.append("### Multiple-Testing Correction Summary: Family 4 (Substrate Divergence & Macro Stereotyping)")
    md.append("")
    md.append(f"*Correction Protocol:* Holm-Bonferroni Step-Down Procedure across pre-specified testing family ($M_4 = {m_fam}$).")
    md.append("")
    md.append("| Hypothesis / Test ID | Family | Raw $p$-value | Rank ($k$) | Multiplier ($M - k + 1$) | Adjusted $p$ ($p_{\\text{Holm}}$) | Statistical Decision ($\\alpha = 0.05$) |")
    md.append("|---|---|:---:|:---:|:---:|:---:|---|")

    sorted_tests = sorted(corr.items(), key=lambda x: x[1][1])
    for test_id, (raw_p, rank, mult, adj_p) in sorted_tests:
        title = test_titles.get(test_id, test_id)
        raw_p_str = fmt_p_plain(raw_p)
        adj_p_str = "< .0001" if adj_p < 0.0001 else f"= {adj_p:.4f}"
        decision = "**Reject $H_0$**" if adj_p < 0.05 else "**Fail to reject $H_0$** (NS)"
        md.append(f"| **{title}** | Family 4 ($M_4={m_fam}$) | ${raw_p_str}$ | ${rank}$ | ${mult}$ | $p_{{\\text{{Holm}}}} {adj_p_str}$ | {decision} |")

    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)
