from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework import status
from rest_framework.response import Response

class BaseResponseMixin:
    def get_success_response_no_content(self, http_status=status.HTTP_204_NO_CONTENT):
        return Response({ 
            "status": True,
            "data": {}
        }, status=http_status)
    
    def get_success_response(self, data, http_status=status.HTTP_200_OK):
        return Response({
            "status": True,
            "data": data
        }, status=http_status)
    
    def get_error_response(self, err, http_status=status.HTTP_400_BAD_REQUEST):
        return Response({
            "status": False,
            "error": err
        }, status=http_status)
    
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
            return self.get_success_response(response.data)
        except PermissionDenied as e:
            return self.get_error_response(str(e), status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return self.get_error_response(str(e))
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            return self.get_success_response(response.data, status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return self.get_error_response("Object not found", status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return self.get_error_response(str(e), status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return self.get_error_response(str(e))
        
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            return self.get_success_response(response.data)
        except ObjectDoesNotExist:
            return self.get_error_response("Object not found", status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return self.get_error_response(str(e), status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return self.get_error_response(str(e))
    
    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return self.get_success_response_no_content()
        except ObjectDoesNotExist:
            return self.get_error_response("Object not found", status.HTTP_404_NOT_FOUND)
        except PermissionDenied as e:
            return self.get_error_response(str(e), status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return self.get_error_response(str(e))
        