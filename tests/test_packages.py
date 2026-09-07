import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / 'skills-manifest.json').read_text())


@pytest.fixture(scope='module')
def packaged(tmp_path_factory):
    output = tmp_path_factory.mktemp('packages')
    subprocess.run(
        [sys.executable, str(ROOT / 'scripts/package_skills.py'), '--output', str(output)],
        cwd=output,
        check=True,
    )
    return output


def test_individual_archives_are_self_contained_and_validate_from_arbitrary_cwd(packaged, tmp_path):
    for skill in MANIFEST['skills']:
        archive = packaged / f"{skill['name']}-{skill['version']}.zip"
        extract_root = tmp_path / skill['name']
        with zipfile.ZipFile(archive) as bundle:
            names = bundle.namelist()
            assert names
            assert all(name.startswith(f"{skill['name']}/") for name in names)
            assert not any('..' in Path(name).parts for name in names)
            bundle.extractall(extract_root)

        installed = extract_root / skill['name']
        assert (installed / 'SKILL.md').is_file()
        assert (installed / 'references/common/workflow.md').is_file()
        if skill['entrypoint']:
            example = next((installed / 'examples').glob('*.json'))
            result = subprocess.run(
                [sys.executable, str(installed / skill['entrypoint']), '--input', str(example), '--validate-only'],
                cwd=tmp_path,
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, result.stderr


def test_aggregate_archive_installer_works_outside_repository(packaged, tmp_path):
    archive = packaged / f"tw-edu-skills-{MANIFEST['version']}.zip"
    extracted = tmp_path / 'aggregate'
    with zipfile.ZipFile(archive) as bundle:
        bundle.extractall(extracted)
    destination = tmp_path / 'installed'
    result = subprocess.run(
        [sys.executable, str(extracted / 'scripts/install.py'), '--agent', 'codex', '--dest', str(destination)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert len(list(destination.glob('tw-edu-*/SKILL.md'))) == len(MANIFEST['skills'])


def test_checksums_cover_every_archive(packaged):
    checksum_lines = (packaged / 'SHA256SUMS').read_text().splitlines()
    recorded = dict(line.split('  ', 1)[::-1] for line in checksum_lines)
    archives = sorted(packaged.glob('*.zip'))
    assert set(recorded) == {path.name for path in archives}
    for archive in archives:
        assert recorded[archive.name] == hashlib.sha256(archive.read_bytes()).hexdigest()


def test_validator_rejects_local_link_that_escapes_skill(tmp_path):
    extracted = tmp_path / 'repo'
    shutil.copytree(ROOT, extracted, ignore=shutil.ignore_patterns('.git', 'dist', '__pycache__', '*.pyc'))
    skill = extracted / MANIFEST['skills'][0]['name']
    outside = extracted / 'outside.md'
    outside.write_text('outside')
    with (skill / 'SKILL.md').open('a') as handle:
        handle.write('\n[escape](../outside.md)\n')
    result = subprocess.run(
        [sys.executable, str(extracted / 'scripts/validate_skills.py')],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert 'link escapes skill directory' in result.stdout
