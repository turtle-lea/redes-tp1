from __future__ import print_function
from __future__ import division

from collections import Counter
import argparse
import sys

parser = argparse.ArgumentParser(description='Transform a list of tuples (weight, src, dst) into a .dot file of the graph')
parser.add_argument('-n', '--nodes', type=int, default=30, help='The X nodes with the most weight will be used')
parser.add_argument('-d', '--divisor', type=float, default=30, help='The weight of each edge in the dotfile will be the actual weight divided by this number')
args = parser.parse_args()

nodes = Counter()
edges = {}

for times, src, dst in [line.split() for line in sys.stdin]:
    times = int(times)
    nodes.update({src: times, dst: times})
    edges[src, dst] = int(times)

print ('digraph G {')

# Remove nodes that aren't in the top X
nodes = {node for node, _ in nodes.most_common(args.nodes)}

for node in nodes:
    print ('\tnode [label="{0}"] "{0}"'.format(node))

print('')

for src, dst in edges:
    if src in nodes and dst in nodes:
        print ('\t"{}" -> "{}" [penwidth={}]'.format(src, dst, edges[src, dst] / args.divisor))

print('}')

