"""Small dependency-free quality gate for the public StudyCanvas report."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {
    ".cfg",
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".md",
    ".mjs",
    ".py",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

REQUIRED_PATHS = {
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "docs/ARCHITECTURE.md",
    "docs/DECISIONS.md",
    "docs/ENGINEERING-JOURNEY.md",
    "docs/PRIVACY-AND-SECURITY.md",
    "docs/PRODUCT-WALKTHROUGH.md",
    "docs/QUALITY.md",
    "assets/product/studycanvas-overview.png",
    "assets/product/highlight-to-question.png",
    "assets/product/highlight-to-answer.mp4",
    "assets/product/exam-room.png",
    "assets/product/browser-python.png",
    "assets/product/learning-canvas.png",
}

# Concatenation keeps the gate from matching its own source text.
US_SPELLINGS = {
    "behav" + "ior": "behaviour",
    "behav" + "iors": "behaviours",
    "col" + "or": "colour",
    "col" + "ors": "colours",
    "organi" + "zation": "organisation",
    "organi" + "zations": "organisations",
    "organi" + "ze": "organise",
    "organi" + "zed": "organised",
    "organi" + "zing": "organising",
    "optimi" + "zation": "optimisation",
    "optimi" + "ze": "optimise",
    "optimi" + "zed": "optimised",
    "cen" + "ter": "centre",
}

MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
WINDOWS_USER_PATH = re.compile(r"[A-Za-z]:\\" + "Users" + r"\\", re.IGNORECASE)


def repository_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return [ROOT / line for line in result.stdout.splitlines() if line]


def display(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def check_required(errors: list[str]) -> None:
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).exists():
            errors.append(f"missing required path: {relative}")


def check_secret_files(files: list[Path], errors: list[str]) -> None:
    for path in files:
        name = path.name.lower()
        if name == ".env" or (name.startswith(".env.") and name != ".env.example"):
            errors.append(f"secret-shaped file is tracked: {display(path)}")


def read_text(path: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        errors.append(f"text file is not valid UTF-8: {display(path)}")
        return None


def check_text(path: Path, text: str, errors: list[str]) -> None:
    relative = display(path)

    if "\u2014" in text:
        for line_number, line in enumerate(text.splitlines(), start=1):
            if "\u2014" in line:
                errors.append(f"em dash found: {relative}:{line_number}")

    if WINDOWS_USER_PATH.search(text) or ("/" + "Users" + "/") in text:
        errors.append(f"local user path found: {relative}")

    for line_number, line in enumerate(text.splitlines(), start=1):
        trailing = len(line) - len(line.rstrip(" \t"))
        if trailing and not (path.suffix == ".md" and trailing == 2 and line.endswith("  ")):
            errors.append(f"trailing whitespace: {relative}:{line_number}")

    if path.suffix == ".md":
        prose = re.sub(r"<[^>]+>", "", text)
        lower = prose.lower()
        for us_word, uk_word in US_SPELLINGS.items():
            match = re.search(rf"\b{re.escape(us_word)}\b", lower)
            if match:
                line_number = lower[: match.start()].count("\n") + 1
                errors.append(
                    f"use UK spelling '{uk_word}': {relative}:{line_number}"
                )


def check_markdown_links(path: Path, text: str, errors: list[str]) -> None:
    for raw_target in MARKDOWN_LINK.findall(text):
        target = raw_target.strip()
        if target.startswith("<") and target.endswith(">"):
            target = target[1:-1]
        target = target.split(maxsplit=1)[0]

        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue

        local_part = unquote(target.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0])
        if not local_part:
            continue

        resolved = (path.parent / local_part).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            errors.append(f"local link escapes repository: {display(path)} -> {target}")
            continue

        if not resolved.exists():
            errors.append(f"broken local link: {display(path)} -> {target}")


def main() -> int:
    errors: list[str] = []
    files = repository_files()

    check_required(errors)
    check_secret_files(files, errors)

    for path in files:
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path, errors)
        if text is None:
            continue
        check_text(path, text, errors)
        if path.suffix.lower() == ".md":
            check_markdown_links(path, text, errors)

    if errors:
        print("Documentation checks failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Documentation checks passed for {len(files)} repository files "
        f"with {len(REQUIRED_PATHS)} required artefacts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
