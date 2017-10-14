#!/bin/sh


./install_hyperion.sh
service hyperion stop
#case 'on or off'
cp ./hyperion.config.json_on /etc/hyperion.config.json
#cp ./hyperion.config.json_off /etc/hyperion.config.json
