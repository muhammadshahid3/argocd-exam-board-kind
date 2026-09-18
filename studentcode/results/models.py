"""
Read-only mirror models for the Student Result Service.

The Admin Management Service owns the authoritative schema and runs all
migrations. This service shares the SAME PostgreSQL database but declares
these models as `managed = False` so Django never attempts to create,
alter, or migrate these tables here. Table names match exactly what the
admin_service's `core` app creates, so both services read/write the same
underlying data.
"""
from django.db import models


def calculate_grade(percentage):
    """Reusable grade calculation logic (kept in sync with admin_service)."""
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
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "school_class"

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=10)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.DO_NOTHING, related_name="sections")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "section"

    def __str__(self):
        return f"{self.school_class.name} - {self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.DO_NOTHING, related_name="subjects")
    total_marks = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "subject"

    def __str__(self):
        return f"{self.name} ({self.school_class.name})"


class Student(models.Model):
    roll_number = models.CharField(max_length=20, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    father_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.DO_NOTHING, related_name="students")
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING, related_name="students")
    academic_year = models.CharField(max_length=9, default="2026")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "student"

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name="results")
    academic_year = models.CharField(max_length=9)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "result"
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
        for item in self.items.all():
            if item.subject.total_marks and (
                item.obtained_marks / item.subject.total_marks
            ) * 100 < 33:
                return False
        return self.percentage >= PASS_PERCENTAGE


class ResultItem(models.Model):
    result = models.ForeignKey(Result, on_delete=models.DO_NOTHING, related_name="items")
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name="result_items")
    obtained_marks = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "result_item"
        ordering = ["subject__name"]

    def __str__(self):
        return f"{self.result} - {self.subject.name}: {self.obtained_marks}"
