from django import forms
from django.contrib.auth import get_user_model

from .models import Account, Withdrawal


User = get_user_model()


class AccountModelForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            # "user",
            "broker",
            "account_number",
            "account_type",
            "leverage",
            "started",
            "platform",
        )
        widgets = {
            'started': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


class WithdrawalModelForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = (
            "date",
            "amount",
        )
        widgets = {
            'date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }
