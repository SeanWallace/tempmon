#!/usr/bin/env bash

sudo apt update
sudo apt install -y python3 python3-pip git

pip3 install -r requirements.txt

ln -f -s "$(pwd)/init/tempmon.service" /etc/systemd/system/tempmon.service
systemctl daemon-reload
systemctl enable tempmon.service
systemctl restart tempmon.service

ln -f -s "$(pwd)/cron/tempmon.sh" /etc/cron.hourly/tempmon
