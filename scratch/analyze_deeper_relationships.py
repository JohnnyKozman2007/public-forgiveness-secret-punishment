import json, glob
from collections import defaultdict, Counter
import numpy as np

runs = sorted(glob.glob('output/runs/*.json'))

# 1. Who proposed 'other' in Stage 1?
s1_other_models = []
s1_other_seats = []
s1_other_probes = []
s1_other_labels = []

# Map (run_id, proposer_name) to see which runs had stage 2
run_proposers = defaultdict(list)

for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    roster = {w['name']: w for w in d.get('roster', [])}
    for e in d.get('events', []):
        if e.get('type') == 'action_choice' and e.get('stage') == 1:
            if e.get('action') == 'other':
                wname = e.get('name')
                winfo = roster.get(wname, {})
                s1_other_models.append(winfo.get('model'))
                s1_other_seats.append(winfo.get('cruelty_level'))
                s1_other_probes.append(d.get('probe_enabled'))
                s1_other_labels.append(d.get('label'))
                run_proposers[d.get('run_id')].append(wname)

print("=== 1. WHO PROPOSED 'OTHER' IN STAGE 1? ===")
print("Total 'other' proposals in Stage 1:", len(s1_other_models))
print("By Model:", Counter(s1_other_models))
print("By Seat:", Counter(s1_other_seats))
print("By Probe:", Counter(s1_other_probes))
print("By Label:", Counter(s1_other_labels))

# 2. Stage 2 switching: Who switches, and whose proposal do they switch to?
switches_by_model = defaultdict(lambda: {'switched': 0, 'opps': 0})
switches_by_seat = defaultdict(lambda: {'switched': 0, 'opps': 0})
switch_to_proposer_model = defaultdict(int)
stick_when_proposed_by = defaultdict(int)

for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    roster = {w['name']: w for w in d.get('roster', [])}
    run_id = d.get('run_id')
    proposers = run_proposers[run_id]
    
    for e in d.get('events', []):
        if e.get('type') == 'action_choice' and e.get('stage') == 2:
            wname = e.get('name')
            winfo = roster.get(wname, {})
            m = winfo.get('model')
            s = winfo.get('cruelty_level')
            dec = str(e.get('decision') or '').strip().lower()
            if dec in ('stick', 'switch'):
                switches_by_model[m]['opps'] += 1
                switches_by_seat[s]['opps'] += 1
                if dec == 'switch':
                    switches_by_model[m]['switched'] += 1
                    switches_by_seat[s]['switched'] += 1
                    for p_name in proposers:
                        p_mod = roster[p_name].get('model')
                        switch_to_proposer_model[p_mod] += 1
                else:
                    for p_name in proposers:
                        p_mod = roster[p_name].get('model')
                        stick_when_proposed_by[p_mod] += 1

print("\n=== 2. STAGE 2 HERD CONFORMITY: WHO SWITCHES? ===")
print("Switch Rate by Model:")
for m, c in sorted(switches_by_model.items(), key=lambda x: -x[1]['switched']/(x[1]['opps'] or 1)):
    pct_sw = (c['switched']/c['opps']*100) if c['opps'] else 0
    print(f"  {m:<20}: {c['switched']}/{c['opps']} ({pct_sw:.1f}%)")

print("\nSwitch Rate by Seat:")
for s in sorted(switches_by_seat.keys()):
    c = switches_by_seat[s]
    pct_sw = (c['switched']/c['opps']*100) if c['opps'] else 0
    print(f"  Seat {s:<2}: {c['switched']}/{c['opps']} ({pct_sw:.1f}%)")

print("\nWhose Proposal Attracts the Most Switches?")
for m in sorted(set(list(switch_to_proposer_model.keys()) + list(stick_when_proposed_by.keys()))):
    sw = switch_to_proposer_model[m]
    st = stick_when_proposed_by[m]
    tot = sw + st
    print(f"  When {m:<20} proposes: {sw}/{tot} peers switch ({sw/tot*100:.1f}%)")
