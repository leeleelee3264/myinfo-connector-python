from rest_framework import status

from utils.exceptions import CustomAPIException
from utils.response import APIResponse


class BadRequestError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Bad request.'
    code = 'BAD_REQUEST'


class ClientPlatformError(BadRequestError):
    """ Client Platform이 올바르지 않은 경우 발생

    Examples:
        Mobile용 API 를 Web(Operation/Test center)에서 사용한 경우.
        >>> ClientPlatformError("Mobile client only")
    """
    message = 'Requested from incorrect client platform.'
    code = 'INCORRECT_PLATFORM'


class UnknownAppInstanceError(BadRequestError):
    """ Mobile Client 요청에서 AppInstance 정보가 올바르지 않은 경우 발생

    Examples:
        있어야 하는 AppInstance 정보가 없을 경우
        >>> UnknownAppInstanceError('AppInstance ID is required.')
        올바르지 않은 AppInstance ID
        >>> UnknownAppInstanceError('Invalid AppInstance ID')
        AppInstance ID 를 가진 AppInstance 가 없는 경우
        >>> UnknownAppInstanceError('Does not exists: AppInstance ID 8f397557-dde7-4913-8178-84d453d8cd3b')
    """

    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Requested from unregistered app_instance.'
    code = 'UNKNOWN_APPINSTANCE'


class InvestmentAccountNotSpecified(BadRequestError):
    message = 'Investment account not specified.'
    code = 'INVESTMENT_ACCOUNT_NOT_SPECIFIED'


class InvalidParamError(BadRequestError):
    message = 'Invalid parameter.'
    code = APIResponse.Code.INVALID_PARAM.value


class InvalidFileTypeError(BadRequestError):
    code = 'INVALID_FILE_TYPE'

    def __init__(self, *allowed_types, **kwargs):
        message = f"Allowed types : {', '.join(allowed_types)}."
        super().__init__(message=message, **kwargs)


class InvalidFileRefError(BadRequestError):
    code = 'INVALID_FILE_REF'


class DuplicatedFileRefError(BadRequestError):
    code = 'FILE_REF_DUPLICATION'


class FileSizeLimitExceededError(BadRequestError):
    code = 'FILE_SIZE_LIMIT_EXCEEDED'


class FileNameTooLongError(BadRequestError):
    code = 'FILE_NAME_TOO_LONG'


class DecodeError(BadRequestError):
    message = 'Fail to decode.'
    code = 'DECODE_ERROR'


class MissingRequiredParameterError(BadRequestError):
    title = 'Miss required parameter'
    description = '필수 입력이 누락되었습니다.'

    def __init__(self, param):
        super().__init__(message=f"Parameter '{param}' is required.")


class InvalidUUIDParameterError(BadRequestError):
    code = 'INVALID_UUID_PARAM'
