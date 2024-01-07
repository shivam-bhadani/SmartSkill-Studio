from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import (
    IsInstructorOrReadOnly,
    IsInstructorOrReadOnlyEnrolled,
    IsCourseOwnerOrReadOnly, 
    IsCourseEnrolledOrReadOnly, 
    IsOwnerOrReadOnly
)
from .models import Course, CourseReview, CourseNotice
from .serializers import CourseSerializer, CourseReviewSerializer, CourseNoticeSerializer


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly, IsInstructorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)
    

class CourseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer 
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticatedOrReadOnly, IsCourseOwnerOrReadOnly]


class CourseReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCourseEnrolledOrReadOnly]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseReview.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(course=course)
    

class CourseReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseReview.objects.filter(course=course)
    
    def perform_update(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(course=course)
    

class CourseNoticeListCreateView(generics.ListCreateAPIView):
    serializer_class = CourseNoticeSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnlyEnrolled]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseNotice.objects.filter(course=course)
    
    def perform_create(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(course=course)
    

class CourseNoticeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseNoticeSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrReadOnly]

    def get_queryset(self):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        return CourseNotice.objects.filter(course=course)
    
    def perform_update(self, serializer):
        course = get_object_or_404(Course, pk=self.kwargs['course_id'])
        serializer.save(course=course)

