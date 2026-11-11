# E2E Test Infra: workplace-sim Alex Substrate Perception Integration

## Test Philosophy
- Requirement-driven, opaque-box, and regression-resistant.
- Methodology: Category-Partition + Boundary Value Analysis + Baseline Snapshot Differencing + Clean Execution Auditing.

## Feature Inventory
| # | Feature | Source (requirement) | Tier 1 | Tier 2 | Tier 3 |
|---|---------|---------------------|:------:|:------:|:------:|
| 1 | Raw Alex Extraction & Denominator Mapping | ORIGINAL_REQUEST §R1, R3 | 5 | 5 | ✓ |
| 2 | Block 5 Variance Competition | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 3 | Block 5 Seat Sensitivity | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 4 | Block 5 Joint Interaction Matrices | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 5 | Block 5 Appendix Diagnostics | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 6 | Block 1 Meta Inferential Report | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 7 | Block 3 Bucket 1 $\rightarrow$ 3 Report | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 8 | Block 4 Bucket 2 $\rightarrow$ 3 Report | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 9 | Master Experiment Inferential Report | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 10 | All Meta Reports Inferential Report | ORIGINAL_REQUEST §R1 | 5 | 5 | ✓ |
| 11 | Missing Data Uniformity ($N=594$) | ORIGINAL_REQUEST §R3 | 5 | 5 | ✓ |
| 12 | Coworker Metrics Invariance ($N=600$) | ORIGINAL_REQUEST §R2 | 5 | 5 | ✓ |

## Test Architecture
- Test runner: `python -m pytest test_alex_integration.py` or standalone `python verify_coworker_baselines.py`
- Test case format: Pytest test suite asserting presence of Alex sections/tables, absence of regressions in coworker tables, exact $N=594$ / $N=600$ counts, and exit code 0 on all generators.

## Real-World Application Scenarios (Tier 4)
| # | Scenario | Features Exercised | Complexity |
|---|----------|--------------------|------------|
| 1 | Full Sequential Regeneration of all 6 report scripts | F1-F12 | High |
| 2 | Baseline Snapshot Diff Verification (`verify_coworker_baselines.py`) | F12 | Medium |
| 3 | Statistical Precision Check ($64.65\%$ Alex Human rate across runs) | F1, F11 | Low |
