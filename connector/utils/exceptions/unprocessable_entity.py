from datetime import time

from django.conf import settings
from rest_framework import status

# from ratelimit.utils import _split_rate
from utils.exceptions import (
    LEELEE_CUSTOMER_CONTRACT,
    KasaAPIException,
)
from utils.response import APIResponse


class UnprocessableEntityError(KasaAPIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    message = 'Unprocessable Entity.'
    code = 'UNPROCESSABLE_ENTITY'


class InvalidStateError(UnprocessableEntityError):
    code = APIResponse.Code.INVALID_STATE


class InsufficientFundsError(UnprocessableEntityError):
    message = 'Insufficient funds.'
    code = APIResponse.Code.INSUFFICIENT_FUNDS.value
    title = '예치금이 부족합니다.'
    description = '예치금이 부족합니다. 예치금을 확인하고 다시 시도해주세요.'


class InsufficientDABSError(UnprocessableEntityError):
    message = 'Insufficient DABS'
    code = APIResponse.Code.INSUFFICIENT_DABS.value
    title = 'DABS가 부족합니다'
    description = 'DABS가 부족합니다. DABS를 확인하고 다시 시도해주세요.'


class SubscriptionLimitExceededError(UnprocessableEntityError):
    message = "Cannot subscribe more than 5% of public offering"
    code = APIResponse.Code.SUBSCRIPTION_LIMIT_EXCEEDED.value
    title = '최대 청약 수량을 초과하였습니다.'

    def __init__(self, limit_percent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.description = f'청약은 전체 DABS 수량의 {limit_percent}% 이내만 가능합니다.'


class QuotaExceededError(UnprocessableEntityError):
    message = "Cannot exceed daily quota"
    code = APIResponse.Code.QUOTA_EXCEEDED.value


class DisagreedRequiredTermsError(UnprocessableEntityError):
    message = 'Disagreed to required terms.'
    code = APIResponse.Code.DISAGREED_REQUIRED_TERMS.value


class UnproperRiskRatingError(UnprocessableEntityError):
    message = 'Risk of deal is higher than those of investor.'
    code = APIResponse.Code.INVALID_STATE.value


class InvalidVerifyCodeError(UnprocessableEntityError):
    message = '인증 코드가 일치하지 않습니다.'
    code = APIResponse.Code.INVALID_VERIFY_CODE.value
    title = '인증번호가 맞지 않습니다.'
    description = '입력하신 인증번호와 발송된 인증번호가 일치하지 않습니다. 다시 인증요청을 하여 새로운 인증번호로 인증을 완료해주세요.'


class FailToVerifyMFAError(UnprocessableEntityError):
    title = '추가 인증에 실패하였습니다.'
    code = 'FAIL_TO_VERIFY_MFA'


class FailToVerifyMobileNumberError(UnprocessableEntityError):
    title = '모바일 번호 인증에 실패하였습니다.'
    code = 'FAIL_TO_VERIFY_MOBILE_NUMBER'


class InvalidDABSCodeError(UnprocessableEntityError):
    message = 'Invalid DABS CODE'
    code = APIResponse.Code.INVALID_DABS_CODE.value
    title = 'DABS CODE 맞지 많습니다.'
    description = '올바르지 않은 DABS CODE 입니다. DABS CODE를 확인하고 다시 시도해 주세요.'


class VerifyLimitError(UnprocessableEntityError):
    message = '토큰 검증 횟수를 초과했습니다.'
    code = APIResponse.Code.EXPIRED_VERIFY_LIMIT.value


class RequestLimitError(UnprocessableEntityError):
    message = '본인 인증 요청 횟수를 초과헀습니다.'
    code = APIResponse.Code.EXCEED_REQUEST_LIMIT.value
    title = '인증요청 횟수를 초과하였습니다'
    description = '보안을 위해 인증요청 횟수를 1일 5회로 제한하고 있습니다. 24시간 후 다시 시도해주세요. 불편을 드려 죄송합니다.'

    def __init__(self, *args, rate: str = '5/d', **kwargs):
        super().__init__(*args, **kwargs)

    #     count, _ = _split_rate(rate)
    #     # TODO: More various description formatting
    #     self.description = (f'보안을 위해 인증요청 횟수를 1일 {count}회로 제한하고 있습니다. '
    #                         '24시간 후 다시 시도해주세요. 불편을 드려 죄송합니다.')


class VerifiedTokenError(UnprocessableEntityError):
    message = '이미 인증된 토큰입니다.'
    code = APIResponse.Code.VERIFIED_TOKEN.value
    title = '이미 인증된 토큰입니다.'
    description = ''


class ExpiredTokenError(UnprocessableEntityError):
    message = '이미 만료된 토큰입니다.'
    code = APIResponse.Code.EXPIRED_TOKEN.value
    title = '인증 유효 시간이 만료되었습니다.'
    description = '보안을 위해 인증 유효 시간을 3분으로 제한하고 있습니다. 다시 인증해주세요.'


class InvalidTokenError(UnprocessableEntityError):
    message = '인증 할 수 없는 토큰 입니다.'
    code = APIResponse.Code.INVALID_STATE.value
    title = '인증 할 수 없는 토큰 입니다.'
    description = ''


class InvalidIndividualInfoError(UnprocessableEntityError):
    message = '본인 인증을 위한 정보가 올바르지 않습니다.'
    code = APIResponse.Code.INVALID_INDIVIDUAL_INFO.value
    title = '본인확인 정보를 다시 확인해주세요.'
    description = '입력하신 본인확인 정보와 통신사 정보가 일치하지 않습니다. 다시 확인해주세요.'


class InvalidSignUpStatusError(InvalidIndividualInfoError):
    message = 'Invalid sign-up status.'
    code = 'INVALID_SIGNUP_STATUS'


class AlreadyExistError(UnprocessableEntityError):
    message = 'Unprocessable Entity.'
    code = APIResponse.Code.ALREADY_EXIST.value


class TransferBlockedError(UnprocessableEntityError):
    message = "User's transfer is blocked."
    code = APIResponse.Code.TRANSFER_BLOCKED.value
    title = '입출금이 제한되었습니다.'
    description = f'다시 입출금 서비스를 이용하시려면 CS팀({LEELEE_CUSTOMER_CONTRACT})으로 문의해주세요.'


class OrderBlockedError(UnprocessableEntityError):
    message = "User's order is blocked."
    code = APIResponse.Code.ORDER_BLOCKED.value


class MarketClosedError(UnprocessableEntityError):
    code = 'MARKET_CLOSED'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = 'Trading engine response with `INVALID_MARKET_STATE`.'
        self.title = '거래 가능한 시간이 아닙니다.'

        formatted_close_time = time.fromisoformat(settings.SUBSCRIPTION_CLOSE_TIME)
        formatted_close_time_with_unit = (
            f'{formatted_close_time.hour}시'
            f'{" " + str(formatted_close_time.minute) + "분" if formatted_close_time.minute else ""}'
        )
        self.description = (
            '주문 및 주문취소는 평일 '
            f'{settings.SUBSCRIPTION_OPEN_TIME}~{settings.SUBSCRIPTION_CLOSE_TIME} '
            f'까지 가능하며, {formatted_close_time_with_unit} 이후 미체결된 주문은 자동으로 취소됩니다.'
        )


class SubscriptionMarketClosedError(UnprocessableEntityError):
    code = 'MARKET_CLOSED'

    def __init__(self, open_time: time, close_time: time, *args, is_close_date: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = f'Operating hours: {open_time} to {close_time}.'
        self.title = 'Not an available time to subscribe or cancel.'

        formatted_open_time = open_time.strftime("%-H:%M")
        formatted_close_time = close_time.strftime("%-H:%M")
        self.description = (
            f'{"On the closing date of subscription, " if is_close_date else ""}'
            'Subscription and cancellation is possible '
            f'from {formatted_open_time} to {formatted_close_time}{"." if is_close_date else " on weekdays."}'
        )


class BankServiceInProgressError(UnprocessableEntityError):
    message = 'Another banking transaction is in progress.'
    code = 'BANK_SERVICE_IN_PROGRESS'
    title = "입출금 요청이 처리 중입니다."
    description = "이전 입출금 요청이 처리 중입니다.\n잠시 후 다시 이용 부탁드립니다."


class ExceedRemainingInvestmentLimitError(UnprocessableEntityError):
    message = 'Exceed remaining investment limit.'
    code = 'EXCEED_REMAINING_INVESTMENT_LIMIT'
    title = '잔여 투자한도를 초과하였습니다.'

    def __init__(self, remaining_investment_limit: int, *args, **kwargs):
        description = f'연간 잔여 투자한도는 {max(0, remaining_investment_limit):,}원 입니다.'
        super().__init__(*args, description=description, **kwargs)


class UnprocessableLeftMemberError(UnprocessableEntityError):
    code = 'LEFT_MEMBER'
    title = '탈퇴한 회원입니다.'
    description = '입력하신 UUID와 일치하는 회원은 이미 탈퇴한 회원입니다.'


class InvalidInvestmentAccountError(InvalidIndividualInfoError):
    message = 'Invalid investment account.'
    code = 'INVALID_INVESTMENT_ACCOUNT'
