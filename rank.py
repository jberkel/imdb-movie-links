#!/usr/bin/env python

import networkx as nx
import csv
import sys
from pprint import pprint as pp

file = sys.argv[1]

G = nx.DiGraph()
for row in csv.reader(open(file, 'rb'), delimiter='|'):
  for connection in row[1:]:
    G.add_edge(row[0], connection)

def top(nodes, n = 250):
  return sorted(nodes.items(), key=lambda(k,v): (v,k), reverse=True)[0:n]

# degree
pp(top(nx.degree(G), 5))

# pagerank
pp(top(nx.pagerank(G)))

# HITS
(hubs, authorities) = nx.hits(G)
pp(top(hubs, 10))
pp(top(authorities, 10))
