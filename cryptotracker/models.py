from datetime import datetime

from django.conf import settings
from django.db import models
from django.db.models import ForeignKey


class Crypto(models.Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="crypto",
    )
    name = models.CharField(max_length=255)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.name

    def serialized_data(self):
        return {
            "cryptocurrency": self.name,
            "amount": self.amount
        }


class Portfolio(models.Model):
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio",
    )
    timestamp = models.TimeField(default=datetime.now)
    amount_value = models.FloatField(default=0)


class BrokerPairs(models.Model):
    broker = models.ForeignKey(
        "Broker",
        on_delete=models.CASCADE,
        related_name="pair"
    )
    usdt_pair = models.CharField(max_length=200)

    class Meta:
        unique_together = ("broker", "usdt_pair")

    def __str__(self):
        return self.broker


class Broker(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
