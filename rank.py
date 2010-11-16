#!/usr/bin/env python

import networkx as nx
import csv
import sys
from pprint import pprint as pp

def unicode_csv_reader(unicode_csv_data, **kwargs):
    csv_reader = csv.reader(unicode_csv_data, **kwargs)
    for row in csv_reader:
      yield [unicode(cell, 'utf-8').encode('utf-8') for cell in row]

def top(nodes, n = 250):
  return sorted(nodes.items(), key=lambda(k,v): (v,k), reverse=True)[0:n]

def read_graph(f):
  g = nx.DiGraph()
  for row in unicode_csv_reader(open(f, 'r'), delimiter='|'):
    for connection in row[1:]:
      g.add_edge(row[0], connection)
  return g

def sub_graph(g, n, algorithm = nx.pagerank):
  return g.subgraph([v[0] for v in top(algorithm(g), n)])

def quote(s):
  return s.replace("'", "\\'")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print __file__, "<file>"
    sys.exit(1)

  g = read_graph(sys.argv[1])
  # degree
  #pp(top(nx.degree(g), 5))

  #nx.write_dot(g, 'g.dot')

  # pagerank
  pp(top(nx.pagerank(g)))
  # HITS
  #(hubs, authorities) = nx.hits(g)
  #pp(top(hubs, 10))
  #pp(top(authorities, 10))
