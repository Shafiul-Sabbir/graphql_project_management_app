# Generated by Django 4.2.19 on 2025-02-06 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='assigned_projects',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='start_date',
        ),
        migrations.CreateModel(
            name='EmployeeProjectAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_assignments', to='graphql_app.employee')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_assignments', to='graphql_app.project')),
            ],
            options={
                'unique_together': {('employee', 'project')},
            },
        ),
    ]
