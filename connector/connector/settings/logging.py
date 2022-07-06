import logging
from typing import Dict

import structlog
from structlog import DropEvent
from structlog.contextvars import merge_contextvars
from structlog.processors import _json_fallback_handler

from utils.json import JSONEncoder

from . import (
    DEBUG,
)
from .env import (
    ENV,
    TESTING,
)


class LogJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return _json_fallback_handler(obj)


if TESTING:
    logging.disable(logging.CRITICAL)

LOG_LEVEL = ENV.str('LOG_LEVEL', 'WARN')  # NOTSET, DEBUG, INFO, WARN, ERROR, FATAL
LOG_BODY = ENV.bool('LOG_BODY', False)
LOG_ENCRYPTED_BODY = ENV.bool('LOG_ENCRYPTED_BODY', False)
STAFF_AUDIT_LOGGER = 'oc_staff_audit'
INVESTOR_AUDIT_LOGGER = 'investor_audit'

LOGGING: Dict = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json_formatter': {
            '()': structlog.stdlib.ProcessorFormatter,
            'processor': structlog.processors.JSONRenderer(ensure_ascii=False, cls=LogJSONEncoder, default=None),
        },
    },
    'handlers': {
        'plain_console': {
            'class': 'logging.StreamHandler',
        },
        'json_console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json_formatter',
        },
    },
    'loggers': {}
}

LOGGING['loggers'] = {
    'connector': {
        'handlers': ['json_console'],
        'level': LOG_LEVEL,
    },
    'services': {
        'handlers': ['json_console'],
        'level': LOG_LEVEL,
    },
    'domain': {
        'handlers': ['json_console'],
        'level': LOG_LEVEL,
    },
    'utils': {
        'handlers': ['json_console'],
        'level': LOG_LEVEL,
    },
    STAFF_AUDIT_LOGGER: {
        'handlers': ['json_console'],
        'level': LOG_LEVEL,
    },
    INVESTOR_AUDIT_LOGGER: {
        'handlers': ['json_console'],
        'level': LOG_LEVEL,
    },
}


def _microseconds_time(_logger, _method_name, event_dict):
    event_dict['time'] = int(event_dict['time'] * 1000)
    return event_dict


def _level_number_to_level(_logger, _method_name, event_dict):
    event_dict['level'] = event_dict.pop('level_number')
    return event_dict


# http://www.structlog.org/en/stable/processors.html#filtering
class PathDropper:
    """
    Place after `merge_contextvars` in ordering of `processors`.
    """

    def __init__(self, *path_to_drop: str):
        self.paths_to_drop = set(path_to_drop)

    def __call__(self, logger, method_name, event_dict):
        if event_dict.get('req') and event_dict['req'].get('path') in self.paths_to_drop:
            raise DropEvent
        return event_dict


class ExceptionFormatter:
    def __init__(self, key: str):
        self.key = key

    def __call__(self, logger, method_name, event_dict):
        if self.key not in event_dict:
            return event_dict

        if isinstance(event_dict[self.key], dict):
            return event_dict

        if isinstance(event_dict[self.key], str):
            event_dict[self.key] = {'value': event_dict[self.key]}
        elif isinstance(event_dict[self.key], Exception):
            e = event_dict[self.key]
            event_dict[self.key] = {
                'type': e.__class__.__name__,
                'str': str(e),
            }
        return event_dict


structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        merge_contextvars,
        PathDropper('/', '/status'),
        structlog.processors.TimeStamper(key='time'),
        _microseconds_time,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level_number,
        _level_number_to_level,
        ExceptionFormatter('err'),
        ExceptionFormatter('error'),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.ExceptionPrettyPrinter(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    context_class=structlog.threadlocal.wrap_dict(dict),
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
