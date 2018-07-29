import multiprocessing as mp
import urlparse as up
import random
from load_page import load_page
from get_links import get_links


def test(crawler,start_url):
    if not up.urlsplit(start_url).scheme:
        start_url = 'http://' + start_url

    crawler.set_url(start_url)
    p = crawler.get_page()
    print(p)
