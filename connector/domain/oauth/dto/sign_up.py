from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class MyinfoAuthoriseRedirectUrlData:
    state: UUID
    url: str


@dataclass
class MyinfoAccessTokenData:
    sub: str
    access_token: str
    token_type: str
    attributes: str


@dataclass(frozen=True)
class MyinfoPersonData:
    name: str
    dob: str
    birthcountry: str
    nationality: str
    uinfin: str
    sex: str
    regadd: dict
    noa_basic: int


DecryptedPersonData = str
DecodedPersonData = dict
