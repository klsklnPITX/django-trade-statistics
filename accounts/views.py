from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

from .models import Account
from .forms import AccountModelForm


class AccountListView(LoginRequiredMixin, generic.ListView):
    template_name = "accounts/account_list.html"
    context_object_name = "accounts"

    def get_queryset(self):
        # user = self.request.user
        # return TradingDay.objects.filter(user=user)
        return Account.objects.all()


class AccountCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "accounts/account_create.html"
    form_class = AccountModelForm

    def get_success_url(self):
        return reverse("accounts:account-create")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user = self.request.user
        user.save()
        return super(AccountCreateView, self).form_valid(form)
