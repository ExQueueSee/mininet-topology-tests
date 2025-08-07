#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_ring_topology():
    
    # Create a custom switch class that enables STP
    # 6 switches, 6 hosts
    # chordal links for redundancy
    # one host per switch
    # STP enabled to block redundant links
    class STPSwitch(OVSSwitch):
        def __init__(self, name, **kwargs):
            super().__init__(name, stp=True, failMode='standalone', **kwargs)
    
    net = Mininet(switch=STPSwitch, link=TCLink, controller=None)
    
    print("*** Creating switches")
    switches = []
    for i in range(1, 7):
        switch = net.addSwitch(f's{i}')
        switches.append(switch)
    
    print("*** Creating hosts")
    hosts = []
    for i in range(1, 7):
        host = net.addHost(f'h{i}')
        hosts.append(host)
    
    print("*** Creating links")
    
    # Host-to-switch links: 75 Mbps, 1ms delay
    for i in range(6):
        net.addLink(hosts[i], switches[i], bw=75, delay='1ms')
    
    # Primary ring links: 100 Mbps, 2ms delay
    # s1-s2, s2-s3, s3-s4, s4-s5, s5-s6, s6-s1
    ring_connections = [(0,1), (1,2), (2,3), (3,4), (4,5), (5,0)]
    for i, j in ring_connections:
        net.addLink(switches[i], switches[j], bw=100, delay='2ms')
    
    # Chordal redundant links: 100 Mbps, 2ms delay
    # s1-s4, s2-s5, s3-s6
    chordal_connections = [(0,3), (1,4), (2,5)]
    for i, j in chordal_connections:
        net.addLink(switches[i], switches[j], bw=100, delay='2ms')
    
    print("*** Starting network")
    net.start()
    
    # Wait for STP to converge
    print("*** Waiting for Spanning Tree Protocol to converge...")
    import time
    time.sleep(15)  # STP needs time to block redundant links
    
    print("*** Testing connectivity")
    net.pingAll()
    
    print("*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_ring_topology()