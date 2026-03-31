from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    year= models.CharField(max_length=10, blank=True)  

    def __str__(self):
        return self.user.first_name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
 
    
class Subject(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.IntegerField()
    name = models.CharField(max_length=100)
    credits = models.IntegerField() 

    def __str__(self):
        return self.name
    
class Semester_Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    semester = models.IntegerField()
    gpa = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - Sem {self.semester}"