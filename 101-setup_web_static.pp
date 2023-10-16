# Puppet manifest to set up web servers for web_static deployment

# Install Nginx if not installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { [
  '/data',
  '/data/web_static',
  '/data/web_static/releases',
  '/data/web_static/shared',
  '/data/web_static/releases/test',
]:
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Create a fake HTML file for testing
file { '/data/web_static/releases/test/index.html':
  content => 'web_static test',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create or recreate the symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  notify => Service['nginx'],
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  ensure  => file,
  content => "
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
",
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
  ensure => 'running',
  enable => true,
}
