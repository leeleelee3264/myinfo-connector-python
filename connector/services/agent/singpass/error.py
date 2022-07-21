class MyinfoError(Exception):
    description = ''


class AccessTokenBadRequest(MyinfoError):
    description = 'Fail to get Myinfo Access Token. Authcode Might be re-used or expired.'


class PersonBadRequest(MyinfoError):
    description = 'Fail to get Myinfo Person data.'


class AccessTokenInternalServerError(MyinfoError):
    description = 'Fail to parse Myinfo Access Token.'


class PersonDataInternalServerError(MyinfoError):
    description = 'Fail to parse Myinfo Person Data.'


class PersonDataInvalid(MyinfoError):
    description = 'Person Data is invalid. Parameters are missing to registry to Kasa.'


class SettingNotFound(MyinfoError):
    description = 'Myinfo setting is not defined, please check server setting.'
