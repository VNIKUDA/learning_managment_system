from django.urls import path
from courses import views

urlpatterns = [
    path("create/", views.CourseCreateView.as_view(), name="course-create"),
    path("<int:pk>/", views.CourseHomeView.as_view(), name="course-detail"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course-update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course-delete"),

    path("join/", views.JoinCourseView.as_view(), name="join-course"),
    path("leave/<int:pk>/", views.LeaveCourseView.as_view(), name="leave-course"),

    path("student-courses/", views.StudentCourses.as_view(), name="student-courses"),
    path("teacher-courses/", views.TeacherCourses.as_view(), name="teacher-courses"),

    path("<int:pk>/module-create/", views.ModuleCreateView.as_view(), name="module-create"),
    path("module/<int:pk>/update/", views.ModuleUpdateView.as_view(), name="module-update"),
    path("module/<int:pk>/delete/", views.ModuleDeleteView.as_view(), name="module-delete"),

    path("module/<int:pk>/lesson-create/", views.LessonCreateView.as_view(), name="lesson-create"),
    path("lesson/<int:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),
    path("lesson/<int:pk>/update/", views.LessonUpdateView.as_view(), name="lesson-update"),
    path("lesson/<int:pk>/delete/", views.LessonDeleteView.as_view(), name="lesson-delete"),

    path("lesson/<int:pk>/materials-create/", views.MaterialsCreateView.as_view(), name="materials-create"),
    path("material/<int:pk>/delete/", views.MaterialDeleteView.as_view(), name="material-delete"),

    path("lesson/<int:pk>/task-create/", views.TaskCreateView.as_view(), name="task-create"),

    path("task/<int:pk>/complete/", views.CompletionCreateView.as_view(), name="completion-create"),
    path("task/<int:pk>/delete-completion/", views.CompletionDeleteView.as_view(), name="completion-delete")
]

app_name = "courses"