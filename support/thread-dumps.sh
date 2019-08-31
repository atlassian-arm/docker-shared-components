#!/bin/bash

# -------------------------------------------------------------------------------------
# Thread dumps collector for containerized Atlassian applications
# 
# This script can be run via `docker exec` to easily trigger the collection of thread
# dumps from the containerized application. For example:
#
#     $ docker exec my_jira /opt/atlassian/support/thread-dumps.sh
#
# By default this script will collect 10 thread dumps at a 5 second interval. This can
# be overridden by passing a custom value for the count and interval, respectively. For
# example, to collect 20 thread dumps at a 3 second interval:
#
#     $ docker exec my_jira /opt/atlassian/support/thread-dumps.sh 20 3
#
# Note: output from top run in 'Thread-mode' is also captured with each thread dump
# -------------------------------------------------------------------------------------


set -euo pipefail

COUNT=${1:-10}
INTERVAL=${2:-5}

SCRIPT_DIR=$(dirname "$0")
source "${SCRIPT_DIR}/common.sh"

OUT_DIR="${APP_HOME}/thread_dumps_$(date +'%Y-%m-%d_%H-%M-%S')"
mkdir $OUT_DIR

echo "Atlassian thread dump collector"
echo "App:       ${APP_NAME}"
echo "Run user:  ${RUN_USER}"
echo
echo "${COUNT} thread dumps will be generated at a ${INTERVAL} second interval"
echo "top 'Threads-mode' output will also be collected for ${APP_NAME} with every thread dump"
echo

for i in $(seq ${COUNT}); do
    echo "Generating thread dump ${i} of ${COUNT}"
    top -b -H -p $APP_PID -n 1 > ${OUT_DIR}/${APP_NAME}_CPU_USAGE.`date +%s`.txt
    su ${RUN_USER} -c "jcmd ${APP_PID} Thread.print" > ${OUT_DIR}/${APP_NAME}_THREADS.`date +%s`.txt
    sleep ${INTERVAL}
done

echo
echo "Thread dumps have been written to ${OUT_DIR}"