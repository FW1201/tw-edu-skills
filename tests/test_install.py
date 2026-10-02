import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('installer', ROOT / 'scripts/install.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)

def package(tmp_path):
    source = tmp_path / 'source' / 'tw-edu-test'
    (source / 'references/common').mkdir(parents=True)
    (source / 'SKILL.md').write_text('skill')
    (source / 'references/common/workflow.md').write_text('workflow')
    return source

def test_backup_custom_and_update(tmp_path):
    source = package(tmp_path)
    dest = tmp_path / 'installed' / source.name
    assert installer.install_one(source, dest) is None
    (dest / 'custom.txt').write_text('KEEP ME')
    with pytest.raises(ValueError):
        installer.install_one(source, dest)
    backup = installer.install_one(source, dest, force=True)
    assert (backup / 'custom.txt').read_text() == 'KEEP ME'
    assert not (dest / 'custom.txt').exists()
    assert installer.install_one(source, dest).exists()

def test_rollback_after_failed_swap(tmp_path):
    source = package(tmp_path)
    dest = tmp_path / 'installed' / source.name
    installer.install_one(source, dest)
    (source / 'SKILL.md').write_text('new')
    real_replace = installer.os.replace
    def fail_staged(src, dst):
        if '.tw-edu-stage-' in str(src):
            raise OSError('simulated swap failure')
        return real_replace(src, dst)
    with patch.object(installer.os, 'replace', side_effect=fail_staged):
        with pytest.raises(OSError):
            installer.install_one(source, dest)
    assert (dest / 'SKILL.md').read_text() == 'skill'
    assert not list(dest.parent.glob('.tw-edu-stage-*'))

def test_symlink_refused(tmp_path):
    source = package(tmp_path)
    dest = tmp_path / 'link'
    dest.symlink_to(source, target_is_directory=True)
    with pytest.raises(ValueError):
        installer.install_one(source, dest, force=True)

def test_symlinked_ancestor_refused_without_touching_target(tmp_path):
    source = package(tmp_path)
    actual = tmp_path / 'actual'
    actual.mkdir()
    alias = tmp_path / 'alias'
    alias.symlink_to(actual, target_is_directory=True)

    with pytest.raises(ValueError, match='symlink path component'):
        installer.install_one(source, alias / source.name)

    assert list(actual.iterdir()) == []

def test_invalid_name_cannot_touch_root(tmp_path):
    target = tmp_path / 'untouched'
    r = subprocess.run([sys.executable, str(ROOT / 'scripts/install.py'), '../escape', '--agent', 'codex', '--dest', str(target)], capture_output=True)
    assert r.returncode != 0
    assert not target.exists()

def test_dry_run_and_both_hosts(tmp_path):
    for host in ['codex', 'claude-code']:
        target = tmp_path / host
        cmd = [sys.executable, str(ROOT / 'scripts/install.py'), '--agent', host, '--dest', str(target)]
        r = subprocess.run(cmd + ['--dry-run'], capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        assert not target.exists()
        r = subprocess.run(cmd, capture_output=True, text=True)
        assert r.returncode == 0, r.stderr
        assert len(list(target.glob('tw-edu-*/SKILL.md'))) == len(json.loads((ROOT / 'skills-manifest.json').read_text())['skills'])
        manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
        for skill in manifest['skills']:
            assert installer.hashes(target / skill['name']) == installer.hashes(ROOT / skill['name'])

def test_all_skill_transaction_rolls_back_prior_swaps(tmp_path):
    first = package(tmp_path)
    second = tmp_path / 'source' / 'tw-edu-second'
    (second / 'references/common').mkdir(parents=True)
    (second / 'SKILL.md').write_text('old second')
    (second / 'references/common/workflow.md').write_text('workflow')
    destination_root = tmp_path / 'installed'
    installer.install_many([first, second], destination_root)

    (first / 'SKILL.md').write_text('new first')
    (second / 'SKILL.md').write_text('new second')
    real_replace = installer.os.replace
    staged_swaps = 0

    def fail_second_swap(src, dst):
        nonlocal staged_swaps
        if '.tw-edu-stage-' in str(src) and Path(dst).name.startswith('tw-edu-'):
            staged_swaps += 1
            if staged_swaps == 2:
                raise OSError('simulated second swap failure')
        return real_replace(src, dst)

    with patch.object(installer.os, 'replace', side_effect=fail_second_swap):
        with pytest.raises(OSError, match='second swap'):
            installer.install_many([first, second], destination_root)

    assert (destination_root / first.name / 'SKILL.md').read_text() == 'skill'
    assert (destination_root / second.name / 'SKILL.md').read_text() == 'old second'
    assert not list(destination_root.glob('.tw-edu-stage-*'))
