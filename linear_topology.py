#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

# kod içindeki "learning switch" ile ilgili kısımlar tamamen yapay zekanın ürünüdür.
# büyük miktarda debugging için gptden yararlanmam gerekti

def create_linear_topology(): # Linear topology, 3 switches, 6 hosts
    
    # Create network with TCLink for bandwidth/delay control, no controller (standalone mode)
    net = Mininet(switch=OVSSwitch, link=TCLink, controller=None)   #sudo mn --test pingall yapıldığında
                                                                    #openflow controller not found olduğundan 
                                                                    #controller=None olarak ayarlandı
                                                                    #ayrıca "falling back to ovsswitch" uyarısı alındığı
                                                                    #için switch=OVSSwitch olarak ayarlandı
    
    # Configure switches to work in standalone mode (learning switch)
    def configure_switch(switch):
        switch.cmd('ovs-ofctl add-flow', switch, 'actions=NORMAL')
    
    print("*** Creating switches")
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2') 
    s3 = net.addSwitch('s3')
    
    print("*** Creating hosts")
    # Web Tier
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    # App Tier  
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    # Data Tier
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    
    print("*** Creating links")
    # Switch-to-switch links: 100 Mbps, 2ms delay
    net.addLink(s1, s2, bw=100, delay='2ms')
    net.addLink(s2, s3, bw=100, delay='2ms')
    
    # Host-to-switch links: 75 Mbps, 1ms delay
    # Web Tier to s1
    net.addLink(h1, s1, bw=75, delay='1ms')
    net.addLink(h2, s1, bw=75, delay='1ms')
    # App Tier to s2
    net.addLink(h3, s2, bw=75, delay='1ms') 
    net.addLink(h4, s2, bw=75, delay='1ms')
    # Data Tier to s3
    net.addLink(h5, s3, bw=75, delay='1ms')
    net.addLink(h6, s3, bw=75, delay='1ms')
    
    print("*** Starting network")
    net.start()
    
    print("*** Configuring switches for learning")
    # Configure all switches to act as learning switches
    for switch in net.switches:
        configure_switch(switch)
    
    print("*** Testing connectivity")
    net.pingAll()
    
    print("*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_linear_topology()