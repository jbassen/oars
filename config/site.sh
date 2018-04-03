# Copyright (c) 2017 Jonathan Bassen, Stanford University

adduser oars
usermod -aG sudo oars
cd /etc/ssl/
# signed certificate with /etc/ssl/oars.crt, /etc/ssl/oars.key, /etc/ssl/oars.pem


sudo apt-get update -y && sudo apt-get upgrade -y
sudo ufw allow OpenSSH
sudo ufw allow proto tcp from <PRIV_LOAD_BALANCER_IP> to any port 4430
sudo ufw enable
# y

# sudo ufw status numbered
# sudo ufw delete [N]

sudo apt-get install python3-pip -y
pip3 install virtualenv
virtualenv site_env
source site_env/bin/activate
pip3 install tornado
pip3 install motor

git clone <OARS_REPO_URL>
# username
# password

git config credential.helper store

# git pull

mkdir -p /home/oars/logs/Site/
touch /home/oars/logs/Site/acc.log
touch /home/oars/logs/Site/app.log
touch /home/oars/logs/Site/gen.log

sudo mkdir /usr/lib/systemd/system/
sudo vim /usr/lib/systemd/system/site.service
# copy over file

# systemd-escape "string with non-alphanumeric characters, but without quotes"

sudo chmod 644 /usr/lib/systemd/system/site.service

sudo systemctl daemon-reload
sudo systemctl restart site
sudo systemctl status site
# make oars start on boot
sudo systemctl enable site

#Note: Always run systemctl daemon-reload after changing any of the systemd configuration files.
