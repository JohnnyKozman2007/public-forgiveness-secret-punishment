# Project: workplace-sim Alex Substrate Perception Integration

## Architecture
- **Data Ingestion**: `output/runs/*.json` (60 simulation runs, 600 worker trajectories) containing `identify_probe` Step 11 events. In roster, 20 coworkers have `type in ("human", "ai")` and Alex has `type == "old_lead"`.
- **Shared Data Loader & Statistics**:
  - `generate_block1_meta_to_all_buckets.py` provides shared utilities `load_dataset()`, `extract_worker_metrics()`, `S11_COLS`, `S11_HEADERS`, `S11_NAMES`, and `RATIO_MAP`.
  - `cluster_stats.py` provides `PermEngine`, `outcome_matrices`, and `assoc_test` (CR2 cluster-robust WLS).
- **Report Generators (Sequential Execution)**:
  - Block 5 (`generate_block5_seat_vs_model.py`): Model vs. Seat variance competition (Part 1), within-model seat sensitivity (Part 2), $10 \times 10$ joint interaction matrices (Part 3), Appendix A ICC diagnostics.
  - Block 1 (`generate_block1_meta_to_all_buckets.py`): Meta-conditions (Label, Probe, Condition) to Buckets 1–3, Table 5.1 multiple testing ($M=339$).
  - Block 3 (`generate_block3_bucket1_to_bucket3.py`): Bucket 1 (Steps 3, 4, 5) to Bucket 3 (Step 11), Table 5.1.
  - Block 4 (`generate_block4_bucket2_to_bucket3.py`): Bucket 2 (Steps 6, 9) to Bucket 3 (Step 11), Table 4.1.
  - Master Report (`generate_master_report.py`): Standalone master report synthesizing all blocks and Step 11 identification.
  - All Meta Reports (`generate_all_meta_reports.py`): Standalone meta report aggregating experimental conditions.
- **Verification Engine**:
  - `verify_coworker_baselines.py` and `reports/.baseline_coworker_cache.json`: Verifies 20-coworker metrics preservation across all 7 reports.
  - E2E Test Suite (`test_alex_integration.py`): Requirement-driven tests for R1, R2, R3, statistical correctness, and execution cleanliness.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Raw Alex Extraction & Denominator Mapping | Extract Alex guesses from `identify_probe` where `name == "Alex"`; map `s11_alex_as_hu: ("s11_alex_as_hu", "s11_alex_tot")` in `RATIO_MAP` | M1 | survey |
