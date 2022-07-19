from __future__ import annotations

from enum import Enum
from functools import wraps
from typing import (
    List,
    Optional,
    Tuple,
    Type,
)

from jsonschema import (
    FormatChecker,
    validate,
)
from jsonschema.exceptions import ValidationError

from utils.exceptions import InvalidParamError


def validate_request(body_schema=None, query_params_schema=None, path_variable_schema=None, multipart_body=False):
    """
    validate a request with the specified schema

    see https://json-schema.org/understanding-json-schema/reference/index.html

    Note that `multipart_body` must be true if and only if used with `utils.multipart.parse_multipart`
    """
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            assert any([body_schema, query_params_schema, path_variable_schema])
            _, request = args
            try:
                if body_schema:
                    data = request.parsed_post.get('json', {}) if multipart_body else request.data
                    validate(data, body_schema, format_checker=FormatChecker())
                if query_params_schema:
                    validate(dict(request.query_params), query_params_schema, format_checker=FormatChecker())
                if path_variable_schema:
                    validate(kwargs, path_variable_schema, format_checker=FormatChecker())
            except ValidationError as e:
                path_str = ".".join([str(path) for path in e.path])
                error_msg = f'path: {path_str}, error: {e.message}' if len(e.path) else e.message
                raise InvalidParamError(message=error_msg) from e

            return func(*args, **kwargs)
        return decorator
    return wrapper


MAX_BIGINT = 9223372036854775807
MAX_BIGUINT = 18446744073709551615

UUID_REGEX = r'^[0-9a-fA-F]{8}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{4}\-?[0-9a-fA-F]{12}$'
RRN_REGEX = r'^\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])-[0-49]\d{6}$'
PHONENUMBER_REGEX = r'^(\+82|0)1\d{8,9}$'
INTERNATIONAL_PHONENUMBER_REGEX = r"^\+[1-9]\d{1,14}$"
EMAIL_REGEX = r'[^@]+@[^@]+\.[^@]+'

# https://wiki.kasa.network/display/KB/DABS+ID
DABS_CODE_REGEX = r"[A-Z]{2}[0-9]{3}[A-Z][0-9]{8}"

UUID_SCHEMA = {
    'type': 'string',
    'pattern': UUID_REGEX,
}


ADDRESS_SCHEMA = {
    'type': 'object',
    'properties': {
        'type': {
            'type': 'string',
            'enum': ['j', 'r'],
        },
        'street': {
            'type': 'string',
        },
        'detailed': {
            'type': 'string',
        },
        'postalCode': {
            'type': 'string',
            'pattern': r'^\d{5}$',
        },
    },
    'required': ['type', 'street', 'detailed', 'postalCode'],
    'additionalProperties': False,
}

INTERNATIONAL_ADDRESS_SCHEMA = {
    "type": "object",
    "properties": {
        "address1": {
            "type": "string",
        },
        "address2": {
            "type": "string",
        },
        "countryCode": {
            "type": "string",
        },
        "city": {
            "type": "string",
        },
        "postalCode": {
            "type": "string",
        },
    },
    "required": ["address1", "countryCode", "city", "postalCode"],
    "additionalProperties": False,
}

EMAIL_SCHEMA = {
    'type': 'string',
    'format': 'email',
}

PHONENUMBER_SCHEMA = {
    'type': 'string',
    'pattern': PHONENUMBER_REGEX,
}

SWIFT_CODE_SCHEMA = {
    'type': 'string',
    'minLength': 8,
    'maxLength': 11,
}


