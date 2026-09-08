# Polymer Informatics — SPE Workshop Edition

This repository contains four Jupyter notebooks that teach an end-to-end polymer
informatics workflow: molecular representation, property prediction, chemical-space
analysis, explainable machine learning, and generative inverse design.

## Workshop sequence

1. `1_Overview.ipynb` — inspect the glass-transition dataset and construct Morgan
   fingerprints, frequency fingerprints, and molecular descriptors.
2. `2_Supervised_Learning.ipynb` — compare Lasso, random forest, and feed-forward
   neural networks for polymer property prediction.
3. `3_Unsupervised_Learning.ipynb` — generate virtual polymers and explore their
   chemical space with t-SNE, K-means, SHAP, and PCA.
4. `4_Generative_models.ipynb` — train a character LSTM and use iterative
   hill-climbing to generate candidates with high predicted glass-transition
   temperature.

## Recommended setup

Python 3.10 is the supported workshop version. From the repository root:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-workshop.txt
jupyter lab
```

Open the notebooks in numerical order. Their setup cell locates the repository
automatically when Jupyter is started here. To launch Jupyter elsewhere, set:

```bash
export POLYMER_WORKSHOP_ROOT=/absolute/path/to/Polymer-Informatics-workshop-ready
```

Google Colab is also supported. Put the complete repository in `MyDrive/SPE`, open
a notebook from that folder, and run its setup cell.

## Dry-run and full modes

Dry-run mode is the default. It executes every teaching stage while shortening
neural-network training, cross-validation, SHAP sampling, t-SNE, and generative
optimization. It is intended for pre-workshop verification.

Use the original full teaching parameters by setting the environment variable
before starting Jupyter:

```bash
export POLYMER_WORKSHOP_DRY_RUN=0
```

Execute all notebooks from clean kernels and save the results under
`dry_run_outputs/` with:

```bash
python tools/run_all_notebooks.py
```

Generated models, SHAP data, images, and candidate CSV files are written to
`workshop_outputs/`; source datasets are never overwritten.

## Presenter checklist

- Run `python tools/run_all_notebooks.py` once on the presentation machine.
- Keep the executed notebooks in `dry_run_outputs/` as an offline fallback.
- Use dry-run mode for live audience participation.
- Use full mode only for results prepared before the session; complete
  cross-validation and generative-model stages may take hours.

## References

- Yue et al., *Journal of Chemical Theory and Computation* 19 (2023), 4641–4653.
- Yue et al., *Digital Discovery* 3 (2024), 2465–2478.
- Yue et al., *Digital Discovery* 4 (2025), 910–926.
