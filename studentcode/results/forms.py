from django import forms


class RollNumberForm(forms.Form):
    roll_number = forms.CharField(
        max_length=20,
        label="Enter your Roll Number",
        error_messages={"required": "Please enter your roll number."},
        widget=forms.TextInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "e.g. 10001",
            "autofocus": "autofocus",
        }),
    )

    def clean_roll_number(self):
        value = self.cleaned_data["roll_number"].strip()
        if not value:
            raise forms.ValidationError("Roll number cannot be empty.")
        return value
