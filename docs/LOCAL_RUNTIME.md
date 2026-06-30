# Local Runtime v2.4

v2.4 connects the private/local data layer to the desktop cockpit without exposing private data on GitHub Pages.

## What it does

The public site continues to load:

```txt
data/demo-health.json
```

When you run the local runtime, the local server intercepts this request and serves a merged private payload from:

```txt
private/health.local.json
```

Direct browser access to these folders is blocked by the local runtime:

```txt
private/
raw-data/
apple-health-export/
exports/
```

## Workflow

### 1. Put Apple Health export locally

```txt
apple-health-export/export.zip
```

### 2. Generate local private health data

```bash
python3 scripts/import_apple_health.py apple-health-export/export.zip \
  --private-out private/health.local.json
```

### 3. Run the local cockpit

```bash
python3 scripts/run_local_cockpit.py
```

Open:

```txt
http://127.0.0.1:8787/app.html
```

### 4. Generate quarterly report

```bash
python3 scripts/build_quarterly_report.py \
  --input private/health.local.json \
  --output private/reports/quarterly-report.html
```

Open the report in a browser and use Print / Save as PDF.

## Public vs local behavior

| Environment | Data source | Privacy posture |
|---|---|---|
| GitHub Pages | `data/demo-health.json` | public-minimized demo |
| Local runtime | merged `private/health.local.json` | local private runtime |

## Safety rule

Never commit `private/health.local.json`, Apple Health zip files, medical PDFs, screenshots, route files, CSV exports, or generated private reports.
