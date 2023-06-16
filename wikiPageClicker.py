from bs4 import BeautifulSoup
import requests
import sys

wikiUrlList = ["", ""]
wikipediaURLFront = "https://en.wikipedia.org"
wikipediaURLFrontLength = 24
substr = ['/wiki/']
maxDepth = 30
fullWikiPath = []
visitedWikis = []

def fitsCriteria(link):
    #This could probably be rewritten with a list and a for loop but whatever
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

def checkPage(curURL, endURL, depth):
    try:
        if(curURL == endURL):
            return [curURL]
        elif(depth == maxDepth):
            return []
        visitedWikis.append(curURL)
        links = []
        filteredLinks = []
        completeLinkPath = []

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

        for curFilteredLink in filteredLinks:
            if(visitedWikis.count(curFilteredLink) == 0):
                completeLinkPath = checkPage(curFilteredLink, endURL, depth+1)
                if(len(completeLinkPath) > 0):
                    completeLinkPath.insert(0, curURL)
                    return completeLinkPath
        #Get to the end without satisfying criteria
        return []
    except:
        return []

def getWikiLinks(urlList):

    urlFinished = False
    while(not urlFinished):
        if (sys.argv.count("-a") != 0):
            #Index of the string after the flag for the first article
            tempUrl = sys.argv[sys.argv.index("-a") + 1]
        else:
            tempUrl = input("Enter the starting wikipedia link: ")
        if(tempUrl == ""):
            urlList[0] = "/wiki/Garfield"
            urlFinished = True
        elif(tempUrl.find("https://en.wikipedia.org") != -1 and len(tempUrl) > wikipediaURLFrontLength):
            urlList[0] = tempUrl[wikipediaURLFrontLength:]
            urlFinished = True

    urlFinished = False
    while(not urlFinished):
        if (sys.argv.count("-b") != 0):
            #Index of the string after the flag for the second article
            tempUrl = sys.argv[sys.argv.index("-b") + 1]
        else:
            tempUrl = input("Enter the starting wikipedia link: ")
        if(tempUrl == ""):
            urlList[1] = "/wiki/Count_Dracula"
            urlFinished = True
        elif(tempUrl.find("https://en.wikipedia.org") != -1 and len(tempUrl) > wikipediaURLFrontLength):
            urlList[1] = tempUrl[wikipediaURLFrontLength:]
            urlFinished = True


getWikiLinks(wikiUrlList)
fullWikiPath = checkPage(wikiUrlList[0], wikiUrlList[1], 0)

if(len(fullWikiPath) > 0):
    print(fullWikiPath)
else:
    print("No path could be found to the end")
