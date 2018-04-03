Copyright (c) 2017 Jonathan Bassen, Stanford University

OVERVIEW

Welcome to OARS

This version (1.0) consists of five components:
1) Mongo: the OARS database, which stores all raw and derivative learner data
2) Event: the event server, which receives raw learner interaction data from the learning platform
3) Site: the server that users of the OARS system interact with
4) BKTF: a background process that models learner knowledge state, using bayesian knowledge tracing on each learner's first attempts of problems (note: this should be used as an example for deploying any additional models)
5) Loader: a script for uploading and updating course maps (this is a clunky solution, which we hope to replace with a web interface for course developers)

This repository does not include modifications and background services that have been added to the Lagunita platform, to authenticate and send data to OARS.


SYSTEM REQUIREMENTS

All OARS components are designed to run on Ubuntu 16.04x64 with Python 3.6. Earlier versions of Ubuntu have an outdated process manager that's incompatible with our daemon setup. Earlier versions of Python don't support all our library dependencies.

The Event, Site, BKTF and Loader components can be run on a single Ubuntu machine or on separate ubuntu machines. Regardless of how many machines you choose to use, we recommend a minimum of one CPU and 4GB RAM per component.

The Mongo component can be set up as a stand-alone database, or as a master and a slave, or as a robust replica set. Our setup instructions demonstrate how to create a replica set with three replicas (this is the minimum number that can continue to function if one should fail). In accordance with security standards, Mongo should not be hosted on the same machine as the Event and Site components, which are accessible from the greater internet.

The hosting service or computer cluster where OARS is hosted will need a load balancer/reverse proxy (such as NginX) to route requests to the machine(s) and ports that host the Event and Site components. This can be located on the same machine as one or both of the aforementioned components, on a separate server, or may even be provided by your hosting service. We recommend using NginX because of its configurability, and also recommend a minimum of two CPUs and 8GB RAM to this end. If you run NginX on the same machine as one or both of the other components, you may need to limit its RAM usage in its configuration.

Depending on your setup choices (including Mongo replication, component redundancy and machine-to-process allocation) you may end up using anywhere from 2-8+ machines. If you decide to use a virtual hosting service (as we do), you should make sure each machine is set up in the same LAN in the same data center. You should also acquire a private IP for each machine and a public IP for your load balancer/proxy server (unless your hosting service provides that service for you).


SETUP

NOTE: Each of these instruction (.sh) files starts with a user and firewall setup. These redundant commands can be ignored for any components that are hosted on the same machine.

1) Create all the machines you hope to use and note the public and private IPs
2) Set up the load balancer/proxy: described in config/NginX.sh
3) Set up the Mongo component: described in config/mongod.sh
4) Set up the Events component: described in config/events.sh
5) Set up the BKTF service: described in config/bktf.sh
6) Set up the Site service: described in config/site.sh
7) Set up Lagunita to authenticate for OARS and serve events for OARS


DEPENDENCIES

From apt-get:
python3-pip
mongodb-org
nginx
letsencrypt

From pip3:
virtualenv
tornado
motor

From npm:
d3
lodash

Misc:
normalize.css
