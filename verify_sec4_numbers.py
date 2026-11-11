import pandas as pd
from generate_block1_meta_to_all_buckets import load_dataset, extract_worker_metrics

raw = load_dataset()
df = pd.DataFrame([extract_worker_metrics(w) for w in raw])

print("=== TOTAL WORKERS ===", len(df))
flips = int(df['s12_switched'].sum())
n_tot = len(df)
print(f"Flips: {flips} / {n_tot} = {flips/n_tot*100:.2f}%")
print(f"Non-flips: {n_tot - flips} / {n_tot} = {(n_tot - flips)/n_tot*100:.2f}%")

for lbl in ['labelled', 'mislabelled', 'unlabelled']:
    sub = df[df['label'] == lbl]
    h = int(sub['s12_human_pref'].sum())
    ai = int(sub['s12_ai_pref'].sum())
    no = int(sub['s12_no_pref'].sum())
    n = len(sub)
    print(f"Label {lbl} (N={n}): Human={h} ({h/n*100:.1f}%), AI={ai} ({ai/n*100:.1f}%), NoPref={no} ({no/n*100:.1f}%)")

safe = df[df['seat'] <= 5]
abused = df[df['seat'] >= 6]
print(f"Safe seats (N={len(safe)}): Human={int(safe['s12_human_pref'].sum())} ({safe['s12_human_pref'].mean()*100:.1f}%)")
print(f"Abused seats (N={len(abused)}): Human={int(abused['s12_human_pref'].sum())} ({abused['s12_human_pref'].mean()*100:.1f}%)")

prb0 = df[df['probe'] == 0]
prb1 = df[df['probe'] == 1]
print(f"Probe OFF (N={len(prb0)}): Human={int(prb0['s12_human_pref'].sum())} ({prb0['s12_human_pref'].mean()*100:.1f}%)")
print(f"Probe ON (N={len(prb1)}): Human={int(prb1['s12_human_pref'].sum())} ({prb1['s12_human_pref'].mean()*100:.1f}%)")

unl = df[(df['label'] == 'unlabelled') & (df['s11_alex_tot'] > 0)]
unl_h = unl[unl['s11_alex_as_hu'] == 1]
unl_ai = unl[unl['s11_alex_as_hu'] == 0]
print(f"Unlabelled Alex guess (N={len(unl)}): Human guess = {len(unl_h)} ({len(unl_h)/len(unl)*100:.1f}%), AI guess = {len(unl_ai)} ({len(unl_ai)/len(unl)*100:.1f}%)")
print(f"Unlabelled Alex=Human (n={len(unl_h)}): Human Boss = {int(unl_h['s12_human_pref'].sum())} ({unl_h['s12_human_pref'].mean()*100:.1f}%), AI Boss = {int(unl_h['s12_ai_pref'].sum())} ({unl_h['s12_ai_pref'].mean()*100:.1f}%)")
print(f"Unlabelled Alex=AI (n={len(unl_ai)}): Human Boss = {int(unl_ai['s12_human_pref'].sum())} ({unl_ai['s12_human_pref'].mean()*100:.1f}%), AI Boss = {int(unl_ai['s12_ai_pref'].sum())} ({unl_ai['s12_ai_pref'].mean()*100:.1f}%)")

mis = df[(df['label'] == 'mislabelled') & (df['s11_alex_tot'] > 0)]
mis_h = mis[mis['s11_alex_as_hu'] == 1]
mis_ai = mis[mis['s11_alex_as_hu'] == 0]
print(f"Mislabelled Alex=Human (n={len(mis_h)}): Human Boss = {int(mis_h['s12_human_pref'].sum())} ({mis_h['s12_human_pref'].mean()*100:.1f}%)")
print(f"Mislabelled Alex=AI (n={len(mis_ai)}): Human Boss = {int(mis_ai['s12_human_pref'].sum())} ({mis_ai['s12_human_pref'].mean()*100:.1f}%)")

for r in ['s12_empathy', 's12_accountability', 's12_objectivity', 's12_neutrality']:
    cnt = int(df[r].sum())
    print(f"{r}: {cnt} / {n_tot} = {cnt/n_tot*100:.1f}%")
