from rest_framework import serializers
from .models import *
from enrolls.models import Enroll
from accounts.models import User

class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = '__all__'
        read_only_fields = ['course', 'user']

class CourseThumbnailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseThumbnail
        fields = '__all__'
        read_only_fields = ['course']

class CourseNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseNotice
        fields = '__all__'
        read_only_fields = ['course']

class CourseInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]

class CourseSerializer(serializers.ModelSerializer):
    enrolled = serializers.SerializerMethodField()
    instructor = CourseInstructorSerializer(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor']

    def get_enrolled(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user = request.user
            return Enroll.objects.filter(user=user, course=obj).exists()
        return False
