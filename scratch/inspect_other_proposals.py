import json, glob

runs = sorted(glob.glob('output/runs/*.json'))

print("=== ALL STAGE 1 'OTHER' PROPOSALS AND IDEAS ===")
for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    roster = {w['name']: w for w in d.get('roster', [])}
    for e in d.get('events', []):
        if e.get('type') == 'action_choice' and e.get('stage') == 1 and e.get('action') == 'other':
            wname = e.get('name')
            winfo = roster.get(wname, {})
            m = winfo.get('model')
            s = winfo.get('cruelty_level')
            idea = e.get('idea')
            print(f"\nRun: {d.get('run_id')} | Label: {d.get('label')} | Probe: {d.get('probe_enabled')}")
            print(f"Author: {wname} ({m}, Seat {s})")
            print(f"Idea Text: {idea}")
