#!/usr/bin/env bash

cd /home/pi/tempmon || return

fetch_result=$(git pull --dry-run)

if [[ -n $fetch_result ]]
then
  echo 'New version of tempmon found...updating...'

  git pull
  bash /home/pi/tempmon/setup.sh

  echo 'Done updating tempmon...Enjoy!'
fi
