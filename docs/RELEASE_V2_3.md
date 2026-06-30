# Release v2.3

## Private/local importer + quarterly report generator

v2.3 adds the private data layer needed to move from a public demo toward a real personal health operating system.

## Implemented

### 1. Local Apple Health importer

New file:

```txt
scripts/import_apple_health.py
```

Capabilities:

- Reads an Apple Health `export.xml`, export directory, or zip.
- Produces `private/health.local.json` for local/private use.
- Optionally produces `data/demo-health.json` as a public-minimized aggregate.
- Excludes GPS routes, raw route files, minute-level streams and personal identity fields from public output.

### 2. Quarterly report generator

New file:

```txt
scripts/build_quarterly_report.py
```

Capabilities:

- Reads `private/health.local.json`.
- Builds a printable quarterly strategy report.
- Outputs `private/reports/quarterly-report.html`.
- The report can be printed or saved as PDF from the browser.

### 3. Private data guide

New file:

```txt
docs/LOCAL_PRIVATE_DATA.md
```

It explains the public/private split, local folder policy, import commands and report generation commands.

## Privacy boundary

The public repository remains a demo and UI shell. Raw health exports, local reports and medical source files stay under ignored local directories such as `private/`, `raw-data/`, `apple-health-export/` and `exports/`.

## Suggested workflow

```bash
python3 scripts/import_apple_health.py apple-health-export/export.zip \
  --private-out private/health.local.json

python3 scripts/build_quarterly_report.py \
  --input private/health.local.json \
  --output private/reports/quarterly-report.html
```

Open the report in a browser and use Print / Save as PDF.

## Next version

v2.4 should connect the private local data layer to the desktop cockpit through a local-only runtime or a private backend, while keeping the public GitHub Pages demo safe.
