from django.db import models
from core.models import TimeStampAndUUIModel
from accounts.models import User

class Course(TimeStampAndUUIModel):
    instructor = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title
    
class CourseThumbnail(TimeStampAndUUIModel):
    course = models.ForeignKey(Course, related_name='thumbnail_s3', on_delete=models.CASCADE)
    bucket = models.CharField(max_length=40)
    key = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.course} <-> {self.key}"
    
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