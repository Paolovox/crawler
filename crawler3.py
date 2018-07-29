import threading, urllib, urlparse
from HTMLParser import HTMLParser
import sys
import urlparse as up
import mysql.connector as db
import datetime

reload(sys)
sys.setdefaultencoding('utf8')

class LinkHTMLParser(HTMLParser):
      A_TAG = "a"
      HREF_ATTRIBUTE = "href"

      def __init__(self):
      	  self.links = []
	  HTMLParser.__init__(self)

      def handle_starttag(self, tag, attrs):
      	  """Add all 'href' links within 'a' tags to self.links"""
      	  if cmp(tag, self.A_TAG) == 0:
	     for (key, value) in attrs:
       	     	 if cmp(key, self.HREF_ATTRIBUTE) == 0:
		    self.links.append(value)

      def handle_endtag(self, tag):
      	  pass


class CrawlerThread(threading.Thread):
        def __init__(self, binarySemaphore, url, crawlDepth):
            self.binarySemaphore = binarySemaphore
            self.url = url
            self.crawlDepth = crawlDepth
            self.threadId = hash(self)
            threading.Thread.__init__(self)
            self.mysql = db.connect(
                              host="localhost",
                              user="root",
                              passwd="root",
                              database="syrus_detector"
                            )

        def run(self):

            try: socket = urllib.urlopen(self.url)
            except:
                return False

            urlMarkUp = socket.read()
            linkHTMLParser = LinkHTMLParser()
            linkHTMLParser.feed(urlMarkUp)
            self.binarySemaphore.acquire()

            print "Thread #%d: Reading from %s" %(self.threadId, self.url)
            print "Thread #%d: Crawl Depth = %d" %(self.threadId, self.crawlDepth)
            print "Thread #%d: Retreived the following links..." %(self.threadId)

            urls = []
            for link in linkHTMLParser.links:
              link = urlparse.urljoin(self.url, link)
              urls.append(link)

            n_threads = get_value()

            self.binarySemaphore.release()

            for url in urls:

                result_url = '{uri.scheme}://{uri.netloc}'.format(uri=up.urlsplit(url))
                result = '{uri.netloc}'.format(uri=up.urlsplit(url))


                self.binarySemaphore.acquire()

                mycursor = self.mysql.cursor()
                sql = "SELECT * FROM domini WHERE url = %s"
                mycursor.execute(sql,(result,))
                myresult = mycursor.fetchall()

                self.binarySemaphore.release()

                if(result_url == self.url or result_url in urls or result == ""):
                    self.binarySemaphore.release()
                    continue

                else:
                    if not myresult:

                        self.binarySemaphore.acquire()

                        sql = "INSERT INTO domini (url, hit, created_date, updated_date) VALUES (%s, %s, %s, %s)"
                        val = (result, 1, datetime.datetime.now(), datetime.datetime.now())
                        mycursor.execute(sql, val)
                        self.mysql.commit()

                        self.binarySemaphore.release()


                if self.crawlDepth > 1 and n_threads < 20:
                    set_value(n_threads+1)
                    CrawlerThread(binarySemaphore, result_url, self.crawlDepth-1).start()
                else:
                    url_ricorsivo(result_url,self.mysql,self.binarySemaphore);


def url_ricorsivo(url,mysql,semaforo):
    try: socket = urllib.urlopen(url)
    except:
        return False

    urlMarkUp = socket.read()
    linkHTMLParser = LinkHTMLParser()
    linkHTMLParser.feed(urlMarkUp)

    urls = []
    for link in linkHTMLParser.links:
      link = urlparse.urljoin(url, link)
      urls.append(link)

    for url in urls:
        result_url = '{uri.scheme}://{uri.netloc}'.format(uri=up.urlsplit(url))
        result = '{uri.netloc}'.format(uri=up.urlsplit(url))

        semaforo.acquire()

        mycursor = mysql.cursor()
        sql = "SELECT * FROM domini WHERE url = %s"
        mycursor.execute(sql,(result,))
        myresult = mycursor.fetchall()

        semaforo.release()

        if(result_url == url or result_url in urls or result == ""):
            continue

        else:
            if not myresult:

                semaforo.acquire()

                sql = "INSERT INTO domini (url, hit, created_date, updated_date) VALUES (%s, %s, %s, %s)"
                val = (result, 1, datetime.datetime.now(), datetime.datetime.now())
                mycursor.execute(sql, val)
                mysql.commit()

                semaforo.release()

                url_ricorsivo(result_url,mysql,semaforo)




def get_value():
    global n_threads
    return n_threads

def set_value(new_value):
    global n_threads
    n_threads = new_value

if __name__ == "__main__":

   n_threads=0

   binarySemaphore = threading.Semaphore(1)
   urls = [("http://www.google.it", 6)]
   for (url, crawlDepth) in urls:
       CrawlerThread(binarySemaphore, url, crawlDepth).start()
