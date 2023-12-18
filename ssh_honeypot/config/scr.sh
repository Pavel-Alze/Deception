#!/bin/bash
sleep 5
inotifywait -e modify -m -r $(docker inspect --format='{{.LogPath}}' $(docker ps -aqf "name=ssh_honeypot_ssh"))|\
(
while read
do
python3 /bin/main.py
done
)
