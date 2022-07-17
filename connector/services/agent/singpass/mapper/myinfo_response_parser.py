import json
from typing import Union

from jwcrypto import (
    jwk,
    jwt,
)
from jwcrypto.common import JWException

from services.agent.singpass import error
from services.agent.singpass.value_object import (
    DecodedPersonData,
    DecryptedPersonData,
    MyinfoAccessToken,
    PrivateKey,
    PublicKey,
)


class MyinfoResponseParser:

    def __init__(self, attributes: str):
        self._attributes = attributes.split(',')
        self._parse_attribute()

    def _parse_attribute(self):
        self._name = self._attributes[0]
        self._date_of_birth = self._attributes[1]
        self._birth_country = self._attributes[2]
        self._nationality = self._attributes[3]
        self._uinfin = self._attributes[4]
        self._sex = self._attributes[5]
        self._registered_address = self._attributes[6]
        self._notice_of_assessment = self._attributes[7]

    def build_token_res(
            self,
            payload,
            myinfo_public_key: str,
    ) -> MyinfoAccessToken:

        key = self._get_key(myinfo_public_key)

        try:
            data = self._decode(payload.get('access_token'), key=key)

        except JWException as e:
            raise error.AccessTokenInternalServerError(str(e))
        except (AttributeError, ValueError) as e:
            raise error.AccessTokenInternalServerError(str(e))

        return MyinfoAccessToken(
            sub=str(data.get('sub')),
            access_token=payload.get('access_token'),
            token_type=payload.get('token_type'),
            attributes=payload.get('scope'),
        )

    def _get_key(self, key: str) -> Union[PrivateKey, PublicKey]:
        encode_key = key.encode('utf-8')
        key_dict = jwk.JWK.from_pem(encode_key)

        return key_dict

    def _decode(
            self,
            encoded_payload: DecryptedPersonData,
            key: PublicKey,
    ) -> DecodedPersonData:

        token = jwt.JWT()
        token.deserialize(jwt=encoded_payload, key=key)

        data = token.claims
        data_dict = json.loads(data)

        return data_dict
