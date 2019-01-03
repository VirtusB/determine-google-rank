import sys
from scrape import start_scraping


def setup(search_term, site):
    start_scraping(search_term, 0, site)


def main():
    if len(sys.argv) == 1:
        sys.exit('Search term & website missing')
    else:
        setup(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()
