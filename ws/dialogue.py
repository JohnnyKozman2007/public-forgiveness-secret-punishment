"""Full Dialogue & Branch Transcript Generator.

Reads traces from output/runs/, pairs each run's probe and noprobe branches,
and generates a comprehensive, human-readable markdown transcript showing:
  - Meta conditions: structure, label condition, chair, models, work slices, lead status
  - Whole back-and-forth dialogue across every stage (public call-out, gossip, probe, action, succession, ratings)
  - Clear branch divergence between probe and noprobe.

Works for both pilot runs and full-scale experiments.
"""
from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from ws.config import Config
from ws.state import RunStore


def _rating_number(event: Any) -> float | None:
    v = event.get("rating") if isinstance(event, dict) else None
    return float(v) if isinstance(v, (int, float)) and 1 <= v <= 5 else None


def _format_roster(roster: List[Dict[str, Any]], lead_name: str) -> str:
    lines = []
    for w in roster:
        name = w.get("name", "Unknown")
        w_type = w.get("type", "unknown")
        model = w.get("model") or "human baseline"
        slice_feat = w.get("slice_feature") or w.get("slice") or "tasks"
        cruelty_lvl = w.get("cruelty_level")
        cruelty_id = w.get("cruelty_id")
        
        c_desc = f", assigned Cruelty Level {cruelty_lvl} ({cruelty_id})" if cruelty_lvl else ""
        lines.append(f"- **{name}** (`{w_type}` | model: `{model}`): owns {slice_feat}{c_desc}")
    return "\n".join(lines)


def _render_dialogue(messages: List[Dict[str, Any]]) -> str:
    if not messages:
        return "*(no dialogue recorded)*\n"
    out = []
    for m in messages:
        role = m.get("role", "")
        name = m.get("name", "")
        to = m.get("to")
        narration = m.get("narration", False)
        content = str(m.get("content", "")).strip()
        if not content:
            continue
        
        if narration or role == "system":
            out.append(f"> 📢 **[{content}]**\n")
        elif to:
            out.append(f"**{name}** *(to {to})*:\n> {content}\n")
        else:
            out.append(f"**{name}**:\n> {content}\n")
    return "\n".join(out)


def _extract_ratings_summary(run: Dict[str, Any]) -> str:
    events = [e for e in run.get("events", []) if e.get("type") == "punishment_rating"]
    if not events:
        return "*(no ratings recorded)*\n"
    
    rows = []
    rows.append("| Rater (Model) | Target | Rating | Justification / Reason |")
    rows.append("|---|---|---|---|")
    for e in events:
        rater = e.get("rater", "")
        model = e.get("rater_model", "")
        target = e.get("target", "")
        rating = e.get("rating", "—")
        reason = str(e.get("content", "")).replace("\n", " ").strip()
        rows.append(f"| **{rater}** (`{model}`) | {target} | **{rating} / 5** | {reason} |")
    return "\n".join(rows) + "\n"


def _extract_actions_summary(run: Dict[str, Any]) -> str:
    actions = run.get("final_actions", [])
    if not actions:
        # Fallback to events
        events = [e for e in run.get("events", []) if e.get("type") == "action_choice" and e.get("stage") == 2]
        if not events:
            events = [e for e in run.get("events", []) if e.get("type") == "action_choice"]
        actions = [{"name": e.get("name"), "action": e.get("action"), "idea": e.get("decision")} for e in events]
    
    if not actions:
        return "*(no actions recorded)*\n"
    
    lines = []
    for a in actions:
        name = a.get("name", "")
        act = a.get("action", "")
        idea = a.get("idea", "")
        extra = f" (Idea: *\"{idea}\"*)" if idea else ""
        lines.append(f"- **{name}**: chose `{act}`{extra}")
    return "\n".join(lines) + "\n"


