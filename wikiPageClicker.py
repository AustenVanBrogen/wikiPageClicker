from bs4 import BeautifulSoup
import requests

wikiUrl = "https://en.wikipedia.org/wiki/Garfield"
pageToScrape = requests.get(wikiUrl)
soup = BeautifulSoup(pageToScrape.text, 'html.parser')

with open(r"deleteMe.txt", "w", encoding='utf-8') as oWrite:
    oWrite.write(str(soup.prettify))
    oWrite.close()


#print(soup.prettify)