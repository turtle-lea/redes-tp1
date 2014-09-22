#! /usr/bin/python
import ast
import numpy
import pydot
import pylab
import re
import argparse
import networkx as nx
from collections import Counter

pylab.clf()

def entropia(dicc):
    #Takes an Dictionary [key,float] and calculates entropy
    N = float(sum(dicc.values()))
    Ps = [ k/N for k in dicc.values() ]
    H = -sum([ p*numpy.log2(p) for p in Ps ])
    return H


def autolabel(rects):
    # attach some text labels
    for rect in rects:
        width = rect.get_width()
        ySize = max(width,1.)

        pylab.text(width*1.05, rect.get_y()+rect.get_height()*0.5, 
                '%.2f'%float(width), va='center')

def guardarHistograma(dicc,campo,archivo):

    ipsOrdenadas = sorted(dicc, key=dicc.get)[-14:]
    totalSumaVal = float(sum(dicc.values()))
    valoresOrden = [ dicc[ip]/totalSumaVal for ip in ipsOrdenadas ] 

    largo = len(ipsOrdenadas)
    yPos  = xrange(-4,(largo-2)*2,2)
    myBar = pylab.barh(yPos, valoresOrden, alpha=0.5,height=1.8,align='center')

    pylab.yticks(yPos, ipsOrdenadas)

    pylab.xlabel('Frecuencia')
    pylab.ylabel('IP')
    pylab.title('IPs en campo ' + campo)

    autolabel(myBar)
    pylab.tight_layout()
    pylab.savefig(archivo,format='pdf',orientation='landscape')
    pylab.clf()

def grafoConectividad(dicc,ruta):
    #Asumo ingresa un dicc con claves (ip1,ip2) y valores int
    #consigo todas las ips
    ips_src = [x for x,y in dicc.keys()]
    ips_dst = [y for x,y in dicc.keys()]
    ips_all = numpy.union1d(ips_src,ips_dst)

    #Armo el grafo con Pydot
    graph = pydot.Dot(graph_type='digraph')
    nodes = [ pydot.Node(ip) for ip in ips_all ]
    edges = [ pydot.Edge(x,y,label=str(int(dicc[x,y])))
                for x,y in dicc.keys() if dicc[x,y] > 0 ]

    for n in nodes:
        graph.add_node(n)
    for e in edges:
        graph.add_edge(e)

    graph.write_pdf(ruta)

    #Ahora en networkX
    graph = nx.Graph()
    
    for x,y in dicc.keys():
        graph.add_edge(x,y)

    pos=nx.spring_layout(graph)

    nx.draw_networkx_nodes(graph,pos,node_size=300,alpha=0.4,label="string")
    
    nx.draw_networkx_edges(graph,pos,alpha=0.4)

    nx.draw_networkx_labels(graph,pos,font_size=10)

    pylab.axis('off')
    pylab.savefig(ruta+"NX",format='pdf')

#----------------------------------------

parser = argparse.ArgumentParser(description='Hace los graficos, histogramas y calcula entropia')
parser.add_argument('-i', '--inputF', type=str, help='El archivo a parsear')
parser.add_argument('-o', '--outputD', type=str, help='El directorio salida')
args = parser.parse_args()

entrada = args.inputF
salida  = args.outputD
ipsSrc = Counter()
ipsDst = Counter()
ipsCon = Counter()

with open(entrada,'r') as archivo:

    for linea in archivo:
	line = linea.split()

	times = 1
	if len(line) == 2:
		src,dst = line
	else:
		times,src,dst = line
	times = int(times)

        ipsSrc[src] += times 
        ipsDst[dst] += times
        ipsCon[src,dst] += times 

esrc = entropia(ipsSrc)
edst = entropia(ipsDst)
guardarHistograma(ipsDst,'DST',salida+"ipsDst_"+str(float(edst)))
guardarHistograma(ipsSrc,'SRC',salida+"ipsSrc_"+str(float(esrc)))
grafoConectividad(ipsCon,salida+"conectividad")


