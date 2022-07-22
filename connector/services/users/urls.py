from django.urls import path

from services.users.rest import (
    ExternalMyinfoRedirectLoginView,
    ExternalMyinfoView,
    MyinfoCallbackView,
)

urlpatterns = [
    path('users/me/external/myinfo/redirect-login',
         ExternalMyinfoRedirectLoginView.as_view(), name='external-myinfo-redirect-login'),
    path('users/me/external/myinfo', ExternalMyinfoView.as_view(), name='external-myinfo'),

    path('callback', MyinfoCallbackView.as_view(), name='internal-myinfo-redirect'),
]
