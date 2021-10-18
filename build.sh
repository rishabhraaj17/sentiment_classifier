#!/usr/bin/env bash

DIR="${BASH_SOURCE%/*}"

${DIR}/docker/tar_app.sh

docker build \
    --force-rm \
    -t german.sentiment.classifier:latest \
    -f ${DIR}/docker/Dockerfile \
    ${DIR}/docker

rm ${DIR}/docker/app.tar
