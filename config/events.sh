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

# if you make mistakes...
# sudo ufw status numbered
# sudo ufw delete [N]

sudo apt-get install python3-pip -y
pip3 install virtualenv
virtualenv events_env
source events_env/bin/activate
pip3 install tornado
pip3 install motor

git clone <OARS_REPO_URL>
# username
# password
git pull

mkdir -p /home/oars/logs/Events/
touch /home/oars/logs/Events/acc.log
touch /home/oars/logs/Events/app.log
touch /home/oars/logs/Events/gen.log

sudo mkdir /usr/lib/systemd/system/
sudo vim /usr/lib/systemd/system/event.service
# copy over file

# systemd-escape "string with non-alphanumeric characters, but without quotes"

sudo chmod 644 /usr/lib/systemd/system/event.service

sudo systemctl daemon-reload
sudo systemctl restart event
sudo systemctl status event
# make oars start on boot
sudo systemctl enable event

#Note: Always run systemctl daemon-reload after changing any of the systemd configuration files.
