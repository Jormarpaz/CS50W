# Generated by Django 5.1.5 on 2025-03-16 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Capstone', '0008_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allDay',
            field=models.BooleanField(default=False),
        ),
    ]
