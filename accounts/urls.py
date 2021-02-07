from django.urls import path

from .views import (
    AccountListView, AccountCreateView, AccountDetailView, AccountDeleteView, AccountUpdateView,
    WithdrawalListView
)

app_name = "account"

urlpatterns = [
    path("", AccountListView.as_view(), name="account-list"),
    path("create/", AccountCreateView.as_view(), name="account-create"),
    path("<int:pk>/", AccountDetailView.as_view(), name="account-detail"),
    path("<int:pk>/update/", AccountUpdateView.as_view(), name="account-update"),
    path("<int:pk>/delete/", AccountDeleteView.as_view(), name="account-delete"),
    path("<int:pk>/withdrawals/", WithdrawalListView.as_view(), name="withdrawal-list"),
]
