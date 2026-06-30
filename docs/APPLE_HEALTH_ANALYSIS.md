# Apple Health Analysis｜2026-03-31 to 2026-06-29

## Executive summary

This export provides a usable 90-day movement and recovery baseline, but it is not yet a complete health operating system dataset.

Key findings:

- Movement baseline is real but not yet sufficient: average steps are 4,620/day, with only 6 days above 8,000 steps and 21 days below 3,000 steps.
- Movement declined in June: average steps moved from about 5,099/day in April to 3,829/day in June.
- Formal training is thin: only 1 day reached 30+ exercise minutes in the export, and the only structured workout captured was one outdoor walk on 2026-04-05.
- Recovery trend has one positive sign: resting heart rate improved from 74.1 bpm in the first 30 days to 68.9 bpm in the last 30 days, and HRV improved from 30.8 ms to 34.6 ms.
- Sleep tracking is not usable yet: only 3 days contain sleep duration data. Sleep must be upgraded from a belief to a measured system.
- Body composition is missing from Apple Health: no weight or body-fat records are present in the export.

## Data quality

| Domain | Status | Notes |
|---|---|---|
| Steps / distance | Good | 91 days of step records and 91 days of distance records. |
| Active energy | Medium | 72 days available. |
| Resting heart rate | Medium | 65 days available. |
| HRV | Medium | 67 days available. |
| VO2 Max | Weak | Only 5 values. Treat as directional only. |
| Sleep | Weak | Only 3 days of sleep duration; stages are not reliable. |
| Body composition | Missing | No Apple Health weight/body-fat records. |
| GPS route | Excluded | Raw route data should not be synchronized to public repo. |

## Movement baseline

- Average steps: 4,620/day.
- Median steps: 4,458/day.
- First 30-day average: 5,050/day.
- Last 30-day average: 3,890/day.
- Last 7-day average: 2,709/day.
- Days above 8,000 steps: 6 / 91.
- Days above 10,000 steps: 1 / 91.
- Days below 3,000 steps: 21 / 91.

Interpretation: the current baseline is closer to a low-to-moderate activity lifestyle than a metabolic-reversal training system. The first 2.0 action is not to optimize charts; it is to stabilize a higher daily movement floor.

## Zone2 baseline

Captured structured workout:

- Type: outdoor walk.
- Date: 2026-04-05.
- Duration: 1:16:12.
- Distance: 5.89 km.
- Average heart rate: 97.1 bpm.
- Max heart rate: 121 bpm.

Interpretation: this is close to the low-intensity aerobic zone and is a useful template. The problem is not ability; the problem is cadence. The system needs 3 weekly Zone2 anchors.

## Recovery baseline

- Resting heart rate average: 71.3 bpm.
- First 30 days: 74.1 bpm.
- Last 30 days: 68.9 bpm.
- HRV average: 32.8 ms.
- First 30 days: 30.8 ms.
- Last 30 days: 34.6 ms.

Interpretation: recovery signals improved, but without reliable sleep data, the Agent should not overinterpret readiness. Recovery scoring must be gated by data completeness.

## Sleep baseline

Only 3 days had sleep duration data, with an average of 0.88 hours. This almost certainly means sleep is not being captured correctly rather than actual sleep being that low.

Action: before optimizing sleep, fix capture. Wear Apple Watch to bed for at least 5 nights/week and keep Sleep Focus enabled.

## Health OS 2.0 priorities

1. Build the movement floor: 6,500 steps/day for 14 days, then 8,000 steps/day.
2. Add Zone2 protocol: Tue 35-40m, Thu 35-40m, Sat 45-60m.
3. Fix sleep tracking: 23:15-23:45 bed window, 07:00-07:30 wake window, Apple Watch on wrist.
4. Reconnect body composition: weekly waist, daily weight, optional body-fat scale.
5. Recheck metabolic labs in the next cycle: liver function, fasting glucose/HbA1c, lipids, uric acid.
