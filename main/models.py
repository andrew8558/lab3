from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Room(models.Model):
    number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(399)])
    is_profile = models.BooleanField()


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)


class Class(models.Model):
    number = models.IntegerField()
    letter = models.CharField(max_length=1)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)


class Student(models.Model):
    genders = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=genders)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)


class Discipline(models.Model):
    name = models.CharField(max_length=100)


class Course(models.Model):
    subject = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)


class Schedule(models.Model):
    numbers = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7')
    ]
    date = models.DateField()
    lesson_number = models.IntegerField(choices=numbers)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Grade(models.Model):
    grades = [
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ]
    grade = models.IntegerField(choices=grades)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Course, on_delete=models.CASCADE)
