from bs4 import BeautifulSoup
import requests

wikiUrl = "https://en.wikipedia.org/wiki/Garfield"
substr = ['/wiki/']

def fitsCriteria(link):
    if(link.find('/wiki/Category:') != -1):
        return False
    if(link.find('/wiki/Help:') != -1):
        return False
    if(link.find('/wiki/Portal:') != -1):
        return False
    if(link.find('/wiki/File:') != -1):
        return False
    if(link.find('/wiki/Wikipedia:') != -1):
        return False
    if(link.find('/wiki/Special:') != -1):
        return False
    if(link.find('/wiki/Template:') != -1):
        return False
    if(link.find('png') != -1):
        return False
    if(link.find('jpg') != -1):
        return False
    if(link.find('jpeg') != -1):
        return False
    if(link.find('svg') != -1):
        return False
    if(link.find('webp') != -1):
        return False
    return True

def checkPage(curURL, depth):
    try:
        links = []
        filteredLinks = []

        pageToScrape = requests.get("https://en.wikipedia.org{}".format(curURL))
        soup = BeautifulSoup(pageToScrape.text, 'html.parser')
        body = soup.find_all("div", {"class": "vector-body"})
        aTags = body[0].find_all("a") #Body is a list so we need the 0th index
        aTags.pop(0) #The fist element is about protection policy, so we get rid of it

        for link in aTags:
            links.append(link.get("href"))

        #Some of the instances in link were NoneType, so those are ignored
        for i in substr:
            for j in links:
                if(isinstance(j, str) and j.find(i)==0 and fitsCriteria(j) and j not in filteredLinks):
                    filteredLinks.append(j)

        #Clears aTags and links to save resources
        links.clear()
        aTags.clear()

        #For testing. Delete Later
        for i in filteredLinks:
            print(i)
    except:
        return ''

checkPage("/wiki/Garfield", 0)