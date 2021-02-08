from django.urls import path

from .views import (
    TradingDayListView, TradingDayCreateView, TradingDayDetailView, TradingDayUpdateView,
    TradingDayDeleteView, upload_csv_view
)


app_name = "tradingdays"

urlpatterns = [
    path("", TradingDayListView.as_view(), name="tradingday-list"),
    path("create/", TradingDayCreateView.as_view(), name="tradingday-create"),
    path("<int:pk>/", TradingDayDetailView.as_view(), name="tradingday-detail"),
    path("<int:pk>/update/", TradingDayUpdateView.as_view(), name="tradingday-update"),
    path("<int:pk>/delete/", TradingDayDeleteView.as_view(), name="tradingday-delete"),
    path("upload/", upload_csv_view, name="tradingday-upload"),
    path("upload/error", upload_csv_view, name="tradingday-upload-error"),
]
