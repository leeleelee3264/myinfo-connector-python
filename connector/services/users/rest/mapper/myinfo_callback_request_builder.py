from services.users import const


class MyinfoCallbackRequestBuilder:

    def build_myinfo_callback_query_option(self, query_params) -> str:
        return query_params.get(const.AUTHORISE_CODE)
