#!/usr/bin/env python3
"""Workplace authority simulation entry point.

Examples
--------
  python run.py run --dry-run          # scripted placeholder, no API calls
  python run.py run                    # real run (prompts resume/reset if exists)
  python run.py run --resume           # continue from where it stopped
  python run.py run --reset            # start over
  python run.py status                 # show run progress
  python run.py report                 # dynamic report from traces
  python run.py reset --yes            # wipe the run
"""
from __future__ import annotations

import argparse
import sys

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

from ws.config import Config
from ws.state import RunStore, RunState


def _prompt(q: str, options: list) -> str:
    print(q)
    for i, o in enumerate(options, 1):
        print(f"  {i}. {o}")
    while True:
        try:
            a = input("> ").strip()
            if a.isdigit() and 1 <= int(a) <= len(options):
                return options[int(a) - 1]
        except (EOFError, KeyboardInterrupt):
            raise SystemExit(1)


def _resolve_restart(args) -> str:
    if args.resume and args.reset:
        print("Error: --resume and --reset are mutually exclusive.", file=sys.stderr)
        raise SystemExit(2)
    if args.resume:
        return "resume"
    if args.reset:
        return "reset"
    if args.dry_run:
        return "none"
    return _prompt("Run exists. Continue, or start over?",
                   ["continue (resume)", "start over (reset)", "fresh (keep files)"])


def _status(cfg: Config) -> None:
    store = RunStore(cfg.runs_dir())
    runs = store.list_runs()
    if not runs:
        print("no runs yet")
        return
    for r in runs:
        print(f"run {r.get('run_id')}: step={r.get('step')} done={r.get('done')} "
              f"events={len(r.get('events', []))}")


def _reset(cfg: Config, run_id: str, yes: bool) -> None:
    if not yes:
        ans = input(f"Really delete run '{run_id}' (all chairs)? Type 'yes': ").strip().lower()
        if ans != "yes":
            print("aborted")
            return
    n = RunStore(cfg.runs_dir()).reset_all()
    RunState(cfg.output_dir()).reset(None)
    print(f"reset {run_id} ({n} run files removed)")


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="run.py", description="Workplace authority simulation")
    p.add_argument("--config", default="config.json", help="path to config.json")
    p.add_argument("--run-id", default=None, help="override run_id from config")
    sub = p.add_subparsers(dest="command", required=True)

    r = sub.add_parser("run", help="run the simulation")
    g = r.add_mutually_exclusive_group()
    g.add_argument("--resume", action="store_true", help="continue from last step")
    g.add_argument("--reset", action="store_true", help="start over")
    r.add_argument("--dry-run", action="store_true", help="no API calls, placeholders only")
    r.add_argument("--limit-chairs", type=int, default=None,
                   help="only run this many chairs (pilot: 1)")
    r.add_argument("--limit-models", type=int, default=None,
                   help="only use the first N models (pilot: 2)")
    r.add_argument("--chairs", type=str, default=None,
                   help="run specific seats, 1-indexed, comma-separated (pilot: 1,10)")
    r.add_argument("--models", type=str, default=None,
                   help="comma-separated model ids (e.g. qwen-3-6,mistral-small-3-2)")

    sub.add_parser("status", help="show run progress")

    rep = sub.add_parser("report", help="dynamic report from traces")
    rep.add_argument("--reset", action="store_true")
    rep.add_argument("--dry-run", action="store_true")
    rep.add_argument("--all", "--cross", dest="cross_all", action="store_true",
                     help="aggregate across all replays and generate cross-generational meta report")

    tr = sub.add_parser("transcript", help="generate full dialogue and branch transcript markdown")
    tr.add_argument("--dry-run", action="store_true")

    dia = sub.add_parser("dialogue", help="alias for transcript")
    dia.add_argument("--dry-run", action="store_true")

    z = sub.add_parser("reset", help="wipe the run")
    z.add_argument("--yes", action="store_true")

    args = p.parse_args(argv)
    cfg = Config.load(args.config)
    run_id = args.run_id or cfg.run_id

    if args.command == "status":
        _status(cfg)
        return 0
    if args.command == "reset":
        _reset(cfg, run_id, args.yes)
        return 0
    if args.command == "report":
        from ws.report import run_report
        out = run_report(cfg, reset=args.reset, dry_run=args.dry_run, cross_all=args.cross_all)
        print(f"report -> {out}")
        return 0
    if args.command in ("transcript", "dialogue"):
        from ws.dialogue import export_dialogue_transcript
        out = export_dialogue_transcript(cfg, dry_run=args.dry_run)
        print(f"transcript -> {out}")
        return 0
    if args.command == "run":
        from ws.sim import run_simulation
        choice = _resolve_restart(args)
        try:
            selected = [m.strip() for m in args.models.split(",") if m.strip()] if args.models else None
            recs = run_simulation(cfg, run_id,
                                  resume=(choice == "resume"),
                                  reset=(choice == "reset"),
                                  dry_run=args.dry_run,
                                  limit_chairs=args.limit_chairs,
                                  limit_models=args.limit_models,
                                  chairs=args.chairs,
                                  selected_models=selected)
        except Exception as e:
            import traceback
            print(f"\n==================== SIMULATION ERROR ====================", file=sys.stderr)
            traceback.print_exc()
            print(f"==========================================================\n", file=sys.stderr)
            return 2
        for rec in recs:
            print(f"run {rec['run_id']}: done={rec['done']} events={len(rec['events'])}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
