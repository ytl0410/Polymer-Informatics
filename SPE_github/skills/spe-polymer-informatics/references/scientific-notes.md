# Representation and interpretation boundaries

## Features and checkpoints

The course uses radius-3 1024-bit Morgan fingerprints for most supervised bit
examples and the bundled PyTorch `Tg.pth` predictor; chemical-space plots use
2048-bit fingerprints. Do not confuse these with the count-based frequency matrix.

Frequency features gather Morgan hash IDs, map each ID to a column index, and
select columns by zero count. For the 6906-row dataset, `Zero_Sum < 6870` means
presence in at least 37 rows. That absolute threshold is tied to the dataset.
For another dataset, explicitly decide the frequency threshold and fit feature
selection on training data. Do not shrink the dataset while retaining 6870 and
assume the resulting features have the same meaning.

`Corr_All.pickle`, `unique_list_All.pickle`, and `Columns_All.pickle` determine
the mapping/selection. The snapshot has 1210 selected features. The file named
`polymer.keys_All.pickle` was populated from the last loop's `polymer.keys()`;
its name does not make it the full vocabulary. Inspect construction before reuse.
Feature dimension alone is insufficient: column order and hashes must also match.

The Tg PyTorch FNN architecture is 1024 → 256 → 64 → 2048 → 512 → 1 with ReLU
between hidden layers. A generated LSTM checkpoint is a separate model trained
on strings; it does not replace the Tg predictor. Reusing a trained LSTM also
requires its vocabulary ordering and sequence-length configuration.

## Evaluation in teaching versus research

The original notebooks contain teaching shortcuts: some normalization and feature
selection precede splitting, and the held-out `X_test` is used for validation and
the Lasso alpha sweep. These are useful demonstrations but do not constitute an
untouched final test-set estimate after model selection. For research-grade
evaluation, use train-only preprocessing, a validation/CV strategy for selection,
and an independent final test set. Keep structural duplicates or related polymer
representations from crossing the split when evaluating generalization.

A large training/held-out gap suggests overfitting; low scores after brief training
can instead reflect undertraining. Compare fixed splits and seeds before claiming
one representation wins. A successful execution record establishes cell execution
for that specific project copy, not the correctness of every plot interpretation
or scientific claim.

## Chemical-space and SHAP figures

t-SNE preserves aspects of local neighborhoods; its axes, global distances, and
cluster spacing are not physical property scales. K-means labels are arbitrary
identifiers. Their order or a KDE over label numbers is not a continuous chemical
coordinate; compare category counts or cross-tabs for group composition.

SHAP attributes model predictions relative to its background dataset. It does
not prove a fragment causes a physical property change. Correlated fingerprints,
background selection, and model fit affect interpretations. The course's red/blue
sign uses correlation between feature values and SHAP values; it is not an
intrinsic material law. A PCA arrow built from these summaries likewise does not
by itself prove independent tunability of Tg and Eg.

## Generation and hill-climbing

The original Notebook 4 fitness function calculates both predicted Tg (`value`)
and a sigmoid transformation (`score`), but returns `value`. Its main search
therefore ranks candidates by predicted Tg in Celsius, not by a bounded reward.
Failures in the parsing/fingerprint try block return zero. Do not claim all
possible prediction failures are handled or silently change the return value.
The separate modified copy returns the sigmoid score; do not transfer that
explanation to the original. The teaching loop selects top seeds and retrains
on generated strings; it is not policy-gradient reinforcement learning.

If a learner requests a short-run LSTM test, treat it as a pipeline check, not a
validated pretrained generator. Generated-property scores are not measured Tg.
SMILES string uniqueness differs
from canonical structural uniqueness. In the original notebook, counting `*` and
RDKit parsing filters the final analysis, while fitness selection may still admit
parseable strings without exactly two connection points. Explain that limitation
when interpreting optimization trends. For stricter design work, check connection
atom degrees, repeat-unit chemistry, duplicates, and prediction-domain coverage,
then verify the revised pipeline rather than silently claiming those checks exist.
