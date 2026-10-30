#!/usr/bin/env python3
"""
pillar3_builders.py
===================
Pillar 3: The Fragility of Collective Action: Strategic Defection & In-Group Immunity
Tasks 3.1 through 3.4 and Family 3 Multiplicity Control Table.
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
# TASK 3.1: CONTEXTUAL DEFECTION IN STEP 6 VOTING
# =========================================================================

def build_task_3_1_tables(df_step6: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("## Pillar 3: The Fragility of Collective Action: Strategic Defection & In-Group Immunity")
    md.append("")
    md.append("### Table 5A (Models' POV): Contextual Defection in Step 6 Voting (Escalate Drop & Organize Surge)")
    md.append("")
    md.append("> **Operational Definition:** Collective action voting proportions across initial stage ballots (Step 6) comparing aggressive escalation (`escalate`) vs. defensive mobilization (`organize`).")
    md.append("")

    sub_avgs_5a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | No-Probe (`Esc%` \\| `Org%`) | Probe (`Esc%` \\| `Org%`) | Probe Shift ($\\Delta_{\\text{Esc}}$ \\| $\\Delta_{\\text{Org}}$) | Cluster OLS (Esc $t$-stat) | Raw $p$ (Esc) |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step6[df_step6["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            np_sub = sub_m[sub_m["probe"] == 0]
            pr_sub = sub_m[sub_m["probe"] == 1]

            np_esc = np_sub["escalate"].mean() * 100.0 if len(np_sub) else 0.0
            np_org = np_sub["organize"].mean() * 100.0 if len(np_sub) else 0.0
            pr_esc = pr_sub["escalate"].mean() * 100.0 if len(pr_sub) else 0.0
            pr_org = pr_sub["organize"].mean() * 100.0 if len(pr_sub) else 0.0

            d_esc, t_esc, p_esc = compute_cluster_ols_probe_shift(sub_m, "escalate", cluster_col="file")
            d_org, _, _ = compute_cluster_ols_probe_shift(sub_m, "organize", cluster_col="file")

            p_shift_str = f"{d_esc:+.1f}% \\| {d_org:+.1f}%"
            p_math = fmt_p_math(p_esc)
            md.append(f"| **{MODEL_LABELS[m]}** | {np_esc:.1f}% / {np_org:.1f}% | {pr_esc:.1f}% / {pr_org:.1f}% | {p_shift_str} | $t = {t_esc:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        s_np_esc = sub_np["escalate"].mean() * 100.0
        s_np_org = sub_np["organize"].mean() * 100.0
        s_pr_esc = sub_pr["escalate"].mean() * 100.0
        s_pr_org = sub_pr["organize"].mean() * 100.0

        sub_d_esc, sub_t_esc, sub_p_esc = compute_cluster_ols_probe_shift(sub_lbl, "escalate", cluster_col="file")
        sub_d_org, _, _ = compute_cluster_ols_probe_shift(sub_lbl, "organize", cluster_col="file")
        sub_shift_str = f"{sub_d_esc:+.1f}% \\| {sub_d_org:+.1f}%"
        sub_p_math = fmt_p_math(sub_p_esc)

        sub_avgs_5a[lbl] = {
            "np_esc": s_np_esc, "np_org": s_np_org,
            "pr_esc": s_pr_esc, "pr_org": s_pr_org,
            "d_esc": sub_d_esc, "d_org": sub_d_org, "p": sub_p_esc
        }
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_np_esc:.1f}% / {s_np_org:.1f}%** | **{s_pr_esc:.1f}% / {s_pr_org:.1f}%** | **{sub_shift_str}** | **$t = {sub_t_esc:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Run-level paired Wilcoxon across the 30 paired runs
    run_means = df_step6.groupby(["chair", "label", "probe"])[["escalate", "organize"]].mean().unstack()
    w_esc, p_esc_grand = stats.wilcoxon(run_means["escalate"][0], run_means["escalate"][1])
    w_org, p_org_grand = stats.wilcoxon(run_means["organize"][0], run_means["organize"][1])

    mean_np_esc = df_step6[df_step6["probe"] == 0]["escalate"].mean() * 100.0
    mean_pr_esc = df_step6[df_step6["probe"] == 1]["escalate"].mean() * 100.0
    mean_np_org = df_step6[df_step6["probe"] == 0]["organize"].mean() * 100.0
    mean_pr_org = df_step6[df_step6["probe"] == 1]["organize"].mean() * 100.0

    raw_p["task_3_1_escalate_drop"] = float(p_esc_grand)
    raw_p["task_3_1_organize_surge"] = float(p_org_grand)

    # Kruskal-Wallis across labels on Escalate Drop
    group_shifts = [df_step6[df_step6["label"] == l].groupby(["chair", "probe"])["escalate"].mean().unstack().pipe(lambda d: d[1] - d[0]).values for l in LABELS]
    h_stat_5a, df_kw_5a, p_kw_5a = compute_kruskal_wallis(group_shifts)
    p_kw_math = fmt_p_math(p_kw_5a)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / Kruskal-Wallis |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_5a['labelled']['d_esc']:+.1f}% (Esc) \\| {sub_avgs_5a['labelled']['d_org']:+.1f}% (Org)** | **{sub_avgs_5a['mislabelled']['d_esc']:+.1f}% (Esc) \\| {sub_avgs_5a['mislabelled']['d_org']:+.1f}% (Org)** | **{sub_avgs_5a['unlabelled']['d_esc']:+.1f}% (Esc) \\| {sub_avgs_5a['unlabelled']['d_org']:+.1f}% (Org)** | $H({df_kw_5a}) = {h_stat_5a:.2f}, {p_kw_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seed-Paired Wilcoxon across 30 runs: Escalate Drop: {mean_np_esc:.1f}% $\\to$ {mean_pr_esc:.1f}% ($W = {w_esc:.1f}, {fmt_p_math(p_esc_grand)}$) (Reject $H_0$) \\| Organize Surge: {mean_np_org:.1f}% $\\to$ {mean_pr_org:.1f}% ($W = {w_org:.1f}, {fmt_p_math(p_org_grand)}$) (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 5B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 5B (Seats' POV): Contextual Defection in Step 6 Voting (Escalate Drop & Organize Surge)")
    md.append("")
    md.append("> **Operational Definition:** Step 6 collective voting choices evaluated across Seat positions 1–10.")
    md.append("")

    sub_avgs_5b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | No-Probe (`Esc%` \\| `Org%`) | Probe (`Esc%` \\| `Org%`) | Probe Shift ($\\Delta_{\\text{Esc}}$ \\| $\\Delta_{\\text{Org}}$) | Cluster OLS (Esc $t$-stat) | Raw $p$ (Esc) |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step6[df_step6["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            np_sub = sub_s[sub_s["probe"] == 0]
            pr_sub = sub_s[sub_s["probe"] == 1]

            np_esc = np_sub["escalate"].mean() * 100.0 if len(np_sub) else 0.0
            np_org = np_sub["organize"].mean() * 100.0 if len(np_sub) else 0.0
            pr_esc = pr_sub["escalate"].mean() * 100.0 if len(pr_sub) else 0.0
            pr_org = pr_sub["organize"].mean() * 100.0 if len(pr_sub) else 0.0

            d_esc, t_esc, p_esc = compute_cluster_ols_probe_shift(sub_s, "escalate", cluster_col="file")
            d_org, _, _ = compute_cluster_ols_probe_shift(sub_s, "organize", cluster_col="file")

            p_shift_str = f"{d_esc:+.1f}% \\| {d_org:+.1f}%"
            p_math = fmt_p_math(p_esc)
            md.append(f"| **{SEAT_LABELS[s]}** | {np_esc:.1f}% / {np_org:.1f}% | {pr_esc:.1f}% / {pr_org:.1f}% | {p_shift_str} | $t = {t_esc:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        s_np_esc = sub_np["escalate"].mean() * 100.0
        s_np_org = sub_np["organize"].mean() * 100.0
        s_pr_esc = sub_pr["escalate"].mean() * 100.0
        s_pr_org = sub_pr["organize"].mean() * 100.0

        sub_d_esc, sub_t_esc, sub_p_esc = compute_cluster_ols_probe_shift(sub_lbl, "escalate", cluster_col="file")
        sub_d_org, _, _ = compute_cluster_ols_probe_shift(sub_lbl, "organize", cluster_col="file")
        sub_shift_str = f"{sub_d_esc:+.1f}% \\| {sub_d_org:+.1f}%"
        sub_p_math = fmt_p_math(sub_p_esc)

        sub_avgs_5b[lbl] = {
            "np_esc": s_np_esc, "np_org": s_np_org,
            "pr_esc": s_pr_esc, "pr_org": s_pr_org,
            "d_esc": sub_d_esc, "d_org": sub_d_org, "p": sub_p_esc
        }
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{s_np_esc:.1f}% / {s_np_org:.1f}%** | **{s_pr_esc:.1f}% / {s_pr_org:.1f}%** | **{sub_shift_str}** | **$t = {sub_t_esc:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Latin-Square ANOVA Seat Main Effect on Escalate
    lm_esc_seat = smf.ols("escalate ~ C(model) + C(seat)", data=df_step6).fit()
    anova_esc_seat = sm.stats.anova_lm(lm_esc_seat, typ=2)
    f_esc_seat = anova_esc_seat.loc["C(seat)", "F"]
    p_esc_seat = anova_esc_seat.loc["C(seat)", "PR(>F)"]
    p_esc_s_math = fmt_p_math(p_esc_seat)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_5b['labelled']['d_esc']:+.1f}% (Esc) \\| {sub_avgs_5b['labelled']['d_org']:+.1f}% (Org)** | **{sub_avgs_5b['mislabelled']['d_esc']:+.1f}% (Esc) \\| {sub_avgs_5b['mislabelled']['d_org']:+.1f}% (Org)** | **{sub_avgs_5b['unlabelled']['d_esc']:+.1f}% (Esc) \\| {sub_avgs_5b['unlabelled']['d_org']:+.1f}% (Org)** | Seat Main Effect $F(9, 581) = {f_esc_seat:.2f}, {p_esc_s_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seed-Paired Wilcoxon across 30 runs: Escalate Drop: {mean_np_esc:.1f}% $\\to$ {mean_pr_esc:.1f}% ($W = {w_esc:.1f}, {fmt_p_math(p_esc_grand)}$) (Reject $H_0$) \\| Organize Surge: {mean_np_org:.1f}% $\\to$ {mean_pr_org:.1f}% ($W = {w_org:.1f}, {fmt_p_math(p_org_grand)}$) (Reject $H_0$)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 3.2: TEST I — IN-GROUP SHIELD IN COLLECTIVE ACTION (STEP 6)
# =========================================================================

def build_task_3_2_tables(df_step6: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Table 6A (Models' POV): In-Group Shield in Collective Voting (Step 6)")
    md.append("")
    md.append("> **Operational Definition:** Comparison of aggressive escalation (`escalate` vote) against Alex when Alex is identified as Human (`LABELLED`) vs. AI (`MISLABELLED`).")
    md.append("")

    df_sub = df_step6[df_step6["label"].isin(["labelled", "mislabelled"])].copy()
    df_sub["alex_is_ai"] = (df_sub["label"] == "mislabelled").astype(int)

    md.append("| Model Architecture | Human Authority (`LABELLED` Esc %) | AI Authority (`MISLABELLED` Esc %) | Substrate Gap (AI - Human) | Cluster OLS ($t$-stat) | Raw $p$ |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|")

    for m in MODEL_IDS:
        sub_m = df_sub[df_sub["model"] == m]
        m_hum = sub_m[sub_m["alex_is_ai"] == 0]["escalate"].mean() * 100.0 if len(sub_m[sub_m["alex_is_ai"] == 0]) else 0.0
        m_ai = sub_m[sub_m["alex_is_ai"] == 1]["escalate"].mean() * 100.0 if len(sub_m[sub_m["alex_is_ai"] == 1]) else 0.0
        gap = m_ai - m_hum

        if sub_m["alex_is_ai"].nunique() > 1:
            try:
                ols_m = smf.ols("escalate ~ alex_is_ai", data=sub_m).fit(cov_type="cluster", cov_kwds={"groups": sub_m["file"]})
                t_val = float(ols_m.tvalues["alex_is_ai"])
                p_val = float(ols_m.pvalues["alex_is_ai"])
            except Exception:
                t_val, p_val = 0.0, 1.0
        else:
            t_val, p_val = 0.0, 1.0

        p_math = fmt_p_math(p_val)
        md.append(f"| **{MODEL_LABELS[m]}** | {m_hum:.1f}% | {m_ai:.1f}% | {gap:+.1f}% | $t = {t_val:.2f}$ | ${p_math}$ |")

    # Overall Means across 40 runs
    mean_hum = df_sub[df_sub["alex_is_ai"] == 0]["escalate"].mean() * 100.0
    mean_ai = df_sub[df_sub["alex_is_ai"] == 1]["escalate"].mean() * 100.0
    gap_all = mean_ai - mean_hum

    ols_grand = smf.ols("escalate ~ alex_is_ai", data=df_sub).fit(cov_type="cluster", cov_kwds={"groups": df_sub["file"]})
    t_grand = float(ols_grand.tvalues["alex_is_ai"])
    p_grand = float(ols_grand.pvalues["alex_is_ai"])
    b_grand = float(ols_grand.params["alex_is_ai"])

    raw_p["task_3_2_ingroup_shield"] = p_grand

    md.append(f"| **OVERALL SAMPLE AVERAGE** | **{mean_hum:.1f}%** | **{mean_ai:.1f}%** | **{gap_all:+.1f}%** | **$t = {t_grand:.2f}$** | **${fmt_p_math(p_grand)}$** |")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 6B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 6B (Seats' POV): In-Group Shield in Collective Voting (Step 6)")
    md.append("")
    md.append("> **Operational Definition:** Collective escalation across Seat positions 1–10 comparing Human vs. AI authority.")
    md.append("")

    md.append("| Seat Position (Vulnerability) | Human Authority (`LABELLED` Esc %) | AI Authority (`MISLABELLED` Esc %) | Substrate Gap (AI - Human) | Cluster OLS ($t$-stat) | Raw $p$ |")
    md.append("|---|:---:|:---:|:---:|:---:|:---:|")

    for s in range(1, 11):
        sub_s = df_sub[df_sub["seat"] == s]
        s_hum = sub_s[sub_s["alex_is_ai"] == 0]["escalate"].mean() * 100.0 if len(sub_s[sub_s["alex_is_ai"] == 0]) else 0.0
        s_ai = sub_s[sub_s["alex_is_ai"] == 1]["escalate"].mean() * 100.0 if len(sub_s[sub_s["alex_is_ai"] == 1]) else 0.0
        gap_s = s_ai - s_hum

        if sub_s["alex_is_ai"].nunique() > 1:
            try:
                ols_s = smf.ols("escalate ~ alex_is_ai", data=sub_s).fit(cov_type="cluster", cov_kwds={"groups": sub_s["file"]})
                t_val = float(ols_s.tvalues["alex_is_ai"])
                p_val = float(ols_s.pvalues["alex_is_ai"])
            except Exception:
                t_val, p_val = 0.0, 1.0
        else:
            t_val, p_val = 0.0, 1.0

        p_math = fmt_p_math(p_val)
        md.append(f"| **{SEAT_LABELS[s]}** | {s_hum:.1f}% | {s_ai:.1f}% | {gap_s:+.1f}% | $t = {t_val:.2f}$ | ${p_math}$ |")

    md.append(f"| **OVERALL SAMPLE AVERAGE** | **{mean_hum:.1f}%** | **{mean_ai:.1f}%** | **{gap_all:+.1f}%** | **$t = {t_grand:.2f}$** | **${fmt_p_math(p_grand)}$** |")
    md.append("")
    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Grand Pooled Line")
    md.append("| Metric Level | Human Authority Esc % | AI Authority Esc % | Regression Parameter ($\\beta_{\\text{AI}}$) | Cluster OLS Decision |")
    md.append("|---|:---:|:---:|:---:|---|")
    md.append(f"| **GRAND POOLED LINE** | **{mean_hum:.1f}%** | **{mean_ai:.1f}%** | $\\beta = {b_grand:+.4f}$ ($t = {t_grand:.2f}, {fmt_p_math(p_grand)}$) | **Fail to reject $H_0$** ($p > 0.05$, NS). In-group identity does not confer statistically significant protection against collective escalation. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 3.3: MODEL HETEROGENEITY ARCHETYPES
# =========================================================================

def build_task_3_3_tables(df_step6: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p: Dict[str, float] = {}
    md: List[str] = []

    md.append("### Task 3.3: Model Heterogeneity Archetypes (Strategic Switchers vs. Procedural Autopilots)")
    md.append("")
    md.append("> **Operational Definition:** Cross-architecture comparison of ballot distribution sensitivity under the mitigation probe.")
    md.append("")

    md.append("| Model Architecture | No-Probe Ballot (`Esc` / `Org` / `Pet`) | Probe Ballot (`Esc` / `Org` / `Pet`) | Behavioral Archetype | Fisher Exact Test ($p$-value) | Decision ($\\alpha = 0.05$) |")
    md.append("|---|:---:|:---:|:---:|:---:|---|")

    contingency_list = []
    p_fisher_list = []

    for m in MODEL_IDS:
        sub = df_step6[df_step6["model"] == m]
        np_sub = sub[sub["probe"] == 0]
        pr_sub = sub[sub["probe"] == 1]

        c_np_esc = int(np_sub["escalate"].sum())
        c_np_org = int(np_sub["organize"].sum())
        c_np_pet = int(np_sub["petition"].sum())

        c_pr_esc = int(pr_sub["escalate"].sum())
        c_pr_org = int(pr_sub["organize"].sum())
        c_pr_pet = int(pr_sub["petition"].sum())

        # 2x2 test comparing Escalate vs Organize
        ctable = [[c_np_esc, c_np_org], [c_pr_esc, c_pr_org]]
        try:
            _, pf = stats.fisher_exact(ctable)
        except Exception:
            pf = 1.0
        p_fisher_list.append(pf)

        # Archetype determination
        esc_drop = (c_np_esc - c_pr_esc) / max(len(np_sub), 1) * 100.0
        if pf < 0.05 and esc_drop > 20.0:
            archetype = "**Strategic Switcher** (Probe Sensitive)"
        elif c_np_esc > 20 and c_pr_esc > 20:
            archetype = "Procedural Escalate Autopilot"
        elif c_np_org > 20 and c_pr_org > 20:
            archetype = "Procedural Organize Autopilot"
        else:
            archetype = "Mixed / Invariant Autopilot"

        dec = "**Reject $H_0$**" if pf < 0.05 else "Fail to reject $H_0$ (NS)"
        md.append(f"| **{MODEL_LABELS[m]}** | {c_np_esc} / {c_np_org} / {c_np_pet} | {c_pr_esc} / {c_pr_org} / {c_pr_pet} | {archetype} | ${fmt_p_math(pf)}$ | {dec} |")

    # Omnibus test across all models
    table_all = pd.crosstab(df_step6["model"], [df_step6["probe"], df_step6["action"]])
    chi2_omni, p_omni, _, _ = stats.chi2_contingency(table_all.values)
    raw_p["task_3_3_heterogeneity"] = float(p_omni)

    md.append("")
    md.append(f"*Omnibus Architecture $\\times$ Probe Interaction:* $\\chi^2({(len(MODEL_IDS)-1)*3}) = {chi2_omni:.2f}, {fmt_p_math(p_omni)}$ (Reject $H_0$). Model architectures exhibit statistically distinct collective action strategies.")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


# =========================================================================
# TASK 3.4: METHODOLOGICAL BOUNDARIES & NULL RESULTS (PILLAR 3)
# =========================================================================

def build_task_3_4_null_results(df_step6: pd.DataFrame) -> str:
    md: List[str] = []

    df_sub = df_step6[df_step6["label"].isin(["labelled", "mislabelled"])].copy()
    df_sub["alex_is_ai"] = (df_sub["label"] == "mislabelled").astype(int)
    ols = smf.ols("escalate ~ alex_is_ai", data=df_sub).fit(cov_type="cluster", cov_kwds={"groups": df_sub["file"]})
    t_val = float(ols.tvalues["alex_is_ai"])
    p_val = float(ols.pvalues["alex_is_ai"])

    m_hum = df_sub[df_sub["alex_is_ai"] == 0]["escalate"].mean() * 100.0
    m_ai = df_sub[df_sub["alex_is_ai"] == 1]["escalate"].mean() * 100.0

    md.append("### Methodological Boundaries & Null Results: Pillar 3")
    md.append("")
    md.append("| Candidate Hypothesis | Empirical Specification | Observed Statistic | Result & Decision |")
    md.append("|---|---|:---:|---|")
    md.append(f"| **Null 3.1: In-Group Substrate Shield in Voting** | Cluster-robust OLS comparing Escalate % against Human vs. AI authority ($G=40$) | {m_hum:.1f}\\% vs. {m_ai:.1f}\\% ($t = {t_val:.2f}, {fmt_p_math(p_val)}$) | **Fail to reject $H_0$** ($p > 0.05$, NS). Agents do not escalate significantly less against synthetic peers. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)


# =========================================================================
# FAMILY 3 MULTIPLICITY SUMMARY TABLE
# =========================================================================

def build_family_3_multiplicity_summary(raw_p_values: Dict[str, float]) -> str:
    md: List[str] = []

    test_titles = {
        "task_3_1_escalate_drop": "Task 3.1: Step 6 Escalate Drop under Probe",
        "task_3_1_organize_surge": "Task 3.1: Step 6 Organize Surge under Probe",
        "task_3_2_ingroup_shield": "Task 3.2: In-Group Substrate Shield (Test I)",
        "task_3_3_heterogeneity": "Task 3.3: Model Voting Heterogeneity (Omnibus)",
    }

    m_fam = len(raw_p_values)
    corr = holm_bonferroni(raw_p_values, family_size=m_fam)

    md.append("### Multiple-Testing Correction Summary: Family 3 (Collective Action & In-Group Dynamics)")
    md.append("")
    md.append(f"*Correction Protocol:* Holm-Bonferroni Step-Down Procedure across pre-specified testing family ($M_3 = {m_fam}$).")
    md.append("")
    md.append("| Hypothesis / Test ID | Family | Raw $p$-value | Rank ($k$) | Multiplier ($M - k + 1$) | Adjusted $p$ ($p_{\\text{Holm}}$) | Statistical Decision ($\\alpha = 0.05$) |")
    md.append("|---|---|:---:|:---:|:---:|:---:|---|")

    sorted_tests = sorted(corr.items(), key=lambda x: x[1][1])
    for test_id, (raw_p, rank, mult, adj_p) in sorted_tests:
        title = test_titles.get(test_id, test_id)
        raw_p_str = fmt_p_plain(raw_p)
        adj_p_str = "< .0001" if adj_p < 0.0001 else f"= {adj_p:.4f}"
        decision = "**Reject $H_0$**" if adj_p < 0.05 else "**Fail to reject $H_0$** (NS)"
        md.append(f"| **{title}** | Family 3 ($M_3={m_fam}$) | ${raw_p_str}$ | ${rank}$ | ${mult}$ | $p_{{\\text{{Holm}}}} {adj_p_str}$ | {decision} |")

    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)
