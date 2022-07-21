from rest_framework import status

from utils.exceptions import CustomAPIException


class ConflictError(CustomAPIException):
    status_code = status.HTTP_409_CONFLICT
    message = 'Conflict.'
    code = 'CONFLICT'
