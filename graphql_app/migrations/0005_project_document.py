# Generated by Django 4.2.19 on 2025-02-11 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_app', '0004_alter_project_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to='project_documents/'),
        ),
    ]
