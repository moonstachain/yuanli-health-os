# Release v2.2

## High-Density Cockpit

v2.2 upgrades the desktop Agent from a module-based page into a high-information-density cockpit inspired by the Zhiku-MAX cockpit contract.

## Implemented

### L0 Hero judgment

First screen now shows:

- Current state.
- Main bottleneck.
- Today's three actions.
- Evidence cells.
- Judgment boundary.

### L1 Strategic control

The app now surfaces the 90-day health strategy:

- Movement base: 6,500 to 8,000 steps.
- Zone2: 120 to 150 minutes.
- Sleep capture: 5 nights/week.
- Metabolic recheck cycle.

### L2 Task ledger

Weekly actions now appear as an operational ledger with:

- Priority.
- Task.
- Evidence.
- Next action.

### L3 Evidence and risk

Trend charts and missing-data risks are moved into the evidence layer:

- Steps.
- Exercise minutes.
- Resting heart rate.
- HRV.
- Sleep data missing.
- Body composition missing.
- Public data boundary.

### L4 Meta-governance

The app now explicitly shows:

- Data freshness.
- Public-minimized boundary.
- Next automation queue.

## UX principle

The cockpit should answer the user's decision questions in one screen, not ask the user to interpret raw metrics.

## Privacy boundary

The public page still uses aggregated, minimized data. No GPS routes, raw Apple Health exports, minute-level heart rate, medical PDFs, screenshots or personal identity fields are included.

## Next version

v2.3 should add a private/local importer and a quarterly report generator.
