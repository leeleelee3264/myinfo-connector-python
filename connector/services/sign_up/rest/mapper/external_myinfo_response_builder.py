from domain.oauth import MyinfoAuthoriseRedirectUrl
from services.sign_up import const


class ExternalMyinfoResponseBuilder:

    def build_myinfo_auth_url_res(self, req: MyinfoAuthoriseRedirectUrl) -> dict:
        return {
            const.AUTHORISE_URL: req.url,
            const.AUTHORISE_STATE: req.state,
        }
