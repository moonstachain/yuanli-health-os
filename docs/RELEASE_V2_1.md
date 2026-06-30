# Release v2.1

## What changed

v2.1 turns the desktop demo from a static dashboard into a data-driven Agent workspace.

## Implemented

1. `data/demo-health.json` now uses `yuanli-health-os.v2.1` and includes privacy-minimized daily aggregates for recent trends.
2. `src/health-agent-core.js` now renders dynamic UI from the JSON data.
3. The desktop app now injects:
   - 7-day trend charts for steps, exercise minutes, resting heart rate and HRV.
   - Weekly completion panel for steps floor, Zone2, sleep capture and experiment completion.
   - Data quality gate.
   - Sleep capture warning.
   - Zone2 weekly progress.
   - 14-day experiment calendar with local browser state.
   - Doctor communication pack with browser print / Save as PDF.

## Privacy boundary

The public repository only contains aggregated and minimized data. It does not include GPS routes, raw Apple Health exports, minute-level heart rate streams, medical PDFs, screenshots or personal identity fields.

## User experience principle

The page should not ask the user to interpret raw data. It should answer:

- What is my state today?
- What should I do today?
- Did I complete this week's rhythm?
- Which bottleneck should I fix next?
- What should I discuss with my doctor?

## Next version

v2.2 should add:

- A real private/local data import script.
- Local-only full daily history.
- More stable experiment state export/import.
- Optional printable quarterly report.
