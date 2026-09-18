from django.urls import path
from . import views

urlpatterns = [
    path("", views.class_list, name="class_list"),
    path("add/", views.class_create, name="class_create"),
    path("<int:pk>/edit/", views.class_update, name="class_update"),
    path("<int:pk>/delete/", views.class_delete, name="class_delete"),
]
