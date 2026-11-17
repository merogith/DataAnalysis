"""Rebuild, execute and render all three analyses from the checked-in data.

Run from any directory: python scripts/rebuild.py
No data download or synthetic regeneration is performed.
"""
from pathlib import Path
import argparse
import subprocess
import sys

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("projects", nargs="*", help="Optional project folder names; defaults to all three")
    args = parser.parse_args()
    projects = [ROOT / name for name in args.projects] if args.projects else sorted(ROOT.glob("project-*"))
    for project in projects:
        if project.parent != ROOT or not (project / "build_notebook.py").is_file():
            parser.error(f"Not a project folder: {project}")
        subprocess.run([sys.executable, "build_notebook.py"], cwd=project, check=True)
        notebook_path = project / "analysis.ipynb"
        notebook = nbformat.read(notebook_path, as_version=4)
        notebook.metadata.kernelspec = {
            "display_name": "Python 3", "language": "python", "name": "python3"
        }
        NotebookClient(notebook, timeout=300, kernel_name="python3",
                       resources={"metadata": {"path": str(project)}}).execute()
        for cell in notebook.cells:
            cell.metadata.pop("execution", None)
        nbformat.write(notebook, notebook_path)
        html, _ = HTMLExporter(template_name="lab").from_notebook_node(notebook)
        (project / "analysis.html").write_text(html)
        print(f"Executed and rendered {project.name}", flush=True)


if __name__ == "__main__":
    main()
