#!/usr/bin/env bash

docker run -d -p 8000:8000 --name classifier german.sentiment.classifier sh /opt/start_app.sh

