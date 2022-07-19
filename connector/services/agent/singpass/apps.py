from django.apps import AppConfig
from django.conf import settings

CLIENT_ID = ''
APP_ID = ''
CLIENT_SECRET = ''

KASA_PRIVATE_KEY = ''
MYINFO_PUBLIC_KEY = ''

ENDPOINT = ''
REDIRECT_URL = ''
REQUEST_ATTRIBUTES = ''


class SingpassAppConfig(AppConfig):
    name = 'services.agent.singpass'
    verbose_name = 'singpass'

    def ready(self):
        global CLIENT_ID
        CLIENT_ID = settings.MYINFO_CLIENT_ID

        global APP_ID
        APP_ID = CLIENT_ID

        global CLIENT_SECRET
        CLIENT_SECRET = settings.MYINFO_CLIENT_SECRET

        global KASA_PRIVATE_KEY
        KASA_PRIVATE_KEY = settings.KASA_GENERATED_PRIVATE_KEY

        global MYINFO_PUBLIC_KEY
        MYINFO_PUBLIC_KEY = settings.MYINFO_GENERATED_PUBLIC_KEY

        global ENDPOINT
        ENDPOINT = settings.MYINFO_HOST

        global REDIRECT_URL
        REDIRECT_URL = settings.KASA_REDIRECT_URL

        global REQUEST_ATTRIBUTES
        REQUEST_ATTRIBUTES = settings.MYINFO_REQUESTED_ATTRIBUTES
