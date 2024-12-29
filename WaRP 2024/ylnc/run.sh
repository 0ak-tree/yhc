#!/bin/bash

# If the server is dead by unintended reason, we have to automatically restart it
while true; do
    if ! pgrep -x "club_server" > /dev/null; then
        echo "Server not running, launching..."
        ./build/club_server &
    fi
    sleep 1
done