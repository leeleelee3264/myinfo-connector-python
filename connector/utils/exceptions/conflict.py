from rest_framework import status

from utils.exceptions import KasaAPIException


class ConflictError(KasaAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = 'Conflict.'
    code = 'CONFLICT'
