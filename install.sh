#!/bin/sh

git clone https://github.com/jqrsound/EYESY_OS_for_RasPiSound.git /home/patch/Eyesy
cd /home/patch/Eyesy

set -ex

# Add patch user to tty
usermod -a -G tty patch

# Add nodejs Debian package as source.
# Note the need to allow releaseinfo changes. See https://askubuntu.com/questions/989906/explicitly-accept-change-for-ppa-label
curl -sL https://deb.nodesource.com/setup_14.x | sed -e 's/apt-get /apt-get --allow-releaseinfo-change /g' | sudo bash -

# Debian packages
apt install -y python-pygame python-liblo python-alsaaudio python-pip libffi-dev nodejs

# Python packages
pip install psutil cherrypy numpy JACK-Client

# Node packages
cd web/node && npm install && cd ../..

# Move service files into place and make sure perms are set correctly.
chmod 644 systemd/*
cp systemd/* /etc/systemd/system

# Reload services.
systemctl daemon-reload

# Pure Data and PiSound packages
apt-get install -y puredata pisound-ctl amidiauto pisound-ctl-scripts-puredata

# Dependencies and Codecs
chmod 755 install_dependencies.sh 
chmod 755 install_codecs.sh 
./install_dependencies.sh && sudo ./install_codecs.sh

apt autoremove && apt clean

echo "Done! Thank you!"
