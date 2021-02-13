from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField

from .models import Account, Withdrawal, Deposit, TradingDay


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


class DepositModelForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = (
            "date",
            "amount",
        )
        widgets = {
            'date': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }


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
            "date_created",
            "note"
        )
        widgets = {
            'date_created': forms.DateInput(format=('%d/%m/%Y'), attrs={'class': 'form-control', 'placeholder': 'Select a date', 'type': 'date'}),
        }

    def __init__(self, user, *args, **kwargs):
        super(TradingDayModelForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}


class CsvUploadForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(CsvUploadForm, self).__init__(*args, **kwargs)
        self.fields['account'].queryset = Account.objects.filter(user=user)

    account = forms.ModelMultipleChoiceField(queryset=None)
    file = forms.FileField(label='Select csv file', widget=forms.FileInput(attrs={'accept': '.csv'}))
    check_delete_account_data = forms.BooleanField(required=False, label='Delete previous account data? (Tradingdays, withdrawals, deposits)')
