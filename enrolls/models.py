from django.db import models
from accounts.models import User
from courses.models import Course

class Enroll(models.Model):
    user = models.ForeignKey(User, related_name='enrolls', on_delete=models.DO_NOTHING)
    course = models.ForeignKey(Course, related_name='enrolls', on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user