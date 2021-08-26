#!/bin/bash

# Wait for the specified process ID to terminate. NOTE: This waits
# indefinitely, but may be killed by higher-level processes
# (e.g. Docker/Kubernetes)

set -e

APP_PID=$1

while [[ -e /proc/${APP_PID} ]]; do
    /bin/sleep 0.5
done
