#!/bin/bash
# Auto Data Cleaner Service Control Script

PID_FILE="/tmp/auto_data_cleaner.pid"
SCRIPT_PATH="/workspaces/sugarglitch-realops/scripts/auto_data_cleaner.py"

start() {
    if [ -f $PID_FILE ]; then
        echo "❌ Auto Data Cleaner is already running (PID: $(cat $PID_FILE))"
        return 1
    fi
    
    echo "🚀 Starting Auto Data Cleaner..."
    nohup python3 $SCRIPT_PATH > /tmp/auto_data_cleaner.log 2>&1 &
    echo $! > $PID_FILE
    echo "✅ Auto Data Cleaner started (PID: $(cat $PID_FILE))"
    echo "📋 Log file: /tmp/auto_data_cleaner.log"
}

stop() {
    if [ ! -f $PID_FILE ]; then
        echo "❌ Auto Data Cleaner is not running"
        return 1
    fi
    
    PID=$(cat $PID_FILE)
    echo "🛑 Stopping Auto Data Cleaner (PID: $PID)..."
    kill $PID
    rm -f $PID_FILE
    echo "✅ Auto Data Cleaner stopped"
}

status() {
    if [ -f $PID_FILE ]; then
        PID=$(cat $PID_FILE)
        if kill -0 $PID 2>/dev/null; then
            echo "✅ Auto Data Cleaner is running (PID: $PID)"
        else
            echo "❌ Auto Data Cleaner is not running (stale PID file)"
            rm -f $PID_FILE
        fi
    else
        echo "❌ Auto Data Cleaner is not running"
    fi
}

logs() {
    if [ -f /tmp/auto_data_cleaner.log ]; then
        tail -f /tmp/auto_data_cleaner.log
    else
        echo "❌ No log file found"
    fi
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        sleep 2
        start
        ;;
    status)
        status
        ;;
    logs)
        logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
