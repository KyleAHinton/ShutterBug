#!/bin/bash
echo "Installing python3"
sudo apt-get install python3 python3-pip pipenv -y

echo "Installing python3-dev"
sudo apt-get install python3-dev -y

echo "Installing git"
sudo apt-get install git -y

echo "Installing mysql"
sudo apt-get install mysql -y

echo "Installing apache2"
sudo apt-get install apache2 libapache2-mod-wsgi-py3 -y

sudo git clone https://github.com/KyleAHinton/ShutterBug.git
sudo mv ShutterBug /var/www/
cd /var/www/ShutterBug
sudo pipenv --python 3.8 install --system



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