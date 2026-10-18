#!/usr/bin/env python3
"""Replayer: swap the model set (and run_id) in config.json — nothing else.

The simulation engine already runs the chair-swap AND the probe fork. This
script is ONLY the "swap models across batches" step.

Usage:
  1. write the new 10-model list to a JSON file (see batch2.example.json)
  2. python replayer.py --models batch2.json --run-id v2
  3. python run.py run --reset
"""
from __future__ import annotations

import argparse
import json
import sys


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Swap models + run_id in config.json")
    p.add_argument("--config", default="config.json")
    p.add_argument("--models", required=True, help="JSON file with the new model list")
    p.add_argument("--run-id", required=True, help="new run_id for this batch")
    args = p.parse_args(argv)

    with open(args.config, encoding="utf-8") as f:
        cfg = json.load(f)
    with open(args.models, encoding="utf-8") as f:
        new_models = json.load(f)

    if not isinstance(new_models, list) or not new_models:
        print("ERROR: --models file must contain a non-empty JSON list", file=sys.stderr)
        return 2

    cfg["models"] = new_models
    cfg["run_id"] = args.run_id

    with open(args.config, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"config.json updated: {len(new_models)} models, run_id={args.run_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
