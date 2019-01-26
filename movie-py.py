import sys
import requests
from bs4 import BeautifulSoup
import time
from colorama import init,Fore
import urllib
import os
import demjson
init(convert=True)

print(Fore.LIGHTBLACK_EX+"Loading...") # for displaying Loading....
time.sleep(0.5) # For 0.5 seconds delay.
print(Fore.LIGHTBLACK_EX+"Please wait...") # for displaying Please wait....
#try and except block below is used to checking the internet conectivity.
try :
    data = urllib.urlopen("http://www.imdb.com/")
except :
    print "No internet connection!" 
    quit()

try:
    args = sys.argv[1:] #for fetching movie name. i.,e program name is 0 and film name is 1 index.
    movie = (' ').join(args).replace(" ", "+") #for replacing spaces with + in the movie string.
    page = requests.get("https://www.imdb.com/find?q=" + movie + "&s=tt&ttype=ft&ref_=fn_ft") #for requesting movie website data from the server.
    soup1 = BeautifulSoup(page.content, 'html.parser') # parsing html
    i = 0
    for name in soup1.find_all("td", "result_text"): #looping through elements in td tags having class=result_text in html code soup1.
        i = i + 1
        print "%d" %(i) + name.text #for print search results of the movie.
    option = input('Enter the serial number of the movie: ') #for reading the serial no. of movie.
    os.system("reset") #for clearing command line 
    #below if block is for checking whether the option is valid or not.
    if option > i and option < 0:
        print("Invalid option.")
        quit()
    movieid = soup1.find_all("td", "result_text")[option - 1].select("a")[0].get('href') #for finding td tags having class = result_text and selecting <a> tags for getting href attribute value.

    movielink = "http://www.imdb.com" + movieid #movie link of select option.
    mlinkpage = requests.get(movielink)
    soup2 = BeautifulSoup(mlinkpage.content, 'html.parser')
    metascore = soup2.find_all("div", class_ = "metacriticScore score_favorable titleReviewBarSubItem") #for fetching the div tags of specified class and extracting the text between them.
    if metascore : #metascore is the score rating given by metacriticscore.com .
        metascore = metascore[0].text[1:len(metascore) - 1] #for getting string by trimming first and last letter
    else: metascore = None
    detailsjson = soup2.find_all("script", attrs = { "type" : True }) #for fetching the script tag having attribute type.
    for detail in detailsjson :
        if detail.get("type") == "application/ld+json" :
            detailsjson = detail.text
    details = demjson.decode(detailsjson) #Converting json to dictonary
    movietitle = details["name"]
    contentrating = details["contentRating"] 
    movielength = details["duration"][2:len(details["duration"])]
    genresndate = [i.text for i in soup2.select(".subtext a")]
    releasedate = genresndate[-1].strip()
    ratingcount = details["aggregateRating"]["ratingCount"]
    worstmovierating = details["aggregateRating"]["worstRating"]
    movierating = details["aggregateRating"]["ratingValue"]
    bestmovierating = details["aggregateRating"]["bestRating"]
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
    moviedesc = details["description"]
    moviedirector = details["director"]["name"]
    i = 0
    actor = [None] * len(details["actor"]) #Creating a null list of length = length of actors list 
    for x in details["actor"] :
        actor[i] = details["actor"][i]["name"] #Fetching actors name from details dictonary.
        i = i + 1
    movieactors = ", ".join(actor) #joining all element in actors list and having ", " as separator.
    #Data printing block
    print(Fore.LIGHTRED_EX + "Title: " + Fore.LIGHTGREEN_EX + movietitle)
    print(Fore.LIGHTRED_EX + "IMDB Rating: ") 
    print("\t" + Fore.LIGHTRED_EX + "Rating count: " + Fore.LIGHTYELLOW_EX + str(ratingcount))
    print("\t" + Fore.LIGHTRED_EX + "Worst movie rating: " + Fore.LIGHTYELLOW_EX + worstmovierating + "/10")
    print("\t" + Fore.LIGHTRED_EX + "Average IMDB rating: " + Fore.LIGHTYELLOW_EX + movierating + "/10")
    print("\t" + Fore.LIGHTRED_EX + "Best IMDB rating: " + Fore.LIGHTYELLOW_EX + bestmovierating + "/10")
    if metascore: print(Fore.LIGHTRED_EX + "Metascore: " + Fore.LIGHTYELLOW_EX + metascore + "/100")
    print(Fore.LIGHTRED_EX + "Length: " + Fore.LIGHTCYAN_EX + movielength)
    print(Fore.LIGHTRED_EX + "Genre: " + Fore.LIGHTBLUE_EX + moviegenres)
    print(Fore.LIGHTRED_EX + "Description: " + Fore.LIGHTWHITE_EX + moviedesc)
    print(Fore.LIGHTRED_EX + "Release date: " + Fore.LIGHTCYAN_EX + releasedate)
    if contentrating: print(Fore.LIGHTRED_EX + "Rating: " + Fore.LIGHTCYAN_EX + contentrating)
    print(Fore.LIGHTRED_EX + "Director: " + Fore.LIGHTBLACK_EX + moviedirector) 
    print(Fore.LIGHTRED_EX + "Lead Cast: " + Fore.LIGHTBLACK_EX + movieactors)
    print(Fore.LIGHTRED_EX + "Country: " + Fore.LIGHTBLUE_EX + moviecountry)
    if moviealsoknown in globals(): print(Fore.LIGHTRED_EX + "Also Known As: " + Fore.LIGHTBLUE_EX + moviealsoknown)
    if "moviebudget" in globals(): print(Fore.LIGHTRED_EX + "Budget: " + Fore.LIGHTBLUE_EX + moviebudget)
    if "movieopening" in globals(): print(Fore.LIGHTRED_EX + "Opening Weekend USA: " + Fore.LIGHTBLUE_EX + movieopening)
    if "movieusagross" in globals(): print(Fore.LIGHTRED_EX + "Gross USA: " + Fore.LIGHTBLUE_EX + movieusagross)
    if "movieworldgross" in globals(): print(Fore.LIGHTRED_EX + "Cumulative Worldwide Gross: " + Fore.LIGHTBLUE_EX + movieworldgross)
    if "movieratio" in globals(): print(Fore.LIGHTRED_EX + "Ratio: " + Fore.LIGHTBLUE_EX + movieratio)
    if "movietaglines" in globals(): print(Fore.LIGHTRED_EX + "Taglines: " + Fore.LIGHTBLUE_EX + movietaglines)
    #End of data printing blockexcept:
except:
    print(Fore.LIGHTRED_EX+"Something's wrong,Try Again Later")
