adduser oars
usermod -aG sudo oars

sudo apt-get update -y && sudo apt-get upgrade -y
sudo ufw allow OpenSSH
sudo ufw enable
# y
sudo apt-get install nginx -y
sudo ufw allow 'Nginx Full'
sudo vim /etc/nginx/snippets/ssl-<YOUR_TLD>.conf
# ssl_certificate /etc/letsencrypt/live/<YOUR_TLD>/fullchain.pem;
# ssl_certificate_key /etc/letsencrypt/live/<YOUR_TLD>/privkey.pem;
sudo vim /etc/nginx/snippets/ssl-params.conf
# ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
# ssl_prefer_server_ciphers on;
# ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
# ssl_ecdh_curve secp384r1;
# ssl_session_cache shared:SSL:10m;
# ssl_session_tickets off;
# ssl_stapling on;
# ssl_stapling_verify on;
# resolver 8.8.8.8 8.8.4.4 valid=300s;
# resolver_timeout 5s;
# add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
# add_header X-Frame-Options DENY;
# add_header X-Content-Type-Options nosniff;
# ssl_dhparam /etc/ssl/certs/dhparam.pem;
sudo vim /etc/nginx/sites-available/default
# paste in default (with changes specific to your configuration)

# ONLY FOR oarsN1...
sudo apt-get install letsencrypt -y
# ASSIGN FLOATING IP FOR <YOUR_TLD> TO THIS SERVER!!!
sudo letsencrypt certonly --webroot -w /var/www/html/ -d <YOUR_TLD> -d www.<YOUR_TLD>
#<your email address>
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
sudo crontab -e
# 30 2 * * 1 /usr/bin/letsencrypt/letsencrypt-auto renew >> /var/log/le-renew.log
# 35 2 * * 1 /bin/systemctl reload nginx

sudo nginx -t
sudo systemctl reload nginx
sudo systemctl restart nginx
