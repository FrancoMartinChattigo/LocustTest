"""
Manejador de Cuentas
"""
import os

from commons_qa_back.helpers.accounts.accounts_manager import AccountManager
from commons_qa_back.log.custom_logger import CustomLogger


class Accounts:
    """
    Todas las cuentas que se utilizan para los distintos ambientes y funcionalidades
    """

    @staticmethod
    def get_account(account_type):
        account_manager = AccountManager(os.path.dirname(os.path.realpath(__file__)))
        return account_manager.get_account(account_type)
