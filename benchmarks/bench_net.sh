#!/bin/bash

# USAGE: ./bench_net.sh <IP_OF_SERVER_MACHINE>

TARGET_IP="$1"

RESULTS_DIR="/shared/data"
mkdir -p "$RESULTS_DIR"

RESULTS="${RESULTS_DIR}/results_net_vs_${TARGET_IP}.log"

if [[ -n "$TARGET_IP" ]]; then
  echo "Running network benchmark against: $TARGET_IP"

  # 1. Standard Test (Client sending to Server)
  echo "Iperf3: Upload Speed (Current machine -> Server)"
  iperf3 -c "$TARGET_IP" -t 30 2>&1 | tee -a "$RESULTS"

  # 2. Reverse Test (Server sending to Client)
  echo "Iperf3: Download Speed (Server -> Current machine)"
  # The -R flag reverses the direction of traffic
  iperf3 -c "$TARGET_IP" -t 30 -R 2>&1 | tee -a "$RESULTS"

  echo "Ping: Latency Test"
  ping -c 50 -i 0.2 "$TARGET_IP" 2>&1 | tee -a "$RESULTS"

  echo "Complete. Results saved to $RESULTS"
else
  echo "Error: No TARGET_IP provided."
  echo "Usage: ./bench_net.sh <IP_ADDRESS_OF_SERVER>"
  exit 1
fi