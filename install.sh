#!/usr/bin/env bash

mkdir temp bin data apps
chmod 777 temp
(echo -e "$(date -u) Pervisor installation started.") >> $PWD/data/log.txt
echo PATH="$PATH:/home/$USER/.local/bin:$PWD/bin" | sudo tee /etc/environment
echo PERVISOR="$PWD" | sudo tee -a /etc/environment
source /etc/environment
sudo DEBIAN_FRONTEND=noninteractive apt full-upgrade -yq
sudo DEBIAN_FRONTEND=noninteractive apt install -y git docker.io docker-compose build-essential python3-dev python3-pip python3-venv tmux cron iputils-ping net-tools unzip
sudo usermod -aG docker $USER
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install pandas -q

cd $PERVISOR
rm -rf temp
mkdir temp
(echo -e "$(date -u) Pervisor system is installed.") >> $PWD/data/log.txt
sudo reboot
