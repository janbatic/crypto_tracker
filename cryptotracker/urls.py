from django.urls import path
from .views import TransactionView, PossessionView, CryptoInfoView

urlpatterns = [
    path('portfolio/transaction/', TransactionView.as_view()),
    path('portfolio/possession/', PossessionView.as_view()),
    path('crypto-info/', CryptoInfoView.as_view()),
]