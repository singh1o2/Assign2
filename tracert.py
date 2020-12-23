from scapy.all import *

def tracert(hostname):#returns number of hops between device and host over maiimum of 30 hops else return 0
    hops = 0
    for x in range(1, 30):
        pkt = IP(dst=hostname, ttl=x) / ICMP()
        reply = sr1(pkt,timeout=5,verbose =0,retry=2)
        if reply is None:
            print(f'Timeout for {x}')
            continue
        elif reply[ICMP].type == 0:
            print (f'DESTINATION {reply.src} reached in {x} hops')
            hops = x
            break
        else:
            print (f'{reply.src} is {x}  hops away')
    return hops
