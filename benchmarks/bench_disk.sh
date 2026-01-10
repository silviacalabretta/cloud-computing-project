#!/bin/bash

# USAGE: ./bench_disk.sh <node_name>
# EXAMPLE: ./bench_disk.sh master
# EXAMPLE: ./bench_disk.sh node01

NODE_NAME="${1:-machine}"

RESULTS_DIR="/shared/data"
mkdir -p "$RESULTS_DIR"

RESULTS="${RESULTS_DIR}/results_disk_${NODE_NAME}.log"
LOCAL_FILE="/tmp/iozone_local.tmp"
SHARED_MOUNT="/shared/home"
SHARED_FILE="$SHARED_MOUNT/iozone_shared_${NODE_NAME}.tmp"

echo "Running IOZone Disk benchmark for: ${NODE_NAME}"

echo "IOZone local filesystem test"

iozone -a -I -s 102400 -r 1024 -f "$LOCAL_FILE" 2>&1 | tee -a "$RESULTS"

# Cleanup the temp file
rm -f "$LOCAL_FILE"


if [[ -d "$SHARED_MOUNT" ]]; then
  echo "IOZone shared filesystem test"
  iozone -a -I -s 102400 -r 1024 -f "$SHARED_FILE" 2>&1 | tee -a "$RESULTS"
  rm -f "$SHARED_FILE"
else
  echo "No shared filesystem found at $SHARED_MOUNT. Skipping shared tests."
fi

echo "Complete. Results saved to $RESULTS"
