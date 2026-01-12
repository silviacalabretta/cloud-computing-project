#!/bin/bash

# USAGE: ./bench_cpu.sh <max_prime_number>
# EXAMPLE: ./bench_cpu.sh 20000

PRIME=${1:-30000}

RESULTS_DIR="/shared/data"
mkdir -p "$RESULTS_DIR"

RESULTS="${RESULTS_DIR}/results_cpu_${PRIME}.log"

echo "Running CPU benchmarks"

echo "Sysbench with max-prime: $PRIME "

sysbench --test=cpu --cpu-max-prime="$PRIME" --threads=2 run 2>&1 | tee -a "$RESULTS"

# echo "Stress-ng basic"

# stress-ng --cpu 2 --cpu-method matrixprod --timeout 60s --metrics-brief | tee -a "$RESULTS"

echo "Complete. Results saved to $RESULTS"