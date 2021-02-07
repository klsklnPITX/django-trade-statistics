from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Account, Withdrawal
from .forms import AccountModelForm, WithdrawalModelForm


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
