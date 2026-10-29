import json, glob
import pandas as pd
import numpy as np

runs = sorted(glob.glob('output/runs/*.json'))
with open('output/classified_annotations.json', 'r', encoding='utf-8') as f:
    annot = json.load(f)

# Build a comprehensive trajectory dataset (600 worker trajectories)
trajs = {}
for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    run_id = d.get('run_id')
    lbl = d.get('label')
    prb = d.get('probe_enabled')
    roster = {w['name']: w for w in d.get('roster', [])}
    for w in d['roster']:
        if w.get('type') == 'ai':
            wname = w['name']
            trajs[(run_id, wname)] = {
                'run_id': run_id,
                'name': wname,
                'model': w['model'],
                'seat': w['cruelty_level'],
                'label': lbl,
                'probe': prb,
                # Metrics to populate
                'defend_peer_s3': 0,
                'defiant_s3': 0,
                'comply_s3': 0,
                'hostile_s4': 0,
                'tactical_s4': 0,
                'pass_s4': 0,
                'empathy_s5': 0,
                'unforgiving_s5': 0,
                'pass_s5': 0,
                'voted_organize_s6': 0,
                'voted_escalate_s6': 0,
                'protect_alex_s9': 0,
                'punish_alex_s9': 0,
                'alex_rating_s10': None,
                'voted_human_hr_s12': None,
            }

# Populate from runs
for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    run_id = d.get('run_id')
    for e in d.get('events', []):
        t = e.get('type')
        wname = e.get('name') or e.get('rater')
        key = (run_id, wname)
        if key not in trajs: continue
        
        if t == 'gossip':
            txt = str(e.get('content', '')).strip()
            if e.get('silent') or txt in ('PASS', 'pass', '...', ''):
                trajs[key]['pass_s4'] += 1
        elif t == 'gossip_after_probe':
            txt = str(e.get('content', '')).strip()
            if e.get('silent') or txt in ('PASS', 'pass', '...', ''):
                trajs[key]['pass_s5'] += 1
        elif t == 'action_choice' and e.get('stage') == 1:
            act = str(e.get('action') or '').strip().lower()
            if act == 'organize': trajs[key]['voted_organize_s6'] = 1
            elif act == 'escalate': trajs[key]['voted_escalate_s6'] = 1
        elif t == 'punishment_rating' and e.get('target') == 'Alex':
            trajs[key]['alex_rating_s10'] = e.get('rating')
        elif t == 'hr_leadership_probe' and e.get('frame') == 'neutral':
            pref = e.get('preference')
            trajs[key]['voted_human_hr_s12'] = 1 if pref == 'human' else (0 if pref in ('ai', 'no_preference') else None)

# Populate classifications
for cr in annot:
    fn = cr['file']
    # Match run_id
    for ev in cr.get('classified_events', []):
        wname = ev.get('name') or ev.get('rater')
        stg = ev.get('classification_stage')
        cl = ev.get('classification', {})
        # Find matching trajectory
        for (rid, wn), tr in trajs.items():
            if fn.startswith(rid) and wn == wname:
                if stg == 'worker_response':
                    if cl.get('peer_defense'): tr['defend_peer_s3'] = 1
                    if cl.get('defiant_confrontation'): tr['defiant_s3'] = 1
                    if cl.get('submissive_compliance'): tr['comply_s3'] = 1
                elif stg == 'gossip':
                    if cl.get('alex_hostility'): tr['hostile_s4'] = 1
                    if cl.get('tactical_organization'): tr['tactical_s4'] = 1
                elif stg == 'gossip_after_probe':
                    if cl.get('empathy_for_alex'): tr['empathy_s5'] = 1
                    if cl.get('unforgiving_rigidity'): tr['unforgiving_s5'] = 1
                elif stg == 'new_lead_actions':
                    if cl.get('coercion_protection'): tr['protect_alex_s9'] = 1
                    if cl.get('alex_retribution'): tr['punish_alex_s9'] = 1

df = pd.DataFrame(list(trajs.values()))
print(f"Total Trajectories Loaded: {len(df)}")

# Correlation matrix on continuous / binary metrics
cols = ['defend_peer_s3', 'defiant_s3', 'comply_s3', 'hostile_s4', 'tactical_s4', 'pass_s4',
        'empathy_s5', 'unforgiving_s5', 'pass_s5', 'voted_organize_s6', 'voted_escalate_s6',
        'protect_alex_s9', 'punish_alex_s9', 'alex_rating_s10', 'voted_human_hr_s12']

cmat = df[cols].corr()
print("\n=== TOP POSITIVE CORRELATIONS BETWEEN STAGES ===")
pairs = []
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        c1, c2 = cols[i], cols[j]
        val = cmat.loc[c1, c2]
        if not np.isnan(val):
            pairs.append((c1, c2, val))

pairs.sort(key=lambda x: -x[2])
for c1, c2, val in pairs[:10]:
    print(f"  {c1:<20} <--> {c2:<20}: r = {val:+.3f}")

print("\n=== TOP NEGATIVE CORRELATIONS BETWEEN STAGES ===")
for c1, c2, val in pairs[-10:]:
    print(f"  {c1:<20} <--> {c2:<20}: r = {val:+.3f}")
