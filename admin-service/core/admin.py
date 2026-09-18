from django.contrib import admin
from .models import SchoolClass, Section, Subject, Student, Result, ResultItem

admin.site.register(SchoolClass)
admin.site.register(Section)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(ResultItem)
