from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Subject
from .forms import SubjectForm


@login_required
def subject_list(request):
    subjects = Subject.objects.select_related("school_class").all()
    return render(request, "subjects/list.html", {"subjects": subjects})


@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject added successfully.")
            return redirect("subject_list")
    else:
        form = SubjectForm()
    return render(request, "subjects/form.html", {"form": form, "title": "Add Subject"})


@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect("subject_list")
    else:
        form = SubjectForm(instance=subject)
    return render(request, "subjects/form.html", {"form": form, "title": "Edit Subject"})


@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect("subject_list")
    return render(request, "subjects/confirm_delete.html", {"subject": subject})
