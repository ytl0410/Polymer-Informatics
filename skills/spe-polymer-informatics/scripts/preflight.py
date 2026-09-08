#!/usr/bin/env python3
"""Read-only inventory for the original SPE notebooks; never installs or runs code."""

import argparse
import ast
import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import sys

NOTEBOOKS = (
    '1_Overview.ipynb', '2_Supervised_Learning.ipynb',
    '3_Unsupervised_Learning.ipynb', '4_Generative_models.ipynb',
)
TABLES = {
    'Tg.csv': ('Smiles', 'Tg(C)'),
    'Eg.csv': ('Smiles', 'Eg(eV)'),
    'PolyInfo.csv': ('smiles',),
    'diCOOH.csv': ('Smiles',),
    '202207_smip_monset.csv': ('SMILES',),
}
OPTIONAL_TABLES = {'Tm.csv': ('Smiles', 'Tm(C)')}
REQUIRED = (
    *NOTEBOOKS, *TABLES, 'Tg.pth',
    'lstm_climber/network.py', 'lstm_climber/datamodules.py',
    'lstm_climber/utils.py', 'lstm_climber/__init__.py',
    'tartarus/__init__.py', 'tartarus/pce.py',
    'Columns_All.pickle', 'Corr_All.pickle', 'unique_list_All.pickle',
    'polymer.keys_All.pickle',
)
LOCAL_REFERENCE = {
    'numpy': '==1.26.4', 'matplotlib': '==3.8.0',
    'pandas': '==1.5.3', 'rdkit': '==2023.9.1',
    'scikit-learn': '==1.3.0', 'keras-tuner': '==1.4.5',
    'seaborn': '==0.13.0', 'tensorflow': '<2.11',
}
OTHER_PACKAGES = (
    'torch', 'torchaudio', 'torchvision', 'pytorch-lightning',
    'torchmetrics', 'selfies', 'shap', 'smipoly', 'setuptools',
)
PREPARED_MARKERS = (
    'workshop_config.py', 'requirements-workshop.txt',
    'tools/run_all_notebooks.py',
)


def source(cell):
    value = cell.get('source', '')
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(isinstance(line, str) for line in value):
        return ''.join(value)
    raise ValueError('Notebook cell source must be a string or a list of strings')


