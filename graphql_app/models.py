from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    PRICE_TYPE_CHOICES = [
        ("fixed", "Fixed Price"),
        ("hourly", "Hourly Rate"),
        ("monthly", "Monthly Rate"),
    ]
    STATUS_CHOICES=[
        ("pending", "Pending"), 
        ("in_progress", "In Progress"), 
        ("completed", "Completed")
        ]

    name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    price_type = models.CharField(max_length=15, choices=PRICE_TYPE_CHOICES)
    price = models.FloatField(max_length=10)
    received_date = models.DateField(auto_now_add=True)
    delivery_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    assigned_projects = models.ManyToManyField(Project, through="EmployeeProjectAssignment")

    def __str__(self):
        return self.name

class EmployeeProjectAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="project_assignments")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="employee_assignments")
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        unique_together = ("employee", "project")

    def __str__(self):
        return f"{self.employee.name} - {self.project.name}"