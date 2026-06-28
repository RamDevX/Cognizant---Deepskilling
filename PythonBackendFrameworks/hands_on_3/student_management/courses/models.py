from django.db import models

# Create your models here.
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100)
    head_of_department = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    credits = models.IntegerField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="courses"
    )

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    enrollment_year = models.IntegerField()
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="students"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )
    enrollment_date = models.DateField()
    grade = models.CharField(
        max_length=2,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"{self.student} - {self.course}"