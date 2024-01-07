from django.contrib import admin
from .models import Course, CourseReview, CourseNotice

admin.site.register(CourseReview)
admin.site.register(CourseNotice)
admin.site.register(Course)