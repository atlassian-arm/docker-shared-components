#!/bin/bash

# -------------------------------------------------------------------------------------
# Heap collector for containerized Atlassian applications
# 
# This script can be run via `docker exec` to easily trigger the collection of a heap
# dump from the containerized application. For example:
#
#     $ docker exec -it my_jira /opt/atlassian/support/heap-dump.sh
#
# -------------------------------------------------------------------------------------


set -euo pipefail


SCRIPT_DIR=$(dirname "$0")
source "${SCRIPT_DIR}/common.sh"

OUT_FILE="${APP_HOME}/heap.bin"

echo "Atlassian heap dump collector"
echo "App:       ${APP_NAME}"
echo "Run user:  ${RUN_USER}"
echo

if [[ -f "${OUT_FILE}" ]]; then
    echo "A previous heap dump already exists at ${OUT_FILE}."
    if [[ ! -t 1 ]]; then
        echo "This script must be run interactively to overwrite an existing heap dump"
        echo "If running in docker, use the '-it' flag to run scripts in interactive mode:"
        echo
        echo "    $ docker exec -it my_container ${0}"
        exit
    fi
    echo "Overwrite it and continue? (y/n)"
    read ANSWER
    if [[ ${ANSWER} =~ ^[Yy] ]]; then
        echo "Removing previous heap dump file"
        rm "${OUT_FILE}"
    else
        echo "Exiting"
    fi
fi

echo "Generating heap dump"

su jira -c "jcmd ${APP_PID} GC.heap_dump -all ${OUT_FILE}"

echo
echo "Heap dump has been written to ${OUT_FILE}"