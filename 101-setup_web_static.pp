# Sets up an Nginx server with custom configurations and content using Puppet.

# Ensure the Nginx package is installed
package { 'nginx':
    ensure => installed,
}

# Create necessary directories for web_static
file { '/data/web_static/releases/test/':
    ensure => directory,
    require => Package['nginx'],
}

file { '/data/web_static/shared/':
    ensure => directory,
    require => Package['nginx'],
}

# Create and write content to the HTML file
file { '/data/web_static/releases/test/index.html':
    ensure  => file,
    content => @("EOF"),
      <!DOCTYPE html>
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
      </html>
      EOF
    require => File['/data/web_static/releases/test/'],
}

# Create symbolic link for web_static
file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test/',
    require => File['/data/web_static/releases/test/'],
}

# Ensure the /data/ folder and its contents are owned by the ubuntu user and group
file { '/data/':
    ensure  => directory,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    recurse => true,
    require => File['/data/web_static/releases/test/'],
}

# Define a variable for the Nginx configuration file
$nginx_conf_file = '/etc/nginx/sites-available/default'

# Ensure the Nginx configuration file exists before running the exec resource
file { $nginx_conf_file:
    ensure => file,
}

# Exec resource to append the location block if it doesn't already exist
exec { 'append_hbnb_static_location':
    command => "sed -i '61i \\n\tlocation /hbnb_static/ {\\n\\t\\talias /data/web_static/current/;\\n\\t}' ${nginx_conf_file}",
    unless  => "grep -qF 'location /hbnb_static' ${nginx_conf_file}",
    require => File[$nginx_conf_file],
}

# Ensure the Nginx service is restarted to apply the changes
service { 'nginx':
    ensure    => running,
    subscribe => Exec['append_hbnb_static_location'],
}
