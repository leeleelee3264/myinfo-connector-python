import base64
import time
import uuid

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

from domain.oauth.dto.common import (
    ApiKey,
    Authorization,
    Signature,
)
from domain.oauth.dto.sign_up import MyinfoAuthoriseRedirectUrlData


class MyinfoRequestBuilder:

    def build_authorise_url(
            self,
            endpoint: str,
            api_key: ApiKey,
            attributes: str,
            redirect_uri: str,
    ) -> MyinfoAuthoriseRedirectUrlData:

        state = uuid.uuid4()

        url = f'{endpoint}' \
              f'?client_id={api_key.client_id}' \
              f'&attributes={attributes}' \
              f'&state={state}' \
              f'&redirect_uri={redirect_uri}' \
              f'&purpose=python-myinfo-connector'

        return MyinfoAuthoriseRedirectUrlData(
            state=state,
            url=url,
        )

    def build_token_auth_header(
            self,
            endpoint: str,
            api_key: ApiKey,
            code: str,
            redirect_uri: str,
            private_key: str,
    ) -> Authorization:
        nonce = uuid.uuid4()
        timestamp = self._get_current_milli_time()

        auth_header_param = f'&app_id={api_key.app_id}' \
                            f'&client_id={api_key.client_id}' \
                            f'&client_secret={api_key.client_secret}' \
                            f'&code={code}' \
                            f'&grant_type=authorization_code' \
                            f'&nonce={nonce}' \
                            f'&redirect_uri={redirect_uri}' \
                            f'&signature_method=RS256' \
                            f'&timestamp={timestamp}'

        raw_auth_header = f'POST&{endpoint}{auth_header_param}'

        signature = self._sign_on_raw_header(
            base_string=raw_auth_header,
            private_key=private_key,
        )

        return self._add_signature_in_header(
            nonce=nonce,
            timestamp=timestamp,
            app_id=api_key.app_id,
            signature=signature,
        )

    def build_person_auth_header(
            self,
            endpoint: str,
            api_key: ApiKey,
            attributes: str,
            private_key: str,
    ) -> Authorization:
        nonce = uuid.uuid4()
        timestamp = self._get_current_milli_time()

        auth_header_param = f'&app_id={api_key.app_id}' \
                            f'&attributes={attributes}' \
                            f'&client_id={api_key.client_id}' \
                            f'&nonce={nonce}' \
                            f'&signature_method=RS256' \
                            f'&timestamp={timestamp}'

        raw_auth_header = f'GET&{endpoint}{auth_header_param}'

        signature = self._sign_on_raw_header(
            base_string=raw_auth_header,
            private_key=private_key,
        )

        return self._add_signature_in_header(
            nonce=nonce,
            timestamp=timestamp,
            app_id=api_key.app_id,
            signature=signature,
        )

    def _add_signature_in_header(
            self,
            nonce: uuid.UUID,
            timestamp: str,
            app_id: str,
            signature: Signature,
    ) -> Authorization:

        return f"PKI_SIGN timestamp=\"{timestamp}" \
               f"\",nonce=\"{nonce}" \
               f"\",app_id=\"{app_id}" \
               f"\",signature_method=\"RS256" \
               f"\",signature=\"{signature}" \
               f"\""

    def _sign_on_raw_header(
            self,
            base_string: str,
            private_key: str,
    ) -> Signature:

        digest = SHA256.new()
        digest.update(
            base_string.encode('utf-8'),
        )

        pk = RSA.importKey(private_key)
        signer = PKCS1_v1_5.new(pk)
        signature = str(base64.b64encode(signer.sign(digest)), 'utf-8')

        return signature

    def _get_current_milli_time(self):
        return str(round(time.time() * 1000))
