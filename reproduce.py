#!/usr/bin/env python3
"""The one command: run every notebook in notebooks/ in name order, then print the headline table.

    python reproduce.py

Each notebook runs top to bottom in a fresh kernel, from the repository root, with
the Python that runs this script (so the packages are the ones requirements.txt
installed). Executed copies, with their outputs, are written to output/executed/.
The run stops at the first cell that fails and says which notebook it was in.

The headline table is output/headline_table.csv, which notebooks/01 writes.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import nbformat
import pandas as pd
from jupyter_client.kernelspec import KernelSpec
from jupyter_client.manager import KernelManager
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

ROOT = Path(__file__).resolve().parent
NOTEBOOKS = ROOT / "notebooks"
OUTPUT = ROOT / "output"
HEADLINE = OUTPUT / "headline_table.csv"
CELL_TIMEOUT = 1800          # seconds per cell; raise it if one estimation takes longer


class ThisPythonKernel(KernelManager):
    """A kernel that runs on this interpreter, not on whatever 'python3' kernel the machine has registered."""

    @property
    def kernel_spec(self) -> KernelSpec:
        return KernelSpec(argv=[sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                          display_name=f"Python ({sys.executable})", language="python")


def run(path: Path) -> None:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=CELL_TIMEOUT, kernel_manager_class=ThisPythonKernel,
                            resources={"metadata": {"path": str(ROOT)}})
    try:
        client.execute()
    finally:
        out = OUTPUT / "executed" / path.name
        out.parent.mkdir(parents=True, exist_ok=True)
        nbformat.write(nb, out)


def main() -> None:
    OUTPUT.mkdir(exist_ok=True)
    notebooks = sorted(NOTEBOOKS.glob("*.ipynb"))
    if not notebooks:
        sys.exit("No notebooks found in notebooks/.")
    start = time.time()
    for path in notebooks:
        t0 = time.time()
        print(f"running {path.relative_to(ROOT)} ...", flush=True)
        try:
            run(path)
        except CellExecutionError as err:
            print(f"\nFAILED in {path.relative_to(ROOT)}. The executed copy is in output/executed/.\n")
            print(err)
            sys.exit(1)
        print(f"  done in {time.time() - t0:.0f} s")
    print(f"\nAll {len(notebooks)} notebooks ran in {time.time() - start:.0f} s.\n")

    if not HEADLINE.exists():
        print("No headline table yet: output/headline_table.csv does not exist.\n"
              "Fill the 'theirs vs mine' table in notebooks/01_positioning_and_replication.ipynb;\n"
              "its last cell writes the file.")
        return
    table = pd.read_csv(HEADLINE, index_col=0)
    if table.empty:
        print("output/headline_table.csv has no rows yet.\n"
              "Add one row per replicated number to the 'theirs vs mine' table in\n"
              "notebooks/01_positioning_and_replication.ipynb: paper_estimate, my_estimate,\n"
              "and likely_source; gap_pct is computed for you.")
        return
    print("Headline table (output/headline_table.csv)\n")
    with pd.option_context("display.max_colwidth", 60, "display.width", 120):
        print(table.to_string())


if __name__ == "__main__":
    main()
