#!/usr/bin/env bash

DIR="${BASH_SOURCE%/*}"

tar -cf ${DIR}/app.tar ${DIR}/../german_sentiment_bert \
                       ${DIR}/../config \
                       ${DIR}/../app.py \
                       ${DIR}/../log.py
