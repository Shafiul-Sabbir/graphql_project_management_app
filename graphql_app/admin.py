from django.contrib import admin
from . models import Client, Employee, Project, EmployeeProjectAssignment
# Register your models here.

admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(EmployeeProjectAssignment)