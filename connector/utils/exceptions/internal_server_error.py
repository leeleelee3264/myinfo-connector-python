from typing import Type

from django.db import models
from rest_framework import status

from utils.exceptions import CustomAPIException


class InternalServerError(CustomAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = 'Internal server error.'
    code = 'INTERNAL_SERVER_ERROR'
    title = '오류가 발생했습니다.'
    description = '알 수 없는 오류가 발생했습니다. 고객센터로 문의 부탁드립니다.'


class DepositAccountNotExistError(InternalServerError):
    message = "Deposit account does not exist"
    code = "DEPOSIT_ACCOUNT_NOT_EXIST"


class BankAccountNotExistError(InternalServerError):
    message = 'Bank account does not exist'
    code = 'BANK_ACCOUNT_NOT_EXIST'


class MultipleSpecialBankAccountsError(InternalServerError):
    message = 'Special bank account must be unique'
    code = 'MULTIPLE_SPECIAL_BANK_ACCOUNTS'


class MultipleObjectsReturned(InternalServerError):
    message = 'Multiple object exists.'

    def __init__(self, model: Type[models.Model], *args, **kwargs):
        if not kwargs.get('message'):
            kwargs['message'] = f"Multiple {model.__name__} object exists."
        super().__init__(*args, **kwargs)


class MoneyTrustAccountNotExistError(BankAccountNotExistError):
    message = 'MoneyTrustAccount does not exist.'


class ExternalBankingServiceError(InternalServerError):
    message = '외부 은행 서비스에 오류가 발생했습니다.'
    code = 'EXTERNAL_BANKING_SERVICE_ERROR'
    title = '외부 은행 서비스에 오류가 발생했습니다.'
    description = '외부 은행 서비스에 오류가 발생했습니다.'
