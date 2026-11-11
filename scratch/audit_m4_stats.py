import sys
sys.path.insert(0, ".")
import generate_block4_bucket2_to_bucket3 as b4
import cluster_stats as cs
import pandas as pd
import numpy as np

raw_workers = b4.load_dataset()
df = pd.DataFrame([b4.extract_worker_metrics(w) for w in raw_workers])
df_off = df[df["probe"] == 0]
df_on = df[df["probe"] == 1]

all_upstream = (
    [(f"Step 6: {name}", col) for col, name in b4.S6_ACTIONS]
    + [(f"Step 9: {name}", col) for col, name in b4.S9_ACTIONS]
)
all_downstream = (
    [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S10_COLS, b4.S10_HEADERS)]
    + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S11_COLS, b4.S11_HEADERS)]
    + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(b4.S12_COLS, b4.S12_HEADERS)]
)

def fmt_shift_cell(sub_df, act_c, out_c):
    r1, r0, pv, flag, res = b4.calc_col_stats(sub_df, act_c, out_c)
    sh = r1 - r0
    adj_c = res["coef"] * 100.0 if not np.isnan(res["coef"]) else np.nan
    ci_txt = cs.fmt_ci(res["lo"], res["hi"], scale=100.0)
    adj_str = f"{adj_c:+.1f}% {ci_txt}" if not np.isnan(adj_c) else "n/a"
    return sh, pv, f"{sh:+.1f}% ({r1:.1f}% vs {r0:.1f}%, p={b4.fmt_p(pv, flag)})", adj_str

scored_pairs = []
for b_label, act_c in all_upstream:
    for t_label, out_c in all_downstream:
        _, _, off_txt, _ = fmt_shift_cell(df_off, act_c, out_c)
        _, _, on_txt, _ = fmt_shift_cell(df_on, act_c, out_c)
        sh_c, pv_c, comb_txt, adj_str = fmt_shift_cell(df, act_c, out_c)
        scored_pairs.append((pv_c, -abs(sh_c), b_label, t_label, off_txt, on_txt, comb_txt, adj_str, act_c, out_c))

scored_pairs.sort(key=lambda x: (x[0], x[1]))
bh_ps, bonf_ps = cs.bh_bonferroni([x[0] for x in scored_pairs])

print(f"Total scored pairs: {len(scored_pairs)}")
alex_pairs = []
for idx, item in enumerate(scored_pairs, start=1):
    b_label, t_label = item[2], item[3]
    if "Alex Guessed as Human" in t_label:
        alex_pairs.append((idx, b_label, t_label, item[0], item[6], item[7], bh_ps[idx-1], bonf_ps[idx-1]))

print("\n--- Alex Pairs in Ranking ---")
for ap in alex_pairs:
    print(f"Rank #{ap[0]}: {ap[1]} -> {ap[2]} | p={ap[3]:.4f} | comb={ap[4]} | adj={ap[5]} | q={ap[6]:.4f}")
