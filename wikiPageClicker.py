from bs4 import BeautifulSoup
import requests

wikiUrl = "https://en.wikipedia.org/wiki/Garfield"
substr = ['/wiki/']

def checkPage(curURL):
    links = []
    filteredLinks = []

    pageToScrape = requests.get(curURL)
    soup = BeautifulSoup(pageToScrape.text, 'html.parser')
    body = soup.find_all("div", {"class": "vector-body"})
    aTags = body[0].find_all("a") #Body is a list so we need the 0th index
    aTags.pop(0) #The fist element is about protection policy, so we get rid of it

    for link in aTags:
        links.append(link.get("href"))

    #Some of the instances in link were NoneType, so those are ignored
    for i in substr:
        for j in links:
            if(isinstance(j, str) and j.find(i)==0 and j not in filteredLinks):
                filteredLinks.append(j)

    #Clears aTags and links to save resources
    links.clear()
    aTags.clear()

    #For testing. Delete Later
    for i in filteredLinks:
        print(i)

checkPage("https://en.wikipedia.org/wiki/Garfield")