from accounts.models import Account
from django.db.models import query
from django.views import generic
from django.shortcuts import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import TradingDay
from .forms import CustomUserCreationForm, TradingDayModelForm, CustomUserCreationForm


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


class TradingDayListView(LoginRequiredMixin, generic.ListView):
    template_name = "tradingdays/tradingday-list.html"
    context_object_name = "tradingdays"

    def get_queryset(self):
        user = self.request.user
        return TradingDay.objects.filter(user=user)


class TradingDayCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "tradingdays/tradingday_create.html"
    form_class = TradingDayModelForm

    def get_form_kwargs(self):
        kwargs = super(TradingDayCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.save()
        return super(TradingDayCreateView, self).form_valid(form)


class TradingDayDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "tradingdays/tradingday_detail.html"

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tradingdays/tradingday_update.html"
    form_class = TradingDayModelForm

    def get_form_kwargs(self):
        kwargs = super(TradingDayUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")

    def get_queryset(self):
        return TradingDay.objects.all()


class TradingDayDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "tradingdays/tradingday_delete.html"
    queryset = TradingDay.objects.all()

    def get_success_url(self):
        return reverse("tradingdays:tradingday-list")
