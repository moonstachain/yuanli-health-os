#!/usr/bin/env python3
"""Build a local quarterly health strategy report for Yuanli Health OS v2.3.

Input is a private/local JSON file, usually `private/health.local.json`.
Output is a printable HTML report under `private/reports/` by default.

The generated report is intended for personal review and doctor communication.
Do not commit generated private reports to the public repo.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding='utf-8'))


def avg(rows: list[dict], key: str):
    vals = [float(r[key]) for r in rows if r.get(key) is not None]
    return sum(vals) / len(vals) if vals else None


def fmt(v, digits=0):
    if v is None:
        return '—'
    return f'{v:,.{digits}f}'


def last(rows: list[dict], n: int) -> list[dict]:
    return rows[-n:] if rows else []


def report(data: dict) -> str:
    rows = data.get('appleHealth', {}).get('dailySeries', [])
    rows90 = last(rows, 90)
    rows7 = last(rows, 7)
    steps90 = avg(rows90, 'steps')
    steps7 = avg(rows7, 'steps')
    exercise7 = sum(float(r.get('exerciseMinutes') or 0) for r in rows7)
    sleep_nights7 = sum(1 for r in rows7 if r.get('sleepDurationHours'))
    rhr90 = avg(rows90, 'restingHeartRate')
    hrv90 = avg(rows90, 'hrvMs')
    today = date.today().isoformat()

    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8" />
<title>原力健康季度战略报告</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;margin:42px;color:#111;line-height:1.65}}
h1{{font-size:30px;margin:0 0 8px}}h2{{font-size:20px;margin-top:28px;border-bottom:1px solid #ddd;padding-bottom:6px}}
.grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:18px 0}}.card{{border:1px solid #ddd;border-radius:12px;padding:14px}}.card small{{display:block;color:#666}}.card b{{font-size:24px}}.warn{{color:#9a6500}}.bad{{color:#b42318}}.good{{color:#067647}}
@media print{{body{{margin:20mm}}}}
</style>
</head>
<body>
<h1>原力健康季度战略报告</h1>
<p>生成日期：{today}。本报告用于个人健康管理和就医沟通，不替代医生诊断。</p>

<h2>1. 本季度一句话判断</h2>
<p><b>当前第一瓶颈仍是运动底盘与睡眠采集。</b> 先稳定步数地板、Zone2 节律和睡眠数据，再评价更复杂的恢复与代谢趋势。</p>

<h2>2. 核心指标</h2>
<div class="grid">
  <div class="card"><small>90天日均步数</small><b>{fmt(steps90)}</b><p>目标：6500 → 8000</p></div>
  <div class="card"><small>近7日步数</small><b>{fmt(steps7)}</b><p class="bad">低于目标则优先补运动底盘</p></div>
  <div class="card"><small>近7日运动分钟</small><b>{fmt(exercise7)}</b><p>目标：120分钟/周</p></div>
  <div class="card"><small>近7日睡眠采集</small><b>{sleep_nights7}/5</b><p class="warn">不足则不做深度恢复判断</p></div>
</div>
<div class="grid">
  <div class="card"><small>90天静息心率</small><b>{fmt(rhr90,1)}</b><p>结合HRV看恢复趋势</p></div>
  <div class="card"><small>90天HRV</small><b>{fmt(hrv90,1)}</b><p>仅作趋势，不做单日结论</p></div>
</div>

<h2>3. 本季度行动策略</h2>
<ol>
<li><b>步数地板：</b>先连续14天达到6500步，再推进到8000步。</li>
<li><b>Zone2：</b>周二/周四/周六三锚点，先达成120分钟/周，两周稳定后升到150分钟。</li>
<li><b>睡眠采集：</b>连续14天戴表睡觉，每周至少5晚有效记录。</li>
<li><b>饮食与代谢：</b>晚饭后20分钟轻走，减少饮酒和高油外食，蛋白质优先。</li>
</ol>

<h2>4. 医生沟通问题</h2>
<ul>
<li>是否需要 FibroScan 或肝脏弹性评估？</li>
<li>糖代谢是否需要 HbA1c、OGTT 或空腹胰岛素进一步确认？</li>
<li>尿酸、血脂和脂肪肝是否仅生活方式干预，还是需要药物评估？</li>
<li>下一次复查间隔建议是多久？</li>
</ul>

<h2>5. 建议复查清单</h2>
<p>肝功能、血脂完整项、HbA1c、空腹胰岛素、尿酸、肌酐/eGFR、UACR、hs-CRP、肝脏弹性评估。</p>
</body>
</html>'''


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--input', default='private/health.local.json')
    p.add_argument('--output', default='private/reports/quarterly-report.html')
    args = p.parse_args()
    data = load(args.input)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report(data), encoding='utf-8')
    print(f'wrote quarterly report: {out}')


if __name__ == '__main__':
    main()
