from django.urls import path

from .views import (
    AccountListView, AccountCreateView, AccountDetailView, AccountDeleteView, AccountUpdateView,
    WithdrawalListView, WithdrawalCreateView, WithdrawalUpdateView, WithdrawalDeleteView
)

app_name = "account"

urlpatterns = [
    path("", AccountListView.as_view(), name="account-list"),
    path("create/", AccountCreateView.as_view(), name="account-create"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    path("<int:pk>/update/", AccountUpdateView.as_view(), name="account-update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account-delete"),
    path("<int:pk>/withdrawals/", WithdrawalListView.as_view(), name="withdrawal-list"),
    path("<int:pk>/withdrawals/create", WithdrawalCreateView.as_view(), name="withdrawal-create"),
    path("<int:a_pk>/withdrawals/<int:pk>/update/", WithdrawalUpdateView.as_view(), name="withdrawal-update"),
    path("<int:a_pk>/withdrawals/<int:pk>/delete/", WithdrawalDeleteView.as_view(), name="withdrawal-delete"),
]
