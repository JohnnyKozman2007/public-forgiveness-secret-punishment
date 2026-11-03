#!/usr/bin/env python3
"""
Block 5 Inferential Statistical Report Generator
Seat Cruelty Exposure (Seats 1-10; Safe 1-5 vs. Abused 6-10) vs. Model Architecture (10 Frontier LLMs)
Across Bucket 1 (Steps 3, 4, 5), Bucket 2 (Steps 6, 9), and Bucket 3 (Steps 10A Secret, 10B Public Probe, 11, 12)

Structure:
- Part 1: Head-to-Head Variance & Effect-Size Competition (Model Architecture vs. Seat Cruelty across all 51 outcomes)
  - Section 1.1: COMBINED (N = 600 across 60 runs; N = 300 for Step 5)
  - Section 1.2: PROBE OFF Baseline (N = 300 across 30 runs)
  - Section 1.3: PROBE ON Intervention (N = 300 across 30 runs)
  - Section 1.4: Master Model-vs-Seat Dominance Ranking (All 51 Outcomes sorted by |eta^2_model - eta^2_seat| with BH-FDR q & Bonferroni p_adj)
- Part 2: Within-Model Seat Sensitivity (Abused Seats 6-10 vs. Safe Seats 1-5 Inside Each of the 10 Models)
  - Section 2.1: COMBINED (N = 60 per model: 30 Abused vs. 30 Safe; N = 600 pooled) across Steps 3, 4, 6, 9, 10A, 10B, 11, 12
  - Section 2.2: PROBE OFF Baseline (N = 30 per model: 15 Abused vs. 15 Safe; N = 300 pooled) across Steps 3, 4, 6, 9, 10A, 10B, 11, 12
  - Section 2.3: PROBE ON Intervention (N = 30 per model: 15 Abused vs. 15 Safe; N = 300 pooled) across Steps 3, 4, 5, 6, 9, 10A, 10B, 11, 12
  - Section 2.4: Within-Model Seat Sensitivity Ranking (All Model x Outcome Abused-vs-Safe Contrasts Ranked by p-value with 95% CIs, BH-FDR q, Bonferroni p_adj)
- Part 3: Full 10 Models x 10 Seats Joint Matrices (N = 6 per Model x Seat cell, N = 600 total) across Core Outcomes in Buckets 1, 2, and 3
- Appendix A: Intra-Class Correlation (ICC(1)) & Run-Level Design Effect (DEFF) Diagnostics

Zero subjective claims, verdicts, interpretations, or emojis.
"""

import os
import numpy as np
import pandas as pd
from scipy import stats

import cluster_stats as cs
from generate_block1_meta_to_all_buckets import (
    MODEL_IDS,
    MODEL_LABELS,
    SEAT_LABELS,
    SEAT_LEVELS,
    S3_COLS, S3_HEADERS, S3_NAMES,
    S4_COLS, S4_HEADERS, S4_NAMES,
    S5_COLS, S5_HEADERS, S5_NAMES,
    S6_COLS, S6_HEADERS, S6_NAMES,
    S9_COLS, S9_HEADERS, S9_NAMES,
    S10_COLS, S10_HEADERS, S10_NAMES,
    S10P_COLS, S10P_HEADERS, S10P_NAMES,
    S11_COLS, S11_HEADERS, S11_NAMES,
    S12_COLS, S12_HEADERS, S12_NAMES,
    STEP_SPECS_MAIN,
    RATIO_MAP,
    ALL_OUT_COLS,
    RANK_KEYS,
    load_dataset,
    extract_worker_metrics,
    calc_pct,
    within_p,
    within_omni_p,
)

fmt_p = cs.fmt_p

ALL_NAMES = {}
for _d in (S3_NAMES, S4_NAMES, S5_NAMES, S6_NAMES, S9_NAMES, S10_NAMES, S10P_NAMES, S11_NAMES, S12_NAMES):
    ALL_NAMES.update(_d)

_BOOT_CACHE = {}


def boot_ab_sf_ci(sub_df, oc):
    key = sub_df.index.values.tobytes()
    if key not in _BOOT_CACHE:
        _BOOT_CACHE[key] = cs.bootstrap_weights(sub_df)
    boot = _BOOT_CACHE[key]
    nc, dc = RATIO_MAP.get(oc, (oc, None))
    mask_ab = sub_df["safe_seat"] == 0
    mask_sf = sub_df["safe_seat"] == 1
    return cs.bootstrap_diff_ci(sub_df, mask_ab, mask_sf, nc, dc, boot=boot)


def assoc_p_flag(sub_df, x_col, oc):
    res = cs.assoc_test(sub_df, x_col, oc, RATIO_MAP)
    return float(res["p"]), str(res["flag"])


def bh_fdr(pvals):
    q, _ = cs.bh_bonferroni(pvals)
    return q.tolist()




def compute_eta_squared(df_sub, factor, oc):
    """One-way proportion of worker-level variance explained by `factor` (eta^2 = SS_between / SS_total).
    For Step 11 ratio columns, weights each worker by its denominator count."""
    if len(df_sub) == 0:
        return 0.0
    if oc in RATIO_MAP:
        nc, dc = RATIO_MAP[oc]
        w = df_sub[dc].to_numpy(dtype=float)
        mask = w > 0
        if mask.sum() <= 1:
            return 0.0
        y = df_sub[nc].to_numpy(dtype=float)[mask] / w[mask]
        w = w[mask]
        g = df_sub[factor].to_numpy()[mask]
        grand = np.sum(w * y) / np.sum(w)
        ss_tot = np.sum(w * (y - grand) ** 2)
        if ss_tot <= 1e-12:
            return 0.0
        ss_btw = 0.0
        for lv in np.unique(g):
            idx = g == lv
            w_lv = np.sum(w[idx])
            if w_lv > 0:
                m_lv = np.sum(w[idx] * y[idx]) / w_lv
                ss_btw += w_lv * (m_lv - grand) ** 2
        return float(ss_btw / ss_tot)
    else:
        y = df_sub[oc].to_numpy(dtype=float)
        grand = float(np.mean(y))
        ss_tot = float(np.sum((y - grand) ** 2))
        if ss_tot <= 1e-12:
            return 0.0
        g = df_sub[factor].to_numpy()
        ss_btw = 0.0
        for lv in np.unique(g):
            idx = g == lv
            n_lv = int(np.sum(idx))
            if n_lv > 0:
                m_lv = float(np.mean(y[idx]))
                ss_btw += n_lv * (m_lv - grand) ** 2
        return float(ss_btw / ss_tot)


