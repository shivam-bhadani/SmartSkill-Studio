from rest_framework.exceptions import APIException
from rest_framework import status 

class PermissionDeniedException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You are not allowed to perform this action."


class UnauthorizedException(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication credentials were not provided or are invalid."


class InternalServerException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_code = "Internal Server Error"
