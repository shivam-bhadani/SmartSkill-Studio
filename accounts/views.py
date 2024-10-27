from rest_framework import generics
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from core.mixins import BaseResponseMixin
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User

class UserRegistrationAPIView(BaseResponseMixin, generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        if email is None:
            return self.get_error_response()
        if User.objects.filter(email=email).exists():
            return self.get_error_response("User with this email already exists")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = {
                'id': user.id,
                'email': user.email
            }
            return self.get_success_response(user_data, status.HTTP_201_CREATED)
        
        return self.get_error_response()
    

class UserLoginAPIView(BaseResponseMixin, generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is None:
                return self.get_error_response("Email or Password is wrong")
            
            refresh = RefreshToken.for_user(user)
            return self.get_success_response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status.HTTP_200_OK)
        
        return self.get_error_response()