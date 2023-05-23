import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# from bs4 import BeautifulSoup
# import pandas as pd
# import json
import re


def logica_uri(uri):
    image_url = "https://www.comics.org{}".format(uri)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    # Send a GET request to the image URL
    response = requests.get(image_url, headers=headers, proxies=proxies, verify=False)
    img = re.findall("https:\/\/files1\.comics\.org\/\/img\/gcd\/covers_by_id\/.*\.jpg", response.text)
    # img_name = re.findall("https:\/\/files1\.comics\.org\/\/img\/gcd\/covers_by_id\/.*\.jpg",response.text)
    image_name = re.findall("https:\/\/files1\.comics\.org\/\/img\/gcd\/covers_by_id\/.*\/(.*)\.jpg", img[0])
    print(img[0])
    print(image_name)
    img_data = requests.get(img[0]).content
    with open('{}.jpg'.format(image_name[0]), 'wb') as handler:
        handler.write(img_data)


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
img_lnks_list = []
# 817
for page in range(1):
    print("extracting comic link information: ")
    image_url = "https://www.comics.org/search/advanced/process/?target=issue_cover&method=icontains&logic=False&type=19&order1=series&order2=date&start_date=01%2F01%2F1900&end_date=01%2F01%2F1961&country=us&page={}".format(
        page + 1)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0'}
    proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    # Send a GET request to the image URL
    response = requests.get(image_url, headers=headers, proxies=proxies, verify=False)
    # print(response.text)
    # soup = BeautifulSoup(response.content, "html.parser")
    # comic_links = soup.find_all("a",href=True)
    # print(comic_links)
    # img_lnks = re.findall("/issue/[0-9]*/[a-z]*/[0-9]*/",response.text)
    print("appending link lists from page {}: ".format(page + 1))
    for uri in re.findall("/issue/[0-9]*/[a-z]*/[0-9]*/", response.text):
        logica_uri(uri)
