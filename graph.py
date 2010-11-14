#!/usr/bin/env python

import networkx as nx
import csv
import sys
import pprint

file = sys.argv[1]

G = nx.DiGraph()
for row in csv.reader(open(file, 'rb'), delimiter='|'):
  for connection in row[1:]:
    G.add_edge(row[0], connection)

#print sorted(nx.degree(G).items(), key=lambda(k,v): (v,k), reverse=True)[0:5]

# pagerank
pprint.pprint(sorted(nx.pagerank(G).items(), key=lambda(k,v): (v,k),
                     reverse=True)[0:250])

# hits
#(hubs, authorities) = nx.hits(G)
#print sorted(hubs.items(), key=lambda(k,v): (v,k), reverse=True)[0:10]
#print
#print sorted(authorities.items(), key=lambda(k,v): (v,k), reverse=True)[0:10]
