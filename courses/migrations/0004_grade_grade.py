# Generated by Django 5.1 on 2024-09-20 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_task_due'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='grade',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
