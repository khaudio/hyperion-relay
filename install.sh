#!/bin/sh

apt update &&
apt install python3-rpi.gpio pyserial

./install_hyperion.sh
service hyperion stop

cp ./default_on /etc/hyperion.config.json
service hyperion start
