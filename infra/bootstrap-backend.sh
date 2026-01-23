#!/bin/bash
set -e
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv build-essential ffmpeg nginx unzip
# create app directory
mkdir -p ~/app
cd ~/app
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask gunicorn sqlalchemy pyodbc python-dotenv
echo "Backend bootstrap done"
