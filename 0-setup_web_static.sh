#!/usr/bin/env bash
# This script sets up an Nginx server with custom configurations and content.

# Update package lists
sudo apt-get update

# Install Nginx
sudo apt-get install -y nginx

# Create necessary directories for web_static
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create and write content to the HTML file
sudo tee /data/web_static/releases/test/index.html >/dev/null <<EOF
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

# Create symbolic link for web_static
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

sudo wget -q -O /etc/nginx/sites-available/default http://exampleconfig.com/static/raw/nginx/ubuntu20.04/etc/nginx/sites-available/default
config="/etc/nginx/sites-available/default"
echo 'Holberton School Hello World!' | sudo tee /var/www/html/index.html > /dev/null
sudo sed -i '/^}$/i \ \n\tlocation \/redirect_me {return 301 https:\/\/www.youtube.com\/watch?v=QH2-TGUlwu4;}' $config
sudo sed -i '/^}$/i \ \n\tlocation @404 {return 404 "Ceci n'\''est pas une page\\n";}' $config
sudo sed -i 's/=404/@404/g' $config
sudo sed -i "/^server {/a \ \tadd_header X-Served-By $HOSTNAME;" $config
# Append location block to serve content from /data/web_static/current/
sed '61i \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' config1

sudo service nginx restart