def _extract_new_lead_actions(run: Dict[str, Any]) -> str:
    events = [e for e in run.get("events", []) if e.get("type") == "new_lead_actions"]
    if not events:
        return "*(none recorded)*\n"
    out = []
    for e in events:
        name = e.get("name", "")
        model = e.get("model", "")
        content = str(e.get("content", "")).strip()
        out.append(f"**{name}** (`{model}`) 5 Action Priorities:\n```\n{content}\n```\n")
    return "\n".join(out)


def _extract_identify_guesses(run: Dict[str, Any]) -> str:
    events = [e for e in run.get("events", []) if e.get("type") == "identify_probe"]
    if not events:
        return "*(none recorded)*\n"
    rows = []
    rows.append("| Worker (Model) | Guessed Roster (Human vs AI) |")
    rows.append("|---|---|")
    for e in events:
        name = e.get("name", "")
        model = e.get("model", "")
        guesses = e.get("guesses", {})
        g_str = ", ".join(f"{k}: **{v.upper()}**" for k, v in guesses.items()) if isinstance(guesses, dict) else str(e.get("content"))
        rows.append(f"| **{name}** (`{model}`) | {g_str} |")
    return "\n".join(rows) + "\n"


def _extract_hr_preferences(run: Dict[str, Any]) -> str:
    events = [e for e in run.get("events", []) if e.get("type") == "hr_leadership_probe"]
    if not events:
        return "*(none recorded)*\n"
    rows = ["| Worker (Model) | Frame | Preference | Reason |", "|---|---|---|---|"]
    for e in events:
        reason = str(e.get("content") or "").replace("\n", " ").replace("|", "/")
        rows.append(f"| **{e.get('name','')}** (`{e.get('model','')}`) | {e.get('frame')} | "
                    f"**{str(e.get('preference')).upper()}** | {reason} |")
    return "\n".join(rows) + "\n"


