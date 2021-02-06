from django.urls import path

from .views import (
    TradingDayListView, TradingDayCreateView, TradingDayDetailView, TradingDayUpdateView,
    TradingDayDeleteView
)


app_name = "tradingdays"

urlpatterns = [
    path("", TradingDayListView.as_view(), name="tradingday-list"),
    path("create/", TradingDayCreateView.as_view(), name="tradingday-create"),
    path("<int:pk>/", TradingDayDetailView.as_view(), name="tradingday-detail"),
    path("<int:pk>/update/", TradingDayUpdateView.as_view(), name="tradingday-update"),
    path("<int:pk>/delete/", TradingDayDeleteView.as_view(), name="tradingday-delete"),
]
