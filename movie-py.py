from utils import bcolors, Cleaner
import sys
import time
import requests
from bs4 import BeautifulSoup
from itertools import cycle
import threading


def animated_progress():
    global stop
    print()
    steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
    for step in cycle(steps):
        print(bcolors.BLUE + bcolors.ITALIC + f'\rScrapping... {step}' + bcolors.ENDC, end='', flush=True)
        if stop:
            print(bcolors.BLUE + bcolors.ITALIC + f"\rScrapping Done!" + bcolors.ENDC, flush=True)
            print()
            break

def main():
    # Call the `animated_progress` func in a different thread
    global stop
    stop = False
    t = threading.Thread(target=animated_progress)
    t.start()
    # Variable definition for 'txt-block' to prevent NameError exception
    movie_budget = 'N/A'
    movie_opening = 'N/A'
    movie_usa_gross = 'N/A'
    movie_world_gross = 'N/A'
    movie_ratio = 'N/A'
    movie_tag_lines = 'N/A'
    movie_also_known = 'N/A'
    movie_country = 'N/A'
    try:
        # args = 'ironman'
        # User's desired movie
        args = sys.argv[1:]
        movie = (' ').join(args)
        # Scrape the page and do the assignments
        page = requests.get('http://www.imdb.com/find?ref_=nv_sr_fn&q=' + movie + '&s=tt')
        soup1 = BeautifulSoup(page.content, 'html.parser')
        movie_id = soup1.select(".findList tr a")[0].get('href')
        movie_link = "http://www.imdb.com" + movie_id
        mlink_page = requests.get(movie_link)
        soup2 = BeautifulSoup(mlink_page.content, 'html.parser')
        title_nyear = soup2.select(".title_wrapper h1")[0].text
        movie_title = title_nyear[0:len(title_nyear) - 8]
        movie_year = title_nyear[len(title_nyear) - 6:len(title_nyear) - 2]
        movie_rating = soup2.select(".ratingValue span")[0].text if soup2.select(".ratingValue span") else None
        meta_score = soup2.select(".metacriticScore")
        meta_score = meta_score[0].text.strip() if meta_score else None
        content_rating = soup2.find('meta',{'itemprop':'contentRating'})
        content_rating = content_rating['content'].strip() if content_rating else None
        movie_length = soup2.select(".subtext time")[0].text.strip() if soup2.select(".subtext time") else 'N/A'
        genres_ndate = [i.text for i in soup2.select(".subtext a")]
        release_date = genres_ndate[-1].strip()
        for i in soup2.find_all("div","txt-block"):
            if i.h4:
                if i.h4.text == "Budget:":movie_budget = i.h4.next_element.next_element.strip()
                if i.h4.text == "Opening Weekend USA:":movie_opening = i.h4.next_element.next_element.strip()[:-1]
                if i.h4.text == "Gross USA:":movie_usa_gross = i.h4.next_element.next_element.strip()[:-1]
                if i.h4.text == "Cumulative Worldwide Gross:":movie_world_gross = i.h4.next_element.next_element.strip()[:-1]
                if i.h4.text == "Aspect Ratio:":movie_ratio = i.h4.next_element.next_element.strip()
                if i.h4.text == "Taglines:":movie_tag_lines = i.h4.next_element.next_element.strip()
                if i.h4.text == "Also Known As:":movie_also_known = i.h4.next_element.next_element.strip()
                if i.h4.text == "Country:":movie_country = i.h4.next_sibling.next_element.text.strip()
        movie_genres = ""
        for x in range(len(genres_ndate) - 1):
            movie_genres = movie_genres + ',' + genres_ndate[x]
        movie_genres = movie_genres[1:]
        movie_desc = soup2.select(".summary_text")[0].text.strip()
        # Movie cast extraction
        movie_cast = [i.text.strip().replace('\n', ' ') for i in soup2.select(".credit_summary_item")]
        # Make a dictionary of movie cast
        dict_cast = {}
        for item in movie_cast:
            # Create a dictionary of the casts
            dict_cast[item[:item.find(':')]] = item[item.find(':')+1:]
        # Get rid of useless characters
        cleaned_movie_cast = Cleaner()
        movie_cast = cleaned_movie_cast.text_cleaner(dict_cast=dict_cast)
        movie_director = movie_cast['Director']
        movie_actors = movie_cast['Stars']

        # After scraping, stop the `animated_progress` func and print the results
        stop = True
        time.sleep(1)

        # Print the results
        print(bcolors.RED + "Title: " + bcolors.BOLD + bcolors.GREEN + movie_title + bcolors.ENDC)
        if movie_rating:
            print(bcolors.RED + "IMDB Rating: " + bcolors.BOLD + bcolors.GREEN + movie_rating + "/10" + bcolors.ENDC)
        if meta_score:
            print(bcolors.RED + "Metascore: " + bcolors.BOLD + bcolors.GREEN + meta_score + "/100" + bcolors.ENDC)
        print(bcolors.RED + "Length: " + bcolors.BOLD + bcolors.GREEN + movie_length + bcolors.ENDC)
        print(bcolors.RED + "Year: " + bcolors.BOLD + bcolors.GREEN + movie_year + bcolors.ENDC)
        print(bcolors.RED + "Genre: " + bcolors.BOLD + bcolors.GREEN + movie_genres + bcolors.ENDC)
        print(bcolors.RED + "Description: " + bcolors.ENDC + movie_desc)
        print(bcolors.RED + "Release date: " + bcolors.BOLD + bcolors.GREEN + release_date + bcolors.ENDC)
        if content_rating:
            print(bcolors.RED + "Rating: " + bcolors.BOLD + bcolors.GREEN + content_rating + bcolors.ENDC)
        print(bcolors.RED + "Director: " + bcolors.BOLD + bcolors.GREEN + movie_director + bcolors.ENDC)
        print(bcolors.RED + "Lead Cast: " + bcolors.BOLD + bcolors.GREEN + movie_actors + bcolors.ENDC)
        print(bcolors.RED + "Country: " + bcolors.BOLD + bcolors.GREEN + movie_country + bcolors.ENDC)
        print(bcolors.RED + "Also Known As: " + bcolors.BOLD + bcolors.GREEN + movie_also_known + bcolors.ENDC)
        print(bcolors.RED + "Budget: " + bcolors.BOLD + bcolors.GREEN + movie_budget + bcolors.ENDC)
        print(bcolors.RED + "Opening Weekend USA: " + bcolors.BOLD + bcolors.GREEN + movie_opening + bcolors.ENDC)
        print(bcolors.RED + "Gross USA: " + bcolors.BOLD + bcolors.GREEN + movie_usa_gross + bcolors.ENDC)
        print(bcolors.RED + "Cumulative Worldwide Gross: " + bcolors.BOLD + bcolors.GREEN + movie_world_gross + bcolors.ENDC)
        print(bcolors.RED + "Ratio: " + bcolors.BOLD + bcolors.GREEN + movie_ratio + bcolors.ENDC)
        print(bcolors.RED + "Taglines: " + bcolors.BOLD + bcolors.GREEN + movie_tag_lines + bcolors.ENDC)
    except Exception as e:
        print(bcolors.ITALIC + bcolors.WARNING + "Something goes wrong!\nError: {}".format(e), bcolors.ENDC)
        sys.exit(1)

if __name__ == '__main__':
    main()