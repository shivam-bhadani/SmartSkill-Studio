import uuid
from decouple import config
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from core.s3 import S3
from core.exceptions import BadRequestException
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
    

class CourseThumbnailUploadPresignedURLCreateView(BaseResponseMixin, generics.CreateAPIView):
    s3 = S3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'), config('AWS_S3_REGION_NAME'))
    def create(self, request, *args, **kwargs):
        try:
            bucket = config('AWS_S3_BUCKET_NAME')
            request_body = request.data
            file_name = request_body.get('file_name', None)
            file_type = request_body.get('file_type', None)
            if file_name is None or file_type not in ["image/jpeg", "image/png"]:
                raise BadRequestException()
            unique_image_name = f"course_thumbnail/{uuid.uuid4()}_{file_name}"
            presigned_url = self.s3.generate_upload_presigned_url(unique_image_name, file_type, bucket)
            return self.get_success_response({
                'url': presigned_url, 
                'file_name': unique_image_name
            })
        except Exception as e:
            raise BadRequestException()


class CourseThumbnailViewPresignedURLCreateView(BaseResponseMixin, generics.CreateAPIView):
    s3 = S3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'), config('AWS_S3_REGION_NAME'))
    def create(self, request, *args, **kwargs):
        try:
            bucket = config('AWS_S3_BUCKET_NAME')
            request_body = request.data
            file_key = request_body.get('file_key', None)
            if file_key is None:
                raise BadRequestException()
            presigned_url = self.s3.generate_read_presigned_url(file_key, bucket)
            return self.get_success_response({
                'url': presigned_url
            })
        except Exception as e:
            raise BadRequestException()