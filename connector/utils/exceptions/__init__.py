from typing import (
    Any,
    Union,
)

from rest_framework import status

from utils.response import (
    APIResponse,
    ErrorData,
)


class ValidationError(Exception):
    message: str
    data: Any

    def __init__(self, data, message=None):
        self.message = message
        self.data = data


class KasaAPIException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    code: Union[APIResponse.Code, str] = APIResponse.Code.INTERNAL_SERVER_ERROR
    message: str = 'Unknown error.'

    title: str = '요청에 실패했습니다.'
    description: str = '고객센터에 문의 부탁드립니다.'

    def __init__(self, message=None, code=None, status_code=None,
                 title=None, description=None, data=None):
        """
        :param message: Error message for debugging
        :param code: Internal error code
        :param status_code: HTTP status code

        `title`, `description`, `data` are data that can be exposed to users.
        """
        self.message = message or self.message
        self.status_code = status_code or self.status_code

        self.title = title or self.title
        self.description = description or self.description
        self.code = str(code or self.code).upper()
        self.data = data

    @property
    def error(self):
        return ErrorData(
            title=self.title,
            description=self.description,
            code=self.code,
            data=self.data
        )

    @classmethod
    def default_error_object(cls) -> ErrorData:
        return ErrorData(
            title=cls.title,
            description=cls.description,
            code=cls.code,
        )


from .bad_request import *
from .conflict import *
from .forbidden import *
from .internal_server_error import *
from .not_found import *
from .service_unavailable import *
from .too_many_requests import *
from .unauthorized import *
from .unprocessable_entity import *
from .upgrade_required import *
