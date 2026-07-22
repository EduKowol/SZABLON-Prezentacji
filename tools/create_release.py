#!/usr/bin/env python3
"""Tworzy minimalną, przenośną paczkę startową szablonu prezentacji."""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT_FILES = (".gitignore", "README.md", "bibliografia.bib")
SOURCE_DIRS = ("assets", "config", "docs")
TOOL_FILES = ("create_release.py", "create_section.py")
RESOURCE_DIRS = (
    "figures",
    "figures/source",
    "data",
    "code",
    "scripts",
    "tables",
)
IGNORED_NAMES = (
    "build",
    "dist",
    "tmp",
    "__pycache__",
    "*.aux",
    "*.bbl",
    "*.bcf",
    "*.blg",
    "*.fdb_latexmk",
    "*.fls",
    "*.log",
    "*.nav",
    "*.out",
    "*.pyc",
    "*.run.xml",
    "*.snm",
    "*.synctex.gz",
    "*.toc",
    "*.vrb",
)
DEFAULT_ARCHIVES = {
    "local": Path("dist/szablon-prezentacji-weail-local.zip"),
    "online": Path("dist/szablon-prezentacji-weail-online.zip"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Utwórz minimalny ZIP szablonu prezentacji z jednym przykładowym "
            "plikiem sekcji, bez wyników kompilacji."
        )
    )
    parser.add_argument("--output", type=Path, help="własna nazwa pliku wynikowego ZIP")
    parser.add_argument(
        "--target",
        choices=("local", "online"),
        help="wariant paczki; bez tej opcji program zapyta o wybór",
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="katalog projektu; domyślnie ustalany automatycznie",
    )
    return parser.parse_args()


def choose_target(requested: str | None) -> str:
    if requested:
        return requested
    if not sys.stdin.isatty():
        raise ValueError(
            "Brak interaktywnego terminala. Podaj --target local albo --target online."
        )
    print("Wybierz wariant paczki startowej:")
    print("  1. local  - komputer lokalny; zawiera latexmkrc")
    print("  2. online - Prism/Overleaf; bez lokalnego latexmkrc")
    while True:
        answer = input("Wariant [1/2, domyślnie 1]: ").strip().lower()
        if answer in {"", "1", "local", "l"}:
            return "local"
        if answer in {"2", "online", "o"}:
            return "online"
        print("Wpisz 1 dla wariantu local albo 2 dla wariantu online.")


def copy_required(source: Path, destination: Path) -> None:
    if not source.exists():
        raise FileNotFoundError(f"Brak wymaganego elementu: {source}")
    if source.is_dir():
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns(*IGNORED_NAMES))
    else:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def starter_main(target: str) -> str:
    program_directive = "% !TeX program = lualatex\n" if target == "online" else ""
    return program_directive + r"""% !TeX TXS-program:compile = txs:///latexmk/{-pdf}
% !TeX root = main.tex
% Kompilacja lokalna: latexmk main.tex (silnik LuaLaTeX wybiera latexmkrc)
% Pełna instrukcja znajduje się w plikach README.md i WARIANT.md.

% === KONFIGURACJA SZABLONU — NIE ZMIENIAJ W TYM PLIKU ===
% Dane prezentacji, język, typ pracy, logotypy i ostatni slajd ustawia się
% wyłącznie w config/metadata.tex.
\input{config/metadata}
\documentclass[aspectratio=169,11pt]{beamer}
\usepackage{config/presentation-style}

\title{\presentationtitle}
\author{\authorname}
\date{\presentationyear}

\begin{document}

% === SLAJDY POCZĄTKOWE — NIE ZMIENIAJ KOLEJNOŚCI POLECEŃ ===
% Tytuł, autor i pozostałe dane są pobierane z config/metadata.tex.
\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{\agendatitle}
  \tableofcontents[hideallsubsections]
\end{frame}

% === SEKCJE PREZENTACJI — TUTAJ USTALASZ ICH KOLEJNOŚĆ ===
% Każdą część umieść w osobnym pliku w katalogu sections/ i dołącz przez
% \input{sections/nazwa-pliku}, bez rozszerzenia .tex.
% Nową strukturę można utworzyć poleceniem:
% python tools/create_section.py 02-nazwa --title-pl "Tytuł" --title-en "Title"
% Polecenie \section ustala nazwę w spisie treści; powinno bezpośrednio
% poprzedzać odpowiadające mu polecenie \input.
\section{Wprowadzenie}
\input{sections/01-wprowadzenie}

% === OSTATNI SLAJD — NIE EDYTUJ PONIŻSZEJ LOGIKI ===
% Wybierz wariant title, thanks albo none przez \lastslidetype w
% config/metadata.tex.
\ifdefstring{\lastslidetype}{title}{%
  \begin{frame}\titlepage\end{frame}
}{%
  \ifdefstring{\lastslidetype}{thanks}{%
    \begin{frame}
      \begin{center}
        {\color{weailblue}\LARGE\bfseries\thankstitle}\par
        \vspace{5mm}{\large\questionslabel}
      \end{center}
    \end{frame}
  }{}%
}
\end{document}
"""


