from bs4 import BeautifulSoup
from urllib.request import urlopen, urljoin
import urllib.error


def make_links_absolute(soup, url):
    for tag in soup.findAll('a', href=True):
        tag['href'] = urljoin(url, tag['href'])

def make_soup(url):
   try:
       page = urlopen(url)
       html = page.read().decode("utf-8")
       soup = BeautifulSoup(html, "html.parser")
       make_links_absolute(soup, url)
       return soup
   except urllib.error.HTTPError as err:
       print(f'An HTTPError was thrown: {err.code} {err.reason} for URL: {url}')

