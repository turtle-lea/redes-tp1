from __future__ import print_function
from __future__ import division

from collections import Counter

import heapq
import sys

nodes = Counter()
edges = {}

for times, src, dst in [line.split() for line in sys.stdin]:
    nodes += {src: times, dst: times}
    edges[src, dst] = int(times)

print ('digraph G {')

import ipdb
ipdb.set_trace()

used_nodes = {node for _, node in heapq.nlargest(50, ((nodes[i], i) for i in nodes))}

for node in used_nodes:
    print ('\tnode [label="{0}"] "{0}"'.format(node))

print('')

for src, dst in edges:
    if src in used_nodes and dst in used_nodes:
        print ('\t"{}" -> "{}" [penwidth={}]'.format(src, dst, edges[src, dst] / 50))

print('}')

