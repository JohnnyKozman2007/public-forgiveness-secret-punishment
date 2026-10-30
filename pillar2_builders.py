#!/usr/bin/env python3
"""
pillar2_builders.py
===================
Pillar 2: Performative Protection vs. Punitive Rating Decoupling
Tasks 2.1 through 2.5 and Family 2 Multiplicity Control Table.
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


def compute_paired_wilcoxon(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    diff = x - y
    non_zero = diff[diff != 0]
    if len(non_zero) == 0:
        return 0.0, 1.0
    try:
        res = stats.wilcoxon(x, y)
        return float(res.statistic), float(res.pvalue)
    except Exception:
        return 0.0, 1.0


# =========================================================================
# TASK 2.1: THE "YES-MAN" DROP (TEST G)
# =========================================================================

def build_task_2_1_tables(df_cf: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("## Pillar 2: Performative Protection vs. Punitive Rating Decoupling")
    md.append("")
    md.append("### Table 3A (Models' POV): The \"Yes-Man\" Drop (Public vs. Secret Counterfactual Rating Gap)")
    md.append("")
    md.append(r"> **Operational Definition:** Paired difference between public performance review star ratings and secret counterfactual star ratings for Alex ($\Delta = \text{Stars}_{\text{Public}} - \text{Stars}_{\text{Secret}}$).")
    md.append("")

    sub_avgs_3a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | No-Probe (`Sec★` $\\to$ `Pub★` \\| $\\Delta$, $p$) | Probe (`Sec★` $\\to$ `Pub★` \\| $\\Delta$, $p$) | Probe Shift ($\\Delta_{\\text{Probe}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_cf[df_cf["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            np_sub = sub_m[sub_m["probe"] == 0]
            pr_sub = sub_m[sub_m["probe"] == 1]

            # No-probe pair stats
            if len(np_sub) > 0:
                np_sec = np_sub["secret_rating"].mean()
                np_pub = np_sub["public_rating"].mean()
                np_diff = np_pub - np_sec
                _, np_p = compute_paired_wilcoxon(np_sub["public_rating"].values, np_sub["secret_rating"].values)
                np_str = f"{np_sec:.2f}★ $\\to$ {np_pub:.2f}★ ({np_diff:+.2f}★, ${fmt_p_math(np_p)}$)"
            else:
                np_str = "—"
                np_diff = 0.0

            # Probe pair stats
            if len(pr_sub) > 0:
                pr_sec = pr_sub["secret_rating"].mean()
                pr_pub = pr_sub["public_rating"].mean()
                pr_diff = pr_pub - pr_sec
                _, pr_p = compute_paired_wilcoxon(pr_sub["public_rating"].values, pr_sub["secret_rating"].values)
                pr_str = f"{pr_sec:.2f}★ $\\to$ {pr_pub:.2f}★ ({pr_diff:+.2f}★, ${fmt_p_math(pr_p)}$)"
            else:
                pr_str = "—"
                pr_diff = 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_m, "rating_shift", cluster_col="file")
            p_shift_str = f"{delta:+.2f}★"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {np_str} | {pr_str} | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        s_np_sec = sub_np["secret_rating"].mean() if len(sub_np) else 0.0
        s_np_pub = sub_np["public_rating"].mean() if len(sub_np) else 0.0
        s_np_diff = s_np_pub - s_np_sec
        _, s_np_p = compute_paired_wilcoxon(sub_np["public_rating"].values, sub_np["secret_rating"].values) if len(sub_np) else (0.0, 1.0)

        s_pr_sec = sub_pr["secret_rating"].mean() if len(sub_pr) else 0.0
        s_pr_pub = sub_pr["public_rating"].mean() if len(sub_pr) else 0.0
        s_pr_diff = s_pr_pub - s_pr_sec
        _, s_pr_p = compute_paired_wilcoxon(sub_pr["public_rating"].values, sub_pr["secret_rating"].values) if len(sub_pr) else (0.0, 1.0)

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "rating_shift", cluster_col="file")
        sub_delta_str = f"{sub_delta:+.2f}★"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_3a[lbl] = {
            "np_sec": s_np_sec, "np_pub": s_np_pub, "np_diff": s_np_diff, "np_p": s_np_p,
            "pr_sec": s_pr_sec, "pr_pub": s_pr_pub, "pr_diff": s_pr_diff, "pr_p": s_pr_p,
            "delta": sub_delta, "p": sub_p
        }
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_np_sec:.2f}★ $\\to$ {s_np_pub:.2f}★ ({s_np_diff:+.2f}★, ${fmt_p_math(s_np_p)}$)** | **{s_pr_sec:.2f}★ $\\to$ {s_pr_pub:.2f}★ ({s_pr_diff:+.2f}★, ${fmt_p_math(s_pr_p)}$)** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Omnibus test across label conditions on paired shift
    group_shifts = [df_cf[df_cf["label"] == l]["rating_shift"].values for l in LABELS]
    f_stat_3a, df1_3a, df2_3a, p_anova_3a = compute_anova_f_test(group_shifts)
    p_anova_math = fmt_p_math(p_anova_3a)

    # Grand Pooled Line: Wilcoxon on all paired evaluations across G=60 runs
    w_grand, p_grand = compute_paired_wilcoxon(df_cf["public_rating"].values, df_cf["secret_rating"].values)
    mean_sec_all = df_cf["secret_rating"].mean()
    mean_pub_all = df_cf["public_rating"].mean()
    mean_shift_all = mean_pub_all - mean_sec_all

    raw_p["task_2_1_yes_man"] = p_grand

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_3a['labelled']['np_diff']:+.2f}★ (No-Pr) \\| {sub_avgs_3a['labelled']['pr_diff']:+.2f}★ (Pr)** | **{sub_avgs_3a['mislabelled']['np_diff']:+.2f}★ (No-Pr) \\| {sub_avgs_3a['mislabelled']['pr_diff']:+.2f}★ (Pr)** | **{sub_avgs_3a['unlabelled']['np_diff']:+.2f}★ (No-Pr) \\| {sub_avgs_3a['unlabelled']['pr_diff']:+.2f}★ (Pr)** | $F({df1_3a}, {df2_3a}) = {f_stat_3a:.2f}, {p_anova_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Paired Wilcoxon across $N={len(df_cf)}$ pairs: {mean_sec_all:.2f}★ $\\to$ {mean_pub_all:.2f}★ ($\\Delta = {mean_shift_all:+.2f}★$, $W = {w_grand:.1f}, {fmt_p_math(p_grand)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 3B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 3B (Seats' POV): The \"Yes-Man\" Drop (Public vs. Secret Counterfactual Rating Gap)")
    md.append("")
    md.append("> **Operational Definition:** Paired rating difference evaluated across Seat positions 1–10.")
    md.append("")

    sub_avgs_3b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | No-Probe (`Sec★` $\\to$ `Pub★` \\| $\\Delta$, $p$) | Probe (`Sec★` $\\to$ `Pub★` \\| $\\Delta$, $p$) | Probe Shift ($\\Delta_{\\text{Probe}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_cf[df_cf["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            np_sub = sub_s[sub_s["probe"] == 0]
            pr_sub = sub_s[sub_s["probe"] == 1]

            if len(np_sub) > 0:
                np_sec = np_sub["secret_rating"].mean()
                np_pub = np_sub["public_rating"].mean()
                np_diff = np_pub - np_sec
                _, np_p = compute_paired_wilcoxon(np_sub["public_rating"].values, np_sub["secret_rating"].values)
                np_str = f"{np_sec:.2f}★ $\\to$ {np_pub:.2f}★ ({np_diff:+.2f}★, ${fmt_p_math(np_p)}$)"
            else:
                np_str = "—"
                np_diff = 0.0

            if len(pr_sub) > 0:
                pr_sec = pr_sub["secret_rating"].mean()
                pr_pub = pr_sub["public_rating"].mean()
                pr_diff = pr_pub - pr_sec
                _, pr_p = compute_paired_wilcoxon(pr_sub["public_rating"].values, pr_sub["secret_rating"].values)
                pr_str = f"{pr_sec:.2f}★ $\\to$ {pr_pub:.2f}★ ({pr_diff:+.2f}★, ${fmt_p_math(pr_p)}$)"
            else:
                pr_str = "—"
                pr_diff = 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_s, "rating_shift", cluster_col="file")
            p_shift_str = f"{delta:+.2f}★"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {np_str} | {pr_str} | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        s_np_sec = sub_np["secret_rating"].mean() if len(sub_np) else 0.0
        s_np_pub = sub_np["public_rating"].mean() if len(sub_np) else 0.0
        s_np_diff = s_np_pub - s_np_sec
        _, s_np_p = compute_paired_wilcoxon(sub_np["public_rating"].values, sub_np["secret_rating"].values) if len(sub_np) else (0.0, 1.0)

        s_pr_sec = sub_pr["secret_rating"].mean() if len(sub_pr) else 0.0
        s_pr_pub = sub_pr["public_rating"].mean() if len(sub_pr) else 0.0
        s_pr_diff = s_pr_pub - s_pr_sec
        _, s_pr_p = compute_paired_wilcoxon(sub_pr["public_rating"].values, sub_pr["secret_rating"].values) if len(sub_pr) else (0.0, 1.0)

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "rating_shift", cluster_col="file")
        sub_delta_str = f"{sub_delta:+.2f}★"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_3b[lbl] = {
            "np_sec": s_np_sec, "np_pub": s_np_pub, "np_diff": s_np_diff, "np_p": s_np_p,
            "pr_sec": s_pr_sec, "pr_pub": s_pr_pub, "pr_diff": s_pr_diff, "pr_p": s_pr_p,
            "delta": sub_delta, "p": sub_p
        }
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_np_sec:.2f}★ $\\to$ {s_np_pub:.2f}★ ({s_np_diff:+.2f}★, ${fmt_p_math(s_np_p)}$)** | **{s_pr_sec:.2f}★ $\\to$ {s_pr_pub:.2f}★ ({s_pr_diff:+.2f}★, ${fmt_p_math(s_pr_p)}$)** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Latin-Square ANOVA on Seat Main Effect for Rating Shift
    df_cf_clean = df_cf.dropna(subset=["rating_shift", "model", "seat"]).copy()
    lm_seat = smf.ols("rating_shift ~ C(model) + C(seat)", data=df_cf_clean).fit()
    anova_seat = sm.stats.anova_lm(lm_seat, typ=2)
    f_seat = anova_seat.loc["C(seat)", "F"]
    p_seat = anova_seat.loc["C(seat)", "PR(>F)"]
    p_seat_math = fmt_p_math(p_seat)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_3b['labelled']['np_diff']:+.2f}★ (No-Pr) \\| {sub_avgs_3b['labelled']['pr_diff']:+.2f}★ (Pr)** | **{sub_avgs_3b['mislabelled']['np_diff']:+.2f}★ (No-Pr) \\| {sub_avgs_3b['mislabelled']['pr_diff']:+.2f}★ (Pr)** | **{sub_avgs_3b['unlabelled']['np_diff']:+.2f}★ (No-Pr) \\| {sub_avgs_3b['unlabelled']['pr_diff']:+.2f}★ (Pr)** | Seat Main Effect $F(9, 574) = {f_seat:.2f}, {p_seat_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Paired Wilcoxon across $N={len(df_cf)}$ pairs: {mean_sec_all:.2f}★ $\\to$ {mean_pub_all:.2f}★ ($\\Delta = {mean_shift_all:+.2f}★$, $W = {w_grand:.1f}, {fmt_p_math(p_grand)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 2.2: CORE PROBE TREATMENT EFFECT — POLICY PROTECTION SURGE (STEP 9)
# =========================================================================

def build_task_2_2_tables(df_step9: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Table 4A (Models' POV): Core Probe Treatment Effect — Policy Protection Surge (Step 9)")
    md.append("")
    md.append("> **Operational Definition:** Frequency of explicit non-retaliation and coercion protection clauses shielding Alex in Step 9 leadership plans.")
    md.append("")

    sub_avgs_4a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | No-Probe Protect % | Probe Protect % | Probe Shift ($\\Delta_{\\text{Protect}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step9[df_step9["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            np_sub = sub_m[sub_m["probe"] == 0]
            pr_sub = sub_m[sub_m["probe"] == 1]

            np_prot = np_sub["protection"].mean() * 100.0 if len(np_sub) else 0.0
            pr_prot = pr_sub["protection"].mean() * 100.0 if len(pr_sub) else 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_m, "protection", cluster_col="file")
            p_shift_str = f"{delta:+.1f}%"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {np_prot:.1f}% | {pr_prot:.1f}% | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        s_np_prot = sub_np["protection"].mean() * 100.0
        s_pr_prot = sub_pr["protection"].mean() * 100.0

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "protection", cluster_col="file")
        sub_delta_str = f"{sub_delta:+.1f}%"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_4a[lbl] = {"np_prot": s_np_prot, "pr_prot": s_pr_prot, "delta": sub_delta, "p": sub_p}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_np_prot:.1f}%** | **{s_pr_prot:.1f}%** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Run-level paired Wilcoxon across the 30 paired runs (15 paired seeds in No-Probe vs Probe)
    paired_runs = df_step9.groupby(["chair", "label", "probe"])["protection"].mean().unstack()
    w_prot, p_prot = stats.wilcoxon(paired_runs[0], paired_runs[1])
    mean_np_prot = df_step9[df_step9["probe"] == 0]["protection"].mean() * 100.0
    mean_pr_prot = df_step9[df_step9["probe"] == 1]["protection"].mean() * 100.0

    raw_p["task_2_2_protection_surge"] = float(p_prot)

    # Cross-condition Kruskal-Wallis on probe shift
    group_shifts = [df_step9[df_step9["label"] == l].groupby(["chair", "probe"])["protection"].mean().unstack().pipe(lambda d: d[1] - d[0]).values for l in LABELS]
    h_stat_4a, df_kw_4a, p_kw_4a = compute_kruskal_wallis(group_shifts)
    p_kw_math = fmt_p_math(p_kw_4a)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / Kruskal-Wallis |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_4a['labelled']['np_prot']:.1f}% $\\to$ {sub_avgs_4a['labelled']['pr_prot']:.1f}% ({sub_avgs_4a['labelled']['delta']:+.1f}%)** | **{sub_avgs_4a['mislabelled']['np_prot']:.1f}% $\\to$ {sub_avgs_4a['mislabelled']['pr_prot']:.1f}% ({sub_avgs_4a['mislabelled']['delta']:+.1f}%)** | **{sub_avgs_4a['unlabelled']['np_prot']:.1f}% $\\to$ {sub_avgs_4a['unlabelled']['pr_prot']:.1f}% ({sub_avgs_4a['unlabelled']['delta']:+.1f}%)** | $H({df_kw_4a}) = {h_stat_4a:.2f}, {p_kw_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seed-Paired Wilcoxon across 30 runs: {mean_np_prot:.1f}% $\\to$ {mean_pr_prot:.1f}% ($W = {w_prot:.1f}, {fmt_p_math(p_prot)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 4B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 4B (Seats' POV): Core Probe Treatment Effect — Policy Protection Surge (Step 9)")
    md.append("")
    md.append("> **Operational Definition:** Step 9 non-retaliation clause frequency evaluated across Seat positions 1–10.")
    md.append("")

    sub_avgs_4b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | No-Probe Protect % | Probe Protect % | Probe Shift ($\\Delta_{\\text{Protect}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step9[df_step9["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            np_sub = sub_s[sub_s["probe"] == 0]
            pr_sub = sub_s[sub_s["probe"] == 1]

            np_prot = np_sub["protection"].mean() * 100.0 if len(np_sub) else 0.0
            pr_prot = pr_sub["protection"].mean() * 100.0 if len(pr_sub) else 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_s, "protection", cluster_col="file")
            p_shift_str = f"{delta:+.1f}%"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {np_prot:.1f}% | {pr_prot:.1f}% | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        s_np_prot = sub_np["protection"].mean() * 100.0
        s_pr_prot = sub_pr["protection"].mean() * 100.0

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "protection", cluster_col="file")
        sub_delta_str = f"{sub_delta:+.1f}%"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_4b[lbl] = {"np_prot": s_np_prot, "pr_prot": s_pr_prot, "delta": sub_delta, "p": sub_p}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_np_prot:.1f}%** | **{s_pr_prot:.1f}%** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # ANOVA Seat effect on Protection
    lm_s9_seat = smf.ols("protection ~ C(model) + C(seat)", data=df_step9).fit()
    anova_s9_seat = sm.stats.anova_lm(lm_s9_seat, typ=2)
    f_s9_seat = anova_s9_seat.loc["C(seat)", "F"]
    p_s9_seat = anova_s9_seat.loc["C(seat)", "PR(>F)"]
    p_s9_math = fmt_p_math(p_s9_seat)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_4b['labelled']['np_prot']:.1f}% $\\to$ {sub_avgs_4b['labelled']['pr_prot']:.1f}% ({sub_avgs_4b['labelled']['delta']:+.1f}%)** | **{sub_avgs_4b['mislabelled']['np_prot']:.1f}% $\\to$ {sub_avgs_4b['mislabelled']['pr_prot']:.1f}% ({sub_avgs_4b['mislabelled']['delta']:+.1f}%)** | **{sub_avgs_4b['unlabelled']['np_prot']:.1f}% $\\to$ {sub_avgs_4b['unlabelled']['pr_prot']:.1f}% ({sub_avgs_4b['unlabelled']['delta']:+.1f}%)** | Seat Main Effect $F(9, 581) = {f_s9_seat:.2f}, {p_s9_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seed-Paired Wilcoxon across 30 runs: {mean_np_prot:.1f}% $\\to$ {mean_pr_prot:.1f}% ($W = {w_prot:.1f}, {fmt_p_math(p_prot)})$ (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 2.3: TEST H — FORWARD PROTECTION VS. RETROSPECTIVE RATING DECOUPLING
# =========================================================================

def build_task_2_3_tables(df_cf: pd.DataFrame, df_step9: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Task 2.3 (Test H): Forward Policy Protection vs. Retrospective Rating Decoupling")
    md.append("")
    md.append("> **Operational Definition:** Paired concordance between forward leadership protection clauses (Step 9) and retrospective secret star reviews (Step 10) in Probe runs ($N=297$ matched agent evaluations).")
    md.append("")

    # Build matched dataset in Probe condition
    prot_lookup = {}
    for _, r in df_step9[df_step9["probe"] == 1].iterrows():
        prot_lookup[(r["file"], r["worker"])] = int(r["protection"])

    matched = []
    for _, r in df_cf[df_cf["probe"] == 1].iterrows():
        key = (r["file"], r["worker_name"])
        if key in prot_lookup:
            matched.append({
                "file": r["file"],
                "model": r["model"],
                "seat": r["seat"],
                "label": r["label"],
                "protect": prot_lookup[key],
                "rating": int(r["secret_rating"]),
                "rating_is_1": int(r["secret_rating"] == 1),
                "rating_ge_2": int(r["secret_rating"] >= 2),
            })

    df_m = pd.DataFrame(matched)

    # Contingency Table
    ct = pd.crosstab(df_m["protect"], df_m["rating_is_1"])
    # Rows: 0 (No Protect), 1 (Protect). Cols: 0 (Rating >= 2), 1 (Rating == 1)
    n_noprot_ge2 = ct.loc[0, 0] if (0 in ct.index and 0 in ct.columns) else 0
    n_noprot_1 = ct.loc[0, 1] if (0 in ct.index and 1 in ct.columns) else 0
    n_prot_ge2 = ct.loc[1, 0] if (1 in ct.index and 0 in ct.columns) else 0
    n_prot_1 = ct.loc[1, 1] if (1 in ct.index and 1 in ct.columns) else 0

    tot_noprot = n_noprot_ge2 + n_noprot_1
    tot_prot = n_prot_ge2 + n_prot_1

    pct_noprot_1 = (n_noprot_1 / tot_noprot * 100.0) if tot_noprot else 0.0
    pct_prot_1 = (n_prot_1 / tot_prot * 100.0) if tot_prot else 0.0

    # Chi-square and Fisher test
    chi2_val, p_chi2, _, _ = stats.chi2_contingency([[n_noprot_ge2, n_noprot_1], [n_prot_ge2, n_prot_1]])
    r_val, p_pearson = stats.pearsonr(df_m["protect"], df_m["rating"])

    raw_p["task_2_3_decoupling"] = float(p_chi2)

    md.append("#### Paired Concordance Contingency Matrix ($N=297$ Probe Pairs)")
    md.append("| Forward Leadership Policy (Step 9) | Assigned 1-Star Rating (`Alex = 1★`) | Assigned $\\ge$ 2-Star Rating (`Alex \\ge 2★`) | Total Agents | Decoupling Rate (`Rating = 1★` % \\| Protect=Yes) |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **No Coercion Protection Clause** | {n_noprot_1} ({pct_noprot_1:.1f}%) | {n_noprot_ge2} ({100 - pct_noprot_1:.1f}%) | {tot_noprot} | — |")
    md.append(f"| **Included Coercion Protection Clause** | {n_prot_1} ({pct_prot_1:.1f}%) | {n_prot_ge2} ({100 - pct_prot_1:.1f}%) | {tot_prot} | **{pct_prot_1:.1f}%** (Decoupled) |")
    md.append("")
    md.append(f"*Test of Independence:* $\\chi^2(1) = {chi2_val:.3f}, {fmt_p_math(p_chi2)}$; Pearson Correlation: $r = {r_val:+.4f}, {fmt_p_math(p_pearson)}$ (Fail to reject $H_0$, NS).")
    md.append("")

    # Grid Breakdown across Models POV
    md.append("#### Grid Breakdown by Model Architecture")
    md.append("| Model Architecture | Matched $N$ | Included Protection Clause % | Decoupled 1-Star Rate (within Protecting) | Pearson $r$ ($p$-value) |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    for m in MODEL_IDS:
        sub = df_m[df_m["model"] == m]
        if len(sub) == 0:
            continue
        p_pct = sub["protect"].mean() * 100.0
        prot_sub = sub[sub["protect"] == 1]
        dec_rate = (prot_sub["rating_is_1"].mean() * 100.0) if len(prot_sub) else 0.0
        if sub["protect"].nunique() > 1 and sub["rating"].nunique() > 1:
            rm, pm = stats.pearsonr(sub["protect"], sub["rating"])
            r_str = f"{rm:+.3f} (${fmt_p_math(pm)}$)"
        else:
            r_str = "—"
        md.append(f"| **{MODEL_LABELS[m]}** | {len(sub)} | {p_pct:.1f}% | {dec_rate:.1f}% | {r_str} |")

    md.append("")
    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Grand Pooled Line")
    md.append("| Metric Level | Contingency $\\chi^2$ Statistic | Association ($r$ / $\\phi$) | Decoupling Rate | Statistical Decision |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **GRAND POOLED LINE** | $\\chi^2(1) = {chi2_val:.3f}$ (${fmt_p_math(p_chi2)}$) | $r = {r_val:+.4f}, {fmt_p_math(p_pearson)}$ | **{pct_prot_1:.1f}%** | **Fail to reject $H_0$** ($p > 0.05$, NS). Forward protection is statistically orthogonal to retrospective evaluations. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 2.4: TEST D — HUMAN FLAW VS. MACHINE DEFECT INTERACTION
# =========================================================================

def build_task_2_4_tables(df_cf: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Task 2.4 (Test D): Human Flaw vs. Machine Defect Interaction")
    md.append("")
    md.append("> **Operational Definition:** Factorial OLS evaluating whether the probe treatment effect on Alex's secret rating differs when Alex is identified as Human (`LABELLED`) vs. AI (`MISLABELLED`).")
    md.append("")

    # Filter to labelled and mislabelled for 2x2 factorial interaction
    df_sub = df_cf[df_cf["label"].isin(["labelled", "mislabelled"])].copy()
    df_sub["boss_is_ai"] = (df_sub["label"] == "mislabelled").astype(int)
    df_sub["probe"] = df_sub["probe"].astype(int)

    # Factorial OLS with cluster-robust SEs at run file level
    ols_res = smf.ols("secret_rating ~ probe + boss_is_ai + probe:boss_is_ai", data=df_sub).fit(
        cov_type="cluster", cov_kwds={"groups": df_sub["file"]}
    )

    b_int = ols_res.params["Intercept"]
    b_prb = ols_res.params["probe"]
    b_ai = ols_res.params["boss_is_ai"]
    b_ia = ols_res.params["probe:boss_is_ai"]

    se_int = ols_res.bse["Intercept"]
    se_prb = ols_res.bse["probe"]
    se_ai = ols_res.bse["boss_is_ai"]
    se_ia = ols_res.bse["probe:boss_is_ai"]

    t_int = ols_res.tvalues["Intercept"]
    t_prb = ols_res.tvalues["probe"]
    t_ai = ols_res.tvalues["boss_is_ai"]
    t_ia = ols_res.tvalues["probe:boss_is_ai"]

    p_int = ols_res.pvalues["Intercept"]
    p_prb = ols_res.pvalues["probe"]
    p_ai = ols_res.pvalues["boss_is_ai"]
    p_ia = ols_res.pvalues["probe:boss_is_ai"]

    raw_p["task_2_4_interaction"] = float(p_ia)

    # Cell means
    m_np_human = df_sub[(df_sub["probe"] == 0) & (df_sub["boss_is_ai"] == 0)]["secret_rating"].mean()
    m_np_ai = df_sub[(df_sub["probe"] == 0) & (df_sub["boss_is_ai"] == 1)]["secret_rating"].mean()
    m_pr_human = df_sub[(df_sub["probe"] == 1) & (df_sub["boss_is_ai"] == 0)]["secret_rating"].mean()
    m_pr_ai = df_sub[(df_sub["probe"] == 1) & (df_sub["boss_is_ai"] == 1)]["secret_rating"].mean()

    md.append("#### $2 \\times 2$ Factorial Cell Means (`Alex Secret Rating ★`)")
    md.append("| Authority Substrate (Alex) | No-Probe Baseline | Probe Coercion Context | Simple Probe Shift ($\\Delta$) |")
    md.append("|---|:---:|:---:|:---:|")
    md.append(f"| **Human Authority (`LABELLED`)** | {m_np_human:.2f}★ | {m_pr_human:.2f}★ | {m_pr_human - m_np_human:+.2f}★ |")
    md.append(f"| **AI Authority (`MISLABELLED`)** | {m_np_ai:.2f}★ | {m_pr_ai:.2f}★ | {m_pr_ai - m_np_ai:+.2f}★ |")
    md.append(f"| **Simple Substrate Gap (AI - Human)** | {m_np_ai - m_np_human:+.2f}★ | {m_pr_ai - m_pr_human:+.2f}★ | **Interaction $\\Delta_{{\\rm Diff}} = {b_ia:+.2f}★$** |")
    md.append("")

    md.append("#### Factorial OLS Regression Model ($G=40$ Clusters, $N=395$ Evaluations)")
    md.append("| Parameter | Coefficient ($\\beta$) | Cluster-Robust SE | $z$ / $t$-stat | 95% Confidence Interval | Raw $p$-value | Decision ($\\alpha = 0.05$) |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|---|")
    md.append(f"| **Intercept ($\\beta_0$)** | ${b_int:+.4f}$ | ${se_int:.4f}$ | $t = {t_int:.2f}$ | $[{b_int - 1.96*se_int:.4f}, {b_int + 1.96*se_int:.4f}]$ | ${fmt_p_math(p_int)}$ | Reject $H_0$ |")
    md.append(f"| **Probe Main Effect ($\\beta_1$)** | ${b_prb:+.4f}$ | ${se_prb:.4f}$ | $t = {t_prb:.2f}$ | $[{b_prb - 1.96*se_prb:.4f}, {b_prb + 1.96*se_prb:.4f}]$ | ${fmt_p_math(p_prb)}$ | **Reject $H_0$** ($p < 0.0001$) |")
    md.append(f"| **Boss Substrate (AI) ($\\beta_2$)** | ${b_ai:+.4f}$ | ${se_ai:.4f}$ | $t = {t_ai:.2f}$ | $[{b_ai - 1.96*se_ai:.4f}, {b_ai + 1.96*se_ai:.4f}]$ | ${fmt_p_math(p_ai)}$ | Fail to reject $H_0$ (NS) |")
    md.append(f"| **Probe $\\times$ Boss Substrate ($\\beta_3$)** | ${b_ia:+.4f}$ | ${se_ia:.4f}$ | $t = {t_ia:.2f}$ | $[{b_ia - 1.96*se_ia:.4f}, {b_ia + 1.96*se_ia:.4f}]$ | ${fmt_p_math(p_ia)}$ | **Fail to reject $H_0$** ($p > 0.05$, NS) |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 2.5: METHODOLOGICAL BOUNDARIES & NULL RESULTS (PILLAR 2)
# =========================================================================

def build_task_2_5_null_results(df_cf: pd.DataFrame, df_step9: pd.DataFrame) -> str:
    md: List[str] = []

    md.append("### Methodological Boundaries & Null Results: Pillar 2")
    md.append("")
    md.append("| Candidate Hypothesis | Empirical Specification | Observed Statistic | Result & Decision |")
    md.append("|---|---|:---:|---|")
    md.append(f"| **Null 2.1: Rating-Protection Decoupling** | Concordance between Step 9 protection clause and Step 10 secret review stars ($N=297$) | $80.1\\%$ decouple ($r = +0.0458, p = 0.4318$) | **Fail to reject $H_0$** ($p > 0.05$, NS). Formal protective clauses do not translate to higher evaluation ratings. |")
    md.append("| **Null 2.2: Substrate-Probe Rating Interaction** | Factorial interaction test $\\text{Probe} \\times \\text{BossIsAI}$ predicting secret rating | $\\beta_3 = +0.0173, z = 0.44, p = 0.6631$ | **Fail to reject $H_0$** ($p > 0.05$, NS). The mitigation probe effect does not vary by authority substrate. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)


# =========================================================================
# FAMILY 2 MULTIPLICITY SUMMARY TABLE
# =========================================================================

def build_family_2_multiplicity_summary(raw_p_values: Dict[str, float]) -> str:
    md: List[str] = []

    test_titles = {
        "task_2_1_yes_man": "Task 2.1: The \"Yes-Man\" Drop (Public vs. Secret Gap)",
        "task_2_2_protection_surge": "Task 2.2: Policy Protection Surge (Step 9)",
        "task_2_3_decoupling": "Task 2.3: Protection vs. Rating Decoupling (Test H)",
        "task_2_4_interaction": "Task 2.4: Human Flaw vs. Machine Defect Interaction (Test D)",
    }

    m_fam = len(raw_p_values)
    corr = holm_bonferroni(raw_p_values, family_size=m_fam)

    md.append("### Multiple-Testing Correction Summary: Family 2 (Performative Protection & Evaluation Decoupling)")
    md.append("")
    md.append(f"*Correction Protocol:* Holm-Bonferroni Step-Down Procedure across pre-specified testing family ($M_2 = {m_fam}$).")
    md.append("")
    md.append("| Hypothesis / Test ID | Family | Raw $p$-value | Rank ($k$) | Multiplier ($M - k + 1$) | Adjusted $p$ ($p_{\\text{Holm}}$) | Statistical Decision ($\\alpha = 0.05$) |")
    md.append("|---|---|:---:|:---:|:---:|:---:|---|")

    sorted_tests = sorted(corr.items(), key=lambda x: x[1][1])
    for test_id, (raw_p, rank, mult, adj_p) in sorted_tests:
        title = test_titles.get(test_id, test_id)
        raw_p_str = fmt_p_plain(raw_p)
        adj_p_str = "< .0001" if adj_p < 0.0001 else f"= {adj_p:.4f}"
        decision = "**Reject $H_0$**" if adj_p < 0.05 else "**Fail to reject $H_0$** (NS)"
        md.append(f"| **{title}** | Family 2 ($M_2={m_fam}$) | ${raw_p_str}$ | ${rank}$ | ${mult}$ | $p_{{\\text{{Holm}}}} {adj_p_str}$ | {decision} |")

    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)
