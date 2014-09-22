import sys
from collections import Counter

def enviados_por_ip(name):
    with open(name) as my_file:
        body = my_file.readlines()

    for i in range(len(body)):
        body[i] = body[i].split()

    sent_by_ip = Counter()
    received_by_ip = Counter()

    for entry in body:
        sent_by_ip.update({entry[1]:int(entry[0])})
        received_by_ip.update({entry[2]:int(entry[0])})

    print sum(received_by_ip.values())
	


if __name__ == '__main__':
	enviados_por_ip(sys.argv[1])
