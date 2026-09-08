import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

def test_missing_ancestor_cannot_hide_parent_traversal(tmp_path):
    with pytest.raises(ValueError, match='traversal'):
        installer.canonical_destination(tmp_path / 'missing' / '..' / 'target')
