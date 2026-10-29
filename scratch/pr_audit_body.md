## Summary of Changes

1. **Removed Orphan `output/human_audit/sample_1050.csv`**:
   - The file was an unused CSV export containing 1,050 rows (from an earlier 150-per-stage draw where 292 rows were never reviewed in `human_reviews.json`).
   - The authoritative ground truth is `output/human_audit/sample_930.json` (100% reviewed across 930 items in `output/human_audit/human_reviews.json`).
   - No scripts or pipeline code depend on `sample_1050.csv`.

2. **Updated `audit_cli.py` Docstring**:
   - Updated the header comment from "1,050 total items" to "930 total items" across the 7 simulation stages.

3. **Verification**:
   - Ran `python audit_cli.py --stats`: All 930 reviewed items and agreement metrics execute cleanly without errors.
