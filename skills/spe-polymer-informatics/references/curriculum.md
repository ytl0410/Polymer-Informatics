# Course map and learner activities

Use the instructor's original notebooks and the learner's selected chapter.
Do not substitute the workshop-ready copy or shorten training unless requested.
For newcomers, start with Notebook 1; for a
presenter, map the selected modules to available time. The following are exercise
ideas, not mandatory questions or fixed session durations.

| Notebook | Teaching question | Demonstration | Small learner activity |
|---|---|---|---|
| `1_Overview.ipynb` | How does a repeat-unit structure become model input? | Tg distribution, RDKit drawings, radius-3 1024-bit Morgan fingerprints, Morgan counts, descriptors | Compare two structures and identify presence versus repeated counts; inspect a selected substructure |
| `2_Supervised_Learning.ipynb` | How do representation and model choice change Tg prediction? | Lasso, random forest, FNN; parity plots; alpha sweep; repeated K-fold CV | Change one Lasso alpha while holding the split fixed; explain the train/held-out gap |
| `3_Unsupervised_Learning.ipynb` | Where do proposed polymers sit, and what drives predictions? | SMiPoly polyether/polyimide generation, RDKit PBI construction, t-SNE, K-means, Tg/Eg SHAP and PCA | Compare family distributions, then inspect a SHAP-supported fragment without treating it as causal proof |
| `4_Generative_models.ipynb` | How can a property predictor guide structure generation? | Character LSTM, temperature-controlled sampling, high-Tg fitness, iterative seed selection/retraining | Change sampling temperature and compare parseability, connection points, duplicates, and predicted Tg |

## Instruction style

Tie SMILES to polymer repeat units and `*` connection atoms before discussing
numerical feature vectors. Explain what a cell consumes, changes, and produces.
Have learners compare outputs before changing multiple parameters. Keep a
baseline and record the training settings and random seed so a comparison is interpretable.
Short-run FNN scores can be poor; that is expected, not proof a representation is
inferior. Do not substitute historical full-training scores for the learner's run.

Notebook 3 spans several topics: rule-based structure generation is not itself
unsupervised learning; SHAP explains a supervised model. Notebook 4's main loop
is a hill-climbing/retraining procedure, not PPO or a Transformer-based LLM.

## Files and schemas in the original snapshot

| File | Rows | Relevant columns | Role |
|---|---:|---|---|
| `Tg.csv` | 6906 | `Smiles`, `Tg(C)` | Main property dataset |
| `Eg.csv` | 3379 | `Smiles`, `Eg(eV)` | Second property for SHAP/PCA |
| `Tm.csv` | 3633 | `Smiles`, `Tm(C)` | Optional extension, not a trained Tm service |
| `PolyInfo.csv` | 12841 | `smiles` | Generative pretraining structures |
| `diCOOH.csv` | 1290 | `Smiles` | PBI monomer input |
| `202207_smip_monset.csv` | 1083 | `SMILES` plus monomer metadata | SMiPoly input |

Counts are snapshot facts, not requirements for learner datasets. Reinspect new
files with a CSV reader, especially BOMs, missing structures, and column case.

## Research context supplied with the course

Use these as bibliographic context; consult the publications if a learner requests
paper-specific findings or quotations.

- Yue, Tianle; He, Jinlong; Tao, Lei; Li, Ying (2023). *High-throughput screening
  and prediction of high modulus of resilience polymers using explainable machine
  learning*. Journal of Chemical Theory and Computation 19(14), 4641–4653.
- Yue, Tianle; He, Jianxin; Li, Ying (2024). *Polyuniverse: generation of a large-scale
  polymer library using rule-based polymerization reactions for polymer informatics*.
  Digital Discovery 3(12), 2465–2478.
- Yue, Tianle; Tao, Lei; Varshney, Vikas; Li, Ying (2025). *Benchmarking study of
  deep generative models for inverse polymer design*. Digital Discovery 4(4), 910–926.