def starter_section() -> str:
    return r"""\begin{frame}{Cel prezentacji}
  \begin{itemize}
    \item Przedstaw problem i cel pracy.
    \item Wyjaśnij przyjętą metodykę.
    \item Pokaż najważniejsze wyniki i wnioski.
  \end{itemize}
\end{frame}
"""


def variant_readme(target: str) -> str:
    if target == "local":
        return """# Wariant lokalny

Ta paczka zawiera `latexmkrc` i jest przeznaczona do kompilacji na komputerze.

Na Windows zainstaluj MiKTeX oraz interpreter Perl (np. Strawberry Perl),
ponieważ `latexmk` jest skryptem napisanym w Perlu. Sprawdź środowisko:

```text
perl --version
latexmk -v
lualatex --version
biber --version
```

Po instalacji Perla uruchom ponownie terminal i edytor LaTeX. Następnie
kompiluj prezentację poleceniem:

```text
latexmk main.tex
```

LuaLaTeX oraz katalog `build/` zostaną wybrane automatycznie. Gotowa
prezentacja znajdzie się w `build/main.pdf`.
"""
    return """# Wariant internetowy

Ta paczka jest przeznaczona do Prism, Overleaf lub podobnego edytora. Nie zawiera
lokalnego pliku `latexmkrc`. Po imporcie ustaw:

- dokument główny: `main.tex`;
- kompilator: LuaLaTeX.

Katalogiem plików pomocniczych zarządza platforma internetowa. Lokalna
instalacja Perla nie jest potrzebna. Jeśli wcześniej wykonano kompilację przez
pdfLaTeX, po zmianie silnika użyj funkcji pełnej kompilacji od początku
(`Recompile from scratch`) albo wyczyść pliki pomocnicze projektu.
"""


def write_starter_tree(project_root: Path, staging: Path, target: str) -> None:
    for name in ROOT_FILES:
        copy_required(project_root / name, staging / name)
    if target == "local":
        copy_required(project_root / "latexmkrc", staging / "latexmkrc")
    for name in SOURCE_DIRS:
        copy_required(project_root / name, staging / name)

    (staging / "WARIANT.md").write_text(variant_readme(target), encoding="utf-8")
    (staging / "main.tex").write_text(starter_main(target), encoding="utf-8")

    tools_dir = staging / "tools"
    tools_dir.mkdir()
    for name in TOOL_FILES:
        copy_required(project_root / "tools" / name, tools_dir / name)

    sections_dir = staging / "sections"
    sections_dir.mkdir()
    (sections_dir / "01-wprowadzenie.tex").write_text(starter_section(), encoding="utf-8")
    resources = sections_dir / "01-wprowadzenie"
    for relative in RESOURCE_DIRS:
        directory = resources / relative
        directory.mkdir(parents=True, exist_ok=True)
        (directory / ".gitkeep").touch()


def create_zip(staging: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    temporary = archive.with_suffix(archive.suffix + ".tmp")
    if temporary.exists():
        temporary.unlink()
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as handle:
            for path in sorted(staging.rglob("*")):
                if path.is_file():
                    handle.write(path, path.relative_to(staging).as_posix())
        temporary.replace(archive)
    finally:
        if temporary.exists():
            temporary.unlink()


def main() -> int:
    args = parse_args()
    project_root = args.project_root.resolve()
    try:
        target = choose_target(args.target)
    except ValueError as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 2

    output = args.output or DEFAULT_ARCHIVES[target]
    if not output.is_absolute():
        output = project_root / output
    output = output.resolve()

    if not (project_root / "main.tex").is_file():
        print(f"Błąd: nie znaleziono main.tex w {project_root}", file=sys.stderr)
        return 2
    if output.suffix.lower() != ".zip":
        print("Błąd: plik wynikowy musi mieć rozszerzenie .zip.", file=sys.stderr)
        return 2

    try:
        with tempfile.TemporaryDirectory(prefix="presentation-release-") as temporary:
            staging = Path(temporary) / "szablon-prezentacji-weail"
            staging.mkdir()
            write_starter_tree(project_root, staging, target)
            create_zip(staging, output)
    except (FileNotFoundError, OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"Błąd: {error}", file=sys.stderr)
        return 1

    with zipfile.ZipFile(output) as handle:
        file_count = len([item for item in handle.infolist() if not item.is_dir()])
    shown = output.relative_to(project_root) if project_root in output.parents else output
    print(f"Utworzono: {shown}")
    print(f"Wariant: {target}")
    print(f"Liczba plików: {file_count}")
    print(f"Rozmiar: {output.stat().st_size / 1024:.1f} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
