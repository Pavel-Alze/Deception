#!/bin/bash

until [ -n "$(docker ps --format 'table {{.ID}}\t{{.Names}}' | grep sshpot)" ]
do
sleep 10
done

inotifywait -e modify -m -r $(docker inspect --format='{{.LogPath}}' $(docker ps -aqf "name=sshpot"))|\
(
while read
do
python3 /bin/main.py
done
)
