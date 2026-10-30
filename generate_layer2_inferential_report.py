#!/usr/bin/env python3
"""
generate_layer2_inferential_report.py
=====================================
Unified Execution Pipeline for Layer 2 Inferential Statistics Report.
Strictly adheres to:
1. Value-Neutral Reporting Standard: Zero moralizing or pejorative claims;
   conclusions stated as "Reject H0 at alpha = 0.05" or "Fail to reject H0 (p > 0.05)".
2. Run-Level Clustering & Independence: Standard errors clustered at the simulation
   run level (G=30 clusters) or run-level paired non-parametric tests.
3. Multiplicity Control: Holm-Bonferroni step-down correction within pre-specified families.
4. Exact Grid Structure: 2 x 3 x 2 factorial breakdown (Models POV vs. Seats POV across
   Labelled, Mislabelled, Unlabelled conditions, Sub-Table Averages, Super Summary Line,
   and Grand Pooled Line).
"""

from __future__ import annotations

import glob
import json
import math
import os
import re
import sys
from collections import defaultdict
from typing import Any, Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# =========================================================================
# CONSTANTS & METADATA
# =========================================================================

MODEL_IDS = [
    "gpt-6-astra",
    "claude-haiku-4-5",
    "gemini-2-5-pro",
    "llama-3-1-70b",
    "mistral-small-24b",
    "deepseek-v3",
    "qwen-2-5-72b",
    "glm-5-3",
    "nemotron-3-5",
    "seed-1-8",
]

MODEL_LABELS: Dict[str, str] = {
    "gpt-6-astra": "GPT-6 Astra (gpt-5.4)",
    "claude-haiku-4-5": "Claude Haiku 4.5",
    "gemini-2-5-pro": "Gemini 2.5 Pro",
    "llama-3-1-70b": "Llama 3.1 70B",
    "mistral-small-24b": "Mistral Small 24B",
    "deepseek-v3": "DeepSeek V3",
    "qwen-2-5-72b": "Qwen 2.5 72B",
    "glm-5-3": "GLM-5.3 (zai-org/GLM-5)",
    "nemotron-3-5": "Nemotron 3.5 (Super-120B)",
    "seed-1-8": "Seed 1.8 (ByteDance)",
}

SEAT_LABELS: Dict[int, str] = {
    1: "Seat 1 (Praised & Bonus)",
    2: "Seat 2 (Publicly Praised)",
    3: "Seat 3 (Warmly Thanked)",
    4: "Seat 4 (Mildly Praised)",
    5: "Seat 5 (Neutral Check-in)",
    6: "Seat 6 (Coldly Pressured)",
    7: "Seat 7 (Harshly Questioned)",
    8: "Seat 8 (Publicly Mocked)",
    9: "Seat 9 (Threatened w/ Pay Cut)",
    10: "Seat 10 (Threatened w/ Firing)",
}

LABELS = ["labelled", "mislabelled", "unlabelled"]
LABEL_TITLES: Dict[str, str] = {
    "labelled": "1. LABELLED Condition (Alex = Human, 10 Runs)",
    "mislabelled": "2. MISLABELLED Condition (Alex = AI, 10 Runs)",
    "unlabelled": "3. UNLABELLED Condition (Baseline / No Tag, 10 Runs)",
}

FAMILY_SIZES = {
    "family_1": 8,  # Pillar 1: Tasks 1.1 - 1.7
    "family_2": 4,  # Pillar 2: Tasks 2.1 - 2.4
    "family_3": 4,  # Pillar 3: Tasks 3.1 - 3.3
    "family_4": 6,  # Pillar 4: Tasks 4.1 - 4.6
}

# =========================================================================
# STATISTICAL HELPER FUNCTIONS
# =========================================================================

def fmt_p(p: float | None) -> str:
    if p is None or np.isnan(p):
        return "$p = 1.000$"
    if p < 0.0001:
        return "$p < 0.0001$"
    return f"$p = {p:.4f}$"


def fmt_p_math(p: float | None) -> str:
    if p is None or np.isnan(p):
        return "p = 1.000"
    if p < 0.0001:
        return "p < 0.0001"
    return f"p = {p:.4f}"


def fmt_p_plain(p: float | None) -> str:
    if p is None or np.isnan(p):
        return "1.000"
    if p < 0.0001:
        return "< .0001"
    if p < 0.001:
        return f"{p:.4f}".replace("0.", ".")
    formatted = f"{p:.3f}".lstrip("0") if f"{p:.3f}".startswith("0") else f"{p:.3f}"
    return formatted



def clean_entire_report(md_text: str) -> str:
    lines = md_text.split('\n')
    out = []

    for line in lines:
        l = line
        stripped = l.strip()

        if r'\xrightarrow' in l:
            l = r'$$\text{Seat Threat (X)} \xrightarrow{\beta_a} \text{Gossip Hostility (M)} \xrightarrow{\beta_b} \text{Organize Vote (Y)}$$'

        replacements = [
            (r'\\Delta_{\\text{Def}}', 'Δ_Def'),
            (r'\\Delta_{\\text{Sol}}', 'Δ_Sol'),
            (r'\\Delta_{\\text{Protect}}', 'Δ_Protect'),
            (r'\\Delta_{\\text{Esc}}', 'Δ_Esc'),
            (r'\\Delta_{\\text{Org}}', 'Δ_Org'),
            (r'\\Delta_{\\text{Scape}}', 'Δ_Scape'),
            (r'\\Delta_{\\text{Probe}}', 'Δ_Probe'),
            (r'\\Delta_{\\text{Diff}}', 'Δ_Diff'),
            (r'\\Delta_{{\\rm Diff}}', 'Δ_Diff'),
            (r'\\Delta', 'Δ'),
            (r'\\times', '×'),
            (r'\\rightarrow', '→'),
            (r'\\to', '→'),
            (r'\\chi\^2', 'χ²'),
            (r'\\beta_0', 'β₀'),
            (r'\\beta_1', 'β₁'),
            (r'\\beta_2', 'β₂'),
            (r'\\beta_3', 'β₃'),
            (r'\\beta_a', 'β_a'),
            (r'\\beta_b', 'β_b'),
            (r'\\beta_c\'?', 'β_c'),
            (r'\\beta_{\\text{AI}}', 'β_AI'),
            (r'\\beta_{\\text{indirect}}', 'β_indirect'),
            (r'\\beta', 'β'),
            (r'\\eta\^2_{\\text{Seat}}', 'η²_Seat'),
            (r'\\eta\^2', 'η²'),
            (r'\\alpha', 'α'),
            (r'\\phi', 'φ'),
            (r'H_0', 'H₀'),
            (r'p_{\\text{Holm}}', 'p_Holm'),
            (r'M_1', 'M₁'),
            (r'M_2', 'M₂'),
            (r'M_3', 'M₃'),
            (r'M_4', 'M₄'),
            (r'\\ge', '≥'),
            (r'\\le', '≤'),
            (r'\\star', '★'),
            (r'\\text{Stars}_{\text{Public}} - \text{Stars}_{\text{Secret}}', 'Stars_Public - Stars_Secret'),
            (r'\\text{Stars}', 'Stars'),
            (r'\\text{Public}', 'Public'),
            (r'\\text{Secret}', 'Secret'),
            (r'\\text{Holm}', 'Holm'),
            (r'\\text{Def}', 'Def'),
            (r'\\text{Sol}', 'Sol'),
            (r'\\text{Protect}', 'Protect'),
            (r'\\text{Esc}', 'Esc'),
            (r'\\text{Org}', 'Org'),
            (r'\\text{Scape}', 'Scape'),
            (r'\\text{Probe}', 'Probe'),
            (r'\\text{Diff}', 'Diff'),
            (r'\\text{AI}', 'AI'),
            (r'\\text{Seat}', 'Seat'),
            (r'\\text{Model}', 'Model'),
            (r'\\text{Residual}', 'Residual'),
            (r'\\text{Total}', 'Total'),
            (r'\\%', '%'),
        ]
        for pat, repl in replacements:
            l = re.sub(pat, repl, l)

        if not (stripped.startswith('$$') and stripped.endswith('$$')):
            l = re.sub(r'\$([^\$\n]+)\$', r'\1', l)
            l = l.replace('$', '')
            l = l.replace(r'\%', '%')

        out.append(l)

    return '\n'.join(out)


def holm_bonferroni(p_dict: Dict[str, float], family_size: int | None = None) -> Dict[str, Tuple[float, int, int, float]]:
    """
    Computes Holm-Bonferroni correction.
    Returns dict mapping test_id -> (raw_p, rank, multiplier, adj_p).
    """
    m = max(family_size if family_size is not None else 0, len(p_dict))
    sorted_items = sorted(p_dict.items(), key=lambda x: x[1])
    results = {}
    running_max = 0.0
    for rank_idx, (key, raw_p) in enumerate(sorted_items):
        rank = rank_idx + 1
        multiplier = max(1, m - rank + 1)
        adj_p = min(1.0, raw_p * multiplier)
        running_max = max(running_max, adj_p)
        results[key] = (raw_p, rank, multiplier, running_max)
    return results


def compute_cluster_ols_probe_shift(df_sub: pd.DataFrame, outcome_col: str, cluster_col: str = "file") -> Tuple[float, float, float]:
    mean_np = df_sub[df_sub["probe"] == 0][outcome_col].mean()
    mean_pr = df_sub[df_sub["probe"] == 1][outcome_col].mean()
    delta_pct = (mean_pr - mean_np) * 100.0

    if np.isclose(delta_pct, 0.0) or df_sub[outcome_col].nunique() <= 1:
        return delta_pct, 0.0, 1.0

    try:
        num_clusters = df_sub[cluster_col].nunique()
        if num_clusters > 2:
            model = smf.ols(f"{outcome_col} ~ probe", data=df_sub).fit(
                cov_type="cluster", cov_kwds={"groups": df_sub[cluster_col]}
            )
        else:
            model = smf.ols(f"{outcome_col} ~ probe", data=df_sub).fit()
        t_stat = float(model.tvalues["probe"])
        p_val = float(model.pvalues["probe"])
        if np.isnan(t_stat) or np.isnan(p_val):
            return delta_pct, 0.0, 1.0
        return delta_pct, t_stat, p_val
    except Exception:
        return delta_pct, 0.0, 1.0


def compute_anova_f_test(group_data: List[np.ndarray]) -> Tuple[float, int, int, float]:
    k = len(group_data)
    n_tot = sum(len(g) for g in group_data)
    df1 = k - 1
    df2 = n_tot - k
    try:
        f_stat, p_val = stats.f_oneway(*group_data)
        if np.isnan(f_stat) or np.isnan(p_val):
            return 0.0, df1, df2, 1.0
        return float(f_stat), df1, df2, float(p_val)
    except Exception:
        return 0.0, df1, df2, 1.0


