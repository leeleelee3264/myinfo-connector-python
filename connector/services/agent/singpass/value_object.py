from dataclasses import dataclass

from jwcrypto import jwk

from domain.oauth import AccessToken


@dataclass
class MyinfoApiKey:
    app_id: str
    client_id: str
    client_secret: str


@dataclass
class MyinfoAccessToken:
    sub: str
    access_token: AccessToken
    token_type: str
    attributes: str


PrivateKey = jwk.JWK
PublicKey = jwk.JWK

DecryptedPersonData = str
DecodedPersonData = dict

SINGAPORE_CITIZEN = 'S'
SINGAPORE_PERMANENT_RESIDENT = 'T'


@dataclass(frozen=True)
class MyinfoPersonOutput:
    name: str
    dob: str
    birthcountry: str
    nationality: str
    uinfin: str
    sex: str
    regadd: dict
    noa_basic: int
    noa_basic_year: str
    decrypted_person_data: str
