import json

import structlog
from requests.exceptions import HTTPError

from domain import oauth as domain
from domain.oauth.services.sign_up import OauthSignupService
from services.agent.singpass import error
from services.agent.singpass.apps import (
    APP_ID,
    CLIENT_ID,
    CLIENT_SECRET,
    ENDPOINT,
    KASA_PRIVATE_KEY,
    MYINFO_PUBLIC_KEY,
    REDIRECT_URL,
    REQUEST_ATTRIBUTES,
)
from services.agent.singpass.mapper.myinfo_request_builder import MyinfoRequestBuilder
from services.agent.singpass.mapper.myinfo_response_parser import MyinfoResponseParser
from services.agent.singpass.singpass_api_call_mixin import SingpassApiMixIn

logger = structlog.getLogger()
MYINFO_SERVICE_LOG_EVENT = "myinfo_service"


class MyinfoSignupService(OauthSignupService, SingpassApiMixIn):

    def __init__(self):
        super().__init__()

        self._req_builder = MyinfoRequestBuilder()
        self._res_parser = MyinfoResponseParser()

    def get_data(
            self,
            code: str,
    ) -> domain.MyinfoPersonData:

        access_token = self._get_access_token(code)

        return self._get_person_data(access_token)

    def _get_access_token(self, code: str) -> domain.MyinfoAccessTokenData:

        url = ENDPOINT + '/token'

        auth = self._req_builder.build_token_auth_header(
            endpoint=url,
            api_key=self._get_api_key(),
            code=code,
            redirect_uri=REDIRECT_URL,
            private_key=KASA_PRIVATE_KEY,
        )

        body = {
            'code': code,
            'client_secret': CLIENT_SECRET,
            'client_id': CLIENT_ID,
            'redirect_uri': REDIRECT_URL,
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
                myinfo_public_key=MYINFO_PUBLIC_KEY,
            )

            return token

        except HTTPError as e:
            logger.error(f'{MYINFO_SERVICE_LOG_EVENT} token',
                         message=f'status: {e.response.status_code}, msg={e.response.content}')

            raise error.AccessTokenBadRequest(e)

    def _get_person_data(self, token: domain.MyinfoAccessTokenData) -> domain.MyinfoPersonData:

        url = ENDPOINT + '/person' + '/' + token.sub + '/'

        auth = self._req_builder.build_person_auth_header(
            endpoint=url,
            api_key=self._get_api_key(),
            attributes=REQUEST_ATTRIBUTES,
            private_key=KASA_PRIVATE_KEY,
        )

        final_auth = f'{auth},Bearer {token.access_token}'

        params = {
            'client_id': CLIENT_ID,
            'attributes': REQUEST_ATTRIBUTES,
        }

        try:
            response = self.get(
                url=url,
                query_params=params,
                authorization=final_auth,
            )

            payload = response.content.decode('utf-8')

            person = self._res_parser.build_person_res(
                payload=payload,
                kasa_private_key=KASA_PRIVATE_KEY,
                myinfo_public_key=MYINFO_PUBLIC_KEY,
            )

            return person

        except HTTPError as e:
            logger.error(f'{MYINFO_SERVICE_LOG_EVENT} person',
                         message=f'status: {e.response.status_code}, msg={e.response.content}')

            raise error.PersonBadRequest(e)

    def get_authorise_url(self) -> domain.MyinfoAuthoriseRedirectUrlData:

        url = ENDPOINT + '/authorise'

        return self._req_builder.build_authorise_url(
            endpoint=url,
            api_key=self._get_api_key(),
            attributes=REQUEST_ATTRIBUTES,
            redirect_uri=REDIRECT_URL,
        )

    def _get_api_key(self) -> domain.ApiKey:
        return domain.ApiKey(
            app_id=APP_ID,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
        )
