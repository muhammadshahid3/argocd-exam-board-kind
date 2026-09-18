from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from core.models import Student
from .forms import StudentForm


@login_required
def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.select_related("school_class", "section").all()
    if query:
        students = students.filter(
            Q(roll_number__icontains=query)
            | Q(name__icontains=query)
            | Q(father_name__icontains=query)
        )
    return render(request, "students/list.html", {"students": students, "query": query})


@login_required
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student created successfully.")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(request, "students/form.html", {"form": form, "title": "Add Student"})


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully.")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)
    return render(request, "students/form.html", {"form": form, "title": "Edit Student"})


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("student_list")
    return render(request, "students/confirm_delete.html", {"student": student})
