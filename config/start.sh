#!bin/bash
gunicorn --workers 1 --bind 0.0.0.0:9999 daily_status_proj.wsgi:application