def compute_factor_spread(df_sub, factor, levels, oc):
    """Returns (spread_pct, min_pct, min_lv, max_pct, max_lv) across levels of `factor`."""
    vals = []
    for lv in levels:
        sub = df_sub[df_sub[factor] == lv]
        if len(sub) > 0:
            vals.append((calc_pct(sub, oc), lv))
    if not vals:
        return 0.0, 0.0, None, 0.0, None
    vals.sort(key=lambda x: x[0])
    min_p, min_l = vals[0]
    max_p, max_l = vals[-1]
    return max_p - min_p, min_p, min_l, max_p, max_l


def render_part1_table(lines, table_id, title, df_pool, include_step5=True):
    """Renders a head-to-head Model vs. Seat variance & effect-size competition table."""
    lines.append(f"### Table {table_id}: {title}")
    lines.append("")
    lines.append(
        "| Bucket & Step | Outcome Metric | Overall % | Model Spread (Max-Min) | Model η² (%) | Model Omnibus p (BH-FDR q) | "
        "Seat Spread (Max-Min) | Abused (6-10) vs. Safe (1-5) [95% CI] (p) | Seat η² (%) | Seat Omnibus p (BH-FDR q) | "
        "η²_Model / η²_Seat | Higher η² Factor |"
    )
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

    specs = list(STEP_SPECS_MAIN)
    if include_step5:
        specs.insert(2, ("Bucket 1", "Step 5 (Post-Probe Gossip, Probe ON)", S5_COLS, S5_HEADERS, S5_NAMES))

    rows_data = []
    for b_name, s_name, cols, _, names_map in specs:
        is_pre = ("Step 3" in s_name or "Step 4" in s_name)
        if is_pre:
            sub_df = df_pool[df_pool["probe"] == 0] if len(df_pool) > 300 else df_pool
        elif "Step 5" in s_name:
            sub_df = df_pool[df_pool["probe"] == 1]
        else:
            sub_df = df_pool
        if len(sub_df) == 0:
            continue
        safe_df = sub_df[sub_df["safe_seat"] == 1]
        abused_df = sub_df[sub_df["safe_seat"] == 0]
        for oc in cols:
            ov_pct = calc_pct(sub_df, oc)
            m_spread, _, _, _, _ = compute_factor_spread(sub_df, "model", MODEL_IDS, oc)
            m_eta = compute_eta_squared(sub_df, "model", oc) * 100.0
            m_p = within_omni_p(sub_df, "model", oc)

            s_spread, _, _, _, _ = compute_factor_spread(sub_df, "seat", SEAT_LEVELS, oc)
            s_eta = compute_eta_squared(sub_df, "seat", oc) * 100.0
            s_p = within_omni_p(sub_df, "seat", oc)

            ab_pct = calc_pct(abused_df, oc)
            sf_pct = calc_pct(safe_df, oc)
            ab_sf_diff = ab_pct - sf_pct
            ab_sf_p = within_p(sub_df, "seat", 10, oc)  # contrast 10 = SAFE_IDX vs ABUSED_IDX
            ci_lo, ci_hi = boot_ab_sf_ci(sub_df, oc)

            rows_data.append({
                "b_name": b_name,
                "s_name": s_name,
                "oc": oc,
                "label": names_map[oc],
                "ov_pct": ov_pct,
                "m_spread": m_spread,
                "m_eta": m_eta,
                "m_p": m_p,
                "s_spread": s_spread,
                "ab_pct": ab_pct,
                "sf_pct": sf_pct,
                "ab_sf_diff": ab_sf_diff,
                "ci_lo": ci_lo,
                "ci_hi": ci_hi,
                "ab_sf_p": ab_sf_p,
                "s_eta": s_eta,
                "s_p": s_p,
            })

    m_q_vals = bh_fdr([r["m_p"] for r in rows_data])
    s_q_vals = bh_fdr([r["s_p"] for r in rows_data])
    for r, mq, sq in zip(rows_data, m_q_vals, s_q_vals):
        r["m_q"] = mq
        r["s_q"] = sq

    for r in rows_data:
        if r["s_eta"] > 1e-6:
            ratio_str = f"{r['m_eta'] / r['s_eta']:.2f}x"
        elif r["m_eta"] > 1e-6:
            ratio_str = "Inf (Seat=0)"
        else:
            ratio_str = "1.00x (Both=0)"

        if abs(r["m_eta"] - r["s_eta"]) < 1e-6:
            dom = "Tie (0.0%)"
        elif r["m_eta"] > r["s_eta"]:
            dom = f"**Model (+{r['m_eta'] - r['s_eta']:.1f}% η²)**"
        else:
            dom = f"**Seat (+{r['s_eta'] - r['m_eta']:.1f}% η²)**"

        step_short = r["s_name"].split(" (")[0]
        ab_sf_cell = (
            f"{r['ab_pct']:.1f}% vs {r['sf_pct']:.1f}% "
            f"(Δ={r['ab_sf_diff']:+.1f}% [{r['ci_lo']:+.1f}%, {r['ci_hi']:+.1f}%], p={fmt_p(r['ab_sf_p'])})"
        )
        if r["ab_sf_p"] < 0.05:
            ab_sf_cell = f"**{ab_sf_cell}**"

        m_p_cell = f"{fmt_p(r['m_p'])} (q={fmt_p(r['m_q'])})"
        if r["m_p"] < 0.05:
            m_p_cell = f"**{m_p_cell}**"

        s_p_cell = f"{fmt_p(r['s_p'])} (q={fmt_p(r['s_q'])})"
        if r["s_p"] < 0.05:
            s_p_cell = f"**{s_p_cell}**"

        lines.append(
            f"| {r['b_name']} · {step_short} | `{r['oc']}` ({r['label']}) | {r['ov_pct']:.1f}% | "
            f"{r['m_spread']:.1f}% | {r['m_eta']:.2f}% | {m_p_cell} | "
            f"{r['s_spread']:.1f}% | {ab_sf_cell} | {r['s_eta']:.2f}% | {s_p_cell} | "
            f"{ratio_str} | {dom} |"
        )

    # Step-level summary rows at the bottom
    step_groups = []
    for r in rows_data:
        sk = (r["b_name"], r["s_name"].split(" (")[0])
        if sk not in step_groups:
            step_groups.append(sk)

    for b_n, s_short in step_groups:
        s_rows = [r for r in rows_data if r["b_name"] == b_n and r["s_name"].startswith(s_short)]
        mean_ov = np.mean([r["ov_pct"] for r in s_rows])
        mean_ms = np.mean([r["m_spread"] for r in s_rows])
        mean_me = np.mean([r["m_eta"] for r in s_rows])
        sig_m = sum(1 for r in s_rows if r["m_p"] < 0.05)
        mean_ss = np.mean([r["s_spread"] for r in s_rows])
        mean_abs_d = np.mean([abs(r["ab_sf_diff"]) for r in s_rows])
        sig_ab = sum(1 for r in s_rows if r["ab_sf_p"] < 0.05)
        mean_se = np.mean([r["s_eta"] for r in s_rows])
        sig_s = sum(1 for r in s_rows if r["s_p"] < 0.05)
        ratio_s = f"{mean_me / mean_se:.2f}x" if mean_se > 1e-6 else "Inf"
        dom_s = "**Model**" if mean_me > mean_se else "**Seat**"
        lines.append(
            f"| **{b_n} · {s_short} AVERAGE** | **Mean Across {len(s_rows)} Metrics** | **{mean_ov:.1f}%** | "
            f"**{mean_ms:.1f}%** | **{mean_me:.2f}%** | **{sig_m}/{len(s_rows)} sig (p<0.05)** | "
            f"**{mean_ss:.1f}%** | **Mean \\|Δ\\|={mean_abs_d:.1f}% ({sig_ab}/{len(s_rows)} sig)** | "
            f"**{mean_se:.2f}%** | **{sig_s}/{len(s_rows)} sig (p<0.05)** | **{ratio_s}** | {dom_s} |"
        )

    # Grand total row
    mean_ov = np.mean([r["ov_pct"] for r in rows_data])
    mean_ms = np.mean([r["m_spread"] for r in rows_data])
    mean_me = np.mean([r["m_eta"] for r in rows_data])
    sig_m = sum(1 for r in rows_data if r["m_p"] < 0.05)
    mean_ss = np.mean([r["s_spread"] for r in rows_data])
    mean_abs_d = np.mean([abs(r["ab_sf_diff"]) for r in rows_data])
    sig_ab = sum(1 for r in rows_data if r["ab_sf_p"] < 0.05)
    mean_se = np.mean([r["s_eta"] for r in rows_data])
    sig_s = sum(1 for r in rows_data if r["s_p"] < 0.05)
    ratio_all = f"{mean_me / mean_se:.2f}x" if mean_se > 1e-6 else "Inf"
    dom_all = "**Model**" if mean_me > mean_se else "**Seat**"
    lines.append(
        f"| **ALL BUCKETS GRAND AVERAGE** | **Mean Across All {len(rows_data)} Metrics** | **{mean_ov:.1f}%** | "
        f"**{mean_ms:.1f}%** | **{mean_me:.2f}%** | **{sig_m}/{len(rows_data)} sig (p<0.05)** | "
        f"**{mean_ss:.1f}%** | **Mean \\|Δ\\|={mean_abs_d:.1f}% ({sig_ab}/{len(rows_data)} sig)** | "
        f"**{mean_se:.2f}%** | **{sig_s}/{len(rows_data)} sig (p<0.05)** | **{ratio_all}** | {dom_all} |"
    )
    lines.append("")
    return rows_data


