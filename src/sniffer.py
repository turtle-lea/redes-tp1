#! /usr/bin/python
from scapy.all import *
from collections import Counter

pairs = Counter()

def arp_monitor_callback(pkt):
    global pairs

    ARP = scapy.all.ARP

    if (ARP in pkt) and (pkt[ARP].op is 1):
        src = pkt[ARP].psrc
        dst = pkt[ARP].pdst

        sys.stderr.write('ARP {} -> {}\n'.format(src, dst))
        pairs.update({(src, dst): 1})

    sniff(prn=arp_monitor_callback, store=0, count=1)