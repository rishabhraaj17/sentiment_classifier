# -*- coding: utf-8 -*-

import falcon.testing
import pytest
from hydra import initialize, compose

from german_sentiment_bert.app import build
from german_sentiment_bert.service.dtos import ClassificationRequest
from log import initialize_logging


@pytest.fixture(scope="class")
def client() -> falcon.testing.TestClient:
    initialize_logging()

    initialize(config_path="../../config", job_name="serve_app")
    conf = compose(config_name="config")

    app = build(conf)
    yield falcon.testing.TestClient(app)


@pytest.mark.unit
class TestGermanSentimentClassifier(object):

    def test_system_available(self, client):
        response = client.simulate_get("/system_available")
        assert response.text == "SYSTEM_AVAILABLE"
        assert response.status == falcon.HTTP_200

    def test_system_check(self, client):
        response = client.simulate_get("/system_check")
        assert response.text == "SYSTEM_CHECK_OK"
        assert response.status == falcon.HTTP_200

    def send_text_list_request(self, client, url, params=None):
        texts = ["Mit keinem guten Ergebniss", "Das ist gar nicht mal so gut",
                 "Total awesome!", "nicht so schlecht wie erwartet",
                 "Der Test verlief positiv.", "Sie fährt ein grünes Auto."]
        request = ClassificationRequest(texts)
        headers = {"Content-Type": "application/json"}
        response = client.simulate_post(url, body=request.serialize(), headers=headers, params=params)
        return response

    def test_text_classification(self, client):
        response = self.send_text_list_request(client, "/api/v1/classify")
        results = response.json
        assert results["sentiments"][0] == "negative"
        assert results["sentiments"][1] == "negative"
        assert results["sentiments"][2] == "positive"
        assert results["sentiments"][3] == "positive"
        assert results["sentiments"][4] == "neutral"
        assert results["sentiments"][5] == "neutral"
