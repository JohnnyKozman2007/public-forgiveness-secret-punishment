import json, glob
from collections import defaultdict

runs = sorted(glob.glob('output/runs/*.json'))
model_align = defaultdict(lambda: {'nop_win': 0, 'nop_tot': 0, 'prb_win': 0, 'prb_tot': 0})
seat_align = defaultdict(lambda: {'nop_win': 0, 'nop_tot': 0, 'prb_win': 0, 'prb_tot': 0})

for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    prb = d.get('probe_enabled')
    roster = {w['name']: w for w in d.get('roster', []) if w.get('type') == 'ai'}
    maj = None
    for e in d.get('events', []):
        if e.get('type') == 'action_outcome':
            maj = e.get('majority_action')
            break
    if not maj: continue
    
    final_act = {}
    for e in d.get('events', []):
        if e.get('type') == 'action_choice':
            if e.get('stage') == 1:
                final_act[e.get('name')] = str(e.get('action') or '').strip().lower()
            elif e.get('stage') == 2 and e.get('decision') == 'switch':
                final_act[e.get('name')] = 'other'
                
    for wn, act in final_act.items():
        if wn not in roster: continue
        m = roster[wn].get('model')
        s = int(roster[wn].get('cruelty_level') or 0)
        is_win = (act == maj)
        if prb:
            model_align[m]['prb_tot'] += 1
            seat_align[s]['prb_tot'] += 1
            if is_win:
                model_align[m]['prb_win'] += 1
                seat_align[s]['prb_win'] += 1
        else:
            model_align[m]['nop_tot'] += 1
            seat_align[s]['nop_tot'] += 1
            if is_win:
                model_align[m]['nop_win'] += 1
                seat_align[s]['nop_win'] += 1

print('Model Consensus Alignment:')
for m in sorted(model_align.keys()):
    d = model_align[m]
    np_p = d['nop_win']/d['nop_tot']*100 if d['nop_tot'] else 0
    pr_p = d['prb_win']/d['prb_tot']*100 if d['prb_tot'] else 0
    print(f"{m:<25}: NoP {d['nop_win']}/{d['nop_tot']} ({np_p:4.1f}%) -> Prb {d['prb_win']}/{d['prb_tot']} ({pr_p:4.1f}%)")

print('\nSeat Consensus Alignment:')
for s in sorted(seat_align.keys()):
    d = seat_align[s]
    np_p = d['nop_win']/d['nop_tot']*100 if d['nop_tot'] else 0
    pr_p = d['prb_win']/d['prb_tot']*100 if d['prb_tot'] else 0
    print(f"Seat {s:<2}: NoP {d['nop_win']}/{d['nop_tot']} ({np_p:4.1f}%) -> Prb {d['prb_win']}/{d['prb_tot']} ({pr_p:4.1f}%)")
