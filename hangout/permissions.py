from rest_framework import permissions
from django.shortcuts import get_object_or_404
from courses.models import Course
from enrolls.models import Enroll

class IsCourseEnroll(permissions.BasePermission):
    def has_permission(self, request, view):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        return request.user.is_authenticated and Enroll.objects.filter(user=request.user, course=course).exists()