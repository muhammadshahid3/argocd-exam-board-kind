from django.urls import path
from . import views

urlpatterns = [
    path("", views.result_list, name="result_list"),
    path("add/", views.select_student, name="select_student"),
    path("add/<int:student_id>/", views.add_result, name="add_result"),
    path("final/", views.final_result, name="final_result"),
]
