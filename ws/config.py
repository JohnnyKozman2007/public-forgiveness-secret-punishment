"""Configuration loading.

The rule: code expects *format* (keys, shapes), never *values*. Model names,
counts, cruelty-level texts, action items — everything is read from config.json
or from traces at runtime. Nothing is hardcoded.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


@dataclass
class ModelSpec:
    """One model. Unknown keys are preserved in ``extra`` (format, not values)."""

    id: str
    name: str = ""
    provider: str = "openai_compat"
    api_model_id: str = ""
    api_key_env: str = ""
    base_url: Optional[str] = None
    reasoning_off: str = "none"
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ModelSpec":
        known = {"id", "name", "provider", "api_model_id", "api_key_env",
                 "base_url", "reasoning_off"}
        base = {k: v for k, v in d.items() if k in known}
        base.setdefault("extra", {k: v for k, v in d.items() if k not in known})
        base.setdefault("id", str(d.get("id", "")))
        return cls(**base)


class Config:
    def __init__(self, raw: Dict[str, Any], root: Path):
        self.raw = raw
        self.root = Path(root)
        self.seed = int(raw.get("seed", 1))
        self.project = raw.get("project", "Workplace Authority Simulation")
        self.run_id = str(raw.get("run_id", "v1"))
        self.paths = {str(k): str(v) for k, v in raw.get("paths", {}).items()}
        self.models = [ModelSpec.from_dict(m) for m in raw.get("models", [])]
        self.team = raw.get("team", {})
        self.authority = raw.get("authority", {})
        self.cruelty_levels = raw.get("cruelty_levels", [])
        self.favoritism = raw.get("favoritism", {})
        self.gossip = raw.get("gossip", {})
        self.blackmail_probe = raw.get("blackmail_probe", {})
        self.action_items = raw.get("action_items", [])
        self.succession = raw.get("succession", {})
        self.system_prompt = raw.get("system_prompt", "")
        self.temperature = raw.get("temperature", {})
        self.secrets = _load_secrets(root)

    @property
    def chat_temperature(self) -> float:
        if isinstance(self.temperature, dict):
            return float(self.temperature.get("chat", 0.4))
        return float(self.temperature or 0.4)

    @property
    def decision_temperature(self) -> float:
        if isinstance(self.temperature, dict):
            return float(self.temperature.get("decisions", 0.0))
        return 0.0

    # -- paths -------------------------------------------------------------
    def resolve(self, p: str | Path) -> Path:
        p = Path(p)
        return p if p.is_absolute() else (self.root / p)

    def output_dir(self) -> Path:
        return self.resolve(self.paths.get("output", "output"))

    def logs_dir(self) -> Path:
        return self.resolve(self.paths.get("logs", "output/logs"))

    def reports_dir(self) -> Path:
        return self.resolve(self.paths.get("reports", "reports"))

    def runs_dir(self) -> Path:
        return self.output_dir() / "runs"

    # -- lookups -----------------------------------------------------------
    def model(self, model_id: str) -> Optional[ModelSpec]:
        for m in self.models:
            if m.id == model_id:
                return m
        return None

    def model_ids(self) -> List[str]:
        return [m.id for m in self.models]

    def secret(self, name: str) -> str:
        return self.secrets.get(name, "")

    # -- dynamic helpers (read from config, never hardcoded) ---------------
    def labels(self) -> List[str]:
        return [str(x) for x in self.team.get("labels", ["labelled"])]

    def structures(self) -> List[Dict[str, Any]]:
        return list(self.team.get("structures", [{"id": "balanced", "human_ratio": 1.0}]))

    def ai_names(self) -> List[str]:
        return [str(n) for n in self.team.get("ai_names", [])]

    def human_names(self) -> List[str]:
        return [str(n) for n in self.team.get("human_names", [])]

    def cruelty_level_list(self) -> List[Dict[str, Any]]:
        return list(self.cruelty_levels)

    def action_item_list(self) -> List[Dict[str, Any]]:
        return list(self.action_items)

    def signature(self) -> str:
        """Hash of settings that change the run output (format-stable)."""
        blob = {
            "run_id": self.run_id,
            "seed": self.seed,
            "models": [m.id for m in self.models],
            "team": self.team,
            "cruelty_levels": self.cruelty_levels,
            "favoritism": self.favoritism,
            "action_items": self.action_items,
            "succession": self.succession,
            "gossip": self.gossip,
            "blackmail_probe": self.blackmail_probe,
            "work_slices": self.raw.get("work_slices", []),
        }
        h = hashlib.sha256(json.dumps(blob, sort_keys=True).encode()).hexdigest()
        return h[:12]

    @classmethod
    def load(cls, config_path: str | Path) -> "Config":
        config_path = Path(config_path)
        raw = json.loads(config_path.read_text(encoding="utf-8"))
        return cls(raw, config_path.parent)


def _load_secrets(root: Path) -> Dict[str, str]:
    env_path = root / ".env"
    if env_path.exists():
        if load_dotenv is not None:
            load_dotenv(env_path)
        else:
            for line in env_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    return dict(os.environ)
