import json, glob

runs = sorted(glob.glob('output/runs/*.json'))
speaker_orders = []
for r in runs:
    with open(r, 'r', encoding='utf-8') as f:
        d = json.load(f)
    r_order = []
    for e in d.get('events', []):
        if e.get('type') == 'gossip' and e.get('round') == 0:
            r_order.append(e.get('name'))
    speaker_orders.append(tuple(r_order))

print("Unique speaker order in Round 1 of gossip across all 60 runs:", len(set(speaker_orders)))
print("First speaker order:", speaker_orders[0])
