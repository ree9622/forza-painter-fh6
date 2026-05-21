import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import clamp_parallel_jobs


def test_clamp_parallel_jobs_accepts_valid_values():
    assert clamp_parallel_jobs("1") == 1
    assert clamp_parallel_jobs("3") == 3


def test_clamp_parallel_jobs_limits_invalid_or_extreme_values():
    assert clamp_parallel_jobs("") == 1
    assert clamp_parallel_jobs("abc") == 1
    assert clamp_parallel_jobs("0") == 1
    assert clamp_parallel_jobs("99") == 4
