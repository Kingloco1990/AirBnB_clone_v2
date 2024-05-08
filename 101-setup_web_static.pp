# This script sets up an Nginx server with custom configurations and content using Puppet.

exec { 'apt-get-update':
    command => '/usr/bin/apt-get update',
}

package { 'nginx':
    ensure  => installed,
    require => Exec['apt-get-update'],
}

exec { 'create_directories':
    command => '/usr/bin/mkdir -p "/data/web_static/releases/test/" "/data/web_static/shared/"',
    require => Package['nginx'],
}

exec { 'index.html':
    command => '/usr/bin/echo "Nginx configuration test" | sudo tee /data/web_static/releases/test/index.html >/dev/null',
    require => Package['nginx'],
}

exec { 'symbolic link':
    command => '/usr/bin/ln -s /data/web_static/releases/test/ /data/web_static/current',
    require => Package['nginx'],
}

exec { 'ownership':
    command => '/usr/bin/chown -R ubuntu:ubuntu /data/',
    require => Package['nginx'],
}

exec { 'hbnb_static':
    command => 'sudo sed -i "61i \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default'
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

service { 'nginx':
    ensure  => running,
    require => Package['nginx'],
}
