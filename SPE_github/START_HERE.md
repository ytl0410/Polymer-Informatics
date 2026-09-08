# SPE Polymer Informatics — Learner Kit

Instructor: Tianle Yue. This kit includes an installable AI teaching-assistant
skill and four polymer informatics labs.

## Understand the two folders

- `skills/spe-polymer-informatics/`: the Codex skill, including the course map,
  environment and troubleshooting guidance, scientific interpretation notes,
  and a read-only preflight script.
- `Polymer-Informatics-workshop-ready/`: the lab notebooks, datasets, Tg prediction
  weights, and execution tools. Executed notebooks in `dry_run_outputs/` are
  historical results for reading and demonstrations.

The complete learner ZIP includes both folders. The standalone skill ZIP includes
only the skill folder and is intended for learners who already have the lab
project. The skill does not replace a Python environment, the datasets, or a
fully trained generative model.

## Install the skill

Copy the entire `spe-polymer-informatics` folder into your Codex skills directory:
the default is `~/.codex/skills/`, or `skills/` under `CODEX_HOME` if you have set
that variable. You can also place it in the course project's `.agents/skills/`
directory as a project-shared skill.

Do not copy only `SKILL.md`. If a version with the same name already exists,
back it up before merging or replacing it. After copying the folder, open the
course project and start a new session so the client can discover the skill.

You do not need to ask the assistant to run every course cell automatically.
Start with a prompt such as:

```text
Use $spe-polymer-informatics. My project is at <path to my extracted course project>.
I have a background in polymer science but am new to machine learning. Explain
the three representations in the first notebook, then guide me through a small
exercise.
```

Other example prompts:

```text
Use $spe-polymer-informatics to check my course environment, then run all four notebooks in dry-run mode.
Use $spe-polymer-informatics to explain why Lasso's alpha affects training and test R².
Use $spe-polymer-informatics to explain what SHAP-highlighted fragments can and cannot tell us.
Use $spe-polymer-informatics to compare LSTM sampling at temperature=0.8 and temperature=1.1.
```

## Start the labs locally

Open a terminal in `Polymer-Informatics-workshop-ready/` and use Python 3.10:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-workshop.txt
python -m jupyter lab
```

On Windows, create the environment with `py -3.10 -m venv .venv`, then use
`.venv\Scripts\python.exe` for the installation and Jupyter commands. The shared
kit does not include a virtual environment.

Open notebooks 1–4 in order. The default dry-run mode shortens training and
sampling. Historical local validation took approximately 12–13 minutes; runtime
varies by device. The four notebooks contain 186 non-empty code cells in total.

To check all four notebooks from the command line:

```bash
python tools/run_all_notebooks.py
```

The `--full` option uses the full training parameters and may take hours. It is
not required for a first pass through the course.

The code includes Google Colab path setup, but the current Colab runtime has not
been revalidated. The pinned dependencies may not support its current Python
version. If you encounter this issue, use local Python 3.10.

## Interpret the shared results

The historical dry run passed on September 2, 2026, on macOS ARM/Python 3.10.
Packaging checks covered files, the skill, and consistency of the historical
outputs; full training was not rerun. The final execution report reused verified
outputs from the first three notebooks and reran the fourth.

The generative model received only brief training and may produce invalid
structures. Its Tg values come from a predictor, not experimental measurements.
The course retains some teaching simplifications; research-grade evaluation
requires a revised data-splitting and preprocessing strategy.

Running the labs updates four feature-mapping pickle files in the project root
and writes model and result directories. Each learner should work in a separate
extracted copy. For sharing, the instructor's personal paths in the executed
notebooks have been replaced with generic paths. Those outputs are historical
records, not a new executable configuration.

This kit includes course source code and data and preserves the original license.
Retain attribution when redistributing the materials.
