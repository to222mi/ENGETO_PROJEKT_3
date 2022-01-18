#!/usr/bin/env python
# coding: utf-8

import sys
import csv
import requests 
import bs4


def stiahni_html(url: str) -> requests.models.Response:
    '''
    stuahne html kod uvodnej stranky
    vrati type requests.models.Response
    '''
    
    odpoved: requests.models.Response = requests.get(url)
    return odpoved


def zmen_html_na_text(doc: requests.models.Response) -> str:
    '''
    dokument typu requests.models.Response
    zmeni na type str
    '''
    text = doc.text
    return text


def parsuj_html(text) -> bs4.BeautifulSoup:
    '''
    parsuje/fromatuje htlm_text
    '''
    formatovany_str: str = bs4.BeautifulSoup(
    text, features="html.parser"
    )
    return formatovany_str


def ziskaj_specificke_tagy(
    formatovany_text: bs4.BeautifulSoup,
    tag: str,
    popis: dict
) ->  bs4.element.ResultSet:
    '''
    pomocou metody find_all najde specifikovane tagy
    a ulozi do formatu bs4.element.ResultSet
    '''
    
    tag: bs4.element.ResultSet = formatovany_text.find_all(f'{tag}', popis)
    return tag


def ziskaj_text_tagov(tagy: bs4.element.ResultSet) -> list:
    '''
    zo zoznamu tagov vybere text 
    vrati list
    '''
    
    texty = list()

    for tag in tagy:
        
        texty.append(tag.get_text())
    return(texty)


def ziskaj_odkazy_tagov(tagy:bs4.element.ResultSet) -> list:
    '''
    zo zoznamu tagov vybere odkazy 
    vrati list odkazov
    '''
    
    odkazy = list()
    
    for tag in tagy:
        
        odkazy.append(tag.find('a').get('href'))
    return(odkazy)


def ziskaj_specificky_tag(
    formatovany_text: bs4.BeautifulSoup,
    tag: str,
    popis: dict
) ->  bs4.element.ResultSet:
    '''
    pomocou metody find najde specifikovany tag
    a ulozi do formatu bs4.element.ResultSet
    '''
    
    tag: bs4.element.ResultSet = formatovany_text.find(f'{tag}', popis)
    return tag


def vytvor_dataframe(*args):
    '''
    pospaja listy do kompletnzch dat - list of lists
    '''
    
    df = list(zip(*args))
    return df


def uloz_csv(nazov_suboru: str, hlavicka: list, data: list)-> None:
    '''
    vytvori csv subor a ulozi donho vsetky data
    '''
    
    with open(nazov_suboru, "w") as subor:
        writer = csv.writer(subor)
        writer.writerow(hlavicka)
        for riadok in data:
            writer.writerow(riadok)
        subor.close()


def definuj_hlavicku(zoznam: list)-> list:
    '''
    zadefinuje hlavicku do csv suboru ktory sa neskor vytvori
    '''
    
    hlavicka: list = zoznam
    return hlavicka


def hlavni(url: str, nazev_souboru: str)-> None:
    '''
    1. stiahne data z primarneho vebu
    2. zmeni html na text
    3. parsuje data pomocou bs4
    4  ziska tagy s kody obci
    5. ziska tagy s nazvami obci
    6. ziska kody obci z prislsnych tagov
    7. ziska nazvy obci z prislusnych tagov
    8. ziska odkazy obci ktore sa budu dalej rozklikavat
    9. vytvori prazdne listy, kde sa budu ukladat data z nasledneho for cyklu
    10. for cyklus
        11. stahuje data zo ziskanych odkazov
        12. zmeni html na text
        13. parsuje data pomocou bs4
        14. ziskava specificke tagy
        15. vyplnuje predpripravene zoznamy
    16. vytvara dataframe
    17. uklada csv
    '''
    
    print(f'STAHUJEM DATA Z URL: {url}')
    
    odpoved_serveru = stiahni_html(url)
    html_text = zmen_html_na_text(odpoved_serveru)
    fmt_text =  parsuj_html(html_text)

    tagy_kody_obci = ziskaj_specificke_tagy(
        fmt_text,
        'td',
        {'class':'cislo'}
    )
    tagy_nazvy_obci = ziskaj_specificke_tagy(
        fmt_text,
        'td',
        {'class':'overflow_name'}
    )

    kody_obci = ziskaj_text_tagov(tagy_kody_obci)
    nazvy_obci = ziskaj_text_tagov(tagy_nazvy_obci)
    odkazy_obci = ziskaj_odkazy_tagov(tagy_kody_obci)

    volici_v_seznamu = list()
    vydane_obalky = list()
    platne_hlasy = list()
    kandidujuce_strany = list()

    for odkaz in odkazy_obci:


        odpoved_serveru_2 = stiahni_html('https://volby.cz/pls/ps2017nss/' + odkaz)

        html_text_2 = zmen_html_na_text(odpoved_serveru_2)
        
        fmt_text_2 =  parsuj_html(html_text_2)

        volici_v_seznamu_obec = ziskaj_specificky_tag(
            fmt_text_2,
            'td',
            {'class': 'cislo', 'headers': 'sa2', 'data-rel': 'L1'}
        ).text
        
        vydane_obalky_obec = ziskaj_specificky_tag(
            fmt_text_2,
            'td',
            {'class': 'cislo', 'headers': 'sa3', 'data-rel': 'L1'}
        ).text
        
        platne_hlasy_obec = ziskaj_specificky_tag(
            fmt_text_2,
            'td',
            {'class': 'cislo', 'headers': 'sa6', 'data-rel': 'L1'}
        ).text

        volici_v_seznamu.append(volici_v_seznamu_obec.strip('\xa0'))
        vydane_obalky.append(vydane_obalky_obec.strip('\xa0')) 
        platne_hlasy.append(platne_hlasy_obec.strip('\xa0'))

        tagy_kandidujuce_strany_1 = ziskaj_specificke_tagy(
            fmt_text_2,
            'td',
            {'class': 'overflow_name', 'headers': 't1sa1 t1sb2'}
        )
        
        tagy_kandidujuce_strany_2 = ziskaj_specificke_tagy(
            fmt_text_2,
            'td',
            {'class': 'overflow_name', 'headers': 't2sa1 t2sb2'}
        )

        tagy_kandidujuce_strany_komplet = tagy_kandidujuce_strany_1 + tagy_kandidujuce_strany_2

        kandidujuce_strany_obec = ziskaj_text_tagov(tagy_kandidujuce_strany_komplet)

        kandidujuce_strany.append(kandidujuce_strany_obec)

    df = vytvor_dataframe(
        kody_obci,
        nazvy_obci,
        volici_v_seznamu,
        vydane_obalky, platne_hlasy,
        kandidujuce_strany
    )
    
    hlavicka = definuj_hlavicku([
        'KÓD OBCE',
        'NÁZOV OBCE', 
        'VOLIČI V ZOZNAME',
        'VYDANÉ OBÁLKY',
        'PLATNÉ HLASY', 
        'KANDIDUJÚCE STRANY'
    ])
    
    print(f'UKLADAM DO SUBORU: {nazev_souboru}')
    
    uloz_csv(nazev_souboru, hlavicka, df)
    
    print('UKONCUJEM PROGRAM !')
    
hlavni(sys.argv[1], sys.argv[2])

