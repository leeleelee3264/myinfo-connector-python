from domain.oauth.dto.sign_up import (
    MyinfoAuthoriseRedirectUrlData,
    MyinfoPersonData,
)
from services.users import const


class ExternalMyinfoResponseBuilder:

    def build_myinfo_auth_url_res(self, req: MyinfoAuthoriseRedirectUrlData) -> dict:
        return {
            const.AUTHORISE_URL: req.url,
            const.AUTHORISE_STATE: req.state,
        }

    def build_myinfo_person_res(self, myinfo_person: MyinfoPersonData) -> dict:

        return {
            const.REGADD: myinfo_person.regadd,
            const.DOB: myinfo_person.dob,
            const.SEX: myinfo_person.sex,

            const.NAME: myinfo_person.name,

            const.BIRTHCOUNTRY: myinfo_person.birthcountry,
            const.NATIONALITY: myinfo_person.nationality,
            const.UINFIN: myinfo_person.uinfin,
            const.NOA_BASIC: myinfo_person.noa_basic,
        }
