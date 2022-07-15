#!/bin/bash
secret_key=1238sdfn12 # Please set your own secret_key
host=sendungsregister.test		# Please set your domain sendungsregister will be available
user=user			# enter your linux username			
group=www-data			# www-data is the apache group. you don't need to edit this


sudo apt-get update
sudo apt-get install git python3 python3-dev python3-ldap python3-pip ldap-utils libldap2-dev libsasl2-dev apache2 redis pipenv libapache2-mod-wsgi-py3 -y
cd  /var/www/
git clone https://github.com/mohnbroetchen2/sendungsregister.git
cd sendungsregister
virtualenv ./
source bin/activate 
pip install -r requirements.txt
sed -e 's/%SECRET_KEY%/'$secret_key'/' \     
    -e 's/%HOST%/'$host'/'< sendungsregister/local_settings.py.template > sendungsregister/local_settings.py
python manage.py collectstatic 
python manage.py makemigrations 
python manage.py migrate
chmod 664 /var/www/sendungsregister/db/db.sqlite3 
chmod g+w /var/www/sendungsregister/db
cd /var/www/
chown $user:$group sendungsregister -R
rm /etc/apache2/sites-enabled/000-default.conf
cp /var/www/sendungsregister/apache_conf.template /etc/apache2/sites-available/sendungsregister.conf
ln -s /etc/apache2/sites-available/sendungsregister.conf /etc/apache2/sites-enabled/sendungsregister.conf
service apache2 restart
