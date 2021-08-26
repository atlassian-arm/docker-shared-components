#!/bin/bash

# Send the specified signal to the main application process.
#
# If 'wait' is added as a second parameter, wait for the process to
# terminate. NOTE: This waits indefinitely, but may be killed by
# higher-level processes (e.g. Docker/Kubernetes)

set -e

SIG=$1
WAIT=$2
SHDIR=$(dirname $0)

source ${SHDIR}/common.sh

kill -${SIG} ${APP_PID}

if [[ "${WAIT}" != "wait" ]]; then
    exit 0
fi

${SHDIR}/wait-pid.sh
