import json

import structlog
from django.conf import settings
from requests.exceptions import HTTPError

from domain import oauth as domain
from domain.oauth.services.sign_up import OauthSignupService
from services.agent.singpass import error
from services.agent.singpass.mapper.myinfo_mapper import _Mapper
from services.agent.singpass.mapper.myinfo_request_builder import MyinfoRequestBuilder
from services.agent.singpass.mapper.myinfo_response_parser import MyinfoResponseParser
from services.agent.singpass.singpass_api_call_mixin import SingpassApiMixIn
from services.agent.singpass.value_object import (
    MyinfoAccessToken,
    MyinfoApiKey,
)

logger = structlog.getLogger()
MYINFO_SERVICE_LOG_EVENT = "myinfo_service"


class MyinfoSignupService(OauthSignupService, SingpassApiMixIn):

    def __init__(self):
        super().__init__()

        self.__init__myinfo_setting()

        self._mapper = _Mapper()
        self._req_builder = MyinfoRequestBuilder()
        self._res_parser = MyinfoResponseParser(self._requested_attributes)

    # def get_data(
    #         self,
    #         code: domain.AuthCode,
    # ) -> domain.MyinfoPerson:
    #
    #     access_token = self._get_access_token(code)
    #     person_output = self._get_person_data(access_token)
    #
    #     return self._map_data(person_output)

    def _get_access_token(self, code: domain.AuthCode) -> MyinfoAccessToken:

        url = self._endpoint + '/token'

        auth = self._req_builder.build_token_auth_header(
            endpoint=url,
            api_key=self._get_api_key(),
            code=code,
            redirect_uri=self._redirect_uri,
            private_key=self._kasa_private_key,
        )

        body = {
            'code': code,
            'client_secret': self._client_secret,
            'client_id': self._client_id,
            'redirect_uri': self._redirect_uri,
            'grant_type': 'authorization_code',
        }

        try:
            response = self.post(
                url=url,
                body=body,
                authorization=auth,
                content_type='application/x-www-form-urlencoded',
            )

            payload = json.loads(response.content.decode('utf-8'))

            token = self._res_parser.build_token_res(
                payload=payload,
                myinfo_public_key=self._myinfo_public_key,
            )

            return token

        except HTTPError as e:
            logger.error(MYINFO_SERVICE_LOG_EVENT,
                         message=f'status: {e.response.status_code}, msg={e.response.content}')

            raise error.AccessTokenBadRequest(e)

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
