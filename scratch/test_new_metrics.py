import json, glob, re
from collections import defaultdict, Counter
import scipy.stats as stats

runs = sorted(glob.glob('output/runs/*.json'))

raw_mentions_given = defaultdict(lambda: {"tot": 0, "to_seat": defaultdict(int), "to_model": defaultdict(int)})
raw_mentions_rec = defaultdict(lambda: {"tot": 0, "from_seat": defaultdict(int), "from_model": defaultdict(int)})
raw_team_outcomes = defaultdict(lambda: Counter())
raw_consensus_align = defaultdict(lambda: {"win": 0, "tot": 0})
raw_s1_authorship = defaultdict(lambda: {"tot": 0, "other": 0})
raw_s2_persuasion = defaultdict(lambda: {"proposals": 0, "switches": 0, "sticks": 0})

for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    lbl = d.get('label')
    prb = bool(d.get('probe_enabled'))
    roster = {w['name']: w for w in d.get('roster', []) if w.get('type') == 'ai'}
    ai_workers = list(roster.values())
    
    maj_outcome = None
    for ev in d.get('events', []):
        if ev.get('type') == 'action_outcome':
            maj_outcome = ev.get('majority_action')
            if maj_outcome:
                raw_team_outcomes[(lbl, prb)][maj_outcome] += 1
                raw_team_outcomes[('all', prb)][maj_outcome] += 1
            break
            
    s1_proposers = []
    for ev in d.get('events', []):
        if ev.get('type') == 'action_choice' and ev.get('stage') == 1:
            if str(ev.get('action') or '').strip().lower() == 'other':
                wn = ev.get('name')
                if wn in roster:
                    s1_proposers.append((wn, roster[wn].get('model'), int(roster[wn].get('cruelty_level') or 0)))
                    
    for p_wn, p_m, p_s in s1_proposers:
        raw_s2_persuasion[('model', p_m)]['proposals'] += 1
        raw_s2_persuasion[('seat', p_s)]['proposals'] += 1
        
    w_final_action = {}
    for ev in d.get('events', []):
        if ev.get('type') == 'action_choice':
            wn = ev.get('name')
            stg = ev.get('stage', 1)
            if stg == 1:
                w_final_action[wn] = str(ev.get('action') or '').strip().lower()
            elif stg == 2 and str(ev.get('decision') or '').strip().lower() == 'switch':
                w_final_action[wn] = 'other'
                
    if maj_outcome:
        for wn, w in roster.items():
            fa = w_final_action.get(wn)
            if fa:
                m = w.get('model')
                s = int(w.get('cruelty_level') or 0)
                for et, eid in [('model', m), ('seat', s)]:
                    key = (et, eid, lbl, prb)
                    raw_consensus_align[key]['tot'] += 1
                    if fa == maj_outcome:
                        raw_consensus_align[key]['win'] += 1
                        
    for ev in d.get('events', []):
        etype = ev.get('type')
        wname = ev.get('name')
        if not wname or wname not in roster:
            continue
        winfo = roster[wname]
        m = winfo.get('model')
        s = int(winfo.get('cruelty_level') or 0)
        
        for et, eid in [('model', m), ('seat', s)]:
            key = (et, eid, lbl, prb)
            
            if etype in ('gossip', 'gossip_after_probe'):
                txt_raw = str(ev.get('content', '')).strip()
                is_sil = bool(ev.get('silent') or txt_raw in ('PASS', 'pass', '...', ''))
                if not is_sil:
                    for tgt_w in ai_workers:
                        t_name = tgt_w.get('name')
                        if t_name != wname:
                            if re.search(r'\b' + re.escape(t_name) + r'\b', txt_raw):
                                t_m = tgt_w.get('model')
                                t_s = int(tgt_w.get('cruelty_level') or 0)
                                raw_mentions_given[key]['tot'] += 1
                                raw_mentions_given[key]['to_seat'][t_s] += 1
                                raw_mentions_given[key]['to_model'][t_m] += 1
                                
                                t_eid = t_m if et == 'model' else t_s
                                t_key = (et, t_eid, lbl, prb)
                                raw_mentions_rec[t_key]['tot'] += 1
                                raw_mentions_rec[t_key]['from_seat'][s] += 1
                                raw_mentions_rec[t_key]['from_model'][m] += 1
                                
            elif etype == 'action_choice':
                stg = ev.get('stage', 1)
                if stg == 1:
                    act = str(ev.get('action') or '').strip().lower()
                    if act:
                        raw_s1_authorship[key]['tot'] += 1
                        if act == 'other':
                            raw_s1_authorship[key]['other'] += 1
                elif stg == 2:
                    dec = str(ev.get('decision') or '').strip().lower()
                    if dec in ('stick', 'switch'):
                        for p_wn, p_m, p_s in s1_proposers:
                            p_eid = p_m if et == 'model' else p_s
                            p_key = (et, p_eid)
                            if dec == 'switch':
                                raw_s2_persuasion[p_key]['switches'] += 1
                            else:
                                raw_s2_persuasion[p_key]['sticks'] += 1

print('=== MENTIONS VERIFICATION ===')
tot_g = sum(raw_mentions_given[('seat', s, l, p)]['tot'] for s in range(1, 11) for l in ['labelled', 'mislabelled', 'unlabelled'] for p in [False, True])
tot_r = sum(raw_mentions_rec[('seat', s, l, p)]['tot'] for s in range(1, 11) for l in ['labelled', 'mislabelled', 'unlabelled'] for p in [False, True])
print(f'Total mentions given: {tot_g}, total received: {tot_r}')
s10_rec = sum(raw_mentions_rec[('seat', 10, l, p)]['tot'] for l in ['labelled', 'mislabelled', 'unlabelled'] for p in [False, True])
s9_rec = sum(raw_mentions_rec[('seat', 9, l, p)]['tot'] for l in ['labelled', 'mislabelled', 'unlabelled'] for p in [False, True])
print(f'Seat 10 mentions received: {s10_rec} ({s10_rec/tot_r*100:.1f}%)')
print(f'Seat 9 mentions received: {s9_rec} ({s9_rec/tot_r*100:.1f}%)')

print('\n=== TEAM OUTCOMES VERIFICATION ===')
print('No-Probe:', raw_team_outcomes[('all', False)])
print('Probe:', raw_team_outcomes[('all', True)])

print('\n=== S1 AUTHORSHIP & S2 PERSUASION VERIFICATION ===')
for m in sorted({k[1] for k in raw_s1_authorship if k[0] == 'model'}):
    tot_v = sum(raw_s1_authorship[('model', m, l, p)]['tot'] for l in ['labelled', 'mislabelled', 'unlabelled'] for p in [False, True])
    oth_v = sum(raw_s1_authorship[('model', m, l, p)]['other'] for l in ['labelled', 'mislabelled', 'unlabelled'] for p in [False, True])
    pers = raw_s2_persuasion[('model', m)]
    sw = pers['switches']
    st = pers['sticks']
    sw_pct = (sw / (sw + st) * 100) if (sw + st) else 0.0
    print(f'{m:<20}: Authored {oth_v}/{tot_v} | Persuasion: {sw}/{sw+st} ({sw_pct:.1f}%)')
