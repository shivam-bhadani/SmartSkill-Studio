from django.urls import path
from .views import CourseHangoutView

urlpatterns = [
    path('<int:course_id>/', CourseHangoutView.as_view(), name='course_hangout_view')
]
