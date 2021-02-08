from django.http.response import Http404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Sum
from django.shortcuts import HttpResponse, render

from .models import Account, Deposit, Withdrawal
from tradingdays.models import TradingDay
from .forms import AccountModelForm, WithdrawalModelForm, DepositModelForm


class AccountListView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/account_list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)


class AccountCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "accounts/account_create.html"
    form_class = AccountModelForm

    def get_success_url(self):
        return reverse("accounts:account-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.save()
        return super(AccountCreateView, self).form_valid(form)


class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "accounts/account_detail.html"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        user = self.request.user
        context_object_name = "account"
        account = self.kwargs["pk"]

        account = Account.objects.filter(user=user).get(pk=account)

        # Get account balance
        # Deposits + Profits - Withdrawals
        deposits_sum = Deposit.objects.filter(account=account).aggregate(Sum("amount"))
        withdrawals_sum = Withdrawal.objects.filter(account=account).aggregate(Sum("amount"))

        profit = TradingDay.objects.filter(user=user).filter(account=account).aggregate(Sum("profit"))

        if not deposits_sum["amount__sum"]:
            deposits_sum["amount__sum"] = 0
        if not withdrawals_sum["amount__sum"]:
            withdrawals_sum["amount__sum"] = 0
        if not profit["profit__sum"]:
            profit["profit__sum"] = 0

        deposits_sum = round(float(deposits_sum["amount__sum"]), 2)
        withdrawals_sum = round(float(withdrawals_sum["amount__sum"]), 2)
        profit = round(float(profit["profit__sum"]), 2)
        balance = round(deposits_sum + profit - withdrawals_sum, 2)

        # Create daily profit chart data
        labels_daily_profit_chart = []
        data_daily_profit_chart = []

        data_decimal = list(TradingDay.objects.filter(user=user).filter(account=account).values_list("profit"))
        dates = list(TradingDay.objects.filter(user=user).filter(account=account).values_list("date_created"))

        for n in data_decimal:
            if n:
                data_daily_profit_chart.append(float(n[0]))
            else:
                data_daily_profit_chart.append(0)

        for d in dates:
            labels_daily_profit_chart.append(d[0].strftime("%d.%m.%Y"))

        context.update({
            "account": account,
            "withdrawals_sum": withdrawals_sum,
            "deposits_sum": deposits_sum,
            "profit": profit,
            "balance": balance,
            "data_daily_profit_chart": data_daily_profit_chart,
            "labels_daily_profit_chart": labels_daily_profit_chart
        })

        return context


class AccountUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/account_update.html"
    form_class = AccountModelForm

    def get_success_url(self):
        return reverse("accounts:account-list")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class AccountDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "accounts/account_delete.html"

    def get_success_url(self):
        return reverse("accounts:account-list")

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


# WITHDRAWALS
class WithdrawalListView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/withdrawal_list.html"
    context_object_name = "withdrawals"

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["pk"]
        if Account.objects.filter(user=user).filter(pk=account):
            return Withdrawal.objects.filter(account=account)
        else:
            return None


class WithdrawalCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "accounts/withdrawal_create.html"
    form_class = WithdrawalModelForm

    def get_success_url(self):
        return reverse("accounts:withdrawal-list", kwargs={'pk': self.kwargs["pk"]})

    def form_valid(self, form):
        account = form.save(commit=False)
        account_pk = self.kwargs["pk"]
        account_instance = Account.objects.get(pk=account_pk)
        account.account = account_instance
        account.save()
        return super(WithdrawalCreateView, self).form_valid(form)


class WithdrawalUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/withdrawal_update.html"
    form_class = WithdrawalModelForm

    def get_success_url(self):
        return reverse("accounts:withdrawal-list", kwargs={'pk': self.kwargs["a_pk"]})

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["a_pk"]
        withdrawal = self.kwargs["pk"]

        if Account.objects.filter(user=user).filter(pk=account):
            return Withdrawal.objects.filter(pk=withdrawal).filter(account=account)
        else:
            return None


class WithdrawalDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "accounts/withdrawal_delete.html"

    def get_success_url(self):
        return reverse("accounts:withdrawal-list", kwargs={'pk': self.kwargs["a_pk"]})

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["a_pk"]
        withdrawal = self.kwargs["pk"]

        if Account.objects.filter(user=user).filter(pk=account):
            return Withdrawal.objects.filter(pk=withdrawal).filter(account=account)
        else:
            return None


# DEPOSITS
class DepositListView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/deposit_list.html"
    context_object_name = "deposits"

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["pk"]
        if Account.objects.filter(user=user).filter(pk=account):
            return Deposit.objects.filter(account=account)
        else:
            return None


class DepositCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "accounts/deposit_create.html"
    form_class = DepositModelForm

    def get_success_url(self):
        return reverse("accounts:deposit-list", kwargs={'pk': self.kwargs["pk"]})

    def form_valid(self, form):
        account = form.save(commit=False)
        account_pk = self.kwargs["pk"]
        account_instance = Account.objects.get(pk=account_pk)
        account.account = account_instance
        account.save()
        return super(DepositCreateView, self).form_valid(form)


class DepositUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/deposit_update.html"
    form_class = DepositModelForm

    def get_success_url(self):
        return reverse("accounts:deposit-list", kwargs={'pk': self.kwargs["a_pk"]})

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["a_pk"]
        deposit = self.kwargs["pk"]

        if Account.objects.filter(user=user).filter(pk=account):
            return Deposit.objects.filter(pk=deposit).filter(account=account)
        else:
            return None


class DepositDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "accounts/deposit_delete.html"

    def get_success_url(self):
        return reverse("accounts:deposit-list", kwargs={'pk': self.kwargs["a_pk"]})

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["a_pk"]
        deposit = self.kwargs["pk"]

        if Account.objects.filter(user=user).filter(pk=account):
            return Deposit.objects.filter(pk=deposit).filter(account=account)
        else:
            return None