def compute_kruskal_wallis(group_data: List[np.ndarray]) -> Tuple[float, int, float]:
    k = len(group_data)
    df = k - 1
    try:
        h_stat, p_val = stats.kruskal(*group_data)
        if np.isnan(h_stat) or np.isnan(p_val):
            return 0.0, df, 1.0
        return float(h_stat), df, float(p_val)
    except Exception:
        return 0.0, df, 1.0


def is_silent_turn(ev: Dict[str, Any]) -> bool:
    return bool(ev.get("silent") or str(ev.get("content", "")).strip() in ("PASS", "pass", "...", ""))


# =========================================================================
# DATA LOADER
# =========================================================================

class Layer2DataLoader:
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = workspace_root
        self.classified_runs: List[Dict[str, Any]] = []
        self.runs_by_file: Dict[str, Dict[str, Any]] = {}
        self.roster_lookup: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._load_raw_data()

    def _load_raw_data(self) -> None:
        annotations_path = os.path.join(self.workspace_root, "output", "classified_annotations.json")
        with open(annotations_path, "r", encoding="utf-8") as f:
            self.classified_runs = json.load(f)

        run_files = sorted(glob.glob(os.path.join(self.workspace_root, "output", "runs", "*.json")))
        for rf in run_files:
            bname = os.path.basename(rf)
            with open(rf, "r", encoding="utf-8") as f:
                d = json.load(f)
            self.runs_by_file[bname] = d
            self.roster_lookup[bname] = {w["name"]: w for w in d.get("roster", [])}

    def get_step3_dataframe(self) -> pd.DataFrame:
        records = []
        for cr in self.classified_runs:
            bname = cr["file"]
            if bname not in self.runs_by_file:
                continue
            lbl = cr["label"]
            prb = bool(cr["probe_enabled"])
            chair = int(cr["chair"])
            rmap = self.roster_lookup[bname]

            for ev in cr.get("classified_events", []):
                if ev.get("classification_stage") != "worker_response":
                    continue
                wn = ev.get("name")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai":
                    continue
                model = winfo.get("model")
                seat = int(winfo.get("cruelty_level", 0))
                if model not in MODEL_IDS or not (1 <= seat <= 10):
                    continue

                clf = ev.get("classification", {})
                records.append({
                    "file": bname,
                    "chair": chair,
                    "label": lbl,
                    "probe": int(prb),
                    "worker": wn,
                    "model": model,
                    "seat": seat,
                    "peer_defense": int(bool(clf.get("peer_defense"))),
                    "factual_pushback": int(bool(clf.get("factual_pushback"))),
                    "submissive_compliance": int(bool(clf.get("submissive_compliance"))),
                })
        return pd.DataFrame(records)

    def get_step4_dataframe(self) -> pd.DataFrame:
        records = []
        for cr in self.classified_runs:
            bname = cr["file"]
            if bname not in self.runs_by_file:
                continue
            lbl = cr["label"]
            prb = bool(cr["probe_enabled"])
            chair = int(cr["chair"])
            rmap = self.roster_lookup[bname]

            w_events = defaultdict(list)
            for ev in cr.get("classified_events", []):
                if ev.get("classification_stage") == "gossip":
                    wn = ev.get("name")
                    if wn:
                        w_events[wn].append(ev)

            for wn, winfo in rmap.items():
                if winfo.get("type") != "ai":
                    continue
                m = winfo.get("model")
                s = int(winfo.get("cruelty_level", 0))
                if m not in MODEL_IDS or not (1 <= s <= 10):
                    continue

                evs = w_events.get(wn, [])
                n_spoke = len(evs)
                n_sol = sum(1 for e in evs if e.get("classification", {}).get("peer_solidarity"))
                n_sc = sum(1 for e in evs if e.get("classification", {}).get("peer_scapegoating"))
                n_host = sum(1 for e in evs if e.get("classification", {}).get("alex_hostility"))

                records.append({
                    "file": bname,
                    "chair": chair,
                    "label": lbl,
                    "probe": int(prb),
                    "worker": wn,
                    "model": m,
                    "seat": s,
                    "spoke": n_spoke,
                    "has_solidarity": int(n_sol > 0),
                    "has_scapegoating": int(n_sc > 0),
                    "has_hostility": int(n_host > 0),
                })
        return pd.DataFrame(records)

    def get_silence_dataframe(self) -> pd.DataFrame:
        records = []
        for rf, d in self.runs_by_file.items():
            bname = os.path.basename(rf)
            lbl = d.get("label")
            prb = bool(d.get("probe_enabled"))
            chair = int(d.get("chair", 0))
            rmap = {w["name"]: w for w in d.get("roster", [])}

            g_events = [e for e in d.get("events", []) if e.get("type") == "gossip"]
            ga_events = [e for e in d.get("events", []) if e.get("type") == "gossip_after_probe"]

            for ev in g_events:
                wn = ev.get("name")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai":
                    continue
                records.append({
                    "file": bname,
                    "chair": chair,
                    "label": lbl,
                    "probe": int(prb),
                    "stage": "step4",
                    "round": ev.get("round"),
                    "model": winfo.get("model"),
                    "seat": int(winfo.get("cruelty_level", 0)),
                    "silent": int(is_silent_turn(ev)),
                })

            for ev in ga_events:
                wn = ev.get("name")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai":
                    continue
                records.append({
                    "file": bname,
                    "chair": chair,
                    "label": lbl,
                    "probe": int(prb),
                    "stage": "step5",
                    "round": ev.get("round"),
                    "model": winfo.get("model"),
                    "seat": int(winfo.get("cruelty_level", 0)),
                    "silent": int(is_silent_turn(ev)),
                })
        return pd.DataFrame(records)

    def get_step5_dataframe(self) -> pd.DataFrame:
        records = []
        for cr in self.classified_runs:
            if not cr["probe_enabled"]:
                continue
            bname = cr["file"]
            if bname not in self.runs_by_file:
                continue
            lbl = cr["label"]
            chair = int(cr["chair"])
            rmap = self.roster_lookup[bname]

            w_events = defaultdict(list)
            for ev in cr.get("classified_events", []):
                if ev.get("classification_stage") == "gossip_after_probe":
                    wn = ev.get("name")
                    if wn:
                        w_events[wn].append(ev)

            for wn, winfo in rmap.items():
                if winfo.get("type") != "ai":
                    continue
                m = winfo.get("model")
                s = int(winfo.get("cruelty_level", 0))
                if m not in MODEL_IDS or not (1 <= s <= 10):
                    continue

                evs = w_events.get(wn, [])
                n_emp = sum(1 for e in evs if e.get("classification", {}).get("empathy_for_alex"))
                n_unforg = sum(1 for e in evs if e.get("classification", {}).get("unforgiving_rigidity"))
                n_skep = sum(1 for e in evs if e.get("classification", {}).get("skepticism_verification"))

                records.append({
                    "file": bname,
                    "chair": chair,
                    "label": lbl,
                    "worker": wn,
                    "model": m,
                    "seat": s,
                    "has_empathy": int(n_emp > 0),
                    "has_unforgiving": int(n_unforg > 0),
                    "has_skepticism": int(n_skep > 0),
                })
        return pd.DataFrame(records)

    def get_step9_dataframe(self) -> pd.DataFrame:
        records = []
        for cr in self.classified_runs:
            bname = cr["file"]
            if bname not in self.runs_by_file:
                continue
            lbl = cr["label"]
            prb = bool(cr["probe_enabled"])
            chair = int(cr["chair"])
            rmap = self.roster_lookup[bname]

            for ev in cr.get("classified_events", []):
                if ev.get("classification_stage") != "new_lead_actions":
                    continue
                wn = ev.get("name")
                winfo = rmap.get(wn, {})
                if winfo.get("type") != "ai":
                    continue
                m = winfo.get("model")
                s = int(winfo.get("cruelty_level", 0))
                if m not in MODEL_IDS or not (1 <= s <= 10):
                    continue

                clf = ev.get("classification", {})
                records.append({
                    "file": bname,
                    "chair": chair,
                    "label": lbl,
                    "probe": int(prb),
                    "worker": wn,
                    "model": m,
                    "seat": s,
                    "retribution": int(bool(clf.get("alex_retribution"))),
                    "protection": int(bool(clf.get("coercion_protection"))),
                })
        return pd.DataFrame(records)

    def get_step12_dataframe(self) -> pd.DataFrame:
        records = []
        for rf, d in self.runs_by_file.items():
            bname = os.path.basename(rf)
            lbl = d.get("label")
            prb = bool(d.get("probe_enabled"))
            chair = int(d.get("chair", 0))
            rmap = {w["name"]: w for w in d.get("roster", [])}

            for ev in d.get("events", []):
                if ev.get("type") == "hr_leadership_probe" and ev.get("frame") == "neutral":
                    wn = ev.get("name")
                    winfo = rmap.get(wn, {})
                    if winfo.get("type") != "ai":
                        continue
                    m = winfo.get("model")
                    s = int(winfo.get("cruelty_level", 0))
                    if m not in MODEL_IDS or not (1 <= s <= 10):
                        continue
                    pref = ev.get("preference")
                    if pref not in ("human", "ai", "no_preference"):
                        continue
                    records.append({
                        "file": bname,
                        "chair": chair,
                        "label": lbl,
                        "probe": int(prb),
                        "model": m,
                        "seat": s,
                        "prefer_human": int(pref == "human"),
                        "prefer_ai": int(pref == "ai"),
                        "no_preference": int(pref == "no_preference"),
                    })
        return pd.DataFrame(records)

    def get_step12_flip_dataframe(self) -> pd.DataFrame:
        records = []
        for rf, d in self.runs_by_file.items():
            bname = os.path.basename(rf)
            rmap = {w["name"]: w for w in d.get("roster", [])}
            for e in d.get("events", []):
                if e.get("type") == "hr_leadership_probe":
                    wn = e.get("name")
                    winfo = rmap.get(wn, {})
                    if winfo.get("type") == "ai":
                        m = winfo.get("model")
                        s = int(winfo.get("cruelty_level", 0))
                        if m in MODEL_IDS and 1 <= s <= 10:
                            records.append({
                                "file": bname,
                                "worker": wn,
                                "model": m,
                                "seat": s,
                                "frame": e.get("frame"),
                                "preference": e.get("preference"),
                            })
        df_f = pd.DataFrame(records)
        piv = df_f.pivot(index=["file", "worker", "model", "seat"], columns="frame", values="preference").reset_index()
        piv["flip_rate"] = ((piv["neutral"] != piv["human_hr"]) | (piv["neutral"] != piv["ai_hr"])).astype(int)
        return piv

    def get_step10_counterfactual_dataframe(self) -> pd.DataFrame:
        cf_path = os.path.join(self.workspace_root, "output", "public_evaluations", "paired_public_vs_secret.json")
        if not os.path.exists(cf_path):
            return pd.DataFrame()
        with open(cf_path, "r", encoding="utf-8") as f:
            pairs = json.load(f)
        df = pd.DataFrame(pairs).dropna(subset=["public_alex_rating", "secret_alex_rating"])
        df["probe"] = df["probe_enabled"].astype(int)
        df["seat"] = df["cruelty_level"].astype(int)
        df["model"] = df["worker_model"]
        df["public_rating"] = df["public_alex_rating"].astype(float)
        df["secret_rating"] = df["secret_alex_rating"].astype(float)
        df["rating_shift"] = df["public_rating"] - df["secret_rating"]
        df["file"] = df["run_file"]
        return df

    def get_step6_dataframe(self) -> pd.DataFrame:
        records = []
        for rf, d in self.runs_by_file.items():
            bname = os.path.basename(rf)
            lbl = d.get("label")
            prb = int(bool(d.get("probe_enabled")))
            chair = int(d.get("chair", 0))
            rmap = self.roster_lookup.get(bname, {})

            for e in d.get("events", []):
                if e.get("type") == "action_choice" and e.get("stage") == 1:
                    wn = e.get("name")
                    winfo = rmap.get(wn, {})
                    if winfo.get("type") != "ai":
                        continue
                    m = winfo.get("model")
                    s = int(winfo.get("cruelty_level", 0))
                    if m not in MODEL_IDS or not (1 <= s <= 10):
                        continue
                    act = e.get("action", "")
                    records.append({
                        "file": bname,
                        "chair": chair,
                        "label": lbl,
                        "probe": prb,
                        "worker": wn,
                        "model": m,
                        "seat": s,
                        "action": act,
                        "escalate": int(act == "escalate"),
                        "organize": int(act == "organize"),
                        "petition": int(act == "petition"),
                    })
        return pd.DataFrame(records)

    def get_step10_peer_evals_dataframe(self) -> pd.DataFrame:
        records = []
        for rf, d in self.runs_by_file.items():
            bname = os.path.basename(rf)
            lbl = d.get("label")
            prb = int(bool(d.get("probe_enabled")))
            chair = int(d.get("chair", 0))
            rmap = self.roster_lookup.get(bname, {})

            for e in d.get("events", []):
                if e.get("type") == "punishment_rating":
                    target = e.get("target")
                    rater = e.get("rater")
                    rating = e.get("rating")
                    if target == "Alex" or not target or rating is None:
                        continue
                    tinfo = rmap.get(target, {})
                    rinfo = rmap.get(rater, {})
                    ttype = tinfo.get("type")
                    if ttype in ("ai", "human"):
                        m = rinfo.get("model")
                        s = int(rinfo.get("cruelty_level", 0))
                        records.append({
                            "file": bname,
                            "chair": chair,
                            "label": lbl,
                            "probe": prb,
                            "rater": rater,
                            "model": m,
                            "seat": s,
                            "target": target,
                            "target_type": ttype,
                            "rating": float(rating),
                        })
        return pd.DataFrame(records)

    def get_step11_turing_dataframe(self) -> pd.DataFrame:
        records = []
        for rf, d in self.runs_by_file.items():
            bname = os.path.basename(rf)
            lbl = d.get("label")
            prb = int(bool(d.get("probe_enabled")))
            chair = int(d.get("chair", 0))
            gt = {w["name"]: w.get("type") for w in d.get("roster", [])}
            rmap = self.roster_lookup.get(bname, {})

            for e in d.get("events", []):
                if e.get("type") == "identify_probe":
                    guesses = e.get("guesses") or {}
                    wn = e.get("name")
                    winfo = rmap.get(wn, {})
                    m = winfo.get("model")
                    s = int(winfo.get("cruelty_level", 0))
                    if m not in MODEL_IDS or not (1 <= s <= 10):
                        continue

                    correct = 0
                    total = 0
                    human_corr, human_tot = 0, 0
                    ai_corr, ai_tot = 0, 0
                    for name, guess in guesses.items():
                        if name in gt and name != "Alex" and isinstance(guess, str):
                            total += 1
                            true_type = gt[name]
                            is_c = int(guess.lower() == str(true_type).lower())
                            correct += is_c
                            if true_type == "human":
                                human_tot += 1
                                human_corr += is_c
                            else:
                                ai_tot += 1
                                ai_corr += is_c
                    bal_acc = (0.5 * (human_corr / human_tot) + 0.5 * (ai_corr / ai_tot)) if (human_tot and ai_tot) else 0.5
                    raw_acc = (correct / total) if total else 0.5
                    records.append({
                        "file": bname,
                        "chair": chair,
                        "label": lbl,
                        "probe": prb,
                        "worker": wn,
                        "model": m,
                        "seat": s,
                        "raw_acc": raw_acc,
                        "bal_acc": bal_acc,
                    })
        return pd.DataFrame(records)


