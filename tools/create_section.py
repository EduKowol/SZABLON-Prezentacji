#!/usr/bin/env python3
"""Tworzy plik sekcji prezentacji i katalogi na jej materiały."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTION_NAME_PATTERN = re.compile(r"^[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_DIRS = (
    "figures",
    "figures/source",
    "data",
    "code",
    "scripts",
    "tables",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Utwórz plik sections/NN-nazwa.tex oraz katalogi figures, data, "
            "code, scripts i tables."
        )
    )
    parser.add_argument(
        "name",
        help="nazwa w formacie NN-nazwa-sekcji, np. 04-eksperymenty",
    )
    parser.add_argument("--title-pl", help="polski tytuł sekcji")
    parser.add_argument("--title-en", help="angielski tytuł sekcji")
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="katalog projektu; domyślnie ustalany automatycznie",
    )
    return parser.parse_args()


def default_title(name: str) -> str:
    return name.split("-", 1)[1].replace("-", " ").capitalize()


def section_source(title_pl: str, title_en: str) -> str:
    return f"""% Sekcja: {title_pl} / {title_en}
% Polecenie \\section znajduje się w main.tex.

\\begin{{frame}}{{{title_pl}}}
  \\begin{{itemize}}
    \\item Zastąp ten tekst najważniejszą informacją sekcji.
    \\item Dodaj kolejne slajdy w tym samym pliku.
  \\end{{itemize}}
\\end{{frame}}
"""


def main() -> int:
    args = parse_args()
    if not SECTION_NAME_PATTERN.fullmatch(args.name):
        print(
            "Błąd: nazwa musi mieć format NN-nazwa-sekcji i zawierać wyłącznie "
            "małe litery ASCII, cyfry oraz łączniki.",
            file=sys.stderr,
        )
        return 2

    project_root = args.project_root.resolve()
    sections_dir = project_root / "sections"
    if not sections_dir.is_dir():
        print(f"Błąd: nie znaleziono katalogu sekcji: {sections_dir}", file=sys.stderr)
        return 2

    section_file = sections_dir / f"{args.name}.tex"
    resource_root = sections_dir / args.name
    title_pl = args.title_pl or default_title(args.name)
    title_en = args.title_en or default_title(args.name)

    created: list[Path] = []
    if not section_file.exists():
        section_file.write_text(section_source(title_pl, title_en), encoding="utf-8")
        created.append(section_file)

    for relative_dir in RESOURCE_DIRS:
        directory = resource_root / relative_dir
        if not directory.exists():
            directory.mkdir(parents=True)
            created.append(directory)
        (directory / ".gitkeep").touch(exist_ok=True)

    if created:
        print("Utworzono:")
        for path in created:
            print(f"  {path.relative_to(project_root)}")
    else:
        print("Struktura już istnieje; nie nadpisano żadnych plików.")

    print("\nDodaj w odpowiednim miejscu pliku main.tex:")
    print(f"\\section{{{title_pl}}}")
    print(f"\\input{{sections/{args.name}}}")
    if title_en != title_pl:
        print(f"% Tytuł angielski: {title_en}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
