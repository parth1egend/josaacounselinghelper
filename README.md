# JoSAA Counselling Helper — IIT Cutoff Explorer

An interactive, mobile-friendly explorer for **JoSAA 2025 Round 6 IIT closing ranks**
(All-India quota, OPEN seat type). Sort every IIT program by closing rank, filter by
college / course / degree, and instantly see which programs are attainable for your
JEE Advanced rank.

**Live site:** https://parth1egend.github.io/josaacounselinghelper/

> Built for an OPEN-category candidate. Both Gender-Neutral and Female-only seat pools
> are included; pick the pool in the dropdown.

## Features

- **Ordered by closing rank** — read from the rank-1 seat downward to see how seats fill.
- **Rank-aware highlighting** — enter your rank to colour each program
  ✅ attainable (closing rank ≥ your rank) · ⚠️ borderline (within 150) · ❌ out of reach.
- **Fuzzy course search** — type `artificial` to see *every* AI-related program; variants
  (4-yr / 5-yr / dual / specialisations / abbreviations) group together automatically.
- **Multi-select course groups** — 25 category chips; pick several (combined as OR).
  Group coverage is verified to include **all 131 programs**.
- **Multi-select college filter** — 23 IIT chips; pick any number (combined as
  OR). None selected = all IITs.
- **Degree / duration filter** — 4-Year, 5-Year, Dual degree (any), Single only.
- **Average package column** — branch-wise average CTC (LPA) from official IIT
  placement reports for 10 IITs, where published. Hover a figure for median /
  highest / placement % and the source; `—` means no data. IITs that publish
  only a placement rate (e.g. Delhi) show a blue "X% placed". Sortable like
  every column.
- **Sortable columns** and live counts. Works offline — the page embeds its own data.

## Data

- Source: JoSAA 2025 Round 6, IITs, AI quota, OPEN seat type (`IIT_ALL.txt`).
- Canonical database: **`josaa_iit_2025_r6.csv`** — 600 rows, 131 programs, 23 IITs.
- The CSV is verified consistent with the raw source (15 automated checks) and
  spot-checked against official JoSAA Round 6 figures on key anchors
  (e.g. IIT Bombay CSE 66, IIT Delhi CSE 126, IIT Madras CSE 171).

### Placement data

- **`placement_2025.csv`** — branch-wise average package (LPA), keyed by
  `(institute_short, program_core)` so it joins onto the cutoff rows in
  `build_site.py`. Optional `median_lpa`, `highest_lpa`, `placement_pct` columns
  feed the hover tooltip; blanks are allowed.
- Hand-transcribed from the official placement-report screenshots in `data/`,
  currently covering **10 IITs / 118 programs**: BHU Varanasi, Delhi,
  Gandhinagar, Guwahati, Indore, Jodhpur, Kanpur, Kharagpur, Roorkee, Ropar.
  Every key is checked to match a real `(institute, program_core)` in the
  cutoff CSV.
- IIT Delhi's report publishes only a **placement rate** (no package figures),
  so its rows carry `placement_pct` with a blank `avg_lpa`; the site renders
  these as a blue "X% placed" instead of a green package figure.
- Years differ by IIT (2024-25 or 2025; Kharagpur is partial to mid-Dec 2025)
  and figures are indicative only. To extend coverage, add rows to
  `placement_2025.csv` and re-run `./build.sh`.

## Build pipeline

`IIT_ALL.txt` → `josaa_iit_2025_r6.csv` → `index.html`

```bash
./build.sh
```

This runs four stages and **stops if any fails**:

| Stage | Script | Purpose |
|------|--------|---------|
| 1 | `make_db.py` | raw text → clean CSV database |
| 2 | `verify_db.py` | verify CSV matches the source (15 checks) |
| 3 | `check_groups.py` | verify course groups cover every program |
| 4 | `build_site.py` | generate `index.html` from the verified CSV |

Course-group definitions live in `groups.py` (shared by the checker and the builder so
they can't drift). Requires Python 3 only — no third-party packages.

## Updating the cutoffs

1. Replace `IIT_ALL.txt` with new data (same tab-separated columns).
2. Run `./build.sh`.
3. Commit and push — GitHub Pages redeploys automatically.

## Repository layout

| File | Description |
|------|-------------|
| `index.html` | the website (self-contained, deploy this) |
| `josaa_iit_2025_r6.csv` | canonical cutoff database (source of truth) |
| `placement_2025.csv` | branch-wise placement stats, joined in at build time |
| `data/` | official placement-report screenshots `placement_2025.csv` is transcribed from |
| `IIT_ALL.txt` | raw JoSAA export (all IIT programs) |
| `make_db.py` `verify_db.py` `check_groups.py` `build_site.py` `groups.py` | build pipeline |
| `build.sh` | runs the full pipeline |
| `JoSAA_Preference_List.md` | static markdown preference table |
| `IIT_ORDERED_by_ClosingRank.txt` | plain-text ordered list |
| `IIT_AI.txt` `IIT_CSE.txt` `IIT_MNC.txt` | curated "good branch" subsets |

## Disclaimer

Cutoffs are historical (2025 Round 6) and indicative only; actual cutoffs vary year to
year. Always confirm against the official JoSAA portal before making counselling choices.
