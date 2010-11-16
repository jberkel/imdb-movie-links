#!/usr/bin/env python

import networkx as nx
import csv
import sys
import re
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

def write_graph(g, out = sys.stdout):
  out.write("strict digraph {\n")
  out.write('rankdir=LR; ranksep=.75; size="10,20"; ratio=auto;\n')

  for (y, nodes) in group_nodes(g.nodes()).items():
    out.write("{ rank = same;")
    for n in (n for n in nodes if g.degree(n) > 0):
      out.write(q(n)+';')
    out.write("}\n")

  for (t,s) in g.edges():
    out.write('%s -> %s;\n' % (q(s), q(t)))

  out.write("}\n")


def group_nodes(nodes):
  grouped = {}
  for n in nodes:
    match = re.search(r'\((\d+)\)$', n)
    if match:
      year = int(match.group(1))
      decade = year - (year % 10)
      if not decade in grouped:
        grouped[decade] = []

      grouped[decade].append(n)
  return grouped

def sub_graph(g, n, algorithm = nx.pagerank):
  return g.subgraph([v[0] for v in top(algorithm(g), n)])

def q(s):
  return '"%s"' %  s.replace('"', '\\"')

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print __file__, "<file> [--graph|--rank|--hits|--degree] [--max=<n>]"
    sys.exit(1)

  n = 200
  for arg in sys.argv:
    m = re.match(r'--max=(\d+)', arg)
    if m: n = int(m.group(1))

  g = read_graph(sys.argv[1])
  if '--graph' in sys.argv:
    sub = sub_graph(g, n)
    write_graph(sub)
  elif '--rank' in sys.argv:
    pp(top(nx.pagerank(g)))
  elif '--hits' in sys.argv:
    # HITS
    (hubs, authorities) = nx.hits(g)
    pp(top(hubs, n))
    pp(top(authorities, n))
  elif '--degree' in sys.argv:
    # degree
    pp(top(nx.degree(g), n))


