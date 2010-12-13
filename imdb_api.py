# Requires Python >= 2.6
import sys
import os
import json

try:
    import imdb
except ImportError:
    imdb = None

class ImdbAPI:
  CACHE = 'imdb_cache.json'

  def __init__(self):
    self.cache = ImdbAPI.load(self)
    self.top_250 = ImdbAPI.read_top_250(self)
    if imdb is not None: self.imdb = imdb.IMDb()

  def save(self):
    if len(self.cache) > 0:
      file = open(self.CACHE, 'w')
      json.dump(self.cache, file, indent = 2)
      file.close()

  def load(self):
    if os.path.exists(self.CACHE):
      cache = json.load(open(self.CACHE, 'r'))
    else:
      cache = {}

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

  def top_250_rank(self, title):
    return self.top_250.index(title) + 1 if self.is_top_250(title) else None

  def find_imdb(self, title):
    title = title.decode('utf-8')

    if title not in self.cache:
      sys.stderr.write("find_imdb %s:" % title.encode('utf-8'))
      m = self.find_first(title)
      if m:
        self.imdb.update(m)
        sys.stderr.write(m.getID())
        sys.stderr.write("\n")

        self.cache[title] = {
          'imdb_id': m.getID(),
          'rating': m.get('rating'),
          'plot_outline': m.get('plot outline'),
          'director': m.get('director')[0].get('name'),
          'top_250_rank': m.get('top 250 rank'),
          'year': m.get('year'),
          'kind': m.get('kind')
        }

      else:
        sys.stderr.write("not found\n")
        self.cache[title] = None

    return self.cache[title]

  def find_first(self, title):
    if self.imdb is None: return None
    try:
        # Do the search, and get the results (a list of Movie objects).
        results = self.imdb.search_movie(title)
    except imdb.IMDbError, e:
        sys.stderr.write(e)
        return None

    if results:
      # This is a Movie instance.
      movie = results[0]
      return movie
    else:
      return None
