#!/usr/bin/env python3
"""Execute all workshop notebooks from clean kernels and write a JSON report."""

from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


NOTEBOOKS = [
    "1_Overview.ipynb",
    "2_Supervised_Learning.ipynb",
    "3_Unsupervised_Learning.ipynb",
    "4_Generative_models.ipynb",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--full", action="store_true", help="Use full workshop parameters.")
    parser.add_argument("--timeout", type=int, default=3600, help="Per-cell timeout in seconds.")
    parser.add_argument(
        "--start-at",
        type=int,
        choices=range(1, len(NOTEBOOKS) + 1),
        default=1,
        help="Resume at this one-based notebook number.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output_dir = root / "dry_run_outputs"
    output_dir.mkdir(exist_ok=True)
    os.environ["POLYMER_WORKSHOP_DRY_RUN"] = "0" if args.full else "1"
    os.environ.setdefault("MPLCONFIGDIR", str(root / ".matplotlib-cache"))
    os.environ.setdefault("XDG_CACHE_HOME", str(root / ".cache"))

    report = {
        "mode": "full" if args.full else "dry-run",
        "started_at_epoch": time.time(),
        "notebooks": [],
    }

    # When resuming after a targeted fix, retain earlier notebooks only after
    # validating their saved execution outputs.
    for name in NOTEBOOKS[: args.start_at - 1]:
        output = output_dir / name
        item = {"notebook": name, "status": "missing"}
        if output.is_file():
            executed = nbformat.read(output, as_version=4)
            errors = [
                result
                for cell in executed.cells
                for result in cell.get("outputs", [])
                if result.get("output_type") == "error"
            ]
            unexecuted = [
                cell
                for cell in executed.cells
                if cell.cell_type == "code"
                and "".join(cell.source).strip()
                and cell.execution_count is None
            ]
            item["status"] = "passed" if not errors and not unexecuted else "failed"
            item["reused_validated_output"] = True
        report["notebooks"].append(item)

    for name in NOTEBOOKS[args.start_at - 1:]:
        started = time.perf_counter()
        source = root / name
        output = output_dir / name
        item = {"notebook": name, "status": "running"}
        print(f"[RUN] {name}", flush=True)
        try:
            notebook = nbformat.read(source, as_version=4)
            client = NotebookClient(
                notebook,
                timeout=args.timeout,
                kernel_name="python3",
                resources={"metadata": {"path": str(root)}},
                allow_errors=False,
            )
            client.execute()
            nbformat.write(notebook, output)
            item["status"] = "passed"
        except Exception as exc:
            item["status"] = "failed"
            item["error"] = f"{type(exc).__name__}: {exc}"
            if "notebook" in locals():
                nbformat.write(notebook, output)
            report["notebooks"].append(item)
            report["finished_at_epoch"] = time.time()
            (output_dir / "report.json").write_text(
                json.dumps(report, indent=2), encoding="utf-8"
            )
            raise
        finally:
            item["seconds"] = round(time.perf_counter() - started, 3)

        report["notebooks"].append(item)
        print(f"[PASS] {name} ({item['seconds']} s)", flush=True)

    report["finished_at_epoch"] = time.time()
    (output_dir / "report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(f"Report: {output_dir / 'report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
