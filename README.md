# TODO: Replicating Author (Year), "Title of the paper"

> **Template note, delete before you submit.** This is the ECON 5200 replication template.
> Replace every line that starts with `TODO:`. The grader clones this repository into an
> empty directory, builds the environment from `requirements.txt` and runs the one command
> below. The number this README claims must be the number that run produces.

## The paper and its headline claim

- **Paper:** TODO: full citation (authors, year, title, journal, volume, pages).
- **Identification strategy:** TODO: difference-in-differences / instrumental variables / regression discontinuity / matching.
- **Headline claim:** TODO: one sentence, with the number and where it is in the paper (for example, Table 2, column 3).
- **My replication:** TODO: my number beside theirs, and the gap in percent, as `python reproduce.py` prints it.

## Reproduce the headline table

Python 3.11 or newer. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python reproduce.py
```

`python reproduce.py` is the one command. Once `MY_PAPER` is set in `download_data.py`,
it downloads the data if `data/` does not have it, runs `notebooks/01_positioning_and_replication.ipynb` and then
`notebooks/02_robustness.ipynb` top to bottom in a fresh kernel, and prints the headline
table from `output/headline_table.csv`. Executed copies of the notebooks, with their
outputs, go to `output/executed/`.

- **Expected runtime:** TODO: minutes on your machine, measured from a clean clone (the empty template runs in under a minute).

## Data: source and licence

- **Source:** TODO: the URL in `download_data.py` for your paper, and who produced the original data.
- **Included or downloaded:** TODO: say which, and why.

The template downloads by default: `.gitignore` excludes `data/*.dta`, and
`download_data.py` fetches the files on the first run. Two facts to check before you
decide:

- The five files from `scunning1975/mixtape` (castle, card, lee, hansen, abortion) are in a
  repository under an MIT-style licence that permits copies if its notice is kept. The
  underlying data were collected by the original authors.
- The Dehejia-Wahba files on `users.nber.org/~rdehejia` state no licence. Download them;
  do not commit them.

If you decide to include the data, delete the `data/*.dta` line from `.gitignore`, commit
the files with the licence notice, and say so above.

## Repository map

| Path | What it is |
|---|---|
| `reproduce.py` | The one command: runs the notebooks in name order, prints the headline table |
| `download_data.py` | Data URLs for the six papers; `python download_data.py --paper card` fetches one into `data/` |
| `notebooks/01_positioning_and_replication.ipynb` | Sections 1 and 2: positioning notes, the replication, the theirs-vs-mine table, the discrepancy log. **No AI.** |
| `notebooks/02_robustness.ipynb` | Section 3: four robustness exercises. AI allowed, logged in `ai-appendix.md` |
| `output/headline_table.csv` | The theirs-vs-mine table, written by notebook 01 |
| `output/` | Every table and figure the report uses |
| `report/` | The report PDF |
| `ai-appendix.md` | P.R.I.M.E. entries and full transcripts for Sections 3 to 6, and the no-AI statement for Sections 1 and 2 |
| `AUDIT.md` | How to run the peer audit you file on a classmate's repository |
| `requirements.txt` | Pinned package versions |

TODO: add a row for every file you add.

## Use of AI

Sections 1 and 2 were completed without AI.

TODO: list the sections where you used AI (from 3, 4, 5 and 6), for what, and point to the
entries in [`ai-appendix.md`](ai-appendix.md). If you used none, say so.
