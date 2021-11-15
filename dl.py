import time
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv

csvfile = open('raw.csv', 'w', newline='', encoding='utf-8')
csvwriter = csv.writer(csvfile, lineterminator='\n')

r = requests.get(
    'https://www.parlament.hu/web/guest/a-partok-kepviselocsoportjai-es-a-fuggetlen-kepviselok-aktualis-')
soup = BeautifulSoup(r.content, 'html.parser')
session = HTMLSession()

for frakcio_table in soup.findAll('table'):
    frakcio_link = frakcio_table.find('a')
    if frakcio_link:
        print(frakcio_link.text)
        print(frakcio_link.get('href'))
        frakcio_request = requests.get(frakcio_link.get('href'))
        frakcio_soup = BeautifulSoup(frakcio_request.content, 'html.parser')
        for kepviselo_row in frakcio_soup.findAll('tr'):
            try:
                kepviselo_link = kepviselo_row.find('a')
                if kepviselo_link:
                    print(kepviselo_link.text)
                    print(kepviselo_link.get('href'))
                    kepviselo_request = requests.get(
                        kepviselo_link.get('href'))
                    kepviselo_soup = BeautifulSoup(
                        kepviselo_request.content, 'html.parser')
                    felszolalas_div = kepviselo_soup.find_all(
                        'div', {'class': 'felszolalasok'})
                    if len(felszolalas_div) > 0:
                        for felszolalas_link in felszolalas_div[0].findAll('a'):
                            if felszolalas_link:
                                print(felszolalas_link.text)
                                print(felszolalas_link.get('href'))
                                felszolalas_request = session.get(
                                    felszolalas_link.get('href'))
                                felszolalas_request.html.render(
                                    timeout=30, sleep=4)
                                # a ehhez a requesthez egy bongeszot kell emulalni, mert a nyers
                                # htmlben nincs benne az adat, ami nekunk kell, js kell hogy a
                                # ezt az oldal letoltse
                                # a js egyebkent csak annyit csinal, hogy letolti a szukseges
                                # htmlt es belerakja a megfelelo helyre a DOMban
                                # felszolalas_request = requests.get(
                                #    felszolalas_link.get('href'))
                                felszolalas_soup = BeautifulSoup(
                                    felszolalas_request.html.html, 'html.parser')
                                felszolalas_table = felszolalas_soup.find_all(
                                    'table')
                                for felszolalas_osszes_link in felszolalas_table[1].findAll('a'):
                                    if felszolalas_osszes_link:
                                        print(
                                            felszolalas_osszes_link.get('href'))
                                        print(felszolalas_osszes_link.text)
                                        felszolalas_osszes_request = session.get(
                                            felszolalas_osszes_link.get('href'))
                                        felszolalas_osszes_request.html.render(
                                            timeout=30, sleep=4)
                                        felszolalas_osszes_soup = BeautifulSoup(
                                            felszolalas_osszes_request.html.html, 'html.parser')
                                        for felszolalas in felszolalas_osszes_soup.find(id='main-content').find_all('p'):
                                            if felszolalas:
                                                if len(str(felszolalas.text).strip()) > 10:
                                                    csvwriter.writerow(
                                                        [frakcio_link.text, kepviselo_link.text, felszolalas.text])
                            time.sleep(5)
                            break  # most csak az utolsó ciklus érdekel
            except:
                time.sleep(30)
csvfile.close()
