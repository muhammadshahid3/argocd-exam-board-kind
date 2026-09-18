from django import forms
from core.models import Student, SchoolClass, Section


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "roll_number", "name", "father_name", "date_of_birth",
            "gender", "school_class", "section", "academic_year",
        ]
        widgets = {
            "roll_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 10001"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Student full name"}),
            "father_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Father's name"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "school_class": forms.Select(attrs={"class": "form-select"}),
            "section": forms.Select(attrs={"class": "form-select"}),
            "academic_year": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. 2026"}),
        }

    def clean_roll_number(self):
        roll_number = self.cleaned_data["roll_number"].strip()
        if not roll_number:
            raise forms.ValidationError("Roll number is required.")
        qs = Student.objects.filter(roll_number=roll_number)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This roll number is already assigned to another student.")
        return roll_number

    def clean(self):
        cleaned_data = super().clean()
        school_class = cleaned_data.get("school_class")
        section = cleaned_data.get("section")
        if school_class and section and section.school_class_id != school_class.id:
            raise forms.ValidationError("Selected section does not belong to the selected class.")
        return cleaned_data
