# Running the original workshop notebooks

## Select the right baseline

Use the instructor's original four notebooks as the teaching source. The
instructor reports successful execution in Google Colab; the exact runtime
versions, hardware, and detailed execution logs from that test are not recorded
in this skill. This is an instructor-reported result, not an independent test.

Keep three sources separate: the local reference configuration in the original
README/slides, the installation cells in each notebook, and the versions actually
loaded in a learner's Colab kernel. They are not a single pinned environment.

## Local reference configuration

The original README and Day 1 slides list the following local setup:

| Component | Original local reference |
|---|---|
| Python | 3.9 |
| CUDA toolkit / cuDNN | 11.2 / 8.1.0 |
| TensorFlow | <2.11 |
| NumPy | 1.26.4 |
| matplotlib | 3.8.0 |
| pandas | 1.5.3 |
| RDKit | 2023.9.1 |
| scikit-learn | 1.3.0 |
| keras-tuner | 1.4.5 |
| seaborn | 0.13.0 |

These are recorded teaching instructions, not a newly validated cross-platform
lockfile. Do not silently replace them with the modified copy's Python 3.10 and
TensorFlow 2.15.1 stack. Preserve a learner's working setup. If asked to build
a fresh local environment, check the target platform and dependency constraints,
activate the intended environment after creating it, and report any conflict
before proposing a version change.

## Notebook-specific Colab setup

The inspected original files contain these installation commands. Reinspect the
learner's copy before running them; unpinned packages may resolve differently.

| Notebook | Installation cells in the original snapshot |
|---|---|
| 1 and 2 | `rdkit` |
| 3 | `rdkit`, `tensorflow==2.15.0`, `smipoly`, `shap==0.41.0` |
| 4 | `rdkit`, `torch==2.2.0`, `torchaudio==2.2.0`, `torchvision==0.17.0`, `pytorch_lightning==1.9.0`, `torchmetrics==0.5.0`, `selfies`, `numpy==1.26.4` |

In particular, Notebook 3's TensorFlow installation differs from the local
reference. Do not apply the local `tensorflow<2.11` instruction to every Colab
notebook or claim that one environment was used for all four.

The original setup mounts Drive at `/content/drive`, sets a notebook variable
named `path`, checks `os.path.isdir(path)`, and appends the folder to
`sys.path`. A `True` directory check only confirms the directory exists.
It does not verify packages, data files, GPU availability, or model checkpoints.
The preflight script's `POLYMER_WORKSHOP_ROOT` fallback locates files for the
script only; it does not configure the original notebook's `path` variable.

If asked to verify Colab, record the Python version and installed packages from
the actual kernel, run the notebook's setup, restart if required, and verify
imports before executing the lab. Google sign-in and Drive authorization may
require the learner. A local run cannot substitute for a real Colab test.

## Read-only preflight

Run with the interpreter whose environment you want to inspect:

```bash
python <skill-dir>/scripts/preflight.py --project <original-project-dir>
python <skill-dir>/scripts/preflight.py --project <original-project-dir> --check-environment
```

The script checks the original file inventory, CSV headers, notebook structure,
and ordinary Python syntax. It records installation commands and historical
output counts without running cells, loading models, or deserializing pickles.
IPython-only cells require a live-kernel check. A successful inventory result is
not an execution or environment-compatibility pass. Version differences are
reported as observations, not proof that the learner's setup is broken.

No modified-copy configuration file, requirements file, saved-output directory,
or bulk runner is required. A detected modified-copy setup is reported explicitly.

## Execution and paths

Follow the notebook's existing cell order and parameter values. The original
has no `--full` flag or global dry-run mode. Full execution can involve long
training and cross-validation; confirm scope before initiating expensive work.
For an explicitly requested shortened test, agree on reductions and use a copy.
Do not present its scores as results from the original training configuration.

Notebook 4 explicitly requests a GPU for initial LSTM training. Check the
selected runtime; do not silently switch its accelerator or model size.

The originals mix notebook `path`, working-directory paths, and hard-coded
Drive paths. Notebook 3 includes `/content/drive/My Drive/SPE_day3+4/` for
feature mappings. Notebook 4 loads `path + '/version_0/final_model.ckpt'`
in its main sampling workflow and also contains another checkpoint path later.
Inspect the selected cell and actual training output. Do not assume the automatic
checkpoint handoff or unified output directory from the modified copy exists.

Running cells can overwrite feature-mapping pickles and write models, CSVs, and
figures at the paths in those cells. Identify these targets before execution,
and use a learner-owned copy for experiments. Diagnose missing paths from the
observed notebook; change them only within an authorized setup or repair.

## Evidence and troubleshooting

- Missing data: check the actual `path`, CSV names, and folder contents.
- Import failure: inspect the current kernel and notebook-specific installation
  cells before suggesting any dependency change.
- SHAP output shape or sample-index error: inspect actual outputs, selected
  samples, and the installed version; do not assume the modified copy's workaround.
- Checkpoint failure: find the file produced by the relevant training cell and
  verify the model class and vocabulary before loading it.
- Unexpected scores: distinguish original saved results from newly executed or
  shortened runs. Report the split and training settings.
- A separate modified copy has a historical local dry-run report. Its runtime,
  timings, and 186-cell count do not describe the original notebooks. Count the
  actual cells and record the scope of any new run instead.
