import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import clamp_parallel_jobs, load_app_preferences, render_source_image, save_app_preferences


def test_clamp_parallel_jobs_accepts_valid_values():
    assert clamp_parallel_jobs("1") == 1
    assert clamp_parallel_jobs("3") == 3


def test_clamp_parallel_jobs_limits_invalid_or_extreme_values():
    assert clamp_parallel_jobs("") == 1
    assert clamp_parallel_jobs("abc") == 1
    assert clamp_parallel_jobs("0") == 1
    assert clamp_parallel_jobs("99") == 4


def test_app_preferences_round_trip_language(tmp_path):
    path = tmp_path / "preferences.json"

    save_app_preferences({"language": "ko"}, path)

    assert load_app_preferences(path) == {"language": "ko"}


def test_app_preferences_ignore_invalid_json(tmp_path):
    path = tmp_path / "preferences.json"
    path.write_text("{not json", encoding="utf-8")

    assert load_app_preferences(path) == {}


def test_render_source_image_supports_korean_file_names(tmp_path):
    cv2 = pytest.importorskip("cv2")
    np = pytest.importorskip("numpy")
    path = tmp_path / "한글 이미지.png"
    image = np.full((8, 8, 3), 255, np.uint8)
    ok, encoded = cv2.imencode(".png", image)
    assert ok
    path.write_bytes(encoded.tobytes())

    assert render_source_image(path) is not None
