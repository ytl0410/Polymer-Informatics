# Polymer-Informatics
This repository contains a set of four Jupyter notebooks designed as a teaching module for polymer informatics and machine learning applications in polymer science. The notebooks cover fundamental concepts, supervised learning, unsupervised learning, and generative models for polymer design.

## Notebooks

1. **1_Overview.ipynb**  
   Introduction to polymer informatics and feature engineering methods.

2. **2_Supervised_Learning.ipynb**  
   Property prediction of polymers using supervised learning approaches.

3. **3_Unsupervised_Learning.ipynb**  
   Introduction to virtual polymer generation approach using small-molecule datasets and polymerization reactions, exploration of polymer feature space using unsupervised learning methods such as T-SNE and clustering, as well as explainable ML method (SHAP).

4. **4_Generative_models.ipynb**  
   Generative modeling approaches for hypothetical polymer generation and inverse design using reinforcement learning strategy.

## Getting Started

You can either use **Google Colab** (see instructions inside each notebook) or set up your own Python environment locally.

### Option 1: Google Colab
- No installation needed.  
- Open the notebook in Colab and follow the inline instructions.

### Option 2: Local Python Environment (Conda)

Create a new environment (Python 3.9 recommended):
```
conda create -n py39 python=3.9
conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0
python -m pip install "tensorflow<2.11"
pip install numpy==1.26.4
pip install matplotlib==3.8.0
pip install pandas==1.5.3
pip install rdkit==2023.9.1
pip install scikit-learn==1.3.0
pip install keras-tuner==1.4.5
pip install seaborn==0.13.0<img width="1157" height="538" alt="image" src="https://github.com/user-attachments/assets/3724e6a7-5177-4b2d-8fab-78357ba1f74e" />
```

## References
1. **Property prediction & unsupervised learning**

```bibtex
@article{yue2023high,
  title={High-throughput screening and prediction of high modulus of resilience polymers using explainable machine learning},
  author={Yue, Tianle and He, Jinlong and Tao, Lei and Li, Ying},
  journal={Journal of Chemical Theory and Computation},
  volume={19},
  number={14},
  pages={4641--4653},
  year={2023},
  publisher={ACS Publications}
}
```

2. **Virtual polymer generation (polymerization reactions & small molecules)**

```bibtex
@article{yue2024polyuniverse,
  title={Polyuniverse: generation of a large-scale polymer library using rule-based polymerization reactions for polymer informatics},
  author={Yue, Tianle and He, Jianxin and Li, Ying},
  journal={Digital Discovery},
  volume={3},
  number={12},
  pages={2465--2478},
  year={2024},
  publisher={Royal Society of Chemistry}
}
```

3. **Generative models**
```bibtex
@article{yue2025benchmarking,
  title={Benchmarking study of deep generative models for inverse polymer design},
  author={Yue, Tianle and Tao, Lei and Varshney, Vikas and Li, Ying},
  journal={Digital Discovery},
  volume={4},
  number={4},
  pages={910--926},
  year={2025},
  publisher={Royal Society of Chemistry}
}
```

## Optional AI Teaching Assistant Skill

The [SPE Polymer Informatics skill](skills/spe-polymer-informatics/) provides
an AI teaching assistant for the four original notebooks in this repository.
It can explain concepts and code, suggest practice exercises, and help diagnose
setup or execution problems. It preserves the instructor's notebook-specific
environment and training settings unless you explicitly request changes.
The skill is optional: it is not required to run the notebooks in Google Colab
or locally, and it is not a pretrained polymer-property prediction service.

### Use with Codex

Copy the entire `skills/spe-polymer-informatics/` directory, including its
references and scripts, into this project's `.agents/skills/` directory.
Preserve an existing installation before replacing it. If the skill does not
appear, restart Codex. These locations and discovery behavior are described in
the [official OpenAI skills documentation](https://learn.chatgpt.com/docs/build-skills).

Open this repository in Codex and use a prompt such as:

> Use $spe-polymer-informatics. This repository contains my original workshop
> notebooks. Explain Notebook 1 while preserving its code and environment settings.

### Optional read-only preflight

From the repository root, use your chosen Python interpreter to inspect the
course files and record installed package versions:

```bash
python skills/spe-polymer-informatics/scripts/preflight.py --project . --check-environment
```

This check does not install packages or execute notebooks. A successful inventory
is not proof that the notebooks have run successfully in the current environment.
See [skills/README.md](skills/README.md) for the complete file list and usage notes.
