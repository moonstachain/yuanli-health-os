# Codex 任务包｜原力健康 OS

请基于本仓库，把原力健康 OS 升级为可持续数据驱动版本。

## 任务 1：数据层

创建：

```txt
data/health.example.json
schemas/health.v1.schema.json
src/health-agent-core.js
scripts/import_apple_health.py
scripts/import_reports.py
scripts/normalize_health_data.py
```

真实数据不要提交 public repo。使用 `.gitignore` 忽略：

```txt
data/health.json
raw/
private/
*.xml
*.pdf
*.xlsx
```

## 任务 2：Apple Health 导入

解析 Apple Health 导出的 `export.xml`，提取过去 90 天：

- steps
- activeEnergy
- sleep
- restingHeartRate
- heartRateVariabilitySDNN
- respiratoryRate
- oxygenSaturation
- wristTemperature
- vo2max
- workouts

输出为标准 `data/health.json`。

## 任务 3：报告解析

解析体检 PDF / 肝功能报告 / 体脂秤截图，映射到：

- observations
- labs
- bodyComposition
- imaging

## 任务 4：Agent Core

实现：

- todayBrief(data)
- zone2Prescription(data)
- sleepStabilityPlan(data)
- metabolicRepairScore(data)
- liverRepairScore(data)
- missingDataQueue(data)
- doctorPack(data)

## 任务 5：前端接入

把 `app.html` 改为优先 fetch `data/health.json`，失败时 fallback 到 demo data。
