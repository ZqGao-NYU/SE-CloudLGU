# Generated by Django 3.2.5 on 2022-04-17 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OfficeHour', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='otEndTime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='otStartTime',
            field=models.TimeField(),
        ),
    ]
