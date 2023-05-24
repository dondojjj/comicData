import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
import unicodedata
# import pandas as pd
# import json
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def logica_uri(uri):
    image_url = "https://www.comics.org{}".format(uri)
    print("url: {}".format(image_url))
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
    # used proxies because of connection restrictions (can be removed)
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    # Send a GET request to the image URL
    response = requests.get(image_url, headers=headers, proxies=proxies, verify=False)
    # create the URL to download the image
    img = re.findall("https:\/\/files1\.comics\.org\/\/img\/gcd\/covers_by_id\/.*\.jpg", response.text)
    # setting image name for download. desired name example: HILLMAN_OCT1952_crime-must-stop-comics_v1-1
    soup = BeautifulSoup(response.content, 'html.parser')
    series = soup.find("div", class_="item_data flex_left").a.get_text(strip=True)
    # print("serie: {}".format(series))
    name = soup.find("div", class_="left").span.a.get_text(strip=True)
    # print("name: {}".format(name))
    try:
        issue_number = soup.find("span", class_="issue_number").text
    except AttributeError:
        issue_number = ''
    # print("issue_number: {}".format(issue_number))
    date = soup.find("div", class_="right").get_text(strip=True)
    if len(date) > 30:
        date = ''
    # print("date: {}".format(date))
    image_name = "{}_{}_{}_{}".format(series,date,name,issue_number)
    # normalize string
    image_name = slugify(image_name)
    # DEBUG PRINTS
    # print(img[0])
    #print(image_name)

    # download image
    img_data = requests.get(img[0]).content
    with open('data/{}.jpg'.format(image_name), 'wb') as handler:
        handler.write(img_data)


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 817 - pages
# number of pages are known
for page in range(26,817): #range(817):

    comics_covers = "https://www.comics.org/search/advanced/process/?target=issue_cover&method=icontains&logic=False&type=19&order1=series&order2=date&start_date=01%2F01%2F1900&end_date=01%2F01%2F1961&country=us&page={}".format(
        page + 1)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
    # used proxies because of connection restrictions (can be removed)
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    print("Connecting to URL: {}".format(comics_covers))
    # Send a GET request to the image URL
    response = requests.get(comics_covers, headers=headers, proxies=proxies, verify=False)
    print("downloading images page {}: ".format(page + 1))
    for uri in re.findall("/issue/[0-9]*/[a-z]*/[0-9]*/", response.text):
        logica_uri(uri)
