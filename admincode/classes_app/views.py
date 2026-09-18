from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from core.models import SchoolClass
from .forms import SchoolClassForm


@login_required
def class_list(request):
    classes = SchoolClass.objects.all()
    return render(request, "classes/list.html", {"classes": classes})


@login_required
def class_create(request):
    if request.method == "POST":
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class created successfully.")
            return redirect("class_list")
    else:
        form = SchoolClassForm()
    return render(request, "classes/form.html", {"form": form, "title": "Create Class"})


@login_required
def class_update(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == "POST":
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated successfully.")
            return redirect("class_list")
    else:
        form = SchoolClassForm(instance=school_class)
    return render(request, "classes/form.html", {"form": form, "title": "Edit Class"})


@login_required
def class_delete(request, pk):
    school_class = get_object_or_404(SchoolClass, pk=pk)
    if request.method == "POST":
        school_class.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect("class_list")
    return render(request, "classes/confirm_delete.html", {"school_class": school_class})
