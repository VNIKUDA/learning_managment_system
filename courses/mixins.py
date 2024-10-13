from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http.response import HttpResponseRedirect
from courses import models

class UserIsTeacher(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.is_teacher


class TeacherIsCourseOwner(UserIsTeacher):
    def has_permission(self) -> bool:
        if super(TeacherIsCourseOwner, self).has_permission():
            instance = self.get_object()

            if isinstance(instance, models.Course):
                return instance.teacher == self.request.user
            
            elif isinstance(instance, models.Module) or isinstance(instance, models.Lesson):
                return instance.course.teacher == self.request.user
            
            elif isinstance(instance, models.Task) or isinstance(instance, models.Material):
                return instance.lesson.course.teacher == self.request.user
            
            elif isinstance(instance, models.Completion):
                return instance.task.lesson.course.teacher == self.request.user

            elif isinstance(instance, models.Grade):
                return instance.completion.task.lesson.course.teacher == self.request.user

        return False

class UserIsCourseStudent(PermissionRequiredMixin):
    def has_permission(self) -> bool:
        return self.request.user in self.get_course().students.all()

class UserIsCompletionOwner(PermissionRequiredMixin):
    def has_permission(self) -> bool:
        completion = self.get_object()

        return completion.student == self.request.user