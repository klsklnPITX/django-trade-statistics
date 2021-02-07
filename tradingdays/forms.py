from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

from .models import TradingDay


User = get_user_model()


class TradingDayModelForm(forms.ModelForm):
    class Meta:
        model = TradingDay
        fields = (
            # "user",
            "account",
            "lotsize",
            "timeframe",
            "profit",
            "date_created"
        )
        widgets = {
            'date_created': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}
