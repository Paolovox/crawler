import multiprocessing as mp
import urlparse as up
import random
from load_page import load_page
from get_links import get_links

class Crawler(object):
    PROCESSES = 10

    def __init__(self):
        '''Inizializza il web crawler'''
        self.pool = mp.Pool(Crawler.PROCESSES)
        self.url = None
        self.tasks = []
        self.all_links, self.toload = set(), []
        self.domain, self.noquery = False, False

    def set_url(self, url):
        '''Imposta il web crawling dall'URL url, per eseguirlo
        invocare ripetutamente il metodo get_page().'''
        url = url.strip()
        if not up.urlsplit(url).scheme:
            url = 'http://' + url
        if url == self.url: return
        while self.tasks:
            if self.tasks[0].ready():
                del self.tasks[0]
        self.url = url
        self.all_links = set([url])
        self.toload = [url]

    def get_page(self):
        '''Effettua un passo del crawling impostato tramite
        il metodo set_url(). Se il crawling e' terminato,
        ritorna None. Se non e' terminato, ritorna una tripla
        (url, page, err) dove url e' l'URL della pagina che ha
        tentato di scaricare (puo' essere None nel caso non
        sia ancora pronta una pagina), se questa e' stata
        scaricata, page e' il contenuto della pagina,
        altrimenti e' None e err e' una stringa che descrive
        l'errore che si e' verificato. Anche se la pagina e'
        stata scaricata err e' non None quando si verifica un
        errore durante il parsing dei links.'''
        toload, tasks = self.toload, self.tasks
        if len(toload) == 0 and len(tasks) == 0:
            self.url = None
            return None
        url, page, err = None, None, None
        for i in range(len(tasks)):
            if tasks[i].ready():
                url, page, err = tasks[i].get()
                del tasks[i]
                if page:
                    links, perr = get_links(url, page,
                                            self.domain,
                                            self.noquery)
                    if links != None:
                        links.difference_update(self.all_links)
                        self.all_links.update(links)
                        self.toload.extend(links)
                    else:
                        err = perr
                break
        if len(tasks) < Crawler.PROCESSES and len(toload):
            i = random.randrange(0, len(toload))
            newurl = toload[i]
            del toload[i]
            tasks.append(self.pool.apply_async(load_page,
                                               (newurl,)))
        return (url, page, err)

    def config(self, domain=None, noquery=None):
        '''Se domain e' True segue solamente i links nello
        stesso dominio dell'URL iniziale. Se noquery e' True
        segue solamente i links senza la componente query.'''
        if domain != None: self.domain = domain
        if noquery != None: self.noquery = noquery

    def n_links(self):
        '''Ritorna il numero totale di links finora letti,
        sia gia' seguiti che ancora da seguire.'''
        return len(self.all_links)

def test():
    from test_crawler import test
    test(Crawler(),"www.google.it")

def test_tk():
    from tk_crawling import crawling
    crawling(Crawler())



if __name__ == '__main__':
    test()
