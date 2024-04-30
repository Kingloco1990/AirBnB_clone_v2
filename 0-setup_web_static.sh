#!/usr/bin/env bash
# This script sets up an Nginx server with custom configurations and content.

# Check if Nginx is installed
if ! command -v nginx &> /dev/null
then
    echo "Nginx is not installed. Installing..."
    # Update package lists
    sudo apt-get update
    # Install Nginx
    sudo apt-get install -y nginx
fi

# Create necessary directories for web_static
sudo mkdir -p "/data/web_static/releases/test/"
sudo mkdir -p "/data/web_static/shared/"

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
target_folder="/data/web_static/releases/test/"
symbolic_link="/data/web_static/current"
if [ -L "$symbolic_link" ]; then
    rm "$symbolic_link" # If symbolic link exists, delete it
fi
ln -s "$target_folder" "$symbolic_link"

# Change ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Set up default index page
echo 'Hello World!' > /var/www/html/index.html

# Create directory for custom error page
sudo mkdir -p /var/www/error

# Create custom 404 page
echo "Ceci n'est pas une page" > /var/www/error/custom_404.html

# Modify Nginx configuration to redirect '/redirect_me' to a YouTube video
file="/etc/nginx/sites-available/default"
sed -i "s/location \/ {/location \/redirect_me {/; s/try_files \$uri \$uri\/ =404;/return 301 https:\/\/www.youtube.com\/watch?v=QH2-TGUlwu4;/" "$file"

# Define the content to append
# The content variable stores the text to be appended to the configuration file.
content='\\n\terror_page 404 /custom_404.html;\n\tlocation = /custom_404.html {\n\t\troot /var/www/error;\n\t\tinternal;\n\t}'

# Use sed to append the content after the specified text in every location block in the file
# Check if the specified text "error_page 404" is already present in the configuration file.
# If not found, use sed to append the content variable after the closing brace of each location block in the file.
if ! grep -qF "error_page 404" "$file"; then
    sed '/^\s\+}/a'"$content" "$file"
fi

# Add a custom HTTP header with hostname as value
if ! grep -qF "add_header X-Served-By" "$file"; then
    sed -i "s/root \/var\/www\/html;/root \/var\/www\/html;\n\n\tadd_header X-Served-By $HOSTNAME;/" "$file"
fi

# Append location block to serve content from /data/web_static/current/
if ! grep -qF "location /hbnb_static/" "$file"; then
    sed -i "s|internal;|internal;\n\t}\n\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;|" "$file"
fi

# Restart Nginx to apply the changes
service nginx restart
