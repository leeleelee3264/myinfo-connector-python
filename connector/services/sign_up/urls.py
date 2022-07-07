from django.urls import path

from services.sign_up.rest import ExternalMyinfoRedirectLoginView

urlpatterns = [
    path('sign-up/me/external/myinfo/redirect-login',
         ExternalMyinfoRedirectLoginView.as_view(), name='external-myinfo-redirect-login')
]