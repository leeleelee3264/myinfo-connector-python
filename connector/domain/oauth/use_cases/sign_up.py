from domain.oauth import MyinfoAuthoriseRedirectUrl
from domain.oauth.services.sign_up import OauthSignupService as Service


class SingpassSignUpUseCase:

    def __init__(self, service: Service) -> None:
        self._myinfo_service = service

    def get_authorise_url(self) -> MyinfoAuthoriseRedirectUrl:
        return self._myinfo_service.get_authorise_url()

    # def get_person(self, ):
