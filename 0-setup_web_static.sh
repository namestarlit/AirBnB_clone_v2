#!/usr/bin/env bash
# Web server setup for web_static deployment
apt-get update
apt-get -y install nginx

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

echo "<html>
  <head>
  </head>
  <body>
	Holberton School
  </body>
</html>" > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

wb_sttc="listen [::]:80 default_server;\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}"
sed -i "s|listen \[::\]:80 default_server;|$wb_sttc|" /etc/nginx/sites-available/default

service nginx restart
