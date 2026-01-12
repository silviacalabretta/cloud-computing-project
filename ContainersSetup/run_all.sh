#!/bin/bash

echo "Starting full cluster benchmark..."

NODES=("master" "node01" "node02")

# CPU & Memory & Disk on each node
for NODE in "${NODES[@]}"; do
  echo "Running CPU benchmark on $NODE"
  docker exec $NODE /root/benchmarks/bench_cpu.sh 30000 $NODE
  echo "CPU benchmarks complete."

  echo "Running Memory benchmark on $NODE"
  docker exec $NODE /root/benchmarks/bench_mem.sh 1M 20G $NODE
  echo "Memory benchmarks complete."

  echo "Running Disk benchmark on $NODE"
  docker exec $NODE /root/benchmarks/bench_disk.sh $NODE
  echo "Disck benchmarks complete."
done

# Network tests

echo "Starting iperf server on master"
docker exec -d master iperf3 -s
sleep 3

echo "Network test: node01 <-> master"
docker exec node01 /root/benchmarks/bench_net.sh master

# Stop iperf server on master
docker exec master pkill iperf3
sleep 2

echo "Starting iperf server on node01"
docker exec -d node01 iperf3 -s
sleep 3

echo "Network test: node02 <-> node01"
docker exec node02 /root/benchmarks/bench_net.sh node01

# Stop iperf server on node01
docker exec node01 pkill iperf3
sleep 2

echo "Network benchmarks complete."

echo "All benchmarks complete."
