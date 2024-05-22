# Sets up an Nginx server with custom configurations and content using Puppet.

# Install Nginx if not already installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories for web_static
exec { 'create_web_static_directories':
  command => '/usr/bin/mkdir -p /data/web_static/releases/test/ /data/web_static/shared/',
}

# Create and write content to the HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => '<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Page</title>
</head>
<body>
    <h1>This is a test page</h1>
    <p>Hello, world!</p>
</body>
</html>',
}

# Create symbolic link for web_static
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}

# Change ownership of /data/ folder to ubuntu user and group
exec { 'change_ownership':
  command => '/bin/chown -R ubuntu:ubuntu /data/',
}

# Append location block to Nginx configuration file
exec { 'append_location_block':
  command => 'sed -i "61i \\n\\tlocation \/hbnb_static {\n\\t\\talias /data/web_static/current/;\n\\t}" /etc/nginx/sites-available/default',
  unless  => 'grep -qF "location /hbnb_static" /etc/nginx/sites-available/default',
  provider => shell,
  require  => Package['nginx'],
}

# Restart Nginx service
service { 'nginx':
  ensure    => running,
  subscribe => Exec['append_location_block'],
}
