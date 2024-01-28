from django.db import models
from core.models import TimeStampAndUUIModel
from accounts.models import User

def upload_thumbnail(instance, filename):
    return "user/{0}/course_thumbnail/{1}".format(instance.instructor.id, filename)

class Course(TimeStampAndUUIModel):
    instructor = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to=upload_thumbnail, default='default_thumbnail.png')
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
    
class CourseReview(TimeStampAndUUIModel):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()

    def __str__(self):
        return f"{self.course} <-> {self.rating} <-> {self.comment}"
    
class CourseNotice(TimeStampAndUUIModel):
    course = models.ForeignKey(Course, related_name='notices', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.course} <-> {self.title}"