import json
from typing import Union

from jwcrypto import (
    jwe,
    jwk,
    jwt,
)
from jwcrypto.common import JWException

from domain.oauth import dto as domain
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
    ) -> domain.MyinfoAccessTokenData:

        key = self._get_key(myinfo_public_key)

        try:
            data = self._decode(payload.get('access_token'), key=key)

        except JWException as e:
            raise error.AccessTokenInternalServerError(str(e))
        except (AttributeError, ValueError) as e:
            raise error.AccessTokenInternalServerError(str(e))

        return domain.MyinfoAccessTokenData(
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

    ) -> domain.MyinfoPersonData:

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
            decoded_payload: domain.DecodedPersonData,
    ) -> domain.MyinfoPersonData:

        return domain.MyinfoPersonData(
            name=decoded_payload.get(self._name).get('value'),
            dob=decoded_payload.get(self._date_of_birth).get('value'),
            birthcountry=decoded_payload.get(self._birth_country).get('code'),
            nationality=decoded_payload.get(self._nationality).get('code'),
            uinfin=decoded_payload.get(self._uinfin).get('value'),
            sex=decoded_payload.get(self._sex).get('code'),
            regadd=decoded_payload.get(self._registered_address),
            noa_basic=decoded_payload.get(self._notice_of_assessment).get('amount').get('value'),
            noa_basic_year=decoded_payload.get(self._notice_of_assessment).get('yearofassessment').get('value'),
        )

    def _verify_person_data(
            self,
            payload,
            kasa_private_key: str,
            myinfo_public_key: str,
    ) -> domain.DecodedPersonData:

        decrypt_key = self._get_key(kasa_private_key)
        decode_key = self._get_key(myinfo_public_key)

        decrypted_payload = self._decrypt(payload, key=decrypt_key)
        decoded_payload = self._decode(decrypted_payload, key=decode_key)

        return decoded_payload

    def _get_key(self, key: str) -> Union[domain.PrivateKey, domain.PublicKey]:
        encode_key = key.encode('utf-8')
        key_dict = jwk.JWK.from_pem(encode_key)

        return key_dict

    def _decode(
            self,
            encoded_payload: domain.DecryptedPersonData,
            key: domain.PublicKey,
    ) -> domain.DecodedPersonData:

        token = jwt.JWT()
        token.deserialize(jwt=encoded_payload, key=key)

        data = token.claims
        data_dict = json.loads(data)

        return data_dict

    def _decrypt(
            self,
            encrypted_payload: str,
            key: domain.PrivateKey,
    ) -> domain.DecryptedPersonData:

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
