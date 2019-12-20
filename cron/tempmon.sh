#!/usr/bin/env bash

cd /home/pi/tempmon || return

fetch_result=$(git pull --dry-run)

if [ -z "$fetch_result" ]
then
  git pull
  bash /home/pi/tempmon/setup.sh
fi
