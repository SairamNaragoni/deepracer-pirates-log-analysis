#!/bin/bash

LOG_DIR=/home/ubuntu/deepracer-pirates-log-analysis/Logs/current
rm $LOG_DIR/*
for name in `docker ps --format "{{.Names}}"`; do
    docker logs ${name} >& $LOG_DIR/${name}.log
done