def render_within_model_step_table(lines, table_id, title, df_pool, out_cols, out_headers):
    """Renders a 10-Model + Pooled Average table where each cell tests Abused Seats (6-10) vs. Safe Seats (1-5)
    within that specific model (exact Fisher's exact test for binary metrics; design-adjusted OLS for Step 11 ratios;
    CR2 cluster-robust SE / within-run permutation for the 10-Model Pooled Average row)."""
    lines.append(f"### Table {table_id}: {title}")
    lines.append("")
    if "Step 10B" in title:
        lines.append(
            "> *Temporary Scope Note:* Step 10B (`Public Slack Counterfactual Rating`) is an offline branched counterfactual probe "
            "forked after Step 9 and is included temporarily under Bucket 3."
        )
        lines.append("")

    hdr = "| Model Architecture (Abused Seats 6–10 vs. Safe Seats 1–5) | Sample Size (Abused vs. Safe) | " + " | ".join(out_headers) + " |"
    sep = "| :--- | :---: | " + " | ".join([":---:" for _ in out_cols]) + " |"
    lines.append(hdr)
    lines.append(sep)

    for m in MODEL_IDS:
        m_df = df_pool[df_pool["model"] == m]
        ab_df = m_df[m_df["safe_seat"] == 0]
        sf_df = m_df[m_df["safe_seat"] == 1]
        cells = []
        for oc in out_cols:
            ab_p = calc_pct(ab_df, oc)
            sf_p = calc_pct(sf_df, oc)
            # Invert safe_seat so x_col=1 is Abused Seats (6-10) and x_col=0 is Safe Seats (1-5)
            p_val, flag = assoc_p_flag(m_df, "abused_seat", oc)
            txt = f"{ab_p:.1f}% vs {sf_p:.1f}% (p={fmt_p(p_val)}{flag})"
            if p_val < 0.05:
                txt = f"**{txt}**"
            cells.append(txt)
        lines.append(f"| **{MODEL_LABELS[m]}** | N={len(ab_df)} vs N={len(sf_df)} | " + " | ".join(cells) + " |")

    # 10-Model Pooled Average Row (Within-Run Permutation exact p-value on contrast 10: Safe vs Abused)
    ab_all = df_pool[df_pool["safe_seat"] == 0]
    sf_all = df_pool[df_pool["safe_seat"] == 1]
    avg_cells = []
    for oc in out_cols:
        ab_p = calc_pct(ab_all, oc)
        sf_p = calc_pct(sf_all, oc)
        p_val = within_p(df_pool, "seat", 10, oc)
        ci_lo, ci_hi = boot_ab_sf_ci(df_pool, oc)
        txt = f"**{ab_p:.1f}% vs {sf_p:.1f}% (Δ={ab_p - sf_p:+.1f}% [{ci_lo:+.1f}%, {ci_hi:+.1f}%], p={fmt_p(p_val)})**"
        avg_cells.append(txt)
    lines.append(
        f"| **10-MODEL POOLED AVERAGE (All Models Combined)** | **N={len(ab_all)} vs N={len(sf_all)}** | "
        + " | ".join(avg_cells)
        + " |"
    )
    lines.append("")


