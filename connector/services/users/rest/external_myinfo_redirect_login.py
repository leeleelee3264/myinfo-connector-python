from rest_framework import status
from rest_framework.views import APIView

from domain.oauth.use_cases.sign_up import SingpassSignUpUseCase
from services.agent.singpass.myinfo_sign_up import MyinfoSignupService
from services.users.rest.mapper.external_myinfo_response_builder import ExternalMyinfoResponseBuilder
from utils.response import APIResponse


class ExternalMyinfoRedirectLoginView(APIView):

    def __init__(self):
        super().__init__()

        self._res_builder = ExternalMyinfoResponseBuilder()

        self._use_case = SingpassSignUpUseCase(
            service=MyinfoSignupService(),
        )

    def get(self, request):
        req = self._use_case.get_authorise_url()

        response_data = self._res_builder.build_myinfo_auth_url_res(req)

        return APIResponse(
            status.HTTP_200_OK,
            message='OK',
            data=response_data,
        )
