from django.db.models import query
from django.views import generic
from django.shortcuts import reverse

from .models import TradingDay
from .forms import TradingDayModelForm


class TradingDayListView(generic.ListView):
    template_name = "tradingdays/tradingday-list.html"
    context_object_name = "tradingdays"

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayCreateView(generic.CreateView):
    template_name = "tradingdays/tradingday_create.html"
    form_class = TradingDayModelForm

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")


class TradingDayDetailView(generic.DetailView):
    template_name = "tradingdays/tradingday_detail.html"

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayUpdateView(generic.UpdateView):
    template_name = "tradingdays/tradingday_update.html"
    form_class = TradingDayModelForm

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayDeleteView(generic.DeleteView):
    template_name = "tradingdays/tradingday_delete.html"
    queryset = TradingDay.objects.all()

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")
