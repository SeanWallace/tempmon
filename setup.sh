#!/usr/bin/env bash

pip install -r requirements.txt

ln -f -s "$(pwd)/init/tempmon.service" /etc/systemd/system/tempmon.service
systemctl daemon-reload
systemctl enable tempmon.service
systemctl restart tempmon.service

ln -f -s "$(pwd)/cron/tempmon.sh" /etc/cron.hourly/tempmon
