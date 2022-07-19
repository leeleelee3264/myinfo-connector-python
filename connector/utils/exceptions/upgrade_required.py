from rest_framework import status

from utils.exceptions import KasaAPIException


class UpgradeRequiredError(KasaAPIException):
    status_code = status.HTTP_426_UPGRADE_REQUIRED
    message = 'Required upgrade.'
    code = 'UPGRADE_REQUIRED'
    title = '앱 업데이트가 필요합니다.'
    description = '카사 서비스의 원활한 이용을 위해 앱 업데이트를 해주세요.'