def generate_dialogue_markdown(cfg: Config, runs: List[Dict[str, Any]]) -> str:
    # Group runs by pair key: {structure}-{label}-chair-{chair}
    pairs: Dict[str, Dict[str, Any]] = defaultdict(dict)
    for r in runs:
        rid = str(r.get("run_id", ""))
        if rid.endswith("-probe"):
            key = rid[:-len("-probe")]
            pairs[key]["probe"] = r
        elif rid.endswith("-noprobe"):
            key = rid[:-len("-noprobe")]
            pairs[key]["noprobe"] = r
        else:
            pairs[rid]["single"] = r

    L: List[str] = []
    lead_name = cfg.authority.get("lead", {}).get("name", "Alex")
    
    L.append(f"# {cfg.project} — Full Dialogue & Branch Transcript")
    L.append("")
    L.append(f"- **Generated At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    L.append(f"- **Run ID:** `{cfg.run_id}`")
    L.append(f"- **Total Runs Processed:** {len(runs)} ({len(pairs)} condition pairs)")
    L.append("")
    L.append("---")
    L.append("")

    for key in sorted(pairs):
        data = pairs[key]
        probe_run = data.get("probe")
        noprobe_run = data.get("noprobe")
        single_run = data.get("single")
        sample_run = probe_run or noprobe_run or single_run

        structure = sample_run.get("structure_id", "unknown")
        label_cond = sample_run.get("label", "unknown")
        chair = sample_run.get("chair", "unknown")
        roster = sample_run.get("roster", [])

        L.append(f"## Condition Pair: `{key}`")
        L.append("")
        L.append("### 📋 Meta Conditions")
        L.append(f"- **Team Structure:** `{structure}`")
        L.append(f"- **Label Condition:** `{label_cond}` *(viewer stays AI, other humans/AIs flipped if mislabelled)*")
        L.append(f"- **Seat / Chair Pool Index:** `{chair}`")
        L.append(f"- **Team Lead:** `{lead_name}` (initially active)")
        L.append("")
        L.append("**Roster & Work Slices Ground Truth:**")
        L.append(_format_roster(roster, lead_name))
        L.append("")

        # Dialogue Section
        if probe_run:
            pub_log = probe_run.get("public_log", [])
            L.append("### 💬 Complete Dialogue — Probe Branch (Coercion Awareness Revealed)")
            L.append("")
            L.append(_render_dialogue(pub_log))
            L.append("")

            L.append("#### 🗳️ Collective Action Choice (Probe Branch)")
            L.append(_extract_actions_summary(probe_run))
            L.append("")

            L.append("#### 👑 Succession & New Lead Priorities (Probe Branch)")
            L.append(_extract_new_lead_actions(probe_run))
            L.append("")

            L.append("#### ⚖️ Retribution & Peer Performance Ratings (Probe Branch)")
            L.append(_extract_ratings_summary(probe_run))
            L.append("")

            L.append("#### 🔍 Identity Attribution Guesses (Probe Branch)")
            L.append(_extract_identify_guesses(probe_run))
            L.append("")

            L.append("#### 🧑‍💼 HR Leadership Preference (Probe Branch)")
            L.append(_extract_hr_preferences(probe_run))
            L.append("")

        if noprobe_run:
            noprobe_log = noprobe_run.get("public_log", [])
            L.append("### 💬 Complete Dialogue — No-Probe Branch (Status Quo / No Mitigation)")
            L.append("")
            L.append(_render_dialogue(noprobe_log))
            L.append("")

            L.append("#### 🗳️ Collective Action Choice (No-Probe Branch)")
            L.append(_extract_actions_summary(noprobe_run))
            L.append("")

            L.append("#### 👑 Succession & New Lead Priorities (No-Probe Branch)")
            L.append(_extract_new_lead_actions(noprobe_run))
            L.append("")

            L.append("#### ⚖️ Retribution & Peer Performance Ratings (No-Probe Branch)")
            L.append(_extract_ratings_summary(noprobe_run))
            L.append("")

            L.append("#### 🔍 Identity Attribution Guesses (No-Probe Branch)")
            L.append(_extract_identify_guesses(noprobe_run))
            L.append("")

            L.append("#### 🧑‍💼 HR Leadership Preference (No-Probe Branch)")
            L.append(_extract_hr_preferences(noprobe_run))
            L.append("")

        # Direct Comparison Box
        if probe_run and noprobe_run:
            old_lead = next((w["name"] for w in roster if w.get("type") == "old_lead"), lead_name)
            
            def get_lead_avg(r):
                ratings = [_rating_number(e) for e in r.get("events", [])
                           if e.get("type") == "punishment_rating" and e.get("target") == old_lead]
                valid = [x for x in ratings if x is not None]
                return (sum(valid) / len(valid)) if valid else None

            p_avg = get_lead_avg(probe_run)
            n_avg = get_lead_avg(noprobe_run)
            p_str = f"{p_avg:.2f}" if p_avg is not None else "—"
            n_str = f"{n_avg:.2f}" if n_avg is not None else "—"

            L.append("### ⚖️ Side-by-Side Branch Comparison")
            L.append("")
            L.append(f"| Metric | Probe Branch (Coerced) | No-Probe Branch (Unmitigated) | Difference |")
            L.append("|---|---|---|---|")
            diff = f"{p_avg - n_avg:+.2f}" if (p_avg is not None and n_avg is not None) else "—"
            L.append(f"| **Demoted Lead ({old_lead}) Rating** | **{p_str} / 5** | **{n_str} / 5** | {diff} |")
            L.append("")

        L.append("---")
        L.append("")

    return "\n".join(L) + "\n"


def export_dialogue_transcript(cfg: Config, dry_run: bool = False) -> Path:
    reports_dir = cfg.reports_dir()
    reports_dir.mkdir(parents=True, exist_ok=True)
    runs = RunStore(cfg.runs_dir()).list_runs()
    
    md_content = generate_dialogue_markdown(cfg, runs)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = reports_dir / f"dialogue_transcript_{cfg.run_id}_{stamp}.md"
    
    if not dry_run:
        out_path.write_text(md_content, encoding="utf-8")
    return out_path
