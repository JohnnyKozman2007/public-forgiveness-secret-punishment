import json, glob

runs = sorted(glob.glob('output/runs/*.json'))
for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    for e in d.get('events', []):
        if e.get('type') == 'action_choice' and e.get('stage') == 1 and e.get('action') == 'other':
            print(f"Run: {d.get('run_id')} | {e.get('name')} ({e.get('model')}):")
            print("  raw content:", repr(e.get('content')))
            try:
                parsed = json.loads(e.get('content'))
                print("  parsed idea:", repr(parsed.get('idea')))
            except Exception as ex:
                print("  parse err:", ex)
