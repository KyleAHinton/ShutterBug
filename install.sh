#!/bin/bash
echo "Installing python3"
sudo apt-get install python3 python3-pip pipenv -y
sudo pip3 install --upgrade pip

echo "Installing python3-dev"
sudo apt-get install python3-dev -y

echo "Installing mysql"
sudo apt-get install mysql-server -y

echo "Installing npm"
sudo apt-get install npm -y

echo "Installing apache2"
sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y

sudo apt-get upgrade

sudo mv ../ShutterBug /var/www/
cd /var/www/ShutterBug
sudo pipenv --python 3.8 sync

cd shutterbug
sudo rm node_modules
sudo npm install
sudo npm run build
sudo cp -r dist/* /var/www/html/

sql="CREATE DATABASE Shutterbug;CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';FLUSH PRIVILEGES;"
sudo mysql -e "$sql"

cd /var/www/ShutterBug
pipenv install
sudo pipenv --python 3.8 install --system --ignore-pipfile --keep-outdated
cd backend
python manage.py migrate

sudo su
conf="<VirtualHost *:80>
 ServerName rebel.shutter-bug.net
 DocumentRoot /var/www/ShutterBug
 WSGIScriptAlias / /var/www/ShutterBug/backend/backend/wsgi.py

 # adjust the following line to match your Python path
 WSGIDaemonProcess rebel.shutter-bug.net processes=2 threads=15 display-name=%{GROUP} python-home=/usr/bin/python3.8
 WSGIProcessGroup rebel.shutter-bug.net

 <directory /var/www/ShutterBug>
   AllowOverride all
   Require all granted
   Options FollowSymlinks
 </directory>

 # Alias /static/ /var/www/vhosts/mysite/static/

 # <Directory /var/www/vhosts/mysite/static>
  # Require all granted
 # </Directory>
</VirtualHost>"

echo "$conf" > /etc/apache2/sites-available/shutterbug.conf
exit