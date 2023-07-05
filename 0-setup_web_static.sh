#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

set -e  # Exit immediately if a command exits with a non-zero status

if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu /data/
sudo chgrp -R ubuntu /data/

nginx_config="/etc/nginx/sites-available/default"
nginx_config_backup="/etc/nginx/sites-available/default.bak"

# Backup the existing nginx configuration
if [ -f "$nginx_config" ]; then
    sudo cp "$nginx_config" "$nginx_config_backup"
fi

# Generate the new nginx configuration
sudo printf '%s\n' 'server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

location /hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}' | sudo tee "$nginx_config" > /dev/null

sudo service nginx restart
