# Generated by Django 5.1.4 on 2025-02-11 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_alter_course_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='start_datetime',
            field=models.DateField(default=datetime.datetime(2025, 2, 12, 11, 23, 59, 473818), verbose_name='Start datetime'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.date(2025, 2, 18), null=True, verbose_name='Deadline'),
        ),
    ]
