from django.db import models


# Create your models here.
class StudentLeave(models.Model):
    roll_number = models.CharField(max_length=6, unique=True)
    full_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    semester = models.PositiveBigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=50)
    reason = models.TextField()
    guardian_contact = models.CharField(max_length=14)
    student_mail = models.EmailField()
    is_delete = models.BooleanField(default=False)
    deleted_time = models.DateTimeField(null = True)