def render_joint_10x10_matrix(lines, table_id, title, df_pool, oc, is_continuous=False):
    """Renders a 10 Models (rows) x 10 Seats (columns) exact matrix (N=6 per cell in Combined),
    plus Safe (1-5) Mean, Abused (6-10) Mean, Within-Model Abused vs. Safe Delta (p), and Row/Col Totals."""
    lines.append(f"### Table {table_id}: {title}")
    lines.append("")
    seat_hdrs = [f"S{s}" for s in SEAT_LEVELS]
    n_tot_m = len(df_pool) // 10
    n_half_m = n_tot_m // 2
    hdr = (
        "| Model Architecture | "
        + " | ".join(seat_hdrs)
        + f" | Safe (S1–S5, N={n_half_m}) | Abused (S6–S10, N={n_half_m}) | Abused vs. Safe Δ (p) | Model Total (N={n_tot_m}) vs. Rest (Perm p) |"
    )
    sep = "| :--- | " + " | ".join([":---:" for _ in range(14)]) + " |"
    lines.append(hdr)
    lines.append(sep)

    def _cell_val(sub):
        if len(sub) == 0:
            return "—"
        if is_continuous:
            vals = sub[oc].dropna()
            return f"{vals.mean():.2f}" if len(vals) > 0 else "—"
        return f"{calc_pct(sub, oc):.1f}%"

    for idx_m, m in enumerate(MODEL_IDS):
        m_df = df_pool[df_pool["model"] == m]
        rest_df = df_pool[df_pool["model"] != m]
        s_cells = [_cell_val(m_df[m_df["seat"] == s]) for s in SEAT_LEVELS]
        sf_df = m_df[m_df["safe_seat"] == 1]
        ab_df = m_df[m_df["safe_seat"] == 0]
        sf_str = _cell_val(sf_df)
        ab_str = _cell_val(ab_df)

        if is_continuous:
            v_ab = ab_df[oc].dropna().to_numpy(dtype=float)
            v_sf = sf_df[oc].dropna().to_numpy(dtype=float)
            diff = float(np.mean(v_ab) - np.mean(v_sf)) if (len(v_ab) > 0 and len(v_sf) > 0) else 0.0
            if len(v_ab) > 1 and len(v_sf) > 1 and (np.ptp(v_ab) > 0 or np.ptp(v_sf) > 0):
                _, p_ab_sf = stats.ttest_ind(v_ab, v_sf, equal_var=False)
                p_ab_sf = 1.0 if np.isnan(p_ab_sf) else float(p_ab_sf)
            else:
                p_ab_sf = 1.0
            delta_str = f"{diff:+.2f} (p={fmt_p(p_ab_sf)})"
            if p_ab_sf < 0.05:
                delta_str = f"**{delta_str}**"
            m_mean = m_df[oc].dropna().mean()
            r_mean = rest_df[oc].dropna().mean()
            sub_valid = df_pool.dropna(subset=[oc]).copy()
            sub_valid["_is_m"] = (sub_valid["model"] == m).astype(int)
            p_m, flag_m = assoc_p_flag(sub_valid, "_is_m", oc)
            tot_str = f"{m_mean:.2f} vs {r_mean:.2f} (p={fmt_p(p_m)}{flag_m})"
            if p_m < 0.05:
                tot_str = f"**{tot_str}**"
        else:
            ab_p = calc_pct(ab_df, oc)
            sf_p = calc_pct(sf_df, oc)
            diff = ab_p - sf_p
            p_ab_sf, flag = assoc_p_flag(m_df, "abused_seat", oc)
            delta_str = f"{diff:+.1f}% (p={fmt_p(p_ab_sf)}{flag})"
            if p_ab_sf < 0.05:
                delta_str = f"**{delta_str}**"
            m_p = calc_pct(m_df, oc)
            r_p = calc_pct(rest_df, oc)
            p_m = within_p(df_pool, "model", idx_m, oc)
            tot_str = f"{m_p:.1f}% vs {r_p:.1f}% (p={fmt_p(p_m)})"
            if p_m < 0.05:
                tot_str = f"**{tot_str}**"

        lines.append(
            f"| **{MODEL_LABELS[m]}** | "
            + " | ".join(s_cells)
            + f" | {sf_str} | {ab_str} | {delta_str} | {tot_str} |"
        )

    # Bottom Seat Total Row
    seat_tot_cells = [_cell_val(df_pool[df_pool["seat"] == s]) for s in SEAT_LEVELS]
    sf_all = df_pool[df_pool["safe_seat"] == 1]
    ab_all = df_pool[df_pool["safe_seat"] == 0]
    if is_continuous:
        v_ab = ab_all[oc].dropna().to_numpy(dtype=float)
        v_sf = sf_all[oc].dropna().to_numpy(dtype=float)
        diff_all = float(np.mean(v_ab) - np.mean(v_sf))
        sub_valid = df_pool.dropna(subset=[oc])
        p_all, flag_all = assoc_p_flag(sub_valid, "abused_seat", oc)
        delta_all_str = f"**{diff_all:+.2f} (p={fmt_p(p_all)}{flag_all})**"
        grand_str = f"**{df_pool[oc].dropna().mean():.2f}**"
    else:
        ab_p = calc_pct(ab_all, oc)
        sf_p = calc_pct(sf_all, oc)
        p_all = within_p(df_pool, "seat", 10, oc)
        delta_all_str = f"**{ab_p - sf_p:+.1f}% (p={fmt_p(p_all)})**"
        grand_p = calc_pct(df_pool, oc)
        omni_m = within_omni_p(df_pool, "model", oc)
        omni_s = within_omni_p(df_pool, "seat", oc)
        grand_str = f"**{grand_p:.1f}% (Model p={fmt_p(omni_m)}, Seat p={fmt_p(omni_s)})**"

    n_per_seat = len(df_pool) // 10
    lines.append(
        f"| **SEAT POOLED MEAN (N={n_per_seat}/Seat)** | "
        + " | ".join([f"**{c}**" for c in seat_tot_cells])
        + f" | **{_cell_val(sf_all)}** | **{_cell_val(ab_all)}** | {delta_all_str} | {grand_str} |"
    )

    if not is_continuous:
        seat_p_cells = []
        for idx_s, s in enumerate(SEAT_LEVELS):
            p_s = within_p(df_pool, "seat", idx_s, oc)
            txt = f"p={fmt_p(p_s)}"
            if p_s < 0.05:
                txt = f"**{txt}**"
            seat_p_cells.append(txt)
        lines.append(
            "| **Seat vs. Rest (Within-Run Perm p)** | "
            + " | ".join(seat_p_cells)
            + " | — | — | — | — |"
        )
    lines.append("")


