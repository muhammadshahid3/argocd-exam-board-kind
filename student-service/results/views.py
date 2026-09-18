from django.shortcuts import render

from .forms import RollNumberForm
from .models import Student, Result


def home(request):
    """Public landing page with the result search form and, on submit, the result."""
    form = RollNumberForm(request.GET or None)
    student = None
    result = None
    not_found = False
    searched = False

    if request.GET.get("roll_number"):
        searched = True
        if form.is_valid():
            roll_number = form.cleaned_data["roll_number"]
            try:
                student = Student.objects.select_related("school_class", "section").get(
                    roll_number=roll_number
                )
                result = (
                    Result.objects.filter(student=student)
                    .order_by("-academic_year")
                    .prefetch_related("items__subject")
                    .first()
                )
                if result is None:
                    not_found = True
                    student = None
            except Student.DoesNotExist:
                not_found = True

    context = {
        "form": form,
        "student": student,
        "result": result,
        "not_found": not_found,
        "searched": searched,
    }
    return render(request, "home.html", context)
