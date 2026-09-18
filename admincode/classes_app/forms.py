from django import forms
from core.models import SchoolClass


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 9th"}),
        }
