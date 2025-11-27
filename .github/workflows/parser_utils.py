from bs4 import BeautifulSoup
from urllib.request import urlopen, urljoin, Request
import urllib.error
import time


def make_links_absolute(soup, url):
    for tag in soup.findAll('a', href=True):
        tag['href'] = urljoin(url, tag['href'])

def make_soup(url, max_retries=3, retry_delay=1):
    """
    Fetch a URL and parse it as HTML soup with retry logic.

    Args:
        url: The URL to fetch
        max_retries: Maximum number of retry attempts (default: 3)
        retry_delay: Initial delay between retries in seconds (default: 1)

    Returns:
        BeautifulSoup object on success, None on failure
    """
    # Create a request with a User-Agent header to avoid being blocked
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    for attempt in range(max_retries):
        try:
            # Add timeout to prevent hanging (30 seconds)
            page = urlopen(req, timeout=30)
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            make_links_absolute(soup, url)
            return soup
        except urllib.error.HTTPError as err:
            print(f'An HTTPError was thrown: {err.code} {err.reason} for URL: {url}')
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f'Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})')
                time.sleep(wait_time)
            else:
                return None
        except urllib.error.URLError as err:
            print(f'A URLError was thrown: {err.reason} for URL: {url}')
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f'Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})')
                time.sleep(wait_time)
            else:
                return None
        except Exception as err:
            print(f'An unexpected error occurred: {type(err).__name__}: {err} for URL: {url}')
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f'Retrying in {wait_time} seconds... (attempt {attempt + 1}/{max_retries})')
                time.sleep(wait_time)
            else:
                return None

    return None

