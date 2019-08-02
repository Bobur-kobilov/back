#!/bin/bash
cd /home/bcoffice/backend/bcoffice

python3 /home/bcoffice/backend/bcoffice/manage.py migrate --settings=bcoffice.settings.production

supervisord -n
