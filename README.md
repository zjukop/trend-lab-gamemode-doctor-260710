# GameMode Doctor

A minimal, safe Windows gaming optimizer prototype. It audits common gaming performance settings, explains suggestions, and writes a local report. Dry-run is the default; no system changes are made.

## Requirements

- Python 3.11+
- Windows recommended (runs with limited checks elsewhere)

## Install

```bash
pip install -e .
```

## Run

```bash
gamemode-doctor --report report.html
# or
python -m gamemode_doctor.main --report report.html
```

## Test

```bash
pytest
```

## Safety scope

This starter does **not** edit the registry, touch game memory, bypass anti-cheat, or run hidden booster scripts. It only audits and reports placeholder recommendations.