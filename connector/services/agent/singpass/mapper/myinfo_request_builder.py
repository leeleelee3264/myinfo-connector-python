import uuid

from domain.oauth import MyinfoAuthoriseRedirectUrl
from services.agent.singpass.value_object import MyinfoApiKey


class MyinfoRequestBuilder:

    def build_authorise_url(
            self,
            endpoint: str,
            api_key: MyinfoApiKey,
            attributes: str,
            redirect_uri: str,
    ) -> MyinfoAuthoriseRedirectUrl:

        state = uuid.uuid4()

        url = f'{endpoint}' \
              f'?client_id={api_key.client_id}' \
              f'&attributes={attributes}' \
              f'&state={state}' \
              f'&redirect_uri={redirect_uri}' \
              f'&purpose=Demonstrating MyInfo APIs'

        return MyinfoAuthoriseRedirectUrl(
            state=state,
            url=url,
        )
