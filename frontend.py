#http://stackoverflow.com/questions/9745056/how-to-save-user-input-data-to-redis-using-tornado-python

import tornado.ioloop
import tornado.web
import pickle
import lucene
from indexer import createIndex
from lucene import \
    SimpleFSDirectory, System, File, \
    Document, Field, StandardAnalyzer, IndexSearcher, Version, QueryParser

doc_urls = pickle.load(open("doc_urls.p", "rb"))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
      
      self.write('<html><body><form action="/" method="post">'
           '<p>Search for query here.</p>'
           '<input type="text" name="query" value="type query here">'
           '<input type="submit" value="Submit">'
           '</form></body></html>')
    def post(self):
      q= self.get_argument("query")

      # self.write(key)

    # def query(query):
      # query = self.get_argument("q")
      lucene.initVM()
      indexDir = "/Tmp/REMOVEME.index-dir"
      dir = SimpleFSDirectory(File(indexDir))
      analyzer = StandardAnalyzer(Version.LUCENE_30)
      searcher = IndexSearcher(dir)
      
      query = QueryParser(Version.LUCENE_30, "text", analyzer).parse(q)
      MAX = 1000
      hits = searcher.search(query, MAX)
      
      print "Found %d document(s) that matched query '%s':" % (hits.totalHits, query)
      items = []

      for hit in hits.scoreDocs:
          #items.append({'score':hit.score, 'doc':hit.doc, 'blah':hit.toString(), 'url':doc_urls[str(hit.doc)]})
          if str(hit.doc) not in doc_urls:
            continue
          if len(items) < 11:
            items.append(doc_urls[str(hit.doc)])
          doc = searcher.doc(hit.doc) 
      self.render("index.html", title="Results", items=items, query=q)




def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
