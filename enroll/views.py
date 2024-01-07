from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Enroll
from .serializers import EnrollSerializer

class EnrollListCreateView(generics.ListCreateAPIView):
    serializer_class = EnrollSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        enrolls = Enroll.objects.filter(user=self.request.user)
        return enrolls

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = EnrollSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
