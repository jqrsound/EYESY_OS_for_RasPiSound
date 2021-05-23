#!/bin/sh

git clone https://github.com/jqrsound/EYESY_OS_for_RasPiSound.git /home/patch/Eyesy
cd /home/patch/Eyesy

set -ex

# Add patch user to tty
sudo usermod -a -G tty patch

# Add nodejs Debian package as source.
# Note the need to allow releaseinfo changes. See https://askubuntu.com/questions/989906/explicitly-accept-change-for-ppa-label
curl -sL https://deb.nodesource.com/setup_14.x | sed -e 's/apt-get /apt-get --allow-releaseinfo-change /g' | sudo bash -

# Debian packages
sudo apt install -y python-pygame python-liblo python-alsaaudio python-pip libffi-dev nodejs

# Python packages
sudo pip install psutil cherrypy numpy JACK-Client

# Node packages
cd web/node && npm install && cd ../..

# Move service files into place and make sure perms are set correctly.
sudo chmod 644 systemd/*
sudo cp systemd/* /etc/systemd/system

# Reload services.
sudo systemctl daemon-reload

# Pure Data and PiSound packages
sudo apt-get install -y puredata pisound-ctl amidiauto pisound-ctl-scripts-puredata

# Dependencies and Codecs
chmod 755 install_dependencies.sh 
chmod 755 install_codecs.sh 
sudo ./install_dependencies.sh && sudo ./install_codecs.sh
sudo mv *.sh shellscript

sudo apt autoremove && sudo apt clean

echo "Done! Thank you!"
