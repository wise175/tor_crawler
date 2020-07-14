#!/bin/bash

TOR_PASS=""
CONTROL_PORT="9051"
HASH=""

while [[ "$#" -gt 0 ]]
  do
    case $1 in
      -p|--port-control)
        TOR_PASS=$2
        ;;
      -w|--password)
        CONTROL_PORT=$2
        ;;
    esac
    shift
  done

# Tor Install
sudo apt-get update
sudo apt-get --yes --force-yes install tor
sudo systemctl restart tor.service

# Config port control
HASH=$(tor --hash-password $TOR_PASS)
sed -i '57a\ControlPort $CONTROL_PORT\' /etc/tor/torrc
sed -i '60a\HashedControlPassword $HASH\' /etc/tor/torrc
sed -i '61a\CookieAuthentication 1\' /etc/tor/torrc

# Restart service
sudo systemctl restart tor.service

echo "TOR configurado con Puerto de Control: $CONTROL_PORT y HASH: $HASH"