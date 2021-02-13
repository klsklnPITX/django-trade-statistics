from django.urls import path

from .views import (
    AccountListView, AccountCreateView, AccountDeleteView, AccountUpdateView,
    WithdrawalListView, WithdrawalCreateView, WithdrawalUpdateView, WithdrawalDeleteView,
    DepositListView, DepositCreateView, DepositUpdateView, DepositDeleteView, AccountView,
    TradingDayListView, TradingDayCreateView, TradingDayDetailView, TradingDayUpdateView,
    TradingDayDeleteView, upload_csv_view
)


app_name = "accounts"

urlpatterns = [
    # Account
    path("", AccountListView.as_view(), name="account-list"),
    path("create/", AccountCreateView.as_view(), name="account-create"),
    path("<int:pk>/", AccountView.as_view(), name="account-detail"),
    path("<int:pk>/update/", AccountUpdateView.as_view(), name="account-update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account-delete"),
    # Withdrawals
    path("<int:pk>/withdrawals/", WithdrawalListView.as_view(), name="withdrawal-list"),
    path("<int:pk>/withdrawals/create", WithdrawalCreateView.as_view(), name="withdrawal-create"),
    path("<int:a_pk>/withdrawals/<int:pk>/update/", WithdrawalUpdateView.as_view(), name="withdrawal-update"),
    path("<int:a_pk>/withdrawals/<int:pk>/delete/", WithdrawalDeleteView.as_view(), name="withdrawal-delete"),
    # Depostis
    path("<int:pk>/deposits/", DepositListView.as_view(), name="deposit-list"),
    path("<int:pk>/deposits/create", DepositCreateView.as_view(), name="deposit-create"),
    path("<int:a_pk>/deposits/<int:pk>/update/", DepositUpdateView.as_view(), name="deposit-update"),
    path("<int:a_pk>/deposits/<int:pk>/delete/", DepositDeleteView.as_view(), name="deposit-delete"),
    # Tradingdays
    path("<int:pk>/tradingday/", TradingDayListView.as_view(), name="tradingday-list"),
    path("<int:pk>/tradingday/create/", TradingDayCreateView.as_view(), name="tradingday-create"),
    path("<int:a_pk>/tradingday/<int:pk>/", TradingDayDetailView.as_view(), name="tradingday-detail"),
    path("<int:a_pk>/tradingday/<int:pk>/update/", TradingDayUpdateView.as_view(), name="tradingday-update"),
    path("<int:a_pk>/tradingday/<int:pk>/delete/", TradingDayDeleteView.as_view(), name="tradingday-delete"),
    # Upload CSV views
    path("upload/", upload_csv_view, name="tradingday-upload"),
    path("upload/error/", upload_csv_view, name="tradingday-upload-error"),
]
