#!/bin/bash

python3 /path/to/src/discovery/discover.py &
DISCOVERY_PID=$!

# wait for discover
sleep 5

python3 /path/to/src/leader-election/elections.py &
ELECTION_PID=$!

# If this is a joystick Pi, start the joystick controller
if [ -e "/dev/input/js0" ]; then
    sleep 5
    python3 /path/to/src/joystick-communication/joystick.py &
    JOYSTICK_PID=$!
fi

# wait for procs
wait $DISCOVERY_PID $ELECTION_PID $JOYSTICK_PID