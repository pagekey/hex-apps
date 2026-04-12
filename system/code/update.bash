#!/bin/bash

systemctl start hexbox-updater
sleep 5
journalctl -u hexbox-updater -b -n 50
