# -------------------------------------------------------------------------------------
# Common bootstrapping for support scripts (get app details: home directory, PID, etc.)
# -------------------------------------------------------------------------------------


# Set up Java utils
JCMD="${JAVA_HOME}/bin/jcmd"

# Set up app info
APP_NAME="$(set | grep '_INSTALL_DIR' | awk -F'_' '{print $1}')"
APP_HOME_VAR="${APP_NAME}_HOME"
APP_HOME="${!APP_HOME_VAR}"

# Get app PID
case "${APP_NAME}" in
    BITBUCKET )
        BOOTSTRAP_PROC="com.atlassian.bitbucket.internal.launcher.BitbucketServerLauncher"
        ;;
    * )
        BOOTSTRAP_PROC="org.apache.catalina.startup.Bootstrap"
        ;;
esac

APP_PID=$(${JCMD} | grep "${BOOTSTRAP_PROC}" | awk '{print $1}')
