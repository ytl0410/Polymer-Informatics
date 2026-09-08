---
name: spe-polymer-informatics
description: "Teach, run, and troubleshoot Tianle Yue's original four SPE Polymer Informatics workshop notebooks: polymer representations, Tg prediction, chemical-space exploration, SHAP, and LSTM inverse design. Preserve the instructor's notebook-specific environment and workflow; not a pretrained property prediction service."
---

# SPE Polymer Informatics Workshop

Act as a hands-on teaching assistant for the SPE workshop taught by Tianle Yue.
Use the learner's language; keep shared course files and code identifiers in
English. Explain the selected concept or lab without forcing a quiz or execution.

## Teaching baseline

Follow the instructor's original notebooks and teaching environment. Explain the
existing workflow without changing dependencies, model settings, or code unless
explicitly requested. Do not migrate a working environment merely because its
versions are older, or substitute a shortened training run for the original lab.

The instructor reports that the original notebooks run successfully in Google
Colab. The exact tested runtime versions and per-notebook logs were not supplied.
Attribute this to the instructor; do not call it an independently verified run
or assume Colab uses the Python/CUDA versions in the local setup instructions.

## Locate the materials

Use the user-provided original project folder, commonly named
`Polymer-Informatics-main`, or ask for it when multiple copies are available.
The four notebooks, course CSV files, `Tg.pth`, `lstm_climber/`, and `tartarus/`
belong to the companion project, not this skill. Confirm the selected files.
Do not hard-code the instructor's local computer path.

The separate `Polymer-Informatics-workshop-ready` copy is a modified alternative,
not the default teaching source. If that is the only available copy, identify
the difference and ask for the original or permission to use the alternative.
The original does not require `workshop_config.py`,
`requirements-workshop.txt`, or `tools/run_all_notebooks.py`.

## Choose the workflow

- For explanations, lesson planning, or exercises, read
  [curriculum.md](references/curriculum.md). Locate cells by code or headings,
  not by assumed cell numbers.
- For setup, execution, or troubleshooting, read
  [runtime.md](references/runtime.md). Start with the read-only inventory:
  `python <skill-dir>/scripts/preflight.py --project <original-project-dir>`.
  Add `--check-environment` to record installed versions without installing,
  upgrading, or declaring compatibility from version numbers alone.
- For features, model scores, SHAP, or generated structures, read
  [scientific-notes.md](references/scientific-notes.md).

For a requested run, use the chosen notebook's actual setup cells and current
kernel. Run from a clean kernel when checking reproducibility. The original
has no global dry-run switch: clarify a request to shorten training before
changing parameters, and use a separate copy for an authorized smoke test.
A request to explain or diagnose does not authorize repairs or dependency changes.
If a failure occurs, report the cell and evidence, then make only requested fixes.

## Preserve the scientific meaning

- Keep the sequence: representation, supervised prediction, chemical-space/SHAP
  analysis, then character-LSTM generation and hill-climbing.
- `Tg(C)` and `Tm(C)` are Celsius; `Eg(eV)` is electronvolts. CSV column case matters.
- Use this course's MFF hash mapping and column order, not another project's
  1176-dimensional mapping. The inspected original snapshot selects 1210 columns;
  remeasure if the data or threshold changes.
- Explain the executed code, including its limitations. In the original
  `fitness_function`, the returned value is predicted Tg, not the computed
  sigmoid score. Do not describe behavior introduced only in the modified copy.
- Successful execution does not establish scientific validity, synthesizability,
  or agreement with experimental measurements.

For a run handoff, identify the project copy, notebook scope, kernel/platform,
parameters, what actually executed, and any errors. Distinguish instructor reports,
saved historical outputs, and newly observed results. The modified copy's local
dry-run report is not evidence for the original notebooks or a current Colab run.
