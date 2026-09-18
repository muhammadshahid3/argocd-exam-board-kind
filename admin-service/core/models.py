from django.db import models


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]


def calculate_grade(percentage):
    """Reusable grade calculation logic used across the system."""
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    return "F"


PASS_PERCENTAGE = 50.0


class SchoolClass(models.Model):
    """Represents a class, e.g. 9th, 10th."""
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "school_class"
        ordering = ["name"]
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name


class Section(models.Model):
    """A section belongs to a class, e.g. 9th - A."""
    name = models.CharField(max_length=10)
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name="sections"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "section"
        unique_together = ("name", "school_class")
        ordering = ["school_class__name", "name"]

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"


class Subject(models.Model):
    """A subject belongs to a class and carries a total mark value."""
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name="subjects"
    )
    total_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "subject"
        unique_together = ("name", "school_class")
        ordering = ["school_class__name", "name"]

    def __str__(self):
        return f"{self.name} ({self.school_class.name})"


class Student(models.Model):
    """A student, uniquely identified by roll number."""
    roll_number = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.PROTECT, related_name="students"
    )
    section = models.ForeignKey(
        Section, on_delete=models.PROTECT, related_name="students"
    )
    academic_year = models.CharField(max_length=9, default="2026")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student"
        ordering = ["roll_number"]
        indexes = [
            models.Index(fields=["roll_number"], name="idx_roll_number"),
        ]

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class Result(models.Model):
    """A result header for a student for a given academic year."""
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="results"
    )
    academic_year = models.CharField(max_length=9)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "result"
        unique_together = ("student", "academic_year")
        ordering = ["-academic_year"]

    def __str__(self):
        return f"Result: {self.student.roll_number} ({self.academic_year})"

    @property
    def total_obtained_marks(self):
        return sum(item.obtained_marks for item in self.items.all())

    @property
    def total_marks(self):
        return sum(item.subject.total_marks for item in self.items.all())

    @property
    def percentage(self):
        total = self.total_marks
        if not total:
            return 0.0
        return round((self.total_obtained_marks / total) * 100, 2)

    @property
    def grade(self):
        return calculate_grade(self.percentage)

    @property
    def is_pass(self):
        # Fail overall if any subject is below 33% of that subject's total,
        # or overall percentage is below the pass percentage.
        for item in self.items.all():
            if item.subject.total_marks and (
                item.obtained_marks / item.subject.total_marks
            ) * 100 < 33:
                return False
        return self.percentage >= PASS_PERCENTAGE


class ResultItem(models.Model):
    """A single subject's marks within a result."""
    result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name="items")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="result_items")
    obtained_marks = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "result_item"
        unique_together = ("result", "subject")
        ordering = ["subject__name"]

    def __str__(self):
        return f"{self.result} - {self.subject.name}: {self.obtained_marks}"
