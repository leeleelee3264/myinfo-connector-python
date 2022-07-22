from services.users import const
from utils.validation import JsonSchema

GET_MYINFO_QUERY_PARAMS_SCHEMA = JsonSchema.object(
    {
        const.AUTHORISE_CODE: JsonSchema.array(JsonSchema.string(), max_items=1),
    },
)

GET_MYINFO_CALLBACK_QUERY_PARAMS_SCHEMA = JsonSchema.object(
    {
        const.AUTHORISE_CODE: JsonSchema.array(JsonSchema.string(), max_items=1),
        const.AUTHORISE_STATE: JsonSchema.array(JsonSchema.string(), max_items=1),
    },
)