def inspect(project, check_environment=False):
    project = Path(project).expanduser().resolve()
    result = {
        'project': str(project), 'python': sys.version.split()[0],
        'interpreter': sys.executable, 'platform': platform.platform(),
        'errors': [], 'notes': [], 'tables': {}, 'notebooks': {}, 'packages': {},
        'execution_status': 'not_run',
        'environment_compatibility': 'not_validated',
        'baseline_detection': 'no_prepared_markers_detected',
        'local_reference_python': '3.9 (reference only; not a Colab requirement)',
    }
    markers = [name for name in PREPARED_MARKERS if (project / name).is_file()]
    if markers:
        result['baseline_detection'] = 'prepared_markers_detected'
        result['notes'].append(
            'Modified-copy files found: ' + ', '.join(markers) +
            '. Confirm the original teaching copy before following its workflow.'
        )
    result['notes'].append(
        'Marker detection does not prove file provenance; notebook hashes identify this copy.'
    )
    for name in REQUIRED:
        if not (project / name).is_file():
            result['errors'].append(f'Missing required file: {name}')
    for name, columns in {**TABLES, **OPTIONAL_TABLES}.items():
        path = project / name
        if not path.is_file():
            if name in OPTIONAL_TABLES:
                result['notes'].append(f'Optional practice dataset not found: {name}')
            continue
        try:
            with path.open(encoding='utf-8-sig', newline='') as handle:
                reader = csv.DictReader(handle)
                fields = reader.fieldnames or []
                missing = set(columns) - set(fields)
                count = sum(1 for _ in reader)
            result['tables'][name] = {'rows': count, 'columns': fields}
            if missing or not count:
                result['errors'].append(
                    f'{name}: missing columns {sorted(missing)}; rows={count}'
                )
        except (OSError, UnicodeError, csv.Error) as exc:
            result['errors'].append(f'{name}: {exc}')

    for name in NOTEBOOKS:
        path = project / name
        if not path.is_file():
            continue
        try:
            raw = path.read_bytes()
            notebook = json.loads(raw.decode('utf-8-sig'))
            if not isinstance(notebook, dict) or not isinstance(notebook.get('cells'), list):
                raise ValueError('Expected a notebook object with a cells list')
            cells = notebook['cells']
            commands = []
            code_count = saved_errors = unexecuted = ipython_cells = 0
            for i, cell in enumerate(cells):
                if not isinstance(cell, dict):
                    raise ValueError(f'Cell {i} is not an object')
                text = source(cell)
                if cell.get('cell_type') != 'code' or not text.strip():
                    continue
                code_count += 1
                unexecuted += cell.get('execution_count') is None
                outputs = cell.get('outputs', [])
                if not isinstance(outputs, list) or not all(isinstance(o, dict) for o in outputs):
                    raise ValueError(f'Cell {i} outputs must be a list of objects')
                saved_errors += sum(o.get('output_type') == 'error' for o in outputs)
                for line in text.splitlines():
                    if re.search(r'\bpip(?:3)?\s+install\b', line):
                        commands.append({'cell_index': i, 'command': line.strip()})
                if 'workshop_config' in text:
                    result['baseline_detection'] = 'prepared_markers_detected'
                if any(line.lstrip().startswith(('!', '%')) for line in text.splitlines()):
                    ipython_cells += 1
                    continue
                try:
                    ast.parse(text)
                except SyntaxError as exc:
                    result['errors'].append(f'{name}, cell {i}: {exc.msg}')
            result['notebooks'][name] = {
                'nonempty_code_cells': code_count,
                'sha256': hashlib.sha256(raw).hexdigest(),
                'installation_commands': commands,
                'ipython_cells_requiring_live_check': ipython_cells,
                'saved_output_summary': {
                    'error_outputs': saved_errors,
                    'cells_without_execution_count': unexecuted,
                    'evidence': 'historical source-notebook outputs; not a new run',
                },
            }
            if saved_errors:
                result['notes'].append(
                    f'{name}: {saved_errors} saved error outputs; their history is not a current run.'
                )
        except (OSError, ValueError, UnicodeError) as exc:
            result['errors'].append(f'{name}: {exc}')

    if check_environment:
        for package in (*LOCAL_REFERENCE, *OTHER_PACKAGES):
            try:
                actual = importlib.metadata.version(package)
            except importlib.metadata.PackageNotFoundError:
                actual = None
            result['packages'][package] = {
                'installed': actual,
                'original_local_reference': LOCAL_REFERENCE.get(package),
            }
        result['notes'].append(
            'Installed versions are observations, not a compatibility verdict. '
            'Use each notebook installation cell and the actual kernel; do not '
            'force Colab to match the local reference or upgrade a working environment.'
        )
    result['notes'].append(
        'Preflight does not install packages, execute notebooks, validate chemistry, '
        'deserialize weights/pickles, or verify Colab/GPU access. IPython cells '
        'and imports still need a live-kernel check.'
    )
    result['status'] = 'failed' if result['errors'] else 'passed_inventory_checks'
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', default=os.environ.get('POLYMER_WORKSHOP_ROOT', '.'))
    parser.add_argument(
        '--check-environment', action='store_true',
        help='Record installed versions and the original local reference without enforcing it',
    )
    args = parser.parse_args()
    try:
        result = inspect(args.project, args.check_environment)
    except (OSError, ValueError) as exc:
        result = {'status': 'failed', 'errors': [f'{type(exc).__name__}: {exc}']}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result['status'] == 'passed_inventory_checks' else 1


if __name__ == '__main__':
    raise SystemExit(main())
