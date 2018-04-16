#!/bin/sh

apt update
apt install python3-rpi.gpio pyserial

git clone https://github.com/arun11299/cpp-subprocess.git

curl -k -L --output install_hyperion.sh --get https://raw.githubusercontent.com/hyperion-project/hyperion/master/bin/install_hyperion.sh
chmod +x install_hyperion.sh
sh ./install_hyperion.sh

service hyperion stop

cp ./hyperion.config.json /etc/hyperion/

cp ./hyperion_relay.py /etc/hyperion/
cp ./relay_off.py /etc/hyperion/
cp ./relay_on.py /etc/hyperion/
chown pi:pi /etc/hyperion/*
chmod +x /etc/hyperion/*.py

cat > /etc/systemd/system/hyperion-relay.service << EOF
[Unit]
Description=hyperion-relay

[Service]
User=pi
Type=simple
ExecStart=/usr/bin/python3 /etc/hyperion/hyperion_relay.py
ExecStop=/usr/bin/python3 /etc/hyperion/relay_off.py
StandardOutput=syslog
StandardError=syslog

[Install]
WantedBy=default.target
After=hyperion.service
EOF

systemctl daemon-reload

service hyperion start
service hyperion-relay start
