"""Shared runtime settings for the SPE Polymer Informatics workshop."""

from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
ARTIFACTS_DIR = PROJECT_ROOT / "workshop_outputs"
ARTIFACTS_DIR.mkdir(exist_ok=True)

DRY_RUN = os.getenv("POLYMER_WORKSHOP_DRY_RUN", "1").strip().lower() not in {
    "0",
    "false",
    "no",
}

RANDOM_SEED = 42
KERAS_EPOCHS = 3 if DRY_RUN else 200
RF_TREES = 20 if DRY_RUN else 100
LASSO_GRID_POINTS = 5 if DRY_RUN else 10
CV_SPLITS = 2 if DRY_RUN else 5
CV_REPEATS = 1 if DRY_RUN else 2
# The teaching example intentionally inspects sample 66 and its three known
# high-impact substructures, so dry-run mode must retain at least 67 samples.
SHAP_SAMPLES = 80 if DRY_RUN else 400
TSNE_ITERATIONS = 250 if DRY_RUN else 500
TSNE_REFERENCE_ROWS = 500 if DRY_RUN else None
KMEANS_CLUSTERS = 20 if DRY_RUN else 300

LANGUAGE_MODEL_ROWS = 512 if DRY_RUN else None
LANGUAGE_MODEL_HIDDEN_DIM = 64 if DRY_RUN else 1024
LANGUAGE_MODEL_LAYERS = 1 if DRY_RUN else 3
LANGUAGE_MODEL_EPOCHS = 1 if DRY_RUN else 5
RL_GENERATIONS = 2 if DRY_RUN else 15
RL_NUM_BEST = 3 if DRY_RUN else 10
RL_NUM_RANDOMIZE = 2 if DRY_RUN else 5
RL_SAMPLES_PER_SEED = 1 if DRY_RUN else 2


def mode_label() -> str:
    return "DRY RUN" if DRY_RUN else "FULL WORKSHOP"
