# 1 — Plan

**Deadline:** Monday 21 September. Hand in the live URL, the repo URL and a 3–5 min video where everyone speaks.

## Checklist

- [x] App: free API, chart, dropdowns, explanation, limitation, error message
- [x] Attribution link to sunrise-sunset.org (app footer + README)
- [x] No API keys (the API needs none)
- [x] Tests pass (`python -m pytest`, 10 tests)
- [ ] README: group names + AI section made true for the group
- [ ] Pushed to GitHub
- [ ] Deployed on Streamlit Community Cloud, live URL in README
- [ ] Video recorded

## Decisions

1. **API v2, one request per city.** `date_start`/`date_end` returns all 365 days at once, so a comparison costs 2 requests and gives daily data. The brief's plan was 24 requests for monthly data.
2. **10 cities** from Tromsø (69.6°N) to Melbourne (37.8°S), so every choice looks different. Near-duplicates (Copenhagen ≈ Aalborg, Beijing ≈ Barcelona) were removed.
3. **One headline number:** the gap on the destination's darkest day. The yearly total would mislead, because northern cities get slightly *more* daylight over a year.
4. **Errors in one place.** `api.py` turns every failure (no connection, HTTP error, empty data) into a `DaylightAPIError`. `app.py` shows it with `st.error` and stops before drawing anything.
5. **`?demo=offline`** on the URL fakes an outage, so the error message can be shown in the video.

## Deploy (Saturday)

1. Create a **public** GitHub repo and push this folder (`app.py` must be at the top level; `.venv/` is ignored):

```bash
git init -b main
```

```bash
git add .
```

```bash
git commit -m "The Daylight Gap"
```

```bash
git remote add origin https://github.com/<user>/daylight-gap.git
```

```bash
git push -u origin main
```

2. On **share.streamlit.io**, sign in with GitHub. Choose Create app, then this repo, branch `main`, file `app.py`. Under **Advanced settings**, pick **Python 3.12 or 3.13** (pandas 3 needs ≥ 3.11). Then Deploy.
3. Check the live app on a phone, and open `<url>/?demo=offline` to see the error message.
4. Paste the URL into the README and push again.

If the app says it has "gone to sleep", click wake up. Open it yourself before the teachers do.

## Timeline

| Day | Goal |
|---|---|
| Fri 18 | Read the docs, adjust anything, assign video parts, push to GitHub |
| Sat 19 | Deploy and test the live URL |
| Sun 20 | Rehearse and record the video |
| Mon 21 | Hand in |
