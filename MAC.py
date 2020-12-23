from scapy.all import ARP, Ether, srp

def find_ip_mac():#returns all the mac and ip address of all devices connected in LAN
    arp_packet = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.2.1/24")
    result = srp(arp_packet, timeout=4,retry=2)[0]
    devices = []
    for req,res in result:
        devices.append({'ip': res.psrc, 'mac': res.hwsrc})

    str = "\nDevices connected in LAN\n"
    str = str+ 'IP\t\t\tMAC\n'
    for c in devices:
        str = str +'{}\t{}\n'.format(c['mac'],c['ip'])

    return str
