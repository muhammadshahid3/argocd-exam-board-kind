from django.urls import path
from . import views

urlpatterns = [
    path("", views.section_list, name="section_list"),
    path("add/", views.section_create, name="section_create"),
    path("<int:pk>/edit/", views.section_update, name="section_update"),
    path("<int:pk>/delete/", views.section_delete, name="section_delete"),
]
