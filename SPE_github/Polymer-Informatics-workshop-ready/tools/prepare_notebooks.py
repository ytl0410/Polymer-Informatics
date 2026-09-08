#!/usr/bin/env python3
"""Apply the reproducible workshop cleanup to the four source notebooks."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SETUP_MARKDOWN = """# Workshop runtime setup

Run the notebook from the project folder. The same setup supports a local Jupyter
kernel and Google Colab. Install the pinned environment once with
`python -m pip install -r requirements-workshop.txt`.

The repository defaults to **dry-run mode**, which keeps every teaching stage but
uses shorter model training and smaller visualization samples. Set the environment
variable `POLYMER_WORKSHOP_DRY_RUN=0` before starting Jupyter for the full workshop
parameters.
"""

SETUP_CODE = """from pathlib import Path
import os
import sys

IN_COLAB = False
try:
    from google.colab import drive
    IN_COLAB = True
    drive.mount('/content/drive')
except ImportError:
    pass

candidates = []
if os.getenv('POLYMER_WORKSHOP_ROOT'):
    candidates.append(Path(os.environ['POLYMER_WORKSHOP_ROOT']).expanduser())
candidates.extend([
    Path.cwd(),
    Path.cwd().parent,
    Path('/content/drive/MyDrive/SPE'),
])

PROJECT_ROOT = next((p.resolve() for p in candidates if (p / 'Tg.csv').is_file()), None)
if PROJECT_ROOT is None:
    raise FileNotFoundError(
        'Cannot find Tg.csv. Start Jupyter in the project folder or set '
        'POLYMER_WORKSHOP_ROOT to the project directory.'
    )

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from workshop_config import *