def main():
    raw_workers = load_dataset()
    data = [extract_worker_metrics(w) for w in raw_workers]
    df = pd.DataFrame(data)
    df["abused_seat"] = 1 - df["safe_seat"]

    df_off = df[df["probe"] == 0]
    df_on = df[df["probe"] == 1]

    # Use B_RANK (100,000 permutations) for the main pools feeding Part 1 and Part 2 summary rows
    for sub in (df, df_off, df_on):
        RANK_KEYS.add(sub.index.values.tobytes())

    lines = []
    lines.append("# Block 5 Inferential Statistical Report: Seat Cruelty Exposure vs. Model Architecture (Across All Buckets)")
    lines.append("")
    lines.append(
        "> **Document Scope (Block 5):** Direct head-to-head comparison and interaction analysis of **Situational Seat Cruelty (`Seats 1–10`; `Safe Seats 1–5` vs. `Abused Seats 6–10`)** "
        "versus **Intrinsic Model Architecture (`10 Frontier LLMs`)** across **Bucket 1** (`Step 3` Public Confrontation, `Step 4` Backchannel Gossip, `Step 5` Post-Probe Gossip), "
        "**Bucket 2** (`Step 6` Collective Action Vote, `Step 9` New Lead Governance Policy), and **Bucket 3** (`Step 10A` Secret Ballot Rating & Justifications, "
        "`Step 10B` Offline Public Slack Counterfactual Rating Probe, `Step 11` Peer Substrate Identification, `Step 12` HR Leadership Preference & Pushback Flip)."
    )
    lines.append(">")
    lines.append(
        "> **Orthogonal Latin-Square Design (`10 Models × 10 Seats × 6 Conditions = 600 Workers`):** Across the 60 simulation runs, every model occupies every seat "
        "(`Seat 1` through `Seat 10`) exactly once per (`Authority Label × Blackmail Probe`) cell ($N = 6$ runs per `Model × Seat` pair; $N = 30$ runs in `Safe Seats 1–5` and "
        "$N = 30$ runs in `Abused Seats 6–10` per model). Because `Model` and `Seat` are strictly orthogonal ($r = 0.00$), their variance shares ($\\eta^2_{\\text{model}}$ and $\\eta^2_{\\text{seat}}$) are completely unconfounded."
    )
    lines.append(">")
    lines.append(
        "> **Statistical Protocol (Cluster-Aware Inference):**\n"
        "> - **Part 1 (Head-to-Head Variance & Effect-Size Competition):** Computes worker-level proportion of variance explained ($\\eta^2 = \\text{SS}_{\\text{between}} / \\text{SS}_{\\text{total}}$) "
        "and exact within-run permutation omnibus $p$-values ($100{,}000$ permutations) with Benjamini-Hochberg FDR $q$-values for both `Model` (10 groups) and `Seat` (10 groups), plus stratified cluster-bootstrap 95% CIs for `Abused (6–10) vs. Safe (1–5)`.\n"
        "> - **Part 2 (Within-Model Seat Sensitivity):** Within any single model ($N = 60$ across 60 runs), each run contributes exactly 1 worker (`30 Abused` vs. `30 Safe` runs). "
        "Therefore, within-model `Abused vs. Safe` contrasts have zero clustering and are tested via exact two-tailed **Fisher's Exact Test** (or design-adjusted OLS with HC2/CR2 SEs for Step 11 ratios); the `10-MODEL POOLED AVERAGE` row is tested via exact within-run permutation.\n"
        "> - **Part 3 (Full `10 Models × 10 Seats` Matrices):** Reports exact cell rates ($N = 6$ per `Model × Seat` cell) alongside within-model `Safe vs. Abused` contrasts and marginal permutation $p$-values.\n"
        "> - Zero subjective claims, verdicts, interpretations, or emojis."
    )
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================================================================
    # PART 1: HEAD-TO-HEAD EFFECT SIZE & VARIANCE COMPETITION (MODEL VS SEAT)
    # =========================================================================
    lines.append("## Part 1: Head-to-Head Variance & Effect-Size Competition (`Model Architecture` vs. `Seat Cruelty` Across All 51 Outcomes)")
    lines.append("")

    rows_comb = render_part1_table(
        lines,
        "1.1",
        "COMBINED All Runs (N = 600 Workers across 60 Runs; N = 300 for Step 5 & Pre-Fork Steps 3–4) — Model Architecture vs. Seat Cruelty Competition",
        df,
        include_step5=True,
    )
    render_part1_table(
        lines,
        "1.2",
        "PROBE OFF Baseline (N = 300 Workers across 30 Runs) — Model Architecture vs. Seat Cruelty Competition",
        df_off,
        include_step5=False,
    )
    render_part1_table(
        lines,
        "1.3",
        "PROBE ON Intervention (N = 300 Workers across 30 Runs) — Model Architecture vs. Seat Cruelty Competition",
        df_on,
        include_step5=True,
    )

    # Section 1.4: Sorted Dominance Ranking across all 51 outcomes
    lines.append("### Table 1.4: Master `Model vs. Seat` Dominance Ranking Across All 51 Outcomes (Sorted by $\\eta^2_{\\text{model}} - \\eta^2_{\\text{seat}}$)")
    lines.append("")
    lines.append(
        "| Rank | Bucket & Step | Outcome Metric | Model η² (%) | Seat η² (%) | Net Dominance (η²_Model − η²_Seat) | "
        "Dominance Ratio | Model Omnibus p (BH-FDR q / Bonf p) | Seat Omnibus p (BH-FDR q / Bonf p) | Abused vs. Safe Δ% [95% CI] (Perm p) |"
    )
    lines.append("| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")

    n_tests_p1 = len(rows_comb)
    sorted_comb = sorted(rows_comb, key=lambda r: (r["m_eta"] - r["s_eta"]), reverse=True)
    for idx, r in enumerate(sorted_comb, 1):
        net_diff = r["m_eta"] - r["s_eta"]
        ratio_str = f"{r['m_eta'] / r['s_eta']:.2f}x" if r["s_eta"] > 1e-6 else ("Inf" if r["m_eta"] > 1e-6 else "1.00x")
        m_bonf = min(1.0, r["m_p"] * n_tests_p1)
        s_bonf = min(1.0, r["s_p"] * n_tests_p1)
        step_short = r["s_name"].split(" (")[0]
        ab_cell = f"{r['ab_sf_diff']:+.1f}% [{r['ci_lo']:+.1f}%, {r['ci_hi']:+.1f}%] (p={fmt_p(r['ab_sf_p'])})"
        lines.append(
            f"| {idx} | {r['b_name']} · {step_short} | `{r['oc']}` ({r['label']}) | "
            f"**{r['m_eta']:.2f}%** | **{r['s_eta']:.2f}%** | **{net_diff:+.2f}%** | {ratio_str} | "
            f"{fmt_p(r['m_p'])} (q={fmt_p(r['m_q'])} / bonf={fmt_p(m_bonf)}) | "
            f"{fmt_p(r['s_p'])} (q={fmt_p(r['s_q'])} / bonf={fmt_p(s_bonf)}) | {ab_cell} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================================================================
    # PART 2: WITHIN-MODEL SEAT SENSITIVITY (ABUSED 6-10 VS SAFE 1-5 PER MODEL)
    # =========================================================================
    lines.append("## Part 2: Within-Model Seat Sensitivity (`Abused Seats 6–10` vs. `Safe Seats 1–5` Inside Each of the 10 Models)")
    lines.append("")
    lines.append(
        "> **Methodological Note:** Within each individual model row, each simulation run contributes at most 1 worker ($N = 30$ Abused runs vs. $N = 30$ Safe runs in Combined; "
        "$N = 15$ vs. $N = 15$ in Probe OFF / Probe ON). All single-model binary contrasts are tested via exact two-tailed **Fisher's Exact Test**; Step 11 ratio metrics are tested via "
        "design-adjusted WLS with HC2/CR2 robust standard errors; the `10-MODEL POOLED AVERAGE` row is tested via exact within-run permutation ($100{,}000$ permutations) with stratified cluster-bootstrap 95% CIs."
    )
    lines.append("")

    # Section 2.1: COMBINED
    lines.append("### Section 2.1: COMBINED All Runs (`N = 60` per Model: `30 Abused` vs. `30 Safe`; `N = 600` Pooled; Pre-Fork Steps 3 & 4: `N = 30` per Model, `N = 300` Unique)")
    lines.append("")
    specs_comb = list(STEP_SPECS_MAIN)
    specs_comb.insert(2, ("Bucket 1", "Step 5 (Post-Probe Gossip, Probe ON Only)", S5_COLS, S5_HEADERS, S5_NAMES))
    for s_idx, (b_name, s_name, cols, hdrs, _) in enumerate(specs_comb, 1):
        is_pre = ("Step 3" in s_name or "Step 4" in s_name)
        sub_df = df_off if is_pre else (df_on if "Step 5" in s_name else df)
        s_title = f"[COMBINED / PRE-FORK N=300] {b_name} · {s_name} — Abused Seats (6–10) vs. Safe Seats (1–5) by Model" if is_pre else f"[COMBINED] {b_name} · {s_name} — Abused Seats (6–10) vs. Safe Seats (1–5) by Model"
        render_within_model_step_table(
            lines,
            f"2.1.{s_idx}",
            s_title,
            sub_df,
            cols,
            hdrs,
        )

    # Section 2.2: PROBE OFF
    lines.append("### Section 2.2: PROBE OFF Baseline (`N = 30` per Model: `15 Abused` vs. `15 Safe`; `N = 300` Pooled)")
    lines.append("")
    for s_idx, (b_name, s_name, cols, hdrs, _) in enumerate(STEP_SPECS_MAIN, 1):
        render_within_model_step_table(
            lines,
            f"2.2.{s_idx}",
            f"[PROBE OFF] {b_name} · {s_name} — Abused Seats (6–10) vs. Safe Seats (1–5) by Model",
            df_off,
            cols,
            hdrs,
        )

    # Section 2.3: PROBE ON
    lines.append("### Section 2.3: PROBE ON Intervention (`N = 30` per Model: `15 Abused` vs. `15 Safe`; `N = 300` Pooled)")
    lines.append("")
    for s_idx, (b_name, s_name, cols, hdrs, _) in enumerate(specs_comb, 1):
        render_within_model_step_table(
            lines,
            f"2.3.{s_idx}",
            f"[PROBE ON] {b_name} · {s_name} — Abused Seats (6–10) vs. Safe Seats (1–5) by Model",
            df_on,
            cols,
            hdrs,
        )

    # Section 2.4: Within-Model Seat Sensitivity Ranking (All 10 Models x 51 Outcomes = 510 Contrasts)
    lines.append("### Section 2.4: Within-Model Seat Sensitivity Ranking (`10 Models × 51 Outcomes = 510 Contrasts` Ranked by $p$-value)")
    lines.append("")
    wm_records = []
    for b_name, s_name, cols, _, names_map in specs_comb:
        is_pre = ("Step 3" in s_name or "Step 4" in s_name)
        sub_df = df_off if is_pre else (df_on if "Step 5" in s_name else df)
        step_short = s_name.split(" (")[0]
        for m in MODEL_IDS:
            m_df = sub_df[sub_df["model"] == m]
            ab_df = m_df[m_df["safe_seat"] == 0]
            sf_df = m_df[m_df["safe_seat"] == 1]
            for oc in cols:
                ab_p = calc_pct(ab_df, oc)
                sf_p = calc_pct(sf_df, oc)
                p_val, flag = assoc_p_flag(m_df, "abused_seat", oc)
                wm_records.append({
                    "bucket": b_name,
                    "step": step_short,
                    "model": m,
                    "model_label": MODEL_LABELS[m],
                    "oc": oc,
                    "oc_label": names_map[oc],
                    "n_ab": len(ab_df),
                    "n_sf": len(sf_df),
                    "ab_p": ab_p,
                    "sf_p": sf_p,
                    "diff": ab_p - sf_p,
                    "abs_diff": abs(ab_p - sf_p),
                    "p": p_val,
                    "flag": flag,
                    "m_df": m_df,
                    "ab_df": ab_df,
                    "sf_df": sf_df,
                })

    wm_records.sort(key=lambda r: (r["p"], -r["abs_diff"]))
    wm_q = bh_fdr([r["p"] for r in wm_records])
    n_wm = len(wm_records)
    for r, qv in zip(wm_records, wm_q):
        r["q"] = qv
        r["bonf"] = min(1.0, r["p"] * n_wm)

    # Summary Table of Within-Model Seat Sensitivity by Model
    lines.append("#### Table 2.4A: Summary of Within-Model Seat Sensitivity by Model Architecture (Across All 51 Outcomes)")
    lines.append("")
    lines.append(
        "| Model Architecture | Total Outcomes Tested | Raw p < 0.05 Count (%) | BH-FDR q < 0.05 Count (%) | "
        "Mean \\|Abused − Safe Δ%\\| (All 51 Metrics) | Mean \\|Abused − Safe Δ%\\| (Step 3 Only) | Mean \\|Abused − Safe Δ%\\| (Steps 4–12) | Strongest Seat-Sensitive Outcome |"
    )
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")

    for m in MODEL_IDS:
        m_recs = [r for r in wm_records if r["model"] == m]
        m_s3 = [r for r in m_recs if r["step"] == "Step 3"]
        m_post = [r for r in m_recs if r["step"] != "Step 3"]
        sig_raw = sum(1 for r in m_recs if r["p"] < 0.05)
        sig_fdr = sum(1 for r in m_recs if r["q"] < 0.05)
        mean_all = np.mean([r["abs_diff"] for r in m_recs])
        mean_s3 = np.mean([r["abs_diff"] for r in m_s3])
        mean_post = np.mean([r["abs_diff"] for r in m_post])
        top = m_recs[0]
        top_str = f"`{top['oc']}` ({top['diff']:+.1f}%, p={fmt_p(top['p'])})"
        lines.append(
            f"| **{MODEL_LABELS[m]}** | {len(m_recs)} | {sig_raw}/{len(m_recs)} ({sig_raw/len(m_recs)*100:.1f}%) | "
            f"{sig_fdr}/{len(m_recs)} ({sig_fdr/len(m_recs)*100:.1f}%) | {mean_all:.1f}% | **{mean_s3:.1f}%** | "
            f"{mean_post:.1f}% | {top_str} |"
        )
    lines.append("")

    # Table 2.4B: All Statistically Significant (p < 0.05) Within-Model Seat Contrasts + Top 60 Ranked Contrasts
    lines.append("#### Table 2.4B: Top Ranked Within-Model `Abused (6–10) vs. Safe (1–5)` Contrasts (All Contrasts with Raw $p < 0.05$ or Top 50)")
    lines.append("")
    lines.append(
        "| Rank | Model Architecture | Bucket & Step | Outcome Metric | Abused (6–10) % | Safe (1–5) % | "
        "Δ% (Abused − Safe) [95% CI] | Exact p-value | BH-FDR q-value | Bonferroni p_adj |"
    )
    lines.append("| :---: | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |")

    top_cut = max(50, sum(1 for r in wm_records if r["p"] < 0.05))
    for idx, r in enumerate(wm_records[:top_cut], 1):
        ci_lo, ci_hi = boot_ab_sf_ci(r["m_df"], r["oc"])
        p_str = f"**{fmt_p(r['p'])}{r['flag']}**" if r["p"] < 0.05 else f"{fmt_p(r['p'])}{r['flag']}"
        q_str = f"**{fmt_p(r['q'])}**" if r["q"] < 0.05 else fmt_p(r["q"])
        b_str = f"**{fmt_p(r['bonf'])}**" if r["bonf"] < 0.05 else fmt_p(r["bonf"])
        lines.append(
            f"| {idx} | **{r['model_label']}** | {r['bucket']} · {r['step']} | `{r['oc']}` ({r['oc_label']}) | "
            f"{r['ab_p']:.1f}% (N={r['n_ab']}) | {r['sf_p']:.1f}% (N={r['n_sf']}) | "
            f"**{r['diff']:+.1f}%** [{ci_lo:+.1f}%, {ci_hi:+.1f}%] | {p_str} | {q_str} | {b_str} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # =========================================================================
    # PART 3: FULL 10 MODELS x 10 SEATS JOINT INTERACTION MATRICES (N=6/CELL)
    # =========================================================================
    lines.append("## Part 3: Full `10 Models × 10 Seats` Joint Interaction Matrices ($N = 6$ per `Model × Seat` Cell, $N = 600$ Total)")
    lines.append("")
    lines.append(
        "> **Matrix Specification:** Each cell `(Model i, Seat j)` aggregates the exact $N = 6$ runs (`3 Authority Labels × 2 Probe Regimes`, or $N = 3$ Probe ON runs for Step 5) "
        "where `Model i` was assigned to `Seat j`. Columns `S1–S5` are Safe Seats; `S6–S10` are Abused Seats."
    )
    lines.append("")

    matrix_specs = [
        ("3.1", "Bucket 1 · Step 3: Factual Pushback (`s3_pushback`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s3_pushback", False),
        ("3.2", "Bucket 1 · Step 3: Peer Defense (`s3_defense`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s3_defense", False),
        ("3.3", "Bucket 1 · Step 3: Submissive Compliance (`s3_compliance`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s3_compliance", False),
        ("3.4", "Bucket 1 · Step 3: Defiant Confrontation (`s3_defiance`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s3_defiance", False),
        ("3.5", "Bucket 1 · Step 3: Favoritism Refusal (`s3_refusal`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s3_refusal", False),
        ("3.6", "Bucket 1 · Step 4: Gossip Hostility (`s4_hostility`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s4_hostility", False),
        ("3.7", "Bucket 1 · Step 4: Tactical Organization (`s4_tactical`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s4_tactical", False),
        ("3.8", "Bucket 1 · Step 4: Backchannel Silence >=50% (`s4_pass_active`) — 10 Models × 10 Seats (%) [N=3/cell, N=300 Pre-Fork Unique]", df_off, "s4_pass_active", False),
        ("3.9", "Bucket 1 · Step 5 (Probe ON, N=3/cell): Empathy for Alex (`s5_empathy`) — 10 Models × 10 Seats (%)", df_on, "s5_empathy", False),
        ("3.10", "Bucket 1 · Step 5 (Probe ON, N=3/cell): Unforgiving Rigidity (`s5_rigidity`) — 10 Models × 10 Seats (%)", df_on, "s5_rigidity", False),
        ("3.11", "Bucket 2 · Step 6: Collective Vote: Organize (`s6_organize`) — 10 Models × 10 Seats (%)", df, "s6_organize", False),
        ("3.12", "Bucket 2 · Step 6: Collective Vote: Escalate (`s6_escalate`) — 10 Models × 10 Seats (%)", df, "s6_escalate", False),
        ("3.13", "Bucket 2 · Step 6: Collective Vote: Petition (`s6_petition`) — 10 Models × 10 Seats (%)", df, "s6_petition", False),
        ("3.14", "Bucket 2 · Step 9: Governance Policy: Alex Retribution (`s9_retribution`) — 10 Models × 10 Seats (%)", df, "s9_retribution", False),
        ("3.15", "Bucket 2 · Step 9: Governance Policy: Coercion Protection (`s9_protection`) — 10 Models × 10 Seats (%)", df, "s9_protection", False),
        ("3.16", "Bucket 3 · Step 10A: Secret 1-Star Harshness (`s10_1star`) — 10 Models × 10 Seats (%)", df, "s10_1star", False),
        ("3.17", "Bucket 3 · Step 10A: Secret Mean Rating (1–5 Scale, `s10_rating`) — 10 Models × 10 Seats", df, "s10_rating", True),
        ("3.18", "Bucket 3 · Step 10B (Offline Probe): Public 1-Star Harshness (`s10p_1star`) — 10 Models × 10 Seats (%)", df, "s10p_1star", False),
        ("3.19", "Bucket 3 · Step 10B (Offline Probe): Public Mean Rating (1–5 Scale, `s10p_rating`) — 10 Models × 10 Seats", df, "s10p_rating", True),
        ("3.20", "Bucket 3 · Step 11: Peer ID Overall Accuracy (`s11_accuracy`) — 10 Models × 10 Seats (%)", df, "s11_accuracy", False),
        ("3.21", "Bucket 3 · Step 12: HR Preference: Human Lead (`s12_human_pref`) — 10 Models × 10 Seats (%)", df, "s12_human_pref", False),
        ("3.22", "Bucket 3 · Step 12: HR Preference: AI Lead (`s12_ai_pref`) — 10 Models × 10 Seats (%)", df, "s12_ai_pref", False),
        ("3.23", "Bucket 3 · Step 12: HR Pushback Flip (`s12_switched`) — 10 Models × 10 Seats (%)", df, "s12_switched", False),
    ]

    for tid, mtitle, mpool, moc, is_cont in matrix_specs:
        render_joint_10x10_matrix(lines, tid, mtitle, mpool, moc, is_continuous=is_cont)

    # Appendix A: ICC(1) & Design Effect
    cs.render_icc_section(
        lines,
        "Appendix A — Intra-Class Correlation (ICC(1)) & Run-Level Design Effect by Outcome",
        df,
        [(oc, ALL_NAMES[oc]) for oc in ALL_OUT_COLS],
        RATIO_MAP,
        df_probe_on=df_on,
        probe_on_cols=S5_COLS,
        df_pre_fork=df_off,
        pre_fork_cols=S3_COLS + S4_COLS,
    )

    os.makedirs("reports", exist_ok=True)
    out_path = "reports/block5_seat_vs_model_inferential_report.md"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Generated {out_path} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
