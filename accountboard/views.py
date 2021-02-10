from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from .modules.accountboard_modules import AccountBoardManager


class AccountBoardView(LoginRequiredMixin, generic.TemplateView):
    template_name = "accountboard/accountboard_list.html"

    def get_context_data(self, **kwargs):
        context = super(AccountBoardView, self).get_context_data(**kwargs)
        context_object_name = "accounts"

        acc_board_mgr = AccountBoardManager()

        accounts_data_list = acc_board_mgr.get_account_board_data()

        context.update({
            "accounts_data_list": accounts_data_list
        })

        return context
