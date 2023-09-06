#!/bin/bash

script_dir='/home/ubuntu/DailyStatus'
cd $script_dir

aws s3 cp s3://daily-status-app-settings/daily_app_settings.py /home/ubuntu/DailyStatus/daily_status_proj/daily_app_settings.py
echo "File copied from S3"
#virtualenv env -p /usr/bin/python3.8

/usr/bin/python3 -m venv venv

# Activate virtual env
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Manager commands
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0.0.0.0:9999