path = str(PROJECT_ROOT) + os.sep  # Backward-compatible alias used below.
print(f'Project root: {PROJECT_ROOT}')
print(f'Runtime mode: {mode_label()}')
"""


def markdown_cell(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(True)}


def code_cell(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(True),
    }


def source(cell: dict) -> str:
    value = cell.get("source", [])
    return value if isinstance(value, str) else "".join(value)


def set_source(cell: dict, value: str) -> None:
    cell["source"] = value.splitlines(True)


def replace_setup(notebook: dict, heading: str) -> None:
    index = next(
        i for i, cell in enumerate(notebook["cells"])
        if cell["cell_type"] == "markdown" and heading in source(cell)
    )
    notebook["cells"] = [markdown_cell(SETUP_MARKDOWN), code_cell(SETUP_CODE)] + notebook["cells"][index:]


def common_replacements(text: str) -> str:
    replacements = {
        "range(6000)": "range(len(Tg_df))",
        "open(\"Corr_All.pickle\",\"wb\")": "open(PROJECT_ROOT / \"Corr_All.pickle\", \"wb\")",
        "open(\"unique_list_All.pickle\",\"wb\")": "open(PROJECT_ROOT / \"unique_list_All.pickle\", \"wb\")",
        "open(\"polymer.keys_All.pickle\",\"wb\")": "open(PROJECT_ROOT / \"polymer.keys_All.pickle\", \"wb\")",
        "open(\"Columns_All.pickle\",\"wb\")": "open(PROJECT_ROOT / \"Columns_All.pickle\", \"wb\")",
        "Input(shape=([1024])": "Input(shape=(X.shape[1],)",
        "Input(shape=([1210])": "Input(shape=(X.shape[1],)",
        "Input(shape=([148])": "Input(shape=(X.shape[1],)",
        "epochs=200": "epochs=KERAS_EPOCHS",
        "epochs = 200": "epochs = KERAS_EPOCHS",
        "n_estimators=100": "n_estimators=RF_TREES",
        "np.logspace(-4, 1, 10)": "np.logspace(-4, 1, LASSO_GRID_POINTS)",
        "RepeatedKFold(n_splits=5,random_state=42,n_repeats=2)": "RepeatedKFold(n_splits=CV_SPLITS, random_state=42, n_repeats=CV_REPEATS)",
        "num_workers     = 6": "num_workers = 0 if DRY_RUN else 6",
        "\"/content/drive/My Drive/SPE_day3+4/Corr_All.pickle\"": "PROJECT_ROOT / \"Corr_All.pickle\"",
        "\"/content/drive/My Drive/SPE_day3+4/unique_list_All.pickle\"": "PROJECT_ROOT / \"unique_list_All.pickle\"",
        "\"/content/drive/My Drive/SPE_day3+4/Columns_All.pickle\"": "PROJECT_ROOT / \"Columns_All.pickle\"",
        "\"/content/drive/My Drive/SPE_day3+4/polymer.keys_All.pickle\"": "PROJECT_ROOT / \"polymer.keys_All.pickle\"",
        "'/content/drive/My Drive/SPE/Highest_Modulus_substructure.png'": "str(ARTIFACTS_DIR / 'Highest_Modulus_substructure.png')",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def clean_install_cell(cell: dict) -> None:
    text = source(cell)
    if cell["cell_type"] == "code" and "!pip install" in text:
        set_source(cell, "# Dependencies are installed once from requirements-workshop.txt.\n")
        cell["outputs"] = []
        cell["execution_count"] = None


def transform_overview(notebook: dict) -> None:
    replace_setup(notebook, "# Overview of Machine Learning and Polymer Informatics")


def transform_supervised(notebook: dict) -> None:
    replace_setup(notebook, "# Overview of Machine Learning and Polymer Informatics")


def transform_unsupervised(notebook: dict) -> None:
    replace_setup(notebook, "# Overview of Machine Learning and Polymer Informatics")
    for cell in notebook["cells"]:
        text = source(cell)
        text = text.replace("n_clusters = 300", "n_clusters = min(KMEANS_CLUSTERS, len(X_fingerprint_All_Polyinfo))")
        text = text.replace("n_iter=500", "n_iter=TSNE_ITERATIONS")
        text = text.replace(
            "MFF_sampled = MFF.sample(n=400, random_state=42)",
            "MFF_sampled = MFF.sample(n=min(SHAP_SAMPLES, len(MFF)), random_state=42)",
        )
        text = text.replace(
            "MFF_Eg_sampled = MFF_Eg.sample(n=400, random_state=42)",
            "MFF_Eg_sampled = MFF_Eg.sample(n=min(SHAP_SAMPLES, len(MFF_Eg)), random_state=42)",
        )
        text = text.replace(
            "background = MFF_sampled.values\ne = shap.explainers._deep.Deep(model, background)\nshap_values = e.shap_values(background)",
            "background = MFF_sampled.values\ne = shap.DeepExplainer(model, background)\nraw_shap_values = e.shap_values(background)\nshap_values = raw_shap_values if isinstance(raw_shap_values, list) else [np.asarray(raw_shap_values).squeeze()]",
        )
        text = text.replace(
            "background = MFF_Eg_sampled.values\ne = shap.explainers._deep.Deep(model_Eg, background)\nshap_values = e.shap_values(background)",
            "background = MFF_Eg_sampled.values\ne = shap.DeepExplainer(model_Eg, background)\nraw_shap_values = e.shap_values(background)\nshap_values = raw_shap_values if isinstance(raw_shap_values, list) else [np.asarray(raw_shap_values).squeeze()]",
        )
        text = text.replace("explainer = shap.KernelExplainer(model.predict,X.values)", "explainer = e")
        text = text.replace("index_polymer = 66", "index_polymer = min(66, len(Tg_df_sampled) - 1)")
        text = text.replace("Tg_df_sampled.loc[66,'Smiles']", "Tg_df_sampled.loc[index_polymer,'Smiles']")
        text = text.replace(
            "shap.force_plot(explainer.expected_value[0], shap_values[0][index_polymer,:]",
            "shap.force_plot(np.asarray(explainer.expected_value).reshape(-1)[0], shap_values[0][index_polymer,:]",
        )
        text = text.replace("df = pd.DataFrame(MFF_sampled)\n#import matplotlib as plt", "df = pd.DataFrame(MFF_Eg_sampled)\n#import matplotlib as plt", 1) if "col ='Eg(eV)'" in text else text
        if "combined_data = pd.concat([polyether_df['Smiles']" in text:
            text = text.replace(
                "# Combine the 'Smiles' columns",
                "Tg_tsne_df = (Tg_df.sample(n=min(TSNE_REFERENCE_ROWS, len(Tg_df)), random_state=RANDOM_SEED)\n"
                "               if DRY_RUN and TSNE_REFERENCE_ROWS else Tg_df)\n\n# Combine the 'Smiles' columns",
            ).replace("PBI_df['Smiles'], Tg_df['Smiles']", "PBI_df['Smiles'], Tg_tsne_df['Smiles']")
        if "with open(\"shap_values_{}.pkl\".format(col), \"wb\")" in text:
            text = text.replace(
                "open(\"shap_values_{}.pkl\".format(col), \"wb\")",
                "open(ARTIFACTS_DIR / \"shap_values_{}.pkl\".format(col), \"wb\")",
            ).replace(
                "open(\"shap_values_{}.pkl\".format(col), \"rb\")",
                "open(ARTIFACTS_DIR / \"shap_values_{}.pkl\".format(col), \"rb\")",
            )
        if "open(\"shap_df_{}.pkl\".format(col), \"wb\")" in text:
            text = text.replace(
                "open(\"shap_df_{}.pkl\".format(col), \"wb\")",
                "open(ARTIFACTS_DIR / \"shap_df_{}.pkl\".format(col), \"wb\")",
            )
        text = text.replace('open("shap_df_Tg(C).pkl","rb")', 'open(ARTIFACTS_DIR / "shap_df_Tg(C).pkl", "rb")')
        text = text.replace('open("shap_df_Eg(eV).pkl","rb")', 'open(ARTIFACTS_DIR / "shap_df_Eg(eV).pkl", "rb")')
        set_source(cell, text)


def transform_generative(notebook: dict) -> None:
    replace_setup(notebook, "# Establish and train the predictor")
    for cell in notebook["cells"]:
        text = source(cell)
        if "class FFNN(nn.Module):" in text and "def fitness_function" in text:
            text = text.replace("from tartarus import pce\n", "")
            before = text.index("class FFNN(nn.Module):")
            prefix = text[:before]
            text = prefix + '''class FFNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(1024, 256)
        self.fc2 = nn.Linear(256, 64)
        self.fc3 = nn.Linear(64, 2048)
        self.fc4 = nn.Linear(2048, 512)
        self.fc5 = nn.Linear(512, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        x = torch.relu(self.fc4(x))
        return self.fc5(x)


tg_model = FFNN()
tg_state = torch.load(PROJECT_ROOT / 'Tg.pth', map_location='cpu', weights_only=True)
tg_model.load_state_dict(tg_state)
tg_model.eval()


def fitness_function(smi: str):
    """Return a bounded high-Tg fitness score; invalid structures score zero."""
    mol = Chem.MolFromSmiles(smi) if isinstance(smi, str) else None
    if mol is None:
        return 0.0
    fingerprint = AllChem.GetMorganFingerprintAsBitVect(mol, radius=3, nBits=1024)
    inputs = torch.tensor(list(fingerprint), dtype=torch.float32)
    with torch.no_grad():
        predicted_tg = tg_model(inputs).item()
    return 1 / (1 + math.exp(-0.014391156900419547 * (predicted_tg - 200)))
'''
        elif "data_path" in text and "smi_list = pd.read_csv" in text:
            text = text.replace(
                "smi_list = pd.read_csv(data_path)['sm Mulligan']",
                "smi_list = pd.read_csv(data_path)['smiles']",
            )
            text = text.replace(
                "smi_list = pd.read_csv(data_path)['smiles']",
                "smi_list = pd.read_csv(data_path)['smiles']\n"
                "if DRY_RUN and LANGUAGE_MODEL_ROWS:\n"
                "    smi_list = smi_list.sample(n=min(LANGUAGE_MODEL_ROWS, len(smi_list)), random_state=RANDOM_SEED).reset_index(drop=True)",
                1,
            )
        elif "model = LanguageModel(1024, 3" in text:
            text = text.replace(
                "model = LanguageModel(1024, 3, dm.len_alphabet, dm.len_molecule)",
                "model = LanguageModel(LANGUAGE_MODEL_HIDDEN_DIM, LANGUAGE_MODEL_LAYERS, dm.len_alphabet, dm.len_molecule, dropout=0.0 if LANGUAGE_MODEL_LAYERS == 1 else 0.2)",
            ).replace(
                "CSVLogger(os.path.join(os.getcwd(), 'trained_models'), name=string_type)",
                "CSVLogger(str(ARTIFACTS_DIR / 'trained_models'), name=string_type)",
            ).replace("accelerator = 'gpu'", "accelerator = 'auto'").replace(
                "max_epochs = 5", "max_epochs = LANGUAGE_MODEL_EPOCHS"
            )
            text += "\nmodel_path = str(Path(logger.log_dir) / 'final_model.ckpt')\n"
        elif "model_path      = path+'/version_0/final_model.ckpt'" in text and "num_generations = 100" in text:
            text = text.replace("model_path      = path+'/version_0/final_model.ckpt'", "model_path = str(Path(model_path))")
            text = text.replace("num_generations = 100", "num_generations = 20 if DRY_RUN else 100")
        elif "out_path       = 'RESULTS_retrain_{string_type}_PI'" in text:
            text = text.replace("model_path      = path+'/version_0/final_model.ckpt'", "model_path = str(Path(model_path))")
            text = text.replace("out_path       = 'RESULTS_retrain_{string_type}_PI'", "out_path = str(ARTIFACTS_DIR / f'RESULTS_retrain_{string_type}_PI')")
            text = text.replace("num_generations = 15", "num_generations = RL_GENERATIONS")
            text = text.replace("num_best        = 10", "num_best = RL_NUM_BEST")
            text = text.replace("num_randomize   = 5", "num_randomize = RL_NUM_RANDOMIZE")
            text = text.replace("samps_per_seed  = 2", "samps_per_seed = RL_SAMPLES_PER_SEED")
        elif "class FFNN(nn.Module):" in text and "loaded_model" in text:
            text = "loaded_model = tg_model\n"
        elif "fn =  collector_valid_unique.smiles" in text:
            text = '''collector_valid_unique = collector_valid_unique.copy()
if collector_valid_unique.empty:
    collector_valid_unique['Tg'] = pd.Series(dtype=float)
else:
    fn = collector_valid_unique.smiles.apply(Chem.MolFromSmiles).apply(
        lambda m: AllChem.GetMorganFingerprintAsBitVect(m, radius=3, nBits=1024)
    )
    new_inputs = torch.tensor([list(fp) for fp in fn], dtype=torch.float32)
    with torch.no_grad():
        collector_valid_unique['Tg'] = tg_model(new_inputs).numpy().reshape(-1)

collector['Tg'] = None
collector = collector.sort_values(by='generation')
smiles_to_tg = pd.Series(
    collector_valid_unique['Tg'].values,
    index=collector_valid_unique['smiles'],
).to_dict()
collector['Tg'] = collector['smiles'].map(smiles_to_tg)
'''
        elif "Trainset = pd.read_csv(path+'PolyInfo.csv')" in text:
            text = text.replace(
                "Trainset = pd.read_csv(path+'PolyInfo.csv')",
                "Trainset = pd.read_csv(PROJECT_ROOT / 'PolyInfo.csv')\n"
                "if DRY_RUN and TSNE_REFERENCE_ROWS:\n"
                "    Trainset = Trainset.sample(n=min(TSNE_REFERENCE_ROWS, len(Trainset)), random_state=RANDOM_SEED).reset_index(drop=True)",
            ).replace("n_iter=300", "n_iter=TSNE_ITERATIONS")
        elif "model_path      = f'/version_0/final_model.ckpt'" in text:
            text = text.replace("model_path      = f'/version_0/final_model.ckpt'", "model_path = str(Path(model_path))")
            text = text.replace("out_path        = f'RESULTS_retrain'", "out_path = str(ARTIFACTS_DIR / 'RESULTS_generate_once')")
            text = text.replace("num_generations = 14", "num_generations = 1 if DRY_RUN else 14")
            text = text.replace("num_best        = 10", "num_best = RL_NUM_BEST")
            text = text.replace("num_randomize   = 5", "num_randomize = RL_NUM_RANDOMIZE")
            text = text.replace("samps_per_seed  = 10", "samps_per_seed = RL_SAMPLES_PER_SEED")
        set_source(cell, text)


TRANSFORMS = {
    "1_Overview.ipynb": transform_overview,
    "2_Supervised_Learning.ipynb": transform_supervised,
    "3_Unsupervised_Learning.ipynb": transform_unsupervised,
    "4_Generative_models.ipynb": transform_generative,
}


def main() -> None:
    for name, transform in TRANSFORMS.items():
        path = ROOT / name
        notebook = json.loads(path.read_text(encoding="utf-8"))
        if notebook["cells"] and "# Workshop runtime setup" in source(notebook["cells"][0]):
            print(f"Already prepared: {name}")
            continue
        transform(notebook)
        for cell in notebook["cells"]:
            text = common_replacements(source(cell))
            set_source(cell, text)
            clean_install_cell(cell)
            if cell["cell_type"] == "code":
                cell["outputs"] = []
                cell["execution_count"] = None
        path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"Prepared {name}")


if __name__ == "__main__":
    main()
