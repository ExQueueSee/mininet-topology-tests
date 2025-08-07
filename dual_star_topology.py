#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

def create_dual_star_topology():
    
    # Dual Star topology with redundant central switches:
    # - Two central switches: s1, s2
    # - Each host connects to both switches
    # - Inter-switch link for better load balancing
    net = Mininet(switch=OVSSwitch, link=TCLink, controller=None) #parametre seçim sebepleri
                                                                    #linear_topology.py ile aynı
    
    def configure_switch(switch):
        switch.cmd('ovs-ofctl add-flow', switch, 'actions=NORMAL')
    
    print("*** Creating redundant central switches")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    
    print("*** Creating hosts")
    h1 = net.addHost('h1')  # Web Tier
    h2 = net.addHost('h2')  # Web Tier
    h3 = net.addHost('h3')  # App Tier
    h4 = net.addHost('h4')  # App Tier
    h5 = net.addHost('h5')  # Data Tier
    h6 = net.addHost('h6')  # Data Tier
    
    print("*** Creating links")
    # All hosts to both switches for redundancy
    hosts = [h1, h2, h3, h4, h5, h6]
    for host in hosts:
        net.addLink(host, s1, bw=75, delay='1ms')
        net.addLink(host, s2, bw=75, delay='1ms')

    # Inter-switch link for better load balancing
    net.addLink(s1, s2, bw=100, delay='2ms')
    
    print("*** Starting network")
    net.start()
    
    print("*** Configuring switches for learning")
    configure_switch(s1)
    configure_switch(s2)
    
    print("*** Testing connectivity")
    net.pingAll()
    
    print("*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_dual_star_topology()