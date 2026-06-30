#!/usr/bin/env python3
"""One-command desktop workflow for Yuanli Health OS v2.5.

Default behavior:
1. Find a local Apple Health export zip under apple-health-export/.
2. Generate private/health.local.json when an export is found.
3. Generate private/reports/quarterly-report.html when private data exists.
4. Start the local private cockpit runtime.

This script does not upload data. Private outputs stay under gitignored folders.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT_DIR = ROOT / 'apple-health-export'
DEFAULT_PRIVATE = ROOT / 'private' / 'health.local.json'
DEFAULT_REPORT = ROOT / 'private' / 'reports' / 'quarterly-report.html'


def run(cmd: list[str]) -> int:
    print('\n$ ' + ' '.join(str(c) for c in cmd))
    return subprocess.call(cmd, cwd=str(ROOT))


def find_export(user_path: str | None) -> Path | None:
    if user_path:
        p = Path(user_path).expanduser()
        return p if p.is_absolute() else ROOT / p
    if not DEFAULT_EXPORT_DIR.exists():
        return None
    zips = sorted(DEFAULT_EXPORT_DIR.glob('*.zip'), key=lambda p: p.stat().st_mtime, reverse=True)
    if zips:
        return zips[0]
    xmls = sorted(DEFAULT_EXPORT_DIR.rglob('export.xml'), key=lambda p: p.stat().st_mtime, reverse=True)
    return xmls[0] if xmls else None


def main() -> None:
    p = argparse.ArgumentParser(description='Run Yuanli Health OS desktop workflow.')
    p.add_argument('--export', help='Apple Health export.zip or export.xml. Default: newest file under apple-health-export/.')
    p.add_argument('--private-out', default=str(DEFAULT_PRIVATE))
    p.add_argument('--report-out', default=str(DEFAULT_REPORT))
    p.add_argument('--skip-import', action='store_true')
    p.add_argument('--skip-report', action='store_true')
    p.add_argument('--no-open', action='store_true')
    p.add_argument('--port', type=int, default=8787)
    args = p.parse_args()

    print('Yuanli Health OS v2.5 desktop workflow')
    print(f'root: {ROOT}')

    export_path = find_export(args.export)

    if not args.skip_import:
        if export_path and export_path.exists():
            print(f'Apple Health export: {export_path}')
            code = run([
                sys.executable,
                'scripts/import_apple_health.py',
                str(export_path),
                '--private-out',
                args.private_out,
            ])
            if code != 0:
                raise SystemExit(code)
        else:
            print('Apple Health export not found. Skipping import.')
            print('Put export.zip under apple-health-export/ or pass --export path/to/export.zip')

    private_path = Path(args.private_out)
    if not private_path.is_absolute():
        private_path = ROOT / private_path

    if not args.skip_report:
        if private_path.exists():
            code = run([
                sys.executable,
                'scripts/build_quarterly_report.py',
                '--input',
                args.private_out,
                '--output',
                args.report_out,
            ])
            if code != 0:
                raise SystemExit(code)
        else:
            print('private/health.local.json not found. Skipping quarterly report.')

    cmd = [sys.executable, 'scripts/run_local_cockpit.py', '--port', str(args.port)]
    if args.no_open:
        cmd.append('--no-open')
    raise SystemExit(run(cmd))


if __name__ == '__main__':
    main()
