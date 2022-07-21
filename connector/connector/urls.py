"""connector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include,  path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.http import JsonResponse
from django.urls import (
    include,
    path,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND

from utils.exceptions import InternalServerError
from utils.exceptions.handlers import custom_exception_handler

urlpatterns = [
    path('', include('services.health_check.urls')),
    path('', include('services.users.urls')),
]


if settings.DEBUG:
    @api_view(['POST'])
    def echo(request):
        return Response(request.data)

    urlpatterns.append(path('echo', echo, name='echo'))


def not_found(request, exception, *args, **kwargs):  # pylint: disable=unused-argument
    # The body should be empty to be consistent with alb's fixed response
    return JsonResponse(data={}, status=HTTP_404_NOT_FOUND)


def internal_server_error(request, *args, **kwargs):  # pylint: disable=unused-argument
    """ Handler for uncaught exception.

    * https://docs.djangoproject.com/en/2.2/topics/http/urls/#error-handling
    * https://docs.djangoproject.com/en/2.2/ref/views/#the-500-server-error-view
    * https://docs.djangoproject.com/en/2.2/ref/urls/#handler500
    """
    r = custom_exception_handler(InternalServerError(), None)
    return JsonResponse(data=r.data,
                        status=r.status_code,
                        json_dumps_params={'ensure_ascii': False})


handler404 = not_found
handler500 = internal_server_error
