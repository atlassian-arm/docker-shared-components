#!/bin/bash

set -e

SIG=$1
WAIT=$2
SHDIR=$(dirname $0)

source ${SHDIR}/common.sh

kill -$SIG $APP_PID

if [[ "$WAIT" != "wait" ]]; then
    exit 0
fi

while [[ -e /proc/$APP_PID ]]; do
    /bin/sleep 0.5
done
