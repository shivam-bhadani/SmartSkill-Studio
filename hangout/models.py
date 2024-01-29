from django.db import models
from accounts.models import User
from courses.models import Course

class Chat(models.Model):
    sender = models.ForeignKey(User, related_name='chats', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='hangouts', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.first_name} - {self.course.title}'
