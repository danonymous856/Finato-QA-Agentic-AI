from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from models.schemas import UnitTestResult


def run_pytest(target: str = "tests", junit_xml: Optional[str] = None) -> UnitTestResult:
    """
    Run pytest programmatically and capture a summary.
    """
    cmd = ["pytest", target, "-q"]
    if junit_xml:
        cmd.extend(["--junitxml", junit_xml])

    process = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )

    logs = process.stdout + "\n" + process.stderr
    success = process.returncode == 0

    # For a lightweight implementation, we don't parse full test counts from output.
    # We just mark total=1 and passed/failed based on exit code.
    result = UnitTestResult(
        success=success,
        total=1,
        passed=1 if success else 0,
        failed=0 if success else 1,
        errors=0,
        report_path=str(Path(junit_xml)) if junit_xml else None,
        logs=logs,
    )
    return result

