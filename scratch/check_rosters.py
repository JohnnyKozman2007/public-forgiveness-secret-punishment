import json, glob

runs = sorted(glob.glob('output/runs/*.json'))
print('Total runs found:', len(runs))

for idx in [0, 1, 2, 5, 10, 20]:
    with open(runs[idx], 'r', encoding='utf-8') as f:
        d = json.load(f)
    print(f"Run {idx} ({d.get('run_id')} - label={d.get('label')}, probe={d.get('probe_enabled')}):")
    ai_workers = [w for w in d['roster'] if w.get('type') == 'ai']
    for w in ai_workers:
        print(f"  {w['name']:<8} Seat={w['cruelty_level']:<2} Model={w['model']}")
    print("-" * 50)
