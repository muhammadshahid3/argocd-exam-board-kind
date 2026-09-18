from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from core.models import Student, Subject, Result, ResultItem
from .forms import SelectStudentForm, RollNumberLookupForm


@login_required
def result_list(request):
    results = Result.objects.select_related("student", "student__school_class", "student__section").all()
    return render(request, "results/list.html", {"results": results})


@login_required
def select_student(request):
    """Step 1: pick a student to enter marks for."""
    if request.method == "POST":
        form = SelectStudentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data["student"]
            return redirect("add_result", student_id=student.id)
    else:
        form = SelectStudentForm()
    return render(request, "results/select_student.html", {"form": form})


@login_required
def add_result(request, student_id):
    """Step 2: enter obtained marks for every subject in the student's class."""
    student = get_object_or_404(Student, pk=student_id)
    subjects = Subject.objects.filter(school_class=student.school_class).order_by("name")

    if not subjects.exists():
        messages.warning(request, "No subjects have been configured for this class yet. Please add subjects first.")
        return redirect("subject_create")

    result, _ = Result.objects.get_or_create(
        student=student, academic_year=student.academic_year
    )
    existing_items = {item.subject_id: item.obtained_marks for item in result.items.all()}

    errors = {}
    if request.method == "POST":
        cleaned_marks = {}
        for subject in subjects:
            raw_value = request.POST.get(f"subject_{subject.id}", "").strip()
            try:
                obtained = int(raw_value)
            except (TypeError, ValueError):
                errors[subject.id] = "Enter a valid whole number."
                continue
            if obtained < 0:
                errors[subject.id] = "Marks cannot be negative."
            elif obtained > subject.total_marks:
                errors[subject.id] = f"Cannot exceed total marks ({subject.total_marks})."
            else:
                cleaned_marks[subject.id] = obtained

        if not errors:
            with transaction.atomic():
                for subject in subjects:
                    ResultItem.objects.update_or_create(
                        result=result,
                        subject=subject,
                        defaults={"obtained_marks": cleaned_marks[subject.id]},
                    )
            messages.success(request, f"Result saved successfully for {student.name} ({student.roll_number}).")
            return redirect("result_list")
        else:
            existing_items.update(cleaned_marks)
            messages.error(request, "Please correct the errors below.")

    subject_rows = [
        {
            "subject": subject,
            "value": existing_items.get(subject.id, ""),
            "error": errors.get(subject.id),
        }
        for subject in subjects
    ]

    return render(request, "results/add_result.html", {
        "student": student,
        "subject_rows": subject_rows,
    })


@login_required
def final_result(request):
    """Admin can look up any student's full computed result, same as the public page."""
    form = RollNumberLookupForm(request.GET or None)
    result = None
    student = None
    not_found = False

    if request.GET.get("roll_number"):
        if form.is_valid():
            roll_number = form.cleaned_data["roll_number"].strip()
            try:
                student = Student.objects.select_related("school_class", "section").get(
                    roll_number=roll_number
                )
                result = Result.objects.filter(student=student).order_by("-academic_year").first()
                if result is None:
                    not_found = True
            except Student.DoesNotExist:
                not_found = True

    return render(request, "results/final_result.html", {
        "form": form,
        "student": student,
        "result": result,
        "not_found": not_found,
    })
