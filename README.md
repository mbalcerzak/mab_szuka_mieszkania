# Projekt pomocniczy do szukania mieszkania

Może szybciej było przeglądać jedno ogłoszenie po drugim a nie pisać od razu apkę...? Nigdy się nie dowiemy :P

#### Informacje z ogłoszenia:
- cena mieszkania
- dzielnica
- wielkość mieszkania
- czy mamy rzut mieszkania  
- ile pokoi
- zdjęcia

#### Dodatkowe informacje z tekstu:
- dokładna lokalizacja (ulica)
- które piętro
- wysokość czynszu
- czy jest balkon
- rok budowy
- cechy okolicy
- komórka / piwnica
- czy garaż dodatkowo płatny

#### Wyliczyć sobie później:
- odległość do stacji metra
- odległość od parku
- jaki dojazd do mojej siłowni (!!!)
- cena za metr


> LOCATION, LOCATION, LOCATION


# Plan 
1. Zebrać dane ze wszystkich ogłoszeń (+ zdjęcia)
2. Wyczyścić dane 
3. Przechowywać dane w jakiś sensowny sposób (+ backup w chmurze)
4. Strona we Flasku do przeglądania wybranych ofert - wg moich kryteriów + wszystkie zdjęcia na raz
5. Analiza wykrycie anomalii?
    - średnia cena za metr w dzielnicy
6. Podgląd na mapie (jak daleko do Goryla) i mapa [akustyczna Wawy](http://mapa.um.warszawa.pl/mapaApp1/mapa?service=mapa_akustyczna&L=PL&X=7501841.83526767&Y=5782957.86084302&S=15&O=0&T=7dffc0100100001007fff004xA9)  
7. Sprawdzać, czy ogłoszenie jeszcze wisi (dodać datę, w której zniknęło)


Gumtree DONE   
olx IN PROGRESS   
otodom NEXT  

## Założenia
1. Każde mieszkanie ma min. jedną łazienkę - więc jeśli nie ma o niej informacji w ogłoszeniu, wypełniam _missing value_ jako 1
2. Przy zmianie ceny ID ogłoszenia pozostaje takie samo
3. Jeśli "mieszkanie" kosztuje mniej niż 100 000 PLN to pewnie chodzi o zamianę / dzielenie własności i nie chcę mieć tego ogłoszenia w bazie



## Nowy plan? 
Może tylko apka we Flasku do sprawdzenia ogległości od wielu miejsc na raz.  
Adres nowego mieszkania - siłownia, szkoły tańca... o różnych godzinach