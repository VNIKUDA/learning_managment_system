from django.db import models
from django.contrib.auth import get_user_model
from hashlib import sha3_224

User = get_user_model()

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_courses", limit_choices_to={"role": "teacher"})
    students = models.ManyToManyField(
        User,
        related_name="student_courses", 
        limit_choices_to={"role": "student"}, 
        blank=True
    )

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")

    def __str__(self):
        return self.name

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return self.title


class Material(models.Model):
    file = models.FileField(upload_to="materials/")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="materials")


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    due = models.DateTimeField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks")


class Completion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completions")
    text = models.TextField(blank=True)


class CompletionFile(models.Model):
    file = models.FileField(upload_to="completions/")
    completion = models.ForeignKey(Completion, on_delete=models.CASCADE, related_name="files")


class Grade(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    completion = models.OneToOneField(Completion, on_delete=models.CASCADE, related_name="grade")