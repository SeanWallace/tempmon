#!/usr/bin/env bash

set -ex

apt update
apt install -y python3 python3-pip git libgpiod2

mkdir -p /etc/tempmon
cp config/config.template.json /etc/tempmon

pip3 install -r requirements.txt

ln -f -s "$(pwd)/init/tempmon.service" /etc/systemd/system/tempmon.service
systemctl daemon-reload
systemctl enable tempmon.service
systemctl restart tempmon.service

ln -f -s "$(pwd)/cron/tempmon.sh" /etc/cron.hourly/tempmon

echo 'Install complete. Make sure to put a config file at /etc/tempmon/config.json.'
