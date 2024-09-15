from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from courses.mixins import UserIsStaff
from courses.models import Course, Module, Lesson

# Create your views here.
class CourseCreateView(UserIsStaff, CreateView):
    model = Course
    fields = ["name", "description"]
    template_name = "courses/course_create.html"

    def form_valid(self, form):
        form.instance.teacher = self.request.user

        self.object = form.instance
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy("courses:course-detail", kwargs={"pk": self.object.pk})
    

class CourseHomeView(DetailView):
    model = Course
    context_object_name = "course"
    template_name = "courses/course_home.html"


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = "lesson"
    template_name = "courses/lesson_detail.html"