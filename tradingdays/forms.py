from django import forms

from .models import TradingDay


class TradingDayModelForm(forms.ModelForm):
    class Meta:
        model = TradingDay
        fields = (
            "user",
            "lotsize",
            "timeframe",
            "profit",
        )
