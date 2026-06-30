# Desktop Workflow v2.5

v2.5 compresses the local private workflow into one command.

## One command

Put your Apple Health export zip here:

```txt
apple-health-export/export.zip
```

Then run:

```bash
python3 scripts/yuanli_health_desktop.py
```

Or:

```bash
bash run.sh
```

The workflow will:

1. Find the newest Apple Health export under `apple-health-export/`.
2. Generate `private/health.local.json`.
3. Generate `private/reports/quarterly-report.html`.
4. Start the local cockpit at `http://127.0.0.1:8787/app.html`.

## Custom export path

```bash
python3 scripts/yuanli_health_desktop.py --export ~/Downloads/export.zip
```

## Useful options

```bash
# Use existing private/health.local.json and skip import
python3 scripts/yuanli_health_desktop.py --skip-import

# Skip quarterly report generation
python3 scripts/yuanli_health_desktop.py --skip-report

# Start server without opening browser
python3 scripts/yuanli_health_desktop.py --no-open

# Use a different port
python3 scripts/yuanli_health_desktop.py --port 8790
```

## Safety

All private outputs stay under ignored local folders:

```txt
private/
apple-health-export/
raw-data/
exports/
```

Do not commit raw Apple Health exports, medical PDFs, screenshots, CSVs, route files, or generated private reports.
