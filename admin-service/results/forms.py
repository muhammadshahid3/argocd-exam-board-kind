from django import forms
from core.models import Student


class SelectStudentForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.select_related("school_class", "section").all(),
        widget=forms.Select(attrs={"class": "form-select", "id": "id_student"}),
        label="Select Student",
    )


class RollNumberLookupForm(forms.Form):
    roll_number = forms.CharField(
        max_length=20,
        label="Enter Roll Number",
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "e.g. 10001",
            "autofocus": "autofocus",
        }),
    )
