#!/bin/bash
# orchestrator : This starts and stops orchestrator daemon
#
# chkconfig: 12345 12 88
# description: orchestrator
# processname: orchestrator
# PIDFILE: /var/run/orchestrator.pid

# Source function library.

. /etc/rc.d/init.d/functions

# DEFAULT SETTINGS

CURR="$( cd "$( dirname "$( readlink -f ${BASH_SOURCE[0]} )" )" && pwd )"
VIRTUALENV=/var/env-orchestrator
ORCHESTRATOR_DIR=${VIRTUALENV}/lib/python2.6/site-packages/iotp-orchestrator
UWGSI=/var/env-orchestrator/bin/uwsgi
PORT=8084
STATS_PORT=8085
PROCESSES=2
THREADS=8
ENVIRONMENT="DJANGO_SETTINGS_MODULE=settings.dev"
PIDFILE="/var/run/orchestrator.pid"
PNAME="orchestrator"
USER="orchestrator"


# LOAD CUSTOMIZED SETTINGS
[ -f /etc/default/orchestrator-daemon ] && . /etc/default/orchestrator-daemon

exe="$UWGSI --http :${PORT} \
--chdir $ORCHESTRATOR_DIR \
--wsgi-file wsgi.py \
--env $ENVIRONMENT \
--virtualenv $VIRTUALENV \
--master \
--processes $PROCESSES \
--threads $THREADS \
--enable-threads \
--disable-logging \
--stats localhost:$STATS_PORT"

server="$exe"


RETVAL=0

start() {
    echo -n "Starting ${PNAME}: "


    status -p ${PIDFILE} ${PNAME} &> /dev/null 

    if [[ ${?} -eq 0 ]]; then
        echo "Already running, skipping $(success)"
        return 0
    fi

    touch ${PIDFILE}
    chown ${USER}:${USER} ${PIDFILE}

    su -s /bin/sh ${USER} -c \
    "cd $ORCHESTRATOR_DIR
     . ${VIRTUALENV}/bin/activate
     exec setsid ${server} < /dev/null >/dev/null 2>&1 &
     echo \$! >${PIDFILE}
     disown \$!"

    PID=$(cat ${PIDFILE})
    [ ${PID} ] && success || failure
    echo
}

stop() {
    echo -n "Shutting down $PNAME : "
    if [ -f ${PIDFILE} ]; then
        PID=`cat $PIDFILE`
        kill -9 $PID
        RETVAL=$?
        [ $RETVAL -eq 0 ] && success || failure
        rm -f $PIDFILE
    else
        echo -n "Not running" && success
    fi
echo
}

restart() {
    echo -n "Restarting $PNAME : "
    stop
    sleep 5
    start
}

case "$1" in
    start)
        start
    ;;
    stop)
        stop
    ;;
    status)
        status ${PNAME}
    ;;
    restart)
        restart
    ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
    ;; esac

exit 0
