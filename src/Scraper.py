import bs4
import urllib.request
from Actor import Actor
from Film import Film
import json
import io

Films =  {}
Actors =  {}
films = []
ats = []
films_left = ['']
ats_left = ['/wiki/Morgan_Freeman']


def fetchValue(soup):
    table = soup.find('table', class_= 'infobox')
    for tr in table.find_all('tr'):
        if (tr.th and tr.th.string == 'Box office'):
            value = (tr.td.split('[')[0])
            value_split = (value.split(' '))
            value = value_split[0][1:].replace('.', '')
            if (len(value_split) > 1):
                if ('million' in value_split[1]):
                    value = float(value) * 10e6
                elif('billion' in value_split[1]):
                    value = float(value) * 10e9
            print(value)


def fetchAge(soup):
    bday = soup.find("span", class_= "bday")
    age = 0.0
    if bday is not None:
        age = bday.text
    return age

def fetchName(soup):
    fhead = soup.find('h1', class_='firstHeading')
    name = ''
    if fhead is not None:
        name = fhead.text
    return name

def fetchFilms(soup):
    a_name = fetchName(soup)
    age = fetchAge(soup)
    if(soup.find('span', id='Filmography')):
        film = soup.find('span', id='Filmography').findNext('ul').find_all('a', href=True)
        for f in film:
            if f not in films and 'film' in f.get('href') and f.get('href').startswith('/wiki/'):
                films.append(f.get('href'))
                films_left.append(f.get('href'))
    Actors[a_name] = age
    return films

def fetchats(soup):
    f_name = fetchName(soup)
    f_casts = []
    if(soup.find('span', id='Cast')):
        cast = soup.find('span', id='Cast').findNext('ul').find_all('a', href=True)
        for at in cast:
            if at not in ats and at.get('href').startswith('/wiki/'):
                ats.append (at.get('href'))
                ats_left.append(at.get('href'))
                f_casts.append(at.get('href')[6: ])
    Films[f_name] = f_casts
    return ats

while (len(films) < 125 or len(ats) < 250):
    while (len(films_left) > 0 and len(ats) < 250):
        next_film = films_left.pop()
        fm_obj = Film()
        sc = urllib.request.urlopen('https://en.wikipedia.org' + next_film).read()
        soup = bs4.BeautifulSoup(sc, 'html5lib')
        fetchats(soup)

    while (len(ats_left) > 0 and len(films) < 125):
        next_at = ats_left.pop()
        sc = urllib.request.urlopen('https://en.wikipedia.org' + next_at).read()
        soup = bs4.BeautifulSoup(sc, 'html5lib')
        fetchFilms(soup)

del Films['Main Page']
with io.open('film_data.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(Films, ensure_ascii=False))

with io.open('actor_data.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(Actors, ensure_ascii=False))
















