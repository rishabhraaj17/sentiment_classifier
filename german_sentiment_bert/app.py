# -*- coding: utf-8 -*-

import falcon

from german_sentiment_bert.controller.controller import GermanSentimentController, SystemAvailableController, \
    SystemCheckController
from german_sentiment_bert.service.service import GermanSentimentClassifier


def build_api(classification_service):
    app = falcon.App()

    classification_controller = GermanSentimentController(classification_service)

    app.add_route("/api/v1/classify", classification_controller)

    app.add_route("/system_available", SystemAvailableController())
    app.add_route("/system_check", SystemCheckController())

    return app


def build(config):
    classification_service = GermanSentimentClassifier(config)
    return build_api(classification_service)
