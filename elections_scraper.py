
import os
import sys
import csv
import requests
import urllib.parse

import bs4
import validators

def stiahni_html(url: str) -> requests.models.Response:
    return requests.get(url)

def parsuj_html(doc: requests.models.Response) -> bs4.BeautifulSoup:
    '''
    parsuje/fromatuje htlm_text
    '''
    text = doc.text
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
    pomocou metody find_all najde specifikovany tag
    a ulozi do formatu bs4.element.ResultSet
    '''
    tag: bs4.element.ResultSet = formatovany_text.find_all(tag, popis)
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

def ziskaj_paths_tagov(tagy:bs4.element.ResultSet) -> list:
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
    tag: bs4.element.ResultSet = formatovany_text.find(tag, popis)
    return tag

def vytvor_list_listu(*args):
    '''
    pospaja listy do kompletnych dat - list of lists
    '''
    return list(zip(*args))

def uloz_csv(nazov_suboru: str, data: list)-> None:
    '''
    vytvori csv subor a ulozi donho vsetky data
    '''
    with open(nazov_suboru, "w") as subor:
        subor.write('# coding: utf-8\n')
        writer = csv.writer(subor)
        writer.writerow(
            [
                'KÓD OBCE',
                'NÁZOV OBCE', 
                'VOLIČI V ZOZNAME',
                'VYDANÉ OBÁLKY',
                'PLATNÉ HLASY', 
                'KANDIDUJÚCE STRANY'
            ]
        )
        for riadok in data:
            subor.write(str(riadok[:-1]).strip('()') + ',')
            subor.write(str(riadok[-1]).strip('[]') + '\n')

def over_argumenty(url: str, nazev_souboru: str)-> None:
    '''
    overi ci je URL validne a ci subor uz nahodou neexistuje
    '''
    if validators.url(url) != True or os.path.exists(nazev_souboru):
        print('neplatné URL alebo subor uz existuje')
        quit()

def stiahni_parsuj_uloz_primarne_url(url: str)-> list:
    '''
    stiahne, parsuje html z  primarneho url,
    vrati zoznamy udajov
    '''
    odpoved_serveru = stiahni_html(url)
    fmt_text =  parsuj_html(odpoved_serveru)

    tagy_kody_obci = ziskaj_specificke_tagy(
        fmt_text,
        'td',
        {'class': 'cislo'}
    )
    tagy_nazvy_obci = ziskaj_specificke_tagy(
        fmt_text,
        'td',
        {'class': 'overflow_name'}
    )

    kody_obci = ziskaj_text_tagov(tagy_kody_obci)
    nazvy_obci = ziskaj_text_tagov(tagy_nazvy_obci)
    paths_obci = ziskaj_paths_tagov(tagy_kody_obci)
    
    return kody_obci, nazvy_obci, paths_obci

def ziskaj_a_spoj_texty_spec_tagov(fmt_text: bs4.element.ResultSet, zoznam: list)-> list:
    '''
    ziska texty specifickych tagov a spoji do 1 listu
    '''
    tagy_kandidujuce_strany_1 = ziskaj_specificke_tagy(
        fmt_text,
        'td',
        {'class': 'overflow_name', 'headers': 't1sa1 t1sb2'}
    )

    tagy_kandidujuce_strany_2 = ziskaj_specificke_tagy(
        fmt_text,
        'td',
        {'class': 'overflow_name', 'headers': 't2sa1 t2sb2'}
    )

    tagy_kandidujuce_strany_komplet = tagy_kandidujuce_strany_1 +         tagy_kandidujuce_strany_2

    kandidujuce_strany_obec = ziskaj_text_tagov(
        tagy_kandidujuce_strany_komplet
    )

    zoznam.append(kandidujuce_strany_obec)
    
    return zoznam

def stiahni_parsuj_uloz_for_cyklus(zoznam_paths: list)-> list:
    '''
    stiahne, parsuje html postupne zo zoznamu paths
    uklada udaje do listov
    '''
    volici_v_seznamu = list()
    vydane_obalky = list()
    platne_hlasy = list()
    kandidujuce_strany = list()

    for path in zoznam_paths:
    
        odpoved_serveru_2 = stiahni_html(
            urllib.parse.urljoin(
                'https://volby.cz/pls/ps2017nss/',
                path
            )
        )
        
        fmt_text_2 =  parsuj_html(odpoved_serveru_2)

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
        
        kandidujuce_strany = ziskaj_a_spoj_texty_spec_tagov(
            fmt_text_2,
            kandidujuce_strany
        )
    
    return volici_v_seznamu, vydane_obalky, platne_hlasy, kandidujuce_strany

def hlavni(url: str, nazev_souboru: str)-> None:
    '''
    1. overi argumenty
    2. stiahne a ulozi data z primarneho url
    3. stiahne a ulozi data podla zoznamu sekundarnych url
    4. utvori databazu
    5. ulozi do .csv
    '''
    over_argumenty(url, nazev_souboru)
    
    print(f'STAHUJEM DATA Z URL: {url}')
    
    kody_obci, nazvy_obci, paths_obci = stiahni_parsuj_uloz_primarne_url(url)
        
    volici_v_seznamu, vydane_obalky, \
        platne_hlasy, kandidujuce_strany = stiahni_parsuj_uloz_for_cyklus(paths_obci)
    
    data = vytvor_list_listu(
        kody_obci,
        nazvy_obci,
        volici_v_seznamu,
        vydane_obalky,
        platne_hlasy,
        kandidujuce_strany
    )
    
    print(f'UKLADAM DO SUBORU: {nazev_souboru}')
    
    uloz_csv(nazev_souboru, data)
    
    print('UKONCUJEM PROGRAM !')
    
if __name__ == "__main__":
    hlavni(sys.argv[1], sys.argv[2])
