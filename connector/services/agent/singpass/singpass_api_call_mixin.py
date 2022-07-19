import requests
import structlog
from rest_framework.response import Response

from domain.oauth.dto.common import Authorization

logger = structlog.getLogger()
SINGPASS_SERVICE_LOG_EVENT = "singpass_api_service"


class SingpassApiMixIn:

    def post(
            self,
            url: str,
            body,
            authorization: Authorization,
            content_type: str = 'application/json',
    ) -> Response:

        header = {
            'Content-Type': content_type,
            'Cache-Control': 'no-cache',
            'Authorization': authorization,
        }

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

    def get(
            self,
            url: str,
            query_params,
            authorization: Authorization,
            content_type: str = 'application/json',
    ) -> Response:

        header = {
            'Content-Type': content_type,
            'Cache-Control': 'no-cache',
            'Authorization': authorization,
        }

        try:
            api_response = requests.get(
                url=url,
                headers=header,
                params=query_params,
            )
        except requests.exceptions.RequestException as re:
            logger.error(SINGPASS_SERVICE_LOG_EVENT, data=str(re))

        api_response.raise_for_status()

        return api_response
