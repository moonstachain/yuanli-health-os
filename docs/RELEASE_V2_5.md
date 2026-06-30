# Release v2.5

## One-command desktop workflow

v2.5 compresses the local private workflow into one command.

## Implemented

### 1. Desktop workflow orchestrator

New file:

```txt
scripts/yuanli_health_desktop.py
```

It runs the full local workflow:

1. Find the newest Apple Health export under `apple-health-export/`.
2. Generate `private/health.local.json`.
3. Generate `private/reports/quarterly-report.html`.
4. Start the local cockpit runtime.

### 2. Shell entry

New file:

```txt
run.sh
```

Use:

```bash
bash run.sh
```

### 3. Desktop workflow guide

New file:

```txt
docs/DESKTOP_WORKFLOW.md
```

It documents the one-command workflow, custom export path, skip flags and privacy boundary.

## Main command

```bash
python3 scripts/yuanli_health_desktop.py
```

Or:

```bash
bash run.sh
```

## Options

```bash
python3 scripts/yuanli_health_desktop.py --export ~/Downloads/export.zip
python3 scripts/yuanli_health_desktop.py --skip-import
python3 scripts/yuanli_health_desktop.py --skip-report
python3 scripts/yuanli_health_desktop.py --no-open
python3 scripts/yuanli_health_desktop.py --port 8790
```

## Privacy boundary

Private outputs stay under ignored local folders and should never be committed:

- `private/`
- `apple-health-export/`
- `raw-data/`
- `exports/`

The public GitHub Pages demo remains safe and continues to use public-minimized demo data.

## Next version

v2.6 should add a local-only report archive index and a preflight checker that validates Python version, input files, and private-folder safety before running.
