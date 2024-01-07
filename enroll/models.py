from django.db import models
from account.models import User
from course.models import Course

class Enroll(models.Model):
    user = models.ForeignKey(User, related_name='enrolls', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='enrolls', on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user