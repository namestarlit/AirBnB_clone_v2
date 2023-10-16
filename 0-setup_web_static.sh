#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# Check if running as root user
if [[ $EUID -ne 0 ]]; then
    echo "Please run this script as root or using sudo."
    exit 1
fi

# Install Nginx if not installed
if ! dpkg -s nginx &> /dev/null; then
    apt-get update
    apt-get install -y nginx
fi

# Create nginx directories if they don't exist
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled
mkdir -p /var/www/html
mkdir -p /var/www/bak

# Backup index.nginx-debian.html
if [ -f /var/www/html/index.nginx-debian.html ]; then
    mv /var/www/html/index.nginx-debian.html /var/www/bak/
    echo "Backed up index.nginx-debian.html to /var/www/bak/"
fi

# Create data directories and files.
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
ln -sf /data/web_static/releases/test/ /data/web_static/current
echo "web_static works!" | tee /data/web_static/releases/test/index.html
chown -R ubuntu:ubuntu /data/

# Update nginx configuration
cat <<EOF > /etc/nginx/sites-available/default
server {
  listen 80;
  listen [::]:80;

  server_name default_server;
  add_header X-Served-By \$hostname;

  root /var/www/html;
  index index.htm index.html;

  location / {
    try_files \$uri \$uri/ =404;
  }

  location /hbnb_static {
    alias /data/web_static/current/;
    index index.htm index.html;
  }

  location /redirect_me {
    return 301 'https://www.youtube.com/watch?v=axlUv9evU2k';
  }

  # Redirect error page
  error_page 404 /404.html;
}
EOF

# Create a symlink to enable the site if it doesn't exist
if [ ! -L /etc/nginx/sites-enabled/default ]; then
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
fi

# Restart Nginx service
service nginx restart
