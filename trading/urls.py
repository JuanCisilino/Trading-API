# trading/urls.py

from django.urls import path
from .views import execute_trade_view, stats_view, trades_list_view, balance_view

urlpatterns = [
    path('trades/execute/', execute_trade_view),
    path('trades/', trades_list_view),
    path('balance/', balance_view),
    path('stats/', stats_view),
]