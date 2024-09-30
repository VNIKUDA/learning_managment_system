from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()

def course_color():
    COLOR_CHOICES = [
        "danger",
        "primary",
        "success",
        "info",
        "dark"
    ]

    return random.choice(COLOR_CHOICES)


# Create your models here.
class Course(models.Model):
    COLOR_CHOICES = (
        ("danger", "червоний"),
        ("primary", "синій"),
        ("success", "зелений"),
        ("info", "голубий"),
        ("dark", "чорний")
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_courses", limit_choices_to={"role": "teacher"})
    students = models.ManyToManyField(
        User,
        related_name="student_courses", 
        limit_choices_to={"role": "student"}, 
        blank=True
    )
    color = models.CharField(default=course_color, choices=COLOR_CHOICES, max_length=10)

    @property
    def join_code(self):
        random.seed(self.pk)
        characters = string.ascii_letters + string.digits

        code = "".join(random.choice(characters) for _ in range(8))
        return code

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

    def delete(self, *args, **kwargs):
        for material in self.materials.all():
            material.delete()

        return super(Lesson, self).delete(*args, **kwargs)

    @property
    def course(self):
        return self.module.course

    def __str__(self):
        return self.title


class Material(models.Model):
    file = models.FileField(upload_to="materials/")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="materials")

    @property
    def name(self):
        return self.file.name.split("/")[-1]

    def delete(self, *args, **kwargs):
        self.file.delete(False)

        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.lesson} - {self.file.name}"


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks")

    def __str__(self) -> str:
        return self.name
    
    @property
    def students(self):
        return [completion.student for completion in Completion.objects.filter(task=self)]


class Completion(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "student"})
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="completions")
    text = models.TextField(blank=True)

    def delete(self, *args, **kwargs):
        for completion_file in self.files.all():
            completion_file.delete()

        return super(Completion, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.task} - {self.student}"


class CompletionFile(models.Model):
    file = models.FileField(upload_to="completions/")
    completion = models.ForeignKey(Completion, on_delete=models.CASCADE, related_name="files")

    def delete(self, *args, **kwargs):
        self.file.delete(False)
        return super(CompletionFile, self).delete(*args, **kwargs)
    
    @property
    def name(self):
        return self.file.name.split("/")[-1]

    def __str__(self) -> str:
        return self.file.name


class Grade(models.Model):
    grade = models.PositiveIntegerField(default=0)
    completion = models.OneToOneField(Completion, on_delete=models.CASCADE, related_name="grade")

    def __str__(self) -> str:
        return f"{self.completion}: {self.grade}"