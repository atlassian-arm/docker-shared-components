# -------------------------------------------------------------------------------------
# Common bootstrapping for support scripts (get app details: home directory, PID, etc.)
# -------------------------------------------------------------------------------------


# Set valid getopt options
function set_valid_options {
    OPTS=$(getopt -o "$1" --long "$2" -n 'parse-options' -- "$@")
    if [ $? != 0 ]; then
        echo "Failed parsing options." >&2
        exit 1
    fi
    eval set -- "$OPTS"
}



# Run command(s)
function run_as_runuser {
    if [ $(id -u) = 0 ]; then
        su "${RUN_USER}" -c '"$@"' -- argv0 "$@"
    else
        $@
    fi
}
