#!/bin/sh
mysql -u root -p -e 'DROP DATABASE IF EXISTS readage;'
mysql -u root -p -e 'CREATE DATABASE readage CHARACTER SET utf8;'
python manage.py syncdb --noinput
