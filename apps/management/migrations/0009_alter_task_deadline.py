# Generated by Django 5.1.4 on 2025-02-07 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_alter_course_students_alter_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.date(2025, 2, 14), null=True, verbose_name='Deadline'),
        ),
    ]
