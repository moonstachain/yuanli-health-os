# Yuanli Health OS 2.0 Framework

## Product definition

Yuanli Health OS 2.0 is a desktop-first personal health Agent system. It turns continuous signals and periodic medical checks into daily decisions, weekly reviews, 14-day experiments and quarterly doctor-communication packs.

## 1. Input layer

### A. Medical baseline

Periodic, high-authority data:

- Physical exam report.
- Liver function report.
- Blood lipids.
- Fasting glucose / HbA1c / insulin if available.
- Uric acid and kidney function.
- Thyroid ultrasound.
- Liver ultrasound or FibroScan.

### B. Apple Health continuous layer

Daily or near-daily signals:

- Steps.
- Walking/running distance.
- Active energy.
- Exercise minutes.
- Stand hours.
- Resting heart rate.
- HRV.
- Walking heart rate.
- VO2 Max.
- SpO2.
- Respiratory rate.
- Sleep duration and sleep stages.

### C. Manual context layer

Low-friction manual records:

- Weight.
- Waist circumference.
- Dinner time.
- Alcohol.
- Protein target achieved or not.
- Energy score 1-5.
- Stress score 1-5.
- Travel / late night / high-pressure event.

## 2. Analysis layer

### Engine 1: Data quality gate

Before any Agent recommendation, check if the data is usable.

- Movement: good when steps/distance have 80 percent or more daily coverage.
- Recovery: usable when resting HR and HRV have 60 percent or more coverage.
- Sleep: usable only when there are at least 5 tracked nights/week.
- Body composition: usable when weight has daily coverage and waist has weekly coverage.

### Engine 2: Movement base score

Core question: does the body have enough daily energy throughput?

Inputs:

- Steps.
- Distance.
- Active energy.
- Stand hours.

Current v2 baseline: average steps are 4,620/day, so movement base is the first bottleneck.

### Engine 3: Zone2 adherence score

Core question: is there a stable aerobic engine?

Inputs:

- Weekly Zone2 minutes.
- Session count.
- Average HR during workouts.
- RPE feedback.

Target:

- Phase 1: 120 min/week.
- Phase 2: 150 min/week.
- Phase 3: 180 min/week.

### Engine 4: Sleep stability score

Core question: can the body recover and regulate appetite, glucose and training stress?

Inputs:

- Sleep duration.
- Bed/wake time stability.
- Resting HR.
- HRV.
- Respiratory rate.
- Wake energy score.

Current v2 baseline: sleep data is insufficient; the first job is capture, not interpretation.

### Engine 5: Metabolic risk engine

Core question: are liver, glucose, lipid, uric acid and waist signals moving together in the right direction?

Inputs:

- Waist.
- Weight.
- TG.
- Fasting glucose / HbA1c.
- Uric acid.
- ALT / AST / GGT.
- Liver imaging.

### Engine 6: Liver repair engine

Core question: is the liver pressure improving?

Inputs:

- ALT.
- AST.
- GGT.
- Platelets.
- Albumin.
- Bilirubin.
- FIB-4.
- Liver ultrasound / FibroScan.

## 3. Output layer

### Daily output

- Today state: green / yellow / red.
- Today's 3 actions.
- Training decision: push / maintain / recover.
- Sleep action.
- Food rule of the day.

### Weekly output

- Step trend.
- Zone2 completion.
- Sleep tracking completeness.
- Resting HR / HRV trend.
- Weight and waist if available.
- Next week's single bottleneck.

### 14-day experiment output

Each experiment needs one variable, one hypothesis and one success metric.

Examples:

- Dinner walk 20 minutes.
- Bed before 23:30.
- 120g protein day.
- 6500+ steps floor.
- No alcohol for 14 days.

### Quarterly output

- Doctor communication pack.
- Lab recheck checklist.
- Metabolic progress summary.
- Experiments kept / killed / revised.

## 4. Health OS 2.0 implementation plan

### v2.0 now

- Aggregated Apple Health file in `data/demo-health.json`.
- Apple Health analysis doc.
- Framework doc.

### v2.1 next

- Add local-only raw import path.
- Build private `data/health.local.json`.
- Add `src/health-agent-core.js`.

### v2.2

- Make app.html read `data/demo-health.json`.
- Render movement, Zone2 and sleep data dynamically.

### v2.3

- Add weekly review page.
- Add experiment tracker.
- Add doctor pack generator.
