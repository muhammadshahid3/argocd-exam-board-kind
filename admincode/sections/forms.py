from django import forms
from core.models import Section


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ["name", "school_class"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. A"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
        }
