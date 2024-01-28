from django.contrib import admin
from .models import Course, CourseNotice, CourseReview

admin.site.register(Course)
admin.site.register(CourseNotice)
admin.site.register(CourseReview)