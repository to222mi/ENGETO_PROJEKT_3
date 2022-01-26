## POPIS PROJEKTU

Tento program slúži na extrahovanie výsledkov parlamentných volieb v ČR v roku 2017:
[volby.cz](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"_https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ_")


## INŠTALÁCIA KNIŽNÍC

Knižnice, ktoré sú potrebné k spusteniu tohto programu sú uložené v súbore requirements.txt
V novom virtuálnom prostredí s nainštalovaným manažérom spustím príkazom:

**pip install -r requirements.txt**

## SPÚŠŤANIE PRGRAMU

Program elections_scraper.py sa spúšťa v príkazovom riadku spolu s dvoma povinnými argumentmi:

python elections_scraper.py <odkaz-na-uzemny-celok> <nazov-vysledneho-suboru>

## UKÁŽKA PROJEKTU

ukážka pre územnú úroveň Mělník:

STAHUJEM DATA Z URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2106
UKLADAM DO SUBORU: vysledky_melnik.csv
UKONCUJEM PROGRAM !

