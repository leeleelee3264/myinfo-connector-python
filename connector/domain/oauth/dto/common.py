from dataclasses import dataclass

from jwcrypto import jwk


@dataclass
class ApiKey:
    app_id: str
    client_id: str
    client_secret: str


PrivateKey = jwk.JWK
PublicKey = jwk.JWK

Authorization = str
Signature = str
