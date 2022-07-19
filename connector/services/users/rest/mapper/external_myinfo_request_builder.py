from services.users import const


class ExternalMyinfoRequestBuilder:

    def build_myinfo_person_query_option(self, query_params) -> str:
        return query_params.get(const.AUTHORISE_CODE)
