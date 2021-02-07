from django.urls import path

from .views import AccountListView, AccountCreateView

app_name = "account"

urlpatterns = [
    path("", AccountListView.as_view(), name="account-list"),
    path("create/", AccountCreateView.as_view(), name="account-create")
]
