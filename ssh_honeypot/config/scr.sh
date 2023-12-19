#!/bin/bash

until [ -n "$(docker ps --format 'table {{.ID}}\t{{.Names}}' | grep honeypot)" ]
do
sleep 10
done

inotifywait -e modify -m -r $(docker inspect --format='{{.LogPath}}' $(docker ps -aqf "name=honeypot"))|\
(
while read
do
python3 /bin/main.py
done
)
