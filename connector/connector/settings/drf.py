################################################################
#
# https://www.django-rest-framework.org/
# https://github.com/davesque/django-rest-framework-simplejwt
#

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'EXCEPTION_HANDLER': 'utils.exceptions.handlers.custom_exception_handler',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
