#!/bin/bash
cd /home/bcoffice/backend/bcoffice

python3 /home/bcoffice/backend/bcoffice/manage.py migrate --settings=bcoffice.settings.$1

supervisord -n -c /etc/supervisor/conf.d/supervisor-app-$1.conf 
