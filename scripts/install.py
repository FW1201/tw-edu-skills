#!/usr/bin/env python3
"""Install independent Skills with preview and recoverable updates."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = '.tw-edu-install.json'

def canonical_destination(path):
    """Return an explicit destination path while rejecting user-controlled symlink ancestors."""
    path = path.expanduser().absolute()
    if '..' in path.parts:
        raise ValueError('Parent traversal is not accepted in installation destinations')
    # macOS exposes these system aliases as symlinks. Normalize them before
    # inspecting user-controlled components so /tmp safely means /private/tmp.
    if sys.platform == 'darwin' and len(path.parts) > 1:
        aliases = {'tmp': ('private', 'tmp'), 'var': ('private', 'var'), 'etc': ('private', 'etc')}
        replacement = aliases.get(path.parts[1])
        if replacement:
            path = Path('/').joinpath(*replacement, *path.parts[2:])
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            raise ValueError(f'Refusing symlink path component: {current}')
        if not current.exists():
            break
    return path

def hashes(path):
    result = {}
    for item in sorted(path.rglob('*')):
        if item.is_symlink():
            raise ValueError(f'Symlinks are not accepted: {item}')
        if item.is_file() and item.name != RECEIPT and '__pycache__' not in item.parts:
            result[item.relative_to(path).as_posix()] = hashlib.sha256(item.read_bytes()).hexdigest()
    return result

def validate_package(path):
    if not (path / 'SKILL.md').is_file():
        raise ValueError(f'Missing SKILL.md: {path}')
    hashes(path)
    if not (path / 'references/common/workflow.md').is_file():
        raise ValueError(f'Missing bundled workflow: {path}')

def check_destination(destination, force):
    if destination.is_symlink():
        raise ValueError(f'Refusing symlink destination: {destination}')
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f'Not a directory: {destination}')
        receipt = destination / RECEIPT
        recorded = json.loads(receipt.read_text()) if receipt.is_file() else {}
        if recorded.get('files') != hashes(destination) and not force:
            raise ValueError(f'Custom or unmanaged files: {destination}; inspect and use --force (backup retained)')

def prepare_one(source, destination, force=False):
    validate_package(source)
    destination = canonical_destination(destination)
    check_destination(destination, force)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.tw-edu-stage-', dir=destination.parent))
    staged = stage / source.name
    try:
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        validate_package(staged)
        (staged / RECEIPT).write_text(json.dumps({'skill': source.name, 'files': hashes(staged)}, indent=2), encoding='utf-8')
        return {'source': source, 'destination': destination, 'stage': stage, 'staged': staged, 'backup': None}
    except Exception:
        shutil.rmtree(stage)
        raise

def install_many(sources, destination_root, force=False):
    destination_root = canonical_destination(destination_root)
    prepared = []
    committed = []
    try:
        for source in sources:
            prepared.append(prepare_one(source, destination_root / source.name, force))
        for item in prepared:
            destination = item['destination']
            if destination.exists():
                item['backup'] = destination.parent / f'.{item["source"].name}.backup-{uuid.uuid4().hex}'
                os.replace(destination, item['backup'])
            try:
                os.replace(item['staged'], destination)
            except Exception:
                if item['backup'] is not None:
                    os.replace(item['backup'], destination)
                raise
            committed.append(item)
        return [item['backup'] for item in prepared]
    except Exception:
        rollback_errors = []
        for item in reversed(committed):
            try:
                displaced = item['stage'] / 'rolled-back-install'
                os.replace(item['destination'], displaced)
                if item['backup'] is not None:
                    os.replace(item['backup'], item['destination'])
            except Exception as exc:
                rollback_errors.append(f"{item['destination']}: {exc}")
        if rollback_errors:
            raise RuntimeError('Installation failed and rollback was incomplete: ' + '; '.join(rollback_errors))
        raise
    finally:
        for item in prepared:
            shutil.rmtree(item['stage'], ignore_errors=True)

def install_one(source, destination, force=False):
    backups = install_many([source], canonical_destination(destination).parent, force)
    return backups[0]

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('skill', nargs='?')
    parser.add_argument('--agent', choices=['codex', 'claude-code'], required=True)
    parser.add_argument('--dest', type=Path)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--force', action='store_true', help='Replace customized installs after backing them up')
    args = parser.parse_args(argv)
    manifest = json.loads((ROOT / 'skills-manifest.json').read_text())
    names = [s['name'] for s in manifest['skills']]
    if args.skill and args.skill not in names:
        parser.error('Unknown skill; only registered names are accepted')
    selected = [args.skill] if args.skill else names
    try:
        root = canonical_destination(args.dest or Path.home() / ('.codex/skills' if args.agent == 'codex' else '.claude/skills'))
        for name in selected:
            validate_package(ROOT / name)
            check_destination(root / name, args.force)
        if args.dry_run:
            for name in selected:
                destination = root / name
                print(f'PREVIEW {name} -> {destination}')
        else:
            backups = install_many([ROOT / name for name in selected], root, args.force)
            for name, backup in zip(selected, backups):
                destination = root / name
                print(f'INSTALLED {destination}' + (f' BACKUP {backup}' if backup else ''))
        return 0
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Installation failed: {exc}\n')

if __name__ == '__main__':
    raise SystemExit(main())
