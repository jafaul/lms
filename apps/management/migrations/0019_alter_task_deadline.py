# Generated by Django 5.1.6 on 2025-02-15 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("management", "0018_alter_task_deadline"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="deadline",
            field=models.DateField(
                blank=True,
                default=datetime.date(2025, 2, 22),
                null=True,
                verbose_name="Deadline",
            ),
        ),
    ]
