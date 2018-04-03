# Copyright (c) 2017 Jonathan Bassen, Stanford University

adduser oars
usermod -aG sudo oars
cd /etc/ssl/
# store signed certificate to /etc/ssl/oars.pem

sudo apt-get update -y && sudo apt-get upgrade -y
sudo ufw allow OpenSSH
sudo ufw enable
# y

# if you make mistakes...
# sudo ufw status numbered
# sudo ufw delete [N]

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo vim /etc/systemd/system/mongodb.service
# [Unit]
# Description=High-performance, schema-free document-oriented database
# After=network.target
#
# [Service]
# User=oars
# ExecStart=/usr/bin/mongod --quiet --config /etc/mongod.conf
# Restart=on-failure
#
# [Install]
# WantedBy=multi-user.target

mkdir -p logs/Mongo/
touch logs/Mongo/mongod.log
mkdir -p db/Mongo/mongodb
sudo vim /etc/mongod.conf
# copy mongod.conf to /etc/mongod.conf

sudo systemctl daemon-reload
sudo systemctl start mongodb
sudo systemctl status mongodb
# make mongodb start on boot
sudo systemctl enable mongodb

# repeat the following command with the private address for all other servers:
sudo uft allow proto tcp from <PRIV_ADDR> to any port 27017

# if running a cluster, using the private address for each of the servers:
mongo --ssl
rs.initiate( {_id: "oars", members: [ {_id: 0, host: "<THIS_PRIV_ADDR>:27017"}]} )
rs.add("<OTHER_PRIV_ADDR>:27017")
rs.add("<OTHER_PRIV_ADDR>:27017")
rs.status() # should show all the servers

# create all the different users
use admin
db.createUser({user: "<ROOT_USR>", pwd: "<ROOT_PWD>", roles: [{role: "userAdminAnyDatabase", db: "admin"}] })
db.createUser({user:"<EVENT_USR>", pwd:"<EVENT_PWD>", roles: [{ role: "readWrite", db: "core" }] })
db.createUser({user:"<BKTF_USR>", pwd:"<BKTF_PWD>", roles: [{ role: "read", db: "core" }, {role: "readWrite", db: "bktf"}] })
db.createUser({user:"<SITE_USR>", pwd:"<SITE_PWD>", roles: [{ role: "readWrite", db: "core" }, {role: "read", db: "bktf"}] })

# you can use the following commands to make the other servers slaves
# everything after requires that you're on the primary
# use core
# rs.slaveOk()


# # to create the indexes:
# # between each action, CHECK STATUS ON PRIMARY...
rs.status()
# # FOR EACH SECONDARY...
sudo systemctl stop mongodb
# # change mongod.conf:
sudo vim /etc/mongod.conf
# X   replSetName: oars
#     port: 47017
sudo systemctl start mongodb
mongo --ssl --sslAllowInvalidCertificates --port 47017
use core
db.enrollments.createIndex( {insertstamp: 1} )
db.enrollments.createIndex( {platform: 1, course_name: 1, platform_uid: 1})
db.logs.createIndex( {insertstamp: 1} )
db.logs.createIndex( {timestamp: 1} )
db.logs.createIndex( {platform: 1, course_name: 1, platform_uid: 1, timestamp: 1})
db.course_maps.createIndex( {plarform: 1, course_name: 1} )
use bktf
db.states.createIndex( {insertstamp: 1} )
db.states.createIndex( {platform: 1, course_name: 1, mapping_name: 1, platform_uid: 1} )
# make the following changes in change mongod.conf:
sudo vim /etc/mongod.conf
# port: 27017
# replSetName: oars
sudo systemctl stop mongodb
sudo systemctl start mongodb
# # FOR THE PRIMARY...
rs.stepDown()
# # THEN FOLLOW SAME INSTRUCTIONS AS WITH SECONDARIES
