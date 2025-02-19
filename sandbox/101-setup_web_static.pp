# Puppet manifest to set up web servers for web_static deployment

# Install Nginx if not installed
package { 'nginx':
  ensure => installed,
}

$nginx_conf = "
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
"
# Create nginx directories if they don't exist
file { [
  '/etc/nginx/sites-available',
  '/etc/nginx/sites-enabled',
  '/var/www/html',
]:
  ensure => directory,
}

# Create data directories and files
file { [
  '/data/web_static/releases/test/',
  '/data/web_static/shared/',
]:
  ensure => directory,
  owner  => 'ubuntu'
  group  => 'ubuntu'
}

file { '/data/web_static/releases/test/index.html':
  content => 'web_static works!',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/current':
  ensure  => link,
  target  => '/data/web_static/releases/test/',
  require => File['/data/web_static/releases/test/index.html'],
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Update nginx configuration
file { '/etc/nginx/sites-available/default':
  content => $nginx_conf
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Create a symlink to enable the site if it doesn't exist
file { '/etc/nginx/sites-enabled/default':
  ensure  => link,
  target  => '/etc/nginx/sites-available/default',
  require => File['/etc/nginx/sites-available/default'],
  notify  => Service['nginx'],
}

# Restart Nginx service
service { 'nginx':
  ensure  => 'running',
  enable  => true,
  require => File['/etc/nginx/sites-enabled/default'],
}
