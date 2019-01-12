import sys
import requests
from bs4 import BeautifulSoup
import time
from colorama import init,Fore
import urllib
import os
import demjson
init(convert=True)

print(Fore.LIGHTBLACK_EX+"Loading...")
time.sleep(0.5)
print(Fore.LIGHTBLACK_EX+"Please wait...")
try :
    data = urllib.urlopen("http://www.imdb.com/")
except :
    print "No internet connection!" 
    quit()

try:
    args = sys.argv[1:]
    movie = (' ').join(args).replace(" ", "+")
    page = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q=' + movie + '&s=tt');
    soup1 = BeautifulSoup(page.content, 'html.parser')
    i = 0
    for name in soup1.find_all("td", "result_text"):
        i = i + 1
        print "%d" %(i) + name.text
    option = input('Enter the serial number of the movie: ')
    os.system("reset") 
    if option > i :
        print("Invalid option.")
        quit()
    movieid = soup1.select(".findList tr a")[option].get('href')
    movielink = "http://www.imdb.com" + movieid
    mlinkpage = requests.get(movielink)
    soup2 = BeautifulSoup(mlinkpage.content, 'html.parser')
    movierating = soup2.select(".ratingValue span")[0].text
    metascore = soup2.find_all("div", class_ = "metacriticScore score_favorable titleReviewBarSubItem")[0].text
    metascore = metascore[1:len(metascore) - 1]
    detailsjson = soup2.find_all("script", attrs = { "type" : True })
    for detail in detailsjson :
        if detail.get("type") == "application/ld+json" :
            detailsjson = detail.text
    details = demjson.decode(detailsjson) 
    movietitle = details["name"]
    contentrating = details["contentRating"] 
    movielength = details["duration"][2:len(details["duration"])]
    genresndate = [i.text for i in soup2.select(".subtext a")]
    releasedate = genresndate[-1].strip()
    for i in soup2.find_all("div","txt-block"):
        if i.h4:
            if i.h4.text=="Budget:": moviebudget = i.h4.next_element.next_element.strip()

            if i.h4.text=="Opening Weekend USA:":movieopening = i.h4.next_element.next_element.strip()[:-1]
            if i.h4.text=="Gross USA:":movieusagross = i.h4.next_element.next_element.strip()[:-1]
            if i.h4.text=="Cumulative Worldwide Gross:":movieworldgross = i.h4.next_element.next_element.strip()[:-1]
            if i.h4.text=="Aspect Ratio:":movieratio = i.h4.next_element.next_element.strip()
            if i.h4.text=="Taglines:":movietaglines = i.h4.next_element.next_element.strip()
            if i.h4.text=="Also Known As:":moviealsoknown = i.h4.next_element.next_element.strip()
            if i.h4.text=="Country:":moviecountry = i.h4.next_sibling.next_element.text.strip()
    moviegenres = ', '.join([str(x) for x in details["genre"]])
    moviedesc = details["trailer"]["description"]
    moviedirector = details["director"]["name"]
    i = 0
    actor = [None] * len(details["actor"])
    for x in details["actor"] :
        actor[i] = details["actor"][i]["name"]
        i = i + 1
    movieactors = ", ".join(actor)
    movierating = soup2.select(".ratingValue span")[0].text

    print(Fore.LIGHTRED_EX + "Title: " + Fore.LIGHTGREEN_EX + movietitle)
    print(Fore.LIGHTRED_EX + "IMDB Rating: " + Fore.LIGHTYELLOW_EX + movierating + "/10")
    if metascore: print(Fore.LIGHTRED_EX + "Metascore: " + Fore.LIGHTYELLOW_EX + metascore + "/100")
    print(Fore.LIGHTRED_EX + "Length: " + Fore.LIGHTCYAN_EX + movielength)
    print(Fore.LIGHTRED_EX + "Genre: " + Fore.LIGHTBLUE_EX + moviegenres)
    print(Fore.LIGHTRED_EX + "Description: " + Fore.LIGHTWHITE_EX + moviedesc)
    print(Fore.LIGHTRED_EX + "Release date: " + Fore.LIGHTCYAN_EX + releasedate)
    if contentrating: print(Fore.LIGHTRED_EX + "Rating: " + Fore.LIGHTCYAN_EX + contentrating)
    print(Fore.LIGHTRED_EX + "Director: " + Fore.LIGHTBLACK_EX + moviedirector)
    print(Fore.LIGHTRED_EX + "Lead Cast: " + Fore.LIGHTBLACK_EX + movieactors)
    print(Fore.LIGHTRED_EX + "Country: " + Fore.LIGHTBLUE_EX + moviecountry)
    print(Fore.LIGHTRED_EX + "Also Known As: " + Fore.LIGHTBLUE_EX + moviealsoknown)
    print(Fore.LIGHTRED_EX + "Budget: " + Fore.LIGHTBLUE_EX + moviebudget)
    print(Fore.LIGHTRED_EX + "Opening Weekend USA: " + Fore.LIGHTBLUE_EX + movieopening)
    print(Fore.LIGHTRED_EX + "Gross USA: " + Fore.LIGHTBLUE_EX + movieusagross)
    print(Fore.LIGHTRED_EX + "Cumulative Worldwide Gross: " + Fore.LIGHTBLUE_EX + movieworldgross)
    print(Fore.LIGHTRED_EX + "Ratio: " + Fore.LIGHTBLUE_EX + movieratio)
    print(Fore.LIGHTRED_EX + "Taglines: " + Fore.LIGHTBLUE_EX + movietaglines)
except:
    print(Fore.LIGHTRED_EX+"Something's wrong,Try Again Later")
