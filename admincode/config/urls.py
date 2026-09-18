from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("django-admin/", admin.site.urls),

    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False)),

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("dashboard/", include("core.urls")),
    path("students/", include("students.urls")),
    path("classes/", include("classes_app.urls")),
    path("sections/", include("sections.urls")),
    path("subjects/", include("subjects.urls")),
    path("results/", include("results.urls")),
]
