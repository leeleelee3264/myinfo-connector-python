import requests
import structlog
from rest_framework.response import Response

logger = structlog.getLogger()
SINGPASS_SERVICE_LOG_EVENT = "singpass_api_service"


class SingpassService:

    def post(self, url: str, header, body) -> Response:
        try:
            api_response = requests.post(
                url=url,
                headers=header,
                data=body,
            )
        except requests.exceptions.RequestException as re:
            logger.error(SINGPASS_SERVICE_LOG_EVENT, data=str(re))
            api_response.raise_for_status()

        return api_response

    def get(self, url: str, header, params=None) -> Response:
        try:
            api_response = requests.get(
                url=url,
                headers=header,
                params=params,
            )
        except requests.exceptions.RequestException as re:
            logger.error(SINGPASS_SERVICE_LOG_EVENT, data=str(re))
            api_response.raise_for_status()

        return api_response
