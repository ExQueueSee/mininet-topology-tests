#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import OVSSwitch
from mininet.log import setLogLevel
import time
import re
import subprocess


def cleanup_mininet():                              # bunu ekstradan çalıştırmam gerekti, önceden zaten 
                                                    # olan link/interface pair'lar
                                                    # temizlenmediği için hata veriyordu, automate ettim
    print("*** Cleaning up Mininet environment...")
    try:
        subprocess.run(['sudo', 'mn', '-c'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Cleanup failed: {e}")

def parse_iperf_output(output):
    match = re.search(r'([\d\.]+)\s+Mbits/sec', output)
    return float(match.group(1)) if match else 0.0

def run_iperf_pair(net, client, server):
    server_host = net.get(server)
    client_host = net.get(client)

    server_host.cmd('iperf -s -u -D')  # Start iperf server (UDP) in background
    time.sleep(1)
    output = client_host.cmd(f'iperf -u -c {server_host.IP()} -t 30')
    server_host.cmd('kill %iperf')  # Stop iperf server

    bandwidth = parse_iperf_output(output)
    print(f"{client} → {server}: {bandwidth:.2f} Mbits/sec")
    return bandwidth

def stress_test(net):
    print("\n=== Test A: Balanced Load Across Leaves ===")
    group_a = ['h1', 'h3', 'h5']
    group_b = ['h4', 'h6', 'h2']
    total_a = 0.0

    for host in group_b:
        net.get(host).cmd('iperf -s -u -D')
    time.sleep(1)

    for client, server in [('h1', 'h4'), ('h3', 'h6'), ('h5', 'h2')]:
        total_a += run_iperf_pair(net, client, server)

    for host in group_b:
        net.get(host).cmd('kill %iperf')

    print(f"→ Total Aggregate Throughput (Test A): {total_a:.2f} Mbits/sec")

    print("\n=== Test B: Bottleneck on Single Leaf (leaf1) ===")
    total_b = 0.0
    for host in ['h5', 'h6']:
        net.get(host).cmd('iperf -s -u -D')
    time.sleep(1)

    for client, server in [('h1', 'h5'), ('h2', 'h6')]:
        total_b += run_iperf_pair(net, client, server)

    for host in ['h5', 'h6']:
        net.get(host).cmd('kill %iperf')

    print(f"→ Total Aggregate Throughput (Test B): {total_b:.2f} Mbits/sec")

def build_topology():
    # Define custom switch class with STP enabled
    class STPSwitch(OVSSwitch):
        def __init__(self, name, **params):
            super().__init__(name, stp=True, failMode='standalone', **params)

    net = Mininet(link=TCLink, switch=STPSwitch, controller=None)

    # Spine and Leaf switches
    spines = [net.addSwitch('spine1'), net.addSwitch('spine2')]
    leaves = [net.addSwitch(f'leaf{i}') for i in range(1, 4)]

    # Hosts
    h = {f'h{i}': net.addHost(f'h{i}') for i in range(1, 7)}
    h['h_loadgen'] = net.addHost('h_loadgen')

    # Connect each leaf to both spines (full mesh)
    for leaf in leaves:
        for spine in spines:
            net.addLink(leaf, spine, bw=100, delay='2ms')

    # Host-to-leaf connections (75 Mbps, 1ms delay)
    net.addLink(h['h1'], leaves[0], bw=75, delay='1ms')
    net.addLink(h['h2'], leaves[0], bw=75, delay='1ms')
    net.addLink(h['h_loadgen'], leaves[0], bw=75, delay='1ms')
    net.addLink(h['h3'], leaves[1], bw=75, delay='1ms')
    net.addLink(h['h4'], leaves[1], bw=75, delay='1ms')
    net.addLink(h['h5'], leaves[2], bw=75, delay='1ms')
    net.addLink(h['h6'], leaves[2], bw=75, delay='1ms')

    net.start()
    print("*** Waiting for STP to converge...")
    time.sleep(15)

    print("*** Testing connectivity")
    net.pingAll()

    print("*** Running stress test...")
    stress_test(net)

    net.stop()

if __name__ == '__main__':
    cleanup_mininet()
    setLogLevel('info')
    build_topology()
