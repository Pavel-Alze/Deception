#!/bin/bash

apt-get install -y iptables
apt-get install -y iptables-persistent
apt-get install -y inotify-tools
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
iptables -A INPUT -p tcp -s 149.154.167.220 -j ACCEPT
service netfilter-persistent save
cp config/main.py /bin/mai.py
cp config/scr.sh /usr/local/bin/scr.sh
cp config/on-boot-script.service /etc/systemd/system/on-boot-script.service
systemctl daemon-reload
systemctl enable on-boot-script.service
docker-compose build
docker-compose up -d
service on-boot-script start
