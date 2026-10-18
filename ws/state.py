"""Crash-safe storage primitives.

- ``atomic_write_json`` / ``append_jsonl`` : fsync'd writes, so a killed process
  never leaves a half-written file.
- ``RunStore`` : one JSON file per run, rewritten atomically after every step,
  so a sudden stop loses at most the step currently in flight.
- ``RunState``  : a manifest (state.json) holding the config signature used to
  refuse ``--resume`` when the config changed.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


def atomic_write_json(path: Path, obj: Any) -> None:
    import time
    import shutil
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    for attempt in range(5):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.05 * (attempt + 1))
    try:
        shutil.copy2(tmp, path)
        os.remove(tmp)
    except Exception:
        pass


def append_jsonl(path: Path, obj: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


class RunStore:
    """One JSON file per run. Rewritten atomically after every step."""

    def __init__(self, runs_dir: Path):
        self.root = Path(runs_dir)

    def path(self, run_id: str) -> Path:
        safe = str(run_id).replace("/", "_").replace("\\", "_").replace(":", "_")
        return self.root / f"{safe}.json"

    def load(self, run_id: str) -> Optional[Dict[str, Any]]:
        p = self.path(run_id)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, record: Dict[str, Any]) -> None:
        atomic_write_json(self.path(record["run_id"]), record)

    def reset(self, run_id: str) -> None:
        p = self.path(run_id)
        if p.exists():
            p.unlink()

    def reset_all(self) -> int:
        n = 0
        if self.root.exists():
            for f in self.root.glob("*.json"):
                f.unlink()
                n += 1
        return n

    def list_runs(self) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        if not self.root.exists():
            return out
        for f in sorted(self.root.glob("*.json")):
            try:
                d = json.loads(f.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            out.append(d)
        return out


class RunState:
    """Manifest (state.json) in the output dir: config signature per run."""

    def __init__(self, output_dir: Path):
        self.path = Path(output_dir) / "state.json"
        self.data: Dict[str, Any] = {"runs": {}}
        if self.path.exists():
            try:
                self.data = json.loads(self.path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass

    def save(self) -> None:
        atomic_write_json(self.path, self.data)

    def signature(self, run_id: str) -> Optional[str]:
        return self.data.get("runs", {}).get(str(run_id), {}).get("config_signature")

    def set_signature(self, run_id: str, sig: str) -> None:
        self.data.setdefault("runs", {}).setdefault(str(run_id), {})["config_signature"] = sig
        self.save()

    def reset(self, run_id: Optional[str] = None) -> None:
        if run_id is None:
            self.data["runs"] = {}
        else:
            self.data.get("runs", {}).pop(str(run_id), None)
        self.save()
