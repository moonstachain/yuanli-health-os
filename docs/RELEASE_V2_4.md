# Release v2.4

## Local private cockpit runtime

v2.4 connects the private/local data layer to the desktop cockpit while keeping the public GitHub Pages demo safe.

## Implemented

### 1. Local runtime server

New file:

```txt
scripts/run_local_cockpit.py
```

Capabilities:

- Runs the cockpit at `http://127.0.0.1:8787/app.html`.
- Intercepts `data/demo-health.json` requests.
- Serves a merged private payload from `private/health.local.json` when available.
- Falls back to the public demo data when private data is missing.
- Blocks direct browser access to `private/`, `raw-data/`, `apple-health-export/`, and `exports/`.

### 2. Local runtime guide

New file:

```txt
docs/LOCAL_RUNTIME.md
```

It documents the safe local workflow:

1. Place Apple Health export locally.
2. Generate `private/health.local.json`.
3. Run the local cockpit server.
4. Generate quarterly report.

## Suggested local workflow

```bash
python3 scripts/import_apple_health.py apple-health-export/export.zip \
  --private-out private/health.local.json

python3 scripts/run_local_cockpit.py
```

Open:

```txt
http://127.0.0.1:8787/app.html
```

## Public vs local behavior

| Environment | Data source | Privacy posture |
|---|---|---|
| GitHub Pages | `data/demo-health.json` | public-minimized demo |
| Local runtime | merged `private/health.local.json` | local private runtime |

## Next version

v2.5 should add a one-command desktop workflow and optional local-only report archive index.
