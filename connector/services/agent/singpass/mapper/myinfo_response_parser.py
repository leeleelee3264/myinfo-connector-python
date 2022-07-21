import json
from typing import Union

from jwcrypto import (
    jwe,
    jwk,
    jwt,
)
from jwcrypto.common import JWException

from domain.oauth.dto.common import (
    PrivateKey,
    PublicKey,
)
from domain.oauth.dto.sign_up import (
    DecodedPersonData,
    DecryptedPersonData,
    JsonPersonData,
    MyinfoAccessTokenData,
    MyinfoPersonData,
)
from services.agent.singpass import error
from services.agent.singpass.apps import REQUEST_ATTRIBUTES


class MyinfoResponseParser:

    def __init__(self):
        self._attributes = REQUEST_ATTRIBUTES.split(',')

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
    ) -> MyinfoAccessTokenData:

        key = self._get_key(myinfo_public_key)

        try:
            data = self._decode(payload.get('access_token'), key=key)

        except JWException as e:
            raise error.AccessTokenInternalServerError(str(e))
        except (AttributeError, ValueError) as e:
            raise error.AccessTokenInternalServerError(str(e))

        return MyinfoAccessTokenData(
            sub=str(data.get('sub')),
            access_token=payload.get('access_token'),
            token_type=payload.get('token_type'),
            attributes=payload.get('scope'),
        )

    def build_person_res(
            self,
            payload,
            kasa_private_key: str,
            myinfo_public_key: str,

    ) -> MyinfoPersonData:

        try:
            data = self._verify_person_data(
                payload=payload,
                kasa_private_key=kasa_private_key,
                myinfo_public_key=myinfo_public_key,
            )
        except JWException as e:
            raise error.PersonDataInternalServerError(str(e))
        except (AttributeError, ValueError) as e:
            raise error.PersonDataInternalServerError(str(e))

        return self._convert_person_data(
            decoded_payload=data,
        )

    def _convert_person_data(
            self,
            decoded_payload: DecodedPersonData,
    ) -> MyinfoPersonData:

        person = JsonPersonData(**decoded_payload)

        return MyinfoPersonData(
            name=person[self._name].get('value'),
            dob=person[self._date_of_birth].get('value'),
            birthcountry=person[self._birth_country].get('code'),
            nationality=person[self._nationality].get('code'),
            sex=person[self._sex].get('code'),
            uinfin=person[self._uinfin].get('value'),
            regadd=person[self._registered_address],
            # noa_basic=decoded_payload.get(self._notice_of_assessment),
        )

    def _verify_person_data(
            self,
            payload,
            kasa_private_key: str,
            myinfo_public_key: str,
    ) -> DecodedPersonData:

        decrypt_key = self._get_key(kasa_private_key)
        decode_key = self._get_key(myinfo_public_key)

        decrypted_payload = self._decrypt(payload, key=decrypt_key)
        decoded_payload = self._decode(decrypted_payload, key=decode_key)

        return decoded_payload

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

        person = DecodedPersonData(**data_dict)
        return person

    def _decrypt(
            self,
            encrypted_payload: str,
            key: PrivateKey,
    ) -> DecryptedPersonData:

        params = self._get_decrypt_params(encrypted_payload)

        encryption = jwe.JWE()
        encryption.deserialize(params, key)

        data = encryption.plaintext
        data_str = json.loads(data)

        return data_str

    def _get_decrypt_params(
            self,
            encrypted_payload: str,
    ) -> str:

        jwe_parts = encrypted_payload.split('.')

        protected = jwe_parts[0]
        encrypted_key = jwe_parts[1]
        iv = jwe_parts[2]
        cipher_text = jwe_parts[3]
        tag = jwe_parts[4]

        return json.dumps({
            'protected': protected,
            'encrypted_key': encrypted_key,
            'iv': iv,
            'ciphertext': cipher_text,
            'tag': tag,
        })
