from django.shortcuts import render
from rest_framework.views import APIView

from services.users.json_schema import GET_MYINFO_CALLBACK_QUERY_PARAMS_SCHEMA
from services.users.rest.mapper.myinfo_callback_request_builder import MyinfoCallbackRequestBuilder
from utils.validation import validate_request


class MyinfoCallbackView(APIView):

    def __init__(self):
        super().__init__()
        self._req_builder = MyinfoCallbackRequestBuilder()

    @validate_request(query_params_schema=GET_MYINFO_CALLBACK_QUERY_PARAMS_SCHEMA)
    def get(self, request):

        code = self._req_builder.build_myinfo_callback_query_option(request.query_params)
        context = {
            'code': code,
        }

        return render(request, 'users/index.html', context)
