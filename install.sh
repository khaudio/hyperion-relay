#!/bin/sh

apt update
apt install python3-rpi.gpio pyserial

curl -k -L --output install_hyperion.sh --get https://raw.githubusercontent.com/hyperion-project/hyperion/master/bin/install_hyperion.sh

chmod +x install_hyperion.sh
sh ./install_hyperion.sh

service hyperion stop

cp ./hyperion.config.json /etc/hyperion/

chmod +x ./hyperion-relay
cp ./hyperion-relay /etc/hyperion/

cat >> /etc/systemd/system/hyperion-relay.service << EOF
[Unit]
Description=hyperion-relay

[Service]
ExecStart=/etc/hyperion/hyperion-relay.py
StandardOutput=tty
StandardError=syslog

[Install]
WantedBy=default.target
EOF

systemctl daemon-reload

service hyperion start
service hyperion-relay start
