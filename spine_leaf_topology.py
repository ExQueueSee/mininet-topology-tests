#!/usr/bin/env python3
# filepath: /home/kingsoul/Desktop/DERSLER/BIL452/project/mininet_project/spine_leaf_topology.py

from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.clean import cleanup


def create_spine_leaf_topology():
    
    # Clean up any previous state
    cleanup()
    
    # Create STP-enabled switch class
    class STPSwitch(OVSKernelSwitch):
        def __init__(self, name, **kwargs):
            super().__init__(name, stp=True, failMode='standalone', **kwargs)
    
    net = Mininet(switch=STPSwitch, link=TCLink, controller=None)
    
    print("*** Creating Spine switches")
    spine1 = net.addSwitch('spine1')
    spine2 = net.addSwitch('spine2')
    spines = [spine1, spine2]
    
    print("*** Creating Leaf switches")
    leaf1 = net.addSwitch('leaf1')
    leaf2 = net.addSwitch('leaf2')
    leaf3 = net.addSwitch('leaf3')
    leaves = [leaf1, leaf2, leaf3]
    
    print("*** Creating hosts")
    # Web Tier hosts -> leaf1
    h1 = net.addHost('h1')
    h2 = net.addHost('h2')
    h_loadgen = net.addHost('h_loadgen')
    
    # App Tier hosts -> leaf2
    h3 = net.addHost('h3')
    h4 = net.addHost('h4')
    
    # Data Tier hosts -> leaf3
    h5 = net.addHost('h5')
    h6 = net.addHost('h6')
    
    print("*** Creating links")
    
    # Spine-Leaf full mesh: Every Leaf to Every Spine
    # 100 Mbps, 2ms delay for spine-leaf links
    for leaf in leaves:
        for spine in spines:
            net.addLink(leaf, spine, bw=100, delay='2ms')
    
    # Host-to-Leaf links: 75 Mbps, 1ms delay
    # Web Tier to leaf1
    net.addLink(h1, leaf1, bw=75, delay='1ms')
    net.addLink(h2, leaf1, bw=75, delay='1ms')
    net.addLink(h_loadgen, leaf1, bw=75, delay='1ms')
    
    # App Tier to leaf2
    net.addLink(h3, leaf2, bw=75, delay='1ms')
    net.addLink(h4, leaf2, bw=75, delay='1ms')
    
    # Data Tier to leaf3
    net.addLink(h5, leaf3, bw=75, delay='1ms')
    net.addLink(h6, leaf3, bw=75, delay='1ms')
    
    print("*** Starting network")
    net.start()
    
    # Wait for STP to converge
    print("*** Waiting for Spanning Tree Protocol to converge...")
    import time
    time.sleep(20)  # STP needs more time in complex topologies
    
    print("*** Testing connectivity")
    net.pingAll()
    
    print("*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_spine_leaf_topology()