import sys
import requests
from bs4 import BeautifulSoup
import time
from colorama import init,Fore
init(convert=True)

print(Fore.LIGHTBLACK_EX+"Loading...")
time.sleep(0.5)
print(Fore.LIGHTBLACK_EX+"Please wait...\n")

try:
    args = sys.argv[1:]
    movie = (' ').join(args)
    page = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q=' + movie + '&s=tt');
    soup1 = BeautifulSoup(page.content, 'html.parser')
    movieid = soup1.select(".findList tr a")[0].get('href')
    movielink = "http://www.imdb.com" + movieid
    mlinkpage = requests.get(movielink)
    soup2 = BeautifulSoup(mlinkpage.content, 'html.parser')
    titlenyear = soup2.select(".title_wrapper h1")[0].text
    movietitle = titlenyear[0:len(titlenyear) - 8]
    movieyear = titlenyear[len(titlenyear) - 6:len(titlenyear) - 2]
    movierating = soup2.select(".ratingValue span")[0].text
    metascore = soup2.select(".metacriticScore")
    metascore = metascore[0].text.strip() if metascore else None
    contentrating = soup2.find('meta',{'itemprop':'contentRating'})
    contentrating = contentrating['content'].strip() if contentrating else None
    movielength = soup2.select(".subtext time")[0].text.strip()
    genresndate = [i.text for i in soup2.select(".subtext a")]
    releasedate = genresndate[-1].strip()
    moviegenres = ""
    for x in range(len(genresndate) - 1):
        moviegenres = moviegenres + ',' + genresndate[x]
    moviegenres = moviegenres[1:]
    moviedesc = soup2.select(".summary_text")[0].text.strip()
    moviecast = [i.text for i in soup2.select(".credit_summary_item span a span")]
    moviedirector = moviecast[0]
    movieactors = moviecast[3] + ',' + moviecast[4] + ',' + moviecast[5];

    print(Fore.LIGHTRED_EX + "Title: " + Fore.LIGHTGREEN_EX + movietitle)
    print(Fore.LIGHTRED_EX + "IMDB Rating: " + Fore.LIGHTYELLOW_EX + movierating + "/10")
    if metascore: print(Fore.LIGHTRED_EX + "Metascore: " + Fore.LIGHTYELLOW_EX + metascore + "/100")
    print(Fore.LIGHTRED_EX + "Length: " + Fore.LIGHTCYAN_EX + movielength)
    print(Fore.LIGHTRED_EX + "Year: " + Fore.LIGHTMAGENTA_EX + movieyear)
    print(Fore.LIGHTRED_EX + "Genre: " + Fore.LIGHTBLUE_EX + moviegenres)
    print(Fore.LIGHTRED_EX + "Description: " + Fore.LIGHTWHITE_EX + moviedesc)
    print(Fore.LIGHTRED_EX + "Release date: " + Fore.LIGHTCYAN_EX + releasedate)
    if contentrating: print(Fore.LIGHTRED_EX + "Rating: " + Fore.LIGHTCYAN_EX + contentrating)
    print(Fore.LIGHTRED_EX + "Director: " + Fore.LIGHTBLACK_EX + moviedirector)
    print(Fore.LIGHTRED_EX + "Lead Cast: " + Fore.LIGHTBLACK_EX + movieactors)
except:
    print(Fore.LIGHTRED_EX+"Something's wrong,Try Again Later")
