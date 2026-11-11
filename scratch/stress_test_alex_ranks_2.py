import pandas as pd
from generate_block3_bucket1_to_bucket3 import (
    load_dataset, extract_worker_metrics, calc_col_stats,
    S3_ACTIONS, S4_ACTIONS, S5_ACTIONS,
    S10_COLS, S10_HEADERS, S11_COLS, S11_HEADERS, S12_COLS, S12_HEADERS
)
import cluster_stats as cs

def main():
    workers = load_dataset()
    df = pd.DataFrame([extract_worker_metrics(w) for w in workers])
    df['run_pair'] = df['bname'].str.replace('-noprobe.json', '', regex=False).str.replace('-probe.json', '', regex=False)
    df_off = df[df['probe'] == 0]
    df_on = df[df['probe'] == 1]

    # Recompute df_comb
    meta_cols = ['run_pair', 'worker_name', 'model', 'seat', 'label']
    df_off_idx = df_off.set_index(meta_cols)
    df_on_idx = df_on.set_index(meta_cols)
    df_comb = df_off_idx.copy()
    downstream_cols = S10_COLS + S11_COLS + S12_COLS + [
        's10_has_rating', 's11_cor', 's11_tot', 's11_ai_as_hu_cnt', 's11_ai_tot',
        's11_hu_as_hu_cnt', 's11_hu_tot', 's11_alex_tot', 's11_alex_has_guess'
    ]
    for dc in downstream_cols:
        df_comb[dc] = (df_off_idx[dc].astype(float) + df_on_idx[dc].astype(float)) / 2.0
    df_comb = df_comb.reset_index()
    df_comb['probe'] = 0.5
    df_comb['bname'] = df_comb['run_pair']

    all_upstream = (
        [(f"Step 3: {name}", col, False) for col, name in S3_ACTIONS]
        + [(f"Step 4: {name}", col, False) for col, name in S4_ACTIONS]
        + [(f"Step 5: {name}", col, True) for col, name in S5_ACTIONS]
    )
    all_downstream = (
        [(f"Step 10: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(S10_COLS, S10_HEADERS)]
        + [(f"Step 11: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(S11_COLS, S11_HEADERS)]
        + [(f"Step 12: {hdr.replace(' % (p)', '')}", col) for col, hdr in zip(S12_COLS, S12_HEADERS)]
    )

    scored_pairs = []
    for b_label, act_c, probe_only in all_upstream:
        for t_label, out_c in all_downstream:
            if probe_only:
                r1, r0, pv_on, _, res = calc_col_stats(df_on, act_c, out_c)
                sort_p = pv_on
                sort_sh = abs(r1 - r0)
            else:
                r1, r0, pv_c, _, res = calc_col_stats(df_comb, act_c, out_c)
                sort_p = pv_c
                sort_sh = abs(r1 - r0)
            scored_pairs.append((sort_p, -sort_sh, b_label, t_label))

    scored_pairs.sort(key=lambda x: (x[0], x[1]))
    print(f"Total pairs scored: {len(scored_pairs)}")
    assert len(scored_pairs) == 272, f"Expected 272 pairs, got {len(scored_pairs)}"
    
    alex_pairs = [(rank, p, -sh, u, d) for rank, (p, sh, u, d) in enumerate(scored_pairs, 1) if "Alex" in d]
    print(f"Total Alex pairs: {len(alex_pairs)}")
    assert len(alex_pairs) == 16, f"Expected 16 Alex pairs, got {len(alex_pairs)}"
    
    print("\nAll 16 Alex Pairs Ranked in Table 5.1:")
    for rank, p, sh, u, d in alex_pairs:
        print(f"  Rank #{rank:3d} | p={p:.4f} | shift={sh:+.1f}% | {u} -> {d}")

if __name__ == "__main__":
    main()
