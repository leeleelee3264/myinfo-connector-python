from rest_framework import status
from rest_framework.views import APIView

from utils.response import APIResponse


class HelloView(APIView):

    def get(self, request):

        data = 'Hello world!'

        return APIResponse(
            status.HTTP_200_OK,
            message='Hello',
            data=data,
        )
