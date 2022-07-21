from rest_framework import status

from utils.exceptions import CustomAPIException
from utils.response import APIResponse


class ServiceUnavailableError(CustomAPIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    message = 'Service unavailable.'
    code = 'SERVICE_UNAVAILABLE'


class IdentityVerificationError(ServiceUnavailableError):
    message = '휴대폰 인증이 원활하지 않습니다.'
    code = APIResponse.Code.IDENTITY_VERIFICATION_ERROR.value
    title = '휴대폰 인증이 원활하지 않습니다.'
    description = '죄송합니다. 현재 휴대폰 인증이 원활하지 않습니다. 잠시 후 다시 시도해주세요.'
