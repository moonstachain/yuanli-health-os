# Mobile iOS Design

## Position

The mobile version is not a smaller desktop cockpit. It is a thumb-first health coach.

Desktop answers:

- What is the full strategic state?
- What is the evidence?
- What should be reviewed weekly or quarterly?

Mobile answers:

- What is my state today?
- What should I do now?
- What can I record in one tap?
- What trend should I notice?
- What should I copy or open later?

## Core principle

Mobile information density comes from compressed judgment, not small text.

## Structure

The mobile app uses five bottom tabs:

1. Today
2. Action
3. Trend
4. Experiment
5. Records

## Today

The first screen shows:

- Today state.
- Main bottleneck.
- Three actions.
- Weekly rhythm.

## Action

Action page includes:

- Zone2 coach.
- Sleep landing checklist.
- Dinner walk card.

## Trend

Trend page uses small cards instead of dashboard charts:

- Steps.
- Exercise minutes.
- Resting heart rate.
- HRV.

Each trend must include a sentence explaining what to do.

## Experiment

Experiment page is a 14-day challenge:

- D1-D14 calendar.
- Active hypotheses.
- Completion stored in browser localStorage.

## Records

Records page includes:

- Doctor communication copy.
- Desktop cockpit entry.
- Data source.
- Privacy boundary.

## iOS adaptation

Use:

- `viewport-fit=cover`.
- `env(safe-area-inset-top)`.
- `env(safe-area-inset-bottom)`.
- Bottom tab bar.
- Large tap targets.
- Sticky top status.

## Visual style

Use dark iOS cards, large rounded corners, calm glass, and reduced decoration. Avoid desktop-style dense KPI grids on small screens.

## Privacy

Public GitHub Pages reads public-minimized data. Local runtime can serve private merged data from `private/health.local.json` without exposing private folders.
