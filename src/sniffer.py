#! /usr/bin/python
import scapy.all

ipVecesEnSrc  = {}
ipVecesEnDst  = {}
ipIntercambio = {}

def arp_monitor_callback(pkt):

	ARP = scapy.all.ARP

	if (ARP in pkt) and (pkt[ARP].op is 1):
		#Is who-has
		src = pkt[ARP].psrc
		dst = pkt[ARP].pdst

		# If no value is defined return cero add one and set
		ipVecesEnSrc[src] = ipVecesEnSrc.get(src, 0.0) + 1.0
		ipVecesEnDst[dst] = ipVecesEnDst.get(dst, 0.0) + 1.0
		ipIntercambio[src,dst] = ipIntercambio.get((src,dst), 0.0) + 1.0

		print "\nNuevos Resultados"
		print ipVecesEnSrc
		print ipVecesEnDst
		print ipIntercambio

scapy.all.sniff(prn=arp_monitor_callback, filter="arp", store=0)

