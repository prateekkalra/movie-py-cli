from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import requests
import urllib
import os
import json
import demjson

mlinkpage = requests.get("https://www.imdb.com/title/tt0145487/?ref_=fn_tt_tt_1")
soup2 = BeautifulSoup(mlinkpage.content, 'html.parser')
temp = soup2.find_all("script", attrs = { "type" : True })[1].text
print demjson.decode(temp)["contentRating"]
