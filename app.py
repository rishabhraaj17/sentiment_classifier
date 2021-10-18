# -*- coding: utf-8 -*-

import logging

from hydra import initialize, compose

from german_sentiment_bert.app import build
from log import initialize_logging


def server():
    """
    Run with: gunicorn [OPTIONS] "<filenameWithoutExtension>:server()"
    """
    initialize(config_path="config", job_name="serve_app")
    conf = compose(config_name="config")
    initialize_logging(logging.INFO)
    return build(conf)
