#!/bin/bash


# cd /app/scripts; python pull_pg_files.py

env > /tmp/env
cat /tmp/env /app/config/cron.conf > /tmp/cron.conf
crontab /tmp/cron.conf

service cron start

#/bin/bash
python /app/app.py