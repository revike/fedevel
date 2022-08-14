#!/bin/sh

python3 fedevel/manage.py migrate
#python3 fedevel/manage.py create_superuser
python3 fedevel/manage.py create_categories
python3 fedevel/manage.py create_products
python3 fedevel/manage.py collectstatic --noinput
sleep 5
python3 fedevel/manage.py runserver 0.0.0.0:8000
