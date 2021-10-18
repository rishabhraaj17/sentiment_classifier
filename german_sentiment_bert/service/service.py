# -*- coding: utf-8 -*-

from typing import List

from germansentiment import SentimentModel
from omegaconf import DictConfig


class GermanSentimentClassifierError(Exception):

    def __init__(self, message):
        super(GermanSentimentClassifierError, self).__init__(message)


class GermanSentimentClassifier(object):
    def __init__(self, config: DictConfig):
        self.config = config
        self.classifier = SentimentModel(model_name=config.classifier.model_name)

    def classify(self, texts: List[str]) -> List[str]:
        return self.classifier.predict_sentiment(texts=texts)
