#!/bin/bash

apt-get install -y iptables
apt-get install -y iptables-persistent
apt-get install -y inotify-tools
iptables -I INPUT 1 -p tcp --dport 22 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 21 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 8000 -j ACCEPT
iptables -I INPUT 1 -p tcp --dport 443 -j ACCEPT
iptables -I INPUT 1 -p tcp -s 149.154.167.220 -j ACCEPT
service netfilter-persistent save
cp config/main.py /bin/
cp config/scr.sh /usr/local/bin/
cp config/on-boot-script.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable on-boot-script.service
docker-compose build
docker-compose up -d
service on-boot-script start
