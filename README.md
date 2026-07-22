# Szablon prezentacji pracy dyplomowej WEAiL

Szablon Beamera odwzorowuje identyfikację wizualną z prezentacji PowerPoint
WEAiL: format 16:9, trzy logotypy w górnym pasie, niebieską linię oraz stopkę
Politechniki Opolskiej i WEAiL. Struktura projektu i sposób konfiguracji są
zgodne z repozytorium
[EduKowol/SZABLON-Pracy-Dyplomowej](https://github.com/EduKowol/SZABLON-Pracy-Dyplomowej),
dzięki czemu oba szablony można wykorzystywać w podobny sposób.

## Szybki start

Do zalecanej kompilacji lokalnej na Windows potrzebne są **MiKTeX oraz Perl**,
ponieważ używany przez szablon program `latexmk` jest skryptem napisanym w
Perlu. Można zainstalować np. [Strawberry Perl](https://strawberryperl.com/),
a następnie ponownie uruchomić terminal i edytor LaTeX. Edytory internetowe,
takie jak Overleaf lub Prism, nie wymagają instalowania Perla na komputerze
użytkownika.

1. Uzupełnij dane w `config/metadata.tex`.
2. Zastąp treści demonstracyjne w katalogu `sections/`.
3. Dodaj własne rysunki w podkatalogach sekcji i wstawiaj je przez `\includegraphics`.
4. Uruchom `latexmk main.tex`.

Gotowy plik znajdzie się w `build/main.pdf`. Projekt wymaga LuaLaTeX; wybór
silnika i katalog wynikowy są zapisane w `latexmkrc`.

## Kompilacja lokalna w Windows

Przed pierwszą kompilacją sprawdź wymagane programy:

```text
perl --version
latexmk -v
lualatex --version
biber --version
```

Jeżeli `latexmk` zgłasza brak interpretera Perl albo polecenie `perl` nie jest
rozpoznawane, zainstaluj Perl (np. Strawberry Perl), zamknij i ponownie otwórz
terminal oraz edytor LaTeX, a potem powtórz sprawdzenie. Sam LuaLaTeX nie wymaga
Perla, ale zalecany w tym projekcie `latexmk` potrzebuje go do automatycznego
wykonywania wszystkich przebiegów LuaLaTeX i Bibera.

```text
latexmk main.tex       # kompilacja
latexmk -g main.tex    # wymuszenie pełnej ponownej kompilacji
latexmk -C main.tex    # usunięcie artefaktów kompilacji
```

Gotowa prezentacja po kompilacji znajduje się w `build/main.pdf`.

## Najważniejsze elementy

- `main.tex` -- kolejność sekcji i slajdów;
- `config/metadata.tex` -- tytuł, autor, promotor, kierunek, język i logotypy;
- `config/presentation-style.sty` -- kompletna warstwa wizualna Beamera;
- `sections/` -- treść i materiały poszczególnych części prezentacji;
- `assets/branding/` -- oficjalne materiały identyfikacji wizualnej;
- `bibliografia.bib` -- baza źródeł obsługiwana przez `biblatex` i `biber`;
- `tools/` -- generatory paczki startowej i struktury nowej sekcji.

## Język i typ pracy

W `config/metadata.tex` ustaw:

```tex
\newcommand{\presentationlanguage}{polish} % polish albo english
\newcommand{\thesistype}{engineering}      % engineering, master albo doctoral
```

Logo KreativEU można ukryć przez ustawienie `\showkreativeulogo` na `false`.
Po ustawieniu `\presentationlanguage` na `english` szablon automatycznie używa
angielskiego logo Politechniki Opolskiej oraz angielskich nazw w stopce. Dwa
pozostałe logotypy pozostają bez zmian.

Plik `logo-en-cropped.pdf` jest pozbawioną pustych marginesów, nadal wektorową
wersją dostarczonego `logo en.pdf`, przygotowaną do użycia w nagłówku slajdu.

## Ostatni slajd

Polecenie `\lastslidetype` w `config/metadata.tex` przyjmuje jedną z wartości:

- `title` -- ponowne wyświetlenie strony tytułowej (ustawienie domyślne);
- `thanks` -- osobny slajd „Dziękuję za uwagę” albo jego wersja angielska;
- `none` -- brak dodatkowego slajdu końcowego.

## Polskie znaki w listingach

Styl listingów rejestruje polskie litery bezpośrednio w `\lst@DefEC`, dzięki
czemu LuaLaTeX zachowuje ich właściwą kolejność, odstępy i kolorowanie.
Komentarze, napisy i identyfikatory zawierające `ąćęłńóśźż` są poprawnie
wyświetlane bez mapowania `literate`.

## Tworzenie nowej sekcji

Nowy plik sekcji oraz katalogi na jej materiały tworzy polecenie:

```text
python tools/create_section.py 04-eksperymenty --title-pl "Eksperymenty" --title-en "Experiments"
```

Powstaną `sections/04-eksperymenty.tex` oraz katalogi `figures`, `data`, `code`,
`scripts` i `tables`. Program nie nadpisuje istniejących plików i na końcu
wyświetla polecenia, które należy dodać do `main.tex`.

## Czysta paczka startowa

Repozytorium zawiera gotowe paczki startowe w katalogu `dist/`:

- `szablon-prezentacji-weail-local.zip` -- do pracy na własnym komputerze;
- `szablon-prezentacji-weail-online.zip` -- do przesłania do edytora online.

Minimalną paczkę dla nowej prezentacji można utworzyć interaktywnie:

```text
python tools/create_release.py
```

Albo wskazać wariant bez pytania:

```text
python tools/create_release.py --target local
python tools/create_release.py --target online
```

- `local` zawiera `latexmkrc` i jest przeznaczony do kompilacji na komputerze;
  na Windows wymaga MiKTeX-u oraz interpretera Perl;
- `online` nie zawiera `latexmkrc` i jest przeznaczony do Prism, Overleaf lub
  podobnego edytora, w którym należy wybrać LuaLaTeX; lokalna instalacja Perla
  nie jest potrzebna.

Archiwa trafiają do `dist/szablon-prezentacji-weail-local.zip` albo
`dist/szablon-prezentacji-weail-online.zip`. Zawierają jeden krótki przykład
sekcji, bez plików z katalogów `build`, `tmp` i bez rozbudowanej treści
demonstracyjnej. Ponowne uruchomienie generatora aktualizuje odpowiednie
archiwum w katalogu `dist/`.

## Dobre praktyki

- Jeden slajd powinien przekazywać jedną główną myśl.
- Na wykresach podawaj jednostki, legendę i źródło danych.
- Nie zmniejszaj tekstu, aby zmieścić nadmiar treści -- skróć go lub podziel slajd.
- Bibliografię twórz przez `\cite{klucz}` i wpisy w `bibliografia.bib`.
- Po kompilacji obejrzyj cały PDF w trybie pełnoekranowym.
