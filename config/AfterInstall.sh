#!/bin/bash

script_dir='/home/ubuntu/DailyStatus'
cd $script_dir


#virtualenv env -p /usr/bin/python3.8

/usr/bin/python3.8 -m venv venv

# Activate virtual env
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Manager commands
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0.0.0.0:9999

