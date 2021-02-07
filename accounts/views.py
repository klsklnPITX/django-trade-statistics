from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Account, Withdrawal
from .forms import AccountModelForm


class AccountListView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/account_list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(user=user)
        # return Account.objects.all()


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
        return Account.objects.all()


class AccountUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "accounts/account_update.html"
    form_class = AccountModelForm

    def get_success_url(self):
        return reverse("accounts:account-list")

    def get_queryset(self):
        return Account.objects.all()


class AccountDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = "accounts/account_delete.html"
    queryset = Account.objects.all()

    def get_success_url(self):
        return reverse("accounts:account-list")


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
