import html, os
import urlparse as up
from load_page import load_page

class HTMLNode(object):
    def __init__(self, tag, attr, content, closed=True):
        self.tag = tag
        self.attr = attr
        self.content = content
        self.closed = closed

    def get_links(self, d=0):
        links = []
        if (self.tag == 'a' and 'href' in self.attr and
            self.attr['href'] != None):
            links.append(self.attr['href'])
        if self.tag != '_text_' and d < 100:
            for c in self.content:
                links.extend(c.get_links(d + 1))
        return links


def get_links(url, page, domain=False, noquery=False):
    '''Se domain e' True ritorna solo i links nello stesso
       dominio dell'URL di input. Se noquery e' True, ritorna
       solamente i links senza la componente query.'''
    try:
        parsed = html.parse(page, HTMLNode)
    except Exception as ex:
        return (None, str(ex))
    if parsed == None:
        return (None, 'HTML Parsing Error')
    linkset = set()
    for link in parsed.get_links():
        parsed = up.urlsplit(link)
        ext = os.path.splitext(parsed.path)[1].lower()
        if (parsed.scheme.lower() in ('http','https','ftp','')
            and (parsed.netloc or parsed.path)
            and ext in ('','.htm','.html')):
            if noquery and parsed.query: continue
            if not parsed.netloc:
                link = up.urljoin(url, link)
                parsed = up.urlsplit(link)
            else:
                if domain: continue
                if not parsed.scheme:
                    link = 'http://' + link
                    parsed = up.urlsplit(link)
            linkset.add(parsed.geturl())
    return (linkset, None)


def test(*urls):
    for url in urls:
        if not up.urlsplit(url).scheme: url = 'http://' + url
        url, page, ex = load_page(url)
        if page != None:
            print url, 'LOADED', len(page)
            links, ex = get_links(url, page)
            if links != None:
                print '  Numero Links:', len(links)
            else:
                print ex
        else:
            print url, ex

if __name__ == '__main__':
    test('www.python.org')
