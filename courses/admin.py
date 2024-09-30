from django.contrib import admin
import nested_admin
from courses.models import Course, Module, Lesson, Material, Task, Completion, CompletionFile, Grade

# Register your models here.
admin.site.register(Completion)
admin.site.register(CompletionFile)
admin.site.register(Grade)

class MaterialInline(nested_admin.NestedTabularInline):
    model = Material
    fields = ["file"]
    extra = 0

class TaskInline(nested_admin.NestedTabularInline):
    model = Task
    fields = ["name", "description"]
    extra = 0

class LessonInline(nested_admin.NestedTabularInline):
    model = Lesson
    fields = ["title", "description"]
    inlines = [MaterialInline, TaskInline]
    extra = 0


class ModuleInline(nested_admin.NestedTabularInline):
    model = Module
    fields = ["name"]
    inlines = [LessonInline]
    extra = 0

@admin.register(Course)
class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [ModuleInline]
    list_display = ("name", "description", "join_code")
    readonly_fields = ('join_code',)