# Projekt pomocniczy do szukania mieszkania

Może szybciej było przeglądać jedno ogłoszenie po drugim a nie pisać od razu apkę...? Nigdy się nie dowiemy :P

#### Informacje z ogłoszenia:
- cena mieszkania
- dzielnica
- wielkość mieszkania
- które piętro
- czy mamy rzut mieszkania
- ile pokoi
- zdjęcia

#### Dodatkowe informacje z tekstu:
- dokładna lokalizacja
- wysokość czynszu
- czy jest balkon
- rok budowy
- cechy okolicy
- komórka / piwnica?

#### Wyliczyć sobie później:
- odległość do stacji metra
- odległość od parku
- jaki dojazd do mojej siłowni (!!!)
- cena za metr


> LOCATION, LOCATION, LOCATION


# Plan 
1. Zebrać dane ze wszystkich ogłoszeń (+zdjęcia)
2. Wyczyścić dane 
3. Przechowywać dane w jakiś sensowny sposób
4. Strona we Flasku do przeglądania wybranych ofert - wg moich kryteriów + wszysktie zdjęcia na raz
5. Analiza wykrycie anomiali?
    - średnia cena za metr w dzielnicy
6. Podgląd na mapie (jak daleko do Goryla) i mapa [akustyczna Wawy](http://mapa.um.warszawa.pl/mapaApp1/mapa?service=mapa_akustyczna&L=PL&X=7501841.83526767&Y=5782957.86084302&S=15&O=0&T=7dffc0100100001007fff004xA9)  


? dodać info, że ogłoszenie zostało zdjęte z datą?

? Gumtree, OtoDom, Olx ? Tylko te strony?


## Założenia
1. Każde mieszkanie ma min. jedną łazienkę - więc jeśli nie ma o niej informacji w ogłoszeniu, wypełniam _missing value_ jako 1


chcę znać historię cen, żeby wiedzieć kto jest najbardziej zdesperowany
