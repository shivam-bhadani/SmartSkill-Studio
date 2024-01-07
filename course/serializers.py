from rest_framework import serializers
from .models import Course, CourseReview, CourseNotice
from enroll.models import Enroll

class CourseReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = '__all__'
        read_only_fields = ['course']

class CourseNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseNotice
        fields = '__all__'
        read_only_fields = ['course']

class CourseSerializer(serializers.ModelSerializer):
    enrolled = serializers.SerializerMethodField()
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