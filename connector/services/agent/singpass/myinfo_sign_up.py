import structlog
from django.conf import settings

from domain import oauth as domain
from domain.oauth.services.sign_up import OauthSignupService
from services.agent.singpass import error
from services.agent.singpass.mapper.myinfo_mapper import _Mapper
from services.agent.singpass.mapper.myinfo_request_builder import MyinfoRequestBuilder
from services.agent.singpass.mapper.myinfo_response_builder import MyinfoResponseBuilder
from services.agent.singpass.value_object import MyinfoApiKey

logger = structlog.getLogger()
MYINFO_SERVICE_LOG_EVENT = "myinfo_service"


class MyinfoSignupService(OauthSignupService):

    def __init__(self):
        self.__init__myinfo_setting()

        self._mapper = _Mapper()
        self._req_builder = MyinfoRequestBuilder()
        self._res_builder = MyinfoResponseBuilder()

    def get_data(self, code: domain.AuthCode) -> domain.MyinfoPerson:
        pass

    def get_authorise_url(self) -> domain.MyinfoAuthoriseRedirectUrl:

        url = self._endpoint + '/authorise'

        return self._req_builder.build_authorise_url(
            endpoint=url,
            api_key=self._get_api_key(),
            attributes=self._requested_attributes,
            redirect_uri=self._redirect_uri,
        )

    def __init__myinfo_setting(self):
        self._client_id = settings.MYINFO_CLIENT_ID
        self._app_id = self._client_id
        self._client_secret = settings.MYINFO_CLIENT_SECRET

        self._kasa_private_key = settings.KASA_GENERATED_PRIVATE_KEY
        self._myinfo_public_key = settings.MYINFO_GENERATED_PUBLIC_KEY

        self._endpoint = settings.MYINFO_HOST
        self._redirect_uri = settings.KASA_REDIRECT_URL
        self._requested_attributes = settings.MYINFO_REQUESTED_ATTRIBUTES

        self._validate_setting()

    def _validate_setting(self) -> None:
        self._validate_credential_setting()
        self._validate_certification_setting()

    def _validate_credential_setting(self) -> None:
        while True:
            if not self._client_id:
                break
            if not self._client_secret:
                break
            return

        raise error.CredentialNotFoundError

    def _validate_certification_setting(self) -> None:
        while True:
            if not self._kasa_private_key:
                break
            if not self._myinfo_public_key:
                break
            return

        raise error.CertificationNotFoundError

    def _get_api_key(self) -> MyinfoApiKey:
        return MyinfoApiKey(
            app_id=self._app_id,
            client_id=self._client_id,
            client_secret=self._client_secret,
        )
