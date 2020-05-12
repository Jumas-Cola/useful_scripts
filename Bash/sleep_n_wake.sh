#!/bin/bash
WAKE_TIME="14:07"

CURRENT_TIME=$(date +%s)
TODAY_WAKE_TIME=$(date +%s -d "today $WAKE_TIME")

if [[ $CURRENT_TIME > $TODAY_WAKE_TIME ]]
then
    sudo rtcwake -m mem -t $(date +%s -d "tomorrow $WAKE_TIME")
else
    sudo rtcwake -m mem -t  $TODAY_WAKE_TIME
fi
