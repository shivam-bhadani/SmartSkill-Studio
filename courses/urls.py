from django.urls import path
from .views import (
    CourseListCreateView,
    CourseRetrieveUpdateDestroyView,
    CourseReviewListCreateView,
    CourseReviewRetrieveUpdateDestroyView,
    CourseNoticeListCreateView,
    CourseNoticeRetrieveUpdateDestroyView
)

urlpatterns = [
    path('', CourseListCreateView.as_view(), name='course_list_create'),
    path('<int:pk>/', CourseRetrieveUpdateDestroyView.as_view(), name='course_detail'),

    path('<int:course_id>/reviews/', CourseReviewListCreateView.as_view(), name='course_review_list_create'),
    path('<int:course_id>/reviews/<int:pk>/', CourseReviewRetrieveUpdateDestroyView.as_view(), name='course_review_detail'),

    path('<int:course_id>/notices/', CourseNoticeListCreateView.as_view(), name='course_notice_list_create'),
    path('<int:course_id>/notices/<int:pk>/', CourseNoticeRetrieveUpdateDestroyView.as_view(), name='course_notice_detail'),
]
