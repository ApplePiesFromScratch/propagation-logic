import pytest, subprocess, sys

def test_pl_unified_runs():
    """pl_unified.py must run cleanly with no assertion errors."""
    result = subprocess.run(
        [sys.executable, "core/pl_unified.py"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"pl_unified.py failed:\n{result.stderr}"

def test_appendix_runs():
    """appendix.py must run cleanly."""
    result = subprocess.run(
        [sys.executable, "core/appendix.py"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"appendix.py failed:\n{result.stderr}"
