# Workshop-ready changes

The original download remains unchanged. This working copy was prepared and tested
on macOS ARM with Python 3.10.

## Reproducibility and presentation

- Added one pinned environment in `requirements-workshop.txt`.
- Added a shared local/Colab project-root setup to all four notebooks.
- Added dry-run and full-workshop parameter profiles in `workshop_config.py`.
- Added a clean-kernel notebook runner and resumable validation report.
- Redirected generated models, plots, SHAP files, and candidate tables to
  `workshop_outputs/`.
- Kept executed notebooks in `dry_run_outputs/` as an offline presentation backup.

## Correctness and compatibility

- Removed hard-coded `SPE_day3+4`, `My Drive`, and missing checkpoint paths.
- Replaced hard-coded neural-network input widths with the actual feature width.
- Updated the LSTM Lightning module for the pinned PyTorch Lightning API.
- Fixed `SMILESDataModule` so its `random_split` argument is honored.
- Reused the loaded Tg predictor instead of loading a 5.6 MB state dictionary for
  every candidate.
- Fixed the generative objective to return the documented bounded fitness score.
- Fixed the literal `{string_type}` output directory and missing checkpoint handoff.
- Made empty generated-candidate sets safe to analyze.
- Preserved the SHAP sample used by the highlighted-substructure teaching example.
- Disabled DataLoader subprocesses in dry-run mode for quieter, more reliable demos.

## Validation result

All non-empty code cells in all four notebooks executed from clean kernels without
saved exceptions. See `dry_run_outputs/report.json` for the machine-readable result.
The full-workshop parameter profile was not run because its cross-validation and
generative stages are intentionally multi-hour workloads.
