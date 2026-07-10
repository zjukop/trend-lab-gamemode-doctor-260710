from pathlib import Path

from gamemode_doctor.main import audit, main, render_report


def test_audit_returns_checks():
    checks = audit()
    assert checks
    assert all(c.name and c.recommendation for c in checks)


def test_render_report_contains_safety_text():
    report = render_report(audit())
    assert "Dry-run audit only" in report
    assert "No changes were applied" in report


def test_main_writes_report(tmp_path: Path):
    output = tmp_path / "report.html"
    assert main(["--report", str(output)]) == 0
    assert output.exists()
    assert "GameMode Doctor Report" in output.read_text(encoding="utf-8")
