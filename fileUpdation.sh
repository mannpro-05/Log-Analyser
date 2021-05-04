#!/bin/bash/

cp /var/log/safesquid/extended/*.log /root/Log-Analyser/logs
python3 updateDatabase.py
cd logs
rm *.log
