from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from core.mixins import BaseResponseMixin
from .models import Enroll
from .serializers import EnrollSerializer

class EnrollListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Enroll
    serializer_class = EnrollSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
