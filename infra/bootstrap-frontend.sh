#!/bin/bash
set -e
sudo apt update && sudo apt upgrade -y
# Install Node.js (18)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs build-essential nginx
sudo mkdir -p /var/www/img2vid
sudo chown $USER:$USER /var/www/img2vid
sudo systemctl enable nginx
sudo systemctl start nginx
echo "Frontend bootstrap done"
