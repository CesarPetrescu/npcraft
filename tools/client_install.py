#!/usr/bin/env python3
"""Install unmodified official client files for an isolated Linux visual test.

No credentials are read, no authenticated public server is contacted, and no game
binary is redistributed. This is not a general-purpose Minecraft launcher.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import urllib.request
import zipfile
from tools.server_test import MANIFEST, get_json


def fetch(url: str, path: Path, sha1: str | None = None) -> Path:
    if not url.startswith('https://'):
        raise ValueError('Only HTTPS downloads are permitted')
    if path.is_file() and (not sha1 or hashlib.sha1(path.read_bytes()).hexdigest() == sha1):
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=90) as response:
                data = response.read()
            if sha1 and hashlib.sha1(data).hexdigest() != sha1:
                raise ValueError(f'Download hash mismatch: {path.name}')
            path.write_bytes(data)
            return path
        except Exception:
            if attempt == 2:
                raise
    raise AssertionError('unreachable')


def allowed(rules: list[dict]) -> bool:
    if not rules:
        return True
    result = False
    for rule in rules:
        os = rule.get('os', {})
        if os.get('name', 'linux') != 'linux':
            continue
        if os.get('arch', 'x86_64') not in ('x86_64', 'amd64', 'x64'):
            continue
        if os.get('version') and not re.search(os['version'], __import__('platform').release()):
            continue
        if rule.get('features'):
            continue
        result = rule['action'] == 'allow'
    return result


def install(version: str, root: Path) -> tuple[dict, list[Path], Path]:
    manifest = get_json(MANIFEST)
    entry = next(x for x in manifest['versions'] if x['id'] == version)
    meta = get_json(entry['url'])
    if meta['id'] != version:
        raise ValueError('Exact version mismatch')
    root.mkdir(parents=True, exist_ok=True)
    (root / 'version.json').write_text(json.dumps(meta, indent=2))
    client = meta['downloads']['client']
    client_path = fetch(client['url'], root / 'client.jar', client['sha1'])
    natives = root / 'natives'
    natives.mkdir(exist_ok=True)
    jobs: dict[Path, tuple[str, str | None]] = {}
    classpath = []
    native_archives = []
    for lib in meta['libraries']:
        if not allowed(lib.get('rules', [])):
            continue
        downloads = lib.get('downloads', {})
        artifact = downloads.get('artifact')
        if artifact:
            path = root / 'libraries' / artifact['path']
            jobs[path] = (artifact['url'], artifact.get('sha1'))
            classpath.append(path)
            if 'natives-linux' in lib['name']:
                native_archives.append(path)
        classifier = lib.get('natives', {}).get('linux', '').replace('${arch}', '64')
        if classifier:
            item = downloads['classifiers'][classifier]
            path = root / 'libraries' / item['path']
            jobs[path] = (item['url'], item.get('sha1'))
            native_archives.append(path)
    index = meta['assetIndex']
    idx_path = fetch(index['url'], root / 'assets/indexes' / (index['id'] + '.json'), index['sha1'])
    assets = json.loads(idx_path.read_text())
    for item in assets['objects'].values():
        h = item['hash']
        jobs[root / 'assets/objects' / h[:2] / h] = ('https://resources.download.minecraft.net/' + h[:2] + '/' + h, h)
    print(f'Installing exact Minecraft {version}: {len(classpath)} libraries, {len(jobs)} verified objects', flush=True)
    with ThreadPoolExecutor(max_workers=16) as pool:
        list(pool.map(lambda pair: fetch(pair[1][0], pair[0], pair[1][1]), jobs.items()))
    for archive in native_archives:
        with zipfile.ZipFile(archive) as zf:
            for name in zf.namelist():
                if name.endswith('.so'):
                    (natives / Path(name).name).write_bytes(zf.read(name))
    logging = meta.get('logging', {}).get('client', {})
    if logging.get('file'):
        f = logging['file']
        fetch(f['url'], root / f['id'], f.get('sha1'))
    classpath.append(client_path)
    return meta, classpath, natives
