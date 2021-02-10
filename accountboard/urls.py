from django.urls import path

from .views import AccountBoardView

app_name = "accountboard"

urlpatterns = [
    path("", AccountBoardView.as_view(), name="accountboard-list"),
]
