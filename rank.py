#!/usr/bin/env python

import networkx as nx
import csv
import sys
import re
from imdb_api import ImdbAPI
from pprint import pprint as pp

def unicode_csv_reader(unicode_csv_data, **kwargs):
  csv_reader = csv.reader(unicode_csv_data, **kwargs)
  for row in csv_reader:
    yield [unicode(cell, 'utf-8').encode('utf-8') for cell in row]

def top(g, nodes, n = 250):
  top = sorted(nodes.items(), key=lambda(k,v): (v,k), reverse=True)[0:n]
  imdb = ImdbAPI()
  i = 1
  for (node, score) in top:
    g.node[node]['rank'] = i
    g.node[node]['score'] = score
    for (k,v) in imdb.find_imdb(node).items():
      g.node[node][k] = v

    i += 1
    imdb.save()

  return top

def read_graph(f):
  g = nx.DiGraph()
  for row in unicode_csv_reader(open(f, 'r'), delimiter='|'):
    for connection in row[1:]:
      g.add_edge(row[0], connection)
  return g


def write_graph(g, out = sys.stdout, max_edge_distance=-1):
  out.write("""
digraph imdb {
rankdir=RL;
ranksep=.5;
size="36,36";
node  [style=filled];
node  [size="30,30", fontsize = 18];
graph [ label = "\\n\\nIMDB movie links\\n", ssize = "30,60" ];
""")

  # ranking
  for (y, nodes) in group_nodes(g.nodes()).items():
    out.write("{ rank = same;")
    for n in (n for n in nodes if g.degree(n) > 0):
      out.write(q(n)+';')
    out.write("}\n")

  # add URLs
  for n in (n for n in g.nodes() if g.degree(n) > 0):
    attrs = {}
    if g.node[n]['imdb_id']:
      attrs['URL'] = 'http://imdb.com/title/tt%s/movieconnections' % g.node[n]['imdb_id']
    if 'top_250_rank' in g.node[n]:
      attrs['style'] = 'bold'
      attrs['penwidth'] = 4
    attrs['tooltip'] = "%s Rank: %s IMDB top 250: %s Plot: %s" % (n, g.node[n]['rank'],
                               g.node[n]['top_250_rank'] if 'top_250_rank' in g.node[n] else "N/A",
                               g.node[n]['plot_outline'])


    if is_tv_series(n):
      attrs['shape'] = 'octagon'

    out.write(q(n))
    out.write(' [')
    for (k,v) in attrs.items(): out.write('%s=%s' % (k, q(v)))
    out.write('];\n')

  # edges
  for (s,t) in g.edges():
    out.write('%s -> %s;\n' % (q(s), q(t)))

  out.write("}\n")

def is_tv_series(node):
  return '"' in node

def get_decade(node):
  match = re.search(r'\((\d{4})(?:/I)?\)', node)
  if match:
    year = int(match.group(1))
    return year - (year % 10)
  else:
    sys.stderr.write(node)
    return None

def group_nodes(nodes):
  grouped = {}
  for n in nodes:
    decade = get_decade(n)
    if not decade in grouped:
      grouped[decade] = []

    grouped[decade].append(n)
  return grouped

def sub_graph(g, n, algorithm = nx.pagerank):
  return g.subgraph([v[0] for v in top(g, algorithm(g), n)])

def remove_long_edges(g, max_edge_distance):
  if max_edge_distance > 0:
    for (s,t) in g.edges():
      distance = get_decade(s) - get_decade(t)
      if distance > max_edge_distance:
        g.remove_edge(s,t)

  return g

def q(s):
  return '"%s"' %  str(s).replace('"', '\\"')

if __name__ == "__main__":
  if len(sys.argv) < 3:
    print __file__, "<file> [--graph|--rank|--hits|--degree] [--max=<n>]"
    sys.exit(1)

  n = 100
  max_edge_distance = -1
  for arg in sys.argv:
    m = re.match(r'--max=(\d+)', arg)
    if m: n = int(m.group(1))

    m = re.match(r'--max-edge-distance=(\d+)', arg)
    if m: max_edge_distance = int(m.group(1))

  g = read_graph(sys.argv[1])
  if '--graph' in sys.argv:
    sub = sub_graph(g, n)
    write_graph(remove_long_edges(sub, max_edge_distance))
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
