#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl
from collections import OrderedDict

cache=dict()

def decodeASCII(chaine):
    unquoted = unquote(chaine)
    split0 = unquoted.split('#')[0]
    chaine = split0.replace('_', ' ')
    return chaine
    
    
def getJSON(page):
    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',  # TODO: compléter ceci
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')

getJSON('Philosophique')

def getRawPage(page):
    parsed = loads(getJSON(page))
    try:
        title = parsed['parse']['title']  # TODO: remplacer ceci
        content = parsed['parse']['text']['*']  # TODO: remplacer ceci
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None

def getPage(page):
    
    if page in cache.keys():
        return page, cache[page]
    else:
        title, content = getRawPage(page)
        title = decodeASCII(title)
        cache[title] = title
        
        soup = BeautifulSoup(content, 'html.parser')
        soup = soup.find('div')
        
        list_link =[]
        for p in soup.find_all('p', recursive=False):
            for a in p.find_all('a'):
                href = a.get('href')
                
                if href != None and href[:6] == '/wiki/' and 'redlink=1' not in href and ':' not in href:
                    href = decodeASCII(href[6:])
                    list_link.append(href)

        
        links = list(OrderedDict.fromkeys(list_link))
        
        if isinstance(links, str):
            links = [links]
        
        cache[title] = links
        cache[page] = links[:10]

        return title, links[:10]

if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    #print(getJSON("Utilisateur:A3nm/INF344"))
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    #print(getRawPage("Histoire"))