#!/usr/bin/env python3
"""Local/private Apple Health importer for Yuanli Health OS v2.3.

This script is designed to run locally. It reads a private Apple Health export
ZIP/XML or a directory containing export.xml and writes:

- private/health.local.json: richer local data for personal use.
- data/demo-health.json: privacy-minimized public aggregate, only when --public-out is given.

It never uploads data. It excludes GPS routes, raw workout route files and
minute-level streams from public output.
"""
from __future__ import annotations

import argparse
import json
import statistics as stats
import tempfile
import zipfile
from collections import defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET

TYPE_MAP = {
    'HKQuantityTypeIdentifierStepCount': 'steps',
    'HKQuantityTypeIdentifierDistanceWalkingRunning': 'distanceKm',
    'HKQuantityTypeIdentifierActiveEnergyBurned': 'activeEnergyKcal',
    'HKQuantityTypeIdentifierAppleExerciseTime': 'exerciseMinutes',
    'HKQuantityTypeIdentifierAppleStandTime': 'standHours',
    'HKQuantityTypeIdentifierRestingHeartRate': 'restingHeartRate',
    'HKQuantityTypeIdentifierHeartRateVariabilitySDNN': 'hrvMs',
    'HKQuantityTypeIdentifierWalkingHeartRateAverage': 'walkingHeartRateAvg',
    'HKQuantityTypeIdentifierVO2Max': 'vo2Max',
    'HKQuantityTypeIdentifierOxygenSaturation': 'spo2',
    'HKQuantityTypeIdentifierRespiratoryRate': 'respiratoryRate',
}

PUBLIC_KEYS = [
    'steps', 'distanceKm', 'activeEnergyKcal', 'exerciseMinutes', 'standHours',
    'restingHeartRate', 'hrvMs', 'walkingHeartRateAvg', 'vo2Max', 'spo2',
    'respiratoryRate', 'sleepDurationHours'
]


def parse_dt(raw: str | None) -> datetime | None:
    if not raw:
        return None
    for fmt in ('%Y-%m-%d %H:%M:%S %z', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            pass
    return None


def day_key(raw: str | None) -> str | None:
    dt = parse_dt(raw)
    return dt.date().isoformat() if dt else None


def safe_float(raw: str | None) -> float | None:
    try:
        return float(raw) if raw not in (None, '') else None
    except ValueError:
        return None


def find_export_xml(path: Path) -> tuple[Path, tempfile.TemporaryDirectory | None]:
    if path.is_dir():
        direct = path / 'export.xml'
        if direct.exists():
            return direct, None
        hits = list(path.rglob('export.xml'))
        if hits:
            return hits[0], None
        raise FileNotFoundError('export.xml not found in directory')
    if path.suffix.lower() == '.zip':
        tmp = tempfile.TemporaryDirectory()
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if n.endswith('export.xml')]
            if not names:
                tmp.cleanup()
                raise FileNotFoundError('export.xml not found in zip')
            zf.extract(names[0], tmp.name)
            return Path(tmp.name) / names[0], tmp
    if path.name == 'export.xml':
        return path, None
    raise ValueError('input must be export.xml, a Health export directory, or a zip')


def add_value(bucket: dict, key: str, value: float) -> None:
    if key not in bucket:
        bucket[key] = []
    bucket[key].append(value)


def parse_health(xml_path: Path) -> dict:
    daily = defaultdict(dict)
    workouts = []
    context = ET.iterparse(xml_path, events=('end',))
    for _, elem in context:
        tag = elem.tag
        if tag == 'Record':
            t = elem.attrib.get('type')
            mapped = TYPE_MAP.get(t)
            if mapped:
                d = day_key(elem.attrib.get('startDate'))
                value = safe_float(elem.attrib.get('value'))
                if d and value is not None:
                    if mapped == 'distanceKm':
                        unit = elem.attrib.get('unit', '').lower()
                        if unit in ('m', 'meter', 'meters'):
                            value = value / 1000
                    if mapped == 'activeEnergyKcal':
                        unit = elem.attrib.get('unit', '').lower()
                        if unit in ('kj', 'kilojoule', 'kilojoules'):
                            value = value / 4.184
                    if mapped == 'standHours':
                        unit = elem.attrib.get('unit', '').lower()
                        if unit in ('min', 'minute', 'minutes'):
                            value = value / 60
                    add_value(daily[d], mapped, value)
        elif tag == 'Workout':
            start = elem.attrib.get('startDate')
            end = elem.attrib.get('endDate')
            sd, ed = parse_dt(start), parse_dt(end)
            if sd and ed:
                workouts.append({
                    'type': elem.attrib.get('workoutActivityType', '').replace('HKWorkoutActivityType', ''),
                    'start': sd.isoformat(),
                    'durationMinutes': round((ed - sd).total_seconds() / 60, 1),
                })
        elem.clear()
    return {'daily_raw': daily, 'workouts': workouts}


