#!/bin/bash
systemctl stop galnetbot.service

mkdir -p /etc/galnetbot

cp ./galnetbot.py /etc/galnetbot/
touch /etc/galnetbot/known_articles.log
cp ./.env /etc/galnetbot/

chmod +x /etc/galnetbot/galnetbot.py
cp ./*.service /etc/systemd/system/
#cp ./*.timer /etc/systemd/system/

systemctl daemon-reload

systemctl start galnetbot.service
systemctl enable galnetbot.service
