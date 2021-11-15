import feedparser
import re
import time
import requests
from bs4 import BeautifulSoup

import spacy

nlp = spacy.load('model')

feed_444_hu = feedparser.parse("https://444.hu/feed")

cleanre = re.compile(
    r'<img[^>]*>|<a[^>]*>[^<]*</a>|</?[^>]*>|„[^”]*”|(A bejegyzés megtekintése az Instagramon)|\"[^\"]*\"')


print('444.hu')

opposition = 0.0
ruleing = 0.0
articlelength = 0
for entry in feed_444_hu.entries:
    content = entry['content'][0]['value']
    title = entry['title']
    clean_content = cleanre.sub('', content).strip()
    clean_title = cleanre.sub('', title).strip()
    clean_full = clean_title + '\n' + clean_content
    if 'tags' in entry:
        terms = [tag['term'] for tag in entry['tags']]
        if True:
            # print(clean_title)
            # print(terms)
            # print(clean_content)
            # print('ellenzék: {:.2} kormány: {:.2}\n'.format(
            #    nlp(clean_full).cats['Ellenzék'], nlp(clean_full).cats['Kormány']))
            # print(nlp(clean_full).cats)
            opposition += nlp(clean_full).cats['Ellenzék']
            ruleing += nlp(clean_full).cats['Kormány']
            articlelength += 1

print('cikkek száma', articlelength)
print('összesen ellenzék: {:.2} kormány: {:.2}\n'.format(
    opposition/(opposition+ruleing), ruleing/(opposition+ruleing)))

cleanre = re.compile(
    r'<img[^>]*>|<a[^>]*>[^<]*</a>|</?[^>]*>|„[^”]*”|(Ezt az írást nem közölhettük volna olvasóink .*)|Nyitókép:.*|\"[^\"]*\"|(KÖSZÖNJÜK!)|(A Válasz Online szerkesztőségi tulajdonban van, .*)|\(Fotó: .*')

feed_valaszonline_hu = feedparser.parse("https://valaszonline.hu/rss")
print('valaszonline.hu')
opposition = 0.0
ruleing = 0.0
articlelength = 0
for entry in feed_valaszonline_hu.entries:
    content = entry['content'][0]['value']
    title = entry['title']
    if '(x)' in title:
        continue
    clean_content = cleanre.sub('', content).strip()
    clean_title = cleanre.sub('', title).strip()
    clean_full = clean_title + '\n' + clean_content
    # print(clean_title)
    # print(entry['author'])
    # print('ellenzék: {:.2} kormány: {:.2}\n'.format(
    #    nlp(clean_full).cats['Ellenzék'], nlp(clean_full).cats['Kormány']))
    # print(clean_content)
    opposition += nlp(clean_full).cats['Ellenzék']
    ruleing += nlp(clean_full).cats['Kormány']
    articlelength += 1

print('cikkek száma', articlelength)
print('összesen ellenzék: {:.2} kormány: {:.2}\n'.format(
    opposition/(opposition+ruleing), ruleing/(opposition+ruleing)))


cleanre = re.compile(
    r'<img[^>]*>|<a[^>]*>[^<]*</a>|</?[^>]*>|„[^”]*”|“[^”]*”|\"[^\"]*\"|(Kapcsolódó.*)|(Forrás.*)|(\(?fényképek.*)|((A )?\(?N|nyitókép.*)|(Címlapkép.*)|(Fotó.*)')
feed_index_hu = feedparser.parse(
    "https://index.hu/belfold/rss")
print('index.hu')
opposition = 0.0
ruleing = 0.0
articlelength = 0
for entry in feed_index_hu.entries:
    r = requests.get(entry['link'])
    title = entry['title']
    clean_title = cleanre.sub('', title).strip()
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find("div", {"class": "cikk-torzs-container"})
    time.sleep(1)
    content = ''
    for paragraph in soup.find_all("p"):
        content += paragraph.text.strip()
    clean_content = re.sub(r'(\n\s*)+\n+', '\n\n',
                           cleanre.sub('', content).strip())
    # print(clean_title)
    clean_full = clean_title + '\n' + clean_content
    # print('ellenzék: {:.2} kormány: {:.2}\n'.format(
    #    nlp(clean_full).cats['Ellenzék'], nlp(clean_full).cats['Kormány']))
    opposition += nlp(clean_full).cats['Ellenzék']
    ruleing += nlp(clean_full).cats['Kormány']
    time.sleep(0.5)
    articlelength += 1

