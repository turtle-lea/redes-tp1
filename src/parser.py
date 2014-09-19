#! /usr/bin/python
import ast
import numpy
import pydot
import pylab
import re
import sys


def entropia(dicc):
	#Takes an Dictionary [key,float] and calculates entropy
    N = sum(dicc.values())
    Ps = [ k/N for k in dicc.values() ]
    H = -sum([ p*numpy.log2(p) for p in Ps ])
    return H


def guardarHistograma(dicc,ruta):
    largo  = len(dicc.keys())
    labels = dicc.keys()
    pylab.xticks(range(largo),labels)
    myHistogram = pylab.histogram(dicc.values(), bins=largo, density=True)
    pylab.show()
    pylab.savefig(ruta,format='pdf')


def grafoConectividad(dicc,ruta):
    #Asumo ingresa un dicc con claves (ip1,ip2) y valores int
    #consigo todas las ips
    ips_src = [x for x,y in dicc.keys()]
    ips_dst = [y for x,y in dicc.keys()]
    ips_all = numpy.union1d(ips_src,ips_dst)

    #creo un nodo por cada ip
    graph = pydot.Dot(graph_type='digraph')
    nodes = [ pydot.Node(ip) for ip in ips_all ]
    edges = [ pydot.Edge(x,y,label=str(int(dicc[x,y])))
                for x,y in dicc.keys() if dicc[x,y] > 0 ]

    for n in nodes:
        graph.add_node(n)
    for e in edges:
        graph.add_edge(e)

    graph.write_pdf(ruta)

entrada = sys.argv[1]
salida  = sys.argv[2]


with open(entrada,'r') as archivo:
    ipsSrc = ast.literal_eval(archivo.readline())
    ipsDst = ast.literal_eval(archivo.readline())
    ipsCon = ast.literal_eval(archivo.readline())

esrc = entropia(ipsSrc)
edst = entropia(ipsDst)
guardarHistograma(ipsSrc,salida+"ipsSrc_"+str(float(esrc)))
guardarHistograma(ipsDst,salida+"ipsDst_"+str(float(edst)))
grafoConectividad(ipsCon,salida+"conectividad")


