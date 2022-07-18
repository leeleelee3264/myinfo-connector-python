from domain.oauth import (
    AuthCode,
    MyinfoAuthoriseRedirectUrl,
    MyinfoPerson,
)
from domain.oauth.error import MyinfoServiceError
from domain.oauth.services.sign_up import OauthSignupService as Service
from services.agent.singpass import error as service_error


class SingpassSignUpUseCase:

    def __init__(self, service: Service) -> None:
        self._myinfo_service = service

    def get_authorise_url(self) -> MyinfoAuthoriseRedirectUrl:
        return self._myinfo_service.get_authorise_url()

    def get_person(self, code: AuthCode) -> MyinfoPerson:

        try:
            return self._get_person_from_myinfo(code)
        except service_error.MyinfoError as e:
            raise MyinfoServiceError(description=e.description) from e

    def _get_person_from_myinfo(self, code: AuthCode) -> MyinfoPerson:

        return self._myinfo_service.get_data(code)
