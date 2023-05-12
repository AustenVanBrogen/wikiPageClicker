from bs4 import BeautifulSoup
import requests

wikiUrl = "https://en.wikipedia.org/wiki/Garfield"
pageToScrape = requests.get(wikiUrl)
soup = BeautifulSoup(pageToScrape.text, 'html.parser')

# Saves the html to a file to read it. DELETE LATER 
# with open(r"deleteMe.txt", "w", encoding='utf-8') as oWrite:
#     oWrite.write(str(soup.prettify))
#     oWrite.close()

#print(soup.title)

body = soup.find_all("div", {"class": "vector-body"})
#print(body[0])
aTags = body[0].find_all("a") #Body is a list so we need the 0th index
aTags.pop(0) #The fist element is about protection policy, so we get rid of it

for link in aTags:
    print(link.get("href"))