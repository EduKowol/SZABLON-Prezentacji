# Wszystkie artefakty kompilacji trafiają do jednego katalogu.
# Dzięki temu katalog główny projektu zawiera wyłącznie źródła.
# Na Windows program latexmk wymaga interpretera Perl, np. Strawberry Perl.
# Sprawdzenie środowiska: perl --version oraz latexmk -v
$out_dir = 'build';
$aux_dir = 'build';

# Domyślnym silnikiem projektu jest LuaLaTeX.
$pdf_mode = 4;
$lualatex = 'lualatex %O %S';

# Pliki usuwane przez: latexmk -C
$clean_ext .= ' run.xml bbl bcf blg synctex.gz';
