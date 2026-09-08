"""Regression tests for the read-only original-notebook inventory."""

import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'preflight.py'
SPEC = importlib.util.spec_from_file_location('spe_preflight', SCRIPT)
PREFLIGHT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PREFLIGHT)


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in PREFLIGHT.REQUIRED:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'fixture; never deserialize or execute')
        for name, columns in PREFLIGHT.TABLES.items():
            (self.root / name).write_text(','.join(columns) + '\n' +
                                          ','.join('1' for _ in columns) + '\n')
        for name in PREFLIGHT.NOTEBOOKS:
            self.notebook(name, ['x = 1\n', '!pip install rdkit\n'])

    def notebook(self, name, sources):
        cells = [{'cell_type': 'code', 'source': s,
                  'execution_count': None, 'outputs': []} for s in sources]
        (self.root / name).write_text(json.dumps({'nbformat': 4, 'cells': cells}))

    def hashes(self):
        return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in self.root.rglob('*') if p.is_file()}

    def test_original_requires_no_modified_helpers_and_is_read_only(self):
        before = self.hashes()
        result = PREFLIGHT.inspect(self.root)
        self.assertEqual(result['status'], 'passed_inventory_checks')
        self.assertEqual(result['execution_status'], 'not_run')
        self.assertEqual(result['environment_compatibility'], 'not_validated')
        self.assertEqual(result['baseline_detection'], 'no_prepared_markers_detected')
        self.assertEqual(before, self.hashes())
        self.assertFalse((self.root / 'workshop_config.py').exists())

    def test_installs_are_recorded_without_execution(self):
        name = PREFLIGHT.NOTEBOOKS[2]
        self.notebook(name, ['!pip install tensorflow==2.15.0\n!pip install shap==0.41.0\n'])
        result = PREFLIGHT.inspect(self.root)['notebooks'][name]
        self.assertEqual(result['ipython_cells_requiring_live_check'], 1)
        self.assertEqual([c['command'] for c in result['installation_commands']],
                         ['!pip install tensorflow==2.15.0', '!pip install shap==0.41.0'])

    def test_missing_required_file_fails(self):
        (self.root / 'Tg.csv').unlink()
        result = PREFLIGHT.inspect(self.root)
        self.assertEqual(result['status'], 'failed')
        self.assertIn('Missing required file: Tg.csv', result['errors'])

    def test_wrong_csv_header_fails(self):
        (self.root / 'Tg.csv').write_text('smiles,Tg(C)\nCC,100\n')
        result = PREFLIGHT.inspect(self.root)
        self.assertEqual(result['status'], 'failed')
        self.assertTrue(any('Smiles' in e for e in result['errors']))

    def test_optional_dataset_not_required_but_checked_if_present(self):
        self.assertEqual(PREFLIGHT.inspect(self.root)['status'], 'passed_inventory_checks')
        (self.root / 'Tm.csv').write_text('Smiles,Tm(C)\nCC,100\n')
        self.assertEqual(PREFLIGHT.inspect(self.root)['tables']['Tm.csv']['rows'], 1)

    def test_syntax_error_fails(self):
        self.notebook(PREFLIGHT.NOTEBOOKS[0], ['def broken(:'])
        self.assertEqual(PREFLIGHT.inspect(self.root)['status'], 'failed')

    def test_malformed_notebook_fails(self):
        (self.root / PREFLIGHT.NOTEBOOKS[0]).write_text('{')
        self.assertEqual(PREFLIGHT.inspect(self.root)['status'], 'failed')

    def test_prepared_markers_are_reported_not_required(self):
        (self.root / 'workshop_config.py').write_text('DRY_RUN = True\n')
        result = PREFLIGHT.inspect(self.root)
        self.assertEqual(result['status'], 'passed_inventory_checks')
        self.assertEqual(result['baseline_detection'], 'prepared_markers_detected')

    def test_different_versions_are_observations_not_failures(self):
        with patch.object(PREFLIGHT.importlib.metadata, 'version', return_value='9.9.9'):
            result = PREFLIGHT.inspect(self.root, check_environment=True)
        self.assertEqual(result['status'], 'passed_inventory_checks')
        self.assertEqual(result['packages']['tensorflow']['installed'], '9.9.9')
        self.assertEqual(result['packages']['tensorflow']['original_local_reference'], '<2.11')
        self.assertEqual(result['environment_compatibility'], 'not_validated')

    def test_saved_error_does_not_claim_a_fresh_execution_failure(self):
        path = self.root / PREFLIGHT.NOTEBOOKS[0]
        nb = json.loads(path.read_text())
        nb['cells'][0]['outputs'] = [{'output_type': 'error', 'ename': 'RuntimeError'}]
        path.write_text(json.dumps(nb))
        result = PREFLIGHT.inspect(self.root)
        self.assertEqual(result['status'], 'passed_inventory_checks')
        self.assertEqual(result['execution_status'], 'not_run')
        summary = result['notebooks'][PREFLIGHT.NOTEBOOKS[0]]['saved_output_summary']
        self.assertEqual(summary['error_outputs'], 1)


if __name__ == '__main__':
    unittest.main()
