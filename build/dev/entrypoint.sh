#!/bin/bash

pip install -e /packages/uilib && \
    pip install -e /packages/pybt  && \
    pip install -e /packages/utils  && \
    pip install -e /packages/simpleworkqueue && \
    pip install -e /packages/aitools


env > /tmp/env
cat /tmp/env /app/config/cron.conf > /tmp/cron.conf
crontab /tmp/cron.conf


/bin/bash
#python /app/app.py

