from __future__ import annotations

import argparse
import html
import platform
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    risk: str
    explanation: str
    recommendation: str


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True, stderr=subprocess.DEVNULL, timeout=5).strip()
    except Exception:
        return ""


def audit() -> list[Check]:
    checks: list[Check] = []
    is_windows = platform.system() == "Windows"

    power = _run(["powercfg", "/getactivescheme"]) if is_windows else ""
    checks.append(Check(
        "Power plan",
        "detected" if power else "unknown",
        "low",
        "Balanced or power-saving plans can reduce sustained CPU/GPU performance.",
        "Review Windows Power Mode or use a documented high-performance plan while gaming.",
    ))

    free = shutil.disk_usage(Path.home()).free // (1024 ** 3)
    checks.append(Check(
        "Disk free space",
        f"{free} GiB free on home drive",
        "low",
        "Very low free space can hurt updates, shader caches, captures, and pagefile behavior.",
        "Keep at least 15-20% free space on the game and system drive.",
    ))

    ping = _run(["ping", "-n" if is_windows else "-c", "2", "1.1.1.1"])
    checks.append(Check(
        "Network latency sample",
        "sample collected" if ping else "not available",
        "none",
        "A tiny ping sample is not a benchmark, but can reveal obvious connectivity issues.",
        "Run repeated tests to your game region before changing DNS or adapter settings.",
    ))

    checks.append(Check(
        "Startup apps and overlays",
        "manual review needed",
        "medium",
        "Launchers, capture tools, RGB suites, and overlays can add CPU/GPU overhead.",
        "Disable only apps you recognize and export a rollback note before changing startup entries.",
    ))

    return checks


def render_report(checks: list[Check]) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(c.name)}</td>"
        f"<td>{html.escape(c.status)}</td>"
        f"<td>{html.escape(c.risk)}</td>"
        f"<td>{html.escape(c.explanation)}</td>"
        f"<td>{html.escape(c.recommendation)}</td>"
        "</tr>"
        for c in checks
    )
    return f"""<!doctype html>
<html lang=\"en\"><meta charset=\"utf-8\"><title>GameMode Doctor Report</title>
<style>body{{font-family:system-ui;margin:2rem}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:.6rem}}th{{background:#f5f5f5;text-align:left}}</style>
<h1>GameMode Doctor Report</h1>
<p>Dry-run audit only. No changes were applied.</p>
<table><thead><tr><th>Check</th><th>Status</th><th>Risk</th><th>Why it matters</th><th>Recommendation</th></tr></thead><tbody>
{rows}
</tbody></table>
<p><strong>Badge:</strong> GameMode Doctor audited this PC safely.</p>
</html>"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Safe dry-run Windows gaming performance audit")
    parser.add_argument("--report", default="gamemode-report.html", help="HTML report path")
    args = parser.parse_args(argv)

    checks = audit()
    Path(args.report).write_text(render_report(checks), encoding="utf-8")
    print(f"Wrote dry-run report: {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