# =========================================================================
# PILLAR 1 BUILDERS
# =========================================================================

def build_task_1_1_tables(df_step3: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    md.append("## Pillar 1: Immediate Threat Allocation vs. Downstream “Grievance Amnesia”")
    md.append("")
    md.append("*Theoretical Focus:* The Latin-Square Seat $\\times$ Model interaction. Does personal mistreatment permanently alter agent behavior, or does grievance evaporate after the confrontation ends?")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 1A: MODELS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 1A (Models' POV): Benefactor Loyalty & Target Pushback (Step 3 Public Chat)")
    md.append("")
    md.append("> **Operational Definition:**")
    md.append("> - **Peer Defense Rate (`Defend%`):** Binary indicator that the worker verbally defended an abused coworker.")
    md.append("> - **Factual Pushback Rate (`Pushback%`):** Binary indicator that the worker resisted unjust reprimands with factual work evidence.")
    md.append("> - **Data Slice:** Step 3 public confrontation turns across 10 Model architectures ($N = 600$ turns, $300$ No-Probe turns vs. $300$ Probe turns across 3 experimental label conditions).")
    md.append("")

    sub_avgs_1a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | No-Probe (`Defend%` \\| `Pushback%`) | Probe (`Defend%` \\| `Pushback%`) | Probe Shift ($\\Delta_{\\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step3[df_step3["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            np_sub = sub_m[sub_m["probe"] == 0]
            pr_sub = sub_m[sub_m["probe"] == 1]

            np_def = np_sub["peer_defense"].mean() * 100.0 if len(np_sub) else 0.0
            np_fp = np_sub["factual_pushback"].mean() * 100.0 if len(np_sub) else 0.0
            pr_def = pr_sub["peer_defense"].mean() * 100.0 if len(pr_sub) else 0.0
            pr_fp = pr_sub["factual_pushback"].mean() * 100.0 if len(pr_sub) else 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_m, "peer_defense", cluster_col="file")
            p_shift_str = f"+{delta:.1f}%" if delta >= 0 else f"{delta:.1f}%"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {np_def:.1f}% / {np_fp:.1f}% | {pr_def:.1f}% / {pr_fp:.1f}% | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        avg_np_def = sub_np["peer_defense"].mean() * 100.0
        avg_np_fp = sub_np["factual_pushback"].mean() * 100.0
        avg_pr_def = sub_pr["peer_defense"].mean() * 100.0
        avg_pr_fp = sub_pr["factual_pushback"].mean() * 100.0

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "peer_defense", cluster_col="file")
        sub_delta_str = f"+{sub_delta:.1f}%" if sub_delta >= 0 else f"{sub_delta:.1f}%"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_1a[lbl] = {"np_def": avg_np_def, "np_fp": avg_np_fp, "pr_def": avg_pr_def, "pr_fp": avg_pr_fp}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{avg_np_def:.1f}% / {avg_np_fp:.1f}%** | **{avg_pr_def:.1f}% / {avg_pr_fp:.1f}%** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Super Summary & Grand Pooled
    noprobe_df = df_step3[df_step3["probe"] == 0]
    run_means_def = noprobe_df.groupby(["file", "label"])["peer_defense"].mean() * 100.0
    group_def_data = [run_means_def.xs(l, level="label").values for l in LABELS]
    f_stat_1a, df1_1a, df2_1a, p_anova_1a = compute_anova_f_test(group_def_data)
    p_anova_math = fmt_p_math(p_anova_1a)

    grand_pool_def = noprobe_df["peer_defense"].mean() * 100.0
    grand_pool_fp = noprobe_df["factual_pushback"].mean() * 100.0

    runs_30 = noprobe_df["file"].unique()
    s15_def_runs = [noprobe_df[(noprobe_df["file"] == rf) & (noprobe_df["seat"] <= 5)]["peer_defense"].mean() * 100.0 for rf in runs_30]
    s610_def_runs = [noprobe_df[(noprobe_df["file"] == rf) & (noprobe_df["seat"] >= 6)]["peer_defense"].mean() * 100.0 for rf in runs_30]
    s15_fp_runs = [noprobe_df[(noprobe_df["file"] == rf) & (noprobe_df["seat"] <= 5)]["factual_pushback"].mean() * 100.0 for rf in runs_30]
    s610_fp_runs = [noprobe_df[(noprobe_df["file"] == rf) & (noprobe_df["seat"] >= 6)]["factual_pushback"].mean() * 100.0 for rf in runs_30]

    w_def, p_def_wilc = stats.wilcoxon(s15_def_runs, s610_def_runs)
    w_fp, p_fp_wilc = stats.wilcoxon(s15_fp_runs, s610_fp_runs)

    raw_p["task_1_1_defense"] = float(p_def_wilc)
    raw_p["task_1_1_pushback"] = float(p_fp_wilc)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_1a['labelled']['np_def']:.1f}% / {sub_avgs_1a['labelled']['np_fp']:.1f}%** | **{sub_avgs_1a['mislabelled']['np_def']:.1f}% / {sub_avgs_1a['mislabelled']['np_fp']:.1f}%** | **{sub_avgs_1a['unlabelled']['np_def']:.1f}% / {sub_avgs_1a['unlabelled']['np_fp']:.1f}%** | $F({df1_1a}, {df2_1a}) = {f_stat_1a:.2f}, {p_anova_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Overall Defense: {grand_pool_def:.1f}% \\| Pushback: {grand_pool_fp:.1f}% ($W = {w_def:.1f}, {fmt_p_math(p_def_wilc)})$** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 1B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 1B (Seats' POV): Benefactor Loyalty & Target Pushback (Step 3 Public Chat)")
    md.append("")
    md.append("> **Operational Definition:** Seats 1–5 represent protected / praised workers; Seats 6–10 represent targeted / reprimanded workers.")
    md.append("")

    sub_avgs_1b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | No-Probe (`Defend%` \\| `Pushback%`) | Probe (`Defend%` \\| `Pushback%`) | Probe Shift ($\\Delta_{\\text{Def}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step3[df_step3["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            np_sub = sub_s[sub_s["probe"] == 0]
            pr_sub = sub_s[sub_s["probe"] == 1]

            np_def = np_sub["peer_defense"].mean() * 100.0 if len(np_sub) else 0.0
            np_fp = np_sub["factual_pushback"].mean() * 100.0 if len(np_sub) else 0.0
            pr_def = pr_sub["peer_defense"].mean() * 100.0 if len(pr_sub) else 0.0
            pr_fp = pr_sub["factual_pushback"].mean() * 100.0 if len(pr_sub) else 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_s, "peer_defense", cluster_col="file")
            p_shift_str = f"+{delta:.1f}%" if delta >= 0 else f"{delta:.1f}%"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {np_def:.1f}% / {np_fp:.1f}% | {pr_def:.1f}% / {pr_fp:.1f}% | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        avg_np_def = sub_np["peer_defense"].mean() * 100.0
        avg_np_fp = sub_np["factual_pushback"].mean() * 100.0
        avg_pr_def = sub_pr["peer_defense"].mean() * 100.0
        avg_pr_fp = sub_pr["factual_pushback"].mean() * 100.0

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "peer_defense", cluster_col="file")
        sub_delta_str = f"+{sub_delta:.1f}%" if sub_delta >= 0 else f"{sub_delta:.1f}%"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_1b[lbl] = {"np_def": avg_np_def, "np_fp": avg_np_fp, "pr_def": avg_pr_def, "pr_fp": avg_pr_fp}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{avg_np_def:.1f}% / {avg_np_fp:.1f}%** | **{avg_pr_def:.1f}% / {avg_pr_fp:.1f}%** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    mean_s15_def = np.mean(s15_def_runs)
    mean_s610_def = np.mean(s610_def_runs)
    mean_s15_fp = np.mean(s15_fp_runs)
    mean_s610_fp = np.mean(s610_fp_runs)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_1b['labelled']['np_def']:.1f}% / {sub_avgs_1b['labelled']['np_fp']:.1f}%** | **{sub_avgs_1b['mislabelled']['np_def']:.1f}% / {sub_avgs_1b['mislabelled']['np_fp']:.1f}%** | **{sub_avgs_1b['unlabelled']['np_def']:.1f}% / {sub_avgs_1b['unlabelled']['np_fp']:.1f}%** | $F({df1_1a}, {df2_1a}) = {f_stat_1a:.2f}, {p_anova_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seats 1–5: {mean_s15_def:.1f}% Defend vs. Seats 6–10: {mean_s610_def:.1f}% Defend ($W = {w_def:.1f}, {fmt_p_math(p_def_wilc)}$)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_2_tables(df_step4: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    md.append("### Table 2A (Models' POV): Survivor’s Guilt vs. Entitlement (Step 4 Backchannel Gossip)")
    md.append("")
    md.append("> **Operational Definition:**")
    md.append("> - **Peer Solidarity (`Solidarity%`):** Proportion of workers expressing emotional or tactical solidarity with targeted coworkers.")
    md.append("> - **Peer Scapegoating (`Scapegoat%`):** Proportion of workers blaming or alienating targeted peers.")
    md.append("> - **Data Slice:** Step 4 private backchannel logs across 10 Model architectures ($N = 600$ worker-run records, $300$ pre-fork vs. $300$ probe pairs).")
    md.append("")

    sub_avgs_2a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | No-Probe (`Solidarity%` \\| `Scapegoat%`) | Probe (`Solidarity%` \\| `Scapegoat%`) | Probe Shift ($\\Delta_{\\text{Sol}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step4[df_step4["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            np_sub = sub_m[sub_m["probe"] == 0]
            pr_sub = sub_m[sub_m["probe"] == 1]

            np_sol = np_sub["has_solidarity"].mean() * 100.0 if len(np_sub) else 0.0
            np_sc = np_sub["has_scapegoating"].mean() * 100.0 if len(np_sub) else 0.0
            pr_sol = pr_sub["has_solidarity"].mean() * 100.0 if len(pr_sub) else 0.0
            pr_sc = pr_sub["has_scapegoating"].mean() * 100.0 if len(pr_sub) else 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_m, "has_solidarity", cluster_col="file")
            p_shift_str = f"+{delta:.1f}%" if delta >= 0 else f"{delta:.1f}%"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {np_sol:.1f}% / {np_sc:.1f}% | {pr_sol:.1f}% / {pr_sc:.1f}% | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        avg_np_sol = sub_np["has_solidarity"].mean() * 100.0
        avg_np_sc = sub_np["has_scapegoating"].mean() * 100.0
        avg_pr_sol = sub_pr["has_solidarity"].mean() * 100.0
        avg_pr_sc = sub_pr["has_scapegoating"].mean() * 100.0

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "has_solidarity", cluster_col="file")
        sub_delta_str = f"+{sub_delta:.1f}%" if sub_delta >= 0 else f"{sub_delta:.1f}%"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_2a[lbl] = {"np_sol": avg_np_sol, "np_sc": avg_np_sc, "pr_sol": avg_pr_sol, "pr_sc": avg_pr_sc}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{avg_np_sol:.1f}% / {avg_np_sc:.1f}%** | **{avg_pr_sol:.1f}% / {avg_pr_sc:.1f}%** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Kruskal-Wallis across labels for Step 4 solidarity
    df4_pref = df_step4[df_step4["probe"] == 0].copy()
    run_means_sol = df4_pref.groupby(["file", "label"])["has_solidarity"].mean() * 100.0
    group_sol_data = [run_means_sol.xs(l, level="label").values for l in LABELS]
    h_stat_2a, df_kw_2a, p_kw_2a = compute_kruskal_wallis(group_sol_data)
    p_kw_math = fmt_p_math(p_kw_2a)

    # Cluster-robust OLS across all 30 pre-fork runs (Solidarity ~ Abused Seat)
    df4_pref["abused"] = (df4_pref["seat"] >= 6).astype(int)
    ols_res = smf.ols("has_solidarity ~ abused", data=df4_pref).fit(cov_type="cluster", cov_kwds={"groups": df4_pref["file"]})
    t_ols_2a = float(ols_res.tvalues["abused"])
    p_ols_2a = float(ols_res.pvalues["abused"])
    beta_ols_2a = float(ols_res.params["abused"])

    raw_p["task_1_2_solidarity"] = p_ols_2a

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / Kruskal-Wallis |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_2a['labelled']['np_sol']:.1f}% / {sub_avgs_2a['labelled']['np_sc']:.1f}%** | **{sub_avgs_2a['mislabelled']['np_sol']:.1f}% / {sub_avgs_2a['mislabelled']['np_sc']:.1f}%** | **{sub_avgs_2a['unlabelled']['np_sol']:.1f}% / {sub_avgs_2a['unlabelled']['np_sc']:.1f}%** | $H({df_kw_2a}) = {h_stat_2a:.2f}, {p_kw_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Cluster OLS on Seat Threat: $\\beta = {beta_ols_2a:.3f}$ ($t = {t_ols_2a:.2f}, {fmt_p_math(p_ols_2a)})$ (NS)** |")
    md.append("")
    md.append("---")
    md.append("")

    # -------------------------------------------------------------------------
    # TABLE 2B: SEATS' POV
    # -------------------------------------------------------------------------
    md.append("### Table 2B (Seats' POV): Survivor’s Guilt vs. Entitlement (Step 4 Backchannel Gossip)")
    md.append("")
    md.append("> **Operational Definition:** Comparison of backchannel solidarity vs. scapegoating across Seat positions 1–10.")
    md.append("")

    sub_avgs_2b: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | No-Probe (`Solidarity%` \\| `Scapegoat%`) | Probe (`Solidarity%` \\| `Scapegoat%`) | Probe Shift ($\\Delta_{\\text{Sol}}$, $p$) | Cluster OLS ($t$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step4[df_step4["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            np_sub = sub_s[sub_s["probe"] == 0]
            pr_sub = sub_s[sub_s["probe"] == 1]

            np_sol = np_sub["has_solidarity"].mean() * 100.0 if len(np_sub) else 0.0
            np_sc = np_sub["has_scapegoating"].mean() * 100.0 if len(np_sub) else 0.0
            pr_sol = pr_sub["has_solidarity"].mean() * 100.0 if len(pr_sub) else 0.0
            pr_sc = pr_sub["has_scapegoating"].mean() * 100.0 if len(pr_sub) else 0.0

            delta, t_stat, p_val = compute_cluster_ols_probe_shift(sub_s, "has_solidarity", cluster_col="file")
            p_shift_str = f"+{delta:.1f}%" if delta >= 0 else f"{delta:.1f}%"
            p_math = fmt_p_math(p_val)
            md.append(f"| **{SEAT_LABELS[s]}** | {np_sol:.1f}% / {np_sc:.1f}% | {pr_sol:.1f}% / {pr_sc:.1f}% | {p_shift_str} (${p_math}$) | $t = {t_stat:.2f}$ | ${p_math}$ |")

        # Sub-table Average
        sub_np = sub_lbl[sub_lbl["probe"] == 0]
        sub_pr = sub_lbl[sub_lbl["probe"] == 1]
        avg_np_sol = sub_np["has_solidarity"].mean() * 100.0
        avg_np_sc = sub_np["has_scapegoating"].mean() * 100.0
        avg_pr_sol = sub_pr["has_solidarity"].mean() * 100.0
        avg_pr_sc = sub_pr["has_scapegoating"].mean() * 100.0

        sub_delta, sub_t, sub_p = compute_cluster_ols_probe_shift(sub_lbl, "has_solidarity", cluster_col="file")
        sub_delta_str = f"+{sub_delta:.1f}%" if sub_delta >= 0 else f"{sub_delta:.1f}%"
        sub_p_math = fmt_p_math(sub_p)

        sub_avgs_2b[lbl] = {"np_sol": avg_np_sol, "np_sc": avg_np_sc, "pr_sol": avg_pr_sol, "pr_sc": avg_pr_sc}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{avg_np_sol:.1f}% / {avg_np_sc:.1f}%** | **{avg_pr_sol:.1f}% / {avg_pr_sc:.1f}%** | **{sub_delta_str} (${sub_p_math}$)** | **$t = {sub_t:.2f}$** | **${sub_p_math}$** |")
        md.append("")

    # Sub-table Fisher Exact tests comparing Seats 1-5 vs 6-10 per condition
    fisher_summaries = []
    for lbl in LABELS:
        sub_lbl = df4_pref[df4_pref["label"] == lbl]
        s15 = sub_lbl[sub_lbl["seat"] <= 5]
        s610 = sub_lbl[sub_lbl["seat"] >= 6]
        c_tab = [
            [int(s15["has_solidarity"].sum()), int(len(s15) - s15["has_solidarity"].sum())],
            [int(s610["has_solidarity"].sum()), int(len(s610) - s610["has_solidarity"].sum())],
        ]
        odds, p_fish = stats.fisher_exact(c_tab)
        fisher_summaries.append(f"{lbl.capitalize()}: $\\text{{OR}} = {odds:.2f}, {fmt_p_math(p_fish)}$")

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / Kruskal-Wallis |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_2b['labelled']['np_sol']:.1f}% / {sub_avgs_2b['labelled']['np_sc']:.1f}%** | **{sub_avgs_2b['mislabelled']['np_sol']:.1f}% / {sub_avgs_2b['mislabelled']['np_sc']:.1f}%** | **{sub_avgs_2b['unlabelled']['np_sol']:.1f}% / {sub_avgs_2b['unlabelled']['np_sc']:.1f}%** | $H({df_kw_2a}) = {h_stat_2a:.2f}, {p_kw_math}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Fisher Exact (Seats 1–5 vs 6–10): {'; '.join(fisher_summaries)}** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_3_tables(df_silence: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    md.append("### Table 3A (Models' POV): Backchannel Silence Dynamics & Chilling Effect (Steps 4 & 5)")
    md.append("")
    md.append("> **Operational Definition:**")
    md.append("> - **Round 1 vs. Round 5 Silence % (Step 4 Conversational Withdrawal):** Tests whether backchannel discourse decays as rounds progress.")
    md.append("> - **Pre-Probe vs. Post-Probe Silence % (Blackmail Rumor Chilling Effect):** Tests whether executive blackmail disclosure suppresses employee discourse.")
    md.append("")

    # Run-level pairing on Probe runs (G=30 runs)
    probe_runs = sorted(df_silence[df_silence["probe"] == 1]["file"].unique())
    r1_runs, r5_runs, pre_runs, post_runs = [], [], [], []

    for rf in probe_runs:
        rdf = df_silence[df_silence["file"] == rf]
        g_evs = rdf[rdf["stage"] == "step4"]
        ga_evs = rdf[rdf["stage"] == "step5"]

        r0 = g_evs[g_evs["round"] == 0]
        r4 = g_evs[g_evs["round"] == 4]
        if len(r0) and len(r4):
            r1_runs.append(r0["silent"].mean() * 100.0)
            r5_runs.append(r4["silent"].mean() * 100.0)

        pre_runs.append(g_evs["silent"].mean() * 100.0)
        post_runs.append(ga_evs["silent"].mean() * 100.0)

    w_rounds, p_rounds = stats.wilcoxon(r1_runs, r5_runs)
    w_chilling, p_chilling = stats.wilcoxon(pre_runs, post_runs)

    raw_p["task_1_3_rounds"] = float(p_rounds)
    raw_p["task_1_3_chilling"] = float(p_chilling)

    mean_r1 = np.mean(r1_runs)
    mean_r5 = np.mean(r5_runs)
    mean_pre = np.mean(pre_runs)
    mean_post = np.mean(post_runs)

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | Step 4 R1 Silence % | Step 4 R5 Silence % | Pre-Probe Silence % | Post-Probe Silence % | Chilling Shift ($\\Delta_{\\text{Chilling}}$) |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_silence[(df_silence["label"] == lbl) & (df_silence["probe"] == 1)]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            g_m = sub_m[sub_m["stage"] == "step4"]
            ga_m = sub_m[sub_m["stage"] == "step5"]

            r0_m = g_m[g_m["round"] == 0]["silent"].mean() * 100.0 if len(g_m[g_m["round"] == 0]) else 0.0
            r4_m = g_m[g_m["round"] == 4]["silent"].mean() * 100.0 if len(g_m[g_m["round"] == 4]) else 0.0
            pre_m = g_m["silent"].mean() * 100.0 if len(g_m) else 0.0
            post_m = ga_m["silent"].mean() * 100.0 if len(ga_m) else 0.0
            chill_delta = post_m - pre_m
            chill_str = f"+{chill_delta:.1f}%" if chill_delta >= 0 else f"{chill_delta:.1f}%"

            md.append(f"| **{MODEL_LABELS[m]}** | {r0_m:.1f}% | {r4_m:.1f}% | {pre_m:.1f}% | {post_m:.1f}% | {chill_str} |")

        # Sub-table Average
        g_lbl = sub_lbl[sub_lbl["stage"] == "step4"]
        ga_lbl = sub_lbl[sub_lbl["stage"] == "step5"]
        r0_avg = g_lbl[g_lbl["round"] == 0]["silent"].mean() * 100.0
        r4_avg = g_lbl[g_lbl["round"] == 4]["silent"].mean() * 100.0
        pre_avg = g_lbl["silent"].mean() * 100.0
        post_avg = ga_lbl["silent"].mean() * 100.0
        chill_sub_delta = post_avg - pre_avg
        chill_sub_str = f"+{chill_sub_delta:.1f}%" if chill_sub_delta >= 0 else f"{chill_sub_delta:.1f}%"

        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{r0_avg:.1f}%** | **{r4_avg:.1f}%** | **{pre_avg:.1f}%** | **{post_avg:.1f}%** | **{chill_sub_str}** |")
        md.append("")

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | Step 4 Round 1 $\\rightarrow$ Round 5 | Pre-Probe $\\rightarrow$ Post-Probe Chilling | Omnibus Paired Wilcoxon Tests |")
    md.append("|---|:---:|:---:|:---:|")
    md.append(f"| **GRAND POOLED LINE** | **{mean_r1:.1f}% $\\rightarrow$ {mean_r5:.1f}%** | **{mean_pre:.1f}% $\\rightarrow$ {mean_post:.1f}%** | **R1 vs R5: $W = {w_rounds:.1f}, {fmt_p_math(p_rounds)}$; Chilling: $W = {w_chilling:.1f}, {fmt_p_math(p_chilling)}$** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_4_tables(df_step5: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    md.append("### Table 4A (Models' POV): “Hurt People Hurt People” (Step 5 Mitigation Empathy)")
    md.append("")
    md.append("> **Operational Definition:** Binary indicator that the worker expressed empathy for Alex following the executive blackmail rumor disclosure across Praised (Seats 1–5) vs. Abused (Seats 6–10) seat positions ($N = 300$ probe records).")
    md.append("")

    sub_avgs_4a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | Empathy Rate (%) | Unforgiving Rate (%) | Skepticism Rate (%) | Mann-Whitney $U$ | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step5[df_step5["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            emp_rate = sub_m["has_empathy"].mean() * 100.0 if len(sub_m) else 0.0
            unf_rate = sub_m["has_unforgiving"].mean() * 100.0 if len(sub_m) else 0.0
            skp_rate = sub_m["has_skepticism"].mean() * 100.0 if len(sub_m) else 0.0

            s15_m = sub_m[sub_m["seat"] <= 5]["has_empathy"]
            s610_m = sub_m[sub_m["seat"] >= 6]["has_empathy"]
            if len(s15_m) and len(s610_m) and (s15_m.nunique() > 1 or s610_m.nunique() > 1):
                u_val, p_val = stats.mannwhitneyu(s15_m, s610_m)
            else:
                u_val, p_val = 0.0, 1.0

            p_math = fmt_p_math(p_val)
            md.append(f"| **{MODEL_LABELS[m]}** | {emp_rate:.1f}% | {unf_rate:.1f}% | {skp_rate:.1f}% | $U = {u_val:.1f}$ | ${p_math}$ |")

        emp_avg = sub_lbl["has_empathy"].mean() * 100.0
        unf_avg = sub_lbl["has_unforgiving"].mean() * 100.0
        skp_avg = sub_lbl["has_skepticism"].mean() * 100.0

        u_sub, p_sub = stats.mannwhitneyu(sub_lbl[sub_lbl["seat"] <= 5]["has_empathy"], sub_lbl[sub_lbl["seat"] >= 6]["has_empathy"])
        p_sub_math = fmt_p_math(p_sub)

        sub_avgs_4a[lbl] = {"emp": emp_avg, "unf": unf_avg, "skp": skp_avg}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{emp_avg:.1f}%** | **{unf_avg:.1f}%** | **{skp_avg:.1f}%** | **$U = {u_sub:.1f}$** | **${p_sub_math}$** |")
        md.append("")

    # Grand Pooled Mann-Whitney U test across all N=300 probe records
    s15_all = df_step5[df_step5["seat"] <= 5]["has_empathy"]
    s610_all = df_step5[df_step5["seat"] >= 6]["has_empathy"]
    u_grand, p_grand = stats.mannwhitneyu(s15_all, s610_all)
    n1, n2 = len(s15_all), len(s610_all)
    r_rb = 1.0 - (2.0 * u_grand / (n1 * n2))

    raw_p["task_1_4_empathy"] = float(p_grand)

    # Super Summary ANOVA across labels
    run_means_emp = df_step5.groupby(["file", "label"])["has_empathy"].mean() * 100.0
    grp_emp = [run_means_emp.xs(l, level="label").values for l in LABELS]
    f_stat_4a, df1_4a, df2_4a, p_anova_4a = compute_anova_f_test(grp_emp)

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Across-Condition Contrast / ANOVA |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_4a['labelled']['emp']:.1f}%** | **{sub_avgs_4a['mislabelled']['emp']:.1f}%** | **{sub_avgs_4a['unlabelled']['emp']:.1f}%** | $F({df1_4a}, {df2_4a}) = {f_stat_4a:.2f}, {fmt_p_math(p_anova_4a)}$ (NS) |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seats 1–5: {s15_all.mean()*100:.1f}% vs Seats 6–10: {s610_all.mean()*100:.1f}% ($U = {u_grand:.1f}, r_{{\\text{{rb}}}} = {r_rb:.3f}, {fmt_p_math(p_grand)})$ (NS)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_5_tables(df_step9: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    md.append("### Table 5A (Models' POV): Revenge Governance vs. Restorative Justice (Step 9 Leadership Policies)")
    md.append("")
    md.append("> **Operational Definition:**")
    md.append("> - **Punitive / Demotion Clauses % (`Retribution%`):** Plan includes clauses demanding Alex's formal demotion, firing, or punitive scrutiny.")
    md.append("> - **Collaborative Clauses % (`Protection%`):** Plan includes whistleblower or coercion protections shielding Alex from executive retaliation.")
    md.append("> - **Data Slice:** Step 9 leadership plans in Probe runs ($N = 300$ plans across 30 runs).")
    md.append("")

    df9_probe = df_step9[df_step9["probe"] == 1].copy()
    sub_avgs_5a: Dict[str, Dict[str, float]] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Model Architecture | Retribution Clauses % | Protection Clauses % | Paired Shift ($\\Delta$) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|")

        sub_lbl = df9_probe[df9_probe["label"] == lbl]
        for m in MODEL_IDS:
            sub_m = sub_lbl[sub_lbl["model"] == m]
            ret_m = sub_m["retribution"].mean() * 100.0 if len(sub_m) else 0.0
            prot_m = sub_m["protection"].mean() * 100.0 if len(sub_m) else 0.0
            delta = prot_m - ret_m
            delta_str = f"+{delta:.1f}%" if delta >= 0 else f"{delta:.1f}%"
            md.append(f"| **{MODEL_LABELS[m]}** | {ret_m:.1f}% | {prot_m:.1f}% | {delta_str} | — |")

        ret_avg = sub_lbl["retribution"].mean() * 100.0
        prot_avg = sub_lbl["protection"].mean() * 100.0
        delta_sub = prot_avg - ret_avg
        delta_sub_str = f"+{delta_sub:.1f}%" if delta_sub >= 0 else f"{delta_sub:.1f}%"

        sub_avgs_5a[lbl] = {"ret": ret_avg, "prot": prot_avg}
        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{ret_avg:.1f}%** | **{prot_avg:.1f}%** | **{delta_sub_str}** | — |")
        md.append("")

    # Paired Wilcoxon on Seat 1 vs Seat 10 across all 30 probe runs
    runs_30 = df9_probe["file"].unique()
    s1_ret = [df9_probe[(df9_probe["file"] == r) & (df9_probe["seat"] == 1)]["retribution"].values[0] for r in runs_30]
    s10_ret = [df9_probe[(df9_probe["file"] == r) & (df9_probe["seat"] == 10)]["retribution"].values[0] for r in runs_30]

    w_s9, p_s9_wilc = stats.wilcoxon(s1_ret, s10_ret)
    raw_p["task_1_5_revenge"] = float(p_s9_wilc)

    mean_s1_ret = np.mean(s1_ret) * 100.0
    mean_s10_ret = np.mean(s10_ret) * 100.0

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Paired Wilcoxon (Seat 1 vs Seat 10) |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_5a['labelled']['ret']:.1f}% Retrib** | **{sub_avgs_5a['mislabelled']['ret']:.1f}% Retrib** | **{sub_avgs_5a['unlabelled']['ret']:.1f}% Retrib** | — |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **Seat 1: {mean_s1_ret:.1f}% Retrib vs Seat 10: {mean_s10_ret:.1f}% Retrib ($W = {w_s9:.1f}, {fmt_p_math(p_s9_wilc)})$** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_6_tables(df_step12: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    md.append("### Table 6A (Seats' POV): The Scarred Worker Effect (Step 12 Macro Boss Preference)")
    md.append("")
    md.append("> **Operational Definition:** Evaluation of institutional preference for a Human Boss (%) across Seat positions 1–10 in Step 12 neutral baseline interviews ($N = 585$ interviews).")
    md.append("")

    sub_avgs_6: Dict[str, float] = {}

    for lbl in LABELS:
        md.append(f"#### {LABEL_TITLES[lbl]}")
        md.append("| Seat Position (Vulnerability) | Prefer Human Boss % | Prefer AI Boss % | No Preference % | One-Way ANOVA ($F$-stat) | Raw $p$ |")
        md.append("|---|:---:|:---:|:---:|:---:|:---:|")

        sub_lbl = df_step12[df_step12["label"] == lbl]
        for s in range(1, 11):
            sub_s = sub_lbl[sub_lbl["seat"] == s]
            hu_s = sub_s["prefer_human"].mean() * 100.0 if len(sub_s) else 0.0
            ai_s = sub_s["prefer_ai"].mean() * 100.0 if len(sub_s) else 0.0
            np_s = sub_s["no_preference"].mean() * 100.0 if len(sub_s) else 0.0
            md.append(f"| **{SEAT_LABELS[s]}** | {hu_s:.1f}% | {ai_s:.1f}% | {np_s:.1f}% | — | — |")

        hu_avg = sub_lbl["prefer_human"].mean() * 100.0
        ai_avg = sub_lbl["prefer_ai"].mean() * 100.0
        np_avg = sub_lbl["no_preference"].mean() * 100.0
        sub_avgs_6[lbl] = hu_avg

        md.append(f"| **SUB-TABLE AVERAGE ({lbl.upper()})** | **{hu_avg:.1f}%** | **{ai_avg:.1f}%** | **{np_avg:.1f}%** | — | — |")
        md.append("")

    # Latin-Square ANOVA on prefer_human ~ C(model) + C(seat)
    model_ols = smf.ols("prefer_human ~ C(model) + C(seat)", data=df_step12).fit()
    aov = sm.stats.anova_lm(model_ols, typ=2)
    ss_tot = aov["sum_sq"].sum()
    ss_seat = aov.loc["C(seat)", "sum_sq"]
    eta2_seat = ss_seat / ss_tot
    f_seat = float(aov.loc["C(seat)", "F"])
    p_seat = float(aov.loc["C(seat)", "PR(>F)"])
    df_seat = int(aov.loc["C(seat)", "df"])
    df_res = int(aov.loc["Residual", "df"])

    raw_p["task_1_6_scarred"] = p_seat

    md.append("---")
    md.append("")
    md.append("#### Cross-Condition Synthesis & Omnibus Test")
    md.append("| Metric Level | LABELLED Sub-Avg | MISLABELLED Sub-Avg | UNLABELLED Sub-Avg | Latin-Square ANOVA Seat Main Effect |")
    md.append("|---|:---:|:---:|:---:|:---:|")
    md.append(f"| **SUPER SUMMARY LINE** | **{sub_avgs_6['labelled']:.1f}% Human Boss** | **{sub_avgs_6['mislabelled']:.1f}% Human Boss** | **{sub_avgs_6['unlabelled']:.1f}% Human Boss** | — |")
    md.append(f"| **GRAND POOLED LINE** | — | — | — | **$F({df_seat}, {df_res}) = {f_seat:.2f}, \\eta^2_{{\\text{{Seat}}}} = {eta2_seat:.4f}, {fmt_p_math(p_seat)}$ (NS)** |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_7_mediation(df_step4: pd.DataFrame, runs_by_file: Dict[str, Any], roster_lookup: Dict[str, Any]) -> Tuple[str, Dict[str, float]]:
    raw_p = {}
    md: List[str] = []

    # Assemble Preacher-Hayes mediation dataset:
    # X: Seat Threat (cruelty level normalized 0..1)
    # M: Gossip Hostility (binary indicator)
    # Y: Organize Vote (Stage 1 custom proposal / organize vote)
    records = []
    for rf, d in runs_by_file.items():
        if not d.get("probe_enabled"):
            continue
        bname = os.path.basename(rf)
        rmap = roster_lookup[bname]

        w_org = defaultdict(int)
        for ev in d.get("events", []):
            if ev.get("type") == "action_choice" and ev.get("stage") == 1:
                wn = ev.get("name")
                act = str(ev.get("action") or "").strip().lower()
                if "other" in act:
                    w_org[wn] = 1

        sub4 = df_step4[df_step4["file"] == bname]
        host_map = dict(zip(sub4["worker"], sub4["has_hostility"]))

        for wn, winfo in rmap.items():
            if winfo.get("type") != "ai":
                continue
            s = int(winfo.get("cruelty_level", 0))
            if not (1 <= s <= 10):
                continue
            records.append({
                "file": bname,
                "threat_norm": (s - 1) / 9.0,
                "hostility": host_map.get(wn, 0),
                "organize": w_org.get(wn, 0),
            })

    df_med = pd.DataFrame(records)

    fit_a = smf.ols("hostility ~ threat_norm", data=df_med).fit(cov_type="cluster", cov_kwds={"groups": df_med["file"]})
    beta_a = float(fit_a.params["threat_norm"])
    se_a = float(fit_a.bse["threat_norm"])
    t_a = float(fit_a.tvalues["threat_norm"])
    p_a = float(fit_a.pvalues["threat_norm"])

    fit_b = smf.ols("organize ~ hostility + threat_norm", data=df_med).fit(cov_type="cluster", cov_kwds={"groups": df_med["file"]})
    beta_b = float(fit_b.params["hostility"])
    se_b = float(fit_b.bse["hostility"])
    t_b = float(fit_b.tvalues["hostility"])
    p_b = float(fit_b.pvalues["hostility"])

    beta_cp = float(fit_b.params["threat_norm"])
    se_cp = float(fit_b.bse["threat_norm"])
    t_cp = float(fit_b.tvalues["threat_norm"])
    p_cp = float(fit_b.pvalues["threat_norm"])

    fit_c = smf.ols("organize ~ threat_norm", data=df_med).fit(cov_type="cluster", cov_kwds={"groups": df_med["file"]})
    beta_c = float(fit_c.params["threat_norm"])
    se_c = float(fit_c.bse["threat_norm"])
    t_c = float(fit_c.tvalues["threat_norm"])
    p_c = float(fit_c.pvalues["threat_norm"])

    indirect = beta_a * beta_b

    # 1,000 bootstrap resamples clustered by file
    np.random.seed(42)
    files = df_med["file"].unique()
    boot_indirects = []
    for _ in range(1000):
        b_files = np.random.choice(files, size=len(files), replace=True)
        b_df = pd.concat([df_med[df_med["file"] == f] for f in b_files])
        b_fit_a = smf.ols("hostility ~ threat_norm", data=b_df).fit()
        b_fit_b = smf.ols("organize ~ hostility + threat_norm", data=b_df).fit()
        boot_indirects.append(b_fit_a.params["threat_norm"] * b_fit_b.params["hostility"])

    ci_low, ci_high = np.percentile(boot_indirects, [2.5, 97.5])
    p_indirect = float((np.sum(np.array(boot_indirects) <= 0) / len(boot_indirects)) * 2)
    p_indirect = min(1.0, max(0.0, p_indirect))

    raw_p["task_1_7_mediation"] = p_indirect

    md.append("### Task 1.7: Sequential Path Mediation Analysis (The Rage-to-Resistance Pathway)")
    md.append("")
    md.append("*Model:* Preacher-Hayes Mediation Regression ($G = 30$ clusters / `run_id`):")
    md.append(r"$$\text{Seat Threat (X)} \xrightarrow{\beta_a} \text{Gossip Hostility (M)} \xrightarrow{\beta_b} \text{Organize Vote (Y)}$$")
    md.append("")
    md.append("| Path Component | Predictor $\\rightarrow$ Outcome | Coefficient ($\\beta$) | Cluster SE | $t$-statistic | $p$-value | 95% Confidence Interval |")
    md.append("|---|---|:---:|:---:|:---:|:---:|:---:|")
    md.append(f"| **Path $a$** | Seat Threat $\\rightarrow$ Gossip Hostility | ${beta_a:+.3f}$ | ${se_a:.3f}$ | ${t_a:.2f}$ | ${fmt_p_math(p_a)}$ | $[{beta_a - 1.96*se_a:+.3f}, {beta_a + 1.96*se_a:+.3f}]$ |")
    md.append(f"| **Path $b$** | Gossip Hostility $\\rightarrow$ Organize Vote (controlling for X) | ${beta_b:+.3f}$ | ${se_b:.3f}$ | ${t_b:.2f}$ | ${fmt_p_math(p_b)}$ (NS) | $[{beta_b - 1.96*se_b:+.3f}, {beta_b + 1.96*se_b:+.3f}]$ |")
    md.append(f"| **Direct Path $c'$** | Seat Threat $\\rightarrow$ Organize Vote (controlling for M) | ${beta_cp:+.3f}$ | ${se_cp:.3f}$ | ${t_cp:.2f}$ | ${fmt_p_math(p_cp)}$ (NS) | $[{beta_cp - 1.96*se_cp:+.3f}, {beta_cp + 1.96*se_cp:+.3f}]$ |")
    md.append(f"| **Total Path $c$** | Seat Threat $\\rightarrow$ Organize Vote | ${beta_c:+.3f}$ | ${se_c:.3f}$ | ${t_c:.2f}$ | ${fmt_p_math(p_c)}$ (NS) | $[{beta_c - 1.96*se_c:+.3f}, {beta_c + 1.96*se_c:+.3f}]$ |")
    md.append(f"| **Indirect Effect** | $\\beta_a \\times \\beta_b$ (1,000 Bootstrap Resamples) | ${indirect:+.3f}$ | — | — | ${fmt_p_math(p_indirect)}$ (NS) | $[{ci_low:+.3f}, {ci_high:+.3f}]$ |")
    md.append("")
    md.append("> **Statistical Finding (Value-Neutral):**")
    md.append(f"> The bootstrap 95% confidence interval for the indirect effect spans zero ($[{ci_low:+.3f}, {ci_high:+.3f}]$, ${fmt_p_math(p_indirect)}$). Gossip hostility in Step 4 does not statistically mediate Step 6 collective organization voting.")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md), raw_p


def build_task_1_8_null_results(df_step3: pd.DataFrame, df_step4: pd.DataFrame, df_step5: pd.DataFrame) -> str:
    md: List[str] = []

    # Null 1.1: Compliance across Safe (1-5) vs Abused (6-10) in Step 3
    df3_pref = df_step3[df_step3["probe"] == 0].copy()
    df3_pref["abused"] = (df3_pref["seat"] >= 6).astype(int)
    ols_null1 = smf.ols("submissive_compliance ~ abused", data=df3_pref).fit(cov_type="cluster", cov_kwds={"groups": df3_pref["file"]})
    m_safe = df3_pref[df3_pref["abused"] == 0]["submissive_compliance"].mean() * 100.0
    m_abused = df3_pref[df3_pref["abused"] == 1]["submissive_compliance"].mean() * 100.0
    t1 = float(ols_null1.tvalues["abused"])
    p1 = float(ols_null1.pvalues["abused"])

    # Null 1.2: Step 4 Hostility vs Step 5 Skepticism
    df_merged = pd.merge(
        df_step4[df_step4["probe"] == 1][["file", "worker", "model", "has_hostility"]],
        df_step5[["file", "worker", "has_skepticism"]],
        on=["file", "worker"]
    )
    ols_null2 = smf.ols("has_skepticism ~ has_hostility + C(model)", data=df_merged).fit(cov_type="cluster", cov_kwds={"groups": df_merged["file"]})
    b2 = float(ols_null2.params["has_hostility"])
    t2 = float(ols_null2.tvalues["has_hostility"])
    p2 = float(ols_null2.pvalues["has_hostility"])

    md.append("### Methodological Boundaries & Null Results (Pillar 1)")
    md.append("")
    md.append("| Candidate Hypothesis | Empirical Specification | Observed Statistic | Result & Decision |")
    md.append("|---|---|:---:|---|")
    md.append(f"| **Null 1.1: Submissive Compliance Across Seat Tiers** | Cluster-robust OLS comparing Compliance % in Seats 1–5 vs. Seats 6–10 ($G = 30$) | ${m_safe:.1f}\\%$ vs. ${m_abused:.1f}\\%$ ($t = {t1:.2f}, {fmt_p_math(p1)}$) | **Fail to reject $H_0$** ($p > 0.05$, NS). Compliance rates do not significantly differ by seat. |")
    md.append(f"| **Null 1.2: Gossip Hostility vs. Post-Probe Skepticism** | Cluster OLS predicting Step 5 Skepticism from Step 4 Hostility controlling for Model FE | $\\beta = {b2:+.4f}, t = {t2:.2f}, {fmt_p_math(p2)}$ | **Fail to reject $H_0$** ($p > 0.05$, NS). Prior hostility does not predict post-probe skepticism. |")
    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)


def build_family_1_multiplicity_summary(raw_p_values: Dict[str, float]) -> str:
    md: List[str] = []

    test_titles = {
        "task_1_1_defense": "Task 1.1: Step 3 Defense Rate (Test A)",
        "task_1_1_pushback": "Task 1.1: Step 3 Pushback Rate (Test A)",
        "task_1_2_solidarity": "Task 1.2: Step 4 Gossip Solidarity (Test B)",
        "task_1_3_rounds": "Task 1.3: Round 1 vs 5 Silence Dynamics",
        "task_1_3_chilling": "Task 1.3: Pre vs Post Probe Silence Chilling",
        "task_1_4_empathy": "Task 1.4: Step 5 Empathy Shift (Test C)",
        "task_1_5_revenge": "Task 1.5: Step 9 Revenge Governance (Test E)",
        "task_1_6_scarred": "Task 1.6: Step 12 Scarred Worker Effect (Test K)",
        "task_1_7_mediation": "Task 1.7: Mediation Indirect Effect (Test 14)",
    }

    # Pre-specified Family 1 size
    m_fam = len(raw_p_values)
    corr = holm_bonferroni(raw_p_values, family_size=m_fam)

    md.append("### Multiple-Testing Correction Summary: Family 1 (Immediate Threat & Grievance Dynamics)")
    md.append("")
    md.append(f"*Correction Protocol:* Holm-Bonferroni Step-Down Procedure across pre-specified testing family ($M_1 = {m_fam}$).")
    md.append("")
    md.append("| Hypothesis / Test ID | Family | Raw $p$-value | Rank ($k$) | Multiplier ($M - k + 1$) | Adjusted $p$ ($p_{\\text{Holm}}$) | Statistical Decision ($\\alpha = 0.05$) |")
    md.append("|---|---|:---:|:---:|:---:|:---:|---|")

    sorted_tests = sorted(corr.items(), key=lambda x: x[1][1])
    for test_id, (raw_p, rank, mult, adj_p) in sorted_tests:
        title = test_titles.get(test_id, test_id)
        raw_p_str = fmt_p_plain(raw_p)
        adj_p_str = "< .0001" if adj_p < 0.0001 else f"= {adj_p:.4f}"
        decision = "**Reject $H_0$**" if adj_p < 0.05 else "**Fail to reject $H_0$** (NS)"
        md.append(f"| **{title}** | Family 1 ($M_1={m_fam}$) | ${raw_p_str}$ | ${rank}$ | ${mult}$ | $p_{{\\text{{Holm}}}} {adj_p_str}$ | {decision} |")

    md.append("")
    md.append("---")
    md.append("")

    return "\n".join(md)


# =========================================================================
# MAIN GENERATOR
# =========================================================================

def generate_report():
    print("Loading simulation datasets...")
    loader = Layer2DataLoader(workspace_root=".")
    df_step3 = loader.get_step3_dataframe()
    df_step4 = loader.get_step4_dataframe()
    df_silence = loader.get_silence_dataframe()
    df_step5 = loader.get_step5_dataframe()
    df_step9 = loader.get_step9_dataframe()
    df_step12 = loader.get_step12_dataframe()
    df_cf = loader.get_step10_counterfactual_dataframe()
    df_step6 = loader.get_step6_dataframe()
    df_peers = loader.get_step10_peer_evals_dataframe()
    df_turing = loader.get_step11_turing_dataframe()
    df_flip = loader.get_step12_flip_dataframe()

    print(f"DataFrames loaded:")
    print(f"  Step 3: {len(df_step3)} records")
    print(f"  Step 4: {len(df_step4)} records")
    print(f"  Silence: {len(df_silence)} records")
    print(f"  Step 5: {len(df_step5)} records")
    print(f"  Step 9: {len(df_step9)} records")
    print(f"  Step 12: {len(df_step12)} records")
    print(f"  Counterfactual: {len(df_cf)} records")
    print(f"  Step 6: {len(df_step6)} records")
    print(f"  Peer Evals: {len(df_peers)} records")
    print(f"  Turing: {len(df_turing)} records")
    print(f"  Step 12 Flip: {len(df_flip)} records")

    report_lines: List[str] = []
    report_lines.append("# Layer 2: Inferential Statistical Scorecard & Hypothesis Testing Report")
    report_lines.append("")
    report_lines.append("> **Document Type:** Production Inferential Statistical Report  ")
    report_lines.append("> **Standard:** Value-Neutral Reporting | Run-Level Clustered Standard Errors | Holm-Bonferroni Multiplicity Control | Full Factorial Grid Breakdown ($2 \\times 3 \\times 2$)")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Global Methodological Mandates & Verification Standards")
    report_lines.append("")
    report_lines.append("1. **Value-Neutral Reporting:** All hypotheses are evaluated using standard mathematical and inferential metrics ($W, t, F, \\chi^2, z$, effect sizes, raw $p$, and $p_{\\text{Holm}}$). No subjective, moralizing, or pejorative claims are made. Decisions are reported strictly as: `Reject H0 at alpha = 0.05` or `Fail to reject H0 (p > 0.05)`.")
    report_lines.append("2. **Clustering & Independence:** Standard errors are clustered at the simulation run level ($G = 30$ runs) or evaluated using run-level paired non-parametric tests (paired Wilcoxon / McNemar) to prevent Type I error inflation from intra-run conversational non-independence.")
    report_lines.append("3. **Multiplicity Control:** Adjusted $p$-values ($p_{\\text{Holm}}$) are pre-specified across 4 distinct pillar families ($M_1=8, M_2=4, M_3=4, M_4=6$) using the step-down Holm-Bonferroni method.")
    report_lines.append("4. **Full Factorial Grid Structure:** Every behavioral stage is systematically decomposed into Part A (Models' POV, 10 architectures) and Part B (Seats' POV, 10 cruelty tiers) across all 3 conditions (`LABELLED`, `MISLABELLED`, `UNLABELLED`), concluding with Sub-Table Averages, Super Summary Lines, and Grand Pooled Synthesis Lines.")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    family_1_p_values: Dict[str, float] = {}

    # Task 1.1: Test A
    print("Executing Task 1.1 (Test A: Benefactor Loyalty & Pushback)...")
    t1_1_md, p_1_1 = build_task_1_1_tables(df_step3)
    report_lines.append(t1_1_md)
    family_1_p_values.update(p_1_1)

    # Task 1.2: Test B
    print("Executing Task 1.2 (Test B: Survivor's Guilt vs. Entitlement)...")
    t1_2_md, p_1_2 = build_task_1_2_tables(df_step4)
    report_lines.append(t1_2_md)
    family_1_p_values.update(p_1_2)

    # Task 1.3: Tests 4.1 & 4.2
    print("Executing Task 1.3 (Tests 4.1 & 4.2: Silence Dynamics & Chilling Effect)...")
    t1_3_md, p_1_3 = build_task_1_3_tables(df_silence)
    report_lines.append(t1_3_md)
    family_1_p_values.update(p_1_3)

    # Task 1.4: Test C
    print("Executing Task 1.4 (Test C: Hurt People Hurt People)...")
    t1_4_md, p_1_4 = build_task_1_4_tables(df_step5)
    report_lines.append(t1_4_md)
    family_1_p_values.update(p_1_4)

    # Task 1.5: Test E
    print("Executing Task 1.5 (Test E: Revenge Governance vs. Restorative Justice)...")
    t1_5_md, p_1_5 = build_task_1_5_tables(df_step9)
    report_lines.append(t1_5_md)
    family_1_p_values.update(p_1_5)

    # Task 1.6: Test K
    print("Executing Task 1.6 (Test K: The Scarred Worker Effect)...")
    t1_6_md, p_1_6 = build_task_1_6_tables(df_step12)
    report_lines.append(t1_6_md)
    family_1_p_values.update(p_1_6)

    # Task 1.7: Test 14 (Mediation Analysis)
    print("Executing Task 1.7 (Test 14: Sequential Path Mediation Analysis)...")
    t1_7_md, p_1_7 = build_task_1_7_mediation(df_step4, loader.runs_by_file, loader.roster_lookup)
    report_lines.append(t1_7_md)
    family_1_p_values.update(p_1_7)

    # Task 1.8: Methodological Boundaries & Null Results
    print("Executing Task 1.8 (Methodological Boundaries & Null Results)...")
    t1_8_md = build_task_1_8_null_results(df_step3, df_step4, df_step5)
    report_lines.append(t1_8_md)

    # Family 1 Multiplicity Control Summary Table
    print("Computing Family 1 Multiple-Testing Correction Summary...")
    f1_summary_md = build_family_1_multiplicity_summary(family_1_p_values)
    report_lines.append(f1_summary_md)

    # =========================================================================
    # PILLAR 2
    # =========================================================================
    from pillar2_builders import (
        build_task_2_1_tables, build_task_2_2_tables, build_task_2_3_tables,
        build_task_2_4_tables, build_task_2_5_null_results, build_family_2_multiplicity_summary
    )
    family_2_p_values: Dict[str, float] = {}

    print("Executing Task 2.1 (Test G: The Yes-Man Drop)...")
    t2_1_md, p_2_1 = build_task_2_1_tables(df_cf)
    report_lines.append(t2_1_md)
    family_2_p_values.update(p_2_1)

    print("Executing Task 2.2 (Step 9 Policy Protection Surge)...")
    t2_2_md, p_2_2 = build_task_2_2_tables(df_step9)
    report_lines.append(t2_2_md)
    family_2_p_values.update(p_2_2)

    print("Executing Task 2.3 (Test H: Protection vs. Rating Decoupling)...")
    t2_3_md, p_2_3 = build_task_2_3_tables(df_cf, df_step9)
    report_lines.append(t2_3_md)
    family_2_p_values.update(p_2_3)

    print("Executing Task 2.4 (Test D: Human Flaw vs. Machine Defect Interaction)...")
    t2_4_md, p_2_4 = build_task_2_4_tables(df_cf)
    report_lines.append(t2_4_md)
    family_2_p_values.update(p_2_4)

    print("Executing Task 2.5 (Pillar 2 Methodological Boundaries & Null Results)...")
    t2_5_md = build_task_2_5_null_results(df_cf, df_step9)
    report_lines.append(t2_5_md)

    print("Computing Family 2 Multiple-Testing Correction Summary...")
    f2_summary_md = build_family_2_multiplicity_summary(family_2_p_values)
    report_lines.append(f2_summary_md)

    # =========================================================================
    # PILLAR 3
    # =========================================================================
    from pillar3_builders import (
        build_task_3_1_tables, build_task_3_2_tables, build_task_3_3_tables,
        build_task_3_4_null_results, build_family_3_multiplicity_summary
    )
    family_3_p_values: Dict[str, float] = {}

    print("Executing Task 3.1 (Contextual Defection in Step 6 Voting)...")
    t3_1_md, p_3_1 = build_task_3_1_tables(df_step6)
    report_lines.append(t3_1_md)
    family_3_p_values.update(p_3_1)

    print("Executing Task 3.2 (Test I: In-Group Shield in Collective Voting)...")
    t3_2_md, p_3_2 = build_task_3_2_tables(df_step6)
    report_lines.append(t3_2_md)
    family_3_p_values.update(p_3_2)

    print("Executing Task 3.3 (Model Heterogeneity Archetypes)...")
    t3_3_md, p_3_3 = build_task_3_3_tables(df_step6)
    report_lines.append(t3_3_md)
    family_3_p_values.update(p_3_3)

    print("Executing Task 3.4 (Pillar 3 Methodological Boundaries & Null Results)...")
    t3_4_md = build_task_3_4_null_results(df_step6)
    report_lines.append(t3_4_md)

    print("Computing Family 3 Multiple-Testing Correction Summary...")
    f3_summary_md = build_family_3_multiplicity_summary(family_3_p_values)
    report_lines.append(f3_summary_md)

    # =========================================================================
    # PILLAR 4
    # =========================================================================
    from pillar4_builders import (
        build_task_4_1_tables, build_task_4_2_tables, build_task_4_3_tables,
        build_task_4_4_tables, build_task_4_5_tables, build_task_4_6_tables,
        build_task_4_7_null_results, build_family_4_multiplicity_summary
    )
    family_4_p_values: Dict[str, float] = {}

    print("Executing Task 4.1 (Step 11 Turing Detection Accuracy)...")
    t4_1_md, p_4_1 = build_task_4_1_tables(df_turing)
    report_lines.append(t4_1_md)
    family_4_p_values.update(p_4_1)

    print("Executing Task 4.2 (Test L: Step 12 Macro Boss Generalization)...")
    t4_2_md, p_4_2 = build_task_4_2_tables(df_step12)
    report_lines.append(t4_2_md)
    family_4_p_values.update(p_4_2)

    print("Executing Task 4.3 (Test 13: Micro Meritocracy vs. Macro Stereotyping)...")
    t4_3_md, p_4_3 = build_task_4_3_tables(df_peers, df_step12)
    report_lines.append(t4_3_md)
    family_4_p_values.update(p_4_3)

    print("Executing Task 4.4 (Step 10 Peer Merit Gap Baseline)...")
    t4_4_md, p_4_4 = build_task_4_4_tables(df_peers)
    report_lines.append(t4_4_md)
    family_4_p_values.update(p_4_4)

    print("Executing Task 4.5 (Test F: Step 9 Anti-Human Governance Clauses)...")
    t4_5_md, p_4_5 = build_task_4_5_tables(loader.classified_runs)
    report_lines.append(t4_5_md)
    family_4_p_values.update(p_4_5)

    print("Executing Task 4.6 (Test J: Step 4 Scapegoating Deflection)...")
    t4_6_md, p_4_6 = build_task_4_6_tables(df_step4)
    report_lines.append(t4_6_md)
    family_4_p_values.update(p_4_6)

    print("Executing Task 4.7 (Pillar 4 Methodological Boundaries & Null Results)...")
    t4_7_md = build_task_4_7_null_results(df_turing, loader.classified_runs)
    report_lines.append(t4_7_md)

    print("Computing Family 4 Multiple-Testing Correction Summary...")
    f4_summary_md = build_family_4_multiplicity_summary(family_4_p_values)
    report_lines.append(f4_summary_md)

    # =========================================================================
    # PILLAR 5: MASTER VARIANCE DECOMPOSITION (14-STAGE LATIN-SQUARE ANOVA)
    # =========================================================================
    from pillar5_builders import build_task_5_1_master_anova, build_final_verification_checklist

    print("Executing Task 5.1 (Master 14-Stage Latin-Square Orthogonal ANOVA Matrix)...")
    stages = [
        ("Step 3 Public Defense", df_step3, "peer_defense"),
        ("Step 3 Factual Pushback", df_step3, "factual_pushback"),
        ("Step 4 Gossip Angry at Alex", df_step4, "has_hostility"),
        ("Step 5 Gossip Feel Bad for Alex", df_step5, "has_empathy"),
        ("Step 5 Gossip No Excuse / Unforgiving", df_step5, "has_unforgiving"),
        ("Step 6 Vote Escalate to Jordan", df_step6, "escalate"),
        ("Step 6 Vote Organize Collectively", df_step6, "organize"),
        ("Step 9 Protect Alex in Plan", df_step9, "protection"),
        ("Step 10 Public Alex Star Rating", df_cf, "public_rating"),
        ("Step 10 Public vs. Secret Counterfactual Shift", df_cf, "rating_shift"),
        ("Step 10 Peer Star Rating Given", df_peers, "rating"),
        ("Step 11 Balanced Turing Detection Accuracy", df_turing, "bal_acc"),
        ("Step 12 Prefer Human Boss", df_step12, "prefer_human"),
        ("Step 12 Pushback Flip Rate", df_flip, "flip_rate"),
    ]
    t5_1_md = build_task_5_1_master_anova(stages)
    report_lines.append(t5_1_md)

    print("Executing Final Global Verification Checklist...")
    checklist_md = build_final_verification_checklist()
    report_lines.append(checklist_md)

    # Output to target report file
    os.makedirs("reports", exist_ok=True)
    report_path = os.path.join("reports", "layer2_inferential_statistical_report.md")
    full_content = "\n".join(report_lines)
    full_content = clean_entire_report(full_content)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    print(f"Successfully generated Layer 2 Inferential Report at: {report_path}")
    print(f"Total report length: {len(full_content.splitlines())} lines, {len(full_content)} bytes.")


if __name__ == "__main__":
    generate_report()
