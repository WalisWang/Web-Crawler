wimport bs4
import urllib.request
import json
import io
import logging

Films =  {}
Actors =  {}
films = []
ats = []
films_left = ['']
ats_left = ['/wiki/Morgan_Freeman']

# Fetch gross value of the actor for the film
def fetchValue(soup):
    table = soup.find('table', class_= 'infobox')
    if table is not None:
        for tr in table.find_all('tr'):
            if (tr.th and tr.th.string == 'Box office'):
                value_parse = (tr.td.split('[')[0]).split(' ')
                value = value_parse[0][1:].replace('.', '')
                if (len(value_parse) > 1):
                    if ('billion' in value_parse[1]):
                        value = float(value) * 10e9
                    elif ('million' in value_parse[1]):
                        value = float(value) * 10e6
                    logging.degug("Fetched  gross value is: " + value)
    else:
        logging.warning("Empty gross value. Information fetching failed!")

# Fetch birthday of the actor
def fetchAge(soup):
    bday = soup.find("span", class_= "bday")
    age = 0.0
    if bday is not None:
        age = bday.text
    else:
        logging.warning("Empty birthday. Information fetching failed!")
    return age

# Fetch name of the actor/film
def fetchName(soup):
    fhead = soup.find('h1', class_='firstHeading')
    name = ''
    if fhead is not None:
        name = fhead.text
    else:
        logging.warning("Empty name. Information fetching failed!")
    return name

# Fetch filmograohy of the actor
def fetchFilms(soup):
    a_name = fetchName(soup)
    age = fetchAge(soup)
    if(soup.find('span', id='Filmography')):
        film = soup.find('span', id='Filmography').findNext('ul').find_all('a', href=True)
        if film is None:
            logging.info("No filmography found")
        for f in film:
            if f not in films and 'film' in f.get('href') and f.get('href').startswith('/wiki/'):
                films.append(f.get('href'))
                films_left.append(f.get('href'))
    Actors[a_name] = age
    return films

# Fetch casts of the film
def fetchats(soup):
    f_name = fetchName(soup)
    f_casts = []
    if(soup.find('span', id='Cast')):
        cast = soup.find('span', id='Cast').findNext('ul').find_all('a', href=True)
        if cast is None:
            logging.info("No cast found.")
        for at in cast:
            if at not in ats and at.get('href').startswith('/wiki/'):
                ats.append (at.get('href'))
                ats_left.append(at.get('href'))
                f_casts.append(at.get('href')[6: ])
    Films[f_name] = f_casts
    return ats

# Collect all actors and films until the data set is enough (film > 125, actors > 250)
while (len(films) < 125 or len(ats) < 250):
    while (len(films_left) > 0 and len(ats) < 250):
        next_film = films_left.pop()
        logging.debug("Film: " + next_film)
        sc = urllib.request.urlopen('https://en.wikipedia.org' + next_film).read()
        soup = bs4.BeautifulSoup(sc, 'html5lib')
        fetchats(soup)

    while (len(ats_left) > 0 and len(films) < 125):
        next_at = ats_left.pop()
        logging.debug("Actor: " + next_at)
        sc = urllib.request.urlopen('https://en.wikipedia.org' + next_at).read()
        soup = bs4.BeautifulSoup(sc, 'html5lib')
        fetchFilms(soup)

# Put all the fetched data into JSON file (film_data, actor_data)
del Films['Main Page']
with io.open('film_data.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(Films, ensure_ascii=False))
with io.open('actor_data.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(Actors, ensure_ascii=False))
















