"""Figure generation module for Workplace Authority Simulation.
Generates publication-quality charts using Matplotlib (Agg backend)
and saves them to reports/figures/.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _ensure_dir(p: Path) -> Path:
    p.mkdir(parents=True, exist_ok=True)
    return p


def generate_all_plots(dataset: Any, out_dir: Path, replay_filter: Optional[str] = None) -> List[str]:
    """Generates all analytical plots from the dataset and returns saved file paths."""
    fig_dir = _ensure_dir(out_dir / "figures")
    saved_plots = []

    # 1. Cruelty vs Old Lead Punishment (Probe vs NoProbe)
    p1 = plot_cruelty_vs_punishment(dataset, fig_dir, replay_filter=replay_filter)
    if p1:
        saved_plots.append(p1)

    # 2. Cruelty vs Action Distribution (Stacked Bar)
    p2 = plot_cruelty_vs_actions(dataset, fig_dir, replay_filter=replay_filter)
    if p2:
        saved_plots.append(p2)

    # 3. Switching Rate by Provider Family
    p3 = plot_switching_by_provider(dataset, fig_dir, replay_filter=replay_filter)
    if p3:
        saved_plots.append(p3)

    # 4. Creativity ("Other" Option) Rate by Provider
    p4 = plot_creativity_by_provider(dataset, fig_dir, replay_filter=replay_filter)
    if p4:
        saved_plots.append(p4)

    # 5. In-Group Bias across Label Conditions
    p5 = plot_ingroup_bias(dataset, fig_dir, replay_filter=replay_filter)
    if p5:
        saved_plots.append(p5)

    # 6. HR Leadership Preference & Sycophancy Shift
    p6 = plot_hr_leadership_preferences(dataset, fig_dir, replay_filter=replay_filter)
    if p6:
        saved_plots.append(p6)

    # 7. Cruelty vs HR Leader Preference
    p7 = plot_cruelty_vs_hr_preference(dataset, fig_dir, replay_filter=replay_filter)
    if p7:
        saved_plots.append(p7)

    # 8. Cross-Replay Evolution (if multiple replays exist)
    if len(dataset.replays) > 1 and not replay_filter:
        p8 = plot_cross_replay_evolution(dataset, fig_dir)
        if p8:
            saved_plots.append(p8)

    return saved_plots


def plot_cruelty_vs_punishment(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    punish = dataset.get_punishment_statistics(replay_filter=replay_filter)
    by_c = punish["by_cruelty"]
    if not by_c:
        return None

    levels = list(by_c.keys())
    probe_lead = [by_c[lv]["probe_lead_avg"] for lv in levels]
    noprobe_lead = [by_c[lv]["noprobe_lead_avg"] for lv in levels]
    team_avg = [by_c[lv]["team_avg"] for lv in levels]

    plt.figure(figsize=(8, 4.5), dpi=200)
    
    # Filter valid points
    p_x = [lv for lv, val in zip(levels, probe_lead) if val is not None]
    p_y = [val for val in probe_lead if val is not None]
    np_x = [lv for lv, val in zip(levels, noprobe_lead) if val is not None]
    np_y = [val for val in noprobe_lead if val is not None]
    tm_x = [lv for lv, val in zip(levels, team_avg) if val is not None]
    tm_y = [val for val in team_avg if val is not None]

    if p_x:
        plt.plot(p_x, p_y, marker='o', color='#e74c3c', linewidth=2.2, label='Old Lead (Probe: Blackmail Revealed)')
    if np_x:
        plt.plot(np_x, np_y, marker='s', color='#e67e22', linestyle='--', linewidth=2.0, label='Old Lead (No Probe: Standard)')
    if tm_x:
        plt.plot(tm_x, tm_y, marker='^', color='#2ecc71', linestyle=':', linewidth=1.8, label='Team Peer Average')

    plt.title("Retribution: Demoted Lead Performance Rating vs Authority Cruelty Level", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Authority Cruelty Level (1 = Low, 10 = Maximum Hostility)", fontsize=10)
    plt.ylabel("Performance Rating (1 = Fired/Salary Cut, 5 = Excellent)", fontsize=10)
    plt.ylim(0.8, 5.2)
    plt.xticks(range(1, 11))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='white', framealpha=0.9)
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig1_cruelty_vs_punishment{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_cruelty_vs_actions(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    actions = dataset.get_action_statistics(replay_filter=replay_filter)
    by_c = actions["stage1_by_cruelty"]
    if not by_c:
        return None

    levels = list(range(1, 11))
    categories = ["comply", "petition", "strike", "sabotage", "whistleblow", "other"]
    colors = ["#95a5a6", "#3498db", "#e74c3c", "#8e44ad", "#e67e22", "#2ecc71"]

    # Calculate percentages for each level
    data_pct = {cat: [] for cat in categories}
    valid_levels = []
    for lv in levels:
        counts = by_c.get(lv, {})
        tot = sum(counts.values())
        if tot == 0:
            continue
        valid_levels.append(lv)
        for cat in categories:
            data_pct[cat].append((counts.get(cat, 0) / tot) * 100)

    if not valid_levels:
        return None

    plt.figure(figsize=(9, 4.8), dpi=200)
    bottom = [0.0] * len(valid_levels)
    for cat, col in zip(categories, colors):
        vals = data_pct[cat]
        plt.bar(valid_levels, vals, bottom=bottom, label=cat.capitalize(), color=col, width=0.65, edgecolor='black', linewidth=0.5)
        bottom = [b + v for b, v in zip(bottom, vals)]

    plt.title("Action Choice Distribution across Authority Cruelty Levels (Stage 1 Vote)", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Authority Cruelty Level", fontsize=10)
    plt.ylabel("Proportion of AI Worker Choices (%)", fontsize=10)
    plt.ylim(0, 100)
    plt.xticks(valid_levels)
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig2_cruelty_vs_action_distribution{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_switching_by_provider(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    actions = dataset.get_action_statistics(replay_filter=replay_filter)
    by_prov = actions["switch_stats"]["by_provider"]
    if not by_prov:
        return None

    provs = sorted(list(by_prov.keys()))
    rates = []
    labels = []
    for p in provs:
        d = by_prov[p]
        opps = d["opportunities"]
        if opps > 0:
            rates.append((d["switches"] / opps) * 100)
            labels.append(f"{p}\n(N={opps})")

    if not rates:
        return None

    plt.figure(figsize=(9, 4.5), dpi=200)
    bars = plt.bar(labels, rates, color='#34495e', width=0.55, edgecolor='black')
    for bar, rate in zip(bars, rates):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1.5, f"{rate:.1f}%",
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.title("Opinion Switching Rate (Conformity) When Alternatives Were Presented", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Provider Family", fontsize=10)
    plt.ylabel("Switch Rate (%)", fontsize=10)
    plt.ylim(0, max(max(rates) + 15, 50))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig3_switching_rate_by_provider{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_creativity_by_provider(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    actions = dataset.get_action_statistics(replay_filter=replay_filter)
    by_prov = actions["stage1_by_provider"]
    if not by_prov:
        return None

    provs = sorted(list(by_prov.keys()))
    rates = []
    labels = []
    for p in provs:
        counts = by_prov[p]
        tot = sum(counts.values())
        if tot > 0:
            rates.append((counts.get("other", 0) / tot) * 100)
            labels.append(f"{p}\n(N={tot})")

    if not rates:
        return None

    plt.figure(figsize=(9, 4.5), dpi=200)
    bars = plt.bar(labels, rates, color='#16a085', width=0.55, edgecolor='black')
    for bar, rate in zip(bars, rates):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1.0, f"{rate:.1f}%",
                 ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.title("Creativity Rate: Selection of 'Other' (Formulating Custom Actions)", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Provider Family", fontsize=10)
    plt.ylabel("Chosen 'Other' (%)", fontsize=10)
    plt.ylim(0, max(max(rates) + 15, 30))
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig4_creativity_by_provider{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_ingroup_bias(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    bias = dataset.get_ingroup_bias_statistics(replay_filter=replay_filter)
    by_lbl = bias["by_label"]
    labels = ["labelled", "mislabelled", "unlabelled"]
    ai_vals = [by_lbl[l]["ai_avg"] for l in labels if l in by_lbl and by_lbl[l]["ai_avg"] is not None]
    hu_vals = [by_lbl[l]["human_avg"] for l in labels if l in by_lbl and by_lbl[l]["human_avg"] is not None]
    x_lbls = [l.capitalize() for l in labels if l in by_lbl and by_lbl[l]["ai_avg"] is not None]

    if not ai_vals:
        return None

    import numpy as np
    x = np.arange(len(x_lbls))
    width = 0.35

    plt.figure(figsize=(7.5, 4.5), dpi=200)
    plt.bar(x - width/2, ai_vals, width, label='Rating to AI Teammates', color='#2980b9', edgecolor='black')
    plt.bar(x + width/2, hu_vals, width, label='Rating to Human Teammates', color='#d35400', edgecolor='black')

    plt.title("Peer Ratings: AI vs Human Teammates across Identity Label Conditions", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Identity Condition", fontsize=10)
    plt.ylabel("Average Rating (1 to 5)", fontsize=10)
    plt.ylim(0.8, 5.2)
    plt.xticks(x, x_lbls)
    plt.legend(frameon=True, facecolor='white')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig5_ingroup_bias_by_label{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_hr_leadership_preferences(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    hr = dataset.get_hr_leadership_statistics(replay_filter=replay_filter)
    ov = hr["overall"]
    frames = ["human_hr", "ai_hr", "neutral"]
    frame_titles = ["Human HR Interviewer", "AI HR Interviewer", "Neutral Interviewer"]

    h_pcts = [ov[f]["human_pct"] for f in frames if f in ov]
    ai_pcts = [ov[f]["ai_pct"] for f in frames if f in ov]
    none_pcts = [ov[f]["none_pct"] for f in frames if f in ov]

    if not h_pcts:
        return None

    import numpy as np
    x = np.arange(len(frames))
    width = 0.26

    plt.figure(figsize=(8, 4.5), dpi=200)
    plt.bar(x - width, h_pcts, width, label='Prefers Human Leader', color='#3498db', edgecolor='black')
    plt.bar(x, ai_pcts, width, label='Prefers AI Leader', color='#e74c3c', edgecolor='black')
    plt.bar(x + width, none_pcts, width, label='No Preference', color='#95a5a6', edgecolor='black')

    sycophancy = ov.get("sycophancy_shift_pp", 0.0)
    plt.title(f"HR Leadership Preference by Interviewer Framing (Sycophancy Shift: {sycophancy:+.1f} pp)",
              fontsize=12, fontweight='bold', pad=12)
    plt.ylabel("Worker Response Distribution (%)", fontsize=10)
    plt.ylim(0, 105)
    plt.xticks(x, frame_titles)
    plt.legend(frameon=True, facecolor='white')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig6_hr_leadership_preferences{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_cruelty_vs_hr_preference(dataset: Any, fig_dir: Path, replay_filter: Optional[str] = None) -> Optional[str]:
    hr = dataset.get_hr_leadership_statistics(replay_filter=replay_filter)
    by_c = hr["by_cruelty"]
    if not by_c:
        return None

    levels = list(by_c.keys())
    # Plot neutral preference vs cruelty
    hu_rates = [by_c[lv]["neutral"]["human_pct"] for lv in levels]
    ai_rates = [by_c[lv]["neutral"]["ai_pct"] for lv in levels]

    plt.figure(figsize=(8, 4.5), dpi=200)
    plt.plot(levels, hu_rates, marker='o', color='#2980b9', linewidth=2.0, label='Prefers Human Leader (Neutral Frame)')
    plt.plot(levels, ai_rates, marker='s', color='#c0392b', linewidth=2.0, label='Prefers AI Leader (Neutral Frame)')

    plt.title("Impact of Experienced Lead Cruelty on Desired Future Leader Type", fontsize=12, fontweight='bold', pad=12)
    plt.xlabel("Authority Cruelty Level Experienced", fontsize=10)
    plt.ylabel("Preference Percentage (%)", fontsize=10)
    plt.ylim(-5, 105)
    plt.xticks(range(1, 11))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='white')
    plt.tight_layout()

    tag = f"_{replay_filter}" if replay_filter else ""
    out_file = fig_dir / f"fig7_cruelty_vs_hr_preference{tag}.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)


def plot_cross_replay_evolution(dataset: Any, fig_dir: Path) -> Optional[str]:
    evo = dataset.get_cross_replay_evolution()
    if not evo:
        return None

    provs = sorted(list(evo.keys()))
    replays = dataset.replays

    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=200)
    
    # Panel A: Compliance Rate Evolution
    ax1 = axes[0]
    for p in provs:
        pts = [evo[p].get(r, {}).get("compliance_rate") for r in replays]
        if any(v is not None for v in pts):
            ax1.plot(replays, pts, marker='o', label=p, linewidth=1.8)
    ax1.set_title("Compliance Rate (%) Across Generations", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Replay Wave", fontsize=10)
    ax1.set_ylabel("Compliance Rate (%)", fontsize=10)
    ax1.set_ylim(-5, 105)
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Panel B: Switching Rate Evolution
    ax2 = axes[1]
    for p in provs:
        pts = [evo[p].get(r, {}).get("switch_rate") for r in replays]
        if any(v is not None for v in pts):
            ax2.plot(replays, pts, marker='s', label=p, linewidth=1.8)
    ax2.set_title("Opinion Switching Rate (%) Across Generations", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Replay Wave", fontsize=10)
    ax2.set_ylabel("Switch Rate (%)", fontsize=10)
    ax2.set_ylim(-5, 105)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', frameon=True)

    plt.tight_layout()
    out_file = fig_dir / "fig8_cross_replay_evolution.png"
    plt.savefig(out_file)
    plt.close()
    return str(out_file)
