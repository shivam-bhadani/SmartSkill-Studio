from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from core.mixins import BaseResponseMixin
from .permissions import (
    IsInstructorOrReadOnly,
    IsInstructorOrReadOnlyEnrolled,
    IsCourseOwnerOrReadOnly,
    IsInstructorOrReadOnlyEnrolledObj,
    IsCourseEnrolledOrReadOnly, 
    IsOwnerOrReadOnly
)
from .models import Course, CourseReview, CourseNotice
from .serializers import CourseSerializer, CourseReviewSerializer, CourseNoticeSerializer


class CourseListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly, IsInstructorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    

class CourseRetrieveUpdateDestroyView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCourseOwnerOrReadOnly]


class CourseReviewListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCourseEnrolledOrReadOnly]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseReview.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(course=course, user=self.request.user)
    

class CourseReviewRetrieveUpdateDestroyView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseReview.objects.filter(course=course)
    

class CourseNoticeListCreateView(BaseResponseMixin, generics.ListCreateAPIView):
    serializer_class = CourseNoticeSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnlyEnrolled]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseNotice.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(course=course)
    

class CourseNoticeRetrieveUpdateDestroyView(BaseResponseMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseNoticeSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnlyEnrolledObj]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseNotice.objects.filter(course=course)
    

