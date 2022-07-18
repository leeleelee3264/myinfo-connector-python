import json
from typing import (
    Tuple,
    Union,
)

from jwcrypto import (
    jwe,
    jwk,
    jwt,
)
from jwcrypto.common import JWException

from services.agent.singpass import error
from services.agent.singpass.value_object import (
    DecodedPersonData,
    DecryptedPersonData,
    MyinfoAccessToken,
    MyinfoPersonOutput,
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

    def build_person_res(
            self,
            payload,
            kasa_private_key: str,
            myinfo_public_key: str,

    ) -> MyinfoPersonOutput:

        try:
            signature, data = self._verify_person_data(
                payload=payload,
                kasa_private_key=kasa_private_key,
                myinfo_public_key=myinfo_public_key,
            )
        except JWException as e:
            raise error.PersonDataInternalServerError(str(e))
        except (AttributeError, ValueError) as e:
            raise error.PersonDataInternalServerError(str(e))

        return self._convert_person_data(
            signature=signature,
            decoded_payload=data,
        )

    def _convert_person_data(
            self,
            signature: DecryptedPersonData,
            decoded_payload: DecodedPersonData,
    ) -> MyinfoPersonOutput:

        self._validate_with_myinfo_empty_value(decoded_payload)

        return MyinfoPersonOutput(
            name=decoded_payload.get(self._name).get('value'),
            dob=decoded_payload.get(self._date_of_birth).get('value'),
            birthcountry=decoded_payload.get(self._birth_country).get('code'),
            nationality=decoded_payload.get(self._nationality).get('code'),
            uinfin=decoded_payload.get(self._uinfin).get('value'),
            sex=decoded_payload.get(self._sex).get('code'),
            regadd=decoded_payload.get(self._registered_address),
            noa_basic=decoded_payload.get(self._notice_of_assessment).get('amount').get('value'),
            noa_basic_year=decoded_payload.get(self._notice_of_assessment).get('yearofassessment').get('value'),
            decrypted_person_data=signature,
        )

    def _verify_person_data(
            self,
            payload,
            kasa_private_key: str,
            myinfo_public_key: str,
    ) -> Tuple[DecryptedPersonData, DecodedPersonData]:

        decrypt_key = self._get_key(kasa_private_key)
        decode_key = self._get_key(myinfo_public_key)

        decrypted_payload = self._decrypt(payload, key=decrypt_key)
        decoded_payload = self._decode(decrypted_payload, key=decode_key)

        return decrypted_payload, decoded_payload

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

    def _validate_with_myinfo_empty_value(
            self,
            person: DecodedPersonData,
    ) -> None:
        """
        Myinfo에서 정보가 없을 떄 값을 비워서 보내지 않고, UNKOWN 과 같은 dummy 값을 채워서 보내기 떄문에 별도로 확인을 한다.
        """
        addr = person.get(self._registered_address)

        while True:
            if person.get(self._birth_country).get('code') == 'UN':
                break
            if person.get(self._nationality).get('code') == 'UN':
                break
            if len(person.get(self._date_of_birth).get('value')) != 10:
                break
            if person.get(self._sex).get('code') == 'U':
                break
            if addr.get('type') != 'SG':
                break
            if addr.get('postal').get('value') == '':
                break
            if addr.get('country').get('code') == '':
                break
            if addr.get('block').get('value') == '' or addr.get('street').get('value') == '':
                break
            if 'unavailable' in person.get(self._notice_of_assessment):
                break
            return

        raise error.PersonDataInvalid