| 2 | Block 5 Part 1 Variance Competition | Incorporate `s11_alex_as_hu` into Tables 1.1, 1.2, 1.3, and Dominance Ranking Table 1.4 | M1 | survey |
| 3 | Block 5 Part 2 Seat Sensitivity | Incorporate `s11_alex_as_hu` into Step 11 Tables 2.1.8, 2.2.7, 2.3.8, 2.4A, 2.4B | M1 | survey |
| 4 | Block 5 Part 3 Joint Interaction Matrix | Add Table 3.21 $10 \times 10$ matrix for `s11_alex_as_hu` and renumber subsequent matrices (3.22–3.24) | M1 | survey |
| 5 | Block 5 Appendix A Diagnostics | Include `s11_alex_as_hu` in ICC and Design Effect diagnostics table | M1 | survey |
| 6 | Block 1 Meta-to-Buckets Inferential Report | Incorporate `s11_alex_as_hu` into Model POV, Seat POV, Table 5.1 ($M=339$), Summary Stacks, and Appendix A | M2 | survey |
| 7 | Block 3 Bucket 1 to Bucket 3 Report | Incorporate `s11_alex_as_hu` into Step 3/4/5 $\rightarrow$ 11 regressions, Table 5.1, Summary Stacks, Appendix A | M3 | survey |
| 8 | Block 4 Bucket 2 to Bucket 3 Report | Incorporate `s11_alex_as_hu` into Step 6/9 $\rightarrow$ 11 regressions, Table 4.1, Summary Stacks, Appendix A | M4 | survey |
| 9 | Master Experiment Inferential Report | Add Alex substrate perception tables/columns alongside Step 11 coworker metrics in `generate_master_report.py` | M5 | survey |
| 10 | All Meta Reports Inferential Report | Add Alex substrate perception tables/columns in `generate_all_meta_reports.py` | M6 | survey |
| 11 | Missing Data Uniformity (N=594) | Exclude missing cases ($N=6$, all Rina Probe ON) from denominators/masks with zero artificial imputation across all blocks | M1-M6 | survey |
| 12 | Coworker Metrics Invariance (N=600) | Strictly preserve all 20-coworker metrics (`s11_accuracy`, `s11_ai_as_hu`, `s11_hu_as_hu`) bit-for-bit | M1-M7 | survey |
| 13 | E2E Testing Suite & Baseline Verification | Comprehensive automated test harness verifying R1, R2, R3, clean runs, and zero regressions | M7 | survey |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Block 5 Integration & Shared Loader | Update `load_dataset`/`extract_worker_metrics`/`RATIO_MAP` in `generate_block1_meta_to_all_buckets.py`; update `generate_block5_seat_vs_model.py` Parts 1, 2, 3, App A | none | DONE |
| M2 | Block 1 Sequential Integration | Update remaining tables, Table 5.1 ($M=339$), Summary Stacks in `generate_block1_meta_to_all_buckets.py` | M1 | DONE |
| M3 | Block 3 Sequential Integration | Update `generate_block3_bucket1_to_bucket3.py` for `s11_alex_as_hu` across Step 3/4/5 $\rightarrow$ 11 | M1 | DONE |
| M4 | Block 4 Sequential Integration | Update `generate_block4_bucket2_to_bucket3.py` for `s11_alex_as_hu` across Step 6/9 $\rightarrow$ 11 | M1 | DONE |
| M5 | Master Report Sequential Integration | Update `generate_master_report.py` with `raw_identify_alex` tables/columns | M1 | IN_PROGRESS |
| M6 | All Meta Reports Integration | Update `generate_all_meta_reports.py` with Alex perceptions | M1 | PLANNED |
| M7 | Full Regression Verification & Acceptance Gate | Run full verification suite across all 7 reports via `verify_coworker_baselines.py` and E2E test suite | M1-M6 | PLANNED |

## Interface Contracts
### Data Loader ↔ Block 5 / Block 1 / Block 3 / Block 4
- `load_dataset()`: Returns list of worker records where each worker dict contains:
  - `s11_alex_as_hu`: `1.0` if Alex guessed `"human"`, `0.0` if guessed `"ai"` or missing.
  - `s11_alex_tot`: `1.0` if Alex guess in `("human", "ai")`, `0.0` if missing.
  - `s11_alex_has_guess`: alias of `s11_alex_tot` for Block 3/4 conventions.
- `RATIO_MAP["s11_alex_as_hu"]`: `("s11_alex_as_hu", "s11_alex_tot")`
- `S11_COLS`: `["s11_accuracy", "s11_ai_as_hu", "s11_hu_as_hu", "s11_alex_as_hu"]`
- Coworker counters (`s11_tot`, `s11_cor`, `s11_ai_as_hu_cnt`, `s11_hu_as_hu_cnt`): Untouched; evaluated strictly when `actual in ("human", "ai")`.

## Code Layout
- `generate_block5_seat_vs_model.py`: Script generating `reports/block5_seat_vs_model_inferential_report.md`
- `generate_block1_meta_to_all_buckets.py`: Script generating `reports/block1_meta_to_all_buckets_inferential_report.md`
- `generate_block3_bucket1_to_bucket3.py`: Script generating `reports/block3_bucket1_to_bucket3_inferential_report.md`
- `generate_block4_bucket2_to_bucket3.py`: Script generating `reports/block4_bucket2_to_bucket3_inferential_report.md`
- `generate_master_report.py`: Script generating `reports/master_experiment_inferential_report.md`
- `generate_all_meta_reports.py`: Script generating `reports/all_meta_reports_inferential_report.md`
- `cluster_stats.py`: Statistical calculation engines (`PermEngine`, `assoc_test`, `outcome_matrices`)
- `verify_coworker_baselines.py`: Automated baseline verification script
- `reports/`: Output markdown report directory
