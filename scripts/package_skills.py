#!/usr/bin/env python3
"""Package manifest-selected Skills only, with deterministic checksums."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile
from validate_skills import validate

ROOT = Path(__file__).resolve().parents[1]

def archive(path, files):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as out:
        for file in sorted(files):
            info = zipfile.ZipInfo(file.relative_to(ROOT).as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            out.writestr(info, file.read_bytes())

def verify_archive(path, files):
    expected = {file.relative_to(ROOT).as_posix(): hashlib.sha256(file.read_bytes()).hexdigest() for file in files}
    with zipfile.ZipFile(path) as bundle:
        names = bundle.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError(f'Archive inventory differs from source: {path}')
        for name in names:
            member = Path(name)
            if member.is_absolute() or '..' in member.parts:
                raise ValueError(f'Unsafe archive member: {name}')
            if hashlib.sha256(bundle.read(name)).hexdigest() != expected[name]:
                raise ValueError(f'Archive content differs from source: {name}')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=ROOT / 'dist')
    args = p.parse_args()
    errors = validate()
    if errors:
        p.exit(2, '\n'.join(errors) + '\n')
    subprocess.run([sys.executable, str(ROOT / 'scripts/sync_assets.py'), '--check'], check=True)
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    args.output.mkdir(parents=True, exist_ok=True)
    packages = []
    all_files = []
    for skill in manifest['skills']:
        files = [f for f in (ROOT / skill['name']).rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix != '.pyc' and not f.is_symlink()]
        path = args.output / f"{skill['name']}-{skill['version']}.zip"
        archive(path, files)
        verify_archive(path, files)
        packages.append(path)
        all_files.extend(files)
    whole = args.output / f"tw-edu-skills-{manifest['version']}.zip"
    aggregate_files = all_files + [
        ROOT / 'skills-manifest.json', ROOT / 'LICENSE', ROOT / 'README.md',
        ROOT / 'CONTRIBUTING.md', ROOT / 'install.sh', ROOT / 'scripts/install.py',
        *[path for path in (ROOT / 'docs').rglob('*') if path.is_file()],
    ]
    archive(whole, aggregate_files)
    verify_archive(whole, aggregate_files)
    packages.append(whole)
    (args.output / 'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in packages), encoding='utf-8')
    print(f'Packaged {len(packages)} archives into {args.output}')

if __name__ == '__main__':
    main()
