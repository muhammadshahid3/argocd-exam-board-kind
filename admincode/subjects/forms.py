from django import forms
from core.models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "school_class", "total_marks"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Mathematics"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "total_marks": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
        }
