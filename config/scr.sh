#!/bin/bash

until [ -n "$(docker ps --format 'table {{.ID}}\t{{.Names}}' | grep ftppot)" ]
do
sleep 10
done

echo '' > /tmp/list
echo $(docker inspect —format='{{.LogPath}}' $(docker ps -aqf "name=sshpot")) » /tmp/list
echo $(docker inspect —format='{{.LogPath}}' $(docker ps -aqf "name=ftppot")) » /tmp/list
echo $(docker inspect —format='{{.LogPath}}' $(docker ps -aqf "name=webpot")) » /tmp/list

inotifywait -e modify -m —fromfile /tmp/list |\
(
while read
do
python3 /bin/main.py
done
)
