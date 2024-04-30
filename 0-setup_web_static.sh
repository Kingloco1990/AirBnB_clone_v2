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
sudo ln -s "$target_folder" "$symbolic_link"

# Change ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Append location block to serve content from /data/web_static/current/
if ! grep -qF "location /hbnb_static/" "$file"; then
    sed -i "s|internal;|internal;\n\t}\n\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;|" "$file"
fi

# Restart Nginx to apply the changes
service nginx restart
