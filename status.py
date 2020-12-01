from scapy.all import *

def isOnline(ip):
    print("sending packets to check if host is online....")
    noResponse = 0 ;
    for x in range(4):
        icmp = IP(dst=ip)/ICMP()
        resp = sr1(icmp,timeout=5)
        if resp == None:
            noResponse+=1
    if(noResponse==4):
        return "The host is not online"
    else:
        return f'The host is  online\nResponse received for {4-noResponse} packets...'

def tcpPortStatus(ip,port):
    tcp = IP(dst=ip)/TCP(sport=RandShort(),dport=port,flags='S')
    response = sr1(tcp,timeout=3,verbose=0)
    if response!=None:
        print(response.getlayer(TCP).flags);
        if(response.haslayer(TCP) and response.getlayer(TCP).flags=='SA'):
            return 'TCP port is opened'
        elif(response.haslayer(TCP) and response.getlayer(TCP).flags=='AR'):
            return 'TCP port is closed'
        else:
            return 'TCP port is filtered'
    else:
        return 'port is filtered'

def udpPortStatus(ip,port):
    udp= IP(dst=ip)/UDP(sport=RandShort(),dport=port)
    for x in range(3):
        udpResponse = sr1(udp,timeout=10,verbose=0)
        if udpResponse!=None:
            if (udpResponse.haslayer(UDP)):
                return 'UDP port is opened'
            elif(udpResponse.haslayer(ICMP)):
                if(int(udpResponse.getlayer(ICMP).type)==3 and int(udpResponse.getlayer(ICMP).code)==3):
                    return 'UDP port is closed'
                elif(int(udpResponse.getlayer(ICMP).type)==3 and int(udpResponse.getlayer(ICMP).code) in [1,2,9,10,13]):
                    return 'UDP port is filtered'
        else:
            return 'UDP port is filtered'
