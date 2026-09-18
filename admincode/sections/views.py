from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Section
from .forms import SectionForm


@login_required
def section_list(request):
    sections = Section.objects.select_related("school_class").all()
    return render(request, "sections/list.html", {"sections": sections})


@login_required
def section_create(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Section created successfully.")
            return redirect("section_list")
    else:
        form = SectionForm()
    return render(request, "sections/form.html", {"form": form, "title": "Create Section"})


@login_required
def section_update(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        form = SectionForm(request.POST, instance=section)
        if form.is_valid():
            form.save()
            messages.success(request, "Section updated successfully.")
            return redirect("section_list")
    else:
        form = SectionForm(instance=section)
    return render(request, "sections/form.html", {"form": form, "title": "Edit Section"})


@login_required
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == "POST":
        section.delete()
        messages.success(request, "Section deleted successfully.")
        return redirect("section_list")
    return render(request, "sections/confirm_delete.html", {"section": section})
