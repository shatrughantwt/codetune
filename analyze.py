
from pathlib import Path
import argparse
import os
import re


# Folders that we don't want to analyze.
IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
}


def analyze_file(file_path):
    """Calculate basic metrics for one Python file."""

    source = file_path.read_text(
        encoding="utf-8",
        errors="replace",
    )
    lines = source.splitlines()

    total_lines = len(lines)

    non_empty_lines = sum(
        1 for line in lines if line.strip()
    )

    function_count = sum(
        1
        for line in lines
        if re.match(r"^\s*(?:async\s+)?def\s+", line)
    )

    return {
        "file": str(file_path),
        "lines": total_lines,
        "non_empty_lines": non_empty_lines,
        "functions": function_count,
    }


def find_python_files(root):
    """Find Python files without entering ignored folders."""

    for current_dir, dirs, files in os.walk(root):
        dirs[:] = [
            name for name in dirs
            if name not in IGNORED_DIRS
        ]

        for name in files:
            if name.endswith(".py"):
                yield Path(current_dir) / name


def analyze_repository(root):
    """Analyze all Python files and return repository metrics."""

    root = Path(root).resolve()
    results = []

    for file_path in find_python_files(root):
        try:
            results.append(analyze_file(file_path))
        except OSError as error:
            print(f"Could not read {file_path}: {error}")

    return {
        "files": results,
        "file_count": len(results),
        "lines": sum(result["lines"] for result in results),
        "non_empty_lines": sum(
            result["non_empty_lines"] for result in results
        ),
        "functions": sum(
            result["functions"] for result in results
        ),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Python source code for CodeTune."
    )
    parser.add_argument(
        "repository",
        nargs="?",
        default=".",
        help="Path to the repository to analyze",
    )
    args = parser.parse_args()

    root = Path(args.repository).resolve()

    if not root.is_dir():
        parser.error(f"directory not found: {root}")

    metrics = analyze_repository(root)

    if not metrics["files"]:
        print("No readable Python files found.")
        return

    print("\nCodeTune - Repository Analysis\n")

    for result in metrics["files"]:
        print(f"File: {result['file']}")
        print(f"  Lines: {result['lines']}")
        print(f"  Non-empty lines: {result['non_empty_lines']}")
        print(f"  Functions: {result['functions']}")
        print()

    print("Repository totals:")
    print(f"  Files: {metrics['file_count']}")
    print(f"  Lines: {metrics['lines']}")
    print(f"  Non-empty lines: {metrics['non_empty_lines']}")
    print(f"  Functions: {metrics['functions']}")


if __name__ == "__main__":
    main()
