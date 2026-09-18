from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Student, SchoolClass, Subject, Result


@login_required
def dashboard(request):
    context = {
        "total_students": Student.objects.count(),
        "total_classes": SchoolClass.objects.count(),
        "total_subjects": Subject.objects.count(),
        "total_results": Result.objects.count(),
    }
    return render(request, "dashboard.html", context)
