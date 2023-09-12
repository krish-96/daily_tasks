#!/bin/bash

script_dir='/home/ubuntu/DailyStatus'
cd $script_dir

aws s3 cp s3://daily-status-app-settings/daily_app_settings.py /home/ubuntu/DailyStatus/daily_status_proj/daily_app_settings.py
echo "File copied from S3"
#virtualenv env -p /usr/bin/python3.8


#/usr/bin/python3.10 -m venv venv
echo "Creating Venv"
python3 -m venv venv

# Activate virtual env
echo "Activating Venv"
pwd
source venv/bin/activate
# Install dependencies
echo "Installing the dependencies"
pip install -r requirements.txt

echo "Killing the port 9999 if it's already running!"
kill -9 $(lsof -i:9999)

# Manager commands
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input
#python3 manage.py runserver 0.0.0.0:9999


echo "Running the gunicorn from externat file"
sh config/start.sh
#gunicorn --workers 1 --bind 0.0.0.0:9999 daily_status_proj.wsgi:application
