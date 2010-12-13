import sys
import csv
import os

# Import the IMDbPY package.
try:
    import imdb
except ImportError:
    imdb = None

class ImdbAPI:
  def __init__(self):
    self.cache = ImdbAPI.load(self)
    self.top_250 = ImdbAPI.read_top_250(self)
    if imdb is not None: self.imdb = imdb.IMDb()

  def save(self, name = 'ids.csv'):
    if len(self.cache) > 0:
      file = open(name, 'wb')
      writer = csv.writer(file)
      for (k,v) in self.cache.items():
        if v: writer.writerow([k,v])
      file.close()

  def load(self, name = 'ids.csv'):
    cache = {}
    if os.path.exists(name):
      for row in csv.reader(open(name, 'r')):
        cache[row[0]] = row[1]
    return cache

  def read_top_250(self, f='top250.txt'):
    #0000001222   47196   8.0  Hauru no ugoku shiro (2004)
    top250 = []
    for row in open(f, 'r'):
      dist, votes, rating, title = row.split(None, 3)
      top250.append(title.strip())

    return top250

  def is_top_250(self,title):
    return title in self.top_250

  def find_imdb_id(self, title):
    if title not in self.cache:
      sys.stderr.write("find_imdb_id %s:" % title)
      m = self.find_first(title)
      if m is not None:
        sys.stderr.write(m.getID())
        sys.stderr.write("\n")
        self.cache[title] = m.getID()
      else:
        sys.stderr.write("not found\n")
        self.cache[title] = None

    return self.cache[title]

  def find_first(self, title):
    if self.imdb is None: return None

    in_encoding = sys.stdin.encoding or sys.getdefaultencoding()
    out_encoding = sys.stdout.encoding or sys.getdefaultencoding()

    title = unicode(title, in_encoding, 'replace')
    try:
        # Do the search, and get the results (a list of Movie objects).
        results = self.imdb.search_movie(title)
    except imdb.IMDbError, e:
        return None

    if results:
      # This is a Movie instance.
      movie = results[0]

      # So far the Movie object only contains basic information like the
      # title and the year; retrieve main information:
      #i.update(movie)

      return movie #, imdb_id
    else:
      return None
