from django.contrib.auth import get_user_model

from accounts.modules.accounts_modules import AccountDataManager
from accounts.models import Account

User = get_user_model()


class AccountBoardManager():
    """
    This class contains all methods for the AccountBoard
    """

    def __init__(self):
        pass

    def get_account_board_data(self):
        """
        This method collects all data from all accounts for the AccountBoardView.
        Returns a list with dictionaries and account's data in it.
        """

        # Get each account with user and account id
        accounts = Account.objects.all().values("user", "id")

        accounts_data_list = []

        # Loop through each account to get it's data with Account DataManager
        for account in accounts:
            acc_data_mgr = AccountDataManager(account["user"], account["id"])
            # Get statistics
            acc_data = acc_data_mgr.get_account_main_statistics()
            # Get tradingdays
            trading_days = acc_data_mgr.get_tradingday_count()
            # Get profit percent
            profit_percent = acc_data_mgr.get_profit_percent(acc_data[0], acc_data[3])
            # Get username
            username = User.objects.filter(id=account["user"]).values("username")
            username = username[0]["username"]
            # Get account number
            account_number = (Account.objects
                              .filter(id=account["id"])
                              .filter(user=account["user"])
                              .values("account_number"))
            account_number = account_number[0]["account_number"]

            # Fill context for html
            accounts_data_list.append({
                "user": username,
                "account_number": account_number,
                "profit": acc_data[0],
                "profit_percent": profit_percent,
                "balance": acc_data[1],
                "trading_days": trading_days,
                "withdrawals": acc_data[2],
                "deposits": acc_data[3],
            })

        return accounts_data_list
