from typing import Optional

from django.conf import settings
from django.core import exceptions as django_exceptions
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.views import (
    exception_handler,
    set_rollback,
)

from elasticapm.contrib.django.client import client
from sentry_sdk import capture_exception
from utils import exceptions as kasa_exceptions
from utils.response import (
    APIErrorResponse,
    ErrorData,
)


def custom_exception_handler(exc, context) -> Optional[APIErrorResponse]:
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    exc = _convert_to_manageable(exc)
    response = exception_handler(exc, context)
    if response:
        return APIErrorResponse(
            status=exc.status_code,
            message="APIException: " + str(exc.detail),
            error=ErrorData(
                title=kasa_exceptions.InternalServerError.title,
                description=kasa_exceptions.InternalServerError.description,
                code=str(exc.default_code).upper()),
        )

    set_rollback()
    response = _kasa_exception_handler(exc, context)

    if settings.TESTING or settings.APP_ENVIRONMENT.is_local:
        if not response:
            return None  # Let an Exception raise

    if _is_error(response):
        if settings.SENTRY_ENABLED:
            capture_exception(exc)
        if settings.ELASTIC_APM_ENABLED:
            client.capture_exception()

    if response:
        return response

    return APIErrorResponse(
        message=str(exc),
        error=kasa_exceptions.InternalServerError.default_error_object(),
    )


def _convert_to_manageable(exc):
    if isinstance(exc, (drf_exceptions.AuthenticationFailed, drf_exceptions.NotAuthenticated)):
        return kasa_exceptions.UnauthorizedError(
            message=str(exc),
            title='인증에 실패하였습니다.',
            description='인증이 필요한 작업입니다.',
        )
    if isinstance(exc, (django_exceptions.PermissionDenied, drf_exceptions.PermissionDenied)):
        return kasa_exceptions.ForbiddenError(
            message=str(exc),
            title='권한이 없습니다.',
            description='권한이 필요한 작업입니다.',
        )
    return exc


def _kasa_exception_handler(exc, _context) -> Optional[APIErrorResponse]:
    if not isinstance(exc, kasa_exceptions.KasaAPIException):
        return None
    return APIErrorResponse(
        status=exc.status_code,
        message=exc.message,
        error=exc.error,
    )


def _is_error(response: Optional[APIErrorResponse]) -> bool:
    if not response:
        return True

    if response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        return True
    return False
