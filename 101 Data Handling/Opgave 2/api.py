"""Everything that talks to the Sunrise-Sunset API (https://sunrise-sunset.org/api).
correctly (midnight sun = 86400 s, polar night = 0 s).
"""

import pandas as pd
import requests
import streamlit as st

from cities import CITIES

API_URL = "https://api.sunrise-sunset.org/v2"


class DaylightAPIError(Exception):
    """The API gave us no usable data. The message is written for the app's users."""


@st.cache_data(ttl=86_400, show_spinner="Fetching a year of sunrise and sunset times…")
def get_year_of_daylight(city: str, year: int, base_url: str = API_URL) -> pd.DataFrame:
    """One API request -> hours of daylight for every day of `year` in `city`.

    Cached for 24 hours, because sunrise and sunset for a given place and date never change.
    Errors are not cached, so a failed request is tried again on the next rerun.
    """
    lat, lng = CITIES[city]
    params = {"lat": lat, "lng": lng, "date_start": f"{year}-01-01", "date_end": f"{year}-12-31"}

    try:
        response = requests.get(base_url, params=params, timeout=15)
    except requests.RequestException as exc:
        raise DaylightAPIError(
            "Couldn't reach the Sunrise-Sunset API. It may be down, or there's no internet connection."
        ) from exc

    try:
        payload = response.json()
    except ValueError:  # not JSON, e.g. an HTML error page
        payload = {}

    if response.status_code != 200:
        message = payload.get("message", "")  # v2 explains bad requests in a "message" field
        raise DaylightAPIError(f"The Sunrise-Sunset API returned an error (HTTP {response.status_code}). {message}".strip())

    days = payload.get("days")
    if not days:
        raise DaylightAPIError("The Sunrise-Sunset API returned no daylight data.")

    df = pd.DataFrame(days)
    df["date"] = pd.to_datetime(df["date"])
    # Seconds -> hours. Near the Arctic Circle the API very rarely sends null (Tromsø, 16 May 2026,
    # when the sunset slips past midnight), so such a day is filled in from its neighbours.
    df["hours"] = pd.to_numeric(df["day_length"], errors="coerce").interpolate(limit_direction="both") / 3600
    return df[["date", "hours"]]
