from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .exceptions import *

def get_error_response(message="Bad Request", http_status=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": False,
        "message": message
    }, status=http_status)


def custom_exception_handler(exc, context):
    if isinstance(exc, PermissionDeniedException) or isinstance(exc, InternalServerException):
        return get_error_response(message=str(exc.detail), http_status=exc.status_code)
    if isinstance(exc, UnauthorizedException) or isinstance(exc, AuthenticationFailed):
        return get_error_response(message="Authentication credentials were not provided or are invalid.", http_status=exc.status_code)
    return exception_handler(exc, context)