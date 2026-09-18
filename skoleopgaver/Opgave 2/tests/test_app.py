"""Tests with a fake API, so they run offline. Run with:  python -m pytest"""

import sys
from pathlib import Path

import pandas as pd
import pytest
import requests
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import api  # noqa: E402
from cities import CITIES  # noqa: E402


class FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.payload = payload

    def json(self):
        if self.payload is None:
            raise ValueError("not JSON")
        return self.payload


def fake_year(url, params, timeout):
    """Barcelona gets 10 h every day; every other city 8 h, except 7.5 h on 21 December."""
    year = params["date_start"][:4]
    days = []
    for d in pd.date_range(f"{year}-01-01", f"{year}-12-31"):
        hours = 10 if params["lat"] == CITIES["Barcelona, Spain"][0] else 7.5 if (d.month, d.day) == (12, 21) else 8
        days.append({"date": f"{d:%Y-%m-%d}", "day_length": hours * 3600})
    return FakeResponse(200, {"days": days})


@pytest.fixture(autouse=True)
def fresh_cache():
    api.get_year_of_daylight.clear()  # otherwise one test's fake data leaks into the next


def use_fake_api(monkeypatch, handler):
    monkeypatch.setattr(api.requests, "get", handler)


def raise_(exception):
    def handler(*args, **kwargs):
        raise exception

    return handler


# --- api.py ---------------------------------------------------------------------------------


def test_one_request_returns_a_year_of_hours(monkeypatch):
    use_fake_api(monkeypatch, fake_year)
    df = api.get_year_of_daylight("Aalborg, Denmark", 2026)

    assert list(df.columns) == ["date", "hours"]
    assert len(df) == 365
    assert df.loc[df["hours"].idxmin(), "date"] == pd.Timestamp("2026-12-21")


def test_missing_day_is_filled_from_neighbours(monkeypatch):
    def handler(url, params, timeout):
        response = fake_year(url, params, timeout)
        response.payload["days"][135]["day_length"] = None  # 16 May, like Tromsø in the real API
        return response

    use_fake_api(monkeypatch, handler)
    df = api.get_year_of_daylight("Tromsø, Norway", 2026)
    assert df.loc[135, "hours"] == 8


@pytest.mark.parametrize(
    ("handler", "message"),
    [
        (raise_(requests.ConnectionError()), "Couldn't reach"),
        (raise_(requests.Timeout()), "Couldn't reach"),
        (lambda *a, **k: FakeResponse(400, {"message": "Invalid date."}), r"HTTP 400\). Invalid date\."),
        (lambda *a, **k: FakeResponse(500), r"HTTP 500\)\.$"),
        (lambda *a, **k: FakeResponse(200, {"days": []}), "no daylight data"),
        (lambda *a, **k: FakeResponse(200), "no daylight data"),
    ],
)
def test_every_failure_becomes_a_readable_error(monkeypatch, handler, message):
    use_fake_api(monkeypatch, handler)
    with pytest.raises(api.DaylightAPIError, match=message):
        api.get_year_of_daylight("Aalborg, Denmark", 2026)


# --- app.py ---------------------------------------------------------------------------------


def run_app():
    return AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()


def test_app_shows_the_gap_chart_and_text(monkeypatch):
    use_fake_api(monkeypatch, fake_year)
    at = run_app()

    assert not at.exception
    assert at.metric[0].value == "−2 h 30 min"  # Aalborg 7.5 h vs Barcelona 10 h
    assert "21 December" in at.metric[0].label
    assert len(at.get("plotly_chart")) == 1
    assert [s.value for s in at.subheader] == ["How to read the chart", "Limitation"]
    assert "sunrise-sunset.org" in at.caption[0].value  # attribution


def test_app_shows_an_error_instead_of_crashing(monkeypatch):
    use_fake_api(monkeypatch, raise_(requests.ConnectionError()))
    at = run_app()

    assert not at.exception
    assert "Couldn't load the daylight data" in at.error[0].value
    assert not at.get("plotly_chart")
