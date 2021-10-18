# -*- coding: utf-8 -*-

import json
import time

import falcon
from falcon import Request, Response

from german_sentiment_bert.controller.constants import ResponseCode
from german_sentiment_bert.service.dtos import ClassificationRequest
from german_sentiment_bert.service.service import GermanSentimentClassifier, GermanSentimentClassifierError
from log import get_logger

logger = get_logger(__name__)


class RESTController(object):
    def __init__(self) -> None:
        pass

    @classmethod
    def log_and_raise(cls, status: str, msg: str) -> None:
        logger.error(f"{msg} (responded with {status})")
        raise falcon.HTTPError(status, description=msg)

    @classmethod
    def get_body(cls, req: Request) -> bytes:
        b: bytes
        if not req.content_length:
            b = req.stream.read()
        else:
            b = req.bounded_stream.read()
        return b


class SystemAvailableController(RESTController):
    def __init__(self) -> None:
        super(SystemAvailableController, self).__init__()

    def on_get(self, req: Request, resp: Response) -> None:
        logger.debug("System available request")
        resp.text = ResponseCode.SYSTEM_AVAILABLE.value
        resp.content_type = "text/plain; charset=us-ascii"
        resp.status = falcon.HTTP_200


class SystemCheckController(RESTController):
    def __init__(self) -> None:
        super(SystemCheckController, self).__init__()

    @classmethod
    def response_for_success(cls, req: Request, resp: Response) -> None:
        logger.debug("System check request")
        resp.text = ResponseCode.SYSTEM_CHECK_OK.value
        resp.content_type = "text/plain; charset=us-ascii"
        resp.status = falcon.HTTP_200

    @classmethod
    def response_for_failure(cls, req: Request, resp: Response) -> None:
        logger.error("System check failed")
        resp.text = ResponseCode.SYSTEM_CHECK_FAILED.value
        resp.content_type = "text/plain; charset=us-ascii"
        resp.status = falcon.HTTP_500

    def on_get(self, req: Request, resp: Response) -> None:
        self.response_for_success(req, resp)


class GermanSentimentController(RESTController):
    def __init__(self, german_sentiment_classifier: GermanSentimentClassifier) -> None:
        super(GermanSentimentController, self).__init__()
        self.german_sentiment_classifier = german_sentiment_classifier

    def classify(self, req: Request):
        request = ClassificationRequest.deserialize(self.get_body(req))
        texts = request.texts

        logger.info(f"Received sentiment classification request for {len(texts)} texts")

        start_time = time.time()
        sentiments = self.german_sentiment_classifier.classify(texts)
        end_time = time.time() - start_time

        logger.info(f"Inference took {end_time} seconds!")

        result = {"sentiments": sentiments}
        return result

    def on_post(self, req, resp):
        try:
            result = self.classify(req)
            resp.text = json.dumps(result)
            resp.content_type = "application/json"
            resp.status = falcon.HTTP_200
        except GermanSentimentClassifierError as e:
            logger.error(f"Caught GermanSentimentClassifierError: '{e}'")
            resp.status = falcon.HTTP_400
