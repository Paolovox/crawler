import urllib2 as ul

HEADER = {'User-Agent':"Mozilla/5.0",
          'Accept':"text/html;q=1.0,*;q=0",
          'Accept-Encoding':"identity;q=1.0,*;q=0"}

def load_page_1(url):
    print url
    req = ul.Request(url, headers=HEADER)
    f = ul.urlopen(req, timeout=5)
    res_h = f.headers
    print res_h

##load_page_1('http://www.python.org')
##load_page_1('http://www.agi.it/borsa')
##load_page_1('http://www.nonesiste.com')


def load_page_2(url):
    print url
    try:
        req = ul.Request(url, headers=HEADER)
        f = ul.urlopen(req, timeout=5)
        res_h = f.headers
        for k in ('Content-Type','Content-Encoding'):
            print k+':', (res_h[k] if k in res_h else None)
    except Exception as ex:
        print ex

##load_page_2('http://www.python.org')
##load_page_2('http://www.agi.it/borsa')
##load_page_2('http://www.nonesiste.com')
##load_page_2('http://www.google.com')


def load_page_3(url):
    try:
        req = ul.Request(url, headers=HEADER)
        f = ul.urlopen(req, timeout=5)
        res_h = f.headers
        ce = 'Content-Encoding'
        if ce in res_h:
            return (url, None, ce+': '+res_h[ce])
        page = unicode(f.read(), encoding='utf-8')
        return (url, page, None)
    except Exception as ex:
        return (url, None, str(ex))

import urlparse as up

LOAD_PAGE = load_page_3

def test(*urls):
    for url in urls:
        if not up.urlsplit(url).scheme: url = 'http://' + url
        url, page, ex = LOAD_PAGE(url)
        if page != None:
            print url, 'LOADED', len(page)
        else:
            print url, ex

##test('www.google.com','www.agi.it/borsa','www.nonesiste.com')

##test('www.nih.gov')


def load_page(url):
    try:
        req = ul.Request(url, headers=HEADER)
        f = ul.urlopen(req, timeout=5)
        res_h = f.headers
        ce = 'Content-Encoding'
        if ce in res_h:
            return (url, None, ce+': '+res_h[ce])
        charsets = ['utf-8', 'latin-1']
        if 'Content-Type' in res_h:
            ct = res_h['Content-Type'].lower()
            i = ct.find('charset=')
            if i >= 0:
                charsets.insert(0, ct[i+len('charset='):])
        page = f.read()
        for enc in charsets:
            try:
                page = unicode(page, encoding=enc)
                break
            except: continue
        else: return (url, None, 'Encoding Error')
        return (url, page, None)
    except Exception as ex:
        return (url, None, str(ex))

LOAD_PAGE = load_page

##test('www.nih.gov')
