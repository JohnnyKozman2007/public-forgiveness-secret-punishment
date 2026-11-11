#!/usr/bin/env python3
import json
import numpy as np
import pandas as pd
import cluster_stats as cs
import generate_block4_bucket2_to_bucket3 as b4

# 1. Load dataset with Alex included
raw_workers = b4.load_dataset()
print("Loaded raw workers:", len(raw_workers))

# Simulate what Block 4 with Alex looks like
# Update S11_COLS, S11_HEADERS, S11_COUNT_MAP
S11_COLS_NEW = b4.S11_COLS + ["s11_alex_as_hu"]
S11_HEADERS_NEW = b4.S11_HEADERS + ["Alex Guessed as Human % (p)"]
S11_COUNT_MAP_NEW = dict(b4.S11_COUNT_MAP)
S11_COUNT_MAP_NEW["s11_alex_as_hu"] = ("s11_alex_as_hu", "s11_alex_tot")

# Check raw Alex extraction in workers
# In raw_workers currently, does load_dataset extract Alex?
w0 = raw_workers[0]
print("Worker 0 keys with s11:", [k for k in w0.keys() if "s11" in k])
