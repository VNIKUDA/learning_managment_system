# Generated by Django 5.1 on 2024-09-27 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_course_color'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='student',
        ),
    ]
