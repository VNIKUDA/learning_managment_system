from django.contrib import admin
from courses.models import Course, Module, Lesson, Material

# Register your models here.
admin.site.register(Course)
admin.site.register(Module)

class MaterialInLine(admin.TabularInline):
    model = Material
    fields = ["file"]
    extra = 1

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [MaterialInLine]