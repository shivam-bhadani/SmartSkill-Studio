from rest_framework import permissions
from enrolls.models import Enroll
from django.shortcuts import get_object_or_404
from .models import Course
from core.exceptions import *


INSTRUCTOR = 1
STUDENT = 2


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and obj.user == request.user:
            return True
        raise PermissionDeniedException()


class IsInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role==INSTRUCTOR:
            return True
        raise PermissionDeniedException()


class IsInstructorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user.role==INSTRUCTOR:
            return True
        raise PermissionDeniedException()
    

class IsInstructorOrReadOnlyEnrolled(permissions.BasePermission):
    def has_permission(self, request, view):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated and Enroll.objects.filter(user=user, course=course).exists():
                return True
        if request.user.is_authenticated and request.user == course.instructor:
            return True
        raise PermissionDeniedException()
    
class IsInstructorOrReadOnlyEnrolledObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated and Enroll.objects.filter(user=user, course=course).exists():
                return True
        if request.user.is_authenticated and request.user == course.instructors:
            return True
        raise PermissionDeniedException()


class IsCourseEnrolledOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and Enroll.objects.filter(user=request.user, course=course).exists():
            return True
        raise PermissionDeniedException()


class IsCourseOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user == obj.instructor:
            return True
        raise PermissionDeniedException()
    

class IsCourseOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.user == obj.instructor:
            return True
        raise PermissionDeniedException()


class IsCourseOwnerOrReadOnlyEnrolled(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = get_object_or_404(Course, pk=view.kwargs.get('course_id'))
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            if user.is_authenticated and Enroll.objects.filter(user=user, course=course).exists():
                return True
        
        if request.user.is_authenticated and request.user == course.instructor:
            return True
        raise PermissionDeniedException()
