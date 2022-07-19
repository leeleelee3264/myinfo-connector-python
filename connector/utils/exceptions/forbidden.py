from rest_framework import status

from services.common.constants import KASA_CUSTOMER_HOPE_TEL_NUMBER
from utils.exceptions import KasaAPIException


class ForbiddenError(KasaAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Forbidden.'
    code = 'FORBIDDEN'


class LeftUserError(ForbiddenError):
    message = 'Left.'
    code = 'LEFT_USER'
    description = ('해당 계정은 탈퇴된 계정입니다.'
                   f'다시 서비스를 이용하시려면 고객센터({KASA_CUSTOMER_HOPE_TEL_NUMBER})로 문의해주세요.')


class BlockedError(ForbiddenError):
    message = 'Blocked.'
    code = 'BLOCKED'
    title = '로그인이 차단되었습니다.'
    description = ('해당 계정을 통한 악의적 시도가 의심되어 로그인이 차단되었습니다. '
                   f'다시 서비스를 이용하시려면 고객센터({KASA_CUSTOMER_HOPE_TEL_NUMBER})로 문의해주세요.')


class InvalidAccessError(ForbiddenError):
    code = 'INVALID_ACCESS'
    title = '잘못된 경로로 접근하셨습니다.'
    description = ('비정상적인 경로로 접근하셨거나 오류가 발생해 요청을 수행할 수 없습니다. '
                   '확인하신 후 다시 시도해주세요. 불편을 드려 죄송합니다.')


class RequiredMFARegistrationError(ForbiddenError):
    code = 'REQUIRED_MFA_REGISTRATION'
    title = '추가인증이 필요합니다.'
    description = '추가인증을 활성화해주세요.'

    def __init__(self, *args, channel: str = '', **kwargs):
        super().__init__(*args, **kwargs)
        if channel:
            self.code = RequiredMFAError.code + f'_{channel.upper()}'


class RequiredMFAError(ForbiddenError):
    code = 'REQUIRED_MFA'
    title = '추가인증이 필요합니다.'
    description = '추가인증을 진행해주세요.'

    def __init__(self, *args, channel: str = '', **kwargs):
        super().__init__(*args, **kwargs)
        if channel:
            self.code = RequiredMFAError.code + f'_{channel.upper()}'
