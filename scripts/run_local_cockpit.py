#!/usr/bin/env python3
"""Run Yuanli Health OS cockpit locally with private data.

This local-only server keeps GitHub Pages safe while letting the desktop app
read `private/health.local.json` on your computer.

How it works:
- Browser opens `http://127.0.0.1:8787/app.html`.
- The app still requests `data/demo-health.json`.
- This server intercepts that request and serves a merged local/private view
  when `private/health.local.json` exists.
- Direct browser access to `private/`, `raw-data/`, `apple-health-export/`, and
  `exports/` is blocked.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import socketserver
import sys
import webbrowser
from datetime import date
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

BLOCKED_PREFIXES = ('/private/', '/raw-data/', '/apple-health-export/', '/exports/')


def deep_merge(base: dict, override: dict) -> dict:
    out = dict(base or {})
    for key, value in (override or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def range_from_daily(rows: list[dict]) -> dict:
    if not rows:
        return {'start': None, 'end': None, 'days': 0}
    return {'start': rows[0].get('date'), 'end': rows[-1].get('date'), 'days': len(rows)}


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding='utf-8'))


def local_payload(root: Path) -> dict:
    public_data = load_json(root / 'data' / 'demo-health.json')
    private_data = load_json(root / 'private' / 'health.local.json')
    if not private_data:
        return public_data

    merged = deep_merge(public_data, private_data)
    rows = merged.get('appleHealth', {}).get('dailySeries', [])
    merged.setdefault('meta', {})
    merged['meta']['schemaVersion'] = 'yuanli-health-os.v2.4-local-runtime'
    merged['meta']['updatedAt'] = date.today().isoformat()
    merged['meta']['visibility'] = 'local-private-runtime'
    merged['meta']['note'] = 'Served locally from private/health.local.json. Do not publish this payload.'
    merged.setdefault('appleHealth', {})
    merged['appleHealth']['range'] = range_from_daily(rows)
    merged['appleHealth'].setdefault('dataQuality', {})
    merged['appleHealth']['dataQuality'].setdefault('location', 'local runtime blocks direct private folder access')
    return merged


class Handler(SimpleHTTPRequestHandler):
    root: Path = Path.cwd()

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write('[yuanli-local] ' + (fmt % args) + '\n')

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/':
            self.send_response(302)
            self.send_header('Location', '/app.html')
            self.end_headers()
            return

        if path == '/data/demo-health.json':
            payload = local_payload(self.root)
            body = json.dumps(payload, ensure_ascii=False, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if any(path.startswith(prefix) for prefix in BLOCKED_PREFIXES):
            self.send_response(403)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write('403: private folder access is blocked by the local runtime.\n'.encode('utf-8'))
            return

        return super().do_GET()

    def end_headers(self):
        self.send_header('X-Yuanli-Local-Runtime', 'v2.4')
        return super().end_headers()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='127.0.0.1')
    p.add_argument('--port', type=int, default=8787)
    p.add_argument('--root', default='.')
    p.add_argument('--no-open', action='store_true')
    args = p.parse_args()

    root = Path(args.root).resolve()
    Handler.root = root
    Handler.directory = str(root)

    url = f'http://{args.host}:{args.port}/app.html'
    print('Yuanli Health OS local runtime v2.4')
    print(f'root: {root}')
    print(f'url:  {url}')
    if (root / 'private' / 'health.local.json').exists():
        print('private data: private/health.local.json found and will be merged at runtime')
    else:
        print('private data: not found; app will use public demo data')

    if not args.no_open:
        webbrowser.open(url)

    with socketserver.TCPServer((args.host, args.port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\nStopped local runtime.')


if __name__ == '__main__':
    main()
