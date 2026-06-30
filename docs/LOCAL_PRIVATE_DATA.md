# Local / Private Data Layer

Yuanli Health OS uses a public/private split.

## Public repo

The public repo may contain:

- UI code.
- Documentation.
- Privacy-minimized demo data.
- Scripts that run locally.

The public repo must not contain:

- Raw Apple Health exports.
- GPS route files.
- Minute-level heart-rate streams.
- Medical PDFs or screenshots.
- Personal identity fields.
- Private local reports.

## Local private folders

Use these folders locally only. They are ignored by git.

```txt
private/
raw-data/
apple-health-export/
exports/
```

## Import Apple Health locally

After exporting Apple Health from iPhone / Apple Health, put the zip under `apple-health-export/` locally.

Then run:

```bash
python3 scripts/import_apple_health.py apple-health-export/export.zip \
  --private-out private/health.local.json \
  --public-out data/demo-health.json
```

For a fully private run, omit `--public-out`:

```bash
python3 scripts/import_apple_health.py apple-health-export/export.zip \
  --private-out private/health.local.json
```

## Generate quarterly report

```bash
python3 scripts/build_quarterly_report.py \
  --input private/health.local.json \
  --output private/reports/quarterly-report.html
```

Open the HTML file in a browser and use Print / Save as PDF.

## Principle

Public pages show a minimal, safe demo. Private local files are the source of truth for personal decisions.
