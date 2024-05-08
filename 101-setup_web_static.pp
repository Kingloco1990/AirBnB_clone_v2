# This script sets up an Nginx server with custom configurations and content using Puppet.

exec { 'apt-get-update':
    command => '/usr/bin/apt-get update',
}

package { 'nginx':
    ensure  => installed,
    require => Exec['apt-get-update'],
}

exec { 'test':
    command => 'sudo mkdir -p /data/web_static/releases/test/',
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

exec { 'shared':
    command => 'sudo mkdir -p /data/web_static/shared/',
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

exec { 'index.html':
    command => 'echo Hi | sudo tee /data/web_static/releases/test/index.html >/dev/null',
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

exec { 'symbolic link':
    command => 'ln -sf /data/web_static/releases/test/ /data/web_static/current',
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

exec { 'ownership':
    command => 'sudo chown -R ubuntu:ubuntu /data/',
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

exec { 'hbnb_static':
    command => 'sed -i "61i \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default'
    path    => ['/usr/bin', '/usr/sbin',],
    require => Package['nginx'],
}

service { 'nginx':
    ensure  => running,
    require => Package['nginx'],
}
