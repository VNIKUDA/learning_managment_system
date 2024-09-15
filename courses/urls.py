from django.urls import path
from courses import views

urlpatterns = [
    path("create/", views.CourseCreateView.as_view(), name="course-create"),
    path("<int:pk>/", views.CourseHomeView.as_view(), name="course-detail"),
    path("lesson/<int:pk>/", views.LessonDetailView.as_view(), name="lesson-detail")
]

app_name = "courses"