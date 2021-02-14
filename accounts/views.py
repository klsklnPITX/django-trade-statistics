from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from django.shortcuts import render, redirect

from .models import Account, Deposit, Withdrawal, TradingDay
from .forms import AccountModelForm, WithdrawalModelForm, DepositModelForm, CsvUploadForm, TradingDayModelForm, CustomUserCreationForm
from .modules.accounts_modules import AccountDataManager


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class LandingPageView(generic.TemplateView):
    template_name = "landing.html"


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


# class AccountDetailView(LoginRequiredMixin, generic.DetailView):
#     template_name = "accounts/account_detail.html"

#     def get_queryset(self):
#         return Account.objects.filter(user=self.request.user)


class AccountView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accounts/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super(AccountView, self).get_context_data(**kwargs)
        user = self.request.user
        context_object_name = "account"
        account = self.kwargs["pk"]
        account = Account.objects.filter(user=user).get(pk=account)

        # GET DATA
        account_data = AccountDataManager(user, account)
        # Get account balance, profit, withdrawals, deposits sum
        profit, balance, withdrawals_sum, deposits_sum = account_data.get_account_main_statistics()

        # Get daily profit chart data
        data_daily_profit_chart, labels_daily_profit_chart = account_data.get_daily_profit_chart_data()

        # Get monthly profit chart data
        data_monthly_profit_chart, labels_monthly_profit_chart = account_data.get_monthly_profit_chart_data()

        # Get average daily profit
        averagy_daily_profit = account_data.get_average_daily_profit()

        # Get trading day count
        tradingday_count = account_data.get_tradingday_count()

        # Get accumulated profit
        data_accumulated_profit_chart, labels_accumulated_profit_chart = \
            account_data.get_accumulated_profit(
                tradingday_count,
                data_daily_profit_chart
            )

        # Get profit percent
        profit_percent = account_data.get_profit_percent(profit, deposits_sum)

        tax_per_year_data = account_data.calculate_yearly_tax(account_data.get_yearly_profit())

        context.update({
            "account": account,
            "withdrawals_sum": withdrawals_sum,
            "deposits_sum": deposits_sum,
            "profit": profit,
            "balance": balance,
            "data_daily_profit_chart": data_daily_profit_chart,
            "labels_daily_profit_chart": labels_daily_profit_chart,
            "data_monthly_profit_chart": data_monthly_profit_chart,
            "labels_monthly_profit_chart": labels_monthly_profit_chart,
            "averagy_daily_profit": averagy_daily_profit,
            "tradingday_count": tradingday_count,
            "data_accumulated_profit_chart": data_accumulated_profit_chart,
            "labels_accumulated_profit_chart": labels_accumulated_profit_chart,
            "profit_percent": profit_percent,
            "tax_per_year_data": tax_per_year_data
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
            return Withdrawal.objects.filter(account=account).order_by("date")
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
            return Deposit.objects.filter(account=account).order_by("date")
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

# TRADINGDAYS


class TradingDayListView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/tradingday_list.html"
    context_object_name = "tradingdays"

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["pk"]
        return (TradingDay.objects
                .filter(user=user)
                .filter(account=account)
                .order_by("date_created"))


class TradingDayCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "accounts/tradingday_create.html"
    form_class = TradingDayModelForm

    def get_form_kwargs(self):
        kwargs = super(TradingDayCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("accounts:tradingday-list", kwargs={'pk': self.kwargs["pk"]})

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.save()
        return super(TradingDayCreateView, self).form_valid(form)


class TradingDayDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "accounts/tradingday_detail.html"

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["a_pk"]
        tradingday = self.kwargs["pk"]

        if Account.objects.filter(user=user).filter(pk=account):
            return TradingDay.objects.filter(pk=tradingday).filter(account=account)
        else:
            return None


class TradingDayUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/tradingday_update.html"
    form_class = TradingDayModelForm

    def get_form_kwargs(self):
        kwargs = super(TradingDayUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse("accounts:tradingday-list", kwargs={'pk': self.kwargs["a_pk"]})

    def get_queryset(self):
        user = self.request.user
        account = self.kwargs["a_pk"]
        tradingday = self.kwargs["pk"]

        if Account.objects.filter(user=user).filter(pk=account):
            return TradingDay.objects.filter(pk=tradingday).filter(account=account)
        else:
            return None


class TradingDayDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "accounts/tradingday_delete.html"

    def get_queryset(self):
        tradingday = self.kwargs["pk"]
        account = self.kwargs["a_pk"]

        return (TradingDay.objects
                .filter(account=account)
                .filter(pk=tradingday))

    def get_success_url(self):
        return reverse("accounts:tradingday-list", kwargs={'pk': self.kwargs["a_pk"]})


# CSV File upload an parse
def upload_csv_view(request):
    if request.method == "POST":
        form = CsvUploadForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            account = request.POST["account"]
            if AccountDataManager.allowed_file(file):
                acc_data_mgr = AccountDataManager(request.user, account)
                if "check_delete_account_data" in request.POST:
                    # Delete previous account data
                    acc_data_mgr.delete_previous_account_data()
                acc_data_mgr.parse_csv_file(file)
                return redirect("accounts:account-list")
            else:
                return upload_csv_error_view(request, "Filetype not allowed")
        else:
            form = CsvUploadForm()
        return render(request, "accounts/csv_upload.html", {"form": form})

    if request.method == "GET":
        form = CsvUploadForm(user=request.user)
        return render(request, "accounts/csv_upload.html", {"form": form})


def upload_csv_error_view(request, errors):
    return render(request, "accounts/csv_error.html", {"errors": errors})
