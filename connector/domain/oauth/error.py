class MyinfoServiceError(Exception):

    def __init__(self, description=''):
        self.description = description

    message = 'Myinfo Registration is not available. Please use another registration.'


class InvalidMyinfoSignature(MyinfoServiceError):
    pass
