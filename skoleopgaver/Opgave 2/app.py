"""The Daylight Gap: compare daylight across a year in two cities.

Run locally with:  streamlit run app.py
"""

from datetime import date

import plotly.graph_objects as go
import streamlit as st

from api import API_URL, DaylightAPIError, get_year_of_daylight
from cities import CITIES

YEAR = date.today().year


def duration(hours: float) -> str:
    """2.48 -> '2 h 29 min'"""
    h, m = divmod(round(abs(hours) * 60), 60)
    return f"{h} h {m:02d} min"


st.set_page_config(page_title="The Daylight Gap", page_icon="☀️")
st.title("The daylight gap")
st.markdown(
    "**For international students thinking about studying in Northern Europe.** "
    "People compare cities on rent and reputation, but almost nobody checks the daylight. "
    "Pick two cities to see how much daylight you would gain or lose, and how big the gap gets at its worst."
)

names = list(CITIES)
left, right = st.columns(2)
home = left.selectbox("Where you live now", names, index=names.index("Barcelona, Spain"))
destination = right.selectbox("Where you might study", names, index=names.index("Aalborg, Denmark"))
home_name, dest_name = home.split(",")[0], destination.split(",")[0]

# Add ?demo=offline to the URL to show the error message on purpose (e.g. in the video).
base_url = "https://offline.invalid" if st.query_params.get("demo") == "offline" else API_URL

try:
    home_df = get_year_of_daylight(home, YEAR, base_url)
    dest_df = get_year_of_daylight(destination, YEAR, base_url)
except DaylightAPIError as error:
    st.error(f"Couldn't load the daylight data. {error}")
    st.stop()

# Headline: the gap on the destination's darkest day (both tables cover the same dates)
darkest = dest_df["hours"].idxmin()
day = dest_df.loc[darkest, "date"]
dest_hours, home_hours = dest_df.loc[darkest, "hours"], home_df.loc[darkest, "hours"]
gap = dest_hours - home_hours

st.metric(
    f"Daylight gap on {dest_name}'s darkest day, {day.day} {day:%B}",
    f"{'−' if gap < 0 else '+'}{duration(gap)}",
    f"{dest_name}: {duration(dest_hours)} · {home_name}: {duration(home_hours)}",
    delta_color="off",
    delta_arrow="off",
    border=True,
)

fig = go.Figure()
fig.add_scatter(x=home_df["date"], y=home_df["hours"], name=home_name, line_color="#2a78d6")
fig.add_scatter(
    x=dest_df["date"], y=dest_df["hours"], name=dest_name, line_color="#eb6834",
    fill="tonexty", fillcolor="rgba(137,135,129,0.2)",  # shade the gap between the lines
)
fig.add_vline(x=day, line_dash="dot", line_color="gray")
fig.update_traces(hovertemplate="%{y:.1f} h")
fig.update_layout(
    title=f"Hours of daylight per day, {YEAR}",
    hovermode="x unified",
    xaxis={"dtick": "M1", "tickformat": "%b"},
    yaxis={"range": [0, 24], "dtick": 4, "ticksuffix": " h"},
    legend={"orientation": "h", "y": 1.12, "traceorder": "normal"},
)
st.plotly_chart(fig)

st.subheader("How to read the chart")
st.markdown(
    f"Each line shows the hours between sunrise and sunset on every day of {YEAR}. The further a city "
    "is from the equator, the steeper its curve. The lines cross around the equinoxes (about 20 March and "
    "23 September), when everywhere gets roughly 12 hours. The **shaded area is the gap**, and its widest "
    "point in winter (dotted line) is what matters most if you're deciding where to live. "
    "Over a whole year the totals are almost equal: moving north moves daylight from winter into summer."
)

st.subheader("Limitation")
st.markdown(
    "This is **astronomical** daylight: sunrise to sunset under a perfectly clear sky. The API knows "
    "nothing about clouds, and Northern European winters are often heavily overcast. So the daylight you "
    "actually *feel* in winter is lower, and the real gap is **bigger** than the chart shows."
)

st.caption("Data: [Sunrise-Sunset.org](https://sunrise-sunset.org/) API, one request per city, cached for 24 hours.")
