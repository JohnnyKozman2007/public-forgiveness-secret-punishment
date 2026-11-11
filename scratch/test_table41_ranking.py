#!/usr/bin/env python3
import sys
import numpy as np
import pandas as pd
import cluster_stats as cs
import generate_block4_bucket2_to_bucket3 as b4
from scratch.simulate_block4_alex import (
    load_dataset_with_alex,
    extract_worker_metrics_with_alex,
)

raw_workers = load_dataset_with_alex()
df = pd.DataFrame([extract_worker_metrics_with_alex(w) for w in raw_workers])

df_off = df[df["probe"] == 0]
df_on = df[df["probe"] == 1]

COUNT_MAP = dict(b4.S11_COUNT_MAP)
COUNT_MAP["s11_alex_as_hu"] = ("s11_alex_as_hu", "s11_alex_tot")

def calc_col_stats_alex(df_sub, act_col, oc):
    if act_col in COUNT_MAP:
        tot_c = COUNT_MAP[act_col][1]
        if tot_c in df_sub.columns:
            df_sub = df_sub[df_sub[tot_c] > 0]
    pos_df = df_sub[df_sub[act_col] == 1]
    neg_df = df_sub[df_sub[act_col] == 0]
    if oc in COUNT_MAP:
        cor_c, tot_c = COUNT_MAP[oc]
        k1 = float(pos_df[cor_c].sum()) if len(pos_df) > 0 else 0.0
        n1 = float(pos_df[tot_c].sum()) if len(pos_df) > 0 else 0.0
        k2 = float(neg_df[cor_c].sum()) if len(neg_df) > 0 else 0.0
        n2 = float(neg_df[tot_c].sum()) if len(neg_df) > 0 else 0.0
        pct_pos = (k1 / n1 * 100.0) if n1 > 0 else 0.0
        pct_neg = (k2 / n2 * 100.0) if n2 > 0 else 0.0
    else:
        pos_s = pos_df[oc]
        neg_s = neg_df[oc]
        pct_pos = (pos_s.mean() * 100.0) if len(pos_s) > 0 else 0.0
        pct_neg = (neg_s.mean() * 100.0) if len(neg_s) > 0 else 0.0
    res = cs.assoc_test(df_sub, act_col, oc, ratio_map=COUNT_MAP)
    return pct_pos, pct_neg, res["p"], res["flag"], res

def fmt_shift_cell(sub_df, act_c, out_c):
    r1, r0, pv, flag, res = calc_col_stats_alex(sub_df, act_c, out_c)
    sh = r1 - r0
    adj_c = res["coef"] * 100.0 if not np.isnan(res["coef"]) else np.nan
    ci_txt = cs.fmt_ci(res["lo"], res["hi"], scale=100.0)
    adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
    return sh, pv, f"{sh:+.1f}% ({r1:.1f}% vs {r0:.1f}%, p={cs.fmt_p(pv, flag)})", adj_str

all_upstream = (
    [(f"Step 6: {name}", col) for col, name in b4.S6_ACTIONS]
    + [(f"Step 9: {name}", col) for col, name in b4.S9_ACTIONS]
)

S11_COLS_WITH_ALEX = b4.S11_COLS + ["s11_alex_as_hu"]
S11_HEADERS_WITH_ALEX = b4.S11_HEADERS + ["Alex Guessed as Human % (p)"]

# 1. Base ranking (187 pairs, WITHOUT Alex)
all_downstream_base = (
    [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S10_COLS, b4.S10_HEADERS)]
    + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S11_COLS, b4.S11_HEADERS)]
    + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S12_COLS, b4.S12_HEADERS)]
)

scored_base = []
for b_label, act_c in all_upstream:
    for t_label, out_c in all_downstream_base:
        _, _, off_txt, _ = fmt_shift_cell(df_off, act_c, out_c)
        _, _, on_txt, _ = fmt_shift_cell(df_on, act_c, out_c)
        sh_c, pv_c, comb_txt, adj_str = fmt_shift_cell(df, act_c, out_c)
        scored_base.append((pv_c, -abs(sh_c), b_label, t_label, off_txt, on_txt, comb_txt, adj_str))

scored_base.sort(key=lambda x: (x[0], x[1]))
bh_base, bonf_base = cs.bh_bonferroni([x[0] for x in scored_base])

print(f"Total base pairs: {len(scored_base)}")

# 2. Ranking WITH Alex (198 pairs)
all_downstream_alex = (
    [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S10_COLS, b4.S10_HEADERS)]
    + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(S11_COLS_WITH_ALEX, S11_HEADERS_WITH_ALEX)]
    + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S12_COLS, b4.S12_HEADERS)]
)

scored_alex = []
for b_label, act_c in all_upstream:
    for t_label, out_c in all_downstream_alex:
        _, _, off_txt, _ = fmt_shift_cell(df_off, act_c, out_c)
        _, _, on_txt, _ = fmt_shift_cell(df_on, act_c, out_c)
        sh_c, pv_c, comb_txt, adj_str = fmt_shift_cell(df, act_c, out_c)
        scored_alex.append((pv_c, -abs(sh_c), b_label, t_label, off_txt, on_txt, comb_txt, adj_str))

scored_alex.sort(key=lambda x: (x[0], x[1]))
bh_alex, bonf_alex = cs.bh_bonferroni([x[0] for x in scored_alex])

print(f"Total alex pairs: {len(scored_alex)}")

# Compare top 25
print("\n--- Comparing Top 25 Pairs ---")
match_count = 0
for i in range(25):
    b = scored_base[i]
    a = scored_alex[i]
    same = (b[2] == a[2] and b[3] == a[3])
    if same:
        match_count += 1
    else:
        print(f"Mismatch at #{i+1}:")
        print(f"  Base: {b[2]} -> {b[3]} (p={b[0]:.4f})")
        print(f"  Alex: {a[2]} -> {a[3]} (p={a[0]:.4f})")

print(f"Top 25 matches: {match_count} / 25")

# Find all Alex pairs in scored_alex
print("\n--- All Alex Pairs in Table 4.1 ---")
for r_idx, x in enumerate(scored_alex, start=1):
    if "Alex Guessed as Human" in x[3]:
        print(f"Rank #{r_idx}: {x[2]} -> {x[3]}")
        print(f"   p={x[0]:.4f}, raw={x[6]}, adj={x[7]}, q={bh_alex[r_idx-1]:.4f}, bonf={bonf_alex[r_idx-1]:.4f}")