def summarize_daily(raw: dict) -> list[dict]:
    rows = []
    for d in sorted(raw):
        item = {'date': d}
        for key, values in raw[d].items():
            if key in ('steps', 'activeEnergyKcal', 'exerciseMinutes', 'standHours', 'distanceKm'):
                item[key] = round(sum(values), 2)
            else:
                item[key] = round(stats.mean(values), 2)
        rows.append(item)
    return rows


def metric_summary(rows: list[dict], key: str) -> dict:
    vals = [num for r in rows if (num := r.get(key)) is not None]
    if not vals:
        return {'days': 0, 'avg': None, 'median': None, 'min': None, 'max': None, 'last7Avg': None}
    last7 = [r.get(key) for r in rows[-7:] if r.get(key) is not None]
    return {
        'days': len(vals),
        'avg': round(stats.mean(vals), 2),
        'median': round(stats.median(vals), 2),
        'min': round(min(vals), 2),
        'max': round(max(vals), 2),
        'last7Avg': round(stats.mean(last7), 2) if last7 else None,
    }


def build_outputs(rows: list[dict], workouts: list[dict], days: int) -> tuple[dict, dict]:
    recent = rows[-days:] if days else rows
    metrics = {key: metric_summary(recent, key) for key in PUBLIC_KEYS}
    public = {
        'meta': {
            'schemaVersion': 'yuanli-health-os.v2.3-local-import',
            'updatedAt': date.today().isoformat(),
            'visibility': 'public-minimized',
            'note': 'Generated locally from Apple Health. Raw exports, routes and personal identifiers are excluded.'
        },
        'appleHealth': {
            'range': {
                'start': recent[0]['date'] if recent else None,
                'end': recent[-1]['date'] if recent else None,
                'days': len(recent),
            },
            'dataQuality': {
                'movement': 'good' if metrics['steps']['days'] >= max(1, len(recent) * 0.8) else 'partial',
                'recovery': 'partial' if metrics['restingHeartRate']['days'] or metrics['hrvMs']['days'] else 'missing',
                'sleep': 'insufficient' if metrics['sleepDurationHours']['days'] < 5 else 'good',
                'bodyComposition': 'missing',
                'location': 'excluded from public output'
            },
            'metrics': metrics,
            'dailySeries': recent[-14:],
            'workouts': workouts[-20:],
        }
    }
    private = {
        'meta': {'schemaVersion': 'yuanli-health-os.v2.3-private', 'updatedAt': date.today().isoformat()},
        'appleHealth': {'dailySeries': rows, 'workouts': workouts, 'metrics': metrics},
    }
    return private, public


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('input', help='Apple Health export.zip, export.xml, or export directory')
    p.add_argument('--private-out', default='private/health.local.json')
    p.add_argument('--public-out', default=None, help='Optional path, e.g. data/demo-health.json')
    p.add_argument('--days', type=int, default=90)
    args = p.parse_args()

    xml_path, tmp = find_export_xml(Path(args.input))
    try:
        parsed = parse_health(xml_path)
        rows = summarize_daily(parsed['daily_raw'])
        private, public = build_outputs(rows, parsed['workouts'], args.days)
        Path(args.private_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.private_out).write_text(json.dumps(private, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'wrote private local data: {args.private_out}')
        if args.public_out:
            Path(args.public_out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.public_out).write_text(json.dumps(public, ensure_ascii=False, indent=2), encoding='utf-8')
            print(f'wrote public-minimized data: {args.public_out}')
    finally:
        if tmp:
            tmp.cleanup()


if __name__ == '__main__':
    main()
