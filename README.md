# Polymer-Informatics
This repository contains a set of four Jupyter notebooks designed as a teaching module for polymer informatics and machine learning applications in polymer science. The notebooks cover fundamental concepts, supervised learning, unsupervised learning, and generative models for polymer design.

## Notebooks

1. **1_Overview.ipynb**  
   Introduction to polymer informatics and machine learning workflows in materials science.

2. **2_Supervised_Learning.ipynb**  
   Property prediction of polymers using supervised learning approaches with explainable ML methods.

3. **3_Unsupervised_Learning.ipynb**  
   Exploration of polymer feature space using unsupervised learning methods such as PCA and clustering.

4. **4_Generative_models.ipynb**  
   Generative modeling approaches for virtual polymer design and inverse design applications.

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
