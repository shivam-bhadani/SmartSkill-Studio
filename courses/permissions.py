from rest_framework import permissions
from enrolls.models import Enroll
from django.shortcuts import get_object_or_404
from .models import Course


INSTRUCTOR = 1
STUDENT = 2


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and obj.user == request.user


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role==INSTRUCTOR


class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role==INSTRUCTOR
    

class IsInstructorOrReadOnlyEnrolled(permissions.BasePermission):
    def has_permission(self, request, view):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated and Enroll.objects.filter(user=user, course=course).exists():
                return True
        return request.user.is_authenticated and request.user == course.instructor
    
class IsInstructorOrReadOnlyEnrolledObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated and Enroll.objects.filter(user=user, course=course).exists():
                return True
        return request.user.is_authenticated and request.user == course.instructors 


class IsCourseEnrolledOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and Enroll.objects.filter(user=request.user, course=course).exists()


class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.instructor
    

class IsCourseOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user == obj.instructor


class IsCourseOwnerOrReadOnlyEnrolled(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated and Enroll.objects.filter(user=user, course=course).exists():
                return True
        
        return request.user.is_authenticated and request.user == course.instructor
