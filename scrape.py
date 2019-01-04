from urllib.request import urlopen as http_req
from urllib.request import Request
from bs4 import BeautifulSoup as Soup
from urllib import parse
import time
import sys


def get_soup(search_term, start):
    search_term = parse.quote_plus(search_term)
    url = f'https://www.google.dk/search?q={search_term}&start={start}'

    req = Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})

    u_client = http_req(req)
    page_html = u_client.read()
    u_client.close()
    page_soup = Soup(page_html, "html.parser")
    results = page_soup.find("body")
    return results


def check_anchor(href, site, start):
    if href.startswith(site):
        if start == 0:
            start = 1
        else:
            start = 1 + int((start / 10))
        print(f"Search term found on page: {start}")
        sys.exit()


def start_scraping(search_term, start, site):
    soup = get_soup(search_term, start)

    results = soup.findAll("div", {"class": 'g'})

    for result in results:
        anchor = None
        if result is not None:
            anchor = result.find("div")
        if anchor is not None:
            anchor = anchor.find("div", {"class": 'rc'})
        if anchor is not None:
            anchor = anchor.find("div", {"class": 'r'})
        if anchor is not None:
            anchor = anchor.find("a")
        if anchor is not None:
            if anchor['href'] is not None:
                check_anchor(anchor['href'], site, start)

    if len(results) == 0:
        sys.exit("Your search was not found")

    if len(results) != 0:
        print("Sleeping 15 seconds")
        time.sleep(15)
        print(f"Start: {start}")
        start_scraping(search_term, start + 10, site)
