# Puppet manifest to set up an Nginx server with custom configurations and content

exec { 'apt-get-update':
    command => '/usr/bin/apt-get update',
}

package { 'nginx':
    ensure  => installed,
    require => Exec['apt-get-update'],
}

# Create necessary directories for web_static
file { '/data/web_static/releases/test/':
    ensure => directory,
}

file { '/data/web_static/shared/':
    ensure => directory,
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
    command => 'chown -R ubuntu:ubuntu /data/',
    path    => ['/bin', '/usr/bin'],
    require => [File['/data/web_static/releases/test/'], File['/data/web_static/shared/']],
}

exec { 'hbnb_static':
    command => 'sed -i "61i \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-enabled/default',
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

exec { 'nginx_restart':
    command => 'service nginx restart',
    path    => ['/bin', '/usr/bin'],
    require => Exec['hbnb_static'],
}
