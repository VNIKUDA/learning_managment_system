from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

# Create your views here.
class HomeView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "core/home.html"

    def get_queryset(self):
        if self.request.user.role == "teacher":
            return Course.objects.filter(teacher=self.request.user)
        else:
            return Course.objects.filter(students=self.request.user)