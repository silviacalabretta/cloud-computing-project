#!/bin/bash

# USAGE: ./bench_cpu.sh <max_prime_number>
# EXAMPLE: ./bench_cpu.sh 20000

# 1. Check if the user provided a number. If not, default to 20000.
PRIME=${1:-30000}

RESULTS_DIR="/shared/data"
mkdir -p "$RESULTS_DIR"

RESULTS="${RESULTS_DIR}/results_cpu_${PRIME}.log"

echo "Running CPU benchmarks"

echo "Sysbench with max-prime: $PRIME "

# 2. Run the benchmark
# --threads=2 : Uses your 2 CPUs (The PDF didn't have this)
# --time=10   : Runs for 10 seconds (standard default)
sysbench --test=cpu --cpu-max-prime="$PRIME" --threads=2 run | tee -a "$RESULTS"

# echo "Stress-ng basic"

# --cpu 2: Spawns 2 workers to load your 2 cores
# --timeout 60s: Runs for 1 minute
# stress-ng --cpu 2 --cpu-method matrixprod --timeout 60s --metrics-brief | tee -a "$RESULTS"

echo "Complete. Results saved to $RESULTS"