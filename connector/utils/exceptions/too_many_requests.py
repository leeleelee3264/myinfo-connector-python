from rest_framework import status

from utils.exceptions import KasaAPIException
from utils.exceptions.unprocessable_entity import UnprocessableEntityError
from utils.response import APIResponse


class TooManyRequestsError(KasaAPIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    message = 'Too many requests.'
    code = 'TOO_MANY_REQUESTS'
    title = '요청이 너무 많습니다.'
    description = '잠시 후 다시 이용부탁드립니다.'


class ZendeskNotificationLimitError(UnprocessableEntityError):
    message = 'Zendesk 질문 답변 Webhook 요청 횟수를 초과했습니다.'
    code = APIResponse.Code.EXCEED_REQUEST_LIMIT.value
    title = 'Zendesk 질문 답변 webhook 요청 횟수를 초과하였습니다'
    description = '보안을 위해 1일 100회로 제한하고 있습니다.'
