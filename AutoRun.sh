#!/bin/sh -e

is_network_alive() {

    /bin/ping -c 2 -w 3 8.8.8.8 2>&1 > /dev/null
    return $?
}

echo "Verifying Network is alive before continuing"

ISALIVE="1"

while [ "$ISALIVE" -ne "0" ]; do

    is_network_alive
    ISALIVE="$?"

    echo "Waiting for network..."
    sleep 3

done

echo "Network is alive, continuing"

cd /home/pi/FehPlexSlideShow 
/usr/bin/python3 /home/pi/FehPlexSlideShow/FehPlexSlideShow.py 2>&1 >> FehPlexSlideShow.log
