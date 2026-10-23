#!/usr/bin/env python3
"""Download the data for one of the six ECON 5200 replication papers into data/.

    python download_data.py --paper card
    python download_data.py                  # uses MY_PAPER below
    python download_data.py --list           # show the six papers and their files

A file already in data/ is not downloaded again; pass --force to replace it.
The notebooks call fetch() from this file, so `python reproduce.py` downloads
the data itself on a clean checkout.

Every file is a Stata .dta. Read one with pandas:

    import pandas as pd
    df = pd.read_stata("data/card.dta")

If pandas raises an error about value labels, pass convert_categoricals=False and
map the codes yourself. Dehejia-Wahba is two files: the NSW experimental sample
(nsw_dw.dta) and the CPS comparison group (cps_controls.dta). You build the
observational sample by stacking the NSW treated units on the CPS controls.
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

# TODO: set this to your paper's key (castle, card, lee, dw, hansen or abortion).
# The notebooks read it, so you set it once.
MY_PAPER = ""

MIXTAPE = "https://raw.githubusercontent.com/scunning1975/mixtape/master"
DEHEJIA = "https://users.nber.org/~rdehejia/data"

PAPERS = {
    "castle": {
        "paper": "Cheng & Hoekstra (2013), castle doctrine laws and homicide",
        "design": "difference-in-differences",
        "files": {"castle.dta": f"{MIXTAPE}/castle.dta"},
    },
    "card": {
        "paper": "Card (1995), proximity to college and returns to schooling",
        "design": "instrumental variables",
        "files": {"card.dta": f"{MIXTAPE}/card.dta"},
    },
    "lee": {
        "paper": "Lee (2008), incumbency advantage in US House elections",
        "design": "regression discontinuity",
        "files": {"lmb-data.dta": f"{MIXTAPE}/lmb-data.dta"},
    },
    "dw": {
        "paper": "Dehejia & Wahba (1999), reanalysis of LaLonde",
        "design": "matching",
        "files": {"nsw_dw.dta": f"{DEHEJIA}/nsw_dw.dta",
                  "cps_controls.dta": f"{DEHEJIA}/cps_controls.dta"},
    },
    "hansen": {
        "paper": "Hansen (2015), punishment and deterrence in drunk driving",
        "design": "regression discontinuity",
        "files": {"hansen_dwi.dta": f"{MIXTAPE}/hansen_dwi.dta"},
    },
    "abortion": {
        "paper": "Donohue & Levitt (2001), legalized abortion and crime",
        "design": "difference-in-differences",
        "files": {"abortion.dta": f"{MIXTAPE}/abortion.dta"},
    },
}


def _download(url: str, dest: Path) -> None:
    part = dest.with_name(dest.name + ".part")
    req = urllib.request.Request(url, headers={"User-Agent": "econ5200-replication"})
    with urllib.request.urlopen(req, timeout=120) as resp, open(part, "wb") as out:
        while chunk := resp.read(1 << 20):
            out.write(chunk)
    head = part.read_bytes()[:64].lstrip().lower()
    if part.stat().st_size == 0 or head.startswith((b"<!doctype", b"<html")):
        part.unlink()
        raise RuntimeError(f"{url} returned a web page or an empty file, not a .dta")
    part.replace(dest)


def fetch(paper: str, force: bool = False) -> list[Path]:
    """Make sure the paper's files are in data/ and return their paths, in PAPERS order."""
    if paper not in PAPERS:
        raise KeyError(f"unknown paper {paper!r}; choose from {', '.join(PAPERS)}")
    DATA_DIR.mkdir(exist_ok=True)
    paths = []
    for name, url in PAPERS[paper]["files"].items():
        dest = DATA_DIR / name
        if force or not dest.exists():
            print(f"downloading {url}", flush=True)
            _download(url, dest)
        size = dest.stat().st_size
        print(f"  {dest.relative_to(ROOT)}  " + (f"{size / 1e6:.1f} MB" if size >= 1e5 else f"{size / 1e3:.0f} KB"))
        paths.append(dest)
    return paths


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--paper", choices=list(PAPERS), default=MY_PAPER or None,
                    help="which paper's data to download (default: MY_PAPER in this file)")
    ap.add_argument("--force", action="store_true", help="download again even if the file is in data/")
    ap.add_argument("--list", action="store_true", help="list the papers and their files, download nothing")
    a = ap.parse_args()
    if a.list:
        for key, p in PAPERS.items():
            print(f"{key:9} {p['paper']} [{p['design']}]")
            for name, url in p["files"].items():
                print(f"{'':9}   {name}  <- {url}")
        return
    if not a.paper:
        sys.exit("Name a paper: python download_data.py --paper card "
                 f"(one of {', '.join(PAPERS)}), or set MY_PAPER in download_data.py.")
    print(PAPERS[a.paper]["paper"])
    fetch(a.paper, force=a.force)


if __name__ == "__main__":
    main()
