from locust import HttpUser, between, task
import random
from models import IngestionSchema
import json
import datetime

key = [1, 2, 3, 4, 5, 6]
text = "String of text"


class TestPerformance(HttpUser):
    wait_time = between(1, 3)

    @task
    def ingest_test(self):
        ingestion = IngestionSchema(key=random.choice(key), payload=text)
        headers = {
            "Accept": "application/json",
            "x-api-key": "BigProfiles-API",
            "Content-Type": "application/json",
        }
        self.client.post(
            "/api/v1/ingest", data=json.dumps(ingestion.dict()), headers=headers
        )

    @task
    def retrive_test(self):
        date_from = (
            (datetime.datetime.now() - datetime.timedelta(minutes=3))
            .replace(second=0, microsecond=0, tzinfo=None)
            .isoformat()
        )
        date_to = (
            datetime.datetime.now()
            .replace(second=0, microsecond=0, tzinfo=None)
            .isoformat()
        )
        date_from = date_from.replace(":", "%3A")
        date_to = date_to.replace(":", "%3A")
        headers = {"Accept": "application/json", "x-api-key": "BigProfiles-API"}
        url = "/api/v1/retrieve?date_from=%s&date_to=%s" % (date_from, date_to)
        self.client.get(url, headers=headers)
