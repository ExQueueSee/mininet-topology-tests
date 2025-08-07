#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time
import threading
import re


#önemli not: bu kodda soru 6 ve 7 için kullanılan iperf scriptinde ağırlıklı olarak yapay zekadan yardım aldım

def create_star_topology():# Star topology, 1 switch, 6 hosts
    
    net = Mininet(switch=OVSSwitch, link=TCLink, controller=None)   #parametre seçim sebepleri
                                                                    #linear_topology.py ile aynı

    def configure_switch(switch):
        switch.cmd('ovs-ofctl add-flow', switch, 'actions=NORMAL')
    
    print("*** Creating central switch")
    s1 = net.addSwitch('s1')
    
    print("*** Creating hosts")
    h1 = net.addHost('h1')  # Web Tier
    h2 = net.addHost('h2')  # Web Tier
    h3 = net.addHost('h3')  # App Tier
    h4 = net.addHost('h4')  # App Tier
    h5 = net.addHost('h5')  # Data Tier
    h6 = net.addHost('h6')  # Data Tier
    
    print("*** Creating links")
    # All host-to-switch links: 75 Mbps, 1ms delay
    net.addLink(h1, s1, bw=75, delay='1ms')
    net.addLink(h2, s1, bw=75, delay='1ms')
    net.addLink(h3, s1, bw=75, delay='1ms')
    net.addLink(h4, s1, bw=75, delay='1ms')
    net.addLink(h5, s1, bw=75, delay='1ms')
    net.addLink(h6, s1, bw=75, delay='1ms')
    
    print("*** Starting network")
    net.start()
    
    print("*** Configuring switch for learning")
    configure_switch(s1)
    
    print("*** Testing connectivity")
    net.pingAll()
    
    #automated concurrent testing for Question 6
    def run_concurrent_iperf_test():
        print("\n*** Starting Concurrent iPerf Test (Question 6)")
        
        # Start iperf servers
        print("Starting iperf servers...")
        net.get('h3').cmd('iperf -s &')
        net.get('h4').cmd('iperf -s &')
        net.get('h5').cmd('iperf -s &')
        net.get('h6').cmd('iperf -s &')
        
        time.sleep(2)  # Wait for servers to start
        
        # Results storage
        results = {}
        
        def run_iperf_client(client_host, server_ip, flow_name):
            result = net.get(client_host).cmd(f'iperf -c {server_ip} -t 30')
            results[flow_name] = result
        
        # Start concurrent clients using threads
        print("Starting concurrent iperf clients for 30 seconds...")
        threads = []
        
        flows = [
            ('h1', '10.0.0.3', 'h1->h3'),
            ('h2', '10.0.0.4', 'h2->h4'),
            ('h3', '10.0.0.5', 'h3->h5'),
            ('h4', '10.0.0.6', 'h4->h6')
        ]
        
        # Start all clients simultaneously
        for client, server_ip, flow_name in flows:
            thread = threading.Thread(target=run_iperf_client, args=(client, server_ip, flow_name))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Parse and display results
        print("\n*** Concurrent iPerf Test Results:")
        total_throughput = 0
        
        for flow_name, result in results.items():
            # Extract bandwidth from iperf output
            bandwidth_match = re.search(r'(\d+\.?\d*)\s+Mbits/sec', result)
            if bandwidth_match:
                bandwidth = float(bandwidth_match.group(1))
                total_throughput += bandwidth
                print(f"{flow_name}: {bandwidth:.1f} Mbits/sec")
            else:
                print(f"{flow_name}: Could not parse result")
        
        print(f"\nTotal Aggregate Throughput: {total_throughput:.1f} Mbits/sec")
        
        # Kill iperf servers
        net.get('h3').cmd('killall iperf')
        net.get('h4').cmd('killall iperf')
        net.get('h5').cmd('killall iperf')
        net.get('h6').cmd('killall iperf')
        
        return total_throughput

    # Add automated concurrent testing for Question 7
    def run_same_server_iperf_test():
        print("\n*** Starting Same Server iPerf Test (Question 7)")
        print("Both application servers (h3, h4) will access the same data server (h5)")
        
        # Start iperf servers
        print("Starting iperf servers...")
        net.get('h3').cmd('iperf -s &')
        net.get('h4').cmd('iperf -s &')
        net.get('h5').cmd('iperf -s &')  # h5 will receive two connections
        
        time.sleep(2)  # Wait for servers to start
        
        # Results storage
        results = {}
        
        def run_iperf_client(client_host, server_ip, flow_name):
            result = net.get(client_host).cmd(f'iperf -c {server_ip} -t 30')
            results[flow_name] = result
        
        # Start concurrent clients using threads
        print("Starting concurrent iperf clients for 30 seconds...")
        threads = []
        
        flows = [
            ('h1', '10.0.0.3', 'h1->h3'),
            ('h2', '10.0.0.4', 'h2->h4'),
            ('h3', '10.0.0.5', 'h3->h5'),
            ('h4', '10.0.0.5', 'h4->h5')  # Both h3 and h4 connect to h5
        ]
        
        # Start all clients simultaneously
        for client, server_ip, flow_name in flows:
            thread = threading.Thread(target=run_iperf_client, args=(client, server_ip, flow_name))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Parse and display results
        print("\n*** Same Server iPerf Test Results:")
        total_throughput = 0
        
        for flow_name, result in results.items():
            # Extract bandwidth from iperf output
            bandwidth_match = re.search(r'(\d+\.?\d*)\s+Mbits/sec', result)
            if bandwidth_match:
                bandwidth = float(bandwidth_match.group(1))
                total_throughput += bandwidth
                print(f"{flow_name}: {bandwidth:.1f} Mbits/sec")
            else:
                print(f"{flow_name}: Could not parse result")
        
        print(f"\nTotal Aggregate Throughput: {total_throughput:.1f} Mbits/sec")
        
        # Kill iperf servers
        net.get('h3').cmd('killall iperf')
        net.get('h4').cmd('killall iperf')
        net.get('h5').cmd('killall iperf')
        
        return total_throughput
    
    # Ask user for Question 6 test
    user_input = input("\nRun automated concurrent iperf test for Question 6? (y/n): ")
    if user_input.lower() == 'y':
        run_concurrent_iperf_test()
    
    # Ask user for Question 7 test
    user_input = input("\nRun same server iperf test for Question 7? (y/n): ")
    if user_input.lower() == 'y':
        run_same_server_iperf_test()
    
    print("\n*** Running CLI")
    CLI(net)
    
    print("*** Stopping network")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_star_topology()