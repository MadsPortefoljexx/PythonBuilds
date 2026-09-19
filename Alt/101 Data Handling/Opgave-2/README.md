# The Daylight Gap

A Streamlit app for **international students considering Northern Europe**. Pick where you live now and where you might study. The app plots daylight hours for every day of the year in both cities and shades the gap between them.

**Question:** How much daylight do you gain or lose by living in one city instead of another, and how big is the gap at its worst?

- **Live app:** _add URL after deploying_
- **Video:** _add link_
- **Group 8 :** Ariel Hernan Martinelli, Bethina Ericka Villanueva Rafa, Ele Brigante Cepule, Junayed Ahmad Sojib, Mads Røge Christensen

## What the app contains

| Requirement         | In the app                                                                        |
| ------------------- | --------------------------------------------------------------------------------- |
| Free API            | [Sunrise-Sunset API](https://sunrise-sunset.org/api), no key needed               |
| Visualisation       | Line chart of both cities, with the gap shaded                                    |
| Interactive control | Two city dropdowns (10 cities)                                                    |
| Explanation         | "How to read the chart"                                                           |
| Limitation          | "Limitation": clear skies assumed, clouds ignored                                 |
| Error message       | If the API fails, a red message is shown instead of a crash (try `?demo=offline`) |

## How it works

| File | Job |
|---|---|
| `app.py` | The page: dropdowns, headline metric, chart, text |
| `api.py` | The only file that calls the API. One request per city returns the whole year. Results are cached for 24 h, and every failure becomes a readable `DaylightAPIError` |
| `cities.py` | The 10 cities and their coordinates |

Data: **[Sunrise-Sunset.org](https://sunrise-sunset.org/)** (attribution is required and is also in the app footer). We use API v2 (`/v2` with `date_start`/`date_end`), because the older `/json` version reports the midnight sun as 0 hours of daylight.

## Run it

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

## AI tools used

> **Group: edit this so it matches what you actually did.**

- **Claude** (Anthropic): brainstormed the idea and wrote the first project brief.
- **Claude Code** (Claude Opus 5): tested the API, wrote and later simplified the code, and checked the app in a browser.
- **What we did ourselves:** _fill in_

All numbers in the app come straight from the API data.
