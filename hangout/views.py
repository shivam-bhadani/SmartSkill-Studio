from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer
from .permissions import IsCourseEnroll

class CourseHangoutView(generics.ListAPIView):
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, IsCourseEnroll]

    def get_queryset(self):
        chats = Chat.objects.filter(course=self.kwargs['course_id'])
        return chats
    