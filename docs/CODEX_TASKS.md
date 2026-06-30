# Codex Tasks

## T1 Public/private separation

Keep public demo data separate from private raw exports and reports.

## T2 Apple data importer

Create a script that reads a local export zip, normalizes movement and recovery fields, and writes an aggregated JSON summary. Exclude GPS route data from public outputs.

## T3 Agent core

Implement scoring functions for movement base, Zone2 adherence, sleep stability, recovery trend, metabolic priority, daily brief, weekly review, and missing-data queue.

## T4 Desktop UI v2

Make `app.html` read `data/demo-health.json` dynamically. Keep the main interface user-facing and hide developer blocks.

## T5 Experiments

Add a 14-day experiment tracker for dinner walk, steps floor, sleep anchor, Zone2 cadence, and alcohol-free cycle.

## T6 Doctor pack

Generate a printable 90-day summary for doctor communication and next-check planning.