print('cikkek száma', articlelength)
print('összesen ellenzék: {:.2} kormány: {:.2}\n'.format(
    opposition/(opposition+ruleing), ruleing/(opposition+ruleing)))


cleanre = re.compile(
    r'<img[^>]*>|<a[^>]*>[^<]*</a>|</?[^>]*>|„[^”]*”|“[^”]*”|\"[^\"]*\"|(A  bejegyzés először.*)|(Forrás)')

feed_pestisracok_hu = feedparser.parse("https://pestisracok.hu/feed/")
print('pestisracok.hu')
opposition = 0.0
ruleing = 0.0
articlelength = 0
for entry in feed_pestisracok_hu.entries:
    content = entry['content'][0]['value']
    title = entry['title']
    clean_content = cleanre.sub('', content).strip()
    clean_title = cleanre.sub('', title).strip()
    clean_full = clean_title + '\n' + clean_content
    # print(clean_title)
    # print('ellenzék: {:.2} kormány: {:.2}\n'.format(
    #    nlp(clean_full).cats['Ellenzék'], nlp(clean_full).cats['Kormány']))
    # print(clean_content)
    opposition += nlp(clean_full).cats['Ellenzék']
    ruleing += nlp(clean_full).cats['Kormány']
    articlelength += 1

print('cikkek száma', articlelength)
print('összesen ellenzék: {:.2} kormány: {:.2}\n'.format(
    opposition/(opposition+ruleing), ruleing/(opposition+ruleing)))


cleanre = re.compile(
    r'<img[^>]*>|<a[^>]*>[^<]*</a>|</?[^>]*>|„[^”]*”|“[^”]*”|\"[^\"]*\"|(Nyitófotó.*)|(Forrás.*)|(\(?fényképek.*)|((A )?\(?N|nyitókép.*)|(Címlapkép.*)|(Fotó.*)')
feed_mandiner_hu = feedparser.parse("https://mandiner.hu/feed/")
print('mandiner.hu')
opposition = 0.0
ruleing = 0.0
articlelength = 0
for entry in feed_mandiner_hu.entries:
    r = requests.get(entry['link'])
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find("div", {"id": "articlecontent"})
    tags = soup.find("div", {"class": "taglist"})
    if not ('belföld' in tags.text or 'baloldal' in tags.text or 'jobboldal' in tags.text):
        continue
    content = div.text
    clean_full = cleanre.sub('', content).strip()
    # print(clean_full)
    # print('ellenzék: {:.2} kormány: {:.2}\n'.format(
    #    nlp(clean_full).cats['Ellenzék'], nlp(clean_full).cats['Kormány']))
    opposition += nlp(clean_full).cats['Ellenzék']
    ruleing += nlp(clean_full).cats['Kormány']
    time.sleep(0.5)
    articlelength += 1

print('cikkek száma', articlelength)
print('összesen ellenzék: {:.2} kormány: {:.2}\n'.format(
    opposition/(opposition+ruleing), ruleing/(opposition+ruleing)))


cleanre = re.compile(
    r'<img[^>]*>|<a[^>]*>[^<]*</a>|</?[^>]*>|„[^”]*”|“[^”]*”|\"[^\"]*\"|(Kapcsolódó.*)|(Forrás.*)|(\(?fényképek.*)|((A )?\(?N|nyitókép.*)|(Címlapkép.*)|(Fotó.*)')
feed_origo_hu = feedparser.parse(
    "https://www.origo.hu/contentpartner/rss/origoall/origo.xml")
print('origo.hu')
opposition = 0.0
ruleing = 0.0
articlelength = 0
for entry in feed_origo_hu.entries:
    category = entry['category']
    if category.strip() != 'Itthon':
        continue
    r = requests.get(entry['link'])
    soup = BeautifulSoup(r.content, 'html.parser')
    div = soup.find("article", {"class": "article-body"})
    time.sleep(1)
    content = div.text
    clean_full = cleanre.sub('', content).strip()
    # print(clean_full)
    # print('ellenzék: {:.2} kormány: {:.2}\n'.format(
    #    nlp(clean_full).cats['Ellenzék'], nlp(clean_full).cats['Kormány']))
    opposition += nlp(clean_full).cats['Ellenzék']
    ruleing += nlp(clean_full).cats['Kormány']
    time.sleep(0.5)
    articlelength += 1

print('cikkek száma', articlelength)
print('összesen ellenzék: {:.2} kormány: {:.2}\n'.format(
    opposition/(opposition+ruleing), ruleing/(opposition+ruleing)))
