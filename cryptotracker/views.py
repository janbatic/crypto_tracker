import logging

import pandas as pd
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from rest_framework import permissions
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from cryptotracker.models import Portfolio

from cryptotracker.models import BrokerPairs

Logger = logging.getLogger("api")
TRANSACTION_TYPES = ["buy", "sell"]


class TransactionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        validation = self.request_validation(request.data)
        if isinstance(validation, HttpResponse):
            return validation
        transaction_response = self.transaction(request.user, request.data)
        return transaction_response

    @staticmethod
    def request_validation(data):

        if not data.get("cryptocurrency"):
            return HttpResponse(status=400, content="No cryptocurrency given")
        try:
            BrokerPairs.objects.get(broker__name="binance", usdt_pair=data.get("cryptocurrency"))
        except ObjectDoesNotExist:
            return HttpResponse(status=400, content="No such cryptocurrency")
        if not data.get("amount"):
            return HttpResponse(status=400, content="No amount given")
        if not data.get("transaction_type"):
            return HttpResponse(status=400, content="No transaction type given")
        if data.get("amount") <= 0:
            return HttpResponse(status=400, content="Wrong amount given")
        if data.get("transaction_type") not in TRANSACTION_TYPES:
            return HttpResponse(status=400, content="Wrong transaction type given possible types buy, sell")

    def transaction(self, user, data):
        cryptocurrency = data.get("cryptocurrency")
        transaction_type = data.get("transaction_type")
        amount = data.get("amount")
        try:
            user_crypto, created = user.crypto.get_or_create(name=cryptocurrency)
            if transaction_type == "buy":
                user_crypto.amount += amount
            elif transaction_type == "sell":
                if user_crypto.amount < amount:
                    return HttpResponse(status=409, content="Not big enough amount on account to sell ")
                user_crypto.amount -= amount

            self.update_portfolio_value(user, cryptocurrency, amount)
            user_crypto.save()
            return HttpResponse(status=200)
        except Exception as e:
            Logger.error(f"Failed adding transaction with error -> {e}")
            return HttpResponse(status=500)

    @staticmethod
    def update_portfolio_value(user, cryptocurrency, amount):
        response = requests.get(
            url=f"https://api.binance.com/api/v3/ticker/price?symbol={cryptocurrency}USDT"
        )
        price = float(response.json().get("price"))
        amount_value = price * amount
        user.portfolio.create(amount_value=amount_value)


class PossessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        parameter = request.GET.get("cryptocurrency", None)
        if parameter:
            cryptocurrency = request.user.crypto.filter(name=parameter)
            if not cryptocurrency:
                return JsonResponse(
                    {
                        "cryptocurrency": parameter,
                        "amount": 0
                    }
                )
            return JsonResponse(cryptocurrency.serialized_data())
        cryptocurrencies = request.user.crypto.filter(amount__gt=0)
        current_portfolio_value = request.user.portfolio.last()
        if not cryptocurrencies:
            return HttpResponse(status=204, content="No cryptocurrency in possession found")
        return JsonResponse(
            {
                "cryptocurrencies": [cryptocurrency.serialized_data() for cryptocurrency in cryptocurrencies],
                "current_portfolio_value": current_portfolio_value.amount_value if current_portfolio_value else 0
            }
        )


class CryptoInfoView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        shown_list = []
        page_number = request.GET.get('page', 1)

        crypto_data_df = self.get_crypto_data()
        for row in crypto_data_df.iterrows():
            shown_list.append(
                {
                    'name': row[1]['b'],
                    'value': row[1]['c'],
                    'market_cap': row[1]['market_cap']
                }
            )
        paginator = Paginator(shown_list, 25)
        page_obj = paginator.get_page(page_number)
        return JsonResponse(
            {
                'crypto_info': page_obj.object_list,
                'page': page_obj.number,
                'num_pages': page_obj.paginator.num_pages
            }
        )

    @staticmethod
    def get_crypto_data():
        response = requests.get(
            url='https://www.binance.com/exchange-api/v2/public/asset-service/product/get-products'
        )
        exchange_info = response.json()
        pairs = exchange_info.get("data")

        df = pd.DataFrame.from_records(pairs)
        mask = pd.DataFrame.from_records(pairs)["q"] == "USDT"
        crypto_data_df = df[mask]
        market_cap_series = crypto_data_df.loc[:, "c"].astype(float) * crypto_data_df.loc[:, "cs"].astype(float)
        crypto_data_df = crypto_data_df.assign(market_cap=market_cap_series)
        crypto_data_df.sort_values('market_cap')
        return crypto_data_df.sort_values('market_cap', ascending=False)
