#!/bin/bash

apt-get install -y iptables
apt-get install -y iptables-persistent
apt-get install -y inotify-tools
iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2222
service netfilter-persistent save
cp main.py /bin/
cp scr.sh /usr/local/bin/
cp on-boot-script.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable on-boot-script.service
docker-compose up -d --build
service on-boot-script start
