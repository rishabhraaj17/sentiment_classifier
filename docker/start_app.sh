#!/usr/bin/env bash
cd /opt/app/
gunicorn --timeout 0 --workers 1 --bind=0.0.0.0:8000 --reload "app:server()"
