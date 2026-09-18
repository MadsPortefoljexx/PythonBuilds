# 3 — Story and video

## Audience and story

- **Who:** international students deciding whether to study in Northern Europe.
- **Why it matters:** people pick a city on rent and reputation, not daylight. Then they arrive in Aalborg in November, when the sun sets before 16:00. We live here, so we can speak to it.
- **Question:** how much daylight do you gain or lose, and how big is the gap at its worst?
- **Headline:** on 21 December Aalborg gets **2 h 29 min less daylight** than Barcelona.
- **Twist:** over a whole year the totals are almost equal. Moving north moves daylight into summer, so the winter gap is what counts.
- **Honesty:** clear skies are assumed, so the real gap is bigger.

## Video (~4 min, everyone speaks)

Record from the **live URL**. Open the app once first so it's awake.

| Part | Speaker | Say / show | Time |
|---|---|---|---|
| A | _name_ | The audience and the question. "Everyone checks the rent; nobody checks the daylight." Aalborg in November. | 0:00–0:50 |
| B | _name_ | Data: a free API with no key. We read the docs and found v2, where **one request gives a whole year**, so a comparison is 2 requests with daily data. The old version said Tromsø's midnight sun had 0 hours of daylight. We checked the API against astronomy: 2.6 min average error. | 0:50–1:50 |
| C | _name_ | Demo: Barcelona → Aalborg gives **−2 h 29 min**. Explain the lines, the shaded gap and the dotted darkest day; hover a day. Switch home to **Nairobi** (−5 h 30 min), then destination to **Tromsø** (polar night). The twist: the yearly totals are almost equal. | 1:50–3:10 |
| D | _name_ | Open `?demo=offline`: a clear error, not a crash. Limitation: clear skies. The AI use (as in the README). Wrap up: "Check the daylight before you pick a city." | 3:10–4:10 |

If you run long, skip the Tromsø switch. If you run short, add Melbourne → Aalborg: **−8 h 05 min**, because the seasons are flipped.
