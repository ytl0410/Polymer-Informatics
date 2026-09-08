# SPE Polymer Informatics Workshop

Instructor: Tianle Yue. A hands-on machine-learning course for learners in polymer
science, including four Jupyter notebooks, course datasets, Tg prediction weights,
an AI teaching-assistant skill, and historical execution results.

**Start with [START_HERE.md](START_HERE.md)** for installation instructions and
example prompts. All learner-facing materials in this repository are in English.

## Contents

| Location | Purpose |
|---|---|
| [Polymer-Informatics-workshop-ready/](Polymer-Informatics-workshop-ready/) | Complete lab project and dependency configuration |
| [skills/spe-polymer-informatics/](skills/spe-polymer-informatics/) | Installable AI lab-assistant skill |
| [downloads/spe-polymer-informatics-skill.zip](downloads/spe-polymer-informatics-skill.zip) | Standalone skill archive for download and sharing |
| [downloads/SPE-workshop-student-kit.zip](downloads/SPE-workshop-student-kit.zip) | Complete learner kit with code, data, the skill, and the learner guide |

The course progresses through polymer representations, supervised Tg prediction,
virtual polymers and chemical-space/SHAP analysis, and character-level LSTM
generation with hill-climbing inverse design.

## Run the labs

From this repository's root directory, create the course environment with Python 3.10:

```bash
cd Polymer-Informatics-workshop-ready
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-workshop.txt
python -m jupyter lab
```

Open notebooks 1–4 in order. The default dry-run mode shortens training and
sampling. To check all four notebooks, run:

```bash
python tools/run_all_notebooks.py
```

For environment and platform details, see the [learner guide](START_HERE.md) and
the [project README](Polymer-Informatics-workshop-ready/README.md).

## Use the AI teaching assistant

Copy the entire `skills/spe-polymer-informatics` folder into your Codex skills
directory (default: `~/.codex/skills/`). Start a new session and provide the course
project path:

> Use $spe-polymer-informatics. My project is at <project path>. Guide me through
> the first notebook, explain the three representations, and help me complete a
> small exercise.

## Validation record

[dry_run_outputs/](Polymer-Informatics-workshop-ready/dry_run_outputs/) contains
historical execution results from September 2, 2026, on macOS ARM/Python 3.10.
All 186 non-empty code cells across the four notebooks executed without saved
errors. These outputs are included as a shareable demonstration record.

Historical results do not establish that the current Colab runtime or the full
training configuration has been validated. Short generative-model training
demonstrates the workflow; predicted Tg values are not experimental measurements.
See [scientific-notes.md](skills/spe-polymer-informatics/references/scientific-notes.md)
for the scientific interpretation limits.

This repository retains the original project's [MIT License](LICENSE) and course
references. Preserve attribution when redistributing the materials.
