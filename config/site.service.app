[Unit]
Description=tornado web server


[Service]
User=oars
Group=oars
Restart=on-failure
ExecStart=/home/oars/site_env/bin/python3 /home/oars/code/Site/__main__.py
KillMode=process
PrivateTmp=true
Environment=TORNADO_PORT=<TORNADO_PORT>
Environment=COOKIE_SECRET=<COOKIE_SECRET>
Environment=CERT_FILE=/etc/ssl/oars.crt
Environment=TEMPLATE_PATH=/home/oars/code/Site/templates
Environment=STATIC_PATH=/home/oars/code/Site/static
Environment=LAGUNITA_REDIRECT_URL=<MUST MATCH REDIRECT URL, for example https://www.openoars.org/edx/login>
Environment=LAGUNITA_TOKEN_URL=<MUST MATCH TOKEN URL, for example https://lagunita.stanford.edu/oauth2/access_token>
Environment=LAGUNITA_USER_INFO_URL=<MUST MATCH USER_INFO URL, for example https://lagunita.stanford.edu/oauth2/user_info>
Environment=LAGUNITA_ACCOUNTS_URL=<MUST MATCH ACCOUNTS URL, for example https://lagunita.stanford.edu/api/user/v1/accounts>
Environment=LAGUNITA_ENROLLMENT_URL=<MUST MATCH ENROLLMENT URL, for example https://lagunita.stanford.edu/api/enrollment/v1/enrollment>
Environment=LAGUNITA_ROSTER_URL=<MUST MATCH ROSTER URL, for example https://lagunita.stanford.edu/api/enrollment/v1/roster/>
Environment=LAGUNITA_AUTHORIZE_URL=<MUST MATCH AUTHORIZE URL OF PLATFORM>
Environment=LAGUNITA_CLIENT_ID=<MUST MATCH ID IN LAGUNITA>
Environment=LAGUNITA_CLIENT_SECRET=<MUST MATCH SECRET IN LAGUNITA>
Environment=LAGUNITA_EVENT_KEY=<MUST MATCH KEY IN LAGUNITA>
Environment=LAGUNITA_EVENT_SECRET=<MUST MATCH SECRET IN LAGUNITA>
Environment=KEY_FILE=/etc/ssl/oars.key
Environment=LOG_PATH=/home/oars/logs/Site
Environment=MONGO1_ADDR=<PRIVATE_IP>
Environment=MONGO2_ADDR=<PRIVATE_IP>
Environment=MONGO3_ADDR=<PRIVATE_IP>
Environment=MONGO_PORT=27017
Environment=MONGO_USR=<SITE_USR>
Environment=MONGO_PWD=<SITE_PWD>
Environment=MONGO_RS=oars


[Install]
WantedBy=multi-user.target
