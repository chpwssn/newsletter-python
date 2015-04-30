#!/bin/bash
#An auto update tool
CURLOG=$(cat curlog.txt)
CURLOG=$(($CURLOG + 1))
mv log.txt log.txt.$CURLOG
echo $CURLOG > curlog.txt
touch log.txt
chmod 777 log.txt
echo "Log rotated to .$CURLOG"
git pull
python archive.py
