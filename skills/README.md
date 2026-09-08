# SPE workshop skills

This directory is the complete, English-language source for the workshop skill.
The teaching baseline is Tianle Yue's original four notebooks, not the separate
workshop-ready revision. No notebook, dataset, or model weight is embedded in the
skill. Provide your original course project when using it.

## Files to share

Share the entire `spe-polymer-informatics/` directory, including `SKILL.md`,
`agents/`, `references/`, `scripts/`, `tests/`, and `LICENSE`. Do not distribute
only the entrypoint: its references and preflight script are part of the skill.
No credentials, virtual environments, or personal machine paths are required.

## Use the skill

Copy the complete skill directory into your Codex skills directory, or the course
project's `.agents/skills/` directory. Preserve any existing version before
replacing it. Start a new session and provide the original project location:

> Use $spe-polymer-informatics. My original course project is at <project path>.
> Explain the first notebook while preserving its code and environment settings.

For a read-only file and environment inventory, use your chosen interpreter:

```bash
python skills/spe-polymer-informatics/scripts/preflight.py --project <original-project-path> --check-environment
```

Run this command from the GitHub repository root, replacing the project-path
placeholder. The result is an inventory, not proof of successful execution.

The instructor reports that the originals run in Colab. Exact tested runtime
versions have not been supplied. The local reference and each notebook's Colab
installation cells differ; the skill explains them separately.

## Scope of this update

The skill source in this directory targets the original course. Updating a skill
does not replace the separate `Polymer-Informatics-workshop-ready/` project or
turn its historical dry-run outputs into tests of the original notebooks.
Use this directory for the current GitHub skill distribution; older bundled
download archives and their learner guides may describe the earlier revision.

## Check the helper

```bash
python -B -m unittest discover -s skills/spe-polymer-informatics/tests -v
```

The tests use temporary fixtures and do not execute the course notebooks.
