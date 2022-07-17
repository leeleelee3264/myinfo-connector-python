from dataclasses import dataclass
from datetime import date

from domain.oauth.models.sign_up.value_object import Gender


@dataclass
class MyinfoPerson:
    address: dict
    date_of_birth: date
    gender: Gender

    name: str
    first_name: str
    last_name: str

    country_of_birth: str
    nationality: str

    identification_number: str
    # TODO 다른 타입으로 바꿔야 한다.
    annual_income: dict
