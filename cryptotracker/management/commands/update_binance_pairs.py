from django.core.management import BaseCommand
import logging
import requests
import pandas as pd

from cryptotracker.models import BrokerPairs, Broker

logger = logging.getLogger("commands")


class Command(BaseCommand):

    def handle(self, **options):
        broker, created = Broker.objects.get_or_create(name='binance')

        response_exchange_info = requests.get(
            url="https://api.binance.com/api/v3/exchangeInfo"
        )
        exchange_info = response_exchange_info.json()
        symbols = exchange_info.get("symbols")

        df = pd.DataFrame.from_records(symbols)
        mask = pd.DataFrame.from_records(symbols)["quoteAsset"] == "USDT"
        usdt_assets = df.mask(~mask).dropna()
        binance_symbols = usdt_assets["baseAsset"].tolist()

        saved_pairs = BrokerPairs.objects.filter(
            broker=broker,
            usdt_pair__in=binance_symbols
        ).values_list('usdt_pair', flat=True)
        unsaved_paris = set(binance_symbols) - set(saved_pairs)
        if unsaved_paris:
            create_pairs = []
            for pair in unsaved_paris:
                create_pairs.append(BrokerPairs(broker=broker, usdt_pair=pair))
            if create_pairs:
                BrokerPairs.objects.bulk_create(create_pairs)

