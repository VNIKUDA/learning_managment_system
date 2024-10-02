from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, View
from courses.mixins import UserIsStaff
from courses.forms import CompletionForm
from courses.models import Course, Module, Lesson, Material, Completion, CompletionFile, Task

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
    

class CourseDeleteView(UserIsStaff, DeleteView):
    model = Course
    http_method_names = ["post"]
    success_url = reverse_lazy("home")


class CourseUpdateView(UserIsStaff, UpdateView):
    model = Course
    fields = ["name", "description", "color"]
    context_object_name = "course"
    template_name = "courses/course_update.html"
    
    def get_success_url(self) -> str:
        course = self.get_object()
        return reverse_lazy("courses:course-detail", kwargs={"pk": course.pk})


class CourseHomeView(DetailView):
    model = Course
    context_object_name = "course"
    template_name = "courses/course_home.html"

    def get_template_names(self) -> list[str]:
        if self.request.user.is_staff or self.get_object().teacher == self.request.user:
            return ["courses/teacher_course_home.html"]
        
        return super().get_template_names()


class JoinCourseView(View):
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        join_code = self.request.POST.get("join_code")

        course: Course = list(filter(lambda course: course.join_code == join_code, Course.objects.all()))[0]
        course.students.add(self.request.user)

        return redirect(reverse_lazy("courses:course-detail", kwargs={"pk": course.pk}))


class LeaveCourseView(View):
    http_method_names = ["post"]

    def post(self, *args, **kwargs):
        course_pk = self.kwargs.get("pk")

        course: Course = Course.objects.get(pk=course_pk)
        course.students.remove(self.request.user)

        return redirect("home")

class ModuleCreateView(CreateView):
    model = Module
    fields = ["name"]
    http_method_names = ["post"]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.course = Course.objects.get(pk=self.kwargs.get("pk"))

        return super().form_valid(form)

    def get_success_url(self) -> str:
        course = Course.objects.get(pk=self.kwargs.get("pk"))
        return reverse_lazy("courses:course-detail", kwargs={"pk": course.pk})


class ModuleUpdateView(UpdateView):
    model = Module
    fields = ["name"]
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        return reverse_lazy("courses:course-detail", kwargs={"pk": self.get_object().course.pk})


class ModuleDeleteView(DeleteView):
    model = Module
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        return reverse_lazy("courses:course-detail", kwargs={"pk": self.get_object().course.pk})


class LessonCreateView(CreateView):
    model = Lesson
    fields = ["title", "description"]
    template_name = "courses/lesson_create.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.module = Module.objects.get(pk=self.kwargs.get("pk"))

        self.object = form.instance
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("courses:lesson-detail", kwargs={"pk": self.object.pk})


class LessonDetailView(DetailView):
    model = Lesson
    context_object_name = "lesson"
    template_name = "courses/lesson_detail.html"

    def get_template_names(self) -> list[str]:
        if self.request.user.role == "teacher":
            return ["courses/teacher_lesson_detail.html"]

        return super().get_template_names()


class LessonDeleteView(DeleteView):
    model = Lesson
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        return reverse_lazy("courses:course-detail", kwargs={"pk": self.get_object().course.pk})
    

class LessonUpdateView(UpdateView):
    model = Lesson
    fields = ["title", "description"]
    context_object_name = "lesson"
    template_name = "courses/lesson_update.html"

    def get_success_url(self) -> str:
        return reverse_lazy("courses:lesson-detail", kwargs={"pk": self.get_object().pk})


class MaterialsCreateView(View):
    http_method_names = ["post"]

    def get_lesson(self):
        return Lesson.objects.get(pk=self.kwargs.get("pk"))

    def post(self, *args, **kwargs):
        lesson = self.get_lesson()

        for file in self.request.FILES.getlist("files"):
            Material.objects.create(lesson=lesson, file=file)

        return redirect(reverse_lazy("courses:lesson-detail", kwargs={"pk": lesson.pk}))


class MaterialDeleteView(DeleteView):
    model = Material
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        return reverse_lazy("courses:lesson-detail", kwargs={"pk": self.get_object().lesson.pk})
    

class TaskCreateView(CreateView):
    model = Task
    fields = ["name", "description"]
    http_method_names = ["post"]
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.lesson = Lesson.objects.get(pk=self.kwargs.get("pk"))

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy("courses:lesson-detail", kwargs={"pk": self.kwargs.get("pk")})


class TaskUpdateView(UpdateView):
    model = Task
    fields = ["name", "description"]
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        return reverse_lazy("courses:lesson-detail", kwargs={"pk": self.get_object().lesson.pk})


class TaskDeleteView(DeleteView):
    model = Task
    http_method_names = ["post"]

    def get_success_url(self) -> str:
        return reverse_lazy("courses:lesson-detail", kwargs={"pk": self.get_object().lesson.pk})


class CompletionCreateView(CreateView):
    model = Completion
    fields = ["text"]
    http_method_names = ["post"]

    def get_task(self):
        return Task.objects.get(pk=self.kwargs.get("pk"))

    def get_success_url(self) -> str:
        task = self.get_task()

        return reverse_lazy("courses:lesson-detail", kwargs={"pk": task.lesson.pk})

    def form_valid(self, form: BaseModelForm):
        form.instance = form.save(commit=False)

        form.instance.student = self.request.user
        form.instance.task = self.get_task()
        
        completion = form.save(commit=True)

        for file in self.request.FILES.getlist("files"):
            CompletionFile.objects.create(completion=completion, file=file)

        return super().form_valid(form)
    

class CompletionDeleteView(DeleteView):
    model = Completion
    http_method_names = ["post"]
    
    def get_task(self):
        return Task.objects.get(pk=self.kwargs.get("pk"))
    
    def get_object(self) -> Model:
        return Completion.objects.get(task=self.get_task(), student=self.request.user)

    def get_success_url(self) -> str:
        task = self.get_task()

        return reverse_lazy("courses:lesson-detail", kwargs={"pk": task.lesson.pk})
    

class StudentCourses(View):
    def get(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == "XMLHttpRequest":
            courses = Course.objects.filter(students=self.request.user)
            context = {"courses": courses}

            return render(self.request, "courses/user_courses.html", context=context)
        else:
            raise PermissionDenied
        

class TeacherCourses(View):
    def get(self, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == "XMLHttpRequest":
            courses = Course.objects.filter(teacher=self.request.user)
            context = {"courses": courses}

            return render(self.request, "courses/user_courses.html", context=context)
        else:
            raise PermissionDenied