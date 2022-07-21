from django.http import JsonResponse

from utils.exceptions import CustomAPIException
from utils.exceptions.handlers import custom_exception_handler


class CustomExceptionHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, CustomAPIException):
            r = custom_exception_handler(exception, None)
            return JsonResponse(data=r.data,
                                status=r.status_code,
                                json_dumps_params={'ensure_ascii': False})
        return None
