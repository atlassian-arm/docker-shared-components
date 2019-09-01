# -------------------------------------------------------------------------------------
# Common bootstrapping for support scripts (get app details: home directory, PID, etc.)
# -------------------------------------------------------------------------------------

# Set up app info
APP_NAME="$(set | grep "_INSTALL_DIR" | awk -F'_' '{print $1}')"
APP_HOME_VAR="${APP_NAME}_HOME"
APP_HOME="${!APP_HOME_VAR}"

APP_PID=$(${JAVA_HOME}/bin/jcmd | grep "org.apache.catalina.startup.Bootstrap" | awk '{print $1}')