class JsonSchema(dict):
    def __init__(self, initial=None, **kwargs):
        initial = dict(initial or {}, **kwargs)

        super().__init__({k: v for k, v in initial.items() if v is not None})

    def __setitem__(self, key, value):
        if value is not None:
            super().__setitem__(key, value)

    def nullable(self) -> JsonSchema:
        return JsonSchema.oneOf(self, JsonSchema.null())

    @classmethod
    def allOf(cls, *args: dict) -> JsonSchema:
        return JsonSchema(allOf=list(args))

    @classmethod
    def oneOf(cls, *args: dict) -> JsonSchema:
        return JsonSchema(oneOf=list(args))

    @classmethod
    def anyOf(cls, *args: dict) -> JsonSchema:
        return JsonSchema(anyOf=list(args))

    @classmethod
    def null(cls) -> JsonSchema:
        return JsonSchema(type='null')

    @classmethod
    def from_enum(cls, enum: Type[Enum]) -> JsonSchema:
        return cls.string_enum([e.value for e in enum])

    @classmethod
    def string_enum(cls, list: List[str]) -> JsonSchema:
        return JsonSchema(type='string', enum=list)

    @classmethod
    def from_integer_enum(cls, enum: Type[Enum]) -> JsonSchema:
        return cls.integer_enum([e.value for e in enum])

    @classmethod
    def integer_enum(cls, list: List[str]) -> JsonSchema:
        return JsonSchema(type='integer', enum=list)

    @classmethod
    def enum_from_choices(cls, choices: List[Tuple]) -> JsonSchema:
        return cls.string_enum([c[0] for c in choices])

    @classmethod
    def string(
        cls,
        min_length: Optional[int] = 0,
        max_length: Optional[int] = None,
        format: Optional[str] = None,
        pattern: Optional[str] = None,
    ) -> JsonSchema:
        return JsonSchema({
            'type': 'string',
            'minLength': min_length,
            'maxLength': max_length,
            'format': format,
            'pattern': pattern,
        })

    @classmethod
    def uri(cls) -> JsonSchema:
        return cls.string(format='uri')

    @classmethod
    def email(cls, **kwargs) -> JsonSchema:
        return cls.string(**kwargs, format='email')

    @classmethod
    def date_string(cls) -> JsonSchema:
        return cls.string(format='date')

    @classmethod
    def datetime_string(cls) -> JsonSchema:
        return cls.string(format='date-time')

    @classmethod
    def uuid(cls) -> JsonSchema:
        return cls.string(pattern=UUID_REGEX)

    @classmethod
    def phonenumber(cls) -> JsonSchema:
        return cls.string(pattern=PHONENUMBER_REGEX)

    @classmethod
    def international_phonenumber(cls) -> JsonSchema:
        return cls.string(pattern=INTERNATIONAL_PHONENUMBER_REGEX)

    @classmethod
    def swift_code(cls) -> JsonSchema:
        return JsonSchema(SWIFT_CODE_SCHEMA)

    @classmethod
    def dabs_code(cls) -> JsonSchema:
        return cls.string(min_length=14, max_length=14)

    @classmethod
    def address(cls) -> JsonSchema:
        return JsonSchema(ADDRESS_SCHEMA)

    @classmethod
    def object(cls, properties: dict, required: Optional[List[str]] = None, additional_properties=False) -> JsonSchema:
        return JsonSchema({
            'type': 'object',
            'properties': properties,
            'required': required,
            'additionalProperties': additional_properties,
        })

    @classmethod
    def array(cls,
              items: dict = None,
              min_items: int = None,
              max_items: int = None,
              unique_items: bool = False):
        return JsonSchema(type='array', items=items, minItems=min_items, maxItems=max_items, uniqueItems=unique_items)

    @classmethod
    def integer(
        cls,
        minimum: Optional[int] = None,
        maximum: Optional[int] = MAX_BIGUINT,
        exclusive_minimum: Optional[int] = None,
        exclusive_maximum: Optional[int] = None,
    ) -> JsonSchema:
        return JsonSchema({
            'type': 'integer',
            'minimum': minimum,
            'maximum': maximum,
            'exclusiveMinimum': exclusive_minimum,
            'exclusiveMaximum': exclusive_maximum,
        })

    @classmethod
    def integer_string(cls) -> JsonSchema:
        return cls.string(pattern=r'^\d+$')

    @classmethod
    def number(
        cls,
        minimum: Optional[float] = None,
        maximum: Optional[float] = MAX_BIGUINT,
        exclusive_minimum: Optional[float] = None,
        exclusive_maximum: Optional[float] = None,
        multiple_of: Optional[float] = None,
    ) -> JsonSchema:
        return JsonSchema({
            'type': 'number',
            'minimum': minimum,
            'maximum': maximum,
            'exclusiveMinimum': exclusive_minimum,
            'exclusiveMaximum': exclusive_maximum,
            'multipleOf': multiple_of,
        })

    @classmethod
    def boolean(cls) -> JsonSchema:
        return JsonSchema(type='boolean')
