# Cloud Computing Project: VM vs. Container Cluster Comparison

This project evaluates the performance trade-offs between traditional **Virtualization** (VirtualBox) and **Containerization** (Docker/WSL 2) in a clustered environment. By building two identical three-node clusters (1 Master, 2 Workers), we analyze how different abstraction layers impact CPU, memory, disk I/O, and network throughput under high-performance workloads.

## Architecture & Setup
Both environments were provisioned with identical resource constraints to ensure a fair comparison: **2 vCPUs** and **2048 MB RAM** per node.

### 1. Virtual Machine Cluster
* **Hypervisor:** VirtualBox.
* **OS:** Ubuntu 24.04.2 LTS.
* **Networking:** Internal private network with `dnsmasq` providing centralized DNS and DHCP.
* **Storage:** Shared filesystem implemented via NFS (Network File System).

### 2. Container Cluster
* **Engine:** Docker with WSL 2 backend.
* **Orchestration:** Docker Compose.
* **Networking:** Custom bridge network (`cluster-net`) for internal DNS resolution.
* **Storage:** Direct bind mounts using Docker volumes for file sharing.

---

## Performance Benchmarking
We utilized a comprehensive suite of industry-standard tools to stress-test the clusters:
* **CPU:** `sysbench` and `hpcc`.
* **Memory:** `sysbench`.
* **Disk I/O:** `IOZone` (testing both local and shared filesystems).
* **Network:** `iperf3` and `ping` (RTT).

---

## Key Results at a Glance
Our analysis revealed that while CPU tasks perform almost identically, containers hold a massive advantage in communication-heavy and memory-intensive tasks.

| Metric | Virtual Machines (VM) | Containers (Docker) | Performance Gap |
| :--- | :--- | :--- | :--- |
| **Network Throughput** | $\approx 1.5$ Gbits/s  | $45-50$ Gbits/s  | **30x Faster**  |
| **Network Latency (RTT)** | $\approx 1.35$ ms  | $\approx 0.1$ ms  | **13x Lower** |
| **Memory Throughput** | $\approx 30,000$ ops/sec  | $\approx 45,000$ ops/sec  | **50% Higher** |
| **HPCC Stability** | Failed at $N=512$  | Stable at $N=8192$  | **16x Scalability**  |

> **Note:** The 30x network gap highlights the substantial overhead of full virtualization where packets must traverse the hypervisor and virtual switches. Containers benefit from sharing the host kernel and network stack via WSL 2.

---

## Technical Challenges & Stability
A significant portion of this study focuses on the "Stability Gap". 
* **Lock Holder Preemption:** Under extreme load (HPCC), the VM cluster suffered catastrophic failures, including RCU stalls and watchdog timeouts. This occurred because the host scheduler paused vCPUs holding critical kernel locks, causing others to "spin" indefinitely.
* **vCPU Time Drift:** Stress-tests with `stress-ng` caused the VM's internal clock to desynchronize from real-time, rendering performance metrics invalid.

---

## Project Structure

```
.
├── benchmrks_vms/                          # Benchmarking scripts for VMs
├── containers/                             # Docker cluster source code
│   ├── setup/                              # Configuration files
│   │   ├── benchmarks/                     # Test scripts for containers
│   │   ├── Dockerfile                      # Dockerfile
│   │   ├── compose.yaml                    # Docker compose file
│   │   └── start.sh                        # Entry point script
│   └── run_all.sh                          # Shell script to run all tests
├── results/                                # Data and performance graphs
│   ├── data/                               # Raw numbers from the tests
│   └── plots/                              # Visual charts
├── Report.pdf                              # Full tecchnical analysis
└── README.md                               # This overview
```
---

### Reference
For a deep dive into the experimental data and architectural decisions, please refer to the **[Project Report](./Report.pdf)**.
