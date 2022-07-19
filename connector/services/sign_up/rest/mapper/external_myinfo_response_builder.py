from domain.oauth.dto.sign_up import MyinfoAuthoriseRedirectUrlData
from services.sign_up import const


class ExternalMyinfoResponseBuilder:

    def build_myinfo_auth_url_res(self, req: MyinfoAuthoriseRedirectUrlData) -> dict:
        return {
            const.AUTHORISE_URL: req.url,
            const.AUTHORISE_STATE: req.state,
        }
