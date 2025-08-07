# Mininet Network Topology Project

A collection of network topology implementations using Mininet for network simulation and performance testing.

## Overview

This project contains various network topologies implemented in Python using the Mininet network emulator. Each topology is designed to simulate different network architectures and test their performance characteristics.

## Topologies Included

### 1. Linear Topology (`linear_topology.py`)
- 3 switches connected in a linear chain
- 6 hosts distributed across switches (Web, App, Data tiers)
- Switch-to-switch links: 100 Mbps, 2ms delay
- Host-to-switch links: 75 Mbps, 1ms delay

### 2. Star Topology (`star_topology.py`)
- Single central switch with 6 hosts
- Includes automated concurrent iPerf testing
- Tests both balanced and same-server load scenarios
- All links: 75 Mbps, 1ms delay

### 3. Dual Star Topology (`dual_star_topology.py`)
- Two central switches for redundancy
- Each host connects to both switches
- Inter-switch link for load balancing
- Enhanced fault tolerance

### 4. Ring Topology (`ring_topology.py`)
- 6 switches in a ring configuration
- Chordal redundant links for improved connectivity
- Spanning Tree Protocol (STP) enabled
- One host per switch

### 5. Spine-Leaf Topology (`spine_leaf_topology.py`)
- Modern data center architecture
- 2 spine switches, 3 leaf switches
- Full mesh between spine and leaf layers
- Hosts distributed across leaf switches by tier

## Performance Testing

### Stress Test (`stress_test.py`)
Automated performance testing suite that includes:
- **Test A**: Balanced load across different leaf switches
- **Test B**: Bottleneck testing on single leaf switch
- Built-in Mininet cleanup functionality
- iPerf-based throughput measurements

## Requirements

- Python 3
- Mininet
- Open vSwitch (OVS)
- iPerf (for performance testing)

## Installation

1. Install Mininet:
```bash
sudo apt-get install mininet
```

2. Install iPerf:
```bash
sudo apt-get install iperf
```

## Usage

Run any topology with:
```bash
sudo python3 <topology_file>.py
```

For example:
```bash
sudo python3 star_topology.py
sudo python3 spine_leaf_topology.py
sudo python3 stress_test.py
```

## Features

- **Bandwidth Control**: Configurable link speeds using TCLink
- **Latency Simulation**: Realistic network delays
- **STP Support**: Spanning Tree Protocol for loop prevention
- **Automated Testing**: Built-in performance benchmarks
- **Multi-tier Architecture**: Web, Application, and Data tier separation

## Network Parameters

- **Inter-switch links**: 100 Mbps, 2ms delay
- **Host-to-switch links**: 75 Mbps, 1ms delay
- **STP convergence time**: 15-20 seconds for complex topologies

## Testing

The project includes comprehensive testing capabilities:
- Connectivity testing with `pingAll()`
- Concurrent traffic generation
- Throughput measurement and analysis
- Bottleneck identification

## Architecture Details

### Host Distribution
- **Web Tier**: h1, h2 (frontend servers)
- **App Tier**: h3, h4 (application servers)
- **Data Tier**: h5, h6 (database servers)

### Switch Configuration
- All switches operate in standalone mode (learning switch)
- STP enabled for topologies with redundant links
- OpenFlow rules configured for NORMAL forwarding

## License

This project is part of an academic network simulation study.