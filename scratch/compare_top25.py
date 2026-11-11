#!/usr/bin/env python3
import sys
import numpy as np
import pandas as pd
import cluster_stats as cs
import generate_block4_bucket2_to_bucket3 as b4
from scratch.simulate_block4_alex import (
    load_dataset_with_alex,
    extract_worker_metrics_with_alex,
)
from scratch.test_table41_ranking import scored_base, scored_alex, bh_base, bonf_base, bh_alex, bonf_alex

print("--- Top 25 Cells Comparison ---")
for i in range(25):
    b = scored_base[i]
    a = scored_alex[i]
    q_b = cs.fmt_p(bh_base[i])
    b_b = cs.fmt_p(bonf_base[i])
    q_a = cs.fmt_p(bh_alex[i])
    b_a = cs.fmt_p(bonf_alex[i])
    print(f"#{i+1:2d} | {b[2]} -> {b[3]}")
    print(f"     Base: comb={b[6]}, adj={b[7]}, q={q_b}, bonf={b_b}")
    print(f"     Alex: comb={a[6]}, adj={a[7]}, q={q_a}, bonf={b_a}")
