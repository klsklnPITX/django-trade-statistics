from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

from .models import TradingDay
from accounts.models import Account


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
