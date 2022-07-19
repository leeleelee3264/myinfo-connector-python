from rest_framework import status
from rest_framework.views import APIView

from domain.oauth.error import MyinfoServiceError
from domain.oauth.use_cases.sign_up import SingpassSignUpUseCase
from services.agent.singpass.myinfo_sign_up import MyinfoSignupService
from services.users.json_schema import GET_MYINFO_QUERY_PARAMS_SCHEMA
from services.users.rest.mapper.external_myinfo_request_builder import ExternalMyinfoRequestBuilder
from services.users.rest.mapper.external_myinfo_response_builder import ExternalMyinfoResponseBuilder
from utils.exceptions import InternalServerError
from utils.response import APIResponse
from utils.validation import validate_request


class ExternalMyinfoView(APIView):

    def __init__(self):
        super().__init__()

        self._res_builder = ExternalMyinfoResponseBuilder()
        self._req_builder = ExternalMyinfoRequestBuilder()

        self._use_case = SingpassSignUpUseCase(
            service=MyinfoSignupService(),
        )

    @validate_request(query_params_schema=GET_MYINFO_QUERY_PARAMS_SCHEMA)
    def get(self, request):
        code = self._req_builder.build_myinfo_person_query_option(request.query_params)

        try:
            myinfo_person = self._use_case.get_person(code)
        except MyinfoServiceError as e:
            raise InternalServerError(message=e.message, description=e.description) from e

        response_data = self._res_builder.build_myinfo_person_res(myinfo_person)

        return APIResponse(
            status.HTTP_200_OK,
            message='OK',
            data=response_data,
        )
