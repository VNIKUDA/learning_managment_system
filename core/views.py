from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import ListView
from courses.models import Course

# Create your views here.
class HomeView(ListView):
    model = Course
    context_object_name = "courses"
    template_name = "core/home.html"

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user)