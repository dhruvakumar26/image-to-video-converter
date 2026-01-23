#!/bin/bash
set -e
# This script installs MariaDB (lightweight alternative to MS SQL) for demo purposes.
# If you need MSSQL, follow Microsoft's official instructions for mssql-server.
sudo apt update && sudo apt upgrade -y
sudo apt install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb
echo "Run: sudo mysql_secure_installation to set root password and secure DB."
