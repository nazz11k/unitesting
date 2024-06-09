from django.db import models
from login.models import User


class Group(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['user']), models.Index(fields=['group'])]

    def __str__(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return self.user.get_full_name()


class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    groups = models.ManyToManyField(Group)

    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()

    class Meta:
        indexes = [models.Index(fields=['name'])]

    def __str__(self):
        return self.name


class CourseElement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['name']), models.Index(fields=['course']), models.Index(fields=['description'])]

    def __str__(self):
        return self.name


class Lecture(CourseElement):
    file = models.FileField(upload_to='lectures/', null=True, blank=True)

    @property
    def file_name(self):
        return self.file.name.split('/')[-1]

    @property
    def file_url(self):
        return self.file.url


class Task(CourseElement):
    max_score = models.FloatField()
    deadline = models.DateTimeField()
    test_file = models.FileField(upload_to='tasks/', null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['max_score'])]

    @property
    def test_file_name(self):
        return self.test_file.name.split('/')[-1]

    @property
    def test_file_url(self):
        return self.test_file.url


class Solution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.FloatField()
    solution = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['task']), models.Index(fields=['student']), models.Index(fields=['score'])]

    def get_student(self):
        return self.student

    def get_student_name(self):
        return self.student.user.get_full_name()

    @property
    def points(self):
        return self.score
    