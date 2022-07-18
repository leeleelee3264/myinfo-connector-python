from datetime import datetime

from domain import oauth as domain
from domain.oauth import Gender
from services.agent.singpass.value_object import MyinfoPersonOutput


class _Mapper:

    @staticmethod
    def to_myinfo_person(
            myinfo_output: MyinfoPersonOutput,
    ) -> domain.MyinfoPerson:

        name_parts = myinfo_output.name.rsplit(" ", 1)

        first_name = name_parts[0]
        last_name = ''
        if len(name_parts) > 1:
            last_name = name_parts[1]

        date_of_birth = datetime.strptime(myinfo_output.dob, '%Y-%m-%d').date()
        gender = Gender(myinfo_output.sex.lower())

        block = myinfo_output.regadd.get('block').get('value')
        street = myinfo_output.regadd.get('street').get('value')

        floor = myinfo_output.regadd.get('floor').get('value')
        unit = myinfo_output.regadd.get('unit').get('value')
        building = myinfo_output.regadd.get('building').get('value')

        country_code = myinfo_output.regadd.get('country').get('code')

        city = ''
        if country_code == 'SG':
            city = 'Singapore'

        address1 = f'{block} {street}'
        address2 = f'{floor} {unit} {building}'

        address = {
            'address1': address1,
            'address2': address2,
            'city': city,
            'countryCode': country_code,
            'postalCode': myinfo_output.regadd.get('postal').get('value'),
        }

        return domain.MyinfoPerson(

            address=address,
            date_of_birth=date_of_birth,
            gender=gender,

            name=myinfo_output.name,
            first_name=first_name,
            last_name=last_name,

            country_of_birth=myinfo_output.birthcountry,
            nationality=myinfo_output.nationality,

            identification_number=myinfo_output.uinfin,

            annual_income={
                'display': myinfo_output.noa_basic,
                'year': myinfo_output.noa_basic_year,
            },
        )
