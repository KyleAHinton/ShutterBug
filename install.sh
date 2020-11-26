#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "Installing python3"
sudo apt-get install python3 python3-pip -y
sudo pip3 install --upgrade pip

sudo pip install pipenv --force-reinstall

echo "Installing python3-dev"
sudo apt-get install python3-dev -y

echo "Installing mysql"
sudo apt-get install mysql-server -y

echo "Installing npm"
sudo apt-get install npm -y

sudo apt-get upgrade -y

cd ${DIR}

sql="CREATE DATABASE Shutterbug;CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';FLUSH PRIVILEGES;"
sudo mysql -e "$sql"
pipenv run pipenv sync
pipenv run python backend/manage.py migrate

cd shutterbug
sudo rm -r node_modules
sudo npm install

echo "Ready to launch!"

exit