#!/bin/bash
# orchestrator : This starts and stops orchestrator daemon
#
# chkconfig: 12345 12 88
# description: orchestrator
# processname: orchestrator
# pidfile: /var/run/orchestrator.pid

# Source function library.

. /etc/rc.d/init.d/functions

CURR="$( cd "$( dirname "$( readlink -f ${BASH_SOURCE[0]} )" )" && pwd )"
ORCHESTRATOR_DIR=/var/env-orchestrator/lib/python2.6/site-packages/iotp-orchestrator
pname="orchestrator"
user="orchestrator"

#exe="/usr/bin/python ./manage.py runserver 0.0.0.0:8084 --settings=settings.dev"
exe="uwsgi --http :8084 --chdir $ORCHESTRATOR_DIR --wsgi-file wsgi.py  --env DJANGO_SETTINGS_MODULE=settings.dev"

server="$exe"

pidfile="/var/run/orchestrator.pid"

RETVAL=0

start() {
    echo -n "Starting $pname : "
    #daemon ${exe} # Not working ...
    if [ -s ${pidfile} ]; then
       RETVAL=1
       echo -n "Already running !" && warning
    else
        touch $pidfile
        chown $user $pidfile
        su -s /bin/sh $user -c "
                cd $ORCHESTRATOR_DIR
                exec setsid ${server}   \
                </dev/null >/dev/null 2>&1 &
                echo \$! >${pidfile}
                disown \$!
                "
        PID=`cat $pidfile`
        [ $PID ] && success || failure
    fi
    echo
}

stop() {
    echo -n "Shutting down $pname : "
    if [ -f $pidfile ]; then
        PID=`cat $pidfile`
        kill $PID
        RETVAL=$?
        [ $RETVAL -eq 0 ] && success || failure
        rm -f $pidfile
    else
        echo -n "Not running" && failure
    fi
    echo
}

restart() {
    echo -n "Restarting $pname : "
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
        status ${pname}
    ;;
    restart)
        restart
    ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
    ;; esac

exit 0
