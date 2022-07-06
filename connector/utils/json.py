from enum import Enum

from rest_framework.utils.encoders import JSONEncoder as RestJSONEncoder

from serializer import JsonSerializable


class JSONEncoder(RestJSONEncoder):
    def default(self, obj):

        if isinstance(obj, JsonSerializable):
            return obj.serialize()
        if isinstance(obj, Enum):
            return obj.value

        return super().default(obj)
