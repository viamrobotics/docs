from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.error


def make_soup(url):
   try:
       page = urlopen(url)
       html = page.read().decode("utf-8")
       return BeautifulSoup(html, "html.parser")
   except urllib.error.HTTPError as err:
       print(f'An HTTPError was thrown: {err.code} {err.reason} for URL: {url}')

