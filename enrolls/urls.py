from django.urls import path
from .views import EnrollListCreateView

urlpatterns = [
    path('', EnrollListCreateView.as_view(), name='enroll_list_create')
]
