from abc import (
    ABC,
    abstractmethod,
)

from domain.oauth.dto.sign_up import (
    MyinfoAuthoriseRedirectUrlData,
    MyinfoPersonData,
)


class OauthSignupService(ABC):

    @abstractmethod
    def get_data(self, code: str) -> MyinfoPersonData:
        pass

    @abstractmethod
    def get_authorise_url(self) -> MyinfoAuthoriseRedirectUrlData:
        pass
