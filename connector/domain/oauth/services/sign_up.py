from abc import (
    ABC,
    abstractmethod,
)

from domain import oauth as domain


class OauthSignupService(ABC):

    # @abstractmethod
    # def get_data(self, code: domain.AuthCode) -> domain.MyinfoPerson:
    #     pass

    @abstractmethod
    def get_authorise_url(self) -> domain.MyinfoAuthoriseRedirectUrl:
        pass
