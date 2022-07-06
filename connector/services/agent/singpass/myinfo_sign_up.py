from domain import oauth as domain
from domain.oauth.services.sign_up import OauthSignupService


class MyinfoSignupService(OauthSignupService):

    def get_data(self, code: domain.AuthCode) -> domain.MyinfoPerson:
        pass

    def get_authorise_url(self) -> domain.MyinfoAuthoriseRedirectUrl:
        pass
