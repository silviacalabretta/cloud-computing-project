#!/bin/bash

# USAGE: ./bench_mem.sh <block_size> <total_size>
# EXAMPLE: ./bench_mem.sh 1M 20G

# 1. Set defaults if no arguments provided (1MB block, 10GB total)
BLOCK_SIZE=${1:-1M}
TOTAL_SIZE=${2:-4G}

RESULTS_DIR="/shared/data"
mkdir -p "$RESULTS_DIR"

RESULTS="${RESULTS_DIR}/results_mem_${BLOCK_SIZE}_${TOTAL_SIZE}.log"

echo "Running Memory benchmarks"

echo "Sysbench with Block=$BLOCK_SIZE, Total=$TOTAL_SIZE"

# 2. Run the benchmark
# Note: We use 1 thread for memory usually, but you can try 2 if you want to saturate the bus.
# For now, we stick to the PDF style which implies default threads (1).
sysbench --test=memory --threads=2 --memory-block-size=$BLOCK_SIZE --memory-total-size=$TOTAL_SIZE run | tee -a "$RESULTS"

# echo "Stress-ng on 2 workers for 1 min (load 500M)"

# stress-ng --vm 2 --vm-bytes 500M --vm-method zero-one --timeout 30s --metrics-brief | tee -a "$RESULTS"

echo "Complete. Results saved to $RESULTS"